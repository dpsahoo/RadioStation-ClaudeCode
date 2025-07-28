/**
 * Application state management for Radio Calico
 */
class AppState {
    constructor() {
        this.player = null;
        this.hls = null;
        this.isPlaying = false;
        this.metadataInterval = null;
        this.currentTrackRating = null;
        this.currentTrackId = null;
        this.userFingerprint = null;
        
        // Configuration
        this.config = {
            streamUrl: 'https://d3d4yli4hf5bmh.cloudfront.net/hls/live.m3u8',
            metadataUrl: 'https://d3d4yli4hf5bmh.cloudfront.net/metadatav2.json',
            coverArtUrl: 'https://d3d4yli4hf5bmh.cloudfront.net/cover.jpg',
            metadataUpdateInterval: 10000 // 10 seconds
        };
        
        // Event listeners for state changes
        this.listeners = {
            playStateChange: [],
            trackChange: [],
            ratingChange: []
        };
    }
    
    /**
     * Add event listener for state changes
     */
    addEventListener(event, callback) {
        if (this.listeners[event]) {
            this.listeners[event].push(callback);
        }
    }
    
    /**
     * Remove event listener
     */
    removeEventListener(event, callback) {
        if (this.listeners[event]) {
            const index = this.listeners[event].indexOf(callback);
            if (index > -1) {
                this.listeners[event].splice(index, 1);
            }
        }
    }
    
    /**
     * Trigger event listeners
     */
    emit(event, data) {
        if (this.listeners[event]) {
            this.listeners[event].forEach(callback => callback(data));
        }
    }
    
    /**
     * Update play state
     */
    setPlayState(isPlaying) {
        if (this.isPlaying !== isPlaying) {
            this.isPlaying = isPlaying;
            this.emit('playStateChange', { isPlaying });
        }
    }
    
    /**
     * Update current track
     */
    setCurrentTrack(trackId, trackData) {
        if (this.currentTrackId !== trackId) {
            this.currentTrackId = trackId;
            this.currentTrackRating = null; // Reset rating for new track
            this.emit('trackChange', { trackId, trackData });
        }
    }
    
    /**
     * Update current rating
     */
    setCurrentRating(rating) {
        if (this.currentTrackRating !== rating) {
            this.currentTrackRating = rating;
            this.emit('ratingChange', { rating, trackId: this.currentTrackId });
        }
    }
    
    /**
     * Get current state snapshot
     */
    getState() {
        return {
            isPlaying: this.isPlaying,
            currentTrackId: this.currentTrackId,
            currentTrackRating: this.currentTrackRating,
            userFingerprint: this.userFingerprint
        };
    }
}

// Export singleton instance
window.appState = window.appState || new AppState();