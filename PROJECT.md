# Radio Sahoo - Lossless Audio Streaming Platform

A modern web-based radio streaming application featuring lossless audio playback, real-time metadata, and an interactive rating system.

## 🎵 Features

### Core Functionality
- **Lossless Audio Streaming**: HLS-based FLAC/AAC streaming with cross-browser compatibility
- **Real-time Metadata**: Live track information, album art, and artist details
- **Interactive Rating System**: Thumbs up/down rating with unique user tracking
- **Recently Played**: Display of last 5 tracks with artist information
- **Responsive Design**: Mobile-friendly interface with RadioSahoo branding

### Technical Features
- **Modern Architecture**: Modular Flask backend with clean separation of concerns
- **Security**: Environment-based configuration, input validation, and XSS protection
- **Performance**: Optimized HLS.js integration with error recovery
- **Accessibility**: Keyboard shortcuts and semantic HTML structure
- **Monitoring**: Structured logging and health check endpoints

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Modern web browser with JavaScript enabled

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd RadioStation-ClaudeCode
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment setup**
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

4. **Run the application**
   ```bash
   python backend/app.py
   ```

5. **Access the radio player**
   ```
   http://127.0.0.1:5000/radio
   ```

## 📁 Project Structure

```
RadioStation-ClaudeCode/
├── 📂 backend/                 # Flask backend application
│   ├── 📄 app.py              # Main application entry point
│   ├── 📄 config.py           # Configuration management
│   ├── 📂 api/                # API route handlers
│   │   ├── 📄 ratings.py      # Track rating endpoints
│   │   ├── 📄 users.py        # User management
│   │   ├── 📄 posts.py        # Post management
│   │   └── 📄 stream.py       # Stream information
│   ├── 📂 models/             # Database models
│   │   ├── 📄 database.py     # Database connection & init
│   │   ├── 📄 rating.py       # Rating model
│   │   ├── 📄 user.py         # User model
│   │   └── 📄 post.py         # Post model
│   └── 📂 utils/              # Utility functions
│       ├── 📄 validation.py   # Input validation
│       ├── 📄 responses.py    # API response helpers
│       └── 📄 logging_config.py # Logging configuration
├── 📂 frontend/               # Frontend assets
│   ├── 📂 templates/          # HTML templates
│   │   └── 📄 radio.html      # Main radio interface
│   ├── 📂 css/                # Stylesheets
│   │   ├── 📄 variables.css   # CSS custom properties
│   │   ├── 📄 base.css        # Base styles
│   │   └── 📂 components/     # Component-specific styles
│   ├── 📂 js/                 # JavaScript modules
│   │   ├── 📂 modules/        # Core application modules
│   │   └── 📄 main.js         # Application entry point
│   └── 📂 static/             # Static assets (images, icons)
├── 📂 docs/                   # Documentation
├── 📂 tests/                  # Test files
├── 📄 .env.example            # Environment configuration template
├── 📄 .gitignore              # Git ignore rules
├── 📄 requirements.txt        # Python dependencies
├── 📄 CLAUDE.md               # Claude AI memory file
└── 📄 PROJECT.md              # This file
```

## 🎨 RadioSahoo Brand Guidelines

### Color Palette
- **Mint**: `#D8F2D5` - Light backgrounds and accents
- **Forest Green**: `#1F4E23` - Primary brand color
- **Teal**: `#38A29D` - Interactive elements and highlights
- **Calico Orange**: `#EFA63C` - Warning states and badges
- **Charcoal**: `#231F20` - Text and dark elements
- **Cream**: `#F5EADA` - Control backgrounds
- **White**: `#FFFFFF` - Main backgrounds

### Typography
- **Primary Font**: Montserrat (headings, branding)
- **Secondary Font**: Open Sans (body text, UI elements)

### Logo
- Cat with headphones design representing audio focus
- Circular green background with TM mark
- 50x50px standard size in navigation

## 🔧 API Documentation

### Ratings API

#### Create/Update Rating
```http
POST /api/ratings
Content-Type: application/json

{
  "track_id": "artist-song-title",
  "rating": "up|down|null",
  "user_fingerprint": "unique_user_id"
}
```

#### Get Track Ratings
```http
GET /api/ratings/{track_id}?fingerprint={user_fingerprint}
```

**Response:**
```json
{
  "success": true,
  "track_id": "artist-song-title",
  "ratings": {
    "up": 15,
    "down": 3
  },
  "user_rating": "up"
}
```

### Stream API

#### Stream Information
```http
GET /api/stream/info
```

#### Stream Status Check
```http
GET /api/stream/status
```

#### Metadata Proxy
```http
GET /api/stream/metadata
```

### Health Check
```http
GET /health
```

## 🛠️ Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```env
# API Keys
CLAUDE_API_KEY=your_api_key_here

# Database
DATABASE_PATH=radio.db

# Stream Configuration
STREAM_URL=https://d3d4yli4hf5bmh.cloudfront.net/hls/live.m3u8
METADATA_URL=https://d3d4yli4hf5bmh.cloudfront.net/metadatav2.json
COVER_ART_URL=https://d3d4yli4hf5bmh.cloudfront.net/cover.jpg

# Flask Configuration
FLASK_SECRET_KEY=your_secret_key_here
FLASK_DEBUG=False
FLASK_HOST=127.0.0.1
FLASK_PORT=5000

# Security
ALLOWED_ORIGINS=http://localhost:5000,http://127.0.0.1:5000

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/radio.log
```

## 🎮 User Interface Controls

### Keyboard Shortcuts
- **Spacebar**: Play/Pause toggle
- **Click**: All interface elements are click-responsive

### Player Controls
- **Play/Pause Button**: Large gradient button with animations
- **Reload Button**: Refresh stream connection
- **Stop Button**: Stop playback and reset position
- **Volume Slider**: Adjust audio volume (0-100%)

### Rating System
- **👍 Thumbs Up**: Rate track positively
- **👎 Thumbs Down**: Rate track negatively
- **Click again**: Remove your rating
- **Real-time Counts**: See other users' ratings

## 🔒 Security Features

### Implemented Security Measures
- ✅ Environment variable configuration (no hardcoded secrets)
- ✅ Input validation and sanitization
- ✅ SQL injection protection via parameterized queries
- ✅ XSS prevention through HTML escaping
- ✅ CORS configuration for allowed origins
- ✅ Error handling without information disclosure

### User Privacy
- Browser fingerprinting for unique identification (no personal data stored)
- No user registration required
- No tracking cookies or persistent storage of personal information

## 📱 Browser Compatibility

### Supported Browsers
- **Chrome**: 85+ (full HLS.js support)
- **Firefox**: 80+ (full HLS.js support) 
- **Safari**: 14+ (native HLS support)
- **Edge**: 85+ (full HLS.js support)

### Mobile Compatibility
- **iOS Safari**: 14+ (native HLS)
- **Android Chrome**: 85+ (HLS.js)
- **Responsive design**: Optimized for all screen sizes

## 🧪 Testing

### Test Framework Overview
Radio Calico includes a comprehensive test suite with **80%+ code coverage** covering:

- **Unit Tests**: Database models, utility functions, validation
- **Integration Tests**: API endpoints, error handling, application flow
- **Frontend Tests**: JavaScript modules, state management, UI components

### Test Structure
```
tests/
├── conftest.py              # Pytest configuration and fixtures
├── pytest.ini              # Test settings and coverage config
├── unit/                    # Unit tests
│   ├── test_models.py       # Database model tests
│   └── test_utils.py        # Utility function tests
├── integration/             # Integration tests
│   ├── test_api_ratings.py  # Rating API tests
│   ├── test_api_users.py    # User API tests
│   ├── test_api_stream.py   # Stream API tests
│   └── test_app.py          # Main application tests
├── frontend/                # Frontend JavaScript tests
│   ├── package.json         # Jest configuration
│   ├── test_state.js        # State management tests
│   └── test_metadata.js     # Metadata handling tests
└── utils/                   # Test utilities and helpers
```

### Running Tests

#### Backend Tests (Python)
```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests with coverage
pytest --cov=backend --cov-report=html

# Run specific test categories
pytest tests/unit/           # Unit tests only
pytest tests/integration/    # Integration tests only
pytest -m api               # API tests only
pytest -m database          # Database tests only

# Run with verbose output
pytest -v

# Generate coverage report
pytest --cov=backend --cov-report=html
open tests/coverage/html/index.html
```

#### Frontend Tests (JavaScript)
```bash
# Navigate to frontend tests
cd tests/frontend

# Install dependencies
npm install

# Run tests
npm test

# Run with coverage
npm run test:coverage

# Watch mode for development
npm run test:watch
```

### Test Features

#### Database Testing
- **In-memory SQLite**: Fast, isolated test database
- **Fixtures**: Pre-configured test data
- **Transaction Rollback**: Clean state between tests
- **Mock Connections**: Simulated database errors

#### API Testing
- **Complete Coverage**: All endpoints tested
- **Error Scenarios**: 400, 404, 500 error handling
- **Request Validation**: Input validation testing
- **Response Validation**: JSON schema verification
- **Authentication**: Security testing

#### Frontend Testing
- **Module Testing**: Individual JavaScript components
- **State Management**: AppState functionality
- **Event Handling**: User interaction simulation
- **Mock APIs**: External service mocking
- **DOM Manipulation**: Virtual DOM testing

#### Mock Support
- **HTTP Requests**: External API mocking
- **Browser APIs**: Canvas, localStorage, fingerprinting
- **Audio Player**: HLS.js mocking
- **Time Functions**: Consistent timestamps

### Test Data and Fixtures

#### Sample Data
```python
@pytest.fixture
def sample_user_data():
    return {
        'name': 'John Doe',
        'email': 'john@example.com'
    }

@pytest.fixture
def sample_rating_data():
    return {
        'track_id': 'test-artist-test-song',
        'rating': 'up',
        'user_fingerprint': 'test-fingerprint-123'
    }
```

#### Test Helpers
```python
from tests.utils import APITestHelper, DatabaseTestHelper

# Create test user
response = helpers.create_test_user(client, user_data)

# Assert response format
APITestHelper.assert_success_response(response.get_json())
```

### Coverage Requirements
- **Minimum Coverage**: 80% for all modules
- **Critical Paths**: 95% for core functionality
- **Exclusions**: Test files, migrations, configuration

### Continuous Integration
```yaml
# GitHub Actions example
- name: Run Tests
  run: |
    pip install -r requirements.txt
    pytest --cov=backend --cov-report=xml --cov-fail-under=80
    
- name: Frontend Tests
  run: |
    cd tests/frontend
    npm install
    npm test -- --coverage --watchAll=false
```

### Manual Testing Checklist
- [ ] Audio playback starts without errors
- [ ] Play/pause controls work correctly
- [ ] Volume control adjusts audio level
- [ ] Album art updates with track changes
- [ ] Rating system saves and displays correctly
- [ ] Recently played list updates
- [ ] Responsive design on mobile devices
- [ ] Keyboard shortcuts function properly
- [ ] Error handling displays appropriate messages
- [ ] Browser fingerprinting works correctly
- [ ] HLS stream recovery functions properly

## 🚀 Deployment

### Production Considerations
1. **Environment**: Use production WSGI server (gunicorn, uWSGI)
2. **Database**: Consider PostgreSQL for production scale
3. **Secrets**: Use secure secret management
4. **Logging**: Configure proper log rotation
5. **Monitoring**: Implement health checks and metrics
6. **HTTPS**: Enable SSL/TLS for secure connections

### Example Production Command
```bash
gunicorn --bind 0.0.0.0:8000 --workers 4 backend.app:create_app()
```

## 🤝 Contributing

### Development Setup
1. Create virtual environment
2. Install dependencies from `requirements.txt`
3. Set up pre-commit hooks
4. Follow existing code style and patterns

### Code Style
- **Python**: Follow PEP 8 guidelines
- **JavaScript**: ES6+ modules with consistent naming
- **CSS**: Use CSS custom properties and BEM methodology
- **Git**: Conventional commit messages

## 📊 Performance Monitoring

### Metrics to Monitor
- **Stream Health**: Connection status and error rates
- **User Engagement**: Rating activity and session duration
- **Performance**: Page load times and audio latency
- **Errors**: Application errors and recovery rates

### Logging
Structured logging is configured with multiple levels:
- **INFO**: General application events
- **WARNING**: Non-critical issues
- **ERROR**: Error conditions requiring attention
- **DEBUG**: Detailed diagnostic information

## 🔮 Future Roadmap

### Short-term Enhancements
- [ ] User authentication and profiles
- [ ] Playlist creation and management
- [ ] Advanced audio controls (equalizer)
- [ ] Social sharing features

### Long-term Vision
- [ ] Multi-station support
- [ ] Real-time chat during streams
- [ ] Mobile application
- [ ] Advanced analytics dashboard
- [ ] Content recommendation engine

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Common Issues
1. **No Audio**: Check browser permissions and HLS.js loading
2. **Rating Not Saving**: Verify API connectivity and fingerprint generation
3. **Metadata Not Loading**: Check stream URL accessibility
4. **Mobile Issues**: Ensure touch events are properly handled

### Getting Help
- Check the CLAUDE.md file for detailed technical information
- Review browser console for JavaScript errors
- Verify environment configuration
- Check application logs for server-side issues

---

**Radio Calico** - Bringing lossless audio streaming to the web with style and functionality. 🎵