#!/usr/bin/env python3
"""
System Monitor - Monitor system resources (CPU, memory, disk usage).

This script monitors system resources and can alert when thresholds are exceeded.
Useful for system health monitoring and capacity planning.
"""

import argparse
import logging
import sys
import time
from datetime import datetime
from typing import Dict, List

try:
    import psutil
except ImportError:
    print("Error: 'psutil' module not found. Install it with: pip install psutil")
    sys.exit(1)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class SystemMonitor:
    """Monitor system resources and performance metrics."""

    def __init__(self, cpu_threshold: float = 80.0, memory_threshold: float = 80.0,
                 disk_threshold: float = 80.0):
        """
        Initialize the system monitor.

        Args:
            cpu_threshold: CPU usage threshold percentage
            memory_threshold: Memory usage threshold percentage
            disk_threshold: Disk usage threshold percentage
        """
        self.cpu_threshold = cpu_threshold
        self.memory_threshold = memory_threshold
        self.disk_threshold = disk_threshold
        self.alerts = []

    def get_cpu_info(self) -> Dict:
        """
        Get CPU usage information.

        Returns:
            Dictionary containing CPU metrics
        """
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        cpu_count_logical = psutil.cpu_count(logical=True)
        cpu_freq = psutil.cpu_freq()

        info = {
            'usage_percent': cpu_percent,
            'count_physical': cpu_count,
            'count_logical': cpu_count_logical,
            'frequency_current': cpu_freq.current if cpu_freq else None,
            'frequency_min': cpu_freq.min if cpu_freq else None,
            'frequency_max': cpu_freq.max if cpu_freq else None,
            'per_cpu': psutil.cpu_percent(interval=1, percpu=True)
        }

        # Check threshold
        if cpu_percent > self.cpu_threshold:
            alert = f"CPU usage ({cpu_percent:.1f}%) exceeds threshold ({self.cpu_threshold}%)"
            self.alerts.append(('CPU', alert))
            logger.warning(alert)

        return info

    def get_memory_info(self) -> Dict:
        """
        Get memory usage information.

        Returns:
            Dictionary containing memory metrics
        """
        virtual_mem = psutil.virtual_memory()
        swap_mem = psutil.swap_memory()

        info = {
            'total': virtual_mem.total,
            'available': virtual_mem.available,
            'used': virtual_mem.used,
            'percent': virtual_mem.percent,
            'total_human': self._format_bytes(virtual_mem.total),
            'available_human': self._format_bytes(virtual_mem.available),
            'used_human': self._format_bytes(virtual_mem.used),
            'swap_total': swap_mem.total,
            'swap_used': swap_mem.used,
            'swap_percent': swap_mem.percent,
            'swap_total_human': self._format_bytes(swap_mem.total),
            'swap_used_human': self._format_bytes(swap_mem.used)
        }

        # Check threshold
        if virtual_mem.percent > self.memory_threshold:
            alert = f"Memory usage ({virtual_mem.percent:.1f}%) exceeds threshold ({self.memory_threshold}%)"
            self.alerts.append(('MEMORY', alert))
            logger.warning(alert)

        return info

    def get_disk_info(self, path: str = '/') -> Dict:
        """
        Get disk usage information.

        Args:
            path: Path to check disk usage for

        Returns:
            Dictionary containing disk metrics
        """
        disk_usage = psutil.disk_usage(path)
        disk_io = psutil.disk_io_counters()

        info = {
            'path': path,
            'total': disk_usage.total,
            'used': disk_usage.used,
            'free': disk_usage.free,
            'percent': disk_usage.percent,
            'total_human': self._format_bytes(disk_usage.total),
            'used_human': self._format_bytes(disk_usage.used),
            'free_human': self._format_bytes(disk_usage.free),
            'read_count': disk_io.read_count if disk_io else None,
            'write_count': disk_io.write_count if disk_io else None,
            'read_bytes': disk_io.read_bytes if disk_io else None,
            'write_bytes': disk_io.write_bytes if disk_io else None
        }

        # Check threshold
        if disk_usage.percent > self.disk_threshold:
            alert = f"Disk usage on {path} ({disk_usage.percent:.1f}%) exceeds threshold ({self.disk_threshold}%)"
            self.alerts.append(('DISK', alert))
            logger.warning(alert)

        return info

    def get_network_info(self) -> Dict:
        """
        Get network statistics.

        Returns:
            Dictionary containing network metrics
        """
        net_io = psutil.net_io_counters()
        net_connections = len(psutil.net_connections())

        info = {
            'bytes_sent': net_io.bytes_sent,
            'bytes_recv': net_io.bytes_recv,
            'packets_sent': net_io.packets_sent,
            'packets_recv': net_io.packets_recv,
            'errors_in': net_io.errin,
            'errors_out': net_io.errout,
            'bytes_sent_human': self._format_bytes(net_io.bytes_sent),
            'bytes_recv_human': self._format_bytes(net_io.bytes_recv),
            'connections': net_connections
        }

        return info

    def get_process_info(self, top_n: int = 5) -> List[Dict]:
        """
        Get information about top processes by CPU and memory usage.

        Args:
            top_n: Number of top processes to return

        Returns:
            List of dictionaries containing process information
        """
        processes = []

        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
            try:
                processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'username': proc.info['username'],
                    'cpu_percent': proc.info['cpu_percent'],
                    'memory_percent': proc.info['memory_percent']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        # Sort by CPU usage
        top_cpu = sorted(processes, key=lambda x: x['cpu_percent'] or 0, reverse=True)[:top_n]

        # Sort by memory usage
        top_mem = sorted(processes, key=lambda x: x['memory_percent'] or 0, reverse=True)[:top_n]

        return {'top_cpu': top_cpu, 'top_memory': top_mem}

    def get_system_info(self) -> Dict:
        """
        Get general system information.

        Returns:
            Dictionary containing system information
        """
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time

        return {
            'boot_time': boot_time.strftime('%Y-%m-%d %H:%M:%S'),
            'uptime': str(uptime).split('.')[0],  # Remove microseconds
            'platform': sys.platform,
            'users': len(psutil.users())
        }

    @staticmethod
    def _format_bytes(bytes_value: int) -> str:
        """Format bytes to human-readable size."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.2f} PB"

    def print_report(self, show_processes: bool = False) -> None:
        """
        Print a comprehensive system monitoring report.

        Args:
            show_processes: Whether to show top processes
        """
        print("\n" + "=" * 80)
        print("SYSTEM MONITORING REPORT")
        print("=" * 80)
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # System Info
        sys_info = self.get_system_info()
        print("\n" + "-" * 80)
        print("SYSTEM INFORMATION")
        print("-" * 80)
        print(f"Platform: {sys_info['platform']}")
        print(f"Boot Time: {sys_info['boot_time']}")
        print(f"Uptime: {sys_info['uptime']}")
        print(f"Users: {sys_info['users']}")

        # CPU Info
        cpu_info = self.get_cpu_info()
        print("\n" + "-" * 80)
        print("CPU USAGE")
        print("-" * 80)
        print(f"Usage: {cpu_info['usage_percent']:.1f}%")
        print(f"Physical Cores: {cpu_info['count_physical']}")
        print(f"Logical Cores: {cpu_info['count_logical']}")
        if cpu_info['frequency_current']:
            print(f"Frequency: {cpu_info['frequency_current']:.2f} MHz")

        # Memory Info
        mem_info = self.get_memory_info()
        print("\n" + "-" * 80)
        print("MEMORY USAGE")
        print("-" * 80)
        print(f"Usage: {mem_info['percent']:.1f}%")
        print(f"Total: {mem_info['total_human']}")
        print(f"Used: {mem_info['used_human']}")
        print(f"Available: {mem_info['available_human']}")
        print(f"Swap Usage: {mem_info['swap_percent']:.1f}%")
        print(f"Swap Used: {mem_info['swap_used_human']} / {mem_info['swap_total_human']}")

        # Disk Info
        disk_info = self.get_disk_info()
        print("\n" + "-" * 80)
        print("DISK USAGE")
        print("-" * 80)
        print(f"Path: {disk_info['path']}")
        print(f"Usage: {disk_info['percent']:.1f}%")
        print(f"Total: {disk_info['total_human']}")
        print(f"Used: {disk_info['used_human']}")
        print(f"Free: {disk_info['free_human']}")

        # Network Info
        net_info = self.get_network_info()
        print("\n" + "-" * 80)
        print("NETWORK STATISTICS")
        print("-" * 80)
        print(f"Bytes Sent: {net_info['bytes_sent_human']}")
        print(f"Bytes Received: {net_info['bytes_recv_human']}")
        print(f"Packets Sent: {net_info['packets_sent']:,}")
        print(f"Packets Received: {net_info['packets_recv']:,}")
        print(f"Active Connections: {net_info['connections']}")

        # Top Processes
        if show_processes:
            proc_info = self.get_process_info()

            print("\n" + "-" * 80)
            print("TOP PROCESSES BY CPU")
            print("-" * 80)
            print(f"{'PID':<8} {'Name':<25} {'User':<15} {'CPU%':<8}")
            print("-" * 80)
            for proc in proc_info['top_cpu']:
                print(f"{proc['pid']:<8} {proc['name'][:24]:<25} {proc['username'][:14]:<15} {proc['cpu_percent']:<8.1f}")

            print("\n" + "-" * 80)
            print("TOP PROCESSES BY MEMORY")
            print("-" * 80)
            print(f"{'PID':<8} {'Name':<25} {'User':<15} {'MEM%':<8}")
            print("-" * 80)
            for proc in proc_info['top_memory']:
                print(f"{proc['pid']:<8} {proc['name'][:24]:<25} {proc['username'][:14]:<15} {proc['memory_percent']:<8.1f}")

        # Alerts
        if self.alerts:
            print("\n" + "-" * 80)
            print("ALERTS")
            print("-" * 80)
            for alert_type, alert_msg in self.alerts:
                print(f"[{alert_type}] {alert_msg}")

        print("\n" + "=" * 80 + "\n")


def main():
    """Main function to parse arguments and monitor system."""
    parser = argparse.ArgumentParser(
        description='Monitor system resources (CPU, memory, disk)'
    )
    parser.add_argument(
        '--cpu-threshold',
        type=float,
        default=80.0,
        help='CPU usage alert threshold percentage (default: 80)'
    )
    parser.add_argument(
        '--memory-threshold',
        type=float,
        default=80.0,
        help='Memory usage alert threshold percentage (default: 80)'
    )
    parser.add_argument(
        '--disk-threshold',
        type=float,
        default=80.0,
        help='Disk usage alert threshold percentage (default: 80)'
    )
    parser.add_argument(
        '--interval',
        type=int,
        help='Monitor continuously with specified interval in seconds'
    )
    parser.add_argument(
        '--processes',
        action='store_true',
        help='Show top processes by CPU and memory usage'
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
        monitor = SystemMonitor(
            cpu_threshold=args.cpu_threshold,
            memory_threshold=args.memory_threshold,
            disk_threshold=args.disk_threshold
        )

        if args.interval:
            logger.info(f"Starting continuous monitoring (interval: {args.interval}s, Ctrl+C to stop)")
            iteration = 1
            while True:
                print(f"\n{'*' * 80}")
                print(f"Iteration #{iteration}")
                print('*' * 80)
                monitor.print_report(show_processes=args.processes)
                monitor.alerts.clear()  # Clear alerts for next iteration
                iteration += 1
                time.sleep(args.interval)
        else:
            monitor.print_report(show_processes=args.processes)

        # Exit with error if alerts were triggered
        if monitor.alerts:
            sys.exit(1)

    except KeyboardInterrupt:
        logger.info("\nMonitoring interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Monitoring error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
