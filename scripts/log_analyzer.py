#!/usr/bin/env python3
"""
Log Analyzer - Parse and analyze log files to extract errors, warnings, and statistics.

This script analyzes log files to identify patterns, extract errors and warnings,
and generate useful statistics about log data.
"""

import argparse
import logging
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class LogAnalyzer:
    """Analyze log files and extract meaningful information."""

    def __init__(self):
        """Initialize the log analyzer."""
        self.total_lines = 0
        self.errors = []
        self.warnings = []
        self.info_messages = []
        self.log_levels = Counter()
        self.timestamps = []
        self.patterns = defaultdict(int)

        # Common log patterns
        self.error_pattern = re.compile(r'\b(ERROR|FATAL|CRITICAL)\b', re.IGNORECASE)
        self.warning_pattern = re.compile(r'\bWARN(ING)?\b', re.IGNORECASE)
        self.info_pattern = re.compile(r'\bINFO\b', re.IGNORECASE)
        self.timestamp_pattern = re.compile(
            r'\d{4}-\d{2}-\d{2}[\sT]\d{2}:\d{2}:\d{2}|\d{2}/\d{2}/\d{4}\s\d{2}:\d{2}:\d{2}'
        )

    def parse_log_file(self, filepath: str) -> None:
        """
        Parse a log file and extract information.

        Args:
            filepath: Path to the log file
        """
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    self.total_lines += 1
                    self._analyze_line(line.strip(), line_num)

            logger.info(f"Successfully analyzed {self.total_lines} lines from {filepath}")

        except FileNotFoundError:
            logger.error(f"File not found: {filepath}")
            raise
        except Exception as e:
            logger.error(f"Error reading file {filepath}: {e}")
            raise

    def _analyze_line(self, line: str, line_num: int) -> None:
        """
        Analyze a single log line.

        Args:
            line: The log line to analyze
            line_num: Line number in the file
        """
        if not line:
            return

        # Extract timestamp
        timestamp_match = self.timestamp_pattern.search(line)
        if timestamp_match:
            self.timestamps.append(timestamp_match.group())

        # Categorize by log level
        if self.error_pattern.search(line):
            self.errors.append((line_num, line))
            self.log_levels['ERROR'] += 1
        elif self.warning_pattern.search(line):
            self.warnings.append((line_num, line))
            self.log_levels['WARNING'] += 1
        elif self.info_pattern.search(line):
            self.info_messages.append((line_num, line))
            self.log_levels['INFO'] += 1
        else:
            self.log_levels['OTHER'] += 1

        # Detect common patterns
        self._detect_patterns(line)

    def _detect_patterns(self, line: str) -> None:
        """
        Detect common error patterns in log lines.

        Args:
            line: The log line to analyze
        """
        patterns = {
            'Connection refused': r'connection refused',
            'Timeout': r'timeout|timed out',
            'Out of memory': r'out of memory|OOM',
            'Permission denied': r'permission denied',
            'File not found': r'file not found|no such file',
            'Database error': r'database error|db error|sql error',
            'HTTP 4xx': r'HTTP/\d\.\d"\s4\d{2}',
            'HTTP 5xx': r'HTTP/\d\.\d"\s5\d{2}',
            'Exception': r'Exception|Traceback',
            'Null pointer': r'null pointer|NullPointerException',
        }

        for pattern_name, pattern_regex in patterns.items():
            if re.search(pattern_regex, line, re.IGNORECASE):
                self.patterns[pattern_name] += 1

    def get_statistics(self) -> Dict:
        """
        Get statistics about the analyzed logs.

        Returns:
            Dictionary containing log statistics
        """
        return {
            'total_lines': self.total_lines,
            'errors': len(self.errors),
            'warnings': len(self.warnings),
            'info': len(self.info_messages),
            'log_levels': dict(self.log_levels),
            'error_patterns': dict(self.patterns),
            'time_range': self._get_time_range()
        }

    def _get_time_range(self) -> Tuple[str, str]:
        """Get the time range of the logs."""
        if not self.timestamps:
            return ('N/A', 'N/A')
        return (self.timestamps[0], self.timestamps[-1])

    def print_report(self, top_n: int = 10, show_details: bool = False) -> None:
        """
        Print a detailed analysis report.

        Args:
            top_n: Number of top items to show in each category
            show_details: Whether to show detailed error/warning messages
        """
        stats = self.get_statistics()

        print("\n" + "=" * 70)
        print("LOG ANALYSIS REPORT")
        print("=" * 70)

        # Overview
        print(f"\nTotal Lines Processed: {stats['total_lines']}")
        print(f"Time Range: {stats['time_range'][0]} to {stats['time_range'][1]}")

        # Log Levels Distribution
        print("\n" + "-" * 70)
        print("LOG LEVELS DISTRIBUTION")
        print("-" * 70)
        for level, count in sorted(stats['log_levels'].items(), key=lambda x: x[1], reverse=True):
            percentage = (count / stats['total_lines']) * 100
            print(f"{level:15} {count:8,} ({percentage:5.1f}%)")

        # Error Patterns
        if stats['error_patterns']:
            print("\n" + "-" * 70)
            print("TOP ERROR PATTERNS")
            print("-" * 70)
            sorted_patterns = sorted(stats['error_patterns'].items(), key=lambda x: x[1], reverse=True)
            for pattern, count in sorted_patterns[:top_n]:
                print(f"{pattern:25} {count:8,}")

        # Detailed Errors
        if show_details and self.errors:
            print("\n" + "-" * 70)
            print(f"ERRORS (showing first {top_n})")
            print("-" * 70)
            for line_num, error in self.errors[:top_n]:
                print(f"Line {line_num:6}: {error[:100]}{'...' if len(error) > 100 else ''}")

        # Detailed Warnings
        if show_details and self.warnings:
            print("\n" + "-" * 70)
            print(f"WARNINGS (showing first {top_n})")
            print("-" * 70)
            for line_num, warning in self.warnings[:top_n]:
                print(f"Line {line_num:6}: {warning[:100]}{'...' if len(warning) > 100 else ''}")

        print("\n" + "=" * 70)

    def export_to_file(self, output_file: str) -> None:
        """
        Export analysis results to a file.

        Args:
            output_file: Path to the output file
        """
        try:
            with open(output_file, 'w') as f:
                f.write("LOG ANALYSIS REPORT\n")
                f.write("=" * 70 + "\n\n")

                stats = self.get_statistics()
                f.write(f"Total Lines: {stats['total_lines']}\n")
                f.write(f"Errors: {stats['errors']}\n")
                f.write(f"Warnings: {stats['warnings']}\n\n")

                f.write("ERRORS:\n")
                f.write("-" * 70 + "\n")
                for line_num, error in self.errors:
                    f.write(f"Line {line_num}: {error}\n")

                f.write("\nWARNINGS:\n")
                f.write("-" * 70 + "\n")
                for line_num, warning in self.warnings:
                    f.write(f"Line {line_num}: {warning}\n")

            logger.info(f"Analysis report exported to {output_file}")

        except Exception as e:
            logger.error(f"Error exporting to file: {e}")
            raise


def main():
    """Main function to parse arguments and run log analysis."""
    parser = argparse.ArgumentParser(
        description='Analyze log files and extract errors, warnings, and statistics'
    )
    parser.add_argument(
        'logfile',
        help='Path to the log file to analyze'
    )
    parser.add_argument(
        '-o', '--output',
        help='Export analysis to output file'
    )
    parser.add_argument(
        '-d', '--details',
        action='store_true',
        help='Show detailed error and warning messages'
    )
    parser.add_argument(
        '-n', '--top',
        type=int,
        default=10,
        help='Number of top items to show (default: 10)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    # Verify log file exists
    if not Path(args.logfile).exists():
        logger.error(f"Log file not found: {args.logfile}")
        sys.exit(1)

    try:
        # Analyze the log file
        analyzer = LogAnalyzer()
        analyzer.parse_log_file(args.logfile)

        # Print report
        analyzer.print_report(top_n=args.top, show_details=args.details)

        # Export if requested
        if args.output:
            analyzer.export_to_file(args.output)

        # Exit with error code if critical errors found
        stats = analyzer.get_statistics()
        if stats['errors'] > 0:
            logger.warning(f"Found {stats['errors']} errors in log file")
            sys.exit(1)

    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
