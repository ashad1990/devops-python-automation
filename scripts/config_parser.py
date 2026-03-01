#!/usr/bin/env python3
"""
Configuration Parser - Parse and validate YAML configuration files.

This script reads YAML configuration files, validates their structure,
and provides utilities for accessing configuration values.
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml
except ImportError:
    print("Error: 'pyyaml' module not found. Install it with: pip install pyyaml")
    sys.exit(1)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class ConfigParser:
    """Parse and validate YAML configuration files."""

    def __init__(self, config_file: str):
        """
        Initialize the configuration parser.

        Args:
            config_file: Path to the YAML configuration file
        """
        self.config_file = config_file
        self.config = {}
        self.errors = []
        self.warnings = []

    def load(self) -> Dict[str, Any]:
        """
        Load and parse the YAML configuration file.

        Returns:
            Dictionary containing the configuration

        Raises:
            FileNotFoundError: If configuration file doesn't exist
            yaml.YAMLError: If YAML parsing fails
        """
        try:
            config_path = Path(self.config_file)

            if not config_path.exists():
                raise FileNotFoundError(f"Configuration file not found: {self.config_file}")

            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f)

            if self.config is None:
                self.config = {}
                logger.warning("Configuration file is empty")

            logger.info(f"Successfully loaded configuration from {self.config_file}")
            return self.config

        except yaml.YAMLError as e:
            logger.error(f"YAML parsing error: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            raise

    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get a configuration value using dot notation.

        Args:
            key_path: Dot-separated path to the configuration key (e.g., 'database.host')
            default: Default value if key doesn't exist

        Returns:
            Configuration value or default
        """
        keys = key_path.split('.')
        value = self.config

        try:
            for key in keys:
                if isinstance(value, dict):
                    value = value[key]
                else:
                    return default
            return value
        except (KeyError, TypeError):
            return default

    def validate_required_keys(self, required_keys: List[str]) -> bool:
        """
        Validate that required configuration keys exist.

        Args:
            required_keys: List of required key paths (dot notation supported)

        Returns:
            True if all required keys exist, False otherwise
        """
        missing_keys = []

        for key in required_keys:
            if self.get(key) is None:
                missing_keys.append(key)
                self.errors.append(f"Missing required key: {key}")

        if missing_keys:
            logger.error(f"Missing required configuration keys: {', '.join(missing_keys)}")
            return False

        logger.info("All required configuration keys are present")
        return True

    def validate_types(self, type_map: Dict[str, type]) -> bool:
        """
        Validate that configuration values have expected types.

        Args:
            type_map: Dictionary mapping key paths to expected types

        Returns:
            True if all types are correct, False otherwise
        """
        type_errors = []

        for key, expected_type in type_map.items():
            value = self.get(key)
            if value is not None and not isinstance(value, expected_type):
                error_msg = f"Key '{key}' has type {type(value).__name__}, expected {expected_type.__name__}"
                type_errors.append(error_msg)
                self.errors.append(error_msg)

        if type_errors:
            logger.error(f"Type validation errors: {len(type_errors)}")
            return False

        logger.info("All type validations passed")
        return True

    def merge(self, other_config: Dict[str, Any]) -> None:
        """
        Merge another configuration dictionary into the current one.

        Args:
            other_config: Dictionary to merge
        """
        self._deep_merge(self.config, other_config)
        logger.info("Configuration merged successfully")

    def _deep_merge(self, base: Dict, update: Dict) -> Dict:
        """
        Recursively merge two dictionaries.

        Args:
            base: Base dictionary
            update: Dictionary to merge into base

        Returns:
            Merged dictionary
        """
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
        return base

    def to_json(self, indent: int = 2) -> str:
        """
        Convert configuration to JSON string.

        Args:
            indent: JSON indentation level

        Returns:
            JSON string representation of configuration
        """
        return json.dumps(self.config, indent=indent)

    def save(self, output_file: str, format: str = 'yaml') -> None:
        """
        Save configuration to a file.

        Args:
            output_file: Output file path
            format: Output format ('yaml' or 'json')
        """
        try:
            with open(output_file, 'w') as f:
                if format == 'json':
                    json.dump(self.config, f, indent=2)
                else:
                    yaml.dump(self.config, f, default_flow_style=False)

            logger.info(f"Configuration saved to {output_file}")

        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            raise

    def print_config(self, show_sensitive: bool = False) -> None:
        """
        Print the configuration in a readable format.

        Args:
            show_sensitive: Whether to show sensitive values
        """
        def _mask_sensitive(key: str, value: Any) -> Any:
            """Mask sensitive configuration values."""
            sensitive_keys = ['password', 'secret', 'token', 'key', 'api_key']
            if not show_sensitive and any(s in key.lower() for s in sensitive_keys):
                return '***MASKED***'
            return value

        def _print_dict(d: Dict, indent: int = 0):
            """Recursively print dictionary."""
            for key, value in d.items():
                if isinstance(value, dict):
                    print(' ' * indent + f"{key}:")
                    _print_dict(value, indent + 2)
                else:
                    masked_value = _mask_sensitive(key, value)
                    print(' ' * indent + f"{key}: {masked_value}")

        print("\n" + "=" * 70)
        print("CONFIGURATION")
        print("=" * 70)
        _print_dict(self.config)
        print("=" * 70 + "\n")


def main():
    """Main function to parse arguments and process configuration."""
    parser = argparse.ArgumentParser(
        description='Parse and validate YAML configuration files'
    )
    parser.add_argument(
        'config_file',
        help='Path to the YAML configuration file'
    )
    parser.add_argument(
        '-g', '--get',
        help='Get a specific configuration value (use dot notation, e.g., database.host)'
    )
    parser.add_argument(
        '-r', '--required',
        nargs='+',
        help='List of required configuration keys to validate'
    )
    parser.add_argument(
        '-o', '--output',
        help='Save configuration to output file'
    )
    parser.add_argument(
        '-f', '--format',
        choices=['yaml', 'json'],
        default='yaml',
        help='Output format (default: yaml)'
    )
    parser.add_argument(
        '--show-sensitive',
        action='store_true',
        help='Show sensitive values (passwords, tokens, etc.)'
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
        # Load configuration
        config_parser = ConfigParser(args.config_file)
        config_parser.load()

        # Get specific value
        if args.get:
            value = config_parser.get(args.get)
            if value is None:
                logger.error(f"Configuration key not found: {args.get}")
                sys.exit(1)
            print(f"{args.get}: {value}")
            sys.exit(0)

        # Validate required keys
        if args.required:
            if not config_parser.validate_required_keys(args.required):
                logger.error("Required key validation failed")
                sys.exit(1)

        # Print configuration
        config_parser.print_config(show_sensitive=args.show_sensitive)

        # Save if requested
        if args.output:
            config_parser.save(args.output, format=args.format)

    except FileNotFoundError as e:
        logger.error(str(e))
        sys.exit(1)
    except yaml.YAMLError as e:
        logger.error(f"Invalid YAML: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
