#!/usr/bin/env python3
"""
File Organizer - Organize files by type, date, or custom rules.

This script helps organize files in directories by moving them into
categorized subdirectories based on file type, modification date, or size.
"""

import argparse
import logging
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class FileOrganizer:
    """Organize files into categorized directories."""

    # File type categories
    FILE_TYPES = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.ico', '.webp'],
        'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.md'],
        'Spreadsheets': ['.xls', '.xlsx', '.csv', '.ods'],
        'Presentations': ['.ppt', '.pptx', '.odp'],
        'Archives': ['.zip', '.tar', '.gz', '.rar', '.7z', '.bz2', '.xz'],
        'Code': ['.py', '.java', '.cpp', '.c', '.js', '.html', '.css', '.go', '.rs', '.rb'],
        'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
        'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'],
        'Executables': ['.exe', '.msi', '.app', '.deb', '.rpm', '.sh', '.bat'],
        'Config': ['.yaml', '.yml', '.json', '.xml', '.ini', '.conf', '.toml'],
    }

    def __init__(self, source_dir: str, dry_run: bool = False):
        """
        Initialize the file organizer.

        Args:
            source_dir: Directory containing files to organize
            dry_run: If True, only simulate organization
        """
        self.source_dir = Path(source_dir)
        self.dry_run = dry_run
        self.stats = {
            'total_files': 0,
            'organized': 0,
            'skipped': 0,
            'errors': 0
        }

        if not self.source_dir.exists():
            raise FileNotFoundError(f"Source directory not found: {source_dir}")

    def organize_by_type(self) -> None:
        """Organize files by their type/extension."""
        logger.info(f"Organizing files by type in: {self.source_dir}")

        for file_path in self.source_dir.iterdir():
            if file_path.is_file():
                self.stats['total_files'] += 1
                category = self._get_file_category(file_path)

                if category:
                    dest_dir = self.source_dir / category
                    self._move_file(file_path, dest_dir)
                else:
                    # Uncategorized files go to "Others"
                    dest_dir = self.source_dir / 'Others'
                    self._move_file(file_path, dest_dir)

    def organize_by_date(self) -> None:
        """Organize files by their modification date."""
        logger.info(f"Organizing files by date in: {self.source_dir}")

        for file_path in self.source_dir.iterdir():
            if file_path.is_file():
                self.stats['total_files'] += 1

                # Get file modification date
                mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                year_month = mod_time.strftime('%Y/%m')

                dest_dir = self.source_dir / year_month
                self._move_file(file_path, dest_dir)

    def organize_by_size(self, size_thresholds: List[int] = None) -> None:
        """
        Organize files by their size.

        Args:
            size_thresholds: List of size thresholds in bytes
        """
        if size_thresholds is None:
            # Default thresholds: 1MB, 10MB, 100MB
            size_thresholds = [1024*1024, 10*1024*1024, 100*1024*1024]

        logger.info(f"Organizing files by size in: {self.source_dir}")

        for file_path in self.source_dir.iterdir():
            if file_path.is_file():
                self.stats['total_files'] += 1
                file_size = file_path.stat().st_size

                # Determine size category
                if file_size < size_thresholds[0]:
                    category = 'Small (< 1MB)'
                elif file_size < size_thresholds[1]:
                    category = 'Medium (1-10MB)'
                elif file_size < size_thresholds[2]:
                    category = 'Large (10-100MB)'
                else:
                    category = 'Very Large (> 100MB)'

                dest_dir = self.source_dir / category
                self._move_file(file_path, dest_dir)

    def _get_file_category(self, file_path: Path) -> str:
        """
        Get the category for a file based on its extension.

        Args:
            file_path: Path to the file

        Returns:
            Category name or None if uncategorized
        """
        extension = file_path.suffix.lower()

        for category, extensions in self.FILE_TYPES.items():
            if extension in extensions:
                return category

        return None

    def _move_file(self, file_path: Path, dest_dir: Path) -> None:
        """
        Move a file to the destination directory.

        Args:
            file_path: Source file path
            dest_dir: Destination directory
        """
        try:
            # Create destination directory if it doesn't exist
            if not self.dry_run:
                dest_dir.mkdir(parents=True, exist_ok=True)

            dest_path = dest_dir / file_path.name

            # Handle file name conflicts
            if dest_path.exists():
                counter = 1
                stem = file_path.stem
                suffix = file_path.suffix
                while dest_path.exists():
                    dest_path = dest_dir / f"{stem}_{counter}{suffix}"
                    counter += 1

            # Move the file
            if self.dry_run:
                logger.info(f"DRY RUN: Would move {file_path.name} to {dest_dir.name}/")
            else:
                shutil.move(str(file_path), str(dest_path))
                logger.info(f"Moved: {file_path.name} → {dest_dir.name}/")

            self.stats['organized'] += 1

        except Exception as e:
            logger.error(f"Error moving {file_path.name}: {e}")
            self.stats['errors'] += 1

    def clean_empty_dirs(self) -> None:
        """Remove empty directories."""
        for dir_path in self.source_dir.rglob('*'):
            if dir_path.is_dir() and not any(dir_path.iterdir()):
                if self.dry_run:
                    logger.info(f"DRY RUN: Would remove empty directory: {dir_path.name}")
                else:
                    dir_path.rmdir()
                    logger.info(f"Removed empty directory: {dir_path.name}")

    def print_summary(self) -> None:
        """Print organization summary."""
        print("\n" + "=" * 70)
        print("FILE ORGANIZATION SUMMARY")
        print("=" * 70)
        print(f"Source Directory: {self.source_dir}")
        print(f"Mode: {'DRY RUN' if self.dry_run else 'LIVE'}")
        print(f"Total Files: {self.stats['total_files']}")
        print(f"Organized: {self.stats['organized']}")
        print(f"Skipped: {self.stats['skipped']}")
        print(f"Errors: {self.stats['errors']}")
        print("=" * 70 + "\n")


def main():
    """Main function to parse arguments and organize files."""
    parser = argparse.ArgumentParser(
        description='Organize files by type, date, or size'
    )
    parser.add_argument(
        'directory',
        help='Directory containing files to organize'
    )
    parser.add_argument(
        '-m', '--method',
        choices=['type', 'date', 'size'],
        default='type',
        help='Organization method (default: type)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simulate organization without moving files'
    )
    parser.add_argument(
        '--clean-empty',
        action='store_true',
        help='Remove empty directories after organization'
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
        organizer = FileOrganizer(args.directory, dry_run=args.dry_run)

        # Organize files based on method
        if args.method == 'type':
            organizer.organize_by_type()
        elif args.method == 'date':
            organizer.organize_by_date()
        elif args.method == 'size':
            organizer.organize_by_size()

        # Clean empty directories if requested
        if args.clean_empty:
            organizer.clean_empty_dirs()

        # Print summary
        organizer.print_summary()

        # Exit with error if there were errors
        if organizer.stats['errors'] > 0:
            sys.exit(1)

    except FileNotFoundError as e:
        logger.error(str(e))
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("\nOrganization interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Organization failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
