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
Result Formatter Module

This module provides functionality to format and export robots.txt scan results
to various formats including JSON, with statistics and summaries.
"""

import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from robots_scanner import RobotsEntry


class ResultFormatter:
    """
    Formats and exports robots.txt scan results to JSON.
    
    This class provides functionality to:
    - Convert scan results to JSON format
    - Generate statistics and summaries
    - Export to files or strings
    - Pretty-print results
    
    Attributes:
        results: List of RobotsEntry results
        scan_metadata: Metadata about the scan
    """
    
    def __init__(self, results: Optional[List[RobotsEntry]] = None):
        """
        Initialize ResultFormatter.
        
        Args:
            results: Optional list of RobotsEntry results
        """
        self.results: List[RobotsEntry] = results or []
        self.scan_metadata: Dict[str, Any] = {
            'scan_start_time': datetime.now().isoformat(),
            'scanner_version': '1.0.0'
        }
    
    def add_result(self, result: RobotsEntry) -> None:
        """
        Add a single result to the collection.
        
        Args:
            result: RobotsEntry to add
        """
        self.results.append(result)
    
    def add_results(self, results: List[RobotsEntry]) -> None:
        """
        Add multiple results to the collection.
        
        Args:
            results: List of RobotsEntry objects
        """
        self.results.extend(results)
    
    def calculate_statistics(self) -> Dict[str, Any]:
        """
        Calculate statistics from scan results.
        
        Returns:
            Dict containing various statistics:
                - total_urls: Total number of URLs scanned
                - robots_exists: Number of sites with robots.txt
                - robots_not_found: Number of sites without robots.txt
                - accessible: Number of accessible sites
                - inaccessible: Number of inaccessible sites
                - with_sitemaps: Number of sites with sitemaps
                - total_sitemaps: Total number of sitemaps found
                - with_errors: Number of scans with errors
                - avg_response_time: Average response time
                
        Example:
            >>> formatter = ResultFormatter(results)
            >>> stats = formatter.calculate_statistics()
            >>> print(stats['total_urls'])
            10
        """
        stats = {
            'total_urls': len(self.results),
            'robots_exists': 0,
            'robots_not_found': 0,
            'accessible': 0,
            'inaccessible': 0,
            'with_sitemaps': 0,
            'total_sitemaps': 0,
            'with_errors': 0,
            'with_user_agents': 0,
            'with_disallow_rules': 0,
            'with_allow_rules': 0,
            'avg_response_time': 0.0,
            'min_response_time': None,
            'max_response_time': None,
        }
        
        response_times = []
        
        for entry in self.results:
            # Count robots.txt existence
            if entry.exists:
                stats['robots_exists'] += 1
            else:
                stats['robots_not_found'] += 1
            
            # Count accessibility
            if entry.accessible:
                stats['accessible'] += 1
            else:
                stats['inaccessible'] += 1
            
            # Count sitemaps
            if entry.sitemaps:
                stats['with_sitemaps'] += 1
                stats['total_sitemaps'] += len(entry.sitemaps)
            
            # Count user agents
            if entry.user_agents:
                stats['with_user_agents'] += 1
            
            # Count rules
            if entry.disallowed_paths:
                stats['with_disallow_rules'] += 1
            
            if entry.allowed_paths:
                stats['with_allow_rules'] += 1
            
            # Count errors
            if entry.error:
                stats['with_errors'] += 1
            
            # Collect response times
            if entry.response_time is not None:
                response_times.append(entry.response_time)
        
        # Calculate response time stats
        if response_times:
            stats['avg_response_time'] = round(sum(response_times) / len(response_times), 3)
            stats['min_response_time'] = min(response_times)
            stats['max_response_time'] = max(response_times)
        
        return stats
    
    def to_dict(self, include_content: bool = False) -> Dict[str, Any]:
        """
        Convert all results to a dictionary format.
        
        Args:
            include_content: Whether to include raw robots.txt content (default: False)
            
        Returns:
            Dict containing:
                - metadata: Scan metadata and statistics
                - results: List of result dictionaries
                
        Example:
            >>> formatter = ResultFormatter(results)
            >>> data = formatter.to_dict()
        """
        self.scan_metadata['scan_end_time'] = datetime.now().isoformat()
        
        results_list = []
        for entry in self.results:
            entry_dict = entry.to_dict()
            if not include_content:
                entry_dict.pop('content', None)
            results_list.append(entry_dict)
        
        return {
            'metadata': {
                **self.scan_metadata,
                'statistics': self.calculate_statistics()
            },
            'results': results_list
        }
    
    def to_json(
        self,
        indent: int = 2,
        include_content: bool = False,
        ensure_ascii: bool = False
    ) -> str:
        """
        Convert results to JSON string.
        
        Args:
            indent: JSON indentation level (default: 2)
            include_content: Whether to include raw robots.txt content
            ensure_ascii: Whether to escape non-ASCII characters
            
        Returns:
            str: JSON formatted string
            
        Example:
            >>> formatter = ResultFormatter(results)
            >>> json_str = formatter.to_json()
            >>> print(json_str[:100])
        """
        data = self.to_dict(include_content=include_content)
        return json.dumps(data, indent=indent, ensure_ascii=ensure_ascii)
    
    def save_to_file(
        self,
        file_path: str,
        indent: int = 2,
        include_content: bool = False,
        ensure_ascii: bool = False
    ) -> None:
        """
        Save results to a JSON file.
        
        Args:
            file_path: Path to output file
            indent: JSON indentation level (default: 2)
            include_content: Whether to include raw robots.txt content
            ensure_ascii: Whether to escape non-ASCII characters
            
        Raises:
            IOError: If file cannot be written
            
        Example:
            >>> formatter = ResultFormatter(results)
            >>> formatter.save_to_file('output.json')
        """
        try:
            data = self.to_dict(include_content=include_content)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii)
        except IOError as e:
            raise IOError(f"Failed to save file {file_path}: {e}")
    
    def get_summary(self) -> str:
        """
        Generate a human-readable summary of scan results.
        
        Returns:
            str: Formatted summary string
            
        Example:
            >>> formatter = ResultFormatter(results)
            >>> print(formatter.get_summary())
        """
        stats = self.calculate_statistics()
        
        summary_lines = [
            "=" * 60,
            "ROBOTS.TXT SCAN SUMMARY",
            "=" * 60,
            f"Total URLs Scanned: {stats['total_urls']}",
            "",
            "Results:",
            f"  - Robots.txt Found: {stats['robots_exists']}",
            f"  - Robots.txt Not Found: {stats['robots_not_found']}",
            f"  - Accessible Sites: {stats['accessible']}",
            f"  - Inaccessible Sites: {stats['inaccessible']}",
            "",
            "Content Analysis:",
            f"  - Sites with Sitemaps: {stats['with_sitemaps']}",
            f"  - Total Sitemaps Found: {stats['total_sitemaps']}",
            f"  - Sites with User Agents: {stats['with_user_agents']}",
            f"  - Sites with Disallow Rules: {stats['with_disallow_rules']}",
            f"  - Sites with Allow Rules: {stats['with_allow_rules']}",
            "",
            "Performance:",
        ]
        
        if stats['avg_response_time']:
            summary_lines.extend([
                f"  - Average Response Time: {stats['avg_response_time']}s",
                f"  - Min Response Time: {stats['min_response_time']}s",
                f"  - Max Response Time: {stats['max_response_time']}s",
            ])
        else:
            summary_lines.append("  - Response time data not available")
        
        if stats['with_errors'] > 0:
            summary_lines.extend([
                "",
                f"Errors: {stats['with_errors']} URLs had scanning errors"
            ])
        
        summary_lines.extend(["", "=" * 60])
        
        return "
".join(summary_lines)
    
    def filter_by(
        self,
        has_robots: Optional[bool] = None,
        has_sitemap: Optional[bool] = None,
        has_error: Optional[bool] = None,
        min_response_time: Optional[float] = None,
        max_response_time: Optional[float] = None
    ) -> 'ResultFormatter':
        """
        Filter results by various criteria and return new formatter.
        
        Args:
            has_robots: Filter by robots.txt existence
            has_sitemap: Filter by sitemap presence
            has_error: Filter by error presence
            min_response_time: Minimum response time filter
            max_response_time: Maximum response time filter
            
        Returns:
            ResultFormatter: New formatter with filtered results
            
        Example:
            >>> formatter = ResultFormatter(results)
            >>> with_robots = formatter.filter_by(has_robots=True)
        """
        filtered_results = []
        
        for entry in self.results:
            # Apply filters
            if has_robots is not None and entry.exists != has_robots:
                continue
            
            if has_sitemap is not None and bool(entry.sitemaps) != has_sitemap:
                continue
            
            if has_error is not None and bool(entry.error) != has_error:
                continue
            
            if min_response_time is not None:
                if entry.response_time is None or entry.response_time < min_response_time:
                    continue
            
            if max_response_time is not None:
                if entry.response_time is None or entry.response_time > max_response_time:
                    continue
            
            filtered_results.append(entry)
        
        return ResultFormatter(filtered_results)
    
    def __len__(self) -> int:
        """Return number of results."""
        return len(self.results)
    
    def __repr__(self) -> str:
        """String representation."""
        return f"ResultFormatter(results_count={len(self.results)})"
