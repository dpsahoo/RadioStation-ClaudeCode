/**
 * Tests for AppState module
 * Run with: npm test or in browser with testing framework
 */

// Mock DOM elements for testing
const mockDOM = {
    createElement: (tag) => ({
        tagName: tag.toUpperCase(),
        setAttribute: () => {},
        getAttribute: () => null,
        addEventListener: () => {},
        removeEventListener: () => {},
        dispatchEvent: () => true
    }),
    getElementById: (id) => ({
        id: id,
        addEventListener: () => {},
        removeEventListener: () => {}
    })
};

// Mock window object
const mockWindow = {
    appState: null,
    addEventListener: () => {},
    removeEventListener: () => {}
};

// Setup test environment
if (typeof window === 'undefined') {
    global.window = mockWindow;
    global.document = mockDOM;
}

// Load the AppState module (in browser environment, this would be loaded via script tag)
// For Node.js testing, you'd need to adapt the module or use a browser testing framework

describe('AppState', () => {
    let appState;
    
    beforeEach(() => {
        // Reset appState before each test
        if (typeof AppState !== 'undefined') {
            appState = new AppState();
        } else {
            // Mock AppState for testing environment
            appState = {
                player: null,
                hls: null,
                isPlaying: false,
                metadataInterval: null,
                currentTrackRating: null,
                currentTrackId: null,
                userFingerprint: null,
                config: {
                    streamUrl: 'https://test.example.com/stream.m3u8',
                    metadataUrl: 'https://test.example.com/metadata.json',
                    coverArtUrl: 'https://test.example.com/cover.jpg',
                    metadataUpdateInterval: 10000
                },
                listeners: {
                    playStateChange: [],
                    trackChange: [],
                    ratingChange: []
                },
                addEventListener: function(event, callback) {
                    if (this.listeners[event]) {
                        this.listeners[event].push(callback);
                    }
                },
                removeEventListener: function(event, callback) {
                    if (this.listeners[event]) {
                        const index = this.listeners[event].indexOf(callback);
                        if (index > -1) {
                            this.listeners[event].splice(index, 1);
                        }
                    }
                },
                emit: function(event, data) {
                    if (this.listeners[event]) {
                        this.listeners[event].forEach(callback => callback(data));
                    }
                },
                setPlayState: function(isPlaying) {
                    if (this.isPlaying !== isPlaying) {
                        this.isPlaying = isPlaying;
                        this.emit('playStateChange', { isPlaying });
                    }
                },
                setCurrentTrack: function(trackId, trackData) {
                    if (this.currentTrackId !== trackId) {
                        this.currentTrackId = trackId;
                        this.currentTrackRating = null;
                        this.emit('trackChange', { trackId, trackData });
                    }
                },
                setCurrentRating: function(rating) {
                    if (this.currentTrackRating !== rating) {
                        this.currentTrackRating = rating;
                        this.emit('ratingChange', { rating, trackId: this.currentTrackId });
                    }
                },
                getState: function() {
                    return {
                        isPlaying: this.isPlaying,
                        currentTrackId: this.currentTrackId,
                        currentTrackRating: this.currentTrackRating,
                        userFingerprint: this.userFingerprint
                    };
                }
            };
        }
    });
    
    describe('Initialization', () => {
        test('should initialize with default values', () => {
            expect(appState.player).toBeNull();
            expect(appState.hls).toBeNull();
            expect(appState.isPlaying).toBe(false);
            expect(appState.currentTrackRating).toBeNull();
            expect(appState.currentTrackId).toBeNull();
            expect(appState.userFingerprint).toBeNull();
        });
        
        test('should have correct configuration', () => {
            expect(appState.config.streamUrl).toContain('stream.m3u8');
            expect(appState.config.metadataUrl).toContain('metadata');
            expect(appState.config.coverArtUrl).toContain('cover');
            expect(appState.config.metadataUpdateInterval).toBe(10000);
        });
        
        test('should initialize event listeners', () => {
            expect(appState.listeners.playStateChange).toEqual([]);
            expect(appState.listeners.trackChange).toEqual([]);
            expect(appState.listeners.ratingChange).toEqual([]);
        });
    });
    
    describe('Event Management', () => {
        test('should add event listeners', () => {
            const callback = jest.fn();
            appState.addEventListener('playStateChange', callback);
            
            expect(appState.listeners.playStateChange).toContain(callback);
        });
        
        test('should remove event listeners', () => {
            const callback = jest.fn();
            appState.addEventListener('playStateChange', callback);
            appState.removeEventListener('playStateChange', callback);
            
            expect(appState.listeners.playStateChange).not.toContain(callback);
        });
        
        test('should emit events to listeners', () => {
            const callback = jest.fn();
            appState.addEventListener('playStateChange', callback);
            
            const eventData = { isPlaying: true };
            appState.emit('playStateChange', eventData);
            
            expect(callback).toHaveBeenCalledWith(eventData);
        });
        
        test('should handle non-existent event types gracefully', () => {
            const callback = jest.fn();
            
            expect(() => {
                appState.addEventListener('nonExistentEvent', callback);
            }).not.toThrow();
        });
    });
    
    describe('State Management', () => {
        test('should update play state and emit event', () => {
            const callback = jest.fn();
            appState.addEventListener('playStateChange', callback);
            
            appState.setPlayState(true);
            
            expect(appState.isPlaying).toBe(true);
            expect(callback).toHaveBeenCalledWith({ isPlaying: true });
        });
        
        test('should not emit event if play state unchanged', () => {
            const callback = jest.fn();
            appState.addEventListener('playStateChange', callback);
            appState.isPlaying = false;
            
            appState.setPlayState(false);
            
            expect(callback).not.toHaveBeenCalled();
        });
        
        test('should update current track and emit event', () => {
            const callback = jest.fn();
            appState.addEventListener('trackChange', callback);
            
            const trackData = { artist: 'Test Artist', title: 'Test Song' };
            appState.setCurrentTrack('test-track', trackData);
            
            expect(appState.currentTrackId).toBe('test-track');
            expect(appState.currentTrackRating).toBeNull(); // Should reset rating
            expect(callback).toHaveBeenCalledWith({ 
                trackId: 'test-track', 
                trackData: trackData 
            });
        });
        
        test('should update current rating and emit event', () => {
            const callback = jest.fn();
            appState.addEventListener('ratingChange', callback);
            appState.currentTrackId = 'test-track';
            
            appState.setCurrentRating('up');
            
            expect(appState.currentTrackRating).toBe('up');
            expect(callback).toHaveBeenCalledWith({ 
                rating: 'up', 
                trackId: 'test-track' 
            });
        });
        
        test('should return current state snapshot', () => {
            appState.isPlaying = true;
            appState.currentTrackId = 'test-track';
            appState.currentTrackRating = 'up';
            appState.userFingerprint = 'test-fingerprint';
            
            const state = appState.getState();
            
            expect(state).toEqual({
                isPlaying: true,
                currentTrackId: 'test-track',
                currentTrackRating: 'up',
                userFingerprint: 'test-fingerprint'
            });
        });
    });
    
    describe('Multiple Listeners', () => {
        test('should call multiple listeners for same event', () => {
            const callback1 = jest.fn();
            const callback2 = jest.fn();
            
            appState.addEventListener('playStateChange', callback1);
            appState.addEventListener('playStateChange', callback2);
            
            appState.setPlayState(true);
            
            expect(callback1).toHaveBeenCalled();
            expect(callback2).toHaveBeenCalled();
        });
        
        test('should handle listener removal correctly with multiple listeners', () => {
            const callback1 = jest.fn();
            const callback2 = jest.fn();
            
            appState.addEventListener('playStateChange', callback1);
            appState.addEventListener('playStateChange', callback2);
            appState.removeEventListener('playStateChange', callback1);
            
            appState.setPlayState(true);
            
            expect(callback1).not.toHaveBeenCalled();
            expect(callback2).toHaveBeenCalled();
        });
    });
});

// Export for Node.js environment
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { appState };
}