# Instagram Scraper Setup

This setup allows your GitHub Pages website to automatically display your latest Instagram posts by scraping them and storing the data in a JSON file.

## How It Works

1. **Playwright Scraper** (`scrape_instagram.py`) - Uses stealth configuration to scrape Instagram posts
2. **GitHub Actions** (`.github/workflows/update-instagram.yml`) - Runs the scraper automatically  
3. **JSON Data** (`instagram_posts.json`) - Stores the scraped post data
4. **JavaScript Loader** (`instagram_loader.js`) - Loads the data into your website

## Setup Instructions

### 1. Install Dependencies (Local Testing)

```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. Test the Scraper Locally

```bash
python test_scraper.py
```

This will test with 1 post to verify everything works.

### 3. Run Full Scraper

```bash
python scrape_instagram.py
```

This creates `instagram_posts.json` with your latest 3 posts.

### 4. Update Your Website

Add this to your `index.html` before the closing `</body>` tag:

```html
<script src="instagram_loader.js"></script>
```

The script will automatically replace your static blog posts with Instagram content.

### 5. Enable GitHub Actions

The workflow is set to run **manually only** to avoid circular deployments.

To trigger manually:
1. Go to your repo on GitHub
2. Click "Actions" tab
3. Click "Update Instagram Posts"  
4. Click "Run workflow"
5. The workflow will scrape Instagram and commit new posts/images
6. GitHub Pages will automatically rebuild with the new content

## JSON Data Format

The scraper outputs data in this format:

```json
[
  {
    "date": "June 27, 2025",
    "excerpt": "COVER DESIGN REVEAL! I am absolutely in LOVE...",
    "image": "https://instagram.fagc1-1.fna.fbcdn.net/...",
    "link": "https://www.instagram.com/p/DLaJKKbOOXd/",
    "content": "Full post content..."
  }
]
```

## Stealth Features

The scraper uses several techniques to avoid detection:
- Realistic browser fingerprinting
- Human-like user agent
- Proper viewport and locale settings
- Anti-detection scripts

## Error Handling

- If scraping fails, your static blog posts remain visible
- The GitHub Action will only commit if data successfully changes
- Console logs show detailed error information

## Maintenance

- Monitor GitHub Actions for failures
- Instagram may change their HTML structure, requiring scraper updates
- Consider the daily run frequency based on your posting schedule

## Files Created

- `instagram_posts.json` - The scraped data (auto-generated)
- `scrape_instagram.py` - Main scraper script
- `test_scraper.py` - Local testing script
- `instagram_loader.js` - Website integration script
- `requirements.txt` - Python dependencies
- `.github/workflows/update-instagram.yml` - Automation workflow