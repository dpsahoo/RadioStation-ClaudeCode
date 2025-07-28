"""Integration tests for stream API endpoints."""

import pytest
from unittest.mock import patch


class TestStreamAPI:
    """Test cases for stream API endpoints."""
    
    def test_stream_info(self, client, test_config):
        """Test getting stream information."""
        response = client.get('/api/stream/info')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'stream_url' in data
        assert 'metadata_url' in data
        assert 'cover_art_url' in data
        assert data['format'] == 'HLS (HTTP Live Streaming)'
        assert data['quality'] == 'Lossless FLAC / AAC'
        assert data['protocol'] == 'HTTPS'
    
    def test_stream_metadata_success(self, client, mock_requests, sample_metadata):
        """Test successful metadata retrieval."""
        mock_requests['response'].json.return_value = sample_metadata
        
        response = client.get('/api/stream/metadata')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'metadata' in data
        assert data['metadata']['artist'] == sample_metadata['artist']
        assert data['metadata']['title'] == sample_metadata['title']
    
    def test_stream_metadata_request_error(self, client, mock_requests):
        """Test metadata retrieval with request error."""
        import requests
        mock_requests['get'].side_effect = requests.RequestException("Connection failed")
        
        response = client.get('/api/stream/metadata')
        
        assert response.status_code == 502
        data = response.get_json()
        assert data['success'] is False
        assert 'Failed to fetch metadata' in data['error']
    
    def test_stream_metadata_timeout(self, client, mock_requests):
        """Test metadata retrieval with timeout."""
        import requests
        mock_requests['get'].side_effect = requests.Timeout("Request timeout")
        
        response = client.get('/api/stream/metadata')
        
        assert response.status_code == 502
        data = response.get_json()
        assert data['success'] is False
    
    def test_stream_status_online(self, client, mock_requests):
        """Test stream status when stream is online."""
        mock_requests['response'].status_code = 200
        mock_requests['response'].headers = {
            'content-type': 'application/vnd.apple.mpegurl',
            'server': 'nginx/1.24.0'
        }
        
        response = client.get('/api/stream/status')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['status'] == 'online'
        assert 'stream_url' in data
        assert 'content_type' in data
        assert 'server' in data
    
    def test_stream_status_offline(self, client, mock_requests):
        """Test stream status when stream is offline."""
        mock_requests['response'].status_code = 404
        mock_requests['head'].return_value = mock_requests['response']
        
        response = client.get('/api/stream/status')
        
        assert response.status_code == 502
        data = response.get_json()
        assert data['success'] is False
        assert 'unavailable' in data['error']
    
    def test_stream_status_connection_error(self, client, mock_requests):
        """Test stream status with connection error."""
        import requests
        mock_requests['head'].side_effect = requests.ConnectionError("Connection failed")
        
        response = client.get('/api/stream/status')
        
        assert response.status_code == 502
        data = response.get_json()
        assert data['success'] is False
        assert 'unavailable' in data['error']
    
    def test_stream_status_timeout(self, client, mock_requests):
        """Test stream status with timeout."""
        import requests
        mock_requests['head'].side_effect = requests.Timeout("Request timeout")
        
        response = client.get('/api/stream/status')
        
        assert response.status_code == 502
        data = response.get_json()
        assert data['success'] is False