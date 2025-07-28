# 🎵 Radio Calico - Lossless Audio Streaming Platform

<div align="center">
  <img src="frontend/static/RadioCalicoLogoTM.png" alt="Radio Calico Logo" width="150" height="150">
  
  **A modern web-based radio streaming application featuring lossless audio playback, real-time metadata, and interactive user engagement.**

  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
  [![Flask](https://img.shields.io/badge/flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
  [![Test Coverage](https://img.shields.io/badge/coverage-80%25+-brightgreen.svg)](./tests/)
  [![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
</div>

## ✨ Features

### 🎧 **Audio Streaming**
- **Lossless Quality**: HLS-based FLAC/AAC streaming
- **Cross-Browser Compatible**: HLS.js integration for universal support
- **Adaptive Bitrate**: Automatic quality adjustment based on connection
- **Error Recovery**: Robust stream reconnection and error handling

### 📱 **User Interface**
- **Responsive Design**: Optimized for desktop, tablet, and mobile
- **RadioCalico Branding**: Professional design with custom color palette
- **Real-time Updates**: Live track information and album art
- **Accessibility**: Keyboard shortcuts and semantic HTML

### ⭐ **Interactive Features**
- **Rating System**: Thumbs up/down with unique user tracking
- **Browser Fingerprinting**: Anonymous user identification
- **Recently Played**: Last 5 tracks with artist information
- **Visual Feedback**: Animated controls and status indicators

### 🔧 **Technical Excellence**
- **Modular Architecture**: Clean separation of backend/frontend
- **Security First**: Environment-based configuration, input validation
- **80%+ Test Coverage**: Comprehensive testing framework
- **Production Ready**: Logging, error handling, monitoring

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Modern web browser with JavaScript enabled

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/RadioStation-ClaudeCode.git
   cd RadioStation-ClaudeCode
   ```

2. **Set up Python environment**
   ```bash
   # Create virtual environment (recommended)
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

4. **Run the application**
   ```bash
   python backend/app.py
   ```

5. **Open your browser**
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
│   ├── 📂 models/             # Database models
│   └── 📂 utils/              # Utility functions
├── 📂 frontend/               # Frontend assets
│   ├── 📂 templates/          # HTML templates
│   ├── 📂 css/                # Modular stylesheets
│   ├── 📂 js/                 # JavaScript modules
│   └── 📂 static/             # Static assets
├── 📂 tests/                  # Comprehensive test suite
│   ├── 📂 unit/               # Unit tests
│   ├── 📂 integration/        # Integration tests
│   ├── 📂 frontend/           # JavaScript tests
│   └── 📂 utils/              # Test utilities
├── 📄 .env.example            # Environment configuration template
├── 📄 requirements.txt        # Python dependencies
├── 📄 CLAUDE.md               # AI development memory
└── 📄 PROJECT.md              # Detailed project documentation
```

## 🎨 RadioCalico Brand

### Color Palette
- **Mint**: `#D8F2D5` - Light backgrounds and accents
- **Forest Green**: `#1F4E23` - Primary brand color
- **Teal**: `#38A29D` - Interactive elements
- **Calico Orange**: `#EFA63C` - Highlights and badges
- **Charcoal**: `#231F20` - Text and dark elements

### Design Philosophy
- **Clean & Modern**: Minimalist interface focusing on content
- **Accessible**: High contrast, clear typography, keyboard navigation
- **Responsive**: Mobile-first design with desktop enhancements
- **Playful**: Cat-themed branding with professional execution

## 🔧 API Documentation

### Stream Information
```http
GET /api/stream/info
```

### Track Ratings
```http
POST /api/ratings
Content-Type: application/json

{
  "track_id": "artist-song-title",
  "rating": "up|down|null",
  "user_fingerprint": "unique_user_id"
}
```

### Get Track Ratings
```http
GET /api/ratings/{track_id}?fingerprint={user_fingerprint}
```

**Response:**
```json
{
  "success": true,
  "track_id": "artist-song-title",
  "ratings": { "up": 15, "down": 3 },
  "user_rating": "up"
}
```

## 🧪 Testing

### Comprehensive Test Suite
- **80%+ Code Coverage**: Rigorous testing standards
- **Multiple Test Types**: Unit, integration, and frontend tests
- **Mock Support**: External API and browser simulation
- **CI/CD Ready**: Automated testing pipeline

### Running Tests
```bash
# Backend tests with coverage
pytest --cov=backend --cov-report=html

# Frontend tests
cd tests/frontend && npm test

# Specific test categories
pytest -m unit              # Unit tests only
pytest -m integration       # Integration tests only
pytest -m api              # API tests only
```

## 🚀 Deployment

### Development
```bash
python backend/app.py
```

### Production
```bash
# Using Gunicorn
pip install gunicorn
gunicorn --bind 0.0.0.0:8000 --workers 4 backend.app:create_app()
```

### Environment Variables
```env
# Required configuration
FLASK_SECRET_KEY=your_secret_key_here
DATABASE_PATH=radio.db
STREAM_URL=https://your-stream-url.com/live.m3u8

# Optional configuration  
FLASK_DEBUG=False
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
LOG_LEVEL=INFO
```

## 🛠️ Development

### Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Code Style
- **Python**: Black formatting, PEP 8 compliance
- **JavaScript**: ES6+ modules with consistent naming
- **CSS**: BEM methodology with CSS custom properties
- **Git**: Conventional commit messages

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt

# Install pre-commit hooks (optional)
pre-commit install

# Run code formatting
black backend/
isort backend/

# Run linting
flake8 backend/
```

## 📊 Technology Stack

### Backend
- **Flask**: Python web framework
- **SQLite**: Lightweight database
- **Python-dotenv**: Environment management
- **Structlog**: Structured logging

### Frontend
- **Vanilla JavaScript**: ES6+ modules
- **HLS.js**: HTTP Live Streaming support
- **CSS3**: Modern styling with custom properties
- **Responsive Design**: Mobile-first approach

### Testing
- **Pytest**: Python testing framework
- **Jest**: JavaScript testing framework
- **Coverage.py**: Code coverage analysis
- **Factory Boy**: Test data generation

## 🌟 Features Showcase

### Audio Player
- **Play/Pause Control**: Large, accessible button with animations
- **Volume Control**: Custom-styled range slider
- **Stream Status**: Real-time connection status
- **Keyboard Shortcuts**: Spacebar for play/pause

### Track Display
- **Album Art**: 500x500px with 3D perspective effects
- **Track Information**: Artist, title, album with real-time updates
- **Quality Indicators**: Bit depth and sample rate display
- **Track Badges**: New, Summer, Gaming classifications

### Rating System
- **Anonymous Voting**: Browser fingerprinting for unique users
- **Real-time Counts**: Live update of thumbs up/down
- **Visual Feedback**: Animated button states
- **Persistent Storage**: SQLite database with optimized queries

## 📈 Performance

### Optimizations
- **Modular Loading**: Separate CSS/JS files for better caching
- **Image Optimization**: Proper sizing and lazy loading
- **Database Indexing**: Optimized queries for ratings
- **Error Recovery**: Graceful handling of network issues

### Browser Support
- **Chrome**: 85+ (full HLS.js support)
- **Firefox**: 80+ (full HLS.js support)
- **Safari**: 14+ (native HLS support)
- **Edge**: 85+ (full HLS.js support)
- **Mobile**: iOS Safari 14+, Android Chrome 85+

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **HLS.js Team**: For excellent HTTP Live Streaming support
- **Flask Community**: For the robust web framework
- **RadioCalico Design**: For the beautiful brand identity
- **Open Source Contributors**: For inspiration and best practices

## 📞 Support

- **Documentation**: Check [PROJECT.md](PROJECT.md) for detailed docs
- **Issues**: Report bugs via GitHub Issues
- **Development**: See [CLAUDE.md](CLAUDE.md) for technical details

---

<div align="center">
  <strong>🎵 Built with ❤️ for music lovers everywhere 🎵</strong>
  
  [Demo](http://your-demo-url.com) • [Documentation](PROJECT.md) • [Report Bug](../../issues) • [Request Feature](../../issues)
</div>