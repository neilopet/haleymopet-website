# A Bloodveiled Descent - Website Implementation Plan
## Book Launch Updates - Phased Approach

---

## 🚀 Phase 1: NOW
**Priority: Immediate Revenue & Core Functionality**
*Deploy these changes first to maximize sales opportunities*

### Purchase Options & Retailers

#### #1 - Add Amazon Paperback Button
- Add button for paperback version using ASIN `B0FT2PFQTF`
- Place alongside existing Kindle button
- Use same Amazon orange styling
- Text: "GET PAPERBACK ON AMAZON"

#### #2 - Add Barnes & Noble Button
- URL: `https://www.barnesandnoble.com/w/a-bloodveiled-descent-haley-m-opet/1148562497`
- Create green-themed button style for B&N branding
- Text: "GET IT AT BARNES & NOBLE"

#### #3 - Add Books-a-Million Button  
- URL: `https://www.booksamillion.com/p/Bloodveiled-Descent/Haley-M-Opet/9798999176905`
- Create red/burgundy themed button style
- Text: "GET IT AT BOOKS-A-MILLION"

#### #4 - Update Release Text
- Change: "Now available on Amazon Kindle!"
- To: "Now available in Kindle and Paperback at major retailers!"

### Format Information

#### #5 - Add Format Badges
- Display available formats clearly:
  - ✅ Kindle Available
  - ✅ Paperback Available
  - 🎧 Audiobook Coming Soon

#### #6 - Create Formats Section
- Add small section in featured book area
- Show all available and upcoming formats
- Keep it concise and scannable

### Layout & Organization

#### #7 - Reorganize Purchase Buttons
- Implement grid layout (2x2 or 3-column)
- Ensure clean visual hierarchy
- Maintain proper spacing and alignment

#### #20 - Mobile Button Stacking
- Ensure buttons stack vertically on mobile
- Test on various screen sizes
- Maintain tap-friendly sizing (44px minimum)

#### #21 - Mobile-Optimized Purchase Section
- Consider accordion/collapsible for mobile
- "Where to Buy" that expands to show all options
- Saves screen real estate on small devices

### Social Media Enhancements

#### #11 - Add Text Labels to Social Icons
- Include platform names or usernames
- "@haleym.opet" for Instagram/Threads
- "@haleymopet" for TikTok
- Improves accessibility and clarity

#### #12 - Prominent Linktr.ee Placement
- Make Linktr.ee link more visible
- Consider adding "All Links" text
- Emphasize as central hub for all links

### Visual Enhancements

#### #16 - Add Retailer Logos
- Use FontAwesome icons or simple CSS icons
- Place next to retailer buttons
- Aids in instant recognition

### Content Updates

#### #24 - Update Button Text
- Change "GET IT ON KINDLE" to "GET IT NOW" 
- Or use "BUY NOW" for format-agnostic approach
- Applies to buttons that will show format selection

#### #25 - Add Duology Reference
- Update hero subtitle or add line
- "Book One of The Solwyn Duology"
- Establishes series context immediately

---

## 📈 Phase 2: NEXT
**Priority: SEO, Analytics & Enhanced Discovery**
*Implement after Phase 1 is deployed and verified stable*

### #8 - Dedicated "Where to Buy" Section
- Create a distinct section with all purchase options
- Include all retailer links in one organized place
- Consider using cards or a table layout
- Add to navigation menu if appropriate

### #9 - Book 2 Teaser
- Add text: "Book Two of The Solwyn Duology coming soon!"
- Place strategically (maybe after blurb)
- Build anticipation for next release
- Consider adding a newsletter signup specifically for Book 2 updates

### #13 - Meta Description Update
- Update HTML meta description tag
- Include "Available Now" messaging
- Optimize for search engines
- Include book title and author name

### #14 - Schema.org Structured Data
- Add Book schema markup
- Include:
  - Title, Author, ISBN
  - Publication date
  - Series information
  - Retailer links with prices
  - Review ratings (when available)
- Helps with rich snippets in search results

### #18 - Enhanced Analytics Tracking
- Differentiate tracking between:
  - Kindle vs Paperback clicks
  - Amazon vs B&N vs BAM clicks
  - Hero section vs Featured section clicks
- Create custom events for each retailer
- Set up conversion tracking if possible

---

## 🔮 Phase 3: LATER
**Priority: Future-Proofing & Advanced Features**
*Implement after Phase 2 is complete and verified*

### #10 - Series Showcase Section
- Create dedicated section for The Solwyn Duology
- Display Book 1 (available) and Book 2 (coming soon)
- Include cover art for both (placeholder for Book 2)
- Timeline or progression visual
- Links to individual book pages

### #15 - "Available Now" Banner
- Add eye-catching banner or badge
- Consider animated/pulsing effect
- Position in hero section
- Time-limited (remove after initial launch period)

### #17 - New Release Badge
- Add "New Release" or "Just Launched" ribbon
- Overlay on book cover image
- Use CSS for easy removal later
- Consider date-based auto-removal

### #19 - Audiobook Interest Tracking
- Add "Notify me when audiobook is available" button
- Track clicks as interest metrics
- Connect to email list with "audiobook interest" tag
- Use data to gauge audiobook demand

### #22 - Audiobook Infrastructure
- Prepare button styling for audiobook
- Create placeholder in code (commented out)
- Design "Coming Soon" state for audiobook button
- Plan for Audible/other platform integration

### #23 - Book 2 Pre-Order Preparation
- Create template/infrastructure for Book 2
- Prepare pre-order button styling
- Plan for easy content swap
- Consider countdown timer functionality
- Design "Coming Soon" page template

---

## 📋 Implementation Notes

### Version Control Strategy
- Each phase should be a separate branch
- Phase 1: `feature/launch-updates-phase-1`
- Phase 2: `feature/launch-updates-phase-2`  
- Phase 3: `feature/launch-updates-phase-3`
- Merge to main only after testing

### Testing Checklist
Before deploying each phase:
- [ ] Desktop browser testing (Chrome, Firefox, Safari)
- [ ] Mobile responsive testing
- [ ] Button functionality verification
- [ ] Analytics tracking confirmation
- [ ] Page load speed check
- [ ] Accessibility scan

### Rollback Plan
- Keep previous version tagged in Git
- Document any database or configuration changes
- Test rollback procedure in development

### Success Metrics
- Phase 1: Increased click-through to retailers
- Phase 2: Improved search visibility, better analytics insights
- Phase 3: Growing interest metrics for future releases

---

## 📅 Suggested Timeline
- **Phase 1**: Implement immediately (1-2 hours)
- **Phase 2**: 1-2 days after Phase 1 verification
- **Phase 3**: 1 week after Phase 2 completion

---

*Document created: November 10, 2025*
*Last updated: November 10, 2025*
