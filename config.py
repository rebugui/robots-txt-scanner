"""
Copyright (C) 2026 rebugui

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

"""
Configuration Module

This module provides configuration management and utility functions
for the robots.txt scanner.
"""

from dataclasses import dataclass
from typing import Optional
import json
from pathlib import Path


@dataclass
class ScannerConfig:
    """
    Configuration settings for the robots.txt scanner.
    
    Attributes:
        timeout: Request timeout in seconds
        max_concurrent: Maximum concurrent requests
        user_agent: User agent string
        retry_attempts: Number of retry attempts for failed requests
        retry_delay: Delay between retries in seconds
        include_content: Whether to include raw robots.txt content
        output_format: Output format ('json' or 'csv')
        verbose: Enable verbose output
    """
    timeout: int = 10
    max_concurrent: int = 10
    user_agent: str = "RobotsScanner/1.0"
    retry_attempts: int = 3
    retry_delay: float = 1.0
    include_content: bool = False
    output_format: str = "json"
    verbose: bool = False
    
    @classmethod
    def from_file(cls, config_path: str) -> 'ScannerConfig':
        """
        Load configuration from a JSON file.
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            ScannerConfig: Configuration object
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            json.JSONDecodeError: If config file is invalid JSON
        """
        with open(config_path, 'r', encoding='utf-8') as f:
            config_dict = json.load(f)
        return cls(**config_dict)
    
    def to_file(self, config_path: str) -> None:
        """
        Save configuration to a JSON file.
        
        Args:
            config_path: Path to save configuration
        """
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, indent=2)
    
    def validate(self) -> bool:
        """
        Validate configuration values.
        
        Returns:
            bool: True if configuration is valid
            
        Raises:
            ValueError: If configuration values are invalid
        """
        if self.timeout < 1:
            raise ValueError("Timeout must be at least 1 second")
        
        if self.max_concurrent < 1 or self.max_concurrent > 100:
            raise ValueError("Max concurrent must be between 1 and 100")
        
        if self.retry_attempts < 0 or self.retry_attempts > 10:
            raise ValueError("Retry attempts must be between 0 and 10")
        
        if self.retry_delay < 0:
            raise ValueError("Retry delay must be non-negative")
        
        return True


def create_sample_config(output_path: str = "config.json") -> None:
    """
    Create a sample configuration file.
    
    Args:
        output_path: Path to save sample config
    """
    config = ScannerConfig()
    config.to_file(output_path)
    print(f"Sample configuration saved to: {output_path}")


def format_size(size_bytes: int) -> str:
    """
    Format byte size to human-readable string.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        str: Formatted size string
        
    Example:
        >>> format_size(1024)
        '1.00 KB'
        >>> format_size(1536)
        '1.50 KB'
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if abs(size_bytes) < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to human-readable string.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        str: Formatted duration string
        
    Example:
        >>> format_duration(65.5)
        '1m 5.5s'
        >>> format_duration(3661)
        '1h 1m 1s'
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.1f}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours}h {minutes}m {secs}s"


def validate_file_path(file_path: str, must_exist: bool = True) -> Path:
    """
    Validate a file path.
    
    Args:
        file_path: Path to validate
        must_exist: Whether the file must exist
        
    Returns:
        Path: Validated Path object
        
    Raises:
        FileNotFoundError: If must_exist=True and file doesn't exist
        ValueError: If path is invalid
    """
    try:
        path = Path(file_path)
        
        if must_exist and not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        return path
        
    except Exception as e:
        raise ValueError(f"Invalid file path: {e}")


def print_banner():
    """Print application banner."""
    banner = """
╔═══════════════════════════════════════════════════╗
║                                                   ║
║           ROBOTS.TXT SCANNER v1.0.0              ║
║                                                   ║
║   Scan multiple websites and analyze             ║
║   their robots.txt files                         ║
║                                                   ║
║   by ChatDev                                     ║
║                                                   ║
╚═══════════════════════════════════════════════════╝
"""
    print(banner)


def print_progress(current: int, total: int, prefix: str = "Progress"):
    """
    Print progress indicator.
    
    Args:
        current: Current progress count
        total: Total count
        prefix: Prefix text
    """
    percent = (current / total) * 100 if total > 0 else 0
    bar_length = 50
    filled = int(bar_length * current // total) if total > 0 else 0
    bar = '█' * filled + '-' * (bar_length - filled)
    
    print(f'{prefix}: |{bar}| {percent:.1f}% ({current}/{total})', end='', flush=True)
    
    if current == total:
        print()  # New line when complete


if __name__ == "__main__":
    # Create sample config
    create_sample_config()
    
    # Test utilities
    print("
Utility Tests:")
    print(f"Format size: {format_size(1024567)}")
    print(f"Format duration: {format_duration(125.5)}")
    print_banner()
