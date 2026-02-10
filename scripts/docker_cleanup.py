#!/usr/bin/env python3
"""
Docker Cleanup - Clean up unused Docker resources.

This script helps clean up Docker environments by removing unused containers,
images, volumes, and networks. Useful for freeing up disk space.
"""

import argparse
import logging
import subprocess
import sys
from datetime import datetime
from typing import Dict, List


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class DockerCleanup:
    """Clean up Docker resources and free up disk space."""

    def __init__(self, dry_run: bool = False):
        """
        Initialize the Docker cleanup tool.

        Args:
            dry_run: If True, only simulate cleanup
        """
        self.dry_run = dry_run
        self.stats = {
            'containers_removed': 0,
            'images_removed': 0,
            'volumes_removed': 0,
            'networks_removed': 0,
            'space_reclaimed': '0B'
        }

    def check_docker(self) -> bool:
        """
        Check if Docker is installed and running.

        Returns:
            True if Docker is available, False otherwise
        """
        try:
            result = subprocess.run(
                ['docker', 'version'],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            logger.error("Docker is not installed or not running")
            return False

    def get_disk_usage(self) -> Dict:
        """
        Get Docker disk usage information.

        Returns:
            Dictionary containing disk usage stats
        """
        try:
            result = subprocess.run(
                ['docker', 'system', 'df'],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                logger.info("Docker disk usage:")
                for line in result.stdout.split('\n'):
                    if line.strip():
                        logger.info(line)

            return {'output': result.stdout}

        except Exception as e:
            logger.error(f"Error getting disk usage: {e}")
            return {}

    def remove_stopped_containers(self, older_than: str = None) -> int:
        """
        Remove stopped containers.

        Args:
            older_than: Remove containers older than this duration (e.g., '24h', '7d')

        Returns:
            Number of containers removed
        """
        logger.info("Removing stopped containers...")

        try:
            # List stopped containers
            cmd = ['docker', 'ps', '-a', '-q', '-f', 'status=exited']
            if older_than:
                # Docker doesn't have built-in age filter, so we get all stopped containers
                pass

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode != 0:
                logger.error("Failed to list stopped containers")
                return 0

            container_ids = result.stdout.strip().split('\n')
            container_ids = [cid for cid in container_ids if cid]

            if not container_ids:
                logger.info("No stopped containers to remove")
                return 0

            logger.info(f"Found {len(container_ids)} stopped container(s)")

            if self.dry_run:
                logger.info(f"DRY RUN: Would remove {len(container_ids)} container(s)")
                return len(container_ids)

            # Remove containers
            result = subprocess.run(
                ['docker', 'rm'] + container_ids,
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                count = len(container_ids)
                logger.info(f"Removed {count} stopped container(s)")
                self.stats['containers_removed'] = count
                return count
            else:
                logger.error(f"Failed to remove containers: {result.stderr}")
                return 0

        except Exception as e:
            logger.error(f"Error removing stopped containers: {e}")
            return 0

    def remove_dangling_images(self) -> int:
        """
        Remove dangling (untagged) images.

        Returns:
            Number of images removed
        """
        logger.info("Removing dangling images...")

        try:
            # List dangling images
            result = subprocess.run(
                ['docker', 'images', '-q', '-f', 'dangling=true'],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                logger.error("Failed to list dangling images")
                return 0

            image_ids = result.stdout.strip().split('\n')
            image_ids = [iid for iid in image_ids if iid]

            if not image_ids:
                logger.info("No dangling images to remove")
                return 0

            logger.info(f"Found {len(image_ids)} dangling image(s)")

            if self.dry_run:
                logger.info(f"DRY RUN: Would remove {len(image_ids)} image(s)")
                return len(image_ids)

            # Remove images
            result = subprocess.run(
                ['docker', 'rmi'] + image_ids,
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode == 0:
                count = len(image_ids)
                logger.info(f"Removed {count} dangling image(s)")
                self.stats['images_removed'] = count
                return count
            else:
                logger.warning(f"Some images could not be removed: {result.stderr}")
                return 0

        except Exception as e:
            logger.error(f"Error removing dangling images: {e}")
            return 0

    def remove_unused_images(self, all_images: bool = False) -> int:
        """
        Remove unused images.

        Args:
            all_images: If True, remove all unused images (not just dangling)

        Returns:
            Number of images removed
        """
        if not all_images:
            return self.remove_dangling_images()

        logger.info("Removing all unused images...")

        try:
            if self.dry_run:
                logger.info("DRY RUN: Would remove all unused images")
                return 0

            result = subprocess.run(
                ['docker', 'image', 'prune', '-a', '-f'],
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode == 0:
                logger.info("Removed unused images")
                logger.info(result.stdout)
                return 1
            else:
                logger.error(f"Failed to remove unused images: {result.stderr}")
                return 0

        except Exception as e:
            logger.error(f"Error removing unused images: {e}")
            return 0

    def remove_unused_volumes(self) -> int:
        """
        Remove unused volumes.

        Returns:
            Number of volumes removed
        """
        logger.info("Removing unused volumes...")

        try:
            if self.dry_run:
                # List unused volumes
                result = subprocess.run(
                    ['docker', 'volume', 'ls', '-q', '-f', 'dangling=true'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                volume_ids = result.stdout.strip().split('\n')
                volume_ids = [vid for vid in volume_ids if vid]
                logger.info(f"DRY RUN: Would remove {len(volume_ids)} volume(s)")
                return len(volume_ids)

            result = subprocess.run(
                ['docker', 'volume', 'prune', '-f'],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                logger.info("Removed unused volumes")
                logger.info(result.stdout)
                return 1
            else:
                logger.error(f"Failed to remove unused volumes: {result.stderr}")
                return 0

        except Exception as e:
            logger.error(f"Error removing unused volumes: {e}")
            return 0

    def remove_unused_networks(self) -> int:
        """
        Remove unused networks.

        Returns:
            Number of networks removed
        """
        logger.info("Removing unused networks...")

        try:
            if self.dry_run:
                logger.info("DRY RUN: Would remove unused networks")
                return 0

            result = subprocess.run(
                ['docker', 'network', 'prune', '-f'],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                logger.info("Removed unused networks")
                logger.info(result.stdout)
                return 1
            else:
                logger.error(f"Failed to remove unused networks: {result.stderr}")
                return 0

        except Exception as e:
            logger.error(f"Error removing unused networks: {e}")
            return 0

    def system_prune(self, all_resources: bool = False, volumes: bool = False) -> None:
        """
        Run Docker system prune to clean up all unused resources.

        Args:
            all_resources: Remove all unused resources, not just dangling ones
            volumes: Also remove unused volumes
        """
        logger.info("Running Docker system prune...")

        try:
            cmd = ['docker', 'system', 'prune', '-f']

            if all_resources:
                cmd.append('-a')

            if volumes:
                cmd.append('--volumes')

            if self.dry_run:
                logger.info(f"DRY RUN: Would run: {' '.join(cmd)}")
                return

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                logger.info("System prune completed")
                logger.info(result.stdout)
            else:
                logger.error(f"System prune failed: {result.stderr}")

        except Exception as e:
            logger.error(f"Error during system prune: {e}")

    def print_summary(self) -> None:
        """Print cleanup summary."""
        print("\n" + "=" * 70)
        print("DOCKER CLEANUP SUMMARY")
        print("=" * 70)
        print(f"Mode: {'DRY RUN' if self.dry_run else 'LIVE'}")
        print(f"Containers Removed: {self.stats['containers_removed']}")
        print(f"Images Removed: {self.stats['images_removed']}")
        print(f"Volumes Removed: {self.stats['volumes_removed']}")
        print(f"Networks Removed: {self.stats['networks_removed']}")
        print("=" * 70 + "\n")


def main():
    """Main function to parse arguments and perform Docker cleanup."""
    parser = argparse.ArgumentParser(
        description='Clean up unused Docker resources'
    )
    parser.add_argument(
        '--containers',
        action='store_true',
        help='Remove stopped containers'
    )
    parser.add_argument(
        '--images',
        action='store_true',
        help='Remove dangling images'
    )
    parser.add_argument(
        '--all-images',
        action='store_true',
        help='Remove all unused images'
    )
    parser.add_argument(
        '--volumes',
        action='store_true',
        help='Remove unused volumes'
    )
    parser.add_argument(
        '--networks',
        action='store_true',
        help='Remove unused networks'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Clean up all unused resources (system prune)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simulate cleanup without removing resources'
    )
    parser.add_argument(
        '--disk-usage',
        action='store_true',
        help='Show Docker disk usage'
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
        cleanup = DockerCleanup(dry_run=args.dry_run)

        # Check if Docker is available
        if not cleanup.check_docker():
            sys.exit(1)

        # Show disk usage
        if args.disk_usage:
            cleanup.get_disk_usage()
            sys.exit(0)

        # Perform cleanup based on arguments
        if args.all:
            cleanup.system_prune(all_resources=True, volumes=args.volumes)
        else:
            if args.containers:
                cleanup.remove_stopped_containers()

            if args.images:
                cleanup.remove_dangling_images()

            if args.all_images:
                cleanup.remove_unused_images(all_images=True)

            if args.volumes:
                cleanup.remove_unused_volumes()

            if args.networks:
                cleanup.remove_unused_networks()

            # If no specific cleanup option was specified, show help
            if not any([args.containers, args.images, args.all_images,
                       args.volumes, args.networks]):
                parser.print_help()
                print("\nNo cleanup options specified. Use --all for comprehensive cleanup.")
                sys.exit(1)

        # Print summary
        cleanup.print_summary()

        # Show disk usage after cleanup
        logger.info("\nDisk usage after cleanup:")
        cleanup.get_disk_usage()

    except KeyboardInterrupt:
        logger.info("\nCleanup interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Cleanup failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
