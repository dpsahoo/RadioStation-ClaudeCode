/**
 * Main application entry point for Radio Sahoo
 */
(function() {
    'use strict';
    
    // Global application instance
    let app = null;
    
    /**
     * Main application class
     */
    class RadioSahooApp {
        constructor() {
            this.state = window.appState;
            this.player = null;
            this.metadata = null;
            this.rating = null;
            this.initialized = false;
        }
        
        /**
         * Initialize the application
         */
        async init() {
            try {
                console.log('Initializing Radio Sahoo...');
                
                // Initialize modules
                this.player = new window.AudioPlayer(this.state);
                this.metadata = new window.MetadataManager(this.state);
                this.rating = new window.RatingManager(this.state);
                
                // Initialize player
                await this.player.initialize();
                
                // Initialize rating system
                this.rating.initialize();
                
                // Setup global event listeners
                this.setupGlobalEventListeners();
                
                // Setup state change listeners
                this.setupStateListeners();
                
                // Load initial metadata
                this.metadata.loadMetadata();
                
                this.initialized = true;
                console.log('Radio Sahoo initialized successfully');
                
            } catch (error) {
                console.error('Failed to initialize Radio Sahoo:', error);
                this.showInitializationError(error);
            }
        }
        
        /**
         * Setup global event listeners
         */
        setupGlobalEventListeners() {
            // Play state event listeners
            this.state.addEventListener('playStateChange', (data) => {
                if (data.isPlaying) {
                    this.metadata.startPolling();
                } else {
                    this.metadata.stopPolling();
                }
            });
            
            // Keyboard shortcuts
            document.addEventListener('keydown', (e) => {
                if (e.code === 'Space' && e.target.tagName !== 'INPUT') {
                    e.preventDefault();
                    this.player.togglePlayPause();
                }
            });
            
            // Page visibility changes
            document.addEventListener('visibilitychange', () => {
                if (document.hidden && this.state.isPlaying) {
                    // Optional: pause when tab is hidden
                    // this.player.togglePlayPause();
                }
            });
            
            // Cleanup on page unload
            window.addEventListener('beforeunload', () => {
                this.cleanup();
            });
        }
        
        /**
         * Setup state change listeners
         */
        setupStateListeners() {
            // Listen for track changes to update ratings
            this.state.addEventListener('trackChange', () => {
                // Track change is already handled by RatingManager
            });
        }
        
        /**
         * Show initialization error
         */
        showInitializationError(error) {
            const statusDiv = document.getElementById('status');
            if (statusDiv) {
                statusDiv.textContent = 'Failed to initialize player: ' + error.message;
                statusDiv.className = 'status error';
            }
        }
        
        /**
         * Cleanup resources
         */
        cleanup() {
            if (this.metadata) {
                this.metadata.stopPolling();
            }
            
            if (this.state.hls) {
                this.state.hls.destroy();
            }
        }
    }
    
    /**
     * Global functions exposed to HTML
     */
    window.togglePlayPause = function() {
        if (app && app.player) {
            app.player.togglePlayPause();
        }
    };
    
    window.stopStream = function() {
        if (app && app.player) {
            app.player.stop();
        }
    };
    
    window.reloadStream = function() {
        if (app && app.player) {
            app.player.reload();
        }
    };
    
    window.rateTrack = function(rating) {
        if (app && app.rating) {
            app.rating.handleRatingClick(rating);
        }
    };
    
    /**
     * Initialize when DOM is loaded
     */
    document.addEventListener('DOMContentLoaded', async function() {
        try {
            app = new RadioSahooApp();
            await app.init();
        } catch (error) {
            console.error('Failed to start application:', error);
        }
    });
    
    // Make app available globally for debugging
    window.radioSahooApp = app;
    
})();