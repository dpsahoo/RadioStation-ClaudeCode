/**
 * Rating system management for Radio Calico
 */
class RatingManager {
    constructor(state) {
        this.state = state;
        this.logger = console;
        
        // Listen for track changes
        this.state.addEventListener('trackChange', (data) => {
            this.handleTrackChange(data.trackId);
        });
    }
    
    /**
     * Initialize rating system
     */
    initialize() {
        this.generateFingerprint();
        this.setupEventListeners();
    }
    
    /**
     * Setup event listeners for rating buttons
     */
    setupEventListeners() {
        // Listen for rating button clicks (delegated event handling)
        document.addEventListener('click', (event) => {
            if (event.target.classList.contains('rating-btn')) {
                const rating = event.target.classList.contains('thumbs-up') ? 'up' : 'down';
                this.handleRatingClick(rating);
            }
        });
    }
    
    /**
     * Handle track change
     */
    async handleTrackChange(trackId) {
        if (trackId) {
            this.state.setCurrentRating(null); // Reset rating for new track
            this.updateRatingButtons();
            await this.loadUserRating(trackId);
        }
    }
    
    /**
     * Handle rating button click
     */
    async handleRatingClick(rating) {
        if (!this.state.currentTrackId) {
            this.logger.warn('No current track to rate');
            return;
        }
        
        // Toggle rating if same button clicked
        const newRating = this.state.currentTrackRating === rating ? null : rating;
        
        this.state.setCurrentRating(newRating);
        this.updateRatingButtons();
        await this.saveRating(this.state.currentTrackId, newRating);
    }
    
    /**
     * Update rating button states
     */
    updateRatingButtons() {
        const thumbsUp = document.getElementById('thumbs-up');
        const thumbsDown = document.getElementById('thumbs-down');
        const ratingStatus = document.getElementById('rating-status');
        
        if (!thumbsUp || !thumbsDown || !ratingStatus) return;
        
        // Reset buttons
        thumbsUp.classList.remove('active');
        thumbsDown.classList.remove('active');
        
        // Update based on current rating
        const rating = this.state.currentTrackRating;
        
        if (rating === 'up') {
            thumbsUp.classList.add('active');
            ratingStatus.textContent = 'You liked this track';
            ratingStatus.style.color = '#28a745';
        } else if (rating === 'down') {
            thumbsDown.classList.add('active');
            ratingStatus.textContent = 'You disliked this track';
            ratingStatus.style.color = '#dc3545';
        } else {
            ratingStatus.textContent = 'Rate this track';
            ratingStatus.style.color = '#666';
        }
    }
    
    /**
     * Save rating to server
     */
    async saveRating(trackId, rating) {
        try {
            const response = await fetch('/api/ratings', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    track_id: trackId,
                    rating: rating,
                    user_fingerprint: this.state.userFingerprint,
                    timestamp: new Date().toISOString()
                })
            });
            
            if (response.ok) {
                this.logger.log('Rating saved successfully');
                // Reload ratings to get updated counts
                await this.loadUserRating(trackId);
            } else {
                const errorData = await response.json();
                this.logger.error('Failed to save rating:', errorData);
            }
        } catch (error) {
            this.logger.error('Error saving rating:', error);
            // Still allow local rating even if save fails
        }
    }
    
    /**
     * Load user rating and counts for a track
     */
    async loadUserRating(trackId) {
        try {
            const url = `/api/ratings/${encodeURIComponent(trackId)}?fingerprint=${encodeURIComponent(this.state.userFingerprint)}`;
            const response = await fetch(url);
            
            if (response.ok) {
                const data = await response.json();
                this.state.setCurrentRating(data.user_rating);
                this.updateRatingButtons();
                this.updateRatingCounts(data.ratings);
            } else {
                this.logger.error('Failed to load user rating');
            }
        } catch (error) {
            this.logger.error('Error loading user rating:', error);
        }
    }
    
    /**
     * Update rating count displays
     */
    updateRatingCounts(ratings) {
        const upCount = document.getElementById('up-count');
        const downCount = document.getElementById('down-count');
        
        if (upCount) {
            upCount.textContent = ratings.up || 0;
        }
        if (downCount) {
            downCount.textContent = ratings.down || 0;
        }
    }
    
    /**
     * Generate browser fingerprint for unique user identification
     */
    generateFingerprint() {
        try {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            ctx.textBaseline = 'top';
            ctx.font = '14px Arial';
            ctx.fillText('Browser fingerprint', 2, 2);
            
            const fingerprint = [
                navigator.userAgent,
                navigator.language,
                screen.width + 'x' + screen.height,
                screen.colorDepth,
                new Date().getTimezoneOffset(),
                !!window.sessionStorage,
                !!window.localStorage,
                navigator.platform,
                canvas.toDataURL()
            ].join('|');
            
            this.state.userFingerprint = btoa(fingerprint).substring(0, 32);
            this.logger.log('Generated fingerprint:', this.state.userFingerprint);
            
        } catch (error) {
            this.logger.error('Failed to generate fingerprint:', error);
            // Fallback to random string
            this.state.userFingerprint = Math.random().toString(36).substring(2, 15);
        }
    }
}

// Make available globally
window.RatingManager = RatingManager;