// Instagram Posts Loader
// Add this to your index.html to load Instagram posts from instagram_posts.json

document.addEventListener('DOMContentLoaded', function() {
    const blogPostsContainer = document.querySelector('.blog-posts');
    
    if (!blogPostsContainer) {
        console.error('Blog posts container not found');
        return;
    }
    
    // Load Instagram posts from JSON file
    // Use relative path for both GitHub Pages and local testing
    const jsonPath = window.location.hostname === 'localhost' || window.location.protocol === 'file:' 
        ? './instagram_posts.json' 
        : '/instagram_posts.json';
    
    fetch(jsonPath)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(posts => {
            if (posts && posts.length > 0) {
                // Clear existing static content
                blogPostsContainer.innerHTML = '';
                
                // Create post elements
                posts.forEach(post => {
                    const postElement = document.createElement('div');
                    postElement.className = 'blog-post';
                    
                    postElement.innerHTML = `
                        <div class="blog-post-image" style="background-image: url('${post.image}');"></div>
                        <div class="blog-post-content">
                            <p class="blog-post-date">${post.date}</p>
                            <p class="blog-post-excerpt">${post.excerpt}</p>
                            <a href="${post.link}" target="_blank" rel="noopener noreferrer" class="btn">VIEW ON INSTAGRAM</a>
                        </div>
                    `;
                    
                    blogPostsContainer.appendChild(postElement);
                });
                
                console.log(`Loaded ${posts.length} Instagram posts`);
            } else {
                // Fallback to static content if no posts
                console.log('No Instagram posts found, keeping static content');
            }
        })
        .catch(error => {
            console.error('Error loading Instagram posts:', error);
            console.log('Keeping static blog content due to error');
            // Keep the existing static content on error
        });
});