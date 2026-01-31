// Goodreads Reviews Loader
// Loads reviews from goodreads_reviews.json and displays them with crossfade animation

document.addEventListener('DOMContentLoaded', function() {
    var carousel = document.getElementById('reviews-carousel');
    if (!carousel) return;

    var jsonPath = window.location.hostname === 'localhost' || window.location.protocol === 'file:'
        ? './goodreads_reviews.json'
        : '/goodreads_reviews.json';

    fetch(jsonPath)
        .then(function(response) {
            if (!response.ok) throw new Error('HTTP error: ' + response.status);
            return response.json();
        })
        .then(function(reviews) {
            if (!reviews || reviews.length === 0) {
                carousel.parentElement.parentElement.style.display = 'none';
                return;
            }

            // Shuffle reviews for variety on each page load
            for (var i = reviews.length - 1; i > 0; i--) {
                var j = Math.floor(Math.random() * (i + 1));
                var temp = reviews[i];
                reviews[i] = reviews[j];
                reviews[j] = temp;
            }

            var currentIndex = 0;
            var perPage = 3;
            var intervalId = null;
            var isPaused = false;

            function escapeHtml(str) {
                var div = document.createElement('div');
                div.appendChild(document.createTextNode(str));
                return div.innerHTML;
            }

            function cleanText(text) {
                // Strip HTML tags but preserve paragraph breaks
                return text
                    .replace(/<br\s*\/?>/gi, ' ')
                    .replace(/<\/?[^>]+(>|$)/g, '')
                    .replace(/&amp;/g, '&')
                    .replace(/&lt;/g, '<')
                    .replace(/&gt;/g, '>')
                    .replace(/\s{2,}/g, ' ')
                    .trim();
            }

            function truncateText(text, maxLen) {
                if (text.length <= maxLen) return text;
                return text.substring(0, maxLen).replace(/\s+\S*$/, '') + '...';
            }

            function buildStars() {
                var html = '';
                for (var s = 0; s < 5; s++) {
                    html += '<i class="fas fa-star"></i>';
                }
                return html;
            }

            function renderReviews(startIndex) {
                var html = '';
                for (var i = 0; i < perPage; i++) {
                    var idx = (startIndex + i) % reviews.length;
                    var review = reviews[idx];

                    var cleaned = cleanText(review.text);
                    var truncated = truncateText(cleaned, 300);
                    var needsMore = cleaned.length > 300;
                    var readMoreLink = '';
                    if (needsMore && review.review_url) {
                        readMoreLink = ' <a href="' + review.review_url + '" target="_blank" rel="noopener noreferrer" class="review-read-more">Read more</a>';
                    }

                    var safeName = escapeHtml(review.reviewer_name);
                    var imgHtml = '';
                    if (review.reviewer_image) {
                        imgHtml = '<img src="' + escapeHtml(review.reviewer_image) + '" alt="' + safeName + '" class="reviewer-pic">';
                    } else {
                        imgHtml = '<div class="reviewer-pic-placeholder"><i class="fas fa-user"></i></div>';
                    }

                    html += '<div class="review-card">' +
                        '<div class="review-stars">' + buildStars() + '</div>' +
                        '<div class="review-text">' + truncated + readMoreLink + '</div>' +
                        '<div class="reviewer-info">' +
                            imgHtml +
                            '<span class="reviewer-name">' + safeName + '</span>' +
                        '</div>' +
                    '</div>';
                }
                return html;
            }

            function showReviews(startIndex) {
                carousel.innerHTML = renderReviews(startIndex);
            }

            function advanceReviews() {
                if (isPaused) return;

                carousel.classList.add('fade-out');

                setTimeout(function() {
                    currentIndex = (currentIndex + perPage) % reviews.length;
                    showReviews(currentIndex);
                    carousel.classList.remove('fade-out');
                }, 500);
            }

            // Initial render
            showReviews(0);

            // Only start rotation if we have more than one page of reviews
            if (reviews.length > perPage) {
                intervalId = setInterval(advanceReviews, 8000);

                // Pause on hover
                carousel.addEventListener('mouseenter', function() {
                    isPaused = true;
                });

                carousel.addEventListener('mouseleave', function() {
                    isPaused = false;
                });
            }

            console.log('Loaded ' + reviews.length + ' Goodreads reviews');
        })
        .catch(function(error) {
            console.error('Error loading Goodreads reviews:', error);
            // Hide the section if reviews fail to load
            if (carousel.parentElement && carousel.parentElement.parentElement) {
                carousel.parentElement.parentElement.style.display = 'none';
            }
        });
});
