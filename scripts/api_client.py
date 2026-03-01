#!/usr/bin/env python3
"""
API Client - Reusable REST API client example.

This script demonstrates a reusable REST API client with proper error handling,
authentication, and common HTTP methods. Useful for API testing and integration.
"""

import argparse
import json
import logging
import sys
from typing import Any, Dict, Optional
from urllib.parse import urljoin

try:
    import requests
    from requests.adapters import HTTPAdapter
    from requests.packages.urllib3.util.retry import Retry
except ImportError:
    print("Error: 'requests' module not found. Install it with: pip install requests")
    sys.exit(1)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class APIClient:
    """Reusable REST API client with retry logic and error handling."""

    def __init__(self, base_url: str, api_key: Optional[str] = None,
                 timeout: int = 30, max_retries: int = 3):
        """
        Initialize the API client.

        Args:
            base_url: Base URL for the API
            api_key: API key for authentication (optional)
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()

        # Configure retry strategy
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Set default headers
        self.session.headers.update({
            'User-Agent': 'Python-API-Client/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })

        # Set authentication if provided
        if api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {api_key}'
            })

    def _build_url(self, endpoint: str) -> str:
        """
        Build full URL from endpoint.

        Args:
            endpoint: API endpoint path

        Returns:
            Full URL
        """
        return urljoin(self.base_url + '/', endpoint.lstrip('/'))

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Handle API response and errors.

        Args:
            response: Response object

        Returns:
            Response data as dictionary

        Raises:
            requests.HTTPError: For HTTP errors
        """
        try:
            response.raise_for_status()

            # Handle empty responses
            if not response.content:
                return {'status': 'success', 'data': None}

            # Try to parse JSON
            try:
                return response.json()
            except json.JSONDecodeError:
                return {'status': 'success', 'data': response.text}

        except requests.HTTPError as e:
            logger.error(f"HTTP Error: {e}")
            logger.error(f"Response: {response.text}")
            raise

    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Send GET request.

        Args:
            endpoint: API endpoint
            params: Query parameters

        Returns:
            Response data
        """
        url = self._build_url(endpoint)
        logger.info(f"GET {url}")

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"GET request failed: {e}")
            raise

    def post(self, endpoint: str, data: Optional[Dict] = None,
             json_data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Send POST request.

        Args:
            endpoint: API endpoint
            data: Form data
            json_data: JSON data

        Returns:
            Response data
        """
        url = self._build_url(endpoint)
        logger.info(f"POST {url}")

        try:
            response = self.session.post(
                url,
                data=data,
                json=json_data,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"POST request failed: {e}")
            raise

    def put(self, endpoint: str, data: Optional[Dict] = None,
            json_data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Send PUT request.

        Args:
            endpoint: API endpoint
            data: Form data
            json_data: JSON data

        Returns:
            Response data
        """
        url = self._build_url(endpoint)
        logger.info(f"PUT {url}")

        try:
            response = self.session.put(
                url,
                data=data,
                json=json_data,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"PUT request failed: {e}")
            raise

    def patch(self, endpoint: str, data: Optional[Dict] = None,
              json_data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Send PATCH request.

        Args:
            endpoint: API endpoint
            data: Form data
            json_data: JSON data

        Returns:
            Response data
        """
        url = self._build_url(endpoint)
        logger.info(f"PATCH {url}")

        try:
            response = self.session.patch(
                url,
                data=data,
                json=json_data,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"PATCH request failed: {e}")
            raise

    def delete(self, endpoint: str) -> Dict[str, Any]:
        """
        Send DELETE request.

        Args:
            endpoint: API endpoint

        Returns:
            Response data
        """
        url = self._build_url(endpoint)
        logger.info(f"DELETE {url}")

        try:
            response = self.session.delete(url, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"DELETE request failed: {e}")
            raise

    def health_check(self) -> bool:
        """
        Check if API is accessible.

        Returns:
            True if API is healthy, False otherwise
        """
        try:
            response = self.session.get(self.base_url, timeout=self.timeout)
            return response.status_code < 500
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False

    def set_header(self, key: str, value: str) -> None:
        """
        Set a custom header.

        Args:
            key: Header name
            value: Header value
        """
        self.session.headers[key] = value

    def close(self) -> None:
        """Close the session."""
        self.session.close()


def main():
    """Main function to demonstrate API client usage."""
    parser = argparse.ArgumentParser(
        description='REST API client for testing and integration'
    )
    parser.add_argument(
        'base_url',
        help='Base URL of the API'
    )
    parser.add_argument(
        '-m', '--method',
        choices=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
        default='GET',
        help='HTTP method (default: GET)'
    )
    parser.add_argument(
        '-e', '--endpoint',
        default='/',
        help='API endpoint path (default: /)'
    )
    parser.add_argument(
        '-d', '--data',
        help='JSON data for POST/PUT/PATCH requests'
    )
    parser.add_argument(
        '-H', '--header',
        action='append',
        help='Custom header in format "Key: Value" (can be used multiple times)'
    )
    parser.add_argument(
        '--api-key',
        help='API key for authentication'
    )
    parser.add_argument(
        '-t', '--timeout',
        type=int,
        default=30,
        help='Request timeout in seconds (default: 30)'
    )
    parser.add_argument(
        '--health-check',
        action='store_true',
        help='Perform health check only'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    try:
        # Initialize client
        client = APIClient(
            base_url=args.base_url,
            api_key=args.api_key,
            timeout=args.timeout
        )

        # Set custom headers
        if args.header:
            for header in args.header:
                if ':' in header:
                    key, value = header.split(':', 1)
                    client.set_header(key.strip(), value.strip())

        # Health check
        if args.health_check:
            if client.health_check():
                logger.info("✓ API is healthy")
                sys.exit(0)
            else:
                logger.error("✗ API is not responding")
                sys.exit(1)

        # Parse JSON data if provided
        json_data = None
        if args.data:
            try:
                json_data = json.loads(args.data)
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON data: {e}")
                sys.exit(1)

        # Make API request
        response = None
        if args.method == 'GET':
            response = client.get(args.endpoint)
        elif args.method == 'POST':
            response = client.post(args.endpoint, json_data=json_data)
        elif args.method == 'PUT':
            response = client.put(args.endpoint, json_data=json_data)
        elif args.method == 'PATCH':
            response = client.patch(args.endpoint, json_data=json_data)
        elif args.method == 'DELETE':
            response = client.delete(args.endpoint)

        # Print response
        print("\n" + "=" * 70)
        print("API RESPONSE")
        print("=" * 70)
        print(json.dumps(response, indent=2))
        print("=" * 70 + "\n")

        client.close()

    except requests.RequestException as e:
        logger.error(f"API request failed: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
