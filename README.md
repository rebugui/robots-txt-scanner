# Robots.txt Scanner

다량의 URL을 수집하고 robots.txt를 스캔한 후 JSON 형식으로 결과를 출력하는 Python 프로그램입니다.

A Python program that collects multiple URLs, scans their robots.txt files, and outputs results in JSON format.

## Features

- ✅ **URL Collection**: Collect URLs from files or command-line arguments
- ✅ **URL Validation**: Validate and normalize URLs
- ✅ **Async Scanning**: Asynchronous robots.txt scanning for better performance
- ✅ **Concurrent Requests**: Configurable concurrent request limits
- ✅ **Robots.txt Parsing**: Parse and extract:
  - User agents
  - Disallowed paths
  - Allowed paths
  - Sitemap URLs
  - Crawl delays
- ✅ **JSON Export**: Export results in JSON format
- ✅ **Statistics**: Generate comprehensive scan statistics
- ✅ **Error Handling**: Robust error handling and recovery
- ✅ **Clean Code**: Well-documented, modular codebase

## Project Structure

```
.
├── main.py              # Main entry point with CLI interface
├── url_collector.py     # URL collection and validation module
├── robots_scanner.py    # Robots.txt scanning module
├── result_formatter.py  # Result formatting and JSON export module
├── sample_urls.txt      # Sample URLs file for testing
└── README.md            # This file
```

## Installation

```bash
# Install dependencies
uv add aiohttp

# Or using pip
pip install aiohttp
```

## Usage

### Command Line Interface

#### Scan a single URL

```bash
python main.py --url https://example.com
```

#### Scan multiple URLs

```bash
python main.py --url https://example.com https://test.com
```

#### Scan from file

```bash
python main.py --file urls.txt
```

#### Save results to file

```bash
python main.py --file urls.txt --output results.json
```

#### Configure concurrent requests and timeout

```bash
python main.py --file sample_urls.txt --concurrent 20 --timeout 15
```

### Programmatic Usage

```python
from url_collector import URLCollector
from robots_scanner import RobotsScanner
from result_formatter import ResultFormatter

# Collect URLs
collector = URLCollector()
collector.add_url("https://example.com")
collector.add_urls_from_file("urls.txt")
base_urls = collector.get_base_urls()  # Get base URLs for scanning

# Scan robots.txt (synchronous - recommended for scripts)
scanner = RobotsScanner(timeout=10, max_concurrent=10)
results = scanner.scan_urls_sync(base_urls)  # Use synchronous scanning

# Format and export results
formatter = ResultFormatter(results)
formatter.save_to_file("output.json")
```

## Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--url` | `-u` | URLs to scan (space-separated) | - |
| `--file` | `-f` | File containing URLs (one per line) | - |
| `--output` | `-o` | Output JSON file path | stdout |
| `--concurrent` | `-c` | Maximum concurrent requests | 10 |
| `--timeout` | `-t` | Request timeout in seconds | 10 |
| `--user-agent` | - | User agent string | RobotsScanner/1.0 |
| `--include-content` | - | Include raw robots.txt content | False |
| `--no-include-content` | - | Exclude raw robots.txt content | - |
| `--verbose` | `-v` | Enable verbose output | False |

## Output Format

The scanner outputs results in JSON format with the following structure:

```json
{
  "scan_metadata": {
    "timestamp": "2024-01-15T10:30:00",
    "total_urls": 5,
    "successful_scans": 4,
    "failed_scans": 1,
    "scan_duration_seconds": 2.5
  },
  "results": [
    {
      "url": "https://example.com",
      "robots_url": "https://example.com/robots.txt",
      "status_code": 200,
      "exists": true,
      "accessible": true,
      "user_agents": ["*"],
      "disallowed_paths": {
        "*": ["/admin", "/private"]
      },
      "allowed_paths": {
        "*": ["/public"]
      },
      "sitemaps": ["https://example.com/sitemap.xml"],
      "crawl_delay": {
        "*": 10
      },
      "scan_time": "2024-01-15T10:30:01",
      "response_time": 0.25
    }
  ],
  "statistics": {
    "total_urls_scanned": 5,
    "robots_txt_exists": 4,
    "robots_txt_missing": 1,
    "unique_user_agents": 8,
    "total_disallowed_paths": 15,
    "total_allowed_paths": 5,
    "total_sitemaps": 3
  }
}
```

## Module Documentation

### URLCollector

Collects and validates URLs from multiple sources.

```python
from url_collector import URLCollector

collector = URLCollector()
collector.add_url("https://example.com")
collector.add_urls_from_list(["https://test.com", "https://demo.com"])
collector.add_urls_from_file("urls.txt")
base_urls = collector.get_base_urls()  # Get base URLs (scheme + netloc)
all_urls = collector.get_all_urls()  # Get all URLs with full paths
```

### RobotsScanner

Scans robots.txt files asynchronously with synchronous wrapper support.

```python
from robots_scanner import RobotsScanner

scanner = RobotsScanner(
    timeout=10,
    max_concurrent=10,
    user_agent="MyBot/1.0"
)

# Synchronous scanning (recommended for scripts)
results = scanner.scan_urls_sync(urls)

# OR asynchronous scanning (for async applications)
# async def scan():
#     results = await scanner.scan_urls(urls)
#     return results
```

### ResultFormatter

Formats and exports scan results to JSON.

```python
from result_formatter import ResultFormatter

formatter = ResultFormatter(results)

# Export to file
formatter.save_to_file("output.json")

# Get JSON string
json_str = formatter.to_json()

# Get summary
summary = formatter.get_summary()
```

## Error Handling

The scanner includes comprehensive error handling:

- Invalid URLs are filtered out
- Network errors are caught and logged
- Timeouts are handled gracefully
- SSL certificate errors are handled
- Failed scans are included in results with error messages

## Performance

- Asynchronous scanning for better performance
- Configurable concurrent request limits
- Connection pooling
- Automatic retry logic (via aiohttp)

## Requirements

- Python 3.11+
- aiohttp

## License

MIT License

## Author

ChatDev - Changing the digital world through programming
