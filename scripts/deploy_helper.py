#!/usr/bin/env python3
"""
Deploy Helper - Simple deployment automation helper.

This script helps automate deployment tasks including pre-deployment checks,
deployment steps, and post-deployment verification.
"""

import argparse
import logging
import os
import subprocess
import sys
import time
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


class DeploymentHelper:
    """Helper class for managing deployment operations."""

    def __init__(self, environment: str, dry_run: bool = False):
        """
        Initialize the deployment helper.

        Args:
            environment: Target environment (dev, staging, production)
            dry_run: If True, only simulate deployment
        """
        self.environment = environment
        self.dry_run = dry_run
        self.deployment_log = []
        self.start_time = None
        self.end_time = None

    def log_step(self, step: str, status: str = 'INFO') -> None:
        """
        Log a deployment step.

        Args:
            step: Description of the step
            status: Status of the step (INFO, SUCCESS, WARNING, ERROR)
        """
        timestamp = datetime.now().isoformat()
        self.deployment_log.append({
            'timestamp': timestamp,
            'step': step,
            'status': status
        })

        log_func = {
            'INFO': logger.info,
            'SUCCESS': logger.info,
            'WARNING': logger.warning,
            'ERROR': logger.error
        }.get(status, logger.info)

        log_func(f"[{status}] {step}")

    def run_command(self, command: str, description: str = None) -> Tuple[bool, str]:
        """
        Execute a shell command.

        Args:
            command: Command to execute
            description: Description of the command

        Returns:
            Tuple of (success, output)
        """
        desc = description or command
        self.log_step(f"Executing: {desc}")

        if self.dry_run:
            self.log_step(f"DRY RUN: Would execute: {command}", 'INFO')
            return True, "Dry run - command not executed"

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                self.log_step(f"Command completed successfully: {desc}", 'SUCCESS')
                return True, result.stdout
            else:
                self.log_step(f"Command failed: {desc}", 'ERROR')
                logger.error(f"Error output: {result.stderr}")
                return False, result.stderr

        except subprocess.TimeoutExpired:
            self.log_step(f"Command timeout: {desc}", 'ERROR')
            return False, "Command timed out"
        except Exception as e:
            self.log_step(f"Exception running command: {str(e)}", 'ERROR')
            return False, str(e)

    def pre_deployment_checks(self) -> bool:
        """
        Run pre-deployment checks.

        Returns:
            True if all checks pass, False otherwise
        """
        self.log_step("=" * 60)
        self.log_step("PRE-DEPLOYMENT CHECKS")
        self.log_step("=" * 60)

        checks_passed = True

        # Check 1: Git status
        self.log_step("Checking Git status...")
        success, output = self.run_command("git status --porcelain", "Git status check")
        if success and output.strip():
            self.log_step("Warning: Uncommitted changes detected", 'WARNING')
        elif success:
            self.log_step("Git working directory clean", 'SUCCESS')

        # Check 2: Current branch
        self.log_step("Checking current branch...")
        success, output = self.run_command("git branch --show-current", "Get current branch")
        if success:
            current_branch = output.strip()
            self.log_step(f"Current branch: {current_branch}", 'INFO')

            # Warn if deploying from non-main branches to production
            if self.environment == 'production' and current_branch not in ['main', 'master']:
                self.log_step(f"Warning: Deploying to production from {current_branch}", 'WARNING')

        # Check 3: Dependencies check
        self.log_step("Checking dependencies...")
        if Path('requirements.txt').exists():
            success, _ = self.run_command(
                "python3 -m pip check",
                "Check Python dependencies"
            )
            if success:
                self.log_step("Dependencies check passed", 'SUCCESS')
            else:
                self.log_step("Dependencies check failed", 'ERROR')
                checks_passed = False

        # Check 4: Environment validation
        self.log_step(f"Validating environment: {self.environment}...")
        valid_environments = ['dev', 'development', 'staging', 'stage', 'production', 'prod']
        if self.environment.lower() not in valid_environments:
            self.log_step(f"Invalid environment: {self.environment}", 'ERROR')
            checks_passed = False
        else:
            self.log_step(f"Environment validated: {self.environment}", 'SUCCESS')

        return checks_passed

    def deploy(self) -> bool:
        """
        Execute deployment steps.

        Returns:
            True if deployment succeeds, False otherwise
        """
        self.start_time = datetime.now()
        self.log_step("=" * 60)
        self.log_step(f"STARTING DEPLOYMENT TO {self.environment.upper()}")
        self.log_step("=" * 60)

        try:
            # Step 1: Pull latest changes
            self.log_step("Pulling latest changes...")
            success, _ = self.run_command("git pull origin $(git branch --show-current)", "Git pull")
            if not success and not self.dry_run:
                raise Exception("Failed to pull latest changes")

            # Step 2: Install/update dependencies
            if Path('requirements.txt').exists():
                self.log_step("Installing/updating dependencies...")
                success, _ = self.run_command(
                    "pip install -r requirements.txt --quiet",
                    "Install Python dependencies"
                )
                if not success and not self.dry_run:
                    raise Exception("Failed to install dependencies")

            # Step 3: Run tests (if test directory exists)
            if Path('tests').exists() or Path('test').exists():
                self.log_step("Running tests...")
                success, _ = self.run_command("python3 -m pytest --tb=short", "Run tests")
                if not success and not self.dry_run:
                    self.log_step("Tests failed - continuing anyway", 'WARNING')

            # Step 4: Build/compile (example)
            self.log_step("Build step (if needed)...")
            # Add your build commands here

            # Step 5: Database migrations (example)
            self.log_step("Running database migrations (if needed)...")
            # Add migration commands here

            # Step 6: Restart services
            self.log_step("Restarting services...")
            # Add service restart commands here

            self.log_step("Deployment completed successfully", 'SUCCESS')
            return True

        except Exception as e:
            self.log_step(f"Deployment failed: {str(e)}", 'ERROR')
            return False

    def post_deployment_checks(self) -> bool:
        """
        Run post-deployment verification.

        Returns:
            True if all checks pass, False otherwise
        """
        self.log_step("=" * 60)
        self.log_step("POST-DEPLOYMENT VERIFICATION")
        self.log_step("=" * 60)

        checks_passed = True

        # Check 1: Process/service status
        self.log_step("Checking process status...")
        # Add process check commands here

        # Check 2: Health check endpoints
        self.log_step("Running health checks...")
        # Add health check commands here

        # Check 3: Smoke tests
        self.log_step("Running smoke tests...")
        # Add smoke test commands here

        return checks_passed

    def rollback(self) -> bool:
        """
        Rollback to previous version.

        Returns:
            True if rollback succeeds, False otherwise
        """
        self.log_step("=" * 60)
        self.log_step("INITIATING ROLLBACK")
        self.log_step("=" * 60)

        try:
            # Get previous commit
            success, output = self.run_command("git rev-parse HEAD~1", "Get previous commit")
            if not success:
                raise Exception("Failed to get previous commit")

            previous_commit = output.strip()
            self.log_step(f"Rolling back to: {previous_commit}")

            # Checkout previous commit
            success, _ = self.run_command(f"git checkout {previous_commit}", "Checkout previous version")
            if not success and not self.dry_run:
                raise Exception("Failed to checkout previous version")

            self.log_step("Rollback completed", 'SUCCESS')
            return True

        except Exception as e:
            self.log_step(f"Rollback failed: {str(e)}", 'ERROR')
            return False

    def print_summary(self) -> None:
        """Print deployment summary."""
        self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds() if self.start_time else 0

        print("\n" + "=" * 70)
        print("DEPLOYMENT SUMMARY")
        print("=" * 70)
        print(f"Environment: {self.environment}")
        print(f"Mode: {'DRY RUN' if self.dry_run else 'LIVE'}")
        print(f"Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S') if self.start_time else 'N/A'}")
        print(f"End Time: {self.end_time.strftime('%Y-%m-%d %H:%M:%S') if self.end_time else 'N/A'}")
        print(f"Duration: {duration:.2f} seconds")
        print(f"Total Steps: {len(self.deployment_log)}")

        errors = sum(1 for log in self.deployment_log if log['status'] == 'ERROR')
        warnings = sum(1 for log in self.deployment_log if log['status'] == 'WARNING')

        print(f"Errors: {errors}")
        print(f"Warnings: {warnings}")
        print("=" * 70 + "\n")


def main():
    """Main function to parse arguments and run deployment."""
    parser = argparse.ArgumentParser(
        description='Simple deployment automation helper'
    )
    parser.add_argument(
        'environment',
        choices=['dev', 'development', 'staging', 'stage', 'production', 'prod'],
        help='Target deployment environment'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simulate deployment without executing commands'
    )
    parser.add_argument(
        '--skip-checks',
        action='store_true',
        help='Skip pre-deployment checks'
    )
    parser.add_argument(
        '--rollback',
        action='store_true',
        help='Rollback to previous version'
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
        helper = DeploymentHelper(args.environment, dry_run=args.dry_run)

        if args.rollback:
            # Rollback
            success = helper.rollback()
            helper.print_summary()
            sys.exit(0 if success else 1)

        # Pre-deployment checks
        if not args.skip_checks:
            if not helper.pre_deployment_checks():
                logger.error("Pre-deployment checks failed")
                sys.exit(1)

        # Deploy
        success = helper.deploy()

        # Post-deployment checks
        if success:
            helper.post_deployment_checks()

        # Print summary
        helper.print_summary()

        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        logger.info("\nDeployment interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Deployment error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
