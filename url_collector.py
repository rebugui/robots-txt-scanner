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
URL Collector Module

This module provides functionality to collect and validate URLs from various sources
including files, lists, and strings.
"""

from typing import List, Set
from urllib.parse import urlparse
import re


class URLCollector:
    """
    Collects and validates URLs from multiple sources.
    
    Attributes:
        urls (Set[str]): Set of unique validated URLs
    """
    
    # Regex pattern for URL validation
    URL_PATTERN = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    def __init__(self):
        """Initialize URLCollector with empty URL set."""
        self.urls: Set[str] = set()
    
    def validate_url(self, url: str) -> bool:
        """
        Validate if a string is a proper HTTP/HTTPS URL.
        
        Args:
            url: URL string to validate
            
        Returns:
            bool: True if URL is valid, False otherwise
            
        Example:
            >>> collector = URLCollector()
            >>> collector.validate_url("https://example.com")
            True
            >>> collector.validate_url("not-a-url")
            False
        """
        try:
            result = urlparse(url.strip())
            is_valid = all([
                result.scheme in ['http', 'https'],
                result.netloc,
                self.URL_PATTERN.match(url.strip()) is not None
            ])
            return is_valid
        except Exception:
            return False
    
    def normalize_url(self, url: str) -> str:
        """
        Normalize URL by removing trailing slash and fragments.
        
        Args:
            url: URL string to normalize
            
        Returns:
            str: Normalized URL
            
        Example:
            >>> collector = URLCollector()
            >>> collector.normalize_url("https://example.com/")
            'https://example.com'
        """
        url = url.strip()
        # Remove fragment
        if '#' in url:
            url = url.split('#')[0]
        # Remove trailing slash
        return url.rstrip('/')
    
    def add_url(self, url: str) -> bool:
        """
        Add a single URL to the collection after validation.
        
        Args:
            url: URL string to add
            
        Returns:
            bool: True if URL was added successfully, False if invalid
            
        Raises:
            ValueError: If URL is empty or None
        """
        if not url or not url.strip():
            raise ValueError("URL cannot be empty or None")
        
        url = url.strip()
        if self.validate_url(url):
            normalized = self.normalize_url(url)
            self.urls.add(normalized)
            return True
        return False
    
    def add_urls_from_list(self, url_list: List[str]) -> dict:
        """
        Add multiple URLs from a list.
        
        Args:
            url_list: List of URL strings
            
        Returns:
            dict: Statistics with 'added', 'invalid', 'duplicates' counts
            
        Example:
            >>> collector = URLCollector()
            >>> result = collector.add_urls_from_list([
            ...     "https://example.com",
            ...     "https://test.com",
            ...     "invalid-url"
            ... ])
            >>> print(result)
            {'added': 2, 'invalid': 1, 'duplicates': 0}
        """
        if not url_list:
            raise ValueError("URL list cannot be empty")
        
        stats = {'added': 0, 'invalid': 0, 'duplicates': 0}
        
        for url in url_list:
            if not url or not url.strip():
                stats['invalid'] += 1
                continue
            
            url = url.strip()
            if self.validate_url(url):
                normalized = self.normalize_url(url)
                if normalized in self.urls:
                    stats['duplicates'] += 1
                else:
                    self.urls.add(normalized)
                    stats['added'] += 1
            else:
                stats['invalid'] += 1
        
        return stats
    
    def add_urls_from_file(self, file_path: str) -> dict:
        """
        Read and add URLs from a text file (one URL per line).
        
        Args:
            file_path: Path to the file containing URLs
            
        Returns:
            dict: Statistics with 'added', 'invalid', 'duplicates', 'total_lines' counts
            
        Raises:
            FileNotFoundError: If file does not exist
            IOError: If file cannot be read
            
        Example:
            >>> collector = URLCollector()
            >>> result = collector.add_urls_from_file('urls.txt')
        """
        stats = {'added': 0, 'invalid': 0, 'duplicates': 0, 'total_lines': 0}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for line in lines:
                stats['total_lines'] += 1
                url = line.strip()
                
                # Skip empty lines and comments
                if not url or url.startswith('#'):
                    continue
                
                if self.validate_url(url):
                    normalized = self.normalize_url(url)
                    if normalized in self.urls:
                        stats['duplicates'] += 1
                    else:
                        self.urls.add(normalized)
                        stats['added'] += 1
                else:
                    stats['invalid'] += 1
            
            return stats
            
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except IOError as e:
            raise IOError(f"Error reading file {file_path}: {e}")
    
    def get_base_urls(self) -> List[str]:
        """
        Get base URLs (scheme + netloc) for all collected URLs.
        
        Returns:
            List[str]: List of unique base URLs
            
        Example:
            >>> collector = URLCollector()
            >>> collector.add_url("https://example.com/path")
            >>> collector.get_base_urls()
            ['https://example.com']
        """
        base_urls = set()
        for url in self.urls:
            parsed = urlparse(url)
            base_url = f"{parsed.scheme}://{parsed.netloc}"
            base_urls.add(base_url)
        return sorted(list(base_urls))
    
    def get_all_urls(self) -> List[str]:
        """
        Get all collected URLs as a sorted list.
        
        Returns:
            List[str]: Sorted list of all URLs
        """
        return sorted(list(self.urls))
    
    def clear(self) -> None:
        """Clear all collected URLs."""
        self.urls.clear()
    
    def count(self) -> int:
        """
        Get the count of collected URLs.
        
        Returns:
            int: Number of URLs in collection
        """
        return len(self.urls)
    
    def __len__(self) -> int:
        """Return the number of URLs in collection."""
        return len(self.urls)
    
    def __repr__(self) -> str:
        """String representation of URLCollector."""
        return f"URLCollector(urls_count={len(self.urls)})"
