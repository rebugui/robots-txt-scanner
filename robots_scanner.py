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
Robots.txt Scanner Module

This module provides asynchronous functionality to scan robots.txt files
from multiple websites and extract their contents and metadata.
"""

import aiohttp
import asyncio
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlparse
from dataclasses import dataclass, asdict
from datetime import datetime
import re


@dataclass
class RobotsEntry:
    """
    Data class representing a robots.txt scan result.
    
    Attributes:
        url: Base URL of the website
        robots_url: Full URL to robots.txt
        status_code: HTTP status code
        content: Raw robots.txt content
        exists: Whether robots.txt exists (200 status)
        accessible: Whether robots.txt is accessible
        sitemaps: List of sitemap URLs found
        user_agents: List of user agents defined
        disallowed_paths: Dict of user agents to their disallowed paths
        allowed_paths: Dict of user agents to their allowed paths
        crawl_delay: Dict of user agents to their crawl delay
        error: Error message if any
        scan_time: Timestamp of scan
        response_time: Time taken to fetch robots.txt (seconds)
    """
    url: str
    robots_url: str
    status_code: Optional[int] = None
    content: Optional[str] = None
    exists: bool = False
    accessible: bool = False
    sitemaps: List[str] = None
    user_agents: List[str] = None
    disallowed_paths: Dict[str, List[str]] = None
    allowed_paths: Dict[str, List[str]] = None
    crawl_delay: Dict[str, Optional[int]] = None
    error: Optional[str] = None
    scan_time: str = None
    response_time: Optional[float] = None
    
    def __post_init__(self):
        """Initialize default values for list and dict fields."""
        if self.sitemaps is None:
            self.sitemaps = []
        if self.user_agents is None:
            self.user_agents = []
        if self.disallowed_paths is None:
            self.disallowed_paths = {}
        if self.allowed_paths is None:
            self.allowed_paths = {}
        if self.crawl_delay is None:
            self.crawl_delay = {}
        if self.scan_time is None:
            self.scan_time = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        """Convert entry to dictionary."""
        return asdict(self)


class RobotsScanner:
    """
    Asynchronous robots.txt scanner for multiple websites.
    
    This class provides functionality to:
    - Fetch robots.txt from multiple URLs asynchronously
    - Parse robots.txt content
    - Extract metadata (sitemaps, user agents, directives)
    - Handle errors gracefully
    
    Attributes:
        timeout: Request timeout in seconds
        max_concurrent: Maximum concurrent requests
        user_agent: User agent string for requests
    """
    
    def __init__(
        self,
        timeout: int = 10,
        max_concurrent: int = 10,
        user_agent: str = "RobotsScanner/1.0"
    ):
        """
        Initialize RobotsScanner.
        
        Args:
            timeout: Request timeout in seconds (default: 10)
            max_concurrent: Maximum concurrent requests (default: 10)
            user_agent: User agent string for requests
        """
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.max_concurrent = max_concurrent
        self.user_agent = user_agent
        self._semaphore: Optional[asyncio.Semaphore] = None
    
    def _get_robots_url(self, base_url: str) -> str:
        """
        Construct robots.txt URL from base URL.
        
        Args:
            base_url: Base URL of the website
            
        Returns:
            str: Full URL to robots.txt
            
        Example:
            >>> scanner = RobotsScanner()
            >>> scanner._get_robots_url("https://example.com")
            'https://example.com/robots.txt'
        """
        parsed = urlparse(base_url)
        return f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    
    def _parse_robots_content(self, content: str) -> Tuple[List[str], Dict, Dict, Dict, Dict]:
        """
        Parse robots.txt content and extract directives.
        
        Args:
            content: Raw robots.txt content
            
        Returns:
            Tuple containing:
                - List of sitemap URLs
                - Dict of user agents to disallowed paths
                - Dict of user agents to allowed paths
                - Dict of user agents to crawl delays
                - List of user agents
                
        Example:
            >>> scanner = RobotsScanner()
            >>> content = "User-agent: *\nDisallow: /admin\nSitemap: https://example.com/sitemap.xml"
            >>> sitemaps, disallowed, allowed, delays, agents = scanner._parse_robots_content(content)
        """
        sitemaps = []
        user_agents = []
        disallowed_paths = {}
        allowed_paths = {}
        crawl_delay = {}
        
        current_agent = '*'
        
        lines = content.split('
')
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            
            # Split by first colon
            if ':' not in line:
                continue
            
            key, value = line.split(':', 1)
            key = key.strip().lower()
            value = value.strip()
            
            if key == 'user-agent':
                current_agent = value
                if current_agent not in user_agents:
                    user_agents.append(current_agent)
                if current_agent not in disallowed_paths:
                    disallowed_paths[current_agent] = []
                if current_agent not in allowed_paths:
                    allowed_paths[current_agent] = []
                    
            elif key == 'disallow':
                if current_agent not in disallowed_paths:
                    disallowed_paths[current_agent] = []
                if value:  # Only add non-empty values
                    disallowed_paths[current_agent].append(value)
                    
            elif key == 'allow':
                if current_agent not in allowed_paths:
                    allowed_paths[current_agent] = []
                if value:
                    allowed_paths[current_agent].append(value)
                    
            elif key == 'sitemap':
                if value:
                    sitemaps.append(value)
                    
            elif key == 'crawl-delay':
                if current_agent not in crawl_delay:
                    try:
                        crawl_delay[current_agent] = int(value)
                    except ValueError:
                        crawl_delay[current_agent] = None
        
        # Remove empty entries
        disallowed_paths = {k: v for k, v in disallowed_paths.items() if v}
        allowed_paths = {k: v for k, v in allowed_paths.items() if v}
        
        return sitemaps, disallowed_paths, allowed_paths, crawl_delay, user_agents
    
    async def scan_single_url(
        self,
        session: aiohttp.ClientSession,
        url: str
    ) -> RobotsEntry:
        """
        Scan robots.txt for a single URL.
        
        Args:
            session: aiohttp client session
            url: Base URL to scan
            
        Returns:
            RobotsEntry: Scan result entry
        """
        robots_url = self._get_robots_url(url)
        entry = RobotsEntry(url=url, robots_url=robots_url)
        
        try:
            start_time = asyncio.get_event_loop().time()
            
            headers = {'User-Agent': self.user_agent}
            
            async with session.get(robots_url, headers=headers) as response:
                entry.status_code = response.status
                entry.exists = response.status == 200
                entry.accessible = response.status in [200, 401, 403]
                
                if response.status == 200:
                    entry.content = await response.text()
                    
                    # Parse content
                    (entry.sitemaps,
                     entry.disallowed_paths,
                     entry.allowed_paths,
                     entry.crawl_delay,
                     entry.user_agents) = self._parse_robots_content(entry.content)
                
                end_time = asyncio.get_event_loop().time()
                entry.response_time = round(end_time - start_time, 3)
                
        except asyncio.TimeoutError:
            entry.error = "Request timeout"
            entry.accessible = False
        except aiohttp.ClientConnectorCertificateError as e:
            # SSL certificate verification failed - security issue detected
            entry.error = f"SSL certificate error: {str(e)}"
            entry.accessible = False
        except aiohttp.ClientSSLError as e:
            # Generic SSL error during connection
            entry.error = f"SSL error: {str(e)}"
            entry.accessible = False
        except aiohttp.ClientError as e:
            entry.error = f"Connection error: {str(e)}"
            entry.accessible = False
        except Exception as e:
            entry.error = f"Unexpected error: {str(e)}"
            entry.accessible = False
        
        return entry
    
    async def scan_urls(self, urls: List[str]) -> List[RobotsEntry]:
        """
        Scan robots.txt for multiple URLs asynchronously.
        
        Args:
            urls: List of base URLs to scan
            
        Returns:
            List[RobotsEntry]: List of scan results
            
        Example:
            >>> scanner = RobotsScanner()
            >>> urls = ["https://example.com", "https://test.com"]
            >>> results = await scanner.scan_urls(urls)
        """
        if not urls:
            return []
        
        self._semaphore = asyncio.Semaphore(self.max_concurrent)
        
        async def bounded_scan(session: aiohttp.ClientSession, url: str) -> RobotsEntry:
            """Scan with semaphore to limit concurrent requests."""
            async with self._semaphore:
                return await self.scan_single_url(session, url)
        
        # SECURITY: Use default SSL context with certificate verification enabled
        # This prevents Man-in-the-Middle (MITM) attacks and ensures data integrity
        connector = aiohttp.TCPConnector(limit=self.max_concurrent)
        
        async with aiohttp.ClientSession(timeout=self.timeout, connector=connector) as session:
            tasks = [bounded_scan(session, url) for url in urls]
            results = await asyncio.gather(*tasks, return_exceptions=False)
        
        return results
    
    def scan_urls_sync(self, urls: List[str]) -> List[RobotsEntry]:
        """
        Synchronous wrapper for scan_urls.
        
        Args:
            urls: List of base URLs to scan
            
        Returns:
            List[RobotsEntry]: List of scan results
            
        Example:
            >>> scanner = RobotsScanner()
            >>> urls = ["https://example.com", "https://test.com"]
            >>> results = scanner.scan_urls_sync(urls)
        """
        return asyncio.run(self.scan_urls(urls))
