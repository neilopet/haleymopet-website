#!/usr/bin/env python3

import asyncio
import json
import sys
import os
from datetime import datetime
from playwright.async_api import async_playwright
import requests


BOOK_URL = "https://www.goodreads.com/book/show/243765865-a-bloodveiled-descent"
GRAPHQL_ENDPOINT = "appsync-api.us-east-1.amazonaws.com/graphql"


async def scrape_goodreads_reviews():
    """
    Scrape 5-star reviews from Goodreads by intercepting the AppSync GraphQL
    responses that load when browsing the reviews page.
    """
    reviews_data = []
    captured_responses = []

    async with async_playwright() as p:
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

        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='en-US',
            timezone_id='America/New_York',
            permissions=['geolocation']
        )

        # Add stealth scripts
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
            });
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: 'granted' }) :
                    originalQuery(parameters)
            );
        """)

        page = await context.new_page()

        async def on_response(response):
            if GRAPHQL_ENDPOINT in response.url:
                try:
                    body = await response.text()
                    data = json.loads(body)
                    captured_responses.append(data)
                except Exception:
                    pass

        page.on("response", on_response)

        try:
            print(f"Navigating to Goodreads book page...")
            await page.goto(BOOK_URL, wait_until='domcontentloaded', timeout=60000)

            # Wait for initial page load
            await page.wait_for_timeout(3000)

            print("Clicking 5-star filter...")
            try:
                # Click the 5-star histogram bar to filter reviews
                await page.click('[data-testid="ratingBar-5"]', timeout=10000)
                print("Clicked 5-star filter")
            except Exception as e:
                print(f"Could not click 5-star filter bar: {e}")
                # Try alternative selector
                try:
                    await page.click('text="5 stars"', timeout=5000)
                    print("Clicked 5-star filter (alternative selector)")
                except Exception:
                    print("Trying to find star filter via histogram bars...")
                    try:
                        # The first bar in the histogram is typically 5 stars
                        bars = await page.query_selector_all('.RatingsHistogram__bar')
                        if bars:
                            await bars[0].click()
                            print("Clicked first histogram bar")
                    except Exception as e2:
                        print(f"All filter attempts failed: {e2}")

            # Wait for filtered reviews to load
            await page.wait_for_timeout(5000)

            # Try to load more reviews by scrolling and clicking "Show more"
            for page_num in range(3):
                try:
                    show_more = await page.query_selector('button:has-text("Show more reviews")')
                    if not show_more:
                        show_more = await page.query_selector('[data-testid="loadMore"]')
                    if show_more:
                        await show_more.click()
                        print(f"Clicked 'Show more' (page {page_num + 2})")
                        await page.wait_for_timeout(3000)
                    else:
                        break
                except Exception:
                    break

            # Extract reviews from captured GraphQL responses
            print(f"\nCaptured {len(captured_responses)} GraphQL responses")
            reviews_data = extract_reviews_from_responses(captured_responses)

            if not reviews_data:
                print("No reviews found in GraphQL responses, trying DOM extraction...")
                reviews_data = await extract_reviews_from_dom(page)

        except Exception as e:
            print(f"Error during scraping: {e}")

        finally:
            await browser.close()

    return reviews_data


def extract_reviews_from_responses(responses):
    """Extract review data from captured GraphQL responses."""
    reviews = []
    seen_ids = set()

    for response_data in responses:
        try:
            # Navigate the GraphQL response structure
            data = response_data.get('data', {})

            # Try getReviews response format
            get_reviews = data.get('getReviews', {})
            edges = get_reviews.get('edges', [])

            if not edges:
                # Try alternative response structures
                for key, value in data.items():
                    if isinstance(value, dict) and 'edges' in value:
                        edges = value.get('edges', [])
                        if edges:
                            break

            for edge in edges:
                node = edge.get('node', edge)
                rating = node.get('rating', 0)

                # Only include 5-star reviews
                if rating != 5:
                    continue

                review_text = node.get('text', '')
                if not review_text:
                    continue

                # Generate a unique ID to avoid duplicates
                review_id = node.get('id', review_text[:50])
                if review_id in seen_ids:
                    continue
                seen_ids.add(review_id)

                creator = node.get('creator', {})
                shelving = node.get('shelving', {})
                created_at = node.get('createdAt', '')

                # Format date
                date_str = ''
                if created_at:
                    try:
                        # Handle epoch milliseconds (numeric)
                        if isinstance(created_at, (int, float)):
                            dt = datetime.fromtimestamp(created_at / 1000)
                            date_str = dt.strftime('%B %d, %Y')
                        else:
                            dt = datetime.fromisoformat(str(created_at).replace('Z', '+00:00'))
                            date_str = dt.strftime('%B %d, %Y')
                    except Exception:
                        date_str = str(created_at)

                review = {
                    'reviewer_name': creator.get('name', 'Anonymous'),
                    'reviewer_image_url': creator.get('imageUrlSquare', ''),
                    'reviewer_url': '',
                    'rating': rating,
                    'text': review_text,
                    'date': date_str,
                    'review_url': shelving.get('webUrl', '')
                }

                reviews.append(review)
                print(f"  Found 5-star review by {review['reviewer_name']}")

        except Exception as e:
            print(f"  Error parsing response: {e}")
            continue

    return reviews


async def extract_reviews_from_dom(page):
    """Fallback: extract reviews directly from the page DOM."""
    reviews = []

    try:
        review_cards = await page.query_selector_all('[data-testid="review"]')
        if not review_cards:
            review_cards = await page.query_selector_all('.ReviewCard')
        if not review_cards:
            review_cards = await page.query_selector_all('[itemprop="review"]')

        print(f"Found {len(review_cards)} review cards in DOM")

        for i, card in enumerate(review_cards):
            try:
                # Check star rating
                stars = await card.query_selector_all('.RatingStar--small[aria-label="Rating 5 out of 5"]')
                if not stars:
                    # Try counting filled stars
                    filled_stars = await card.query_selector_all('.RatingStar--fill')
                    if len(filled_stars) != 5:
                        continue

                # Get review text
                text_el = await card.query_selector('[data-testid="contentContainer"]')
                if not text_el:
                    text_el = await card.query_selector('.ReviewText__content')
                if not text_el:
                    text_el = await card.query_selector('.Formatted')

                text = await text_el.inner_text() if text_el else ''
                if not text:
                    continue

                # Get reviewer name
                name_el = await card.query_selector('[data-testid="name"]')
                if not name_el:
                    name_el = await card.query_selector('.ReviewerProfile__name')
                name = await name_el.inner_text() if name_el else 'Anonymous'

                # Get reviewer image
                img_el = await card.query_selector('img[data-testid="avatar"]')
                if not img_el:
                    img_el = await card.query_selector('.ReviewerProfile__avatar img')
                img_url = await img_el.get_attribute('src') if img_el else ''

                # Get reviewer profile URL
                profile_el = await card.query_selector('a[data-testid="name"]')
                if not profile_el:
                    profile_el = await card.query_selector('.ReviewerProfile__name a')
                profile_url = await profile_el.get_attribute('href') if profile_el else ''
                if profile_url and not profile_url.startswith('http'):
                    profile_url = f"https://www.goodreads.com{profile_url}"

                # Get date
                date_el = await card.query_selector('[data-testid="reviewDate"]')
                if not date_el:
                    date_el = await card.query_selector('.ReviewCard__date')
                date_str = await date_el.inner_text() if date_el else ''

                review = {
                    'reviewer_name': name.strip(),
                    'reviewer_image_url': img_url,
                    'reviewer_url': profile_url,
                    'rating': 5,
                    'text': text.strip(),
                    'date': date_str.strip(),
                    'review_url': ''
                }

                reviews.append(review)
                print(f"  Found 5-star review by {review['reviewer_name']} (DOM)")

            except Exception as e:
                print(f"  Error parsing review card {i}: {e}")
                continue

    except Exception as e:
        print(f"Error in DOM extraction: {e}")

    return reviews


def download_reviewer_image(image_url, index):
    """Download reviewer profile picture and save locally."""
    if not image_url:
        return ''

    try:
        os.makedirs('images/reviewers', exist_ok=True)

        filename = f"reviewer-{index}.jpg"
        filepath = f"images/reviewers/{filename}"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(image_url, headers=headers, timeout=15)
        response.raise_for_status()

        with open(filepath, 'wb') as f:
            f.write(response.content)

        print(f"  Downloaded reviewer image: {filepath}")
        return filepath

    except Exception as e:
        print(f"  Error downloading reviewer image: {e}")
        return ''


async def main():
    """Main function to run the scraper."""
    try:
        print("Starting Goodreads review scraper...")
        reviews = await scrape_goodreads_reviews()

        if not reviews:
            print("No 5-star reviews found")
            sys.exit(1)

        print(f"\nFound {len(reviews)} five-star reviews")

        # Download reviewer images and finalize data
        output = []
        for i, review in enumerate(reviews, 1):
            local_image = download_reviewer_image(review.get('reviewer_image_url', ''), i)

            output.append({
                'reviewer_name': review['reviewer_name'],
                'reviewer_image': local_image,
                'reviewer_url': review.get('reviewer_url', ''),
                'rating': review['rating'],
                'text': review['text'],
                'date': review.get('date', ''),
                'review_url': review.get('review_url', '')
            })

        # Write to JSON file
        with open('goodreads_reviews.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        print(f"\nData saved to goodreads_reviews.json")

        # Print summary
        for i, review in enumerate(output, 1):
            print(f"\nReview {i}:")
            print(f"  Reviewer: {review['reviewer_name']}")
            print(f"  Date: {review['date']}")
            print(f"  Text: {review['text'][:100]}...")

    except Exception as e:
        print(f"Script failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
