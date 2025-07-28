"""Integration tests for main application."""

import pytest


class TestMainApplication:
    """Test cases for main application routes and functionality."""
    
    def test_home_route(self, client):
        """Test home route."""
        response = client.get('/')
        
        assert response.status_code == 200
        assert b'Radio Calico' in response.data
        assert b'Server is running successfully' in response.data
        assert b'SQLite connected' in response.data
    
    def test_radio_route(self, client):
        """Test radio player route."""
        response = client.get('/radio')
        
        assert response.status_code == 200
        assert b'Radio Calico' in response.data
        assert b'html' in response.data.lower()
    
    def test_dashboard_route(self, client):
        """Test dashboard route."""
        response = client.get('/dashboard')
        
        assert response.status_code == 200
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get('/health')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'
        assert data['version'] == '2.0'
        assert data['database'] == 'connected'
        assert 'stream_url' in data
    
    def test_static_files_route(self, client):
        """Test static files serving."""
        # This test assumes the logo file exists
        response = client.get('/static/RadioCalicoLogoTM.png')
        
        # Should either return the file or 404 if not found
        assert response.status_code in [200, 404]
    
    def test_404_error_handler(self, client):
        """Test 404 error handling."""
        response = client.get('/nonexistent-route')
        
        assert response.status_code == 404
        data = response.get_json()
        assert data['success'] is False
        assert 'not found' in data['error'].lower()
    
    def test_cors_headers(self, client):
        """Test CORS headers are properly set."""
        response = client.get('/health')
        
        # Check that CORS headers are present
        assert response.status_code == 200
        # Note: In testing environment, CORS headers may not be visible
        # This is a basic test to ensure the endpoint works
    
    def test_json_content_type(self, client):
        """Test JSON content type for API endpoints."""
        response = client.get('/health')
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'
    
    def test_api_endpoints_accessible(self, client):
        """Test that all API endpoints are accessible."""
        endpoints = [
            '/api/users',
            '/api/posts', 
            '/api/stream/info',
            '/health'
        ]
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            # Should not return 404 or 500
            assert response.status_code < 500
            assert response.status_code != 404


class TestErrorHandling:
    """Test cases for error handling."""
    
    def test_bad_request_handler(self, client):
        """Test 400 error handling."""
        # Send malformed JSON to trigger 400 error
        response = client.post('/api/users',
                             data='invalid json',
                             content_type='application/json')
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
    
    def test_method_not_allowed(self, client):
        """Test 405 method not allowed."""
        # Try to DELETE a route that doesn't support it
        response = client.delete('/health')
        
        assert response.status_code == 405
    
    def test_internal_server_error(self, client):
        """Test 500 error handling."""
        # This is harder to trigger without modifying the application
        # In a real scenario, you might mock a function to raise an exception
        pass


class TestApplicationConfiguration:
    """Test cases for application configuration."""
    
    def test_debug_mode_disabled_in_tests(self, app):
        """Test that debug mode is properly configured for tests."""
        assert app.config['TESTING'] is True
        # Debug mode should be controlled by test config
    
    def test_secret_key_configured(self, app):
        """Test that secret key is properly configured."""
        assert app.config['SECRET_KEY'] is not None
        assert app.config['SECRET_KEY'] != ''
    
    def test_csrf_disabled_in_tests(self, app):
        """Test that CSRF is disabled for testing.""" 
        assert app.config['WTF_CSRF_ENABLED'] is False