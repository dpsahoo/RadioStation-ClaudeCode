/**
 * Metadata management for Radio Calico
 */
class MetadataManager {
    constructor(state) {
        this.state = state;
        this.logger = console;
    }
    
    /**
     * Start metadata polling
     */
    startPolling() {
        if (this.state.metadataInterval) {
            this.stopPolling();
        }
        
        // Load initial metadata
        this.loadMetadata();
        
        // Set up polling interval
        this.state.metadataInterval = setInterval(() => {
            this.loadMetadata();
        }, this.state.config.metadataUpdateInterval);
        
        this.logger.log('Metadata polling started');
    }
    
    /**
     * Stop metadata polling
     */
    stopPolling() {
        if (this.state.metadataInterval) {
            clearInterval(this.state.metadataInterval);
            this.state.metadataInterval = null;
            this.logger.log('Metadata polling stopped');
        }
    }
    
    /**
     * Load metadata from API
     */
    async loadMetadata() {
        try {
            const response = await fetch(this.state.config.metadataUrl);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const metadata = await response.json();
            this.updateNowPlaying(metadata);
            this.updateRecentlyPlayed(metadata);
            this.updateAudioQuality(metadata);
            
        } catch (error) {
            this.logger.error('Failed to load metadata:', error);
            // Don't show error to user for metadata failures, just log it
        }
    }
    
    /**
     * Update now playing information
     */
    updateNowPlaying(metadata) {
        // Update track information
        this.updateElement('track-artist', metadata.artist || 'Unknown Artist');
        this.updateElement('track-title', metadata.title || 'Unknown Track');
        this.updateElement('track-album', metadata.album || 'Unknown Album');
        
        // Update year badge
        const yearBadge = document.getElementById('year-badge');
        if (yearBadge) {
            yearBadge.textContent = metadata.date || '----';
        }
        
        // Update album art with cache busting
        this.updateAlbumArt();
        
        // Update badges
        this.updateTrackBadges(metadata);
        
        // Handle track change
        const newTrackId = this.generateTrackId(metadata);
        this.state.setCurrentTrack(newTrackId, metadata);
    }
    
    /**
     * Update album art with cache busting
     */
    updateAlbumArt() {
        const albumArt = document.getElementById('album-art');
        if (albumArt) {
            const albumArtUrl = `${this.state.config.coverArtUrl}?t=${Date.now()}`;
            albumArt.src = albumArtUrl;
        }
    }
    
    /**
     * Update track badges
     */
    updateTrackBadges(metadata) {
        const badgesContainer = document.getElementById('track-badges');
        if (!badgesContainer) return;
        
        let badgesHTML = '';
        
        if (metadata.is_new) {
            badgesHTML += '<span class="badge new">New</span>';
        }
        if (metadata.is_summer) {
            badgesHTML += '<span class="badge summer">Summer</span>';
        }
        if (metadata.is_vidgames) {
            badgesHTML += '<span class="badge vidgames">Gaming</span>';
        }
        
        badgesContainer.innerHTML = badgesHTML;
    }
    
    /**
     * Update recently played tracks
     */
    updateRecentlyPlayed(metadata) {
        const recentTracksContainer = document.getElementById('recent-tracks');
        if (!recentTracksContainer) return;
        
        let recentHTML = '';
        
        for (let i = 1; i <= 5; i++) {
            const artist = metadata[`prev_artist_${i}`];
            const title = metadata[`prev_title_${i}`];
            
            if (artist && title) {
                recentHTML += `
                    <div class="recent-track">
                        <div class="recent-track-info">
                            <div class="recent-track-artist">${this.escapeHtml(artist)}</div>
                            <div class="recent-track-title">${this.escapeHtml(title)}</div>
                        </div>
                    </div>
                `;
            }
        }
        
        recentTracksContainer.innerHTML = recentHTML || '<p>No recent tracks available</p>';
    }
    
    /**
     * Update audio quality information
     */
    updateAudioQuality(metadata) {
        const qualityElement = document.getElementById('audio-quality-display');
        if (qualityElement && metadata.bit_depth && metadata.sample_rate) {
            const quality = `Source quality: ${metadata.bit_depth}-bit ${metadata.sample_rate/1000}kHz`;
            qualityElement.textContent = quality;
        }
    }
    
    /**
     * Generate unique track ID
     */
    generateTrackId(metadata) {
        const artist = metadata.artist || 'unknown';
        const title = metadata.title || 'unknown';
        return `${artist}-${title}`.toLowerCase().replace(/[^a-z0-9-]/g, '-');
    }
    
    /**
     * Update element text content safely
     */
    updateElement(elementId, text) {
        const element = document.getElementById(elementId);
        if (element) {
            element.textContent = text;
        }
    }
    
    /**
     * Escape HTML to prevent XSS
     */
    escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, m => map[m]);
    }
}

// Make available globally
window.MetadataManager = MetadataManager;