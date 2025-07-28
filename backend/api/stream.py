"""Stream API endpoints for Radio Calico."""

from flask import Blueprint, jsonify
import logging
import requests
from ..config import config
from ..utils.responses import success_response, error_response

logger = logging.getLogger(__name__)
stream_bp = Blueprint('stream', __name__, url_prefix='/api/stream')


@stream_bp.route('/info', methods=['GET'])
def stream_info():
    """Get stream information."""
    try:
        return success_response({
            'stream_url': config.STREAM_URL,
            'metadata_url': config.METADATA_URL,
            'cover_art_url': config.COVER_ART_URL,
            'format': 'HLS (HTTP Live Streaming)',
            'quality': 'Lossless FLAC / AAC',
            'protocol': 'HTTPS'
        })
        
    except Exception as e:
        logger.error(f"Error in stream_info: {e}")
        return error_response('Internal server error', 500)


@stream_bp.route('/metadata', methods=['GET'])
def get_metadata():
    """Proxy metadata requests to avoid CORS issues."""
    try:
        response = requests.get(config.METADATA_URL, timeout=10)
        response.raise_for_status()
        
        metadata = response.json()
        
        return success_response({
            'metadata': metadata,
            'timestamp': response.headers.get('date'),
            'cache_control': response.headers.get('cache-control')
        })
        
    except requests.RequestException as e:
        logger.error(f"Error fetching metadata: {e}")
        return error_response('Failed to fetch metadata', 502)
    except Exception as e:
        logger.error(f"Error in get_metadata: {e}")
        return error_response('Internal server error', 500)


@stream_bp.route('/status', methods=['GET'])
def stream_status():
    """Check if the stream is available."""
    try:
        # Check stream availability
        response = requests.head(config.STREAM_URL, timeout=10)
        
        if response.status_code == 200:
            return success_response({
                'status': 'online',
                'stream_url': config.STREAM_URL,
                'content_type': response.headers.get('content-type'),
                'server': response.headers.get('server')
            })
        else:
            return error_response(f'Stream unavailable (HTTP {response.status_code})', 502)
            
    except requests.RequestException as e:
        logger.error(f"Stream status check failed: {e}")
        return error_response('Stream unavailable', 502)
    except Exception as e:
        logger.error(f"Error in stream_status: {e}")
        return error_response('Internal server error', 500)