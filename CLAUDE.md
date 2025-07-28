# Radio Calico - Claude Memory File

## Project Overview
Radio Calico is a web-based lossless audio streaming application that plays HLS radio streams and provides track rating functionality. The project has been completely refactored for production readiness.

## Key Technologies
- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript (modular)
- **Database**: SQLite with proper schema
- **Streaming**: HLS.js for cross-browser HLS support
- **Audio Format**: FLAC/AAC lossless streaming

## Project Structure (Refactored)
```
RadioStation-ClaudeCode/
├── backend/
│   ├── app.py                  # Main Flask application
│   ├── config.py              # Environment configuration
│   ├── api/                   # API route modules
│   │   ├── ratings.py         # Track rating endpoints
│   │   ├── users.py          # User management endpoints
│   │   ├── posts.py          # Post management endpoints
│   │   └── stream.py         # Stream info endpoints
│   ├── models/               # Database models
│   │   ├── database.py       # Database connection/init
│   │   ├── rating.py         # Rating model
│   │   ├── user.py          # User model
│   │   └── post.py          # Post model
│   └── utils/               # Utility functions
│       ├── validation.py    # Input validation
│       ├── responses.py     # Standardized responses
│       └── logging_config.py # Logging setup
├── frontend/
│   ├── templates/           # HTML templates
│   │   └── radio.html       # Main radio player
│   ├── css/                # Modular stylesheets
│   │   ├── variables.css    # CSS custom properties
│   │   ├── base.css        # Base styles
│   │   └── components/     # Component-specific CSS
│   ├── js/                 # JavaScript modules
│   │   ├── modules/        # Core modules
│   │   │   ├── state.js    # Application state
│   │   │   ├── player.js   # Audio player logic
│   │   │   ├── metadata.js # Metadata management
│   │   │   └── rating.js   # Rating system
│   │   └── main.js         # Application entry point
│   └── static/             # Static assets
└── logs/                   # Application logs
```

## Core Features
1. **HLS Audio Streaming**: Cross-browser compatible lossless audio
2. **Real-time Metadata**: Track info, album art, artist details
3. **Rating System**: Thumbs up/down with unique user tracking
4. **Responsive Design**: Mobile-friendly RadioCalico branding
5. **Recently Played**: Last 5 tracks display

## Key URLs and Endpoints
- **Stream**: https://d3d4yli4hf5bmh.cloudfront.net/hls/live.m3u8
- **Metadata**: https://d3d4yli4hf5bmh.cloudfront.net/metadatav2.json
- **Cover Art**: https://d3d4yli4hf5bmh.cloudfront.net/cover.jpg

### API Endpoints
- `GET/POST /api/ratings` - Track rating management
- `GET /api/ratings/<track_id>` - Get track ratings
- `GET/POST /api/users` - User management
- `GET/POST /api/posts` - Post management
- `GET /api/stream/info` - Stream information
- `GET /api/stream/metadata` - Proxy metadata requests
- `GET /health` - Health check endpoint

## Database Schema
```sql
-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Posts table
CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT,
    user_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Ratings table
CREATE TABLE ratings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    track_id TEXT NOT NULL,
    rating TEXT CHECK(rating IN ('up', 'down')) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_fingerprint TEXT NOT NULL,
    UNIQUE(track_id, user_fingerprint)
);
```

## Environment Configuration
The application uses environment variables for configuration:
- `CLAUDE_API_KEY` - API key (moved from plain text file)
- `DATABASE_PATH` - SQLite database path
- `STREAM_URL` - HLS stream URL
- `FLASK_SECRET_KEY` - Flask secret key
- `FLASK_DEBUG` - Debug mode flag

## Security Improvements
1. ✅ **API Key Protection**: Moved to environment variables
2. ✅ **Input Validation**: Comprehensive validation for all inputs
3. ✅ **SQL Injection Protection**: Parameterized queries
4. ✅ **XSS Prevention**: HTML escaping in frontend
5. ✅ **Error Handling**: Proper error responses without data leaks

## RadioCalico Branding
- **Colors**: Mint (#D8F2D5), Forest Green (#1F4E23), Teal (#38A29D), Calico Orange (#EFA63C)
- **Typography**: Montserrat (headers), Open Sans (body text)
- **Logo**: Cat with headphones design
- **Layout**: Two-column grid with prominent 500x500px album art

## User Experience Features
1. **Play Button**: Premium gradient design with shimmer animation
2. **Album Art**: 3D perspective transform with hover effects
3. **Control Container**: Glass morphism design with subtle gradients
4. **Rating System**: Real-time thumbs up/down with visual feedback
5. **Volume Control**: Custom styled range slider

## Browser Fingerprinting
Unique user identification using:
- Canvas fingerprinting
- Navigator properties
- Screen specifications
- Timezone offset
- Storage capability detection

## Recent Refactoring (Current Session)
1. **Security**: Moved API key to environment variables, added .gitignore
2. **Architecture**: Separated backend/frontend, removed duplicate Node.js backend
3. **Code Organization**: Modular CSS/JS, proper MVC structure
4. **Configuration**: Centralized config management with environment support
5. **Error Handling**: Structured logging and standardized API responses
6. **Database**: Unified schema with proper indexes and constraints

## Development Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your values

# Run application
python backend/app.py

# Access application
http://127.0.0.1:5000/radio
```

## Common Issues & Solutions
1. **HLS Playback Issues**: Ensure HLS.js is loaded, check browser console
2. **CORS Errors**: Verify ALLOWED_ORIGINS in config
3. **Database Errors**: Check database permissions and schema
4. **Rating Not Saving**: Verify user fingerprint generation
5. **Metadata Not Loading**: Check stream URL accessibility

## Testing Checklist
- [ ] Audio playback starts/stops correctly
- [ ] Album art updates with track changes
- [ ] Rating system saves and displays counts
- [ ] Recently played list updates
- [ ] Responsive design works on mobile
- [ ] Keyboard shortcuts (spacebar for play/pause)
- [ ] Volume control functions properly

## Testing Framework
The application now includes a comprehensive test suite covering backend, frontend, and integration testing.

### Test Structure
```
tests/
├── conftest.py              # Pytest configuration and fixtures
├── unit/                    # Unit tests for models and utilities
├── integration/             # API endpoint integration tests
├── frontend/                # JavaScript module tests (Jest)
└── utils/                   # Test helper functions
```

### Test Coverage
- **Backend**: 80%+ coverage requirement with pytest-cov
- **Models**: Complete CRUD operations testing
- **API Endpoints**: All routes with success/error scenarios
- **Frontend**: State management and module testing
- **Utilities**: Validation and response helpers

### Running Tests
```bash
# Backend tests
pytest --cov=backend --cov-report=html

# Frontend tests
cd tests/frontend && npm test

# Specific test categories
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m api          # API tests only
```

### Test Features
- **Database Testing**: In-memory SQLite for fast, isolated tests
- **API Testing**: Complete HTTP request/response testing
- **Mock Support**: External API and service mocking
- **Fixtures**: Reusable test data and configurations
- **Coverage Reports**: HTML and XML coverage reporting
- **CI/CD Ready**: Configured for GitHub Actions integration

## Future Enhancements
- [ ] User authentication system
- [ ] Playlist functionality
- [ ] Social sharing features
- [ ] Advanced audio controls (EQ, filters)
- [ ] Offline mode with service workers
- [ ] Real-time chat during streams
- [ ] Advanced analytics and reporting
- [ ] Performance testing with load tests
- [ ] End-to-end testing with Selenium/Playwright

## Important Notes
- The original monolithic HTML file (1,157 lines) has been split into modular components
- HLS.js provides better cross-browser compatibility than native HTML5 audio
- Browser fingerprinting ensures unique rating counting without user registration
- The application follows Flask best practices with blueprint organization
- All CSS uses custom properties for consistent theming
- JavaScript is organized in ES6 modules for maintainability