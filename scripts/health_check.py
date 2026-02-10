#!/usr/bin/env python3
"""
Health Check Script - Monitor multiple endpoints and report their status.

This script checks the health of multiple HTTP/HTTPS endpoints by sending
GET requests and reporting their status, response time, and availability.
"""

import argparse
import logging
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Dict, List

try:
    import requests
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


def check_endpoint(url: str, timeout: int = 10) -> Dict:
    """
    Check the health of a single endpoint.

    Args:
        url: The endpoint URL to check
        timeout: Request timeout in seconds

    Returns:
        Dictionary containing status information
    """
    result = {
        'url': url,
        'status': 'DOWN',
        'status_code': None,
        'response_time': None,
        'error': None,
        'timestamp': datetime.now().isoformat()
    }

    try:
        start_time = time.time()
        response = requests.get(url, timeout=timeout, allow_redirects=True)
        response_time = (time.time() - start_time) * 1000  # Convert to ms

        result['status_code'] = response.status_code
        result['response_time'] = round(response_time, 2)

        if response.status_code >= 200 and response.status_code < 400:
            result['status'] = 'UP'
            logger.info(f"✓ {url} - UP ({response.status_code}) - {result['response_time']}ms")
        else:
            result['status'] = 'DEGRADED'
            logger.warning(f"⚠ {url} - DEGRADED ({response.status_code}) - {result['response_time']}ms")

    except requests.exceptions.Timeout:
        result['error'] = 'Timeout'
        logger.error(f"✗ {url} - DOWN (Timeout after {timeout}s)")
    except requests.exceptions.ConnectionError:
        result['error'] = 'Connection Error'
        logger.error(f"✗ {url} - DOWN (Connection Error)")
    except requests.exceptions.RequestException as e:
        result['error'] = str(e)
        logger.error(f"✗ {url} - DOWN ({str(e)})")
    except Exception as e:
        result['error'] = f"Unexpected error: {str(e)}"
        logger.error(f"✗ {url} - DOWN (Unexpected error: {str(e)})")

    return result


def check_multiple_endpoints(urls: List[str], timeout: int = 10, max_workers: int = 5) -> List[Dict]:
    """
    Check multiple endpoints concurrently.

    Args:
        urls: List of URLs to check
        timeout: Request timeout in seconds
        max_workers: Maximum number of concurrent workers

    Returns:
        List of dictionaries containing status information for each endpoint
    """
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(check_endpoint, url, timeout): url for url in urls}

        for future in as_completed(future_to_url):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                logger.error(f"Error processing endpoint: {e}")

    return results


def print_summary(results: List[Dict]):
    """Print a summary of health check results."""
    total = len(results)
    up = sum(1 for r in results if r['status'] == 'UP')
    degraded = sum(1 for r in results if r['status'] == 'DEGRADED')
    down = sum(1 for r in results if r['status'] == 'DOWN')

    print("\n" + "=" * 60)
    print("HEALTH CHECK SUMMARY")
    print("=" * 60)
    print(f"Total Endpoints: {total}")
    print(f"UP: {up} ({(up/total)*100:.1f}%)")
    print(f"DEGRADED: {degraded} ({(degraded/total)*100:.1f}%)")
    print(f"DOWN: {down} ({(down/total)*100:.1f}%)")
    print("=" * 60)

    # Calculate average response time for UP endpoints
    up_results = [r for r in results if r['status'] == 'UP' and r['response_time']]
    if up_results:
        avg_response_time = sum(r['response_time'] for r in up_results) / len(up_results)
        print(f"Average Response Time (UP): {avg_response_time:.2f}ms")
        print("=" * 60)


def main():
    """Main function to parse arguments and run health checks."""
    parser = argparse.ArgumentParser(
        description='Check the health of multiple HTTP/HTTPS endpoints'
    )
    parser.add_argument(
        'urls',
        nargs='*',
        help='URLs to check (space-separated)'
    )
    parser.add_argument(
        '-f', '--file',
        help='File containing URLs (one per line)'
    )
    parser.add_argument(
        '-t', '--timeout',
        type=int,
        default=10,
        help='Request timeout in seconds (default: 10)'
    )
    parser.add_argument(
        '-w', '--workers',
        type=int,
        default=5,
        help='Maximum concurrent workers (default: 5)'
    )
    parser.add_argument(
        '--interval',
        type=int,
        help='Run continuously with specified interval in seconds'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    # Collect URLs from arguments or file
    urls = list(args.urls) if args.urls else []

    if args.file:
        try:
            with open(args.file, 'r') as f:
                file_urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                urls.extend(file_urls)
        except FileNotFoundError:
            logger.error(f"File not found: {args.file}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            sys.exit(1)

    if not urls:
        # Default URLs for demonstration
        urls = [
            'https://www.google.com',
            'https://www.github.com',
            'https://httpbin.org/status/200',
            'https://httpbin.org/status/404',
            'https://httpbin.org/delay/2'
        ]
        logger.info("No URLs provided, using default endpoints for demonstration")

    # Run health checks
    try:
        if args.interval:
            logger.info(f"Running continuous health checks every {args.interval} seconds (Ctrl+C to stop)")
            iteration = 1
            while True:
                print(f"\n{'*' * 60}")
                print(f"Iteration #{iteration} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print('*' * 60)
                results = check_multiple_endpoints(urls, args.timeout, args.workers)
                print_summary(results)
                iteration += 1
                time.sleep(args.interval)
        else:
            results = check_multiple_endpoints(urls, args.timeout, args.workers)
            print_summary(results)

            # Exit with error code if any endpoint is down
            if any(r['status'] == 'DOWN' for r in results):
                sys.exit(1)

    except KeyboardInterrupt:
        logger.info("\nHealth check interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
