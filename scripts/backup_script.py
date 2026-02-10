#!/usr/bin/env python3
"""
Backup Script - Automated backup with rotation and compression.

This script creates compressed backups of specified directories or files
with automatic rotation to manage disk space.
"""

import argparse
import gzip
import logging
import os
import shutil
import sys
import tarfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import List


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class BackupManager:
    """Manage file and directory backups with rotation."""

    def __init__(self, backup_dir: str, retention_days: int = 7):
        """
        Initialize the backup manager.

        Args:
            backup_dir: Directory where backups will be stored
            retention_days: Number of days to retain backups
        """
        self.backup_dir = Path(backup_dir)
        self.retention_days = retention_days
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def create_backup(self, source_path: str, backup_name: str = None) -> str:
        """
        Create a compressed backup of the source path.

        Args:
            source_path: Path to the file or directory to backup
            backup_name: Custom backup name (optional)

        Returns:
            Path to the created backup file

        Raises:
            FileNotFoundError: If source path doesn't exist
        """
        source = Path(source_path)

        if not source.exists():
            raise FileNotFoundError(f"Source path not found: {source_path}")

        # Generate backup filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        if backup_name is None:
            backup_name = source.name

        backup_filename = f"{backup_name}_{timestamp}.tar.gz"
        backup_path = self.backup_dir / backup_filename

        try:
            logger.info(f"Creating backup: {backup_filename}")

            with tarfile.open(backup_path, 'w:gz') as tar:
                tar.add(source, arcname=source.name)

            backup_size = backup_path.stat().st_size
            logger.info(f"Backup created successfully: {backup_path} ({self._format_size(backup_size)})")

            return str(backup_path)

        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            if backup_path.exists():
                backup_path.unlink()
            raise

    def rotate_backups(self) -> int:
        """
        Remove backups older than retention period.

        Returns:
            Number of backups removed
        """
        cutoff_date = datetime.now() - timedelta(days=self.retention_days)
        removed_count = 0

        try:
            for backup_file in self.backup_dir.glob('*.tar.gz'):
                file_time = datetime.fromtimestamp(backup_file.stat().st_mtime)

                if file_time < cutoff_date:
                    logger.info(f"Removing old backup: {backup_file.name}")
                    backup_file.unlink()
                    removed_count += 1

            if removed_count > 0:
                logger.info(f"Removed {removed_count} old backup(s)")
            else:
                logger.info("No old backups to remove")

            return removed_count

        except Exception as e:
            logger.error(f"Error during backup rotation: {e}")
            raise

    def list_backups(self) -> List[dict]:
        """
        List all available backups.

        Returns:
            List of dictionaries containing backup information
        """
        backups = []

        for backup_file in sorted(self.backup_dir.glob('*.tar.gz'), reverse=True):
            stat = backup_file.stat()
            backups.append({
                'name': backup_file.name,
                'path': str(backup_file),
                'size': stat.st_size,
                'size_human': self._format_size(stat.st_size),
                'modified': datetime.fromtimestamp(stat.st_mtime),
                'age_days': (datetime.now() - datetime.fromtimestamp(stat.st_mtime)).days
            })

        return backups

    def restore_backup(self, backup_file: str, restore_path: str) -> None:
        """
        Restore a backup to the specified location.

        Args:
            backup_file: Path to the backup file
            restore_path: Path where backup should be restored
        """
        backup = Path(backup_file)

        if not backup.exists():
            raise FileNotFoundError(f"Backup file not found: {backup_file}")

        restore_dir = Path(restore_path)
        restore_dir.mkdir(parents=True, exist_ok=True)

        try:
            logger.info(f"Restoring backup: {backup.name} to {restore_path}")

            with tarfile.open(backup, 'r:gz') as tar:
                tar.extractall(restore_dir)

            logger.info("Backup restored successfully")

        except Exception as e:
            logger.error(f"Error restoring backup: {e}")
            raise

    def verify_backup(self, backup_file: str) -> bool:
        """
        Verify the integrity of a backup file.

        Args:
            backup_file: Path to the backup file

        Returns:
            True if backup is valid, False otherwise
        """
        backup = Path(backup_file)

        if not backup.exists():
            logger.error(f"Backup file not found: {backup_file}")
            return False

        try:
            logger.info(f"Verifying backup: {backup.name}")

            with tarfile.open(backup, 'r:gz') as tar:
                members = tar.getmembers()
                logger.info(f"Backup contains {len(members)} file(s)")

            logger.info("Backup verification successful")
            return True

        except Exception as e:
            logger.error(f"Backup verification failed: {e}")
            return False

    @staticmethod
    def _format_size(size_bytes: int) -> str:
        """Format bytes to human-readable size."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"

    def print_summary(self) -> None:
        """Print a summary of all backups."""
        backups = self.list_backups()

        print("\n" + "=" * 80)
        print("BACKUP SUMMARY")
        print("=" * 80)
        print(f"Backup Directory: {self.backup_dir}")
        print(f"Retention Period: {self.retention_days} days")
        print(f"Total Backups: {len(backups)}")

        if backups:
            total_size = sum(b['size'] for b in backups)
            print(f"Total Size: {self._format_size(total_size)}")

            print("\n" + "-" * 80)
            print(f"{'Backup Name':<40} {'Size':<12} {'Age':<10} {'Date'}")
            print("-" * 80)

            for backup in backups:
                age_str = f"{backup['age_days']}d"
                date_str = backup['modified'].strftime('%Y-%m-%d %H:%M')
                print(f"{backup['name']:<40} {backup['size_human']:<12} {age_str:<10} {date_str}")

        print("=" * 80 + "\n")


def main():
    """Main function to parse arguments and perform backup operations."""
    parser = argparse.ArgumentParser(
        description='Automated backup script with rotation and compression'
    )
    parser.add_argument(
        '-s', '--source',
        help='Source file or directory to backup'
    )
    parser.add_argument(
        '-d', '--destination',
        default='./backups',
        help='Backup destination directory (default: ./backups)'
    )
    parser.add_argument(
        '-n', '--name',
        help='Custom backup name'
    )
    parser.add_argument(
        '-r', '--retention',
        type=int,
        default=7,
        help='Backup retention period in days (default: 7)'
    )
    parser.add_argument(
        '--restore',
        help='Restore a backup from the specified file'
    )
    parser.add_argument(
        '--restore-to',
        help='Directory to restore backup to'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all available backups'
    )
    parser.add_argument(
        '--verify',
        help='Verify a backup file'
    )
    parser.add_argument(
        '--rotate',
        action='store_true',
        help='Rotate old backups based on retention policy'
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
        manager = BackupManager(args.destination, args.retention)

        # List backups
        if args.list:
            manager.print_summary()
            sys.exit(0)

        # Verify backup
        if args.verify:
            if manager.verify_backup(args.verify):
                sys.exit(0)
            else:
                sys.exit(1)

        # Restore backup
        if args.restore:
            if not args.restore_to:
                logger.error("--restore-to is required when using --restore")
                sys.exit(1)
            manager.restore_backup(args.restore, args.restore_to)
            sys.exit(0)

        # Rotate backups
        if args.rotate:
            manager.rotate_backups()
            sys.exit(0)

        # Create backup
        if args.source:
            backup_path = manager.create_backup(args.source, args.name)
            manager.rotate_backups()
            logger.info(f"Backup process completed: {backup_path}")
        else:
            parser.print_help()
            sys.exit(1)

    except FileNotFoundError as e:
        logger.error(str(e))
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("\nBackup interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Backup failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
