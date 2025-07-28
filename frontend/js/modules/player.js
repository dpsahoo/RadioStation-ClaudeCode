/**
 * Audio player management for Radio Calico
 */
class AudioPlayer {
    constructor(state) {
        this.state = state;
        this.logger = console; // Simple logger, could be enhanced
    }
    
    /**
     * Initialize the HLS player
     */
    async initialize() {
        try {
            this.state.player = document.getElementById('radio-player');
            
            if (!this.state.player) {
                throw new Error('Audio player element not found');
            }
            
            // Set initial volume
            this.state.player.volume = 0.8;
            
            // Initialize HLS.js if supported
            if (window.Hls && Hls.isSupported()) {
                await this.initializeHLS();
            } else if (this.state.player.canPlayType('application/vnd.apple.mpegurl')) {
                // Fallback for Safari which has native HLS support
                this.initializeNativeHLS();
            } else {
                throw new Error('HLS not supported in this browser');
            }
            
            this.setupEventListeners();
            this.logger.log('Audio player initialized successfully');
            
        } catch (error) {
            this.logger.error('Failed to initialize audio player:', error);
            this.updateStatus('Failed to initialize player', 'error');
        }
    }
    
    /**
     * Initialize HLS.js player
     */
    async initializeHLS() {
        this.state.hls = new Hls({
            enableWorker: true,
            lowLatencyMode: true,
            backBufferLength: 90
        });
        
        this.state.hls.loadSource(this.state.config.streamUrl);
        this.state.hls.attachMedia(this.state.player);
        
        // HLS event listeners
        this.state.hls.on(Hls.Events.MEDIA_ATTACHED, () => {
            this.logger.log('HLS media attached');
            this.updateStatus('Stream loaded and ready', 'ready');
        });
        
        this.state.hls.on(Hls.Events.MANIFEST_PARSED, () => {
            this.logger.log('HLS manifest parsed');
            this.updateStatus('Stream ready to play', 'ready');
        });
        
        this.state.hls.on(Hls.Events.ERROR, (event, data) => {
            this.handleHLSError(data);
        });
    }
    
    /**
     * Initialize native HLS support (Safari)
     */
    initializeNativeHLS() {
        this.state.player.src = this.state.config.streamUrl;
        this.updateStatus('Using native HLS support', 'ready');
    }
    
    /**
     * Handle HLS errors with recovery attempts
     */
    handleHLSError(data) {
        this.logger.error('HLS Error:', data);
        
        if (data.fatal) {
            switch(data.type) {
                case Hls.ErrorTypes.NETWORK_ERROR:
                    this.updateStatus('Network error. Trying to recover...', 'error');
                    this.state.hls.startLoad();
                    break;
                case Hls.ErrorTypes.MEDIA_ERROR:
                    this.updateStatus('Media error. Trying to recover...', 'error');
                    this.state.hls.recoverMediaError();
                    break;
                default:
                    this.updateStatus('Fatal error. Please reload.', 'error');
                    this.state.hls.destroy();
                    break;
            }
        }
    }
    
    /**
     * Setup audio player event listeners
     */
    setupEventListeners() {
        const player = this.state.player;
        
        player.addEventListener('loadstart', () => {
            this.updateStatus('Loading stream...', 'loading');
        });
        
        player.addEventListener('canplay', () => {
            this.updateStatus('Stream ready to play', 'ready');
        });
        
        player.addEventListener('play', () => {
            this.state.setPlayState(true);
            this.updatePlayPauseButton();
            this.updateStatus('🎵 Now playing live radio', 'playing');
        });
        
        player.addEventListener('pause', () => {
            this.state.setPlayState(false);
            this.updatePlayPauseButton();
            this.updateStatus('Stream paused', 'paused');
        });
        
        player.addEventListener('ended', () => {
            this.state.setPlayState(false);
            this.updatePlayPauseButton();
            this.updateStatus('Stream ended', 'paused');
        });
        
        player.addEventListener('error', (e) => {
            this.logger.error('Player error:', e);
            this.state.setPlayState(false);
            this.updatePlayPauseButton();
            this.updateStatus('Error loading stream. Please try again.', 'error');
        });
        
        player.addEventListener('loadeddata', () => {
            this.updateStatus('Stream loaded successfully', 'ready');
        });
        
        // Volume control
        this.setupVolumeControl();
    }
    
    /**
     * Setup volume control
     */
    setupVolumeControl() {
        const volumeSlider = document.getElementById('volume-slider');
        const volumeDisplay = document.getElementById('volume-display');
        const player = this.state.player;
        
        if (volumeSlider && volumeDisplay) {
            volumeSlider.addEventListener('input', () => {
                const volume = volumeSlider.value;
                player.volume = volume;
                volumeDisplay.textContent = Math.round(volume * 100) + '%';
            });
            
            player.addEventListener('volumechange', () => {
                const volume = player.volume;
                volumeSlider.value = volume;
                volumeDisplay.textContent = Math.round(volume * 100) + '%';
            });
        }
    }
    
    /**
     * Toggle play/pause
     */
    async togglePlayPause() {
        if (!this.state.player) return;
        
        try {
            if (this.state.isPlaying) {
                this.state.player.pause();
            } else {
                await this.state.player.play();
            }
        } catch (error) {
            this.logger.error('Play error:', error);
            this.updateStatus('Unable to play stream. Please check your connection.', 'error');
        }
    }
    
    /**
     * Stop playback
     */
    stop() {
        if (this.state.player) {
            this.state.player.pause();
            this.state.player.currentTime = 0;
            this.updatePlayPauseButton();
            this.updateStatus('Stream stopped', 'paused');
        }
    }
    
    /**
     * Reload stream
     */
    reload() {
        this.updateStatus('Reloading stream...', 'loading');
        
        if (this.state.hls) {
            this.state.hls.stopLoad();
            this.state.hls.startLoad();
        } else if (this.state.player) {
            this.state.player.load();
        }
    }
    
    /**
     * Update play/pause button
     */
    updatePlayPauseButton() {
        const btn = document.getElementById('playPauseBtn');
        if (btn) {
            btn.innerHTML = this.state.isPlaying ? '⏸️' : '▶️';
            btn.title = this.state.isPlaying ? 'Pause' : 'Play';
        }
    }
    
    /**
     * Update status display
     */
    updateStatus(message, type) {
        const statusDiv = document.getElementById('status');
        if (statusDiv) {
            statusDiv.textContent = message;
            statusDiv.className = 'status ' + type;
        }
    }
}

// Make available globally
window.AudioPlayer = AudioPlayer;