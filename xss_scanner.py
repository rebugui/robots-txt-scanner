#!/usr/bin/env python3
"""XSS Scanner - Auto-generated scanner module"""

import asyncio
import aiohttp
from typing import List, Dict, Optional
from urllib.parse import urlparse


class Scanner:
    """Base scanner class with async support."""
    
    def __init__(self, max_workers: int = 50, timeout: int = 10):
        self.max_workers = max_workers
        self.timeout = aiohttp.ClientTimeout(total=timeout)
    
    async def fetch(self, session: aiohttp.ClientSession, url: str) -> Optional[str]:
        """Fetch content from URL.
        
        Args:
            session: aiohttp session
            url: Target URL
        
        Returns:
            Content string or None on error
        """
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.text()
        except Exception as e:
            print(f"Error fetching {url}: {e}")
        return None
    
    async def scan_urls(self, urls: List[str]) -> Dict[str, Optional[str]]:
        """Scan multiple URLs concurrently.
        
        Args:
            urls: List of URLs to scan
        
        Returns:
            Dict mapping URLs to their content
        """
        results = {}
        
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            tasks = [self.fetch(session, url) for url in urls]
            contents = await asyncio.gather(*tasks, return_exceptions=True)
            
            for url, content in zip(urls, contents):
                if isinstance(content, Exception):
                    results[url] = None
                else:
                    results[url] = content
        
        return results


if __name__ == "__main__":
    # Demo
    async def demo():
        scanner = Scanner()
        urls = ["https://example.com", "https://example.org"]
        results = await scanner.scan_urls(urls)
        for url, content in results.items():
            print(f"{url}: {len(content) if content else 0} bytes")
    
    asyncio.run(demo())
