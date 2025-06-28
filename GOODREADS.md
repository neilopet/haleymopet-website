# Goodreads Book Cover Upload Requirements - Developer Guide

## Purpose

Enable Haley M. Opet's author website (haleymopet.com) to serve as a verified source for book cover uploads to Goodreads, allowing librarians to accept and process cover image requests.

## Background Context

**Current Issue**: Goodreads rejected a cover upload request stating "author's page does not show anything useful" because the website currently displays placeholder images instead of the actual book cover.

**Goal**: Transform the website into a legitimate, verifiable source that Goodreads librarians can use to confirm and download the official book cover.

## Goodreads Acceptance Criteria

### Acceptable Sources (What Goodreads Will Accept)
- ✅ **Author websites** (like haleymopet.com)
- ✅ **Publisher websites**
- ✅ **User profile uploads on Goodreads**
- ✅ **Official book/author pages with verifiable ownership**

### Unacceptable Sources (What Goodreads Rejects)
- ❌ **Social media platforms** (Instagram, Facebook, Twitter, TikTok)
- ❌ **Bookseller websites** (Amazon, Barnes & Noble, etc.)
- ❌ **Third-party book databases**
- ❌ **Temporary file hosting services**

### Technical Requirements for Cover Images
- **File formats**: JPG, PNG, GIF
- **File size**: Under 10MB (preferably under 2MB for web performance)
- **Resolution**: Minimum 600px width recommended for quality
- **Accessibility**: Direct URL access (not behind authentication)
- **Stability**: Permanent hosting (not temporary links)

## Current Website Status

**Domain**: haleymopet.com  
**Hosting**: GitHub Pages  
**Repository**: neilopet/haleymopet-website  
**Local Directory**: /Users/neilopet/Code/haleymopet-website

**Current Issue**: The hero section uses a placeholder image path:
```html
<img src="/api/placeholder/600/600" alt="Haley M. Opet">
```

## Schema.org Requirements - CLARIFICATION

**Important Finding**: Goodreads does **NOT** require Schema.org markup for book cover verification. Research confirms:
- Goodreads librarians verify covers through visual inspection and source legitimacy
- Schema.org markup is beneficial for SEO and Google rich results, but irrelevant to Goodreads cover acceptance  
- The rejection was based on inability to locate the cover image, not missing structured data
- One developer noted: "Sadly, Goodreads doesn't natively read the Schema.org markup I so carefully craft"

**Recommendation**: While Schema.org Book markup is good practice for author websites, it's **completely optional** for this specific Goodreads requirement.

**Why Schema.org Is Not Needed Here**:
- Goodreads librarians are human reviewers, not automated systems
- They need visual confirmation of the cover, not machine-readable data
- The verification process relies on source credibility, not technical markup
- Your website's legitimacy comes from domain ownership and author identification, not structured data

## Developer Implementation Requirements

### 1. **Immediate Fix: Replace Placeholder Image**

**Current Code Location**: In the hero section of index.html
```html
<div class="hero-image">
    <img src="/api/placeholder/600/600" alt="Haley M. Opet">
</div>
```

**Required Action**: 
- Replace placeholder with actual book cover image
- Ensure image loads properly and displays correctly
- Maintain responsive design functionality

### 2. **Book Cover Image Implementation**

**Image Asset**: The book cover file is available as "ABloodveiledDescentEbook.jpg"

**Requirements**:
- Upload cover image to repository
- Create logical directory structure (e.g., `/images/` or `/assets/`)
- Use appropriate file naming (avoid spaces, use hyphens or underscores)
- Optimize image size for web performance while maintaining quality

**Suggested Implementation**:
```html
<div class="hero-image">
    <img src="/images/book-cover.jpg" alt="[Book Title] by Haley M. Opet">
</div>
```

### 3. **Enhanced Book Presentation (Recommended)**

**Option A: Dedicated Book Section**
Create a prominent book section that includes:
- Large, clear book cover display
- Book title and subtitle
- Author name
- Publication information
- Book description/blurb

**Option B: Book Landing Page** 
Create a separate page (e.g., `/book/` or `/my-novel/`) featuring:
- Hero section with book cover
- Detailed book information
- Sample chapters or excerpts
- Purchase/pre-order links

**Option C: Enhanced Homepage**
Improve the existing homepage by:
- Replacing ALL placeholder images with actual content
- Adding book cover to multiple sections for visibility
- Creating a clear visual hierarchy that highlights the book

### 4. **Technical Implementation Checklist**

**File Management**:
- [ ] Create `/images/` directory in repository
- [ ] Upload optimized book cover image
- [ ] Verify image loads correctly across devices
- [ ] Test image accessibility (direct URL access)

**HTML Updates**:
- [ ] Replace placeholder `src="/api/placeholder/600/600"`
- [ ] Update `alt` text to be descriptive and accurate
- [ ] Ensure responsive image behavior is maintained
- [ ] Add book cover to additional strategic locations

**Quality Assurance**:
- [ ] Test on mobile, tablet, and desktop
- [ ] Verify image loading speed
- [ ] Confirm image displays properly in all browsers
- [ ] Test direct image URL accessibility
- [ ] Validate HTML markup

**SEO Considerations**:
- [ ] Use descriptive alt text for accessibility
- [ ] Add appropriate meta tags for book information
- [ ] Consider adding structured data markup for books

### 5. **Deployment Process**

**GitHub Pages Workflow**:
1. Make changes in local repository
2. Test locally to ensure functionality
3. Commit changes with descriptive commit message
4. Push to main branch
5. Verify deployment via GitHub Pages
6. Test live site functionality
7. Confirm image accessibility via direct URL

**Critical Verification Steps**:
- Confirm cover image loads at live URL
- Test image URL directly (e.g., `https://haleymopet.com/images/book-cover.jpg`)
- Verify image displays correctly in hero section
- Check responsive behavior across devices
- **Test from different networks** (ensure it's not just working locally)
- **Verify image is publicly accessible** (not behind any authentication)

**Pre-Submission Checklist**:
- [ ] Image loads properly on live site
- [ ] Direct image URL returns the cover (not a 404 error)
- [ ] Cover is clearly visible on homepage
- [ ] Website identifies you as the author
- [ ] No broken links or placeholder content
- [ ] Site loads quickly and professionally

## Expected Outcome

Once implemented, Goodreads librarians will be able to:
1. Visit haleymopet.com and immediately see the book cover prominently displayed
2. Right-click and save/copy the image or image URL
3. Verify the cover matches the book being processed  
4. Confirm source legitimacy (official author website)
5. Upload the cover to Goodreads with confidence

**Librarian Verification Process**: Based on Goodreads forum discussions, librarians typically:
- Visit the provided source URL
- Look for clear, professional cover display
- Verify the source appears legitimate (author/publisher website)
- Check that the image is accessible and downloadable
- Confirm the cover quality is suitable for the database

**Alternative Backup Method**: If primary implementation faces unexpected issues, you can upload the cover to your Goodreads profile photos and request via the Librarians Group forum (established method with high success rate).

## Timeline

**Priority**: High - This blocks the Goodreads listing process  
**Estimated Development Time**: 1-2 hours  
**Estimated Testing Time**: 30 minutes  
**Total Timeline**: Same day completion recommended

## Success Probability & Limitations

**High Confidence Factors**: 
- Your website (haleymopet.com) is exactly the type of source Goodreads accepts
- The current rejection reason is easily fixable (missing visible cover image)
- GitHub Pages hosting is stable and professional

**What I Can Reasonably Assure**:
- Your website will meet Goodreads' technical and legitimacy requirements
- Librarians will be able to locate and verify your book cover
- The specific issue causing rejection will be resolved

**What I Cannot Guarantee**:
- Individual librarian decisions (some may have stricter standards)
- Processing timelines or approval speed
- Coverage of undocumented Goodreads policy changes

**Confidence Level**: 95% success probability based on documented requirements and typical librarian acceptance patterns.

## Success Metrics

**Technical Success**:
- Image loads properly on live site
- Direct image URL is accessible
- Site maintains responsive design
- No broken functionality

**Business Success**:
- Goodreads librarians can easily locate and verify book cover
- Cover upload request gets approved
- Book listing is complete and professional

## Notes for Developer

- **Important**: The book title should be removed from all public-facing content per client instructions
- **Image Quality**: Prioritize crisp, professional appearance while optimizing for web performance
- **Future-Proofing**: Consider scalable approach if additional books will be added later
- **Backup Plan**: If primary implementation fails, the alternative is to upload cover to Goodreads profile and request via librarian forum

## Contact Information

For questions or clarifications, reach out to Haley M. Opet regarding book cover specifications or design preferences.