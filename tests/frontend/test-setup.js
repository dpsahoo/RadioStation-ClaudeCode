/**
 * Test setup for frontend JavaScript tests
 */

// Mock global objects that would be available in browser
global.console = {
    log: jest.fn(),
    error: jest.fn(),
    warn: jest.fn(),
    info: jest.fn()
};

// Mock fetch for API calls
global.fetch = jest.fn();

// Mock DOM APIs
global.document = {
    getElementById: jest.fn(),
    createElement: jest.fn(),
    addEventListener: jest.fn(),
    removeEventListener: jest.fn()
};

global.window = {
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    location: {
        href: 'http://localhost:3000'
    }
};

// Mock HLS.js
global.Hls = {
    isSupported: jest.fn(() => true),
    Events: {
        MEDIA_ATTACHED: 'hlsMediaAttached',
        MANIFEST_PARSED: 'hlsManifestParsed',
        ERROR: 'hlsError'
    },
    ErrorTypes: {
        NETWORK_ERROR: 'networkError',
        MEDIA_ERROR: 'mediaError'
    }
};

global.Hls.constructor = jest.fn(() => ({
    loadSource: jest.fn(),
    attachMedia: jest.fn(),
    on: jest.fn(),
    startLoad: jest.fn(),
    stopLoad: jest.fn(),
    recoverMediaError: jest.fn(),
    destroy: jest.fn()
}));

// Mock localStorage
const localStorageMock = {
    getItem: jest.fn(),
    setItem: jest.fn(),
    removeItem: jest.fn(),
    clear: jest.fn()
};
global.localStorage = localStorageMock;

// Mock sessionStorage
const sessionStorageMock = {
    getItem: jest.fn(),
    setItem: jest.fn(),
    removeItem: jest.fn(),
    clear: jest.fn()
};
global.sessionStorage = sessionStorageMock;

// Mock navigator
global.navigator = {
    userAgent: 'Mozilla/5.0 (Test Browser)',
    language: 'en-US',
    platform: 'Test Platform'
};

// Mock screen
global.screen = {
    width: 1920,
    height: 1080,
    colorDepth: 24
};

// Mock canvas for fingerprinting
global.HTMLCanvasElement.prototype.getContext = jest.fn(() => ({
    textBaseline: 'top',
    font: '14px Arial',
    fillText: jest.fn()
}));

global.HTMLCanvasElement.prototype.toDataURL = jest.fn(() => 'data:image/png;base64,test');

// Mock btoa
global.btoa = jest.fn((str) => Buffer.from(str).toString('base64'));

// Mock Date.now for consistent timestamps in tests
const mockDateNow = jest.fn(() => 1234567890);
global.Date.now = mockDateNow;

// Mock setTimeout and setInterval
global.setTimeout = jest.fn((callback, delay) => {
    return { callback, delay, id: Math.random() };
});

global.clearTimeout = jest.fn();

global.setInterval = jest.fn((callback, delay) => {
    return { callback, delay, id: Math.random() };
});

global.clearInterval = jest.fn();

// Reset all mocks before each test
beforeEach(() => {
    jest.clearAllMocks();
    
    // Reset fetch mock
    fetch.mockReset();
    
    // Reset DOM mocks
    document.getElementById.mockReset();
    document.createElement.mockReset();
    
    // Reset console mocks
    console.log.mockReset();
    console.error.mockReset();
    console.warn.mockReset();
    console.info.mockReset();
});