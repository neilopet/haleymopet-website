# haleymopet-website - Development Context

## Project Overview
Author website for Haley M. Opet, promoting her debut novel "A Bloodveiled Descent" (The Solwyn Duology, Book One). Features book promotion, newsletter signup, Instagram integration, and author information.

## Domain & Hosting
- **Domain**: haleymopet.com (registered at iwantmyname.com)
- **Hosting**: GitHub Pages (free static hosting)
- **Repository**: github.com/neilopet/haleymopet-website
- **DNS**: A records pointing to GitHub Pages IPs, CNAME www → neilopet.github.io

## Technology Stack
- **Frontend**: Vanilla HTML, CSS, JavaScript (no framework)
- **Newsletter**: HubSpot Forms integration (Portal ID: 242278621)
- **Analytics**: Google Analytics 4 with consent management
- **Social Integration**: Instagram scraper with local image hosting
- **Build Process**: GitHub Actions injects GA4 ID during deployment
- **CI/CD**: GitHub Actions for deployments and Instagram updates

## Key Features

### 1. Instagram Integration (NEW June 2025)
- **Scraper**: `scrape_instagram.py` uses Playwright with stealth config
- **Local Images**: Downloads Instagram images to avoid CORS issues
- **Data Format**: JSON file with blog post structure
- **Frontend**: `instagram_loader.js` dynamically loads posts
- **Automation**: Manual GitHub Action workflow (avoids circular deploys)

### 2. Newsletter Signup
- **Provider**: HubSpot Forms
- **Form ID**: bd03cd07-1971-48b5-8a2e-d06fb0888fd5
- **Portal ID**: 242278621
- **Location**: Subscribe section near footer
- **Tracking**: Form submissions tracked as `generate_lead` events

### 3. Book Promotion
- **Book**: "A Bloodveiled Descent" by Haley M. Opet
- **Release**: November 10, 2025
- **Pre-order**: Amazon Kindle link with conversion tracking
- **Cover**: Local image at `images/ABloodveiledDescent-Ebook.jpg`
- **Tracking**: Pre-order clicks tracked as `purchase_intent` events

### 4. Analytics & Privacy (NEW June 2025)
- **Platform**: Google Analytics 4 (Measurement ID: G-S2C5TDLRZZ)
- **Implementation**: Consent-based loading via cookie banner
- **Privacy**: GDPR/CCPA compliant with explicit opt-in
- **Tracking**: Pre-orders, newsletter signups, social clicks
- **Privacy Policy**: Available at `/privacy-policy.html`

## Project Structure
```
/
├── index.html                    # Main website (single page)
├── privacy-policy.html          # Privacy policy page
├── CNAME                        # GitHub Pages domain config
├── README.md                    # Basic project info
├── CLAUDE.md                    # This file - dev context
├── GOODREADS.md                 # Goodreads submission guide
├── INSTAGRAM_SCRAPER.md         # Instagram integration docs
├── ANALYTICS_SETUP.md           # GA4 setup instructions
├── images/
│   ├── ABloodveiledDescent-Ebook.jpg
│   ├── haley-headshot-400.jpg
│   ├── velvet-tea-press-logo-transparent.png
│   └── instagram/              # Scraped Instagram images
├── instagram_posts.json         # Instagram data cache
├── instagram_loader.js          # Frontend Instagram loader
├── scrape_instagram.py          # Instagram scraper script
├── requirements.txt             # Python dependencies
└── .github/workflows/
    ├── deploy.yml              # Deployment with GA4 injection
    └── update-instagram.yml     # Manual Instagram update
```

## Recent Changes (June 2025)

### Instagram Integration
- Replaced static blog posts with dynamic Instagram feed
- Scrapes @haleym.opet Instagram account
- Downloads images locally to solve CORS issues
- Manual GitHub Action to avoid deployment loops
- Maintains responsive design across devices

### Analytics & Privacy Implementation
- Added Google Analytics 4 with conversion tracking
- Implemented GDPR-compliant cookie consent banner
- Created privacy policy page
- Consent-based analytics loading (no tracking without permission)
- Tracks pre-order clicks, newsletter signups, social engagement

### UI/UX Improvements
- Book cover prominently displayed (Goodreads requirement)
- Author name standardized to "Haley M. Opet"
- Pre-order buttons in hero and featured sections
- Floating header with scroll effects
- Max-width containers for readability
- Footer uses transparent logo

### Infrastructure
- GitHub Actions deployment workflow with GA4 injection
- Playwright-based Instagram scraping with stealth
- Local image hosting strategy
- JSON-based data storage
- Environment variable support for secure credentials

## Development Guidelines

### Testing
- Use `python3 test_instagram_loader.py` for local testing
- Screenshots: `python3 capture_screenshot.py`
- Always verify HubSpot form loads properly
- Test on multiple screen sizes

### Git Workflow
- Main branch deploys to production via GitHub Actions
- Deployment workflow injects GA4 ID from repository secrets
- Use descriptive commit messages
- Include co-author credit for AI assistance

### Instagram Updates
1. Go to GitHub Actions tab
2. Run "Update Instagram Posts" manually
3. Scraper fetches latest 3 posts
4. Images downloaded to `images/instagram/`
5. JSON data updated
6. Commits and pushes automatically

### Common Tasks

#### Update Instagram Content
```bash
python3 scrape_instagram.py  # Local test
# OR use GitHub Actions UI for production
```

#### Test Website Locally
```bash
python3 -m http.server 8080
# Browse to http://localhost:8080
```

#### Capture Screenshots
```bash
python3 capture_screenshot.py  # Various devices
python3 test_instagram_loader.py  # With server
```

#### Configure Analytics
1. Set `GA4_MEASUREMENT_ID` in GitHub repository secrets
2. Push changes to trigger deployment
3. Verify in GA4 real-time reports

## Important Notes

### Security
- No API keys in repository
- GA4 Measurement ID injected during deployment
- Instagram scraping uses public data only
- HubSpot form loaded client-side
- All secrets in GitHub Actions environment variables

### Performance
- Static site - very fast
- Images optimized for web
- No JavaScript frameworks
- Minimal external dependencies

### SEO Considerations
- Single page site
- Meta description present
- Semantic HTML structure
- Mobile responsive design

### Known Issues
- Instagram scraping can break if UI changes
- Manual updates required for fresh content
- Single page limits SEO potential
- Analytics blocked by ad blockers (20-30% of users)

## Contact & Support
- **Author**: Haley M. Opet
- **Developer**: Neil Opet (neilopet)
- **Publisher**: Velvet Tea Press
- **Website Issues**: Create GitHub issue

## Future Considerations
- Link Google Search Console for SEO insights
- Implement blog/news section
- Add book retailer links beyond Amazon
- Consider static site generator for scalability
- Add schema.org metadata for books
- Implement automated Instagram updates (carefully)
- Add A/B testing for conversion optimization

---
Last Updated: June 28, 2025