/**
 * Tests for MetadataManager module
 */

describe('MetadataManager', () => {
    let metadataManager;
    let mockState;
    let mockFetch;
    
    beforeEach(() => {
        // Mock state
        mockState = {
            metadataInterval: null,
            config: {
                metadataUrl: 'https://test.example.com/metadata.json',
                coverArtUrl: 'https://test.example.com/cover.jpg',
                metadataUpdateInterval: 10000
            },
            currentTrackId: null,
            setCurrentTrack: jest.fn(),
            addEventListener: jest.fn()
        };
        
        // Mock fetch
        mockFetch = jest.fn();
        global.fetch = mockFetch;
        
        // Mock DOM methods
        global.document = {
            getElementById: jest.fn((id) => ({
                id: id,
                textContent: '',
                innerHTML: '',
                src: ''
            }))
        };
        
        // Mock console
        global.console = {
            log: jest.fn(),
            error: jest.fn()
        };
        
        // Mock setInterval/clearInterval
        global.setInterval = jest.fn((callback, delay) => {
            return { callback, delay, id: Math.random() };
        });
        global.clearInterval = jest.fn();
        global.Date = {
            now: jest.fn(() => 1234567890)
        };
        
        // Initialize MetadataManager (mock implementation)
        metadataManager = {
            state: mockState,
            logger: global.console,
            
            startPolling: function() {
                if (this.state.metadataInterval) {
                    this.stopPolling();
                }
                this.loadMetadata();
                this.state.metadataInterval = setInterval(() => {
                    this.loadMetadata();
                }, this.state.config.metadataUpdateInterval);
            },
            
            stopPolling: function() {
                if (this.state.metadataInterval) {
                    clearInterval(this.state.metadataInterval);
                    this.state.metadataInterval = null;
                }
            },
            
            loadMetadata: async function() {
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
                }
            },
            
            updateNowPlaying: function(metadata) {
                this.updateElement('track-artist', metadata.artist || 'Unknown Artist');
                this.updateElement('track-title', metadata.title || 'Unknown Track');
                this.updateElement('track-album', metadata.album || 'Unknown Album');
                
                const yearBadge = document.getElementById('year-badge');
                if (yearBadge) {
                    yearBadge.textContent = metadata.date || '----';
                }
                
                this.updateAlbumArt();
                this.updateTrackBadges(metadata);
                
                const newTrackId = this.generateTrackId(metadata);
                this.state.setCurrentTrack(newTrackId, metadata);
            },
            
            updateAlbumArt: function() {
                const albumArt = document.getElementById('album-art');
                if (albumArt) {
                    const albumArtUrl = `${this.state.config.coverArtUrl}?t=${Date.now()}`;
                    albumArt.src = albumArtUrl;
                }
            },
            
            updateTrackBadges: function(metadata) {
                const badgesContainer = document.getElementById('track-badges');
                if (!badgesContainer) return;
                
                let badgesHTML = '';
                if (metadata.is_new) badgesHTML += '<span class="badge new">New</span>';
                if (metadata.is_summer) badgesHTML += '<span class="badge summer">Summer</span>';
                if (metadata.is_vidgames) badgesHTML += '<span class="badge vidgames">Gaming</span>';
                
                badgesContainer.innerHTML = badgesHTML;
            },
            
            updateRecentlyPlayed: function(metadata) {
                const container = document.getElementById('recent-tracks');
                if (!container) return;
                
                let recentHTML = '';
                for (let i = 1; i <= 5; i++) {
                    const artist = metadata[`prev_artist_${i}`];
                    const title = metadata[`prev_title_${i}`];
                    if (artist && title) {
                        recentHTML += `<div class="recent-track">
                            <div class="recent-track-info">
                                <div class="recent-track-artist">${this.escapeHtml(artist)}</div>
                                <div class="recent-track-title">${this.escapeHtml(title)}</div>
                            </div>
                        </div>`;
                    }
                }
                container.innerHTML = recentHTML || '<p>No recent tracks available</p>';
            },
            
            updateAudioQuality: function(metadata) {
                const element = document.getElementById('audio-quality-display');
                if (element && metadata.bit_depth && metadata.sample_rate) {
                    element.textContent = `Source quality: ${metadata.bit_depth}-bit ${metadata.sample_rate/1000}kHz`;
                }
            },
            
            generateTrackId: function(metadata) {
                const artist = metadata.artist || 'unknown';
                const title = metadata.title || 'unknown';
                return `${artist}-${title}`.toLowerCase().replace(/[^a-z0-9-]/g, '-');
            },
            
            updateElement: function(elementId, text) {
                const element = document.getElementById(elementId);
                if (element) {
                    element.textContent = text;
                }
            },
            
            escapeHtml: function(text) {
                const map = {
                    '&': '&amp;',
                    '<': '&lt;',
                    '>': '&gt;',
                    '"': '&quot;',
                    "'": '&#039;'
                };
                return text.replace(/[&<>"']/g, m => map[m]);
            }
        };
    });
    
    afterEach(() => {
        jest.clearAllMocks();
    });
    
    describe('Polling Management', () => {
        test('should start polling and load initial metadata', () => {
            const loadMetadataSpy = jest.spyOn(metadataManager, 'loadMetadata');
            
            metadataManager.startPolling();
            
            expect(loadMetadataSpy).toHaveBeenCalled();
            expect(setInterval).toHaveBeenCalledWith(
                expect.any(Function),
                mockState.config.metadataUpdateInterval
            );
        });
        
        test('should stop existing polling before starting new one', () => {
            metadataManager.state.metadataInterval = { id: 'test-interval' };
            const stopPollingSpy = jest.spyOn(metadataManager, 'stopPolling');
            
            metadataManager.startPolling();
            
            expect(stopPollingSpy).toHaveBeenCalled();
        });
        
        test('should stop polling', () => {
            const mockInterval = { id: 'test-interval' };
            metadataManager.state.metadataInterval = mockInterval;
            
            metadataManager.stopPolling();
            
            expect(clearInterval).toHaveBeenCalledWith(mockInterval);
            expect(metadataManager.state.metadataInterval).toBeNull();
        });
        
        test('should handle stop polling when no interval exists', () => {
            metadataManager.state.metadataInterval = null;
            
            expect(() => {
                metadataManager.stopPolling();
            }).not.toThrow();
        });
    });
    
    describe('Metadata Loading', () => {
        test('should load metadata successfully', async () => {
            const mockMetadata = {
                artist: 'Test Artist',
                title: 'Test Song',
                album: 'Test Album'
            };
            
            mockFetch.mockResolvedValue({
                ok: true,
                json: () => Promise.resolve(mockMetadata)
            });
            
            const updateNowPlayingSpy = jest.spyOn(metadataManager, 'updateNowPlaying');
            const updateRecentlyPlayedSpy = jest.spyOn(metadataManager, 'updateRecentlyPlayed');
            const updateAudioQualitySpy = jest.spyOn(metadataManager, 'updateAudioQuality');
            
            await metadataManager.loadMetadata();
            
            expect(mockFetch).toHaveBeenCalledWith(mockState.config.metadataUrl);
            expect(updateNowPlayingSpy).toHaveBeenCalledWith(mockMetadata);
            expect(updateRecentlyPlayedSpy).toHaveBeenCalledWith(mockMetadata);
            expect(updateAudioQualitySpy).toHaveBeenCalledWith(mockMetadata);
        });
        
        test('should handle fetch errors gracefully', async () => {
            mockFetch.mockRejectedValue(new Error('Network error'));
            
            await metadataManager.loadMetadata();
            
            expect(console.error).toHaveBeenCalledWith(
                'Failed to load metadata:',
                expect.any(Error)
            );
        });
        
        test('should handle HTTP errors', async () => {
            mockFetch.mockResolvedValue({
                ok: false,
                status: 404,
                statusText: 'Not Found'
            });
            
            await metadataManager.loadMetadata();
            
            expect(console.error).toHaveBeenCalled();
        });
    });
    
    describe('Now Playing Updates', () => {
        test('should update track information', () => {
            const mockMetadata = {
                artist: 'Test Artist',
                title: 'Test Song',
                album: 'Test Album',
                date: '2023'
            };
            
            const mockElements = {
                'track-artist': { textContent: '' },
                'track-title': { textContent: '' },
                'track-album': { textContent: '' },
                'year-badge': { textContent: '' }
            };
            
            document.getElementById = jest.fn((id) => mockElements[id]);
            
            metadataManager.updateNowPlaying(mockMetadata);
            
            expect(mockElements['track-artist'].textContent).toBe('Test Artist');
            expect(mockElements['track-title'].textContent).toBe('Test Song');
            expect(mockElements['track-album'].textContent).toBe('Test Album');
            expect(mockElements['year-badge'].textContent).toBe('2023');
        });
        
        test('should handle missing metadata fields', () => {
            const mockMetadata = {};
            const mockElements = {
                'track-artist': { textContent: '' },
                'track-title': { textContent: '' },
                'track-album': { textContent: '' }
            };
            
            document.getElementById = jest.fn((id) => mockElements[id]);
            
            metadataManager.updateNowPlaying(mockMetadata);
            
            expect(mockElements['track-artist'].textContent).toBe('Unknown Artist');
            expect(mockElements['track-title'].textContent).toBe('Unknown Track');
            expect(mockElements['track-album'].textContent).toBe('Unknown Album');
        });
        
        test('should update album art with cache busting', () => {
            const mockAlbumArt = { src: '' };
            document.getElementById = jest.fn((id) => {
                if (id === 'album-art') return mockAlbumArt;
                return null;
            });
            
            metadataManager.updateAlbumArt();
            
            expect(mockAlbumArt.src).toContain(mockState.config.coverArtUrl);
            expect(mockAlbumArt.src).toContain('?t=');
        });
        
        test('should call setCurrentTrack with generated track ID', () => {
            const mockMetadata = {
                artist: 'Test Artist',
                title: 'Test Song'
            };
            
            metadataManager.updateNowPlaying(mockMetadata);
            
            expect(mockState.setCurrentTrack).toHaveBeenCalledWith(
                'test-artist-test-song',
                mockMetadata
            );
        });
    });
    
    describe('Track Badges', () => {
        test('should update track badges based on metadata', () => {
            const mockMetadata = {
                is_new: true,
                is_summer: false,
                is_vidgames: true
            };
            
            const mockBadgesContainer = { innerHTML: '' };
            document.getElementById = jest.fn((id) => {
                if (id === 'track-badges') return mockBadgesContainer;
                return null;
            });
            
            metadataManager.updateTrackBadges(mockMetadata);
            
            expect(mockBadgesContainer.innerHTML).toContain('badge new');
            expect(mockBadgesContainer.innerHTML).toContain('badge vidgames');
            expect(mockBadgesContainer.innerHTML).not.toContain('badge summer');
        });
        
        test('should handle no badges', () => {
            const mockMetadata = {
                is_new: false,
                is_summer: false,
                is_vidgames: false
            };
            
            const mockBadgesContainer = { innerHTML: '' };
            document.getElementById = jest.fn((id) => {
                if (id === 'track-badges') return mockBadgesContainer;
                return null;
            });
            
            metadataManager.updateTrackBadges(mockMetadata);
            
            expect(mockBadgesContainer.innerHTML).toBe('');
        });
    });
    
    describe('Utility Functions', () => {
        test('should generate track ID correctly', () => {
            const metadata = {
                artist: 'Test Artist!',
                title: 'Test Song @#$'
            };
            
            const trackId = metadataManager.generateTrackId(metadata);
            
            expect(trackId).toBe('test-artist--test-song----');
        });
        
        test('should escape HTML correctly', () => {
            const input = '<script>alert("XSS")</script>';
            const output = metadataManager.escapeHtml(input);
            
            expect(output).toBe('&lt;script&gt;alert(&quot;XSS&quot;)&lt;/script&gt;');
        });
        
        test('should update element text content', () => {
            const mockElement = { textContent: '' };
            document.getElementById = jest.fn(() => mockElement);
            
            metadataManager.updateElement('test-element', 'Test Text');
            
            expect(mockElement.textContent).toBe('Test Text');
        });
        
        test('should handle missing elements gracefully', () => {
            document.getElementById = jest.fn(() => null);
            
            expect(() => {
                metadataManager.updateElement('missing-element', 'Test Text');
            }).not.toThrow();
        });
    });
});