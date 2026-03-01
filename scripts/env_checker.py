#!/usr/bin/env python3
"""
Environment Checker - Validate required environment variables and configurations.

This script validates that all required environment variables are set and
optionally checks their values against expected patterns or ranges.
"""

import argparse
import logging
import os
import re
import sys
from typing import Dict, List, Optional, Tuple


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class EnvironmentChecker:
    """Validate environment variables and configurations."""

    def __init__(self):
        """Initialize the environment checker."""
        self.errors = []
        self.warnings = []
        self.validations = []

    def check_required_vars(self, required_vars: List[str]) -> bool:
        """
        Check if required environment variables are set.

        Args:
            required_vars: List of required environment variable names

        Returns:
            True if all required variables are set, False otherwise
        """
        all_present = True

        for var in required_vars:
            if var in os.environ:
                value = os.environ[var]
                if value:
                    self.validations.append((var, 'SET', '✓'))
                    logger.info(f"✓ {var} is set")
                else:
                    self.validations.append((var, 'EMPTY', '✗'))
                    self.errors.append(f"{var} is set but empty")
                    logger.error(f"✗ {var} is set but empty")
                    all_present = False
            else:
                self.validations.append((var, 'MISSING', '✗'))
                self.errors.append(f"{var} is not set")
                logger.error(f"✗ {var} is not set")
                all_present = False

        return all_present

    def check_optional_vars(self, optional_vars: List[str]) -> None:
        """
        Check optional environment variables and warn if missing.

        Args:
            optional_vars: List of optional environment variable names
        """
        for var in optional_vars:
            if var in os.environ:
                self.validations.append((var, 'SET', '✓'))
                logger.info(f"✓ {var} is set (optional)")
            else:
                self.validations.append((var, 'NOT SET', '⚠'))
                self.warnings.append(f"{var} is not set (optional)")
                logger.warning(f"⚠ {var} is not set (optional)")

    def validate_pattern(self, var_name: str, pattern: str, description: str = None) -> bool:
        """
        Validate environment variable value against a regex pattern.

        Args:
            var_name: Environment variable name
            pattern: Regex pattern to match
            description: Human-readable description of the expected format

        Returns:
            True if validation passes, False otherwise
        """
        if var_name not in os.environ:
            error_msg = f"{var_name} is not set (required for pattern validation)"
            self.errors.append(error_msg)
            logger.error(f"✗ {error_msg}")
            return False

        value = os.environ[var_name]

        try:
            if re.match(pattern, value):
                logger.info(f"✓ {var_name} matches expected pattern")
                return True
            else:
                desc = description or f"pattern: {pattern}"
                error_msg = f"{var_name} does not match expected {desc}"
                self.errors.append(error_msg)
                logger.error(f"✗ {error_msg}")
                return False
        except re.error as e:
            logger.error(f"Invalid regex pattern for {var_name}: {e}")
            return False

    def validate_numeric_range(self, var_name: str, min_val: Optional[float] = None,
                               max_val: Optional[float] = None) -> bool:
        """
        Validate that an environment variable is numeric and within range.

        Args:
            var_name: Environment variable name
            min_val: Minimum acceptable value (optional)
            max_val: Maximum acceptable value (optional)

        Returns:
            True if validation passes, False otherwise
        """
        if var_name not in os.environ:
            error_msg = f"{var_name} is not set (required for numeric validation)"
            self.errors.append(error_msg)
            logger.error(f"✗ {error_msg}")
            return False

        value = os.environ[var_name]

        try:
            num_value = float(value)

            if min_val is not None and num_value < min_val:
                error_msg = f"{var_name} ({num_value}) is below minimum ({min_val})"
                self.errors.append(error_msg)
                logger.error(f"✗ {error_msg}")
                return False

            if max_val is not None and num_value > max_val:
                error_msg = f"{var_name} ({num_value}) is above maximum ({max_val})"
                self.errors.append(error_msg)
                logger.error(f"✗ {error_msg}")
                return False

            logger.info(f"✓ {var_name} is numeric and within range")
            return True

        except ValueError:
            error_msg = f"{var_name} is not a valid number: {value}"
            self.errors.append(error_msg)
            logger.error(f"✗ {error_msg}")
            return False

    def validate_choices(self, var_name: str, choices: List[str],
                        case_sensitive: bool = False) -> bool:
        """
        Validate that an environment variable is one of the allowed choices.

        Args:
            var_name: Environment variable name
            choices: List of allowed values
            case_sensitive: Whether comparison should be case-sensitive

        Returns:
            True if validation passes, False otherwise
        """
        if var_name not in os.environ:
            error_msg = f"{var_name} is not set (required for choice validation)"
            self.errors.append(error_msg)
            logger.error(f"✗ {error_msg}")
            return False

        value = os.environ[var_name]

        # Prepare for comparison
        if case_sensitive:
            is_valid = value in choices
            choices_str = ', '.join(choices)
        else:
            is_valid = value.lower() in [c.lower() for c in choices]
            choices_str = ', '.join(choices)

        if is_valid:
            logger.info(f"✓ {var_name} is a valid choice")
            return True
        else:
            error_msg = f"{var_name} value '{value}' is not in allowed choices: {choices_str}"
            self.errors.append(error_msg)
            logger.error(f"✗ {error_msg}")
            return False

    def validate_url(self, var_name: str) -> bool:
        """
        Validate that an environment variable is a valid URL.

        Args:
            var_name: Environment variable name

        Returns:
            True if validation passes, False otherwise
        """
        url_pattern = r'^https?://.+'
        return self.validate_pattern(var_name, url_pattern, "valid URL (http:// or https://)")

    def validate_email(self, var_name: str) -> bool:
        """
        Validate that an environment variable is a valid email address.

        Args:
            var_name: Environment variable name

        Returns:
            True if validation passes, False otherwise
        """
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return self.validate_pattern(var_name, email_pattern, "valid email address")

    def list_all_env_vars(self, filter_pattern: Optional[str] = None) -> List[Tuple[str, str]]:
        """
        List all environment variables, optionally filtered by pattern.

        Args:
            filter_pattern: Regex pattern to filter variable names

        Returns:
            List of (name, value) tuples
        """
        env_vars = []

        for name, value in sorted(os.environ.items()):
            if filter_pattern:
                if re.search(filter_pattern, name, re.IGNORECASE):
                    env_vars.append((name, value))
            else:
                env_vars.append((name, value))

        return env_vars

    def print_report(self, show_values: bool = False, mask_sensitive: bool = True) -> None:
        """
        Print validation report.

        Args:
            show_values: Whether to show environment variable values
            mask_sensitive: Whether to mask sensitive values
        """
        print("\n" + "=" * 80)
        print("ENVIRONMENT VALIDATION REPORT")
        print("=" * 80)

        # Validation results
        if self.validations:
            print("\n" + "-" * 80)
            print("VARIABLE CHECKS")
            print("-" * 80)
            print(f"{'Variable':<30} {'Status':<15} {'Result'}")
            print("-" * 80)

            for var_name, status, result in self.validations:
                value = ''
                if show_values and var_name in os.environ:
                    val = os.environ[var_name]
                    # Mask sensitive values
                    if mask_sensitive and any(s in var_name.lower() for s in
                                             ['password', 'secret', 'token', 'key', 'api']):
                        value = f" = {'*' * 8}"
                    else:
                        value = f" = {val[:50]}{'...' if len(val) > 50 else ''}"

                print(f"{var_name:<30} {status:<15} {result}{value}")

        # Errors
        if self.errors:
            print("\n" + "-" * 80)
            print(f"ERRORS ({len(self.errors)})")
            print("-" * 80)
            for error in self.errors:
                print(f"✗ {error}")

        # Warnings
        if self.warnings:
            print("\n" + "-" * 80)
            print(f"WARNINGS ({len(self.warnings)})")
            print("-" * 80)
            for warning in self.warnings:
                print(f"⚠ {warning}")

        # Summary
        print("\n" + "-" * 80)
        print("SUMMARY")
        print("-" * 80)
        print(f"Total Checks: {len(self.validations)}")
        print(f"Errors: {len(self.errors)}")
        print(f"Warnings: {len(self.warnings)}")
        print("=" * 80 + "\n")


def main():
    """Main function to parse arguments and validate environment."""
    parser = argparse.ArgumentParser(
        description='Validate required environment variables'
    )
    parser.add_argument(
        '-r', '--required',
        nargs='+',
        help='Required environment variables (space-separated)'
    )
    parser.add_argument(
        '-o', '--optional',
        nargs='+',
        help='Optional environment variables (space-separated)'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all environment variables'
    )
    parser.add_argument(
        '--filter',
        help='Filter environment variables by pattern (regex)'
    )
    parser.add_argument(
        '--show-values',
        action='store_true',
        help='Show environment variable values in report'
    )
    parser.add_argument(
        '--no-mask',
        action='store_true',
        help='Do not mask sensitive values'
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
        checker = EnvironmentChecker()

        # List environment variables
        if args.list:
            env_vars = checker.list_all_env_vars(args.filter)
            print("\n" + "=" * 80)
            print("ENVIRONMENT VARIABLES")
            if args.filter:
                print(f"Filter: {args.filter}")
            print("=" * 80)

            for name, value in env_vars:
                if args.show_values:
                    # Mask sensitive values unless --no-mask is used
                    if not args.no_mask and any(s in name.lower() for s in
                                               ['password', 'secret', 'token', 'key', 'api']):
                        display_value = '*' * 8
                    else:
                        display_value = value
                    print(f"{name} = {display_value}")
                else:
                    print(f"{name}")

            print("=" * 80)
            print(f"\nTotal: {len(env_vars)} variable(s)")
            sys.exit(0)

        # Check required variables
        all_valid = True
        if args.required:
            all_valid = checker.check_required_vars(args.required)

        # Check optional variables
        if args.optional:
            checker.check_optional_vars(args.optional)

        # Print report if any checks were performed
        if args.required or args.optional:
            checker.print_report(
                show_values=args.show_values,
                mask_sensitive=not args.no_mask
            )

            # Exit with error code if validation failed
            if not all_valid or checker.errors:
                sys.exit(1)
        else:
            # No checks specified, show help
            parser.print_help()
            print("\nExample usage:")
            print("  env_checker.py -r DATABASE_URL API_KEY")
            print("  env_checker.py -r PORT -o DEBUG_MODE")
            print("  env_checker.py --list --filter 'AWS|AZURE'")

    except KeyboardInterrupt:
        logger.info("\nValidation interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Validation failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
