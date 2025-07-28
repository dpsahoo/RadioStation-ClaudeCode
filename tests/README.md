# Radio Sahoo Test Suite

Comprehensive testing framework for the Radio Sahoo application, covering backend API endpoints, database models, utility functions, and frontend JavaScript modules.

## 🧪 Test Structure

```
tests/
├── conftest.py              # Pytest configuration and fixtures
├── pytest.ini              # Pytest settings
├── README.md               # This file
├── .gitignore              # Test-specific Git ignore rules
├── unit/                   # Unit tests
│   ├── test_models.py      # Database model tests
│   └── test_utils.py       # Utility function tests
├── integration/            # Integration tests
│   ├── test_api_ratings.py # Rating API endpoint tests
│   ├── test_api_users.py   # User API endpoint tests
│   ├── test_api_stream.py  # Stream API endpoint tests
│   └── test_app.py         # Main application tests
├── frontend/               # Frontend JavaScript tests
│   ├── package.json        # Jest configuration
│   ├── test-setup.js       # Jest test setup
│   ├── test_state.js       # AppState module tests
│   └── test_metadata.js    # MetadataManager tests
└── utils/                  # Test utilities
    ├── test_helpers.py     # Test helper functions
    └── __init__.py         # Package init
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+ (for frontend tests)
- All dependencies from `requirements.txt`

### Installation

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Install frontend test dependencies**:
   ```bash
   cd tests/frontend
   npm install
   ```

## 🔧 Running Tests

### Backend Tests (Python)

#### Run All Tests
```bash
# From project root
pytest

# With verbose output
pytest -v

# With coverage report
pytest --cov=backend --cov-report=html
```

#### Run Specific Test Categories
```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# Specific test file
pytest tests/unit/test_models.py

# Specific test class
pytest tests/unit/test_models.py::TestUserModel

# Specific test method
pytest tests/unit/test_models.py::TestUserModel::test_create_user_success
```

#### Run Tests with Markers
```bash
# Database tests only
pytest -m database

# API tests only
pytest -m api

# Skip slow tests
pytest -m "not slow"
```

### Frontend Tests (JavaScript)

```bash
# Navigate to frontend test directory
cd tests/frontend

# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage
```

## 📊 Test Coverage

### Backend Coverage
Target: **80%** minimum coverage

```bash
# Generate coverage report
pytest --cov=backend --cov-report=html

# View HTML report
open tests/coverage/html/index.html
```

### Frontend Coverage
```bash
cd tests/frontend
npm run test:coverage
```

## 🧪 Test Categories

### Unit Tests
Test individual components in isolation:
- **Database Models**: User, Post, Rating models
- **Utility Functions**: Validation, responses, logging
- **Configuration**: Environment handling

### Integration Tests
Test component interactions:
- **API Endpoints**: All REST API routes
- **Database Integration**: Real database operations
- **Error Handling**: Application-level error responses
- **Authentication**: Security and validation

### Frontend Tests
Test JavaScript modules:
- **State Management**: AppState functionality
- **Player Logic**: Audio player controls
- **Metadata Handling**: Real-time updates
- **Rating System**: User interaction handling

## 🔧 Test Configuration

### Pytest Configuration (`pytest.ini`)
- Test discovery patterns
- Coverage settings
- Marker definitions
- Environment variables

### Test Fixtures (`conftest.py`)
- Database fixtures with in-memory SQLite
- Mock HTTP requests
- Sample test data
- Application configuration

### Jest Configuration (`frontend/package.json`)
- JSDOM environment for browser simulation
- Test setup and mocking
- Coverage collection

## 📝 Writing Tests

### Backend Test Example
```python
def test_create_user_success(client, sample_user_data, auth_headers):
    """Test successful user creation."""
    response = client.post('/api/users',
                         json=sample_user_data,
                         headers=auth_headers)
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['success'] is True
    assert data['name'] == sample_user_data['name']
```

### Frontend Test Example
```javascript
test('should update play state and emit event', () => {
    const callback = jest.fn();
    appState.addEventListener('playStateChange', callback);
    
    appState.setPlayState(true);
    
    expect(appState.isPlaying).toBe(true);
    expect(callback).toHaveBeenCalledWith({ isPlaying: true });
});
```

## 🎯 Test Data

### Fixtures and Factories
- **Database Fixtures**: Pre-populated test database
- **API Payloads**: Standard request/response data
- **Mock Responses**: External API simulation
- **User Data**: Realistic test users and content

### Test Helpers
- **DatabaseTestHelper**: Database operations
- **APITestHelper**: HTTP request utilities
- **MockHelper**: Mock object creation
- **ValidationTestHelper**: Input validation testing

## 🐛 Debugging Tests

### Common Issues

1. **Database Connection Errors**
   ```bash
   # Ensure test database is properly mocked
   pytest tests/unit/test_models.py -v
   ```

2. **Import Errors**
   ```bash
   # Check Python path configuration
   python -m pytest tests/
   ```

3. **Frontend Module Not Found**
   ```bash
   # Install dependencies
   cd tests/frontend && npm install
   ```

### Debug Specific Tests
```bash
# Run with debug output
pytest tests/unit/test_models.py::TestUserModel::test_create_user_success -v -s

# Drop into debugger on failure
pytest --pdb tests/integration/test_api_users.py
```

## 📈 Continuous Integration

### Test Commands for CI/CD
```bash
# Full test suite with coverage
pytest --cov=backend --cov-report=xml --cov-fail-under=80

# Frontend tests
cd tests/frontend && npm test -- --coverage --watchAll=false

# Code quality checks
black --check backend/
flake8 backend/
isort --check-only backend/
```

### GitHub Actions Example
```yaml
- name: Run Backend Tests
  run: |
    pip install -r requirements.txt
    pytest --cov=backend --cov-report=xml

- name: Run Frontend Tests  
  run: |
    cd tests/frontend
    npm install
    npm test -- --coverage --watchAll=false
```

## 🔍 Test Markers

Available test markers for selective test running:

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.slow` - Slow-running tests
- `@pytest.mark.api` - API endpoint tests
- `@pytest.mark.database` - Database-related tests
- `@pytest.mark.frontend` - Frontend tests

## 📚 Best Practices

### Test Organization
1. Group related tests in classes
2. Use descriptive test names
3. Follow AAA pattern (Arrange, Act, Assert)
4. Keep tests isolated and independent

### Test Data
1. Use fixtures for reusable test data
2. Create realistic but minimal test scenarios
3. Clean up after tests automatically
4. Use factory patterns for complex data

### Mocking
1. Mock external dependencies
2. Use dependency injection where possible
3. Verify mock interactions
4. Reset mocks between tests

### Performance
1. Use in-memory databases for speed
2. Minimize I/O operations in tests
3. Run slow tests separately
4. Parallelize test execution when possible

## 🆘 Troubleshooting

### Common Solutions

1. **Tests fail with import errors**:
   - Check `PYTHONPATH` includes project root
   - Verify all dependencies are installed

2. **Database tests fail**:
   - Ensure in-memory database is being used
   - Check fixture configuration in `conftest.py`

3. **Frontend tests fail**:
   - Verify Node.js and npm are installed
   - Check Jest configuration in `package.json`

4. **Coverage too low**:
   - Identify untested code with `--cov-report=html`
   - Add tests for critical paths first
   - Consider excluding test files from coverage

### Getting Help

- Check test output for specific error messages
- Review test configuration files for issues
- Ensure all dependencies are correctly installed
- Verify environment variables are set correctly

---

**Happy Testing!** 🧪✅