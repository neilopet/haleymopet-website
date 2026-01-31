#!/usr/bin/env python3

import asyncio
import json
import sys
import os
from datetime import datetime
from playwright.async_api import async_playwright
import requests


async def scrape_instagram_posts(username="haleym.opet", num_posts=3):
    """
    Scrape Instagram posts by intercepting the web_profile_info API response
    that Instagram makes when loading a profile page. This gives us accurate
    timestamps, captions, and high-res image URLs without needing to visit
    individual post pages (which require login).
    """
    posts_data = []

    async with async_playwright() as p:
        # Launch browser with stealth configuration
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--no-first-run',
                '--no-zygote',
                '--disable-gpu',
                '--disable-background-timer-throttling',
                '--disable-backgrounding-occluded-windows',
                '--disable-renderer-backgrounding',
                '--disable-features=TranslateUI',
                '--disable-ipc-flooding-protection',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor'
            ]
        )

        # Create context with stealth settings
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='en-US',
            timezone_id='America/New_York',
            permissions=['geolocation']
        )

        # Add stealth scripts
        await context.add_init_script("""
            // Remove webdriver property
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });

            // Mock plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });

            // Mock languages
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
            });

            // Mock permissions
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: 'granted' }) :
                    originalQuery(parameters)
            );
        """)

        page = await context.new_page()

        # Listen for the web_profile_info API response
        profile_info = None

        async def on_response(response):
            nonlocal profile_info
            if 'web_profile_info' in response.url:
                try:
                    body = await response.text()
                    profile_info = json.loads(body)
                except Exception:
                    pass

        page.on("response", on_response)

        try:
            print(f"Navigating to Instagram profile: {username}")
            await page.goto(f'https://www.instagram.com/{username}/', wait_until='networkidle')

            # Wait for the API response to be captured
            for _ in range(10):
                if profile_info:
                    break
                await page.wait_for_timeout(500)

            if not profile_info:
                print("Failed to capture web_profile_info API response")
                return posts_data

            # Extract media edges from the API response
            user = profile_info.get('data', {}).get('user', {})
            media = user.get('edge_owner_to_timeline_media', {})
            edges = media.get('edges', [])

            print(f"Found {len(edges)} posts in API response")

            # Skip posts without captions (e.g. pinned banner images)
            edges = [e for e in edges
                     if e.get('node', {}).get('edge_media_to_caption', {}).get('edges')]

            for i, edge in enumerate(edges[:num_posts]):
                try:
                    node = edge.get('node', {})
                    shortcode = node.get('shortcode', '')
                    post_url = f"https://www.instagram.com/p/{shortcode}/"

                    print(f"\nProcessing post {i+1}/{num_posts} (shortcode: {shortcode})")

                    # Extract caption
                    caption = ""
                    caption_edges = node.get('edge_media_to_caption', {}).get('edges', [])
                    if caption_edges:
                        caption = caption_edges[0].get('node', {}).get('text', '')

                    # Extract date from taken_at_timestamp
                    taken_at = node.get('taken_at_timestamp', 0)
                    if taken_at:
                        date_str = datetime.fromtimestamp(int(taken_at)).strftime('%B %d, %Y')
                    else:
                        date_str = datetime.now().strftime('%B %d, %Y')

                    # Extract high-res image URL
                    display_url = node.get('display_url', '')

                    print(f"  Date: {date_str}")
                    print(f"  Caption: {caption[:80]}..." if caption else "  Caption: (none)")

                    # Download the image
                    if not display_url:
                        print(f"  No image URL for post {i+1}, skipping")
                        continue

                    local_image_path = download_image(display_url, post_url, i + 1)

                    post_data = {
                        "date": date_str,
                        "excerpt": caption[:200] + "..." if len(caption) > 200 else caption,
                        "image": local_image_path if local_image_path else display_url,
                        "link": post_url,
                        "content": caption
                    }

                    posts_data.append(post_data)
                    print(f"Successfully processed post {i+1}")

                except Exception as e:
                    print(f"Error processing post {i+1}: {e}")
                    continue

        except Exception as e:
            print(f"Error during scraping: {e}")

        finally:
            await browser.close()

    return posts_data


def download_image(image_url, post_url, post_number):
    """
    Download Instagram image and save locally
    """
    try:
        # Create images directory if it doesn't exist
        os.makedirs('images/instagram', exist_ok=True)

        # Extract post ID from URL for filename
        post_id = post_url.split('/p/')[-1].rstrip('/')
        filename = f"instagram-post-{post_number}-{post_id}.jpg"
        filepath = f"images/instagram/{filename}"

        print(f"  Downloading image to: {filepath}")

        # Download the image
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(image_url, headers=headers, timeout=15)
        response.raise_for_status()

        # Save the image
        with open(filepath, 'wb') as f:
            f.write(response.content)

        print(f"  Successfully downloaded image: {filepath}")
        return filepath

    except Exception as e:
        print(f"  Error downloading image: {e}")
        return None


async def main():
    """
    Main function to run the scraper
    """
    try:
        print("Starting Instagram scraper...")
        posts = await scrape_instagram_posts()

        if posts:
            print(f"\nSuccessfully scraped {len(posts)} posts")

            # Write to JSON file
            with open('instagram_posts.json', 'w', encoding='utf-8') as f:
                json.dump(posts, f, indent=2, ensure_ascii=False)

            print("Data saved to instagram_posts.json")

            # Print summary
            for i, post in enumerate(posts, 1):
                print(f"\nPost {i}:")
                print(f"  Date: {post['date']}")
                print(f"  URL: {post['link']}")
                print(f"  Excerpt: {post['excerpt'][:100]}...")
        else:
            print("No posts found or all posts failed to process")
            sys.exit(1)

    except Exception as e:
        print(f"Script failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
