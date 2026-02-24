#!/usr/bin/env python3
"""
Robots.txt Scanner - Main Entry Point

This is the main module to launch the robots.txt scanner program.
It provides a CLI interface for scanning multiple URLs and exporting results.

Usage:
    python main.py --url https://example.com
    python main.py --file urls.txt
    python main.py --url https://example.com https://test.com
    python main.py --file urls.txt --output results.json --concurrent 20
"""

import argparse
import sys
from pathlib import Path
from typing import List

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from url_collector import URLCollector
from robots_scanner import RobotsScanner, RobotsEntry
from result_formatter import ResultFormatter


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description='Scan robots.txt files from multiple websites',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Scan a single URL:
    python main.py --url https://example.com
    
  Scan multiple URLs:
    python main.py --url https://example.com https://test.com
    
  Scan from file:
    python main.py --file urls.txt
    
  Save results to file:
    python main.py --file urls.txt --output results.json
    
  Increase concurrent requests:
    python main.py --file urls.txt --concurrent 20
    
  Include raw robots.txt content:
    python main.py --file urls.txt --include-content
        """
    )
    
    # Input sources (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '--url', '-u',
        nargs='+',
        metavar='URL',
        help='One or more URLs to scan'
    )
    input_group.add_argument(
        '--file', '-f',
        metavar='FILE',
        help='Path to file containing URLs (one per line)'
    )
    
    # Output options
    parser.add_argument(
        '--output', '-o',
        metavar='FILE',
        help='Output JSON file path (default: stdout)'
    )
    
    # Scan options
    parser.add_argument(
        '--concurrent', '-c',
        type=int,
        default=10,
        metavar='NUM',
        help='Maximum concurrent requests (default: 10)'
    )
    
    parser.add_argument(
        '--timeout', '-t',
        type=int,
        default=10,
        metavar='SEC',
        help='Request timeout in seconds (default: 10)'
    )
    
    parser.add_argument(
        '--user-agent',
        default='RobotsScanner/1.0',
        metavar='AGENT',
        help='User agent string for requests'
    )
    
    parser.add_argument(
        '--include-content',
        action='store_true',
        help='Include raw robots.txt content in output'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress summary output'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show verbose output'
    )
    
    return parser.parse_args()


def collect_urls(args: argparse.Namespace) -> List[str]:
    """
    Collect URLs from command-line arguments.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        List[str]: List of base URLs to scan
        
    Raises:
        ValueError: If no valid URLs are found
        FileNotFoundError: If input file is not found
    """
    collector = URLCollector()
    
    if args.url:
        # Collect from command-line URLs
        if args.verbose:
            print(f"[*] Adding {len(args.url)} URL(s) from command line...")
        
        stats = collector.add_urls_from_list(args.url)
        
        if args.verbose:
            print(f"    Added: {stats['added']}, Invalid: {stats['invalid']}, Duplicates: {stats['duplicates']}")
        
    elif args.file:
        # Collect from file
        if args.verbose:
            print(f"[*] Reading URLs from file: {args.file}")
        
        stats = collector.add_urls_from_file(args.file)
        
        if args.verbose:
            print(f"    Total lines: {stats['total_lines']}, Added: {stats['added']}, Invalid: {stats['invalid']}, Duplicates: {stats['duplicates']}")
    
    # Get base URLs for scanning
    base_urls = collector.get_base_urls()
    
    if not base_urls:
        raise ValueError("No valid URLs found to scan")
    
    return base_urls


def scan_robots(
    urls: List[str],
    concurrent: int,
    timeout: int,
    user_agent: str,
    verbose: bool = False
) -> List[RobotsEntry]:
    """
    Scan robots.txt for all URLs.
    
    Args:
        urls: List of base URLs to scan
        concurrent: Maximum concurrent requests
        timeout: Request timeout in seconds
        user_agent: User agent string
        verbose: Show verbose output
        
    Returns:
        List[RobotsEntry]: List of scan results
    """
    if verbose:
        print(f"\n[*] Starting robots.txt scan...")
        print(f"    URLs to scan: {len(urls)}")
        print(f"    Concurrent requests: {concurrent}")
        print(f"    Timeout: {timeout}s")
        print(f"    User Agent: {user_agent}")
        print()
    
    scanner = RobotsScanner(
        timeout=timeout,
        max_concurrent=concurrent,
        user_agent=user_agent
    )
    
    results = scanner.scan_urls_sync(urls)
    
    if verbose:
        print(f"\n[*] Scan completed. {len(results)} results collected.")
    
    return results


def output_results(
    results: List[RobotsEntry],
    output_file: str = None,
    include_content: bool = False,
    quiet: bool = False,
    verbose: bool = False
) -> None:
    """
    Format and output results.
    
    Args:
        results: List of scan results
        output_file: Path to output JSON file (optional)
        include_content: Include raw robots.txt content
        quiet: Suppress summary output
        verbose: Show verbose output
    """
    formatter = ResultFormatter(results)
    
    if output_file:
        # Save to file
        if verbose:
            print(f"\n[*] Saving results to: {output_file}")
        
        formatter.save_to_file(
            output_file,
            include_content=include_content
        )
        
        if verbose:
            print(f"    Results saved successfully.")
        
        # Show summary unless quiet
        if not quiet:
            print("\n" + formatter.get_summary())
    else:
        # Output to stdout
        print(formatter.to_json(include_content=include_content))
        
        # Show summary if verbose and not quiet
        if verbose and not quiet:
            print("\n" + formatter.get_summary())


def main() -> int:
    """
    Main entry point for the robots.txt scanner.
    
    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    try:
        # Parse arguments
        args = parse_arguments()
        
        # Collect URLs
        urls = collect_urls(args)
        
        if args.verbose:
            print(f"\n[*] Found {len(urls)} unique base URLs to scan")
        
        # Scan robots.txt
        results = scan_robots(
            urls,
            concurrent=args.concurrent,
            timeout=args.timeout,
            user_agent=args.user_agent,
            verbose=args.verbose
        )
        
        # Output results
        output_results(
            results,
            output_file=args.output,
            include_content=args.include_content,
            quiet=args.quiet,
            verbose=args.verbose
        )
        
        return 0
        
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    except KeyboardInterrupt:
        print("\n\nScan interrupted by user.", file=sys.stderr)
        return 1
    
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        # Check if args exists and verbose mode is enabled before showing traceback
        if 'args' in locals() and hasattr(args, 'verbose') and args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
