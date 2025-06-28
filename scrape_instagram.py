#!/usr/bin/env python3

import asyncio
import json
import sys
import re
import os
from datetime import datetime
from playwright.async_api import async_playwright
import requests
from urllib.parse import urljoin

async def scrape_instagram_posts(username="haleym.opet", num_posts=3):
    """
    Scrape Instagram posts using Playwright with stealth configuration
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
                    Promise.resolve({ state: Cypress.env('NOTIFICATION_PERMISSION') || 'granted' }) :
                    originalQuery(parameters)
            );
        """)
        
        page = await context.new_page()
        
        try:
            print(f"Navigating to Instagram profile: {username}")
            await page.goto(f'https://www.instagram.com/{username}/', wait_until='networkidle')
            
            # Wait for posts to load
            print("Waiting for posts to load...")
            await page.wait_for_selector('a[href*="/p/"]', timeout=15000)
            
            # Find all post links matching the pattern
            post_links = await page.locator('a[href*="/haleym.opet/p/"]').all()
            print(f"Found {len(post_links)} post links")
            
            for i, link_element in enumerate(post_links[:num_posts]):
                try:
                    print(f"Processing post {i+1}/{num_posts}")
                    
                    # Extract post URL
                    post_href = await link_element.get_attribute('href')
                    if not post_href:
                        continue
                    
                    post_url = urljoin('https://www.instagram.com', post_href)
                    print(f"Post URL: {post_url}")
                    
                    # Find the image within this link
                    img_element = link_element.locator('img').first
                    img_src = await img_element.get_attribute('src')
                    img_alt = await img_element.get_attribute('alt')
                    
                    if not img_src:
                        print(f"No image found for post {i+1}")
                        continue
                    
                    print(f"Image URL: {img_src}")
                    
                    # Download and save image locally
                    local_image_path = download_image(img_src, post_url, i+1)
                    
                    # Get image metadata via HTTP request
                    image_date = get_image_metadata(img_src)
                    
                    # Find the description text
                    # Based on your HTML structure, the description is in a sibling div
                    parent_container = link_element.locator('xpath=..')
                    description_element = parent_container.locator('div.x1s85apg span').first
                    description = ""
                    
                    if await description_element.count() > 0:
                        description = await description_element.text_content()
                        description = description.strip() if description else ""
                    
                    print(f"Description: {description[:100]}...")
                    
                    # Format for blog post structure (no title needed as per requirements)
                    post_data = {
                        "date": image_date,
                        "excerpt": description[:200] + "..." if len(description) > 200 else description,
                        "image": local_image_path if local_image_path else img_src,
                        "link": post_url,
                        "content": description
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
        
        print(f"Downloading image to: {filepath}")
        
        # Download the image
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(image_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Save the image
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        print(f"Successfully downloaded image: {filepath}")
        return filepath
        
    except Exception as e:
        print(f"Error downloading image: {e}")
        return None

def get_image_metadata(image_url):
    """
    Get Last-Modified header from image URL
    """
    try:
        print(f"Getting metadata for image: {image_url}")
        response = requests.head(image_url, timeout=10)
        
        if 'Last-Modified' in response.headers:
            last_modified = response.headers['Last-Modified']
            # Parse the date and format it
            try:
                date_obj = datetime.strptime(last_modified, '%a, %d %b %Y %H:%M:%S %Z')
                return date_obj.strftime('%B %d, %Y')
            except:
                return datetime.now().strftime('%B %d, %Y')
        else:
            return datetime.now().strftime('%B %d, %Y')
            
    except Exception as e:
        print(f"Error getting image metadata: {e}")
        return datetime.now().strftime('%B %d, %Y')

async def main():
    """
    Main function to run the scraper
    """
    try:
        print("Starting Instagram scraper...")
        posts = await scrape_instagram_posts()
        
        if posts:
            print(f"Successfully scraped {len(posts)} posts")
            
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