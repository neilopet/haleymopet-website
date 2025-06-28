# Website Analytics Setup Guide

## Google Analytics 4 Configuration

### Step 1: Create GA4 Property
1. Go to [Google Analytics](https://analytics.google.com/)
2. Create a new GA4 property for `haleymopet.com`
3. Copy the **Measurement ID** (format: G-XXXXXXXXXX)

### Step 2: Configure GitHub Repository Secrets
1. Go to your GitHub repository: `neilopet/haleymopet-website`
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add the following secret:
   - **Name**: `GA4_MEASUREMENT_ID`
   - **Value**: Your GA4 Measurement ID (e.g., `G-ABC123DEF4`)

### Step 3: Enable GitHub Pages with Actions
1. Go to **Settings** → **Pages**
2. Under **Source**, select **GitHub Actions**
3. The new deployment workflow will automatically inject your GA4 ID

### Step 4: Configure Google Search Console
1. Go to [Google Search Console](https://search.google.com/search-console)
2. Add `haleymopet.com` as a property
3. Verify ownership using the GA4 verification method
4. Link Search Console to your GA4 property

## What This Gives You

### Marketing Insights
- **Traffic Sources**: Organic search, social media, direct visits, referrals
- **User Demographics**: Age, gender, interests, location data
- **Campaign Attribution**: Which channels drive the most engagement
- **Content Performance**: Most viewed pages, bounce rates, time on site

### Revenue Tracking
- **Pre-order Conversions**: Tracks clicks on Amazon pre-order buttons
  - Hero section vs featured section performance
  - Conversion rates by traffic source
- **Funnel Analysis**: User journey from landing to pre-order
- **Value Attribution**: Revenue attribution by marketing channel

### SEO Performance
- **Organic Traffic**: Search engine visibility and performance
- **Search Queries**: What keywords users find you with
- **Page Rankings**: Track improvement in search results
- **Technical Issues**: Core Web Vitals, mobile usability

### User Behavior
- **Newsletter Signups**: Lead generation tracking
- **Social Media Clicks**: Instagram, TikTok, Threads engagement
- **Content Engagement**: Scroll depth, reading time
- **Device/Browser**: User technology preferences

## Key Reports You Can Generate

### Monthly Business Reports
1. **Traffic Overview**: Sessions, users, page views
2. **Conversion Summary**: Pre-order clicks, newsletter signups
3. **Top Content**: Most engaging blog posts/Instagram content
4. **Mobile Performance**: Mobile vs desktop engagement

### Marketing Campaign Analysis
1. **Social Media ROI**: Which platforms drive most pre-orders
2. **Content Marketing**: Instagram post engagement correlation
3. **SEO Progress**: Organic growth month-over-month
4. **User Acquisition**: Cost per acquisition by channel

### Revenue Insights
1. **Pre-order Funnel**: Drop-off points in conversion process
2. **Geographic Performance**: Best-performing regions
3. **Device-based Conversions**: Mobile vs desktop purchasing behavior
4. **Seasonal Trends**: Launch timeline impact analysis

## Dashboard Access
- **Google Analytics**: Real-time and historical data
- **Google Search Console**: SEO performance metrics
- **Combined Reports**: Cross-platform insights for comprehensive analysis

## Next Steps After Setup
1. Let analytics collect data for 2-3 weeks
2. Set up custom audiences for retargeting
3. Create conversion goals and funnels
4. Set up automated email reports for stakeholders

This comprehensive setup provides the data foundation needed to answer all business questions from Marketing, SEO, Revenue, and Operations teams.