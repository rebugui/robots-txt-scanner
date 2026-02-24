# Robots.txt Scanner - 사용자 매뉴얼

**다량의 URL을 수집하고 robots.txt를 스캔 후 JSON 형식으로 결과를 출력하는 Python 도구**

---

## 📋 목차

1. [소개](#소개)
2. [주요 기능](#주요-기능)
3. [시스템 요구사항](#시스템-요구사항)
4. [설치 가이드](#설치-가이드)
5. [빠른 시작](#빠른-시작)
6. [사용 방법](#사용-방법)
7. [명령줄 옵션](#명령줄-옵션)
8. [프로그래밍 API](#프로그래밍-api)
9. [출력 형식](#출력-형식)
10. [예제](#예제)
11. [문제 해결](#문제-해결)
12. [FAQ](#faq)

---

## 소개

**Robots.txt Scanner**는 웹사이트들의 robots.txt 파일을 자동으로 스캔하고 분석하는 Python 기반 도구입니다. 여러 URL을 한 번에 처리하고, 그 결과를 체계적인 JSON 형식으로 출력합니다.

### 특징

- ✅ **대량 처리**: 수십~수백 개의 URL을 동시에 스캔
- 🚀 **비동기 처리**: aiohttp 기반의 빠른 병렬 처리
- 📊 **JSON 출력**: 구조화된 JSON 형식으로 결과 저장
- 🛡️ **에러 처리**: 견고한 예외 처리 및 재시도 메커니즘
- 📝 **완전한 문서화**: 코드 주석 및 독스트링 포함
- 🔧 **유연한 설정**: 타임아웃, 동시성 등 다양한 옵션

---

## 주요 기능

### 1. URL 수집 (URLCollector)
- 파일에서 URL 읽기
- 리스트에서 URL 추가
- URL 유효성 검사
- 중복 URL 제거
- 자동으로 base URL 추출

### 2. Robots.txt 스캔 (RobotsScanner)
- 비동기 HTTP 요청
- robots.txt 존재 여부 확인
- 응답 시간 측정
- 재시도 메커니즘
- SSL/TLS 지원

### 3. 결과 파싱 (RobotsEntry)
- User-agent 식별
- Disallow/Allow 경로 추출
- Sitemap URL 수집
- Crawl-delay 파싱
- 원본 콘텐츠 보존

### 4. 결과 포맷팅 (ResultFormatter)
- JSON 형식으로 변환
- 통계 정보 생성
- 요약 보고서 작성
- 파일로 내보내기

### 5. 통계 생성
- 총 스캔 URL 수
- 성공/실패 비율
- 평균 응답 시간
- robots.txt 존재 비율

---

## 시스템 요구사항

### 필수 요구사항

- **Python**: 3.11 이상
- **운영체제**: Windows, macOS, Linux

### 의존성

- **aiohttp** >= 3.9.0 (비동기 HTTP 클라이언트)

---

## 설치 가이드

### 방법 1: 직접 실행 (권장)

```bash
# 1. 프로젝트 디렉토리로 이동
cd robots-txt-scanner

# 2. 가상 환경 생성 (선택 사항)
python -m venv venv

# 가상 환경 활성화
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. 의존성 설치
pip install -r requirements.txt
# 또는
pip install aiohttp>=3.9.0
```

### 방법 2: uv 사용 (빠른 설치)

```bash
# uv가 설치되어 있다면
uv venv
source .venv/bin/activate  # macOS/Linux
# 또는
.venv\Scripts\activate  # Windows

uv pip install aiohttp
```

### 설치 확인

```bash
# 버전 확인
python --version  # Python 3.11+ 필요

# 모듈 import 테스트
python -c "import aiohttp; print('aiohttp version:', aiohttp.__version__)"
```

---

## 빠른 시작

### 가장 간단한 사용법

```bash
# 단일 URL 스캔
python main.py --url https://www.google.com

# 결과를 파일로 저장
python main.py --url https://www.google.com --output result.json
```

### 여러 URL 스캔

```bash
# 여러 URL 직접 입력
python main.py --url https://google.com https://github.com https://python.org

# 파일에서 URL 읽기
python main.py --file sample_urls.txt --output scan_results.json
```

---

## 사용 방법

### 1. 명령줄 인터페이스 (CLI)

#### 기본 구문

```bash
python main.py [OPTIONS] (--url URL [URL...] | --file FILE)
```

#### 입력 소스 옵션 (필수, 둘 중 하나 선택)

- `--url, -u`: 하나 이상의 URL을 직접 지정
- `--file, -f`: URL이 포함된 파일 경로 지정

### 2. URL 파일 형식

URL 파일은 한 줄에 하나의 URL을 작성합니다:

```text
# 주석은 #으로 시작
https://www.google.com
https://www.github.com
https://www.python.org

# 빈 줄은 무시됨
https://www.stackoverflow.com
```

### 3. 출력 옵션

```bash
# 화면에 출력 (기본)
python main.py --url https://example.com

# 파일로 저장
python main.py --url https://example.com --output results.json

# JSON 예쁘게 출력 (기본값)
python main.py --url https://example.com --output results.json
```

### 4. 성능 튜닝

```bash
# 동시 요청 수 증가 (기본값: 10)
python main.py --file urls.txt --concurrent 20

# 타임아웃 설정 (기본값: 10초)
python main.py --file urls.txt --timeout 15

# 조합
python main.py --file urls.txt --concurrent 20 --timeout 15
```

### 5. 상세 출력

```bash
# 진행 과정 표시
python main.py --file urls.txt --verbose

# 요약 숨기기
python main.py --file urls.txt --quiet

# 원본 robots.txt 내용 포함
python main.py --file urls.txt --include-content
```

---

## 명령줄 옵션

### 필수 옵션 (둘 중 하나)

| 옵션 | 단축 | 설명 | 예제 |
|------|------|------|------|
| `--url URL [URL...]` | `-u` | 하나 이상의 URL 지정 | `--url https://example.com` |
| `--file FILE` | `-f` | URL 파일 경로 | `--file urls.txt` |

### 출력 옵션

| 옵션 | 단축 | 기본값 | 설명 |
|------|------|--------|------|
| `--output FILE` | `-o` | stdout | 출력 JSON 파일 경로 |
| `--quiet` | `-q` | False | 요약 출력 숨기기 |
| `--verbose` | `-v` | False | 상세 진행 과정 표시 |
| `--include-content` | - | False | 원본 robots.txt 내용 포함 |

### 스캔 옵션

| 옵션 | 단축 | 기본값 | 설명 |
|------|------|--------|------|
| `--concurrent NUM` | `-c` | 10 | 최대 동시 요청 수 |
| `--timeout SEC` | `-t` | 10 | 요청 타임아웃 (초) |
| `--user-agent AGENT` | - | RobotsScanner/1.0 | User-Agent 문자열 |

### 도움말

```bash
# 전체 도움말 보기
python main.py --help

# 버전 정보
python main.py --version
```

---

## 프로그래밍 API

Python 코드에서 직접 모듈을 사용할 수 있습니다.

### 기본 사용법

```python
from url_collector import URLCollector
from robots_scanner import RobotsScanner
from result_formatter import ResultFormatter
import asyncio

async def scan_websites():
    # 1. URL 수집
    collector = URLCollector()
    collector.add_urls_from_list([
        "https://www.google.com",
        "https://www.github.com"
    ])
    base_urls = collector.get_base_urls()
    
    # 2. robots.txt 스캔
    scanner = RobotsScanner(
        timeout=10,
        max_concurrent=10,
        user_agent="MyBot/1.0"
    )
    results = await scanner.scan_multiple(base_urls)
    
    # 3. 결과 포맷팅
    formatter = ResultFormatter(results)
    
    # JSON으로 저장
    formatter.save_to_file("output.json")
    
    # 또는 문자열로 얻기
    json_str = formatter.to_json_string()
    print(json_str)
    
    # 통계 얻기
    stats = formatter.get_statistics()
    print(f"성공: {stats['successful_scans']}/{stats['total_urls']}")

# 실행
asyncio.run(scan_websites())
```

### URLCollector 사용법

```python
from url_collector import URLCollector

collector = URLCollector()

# 리스트에서 추가
stats = collector.add_urls_from_list([
    "https://example.com",
    "https://test.com",
    "invalid-url"  # 자동으로 필터링됨
])
print(f"추가됨: {stats['added']}, 무효: {stats['invalid']}")

# 파일에서 추가
stats = collector.add_urls_from_file("urls.txt")
print(f"파일에서 {stats['added']}개 URL 추가")

# 수집된 URL 얻기
base_urls = collector.get_base_urls()
print(f"총 {len(base_urls)}개 URL")

# URL 유효성 검사
is_valid = collector.validate_url("https://example.com")  # True
```

### RobotsScanner 사용법

```python
from robots_scanner import RobotsScanner
import asyncio

async def scan_single():
    scanner = RobotsScanner(
        timeout=10,
        max_concurrent=10,
        user_agent="MyBot/1.0",
        retry_attempts=3
    )
    
    # 단일 URL 스캔
    result = await scanner.scan_single("https://example.com")
    
    print(f"Status: {result.status_code}")
    print(f"Exists: {result.exists}")
    print(f"Sitemaps: {result.sitemaps}")
    print(f"Response time: {result.response_time}s")

asyncio.run(scan_single())
```

### ResultFormatter 사용법

```python
from result_formatter import ResultFormatter

# 결과 리스트로 초기화
formatter = ResultFormatter(results)

# 통계 얻기
stats = formatter.get_statistics()
print(f"Total: {stats['total_urls']}")
print(f"Success rate: {stats['success_rate']:.1%}")
print(f"Avg response time: {stats['average_response_time']:.2f}s")

# JSON 문자열로 변환
json_output = formatter.to_json_string()
print(json_output)

# 파일로 저장
formatter.save_to_file("results.json")

# 요약 출력
formatter.print_summary()
```

---

## 출력 형식

### JSON 구조

```json
{
  "scan_metadata": {
    "scan_time": "2024-01-15T10:30:00",
    "total_urls": 5,
    "config": {
      "timeout": 10,
      "max_concurrent": 10,
      "user_agent": "RobotsScanner/1.0"
    }
  },
  "results": [
    {
      "url": "https://example.com",
      "robots_url": "https://example.com/robots.txt",
      "status_code": 200,
      "exists": true,
      "accessible": true,
      "sitemaps": [
        "https://example.com/sitemap.xml"
      ],
      "user_agents": ["*", "Googlebot"],
      "disallowed_paths": {
        "*": ["/admin/", "/private/"],
        "Googlebot": ["/secret/"]
      },
      "allowed_paths": {
        "*": ["/public/"]
      },
      "crawl_delay": {
        "*": 1.0
      },
      "response_time": 0.234,
      "scan_time": "2024-01-15T10:30:01",
      "error": null,
      "content": null
    }
  ],
  "statistics": {
    "total_urls": 5,
    "successful_scans": 4,
    "failed_scans": 1,
    "robots_exist": 3,
    "success_rate": 0.80,
    "average_response_time": 0.345,
    "urls_with_sitemaps": 2
  }
}
```

### 주요 필드 설명

#### scan_metadata
- `scan_time`: 스캔 시작 시간 (ISO 8601)
- `total_urls`: 스캔할 총 URL 수
- `config`: 스캔 설정 정보

#### results 배열
- `url`: 기본 URL
- `robots_url`: robots.txt 전체 URL
- `status_code`: HTTP 상태 코드
- `exists`: robots.txt 존재 여부 (200 상태)
- `accessible`: 접근 가능 여부
- `sitemaps`: 발견된 sitemap URL 목록
- `user_agents`: 정의된 User-agent 목록
- `disallowed_paths`: User-agent별 Disallow 경로
- `allowed_paths`: User-agent별 Allow 경로
- `crawl_delay`: User-agent별 크롤 지연 시간
- `response_time`: 응답 시간 (초)
- `error`: 에러 메시지 (없으면 null)
- `content`: 원본 robots.txt 내용 (옵션)

#### statistics
- `total_urls`: 총 URL 수
- `successful_scans`: 성공한 스캔 수
- `failed_scans`: 실패한 스캔 수
- `robots_exist`: robots.txt가 있는 사이트 수
- `success_rate`: 성공률 (0.0 ~ 1.0)
- `average_response_time`: 평균 응답 시간
- `urls_with_sitemaps`: sitemap이 있는 URL 수

---

## 예제

### 예제 1: 단일 URL 스캔

```bash
python main.py --url https://www.python.org
```

### 예제 2: 여러 URL 스캔 후 파일 저장

```bash
python main.py \
  --url https://google.com https://github.com https://stackoverflow.com \
  --output tech_sites.json
```

### 예제 3: 대량 스캔 with 성능 최적화

```bash
python main.py \
  --file large_url_list.txt \
  --output bulk_results.json \
  --concurrent 30 \
  --timeout 15 \
  --verbose
```

### 예제 4: 원본 내용 포함 스캔

```bash
python main.py \
  --file urls.txt \
  --output with_content.json \
  --include-content
```

### 예제 5: 빠른 스캔 (요약만)

```bash
python main.py \
  --file urls.txt \
  --output quick_scan.json \
  --quiet \
  --concurrent 50 \
  --timeout 5
```

### 예제 6: 한국 웹사이트 스캔

```bash
python main.py \
  --url https://naver.com https://daum.net https://kakao.com \
  --output korean_sites.json \
  --verbose
```

### 예제 7: 프로그래밍 방식 사용

```python
#!/usr/bin/env python3
"""커스텀 스캔 스크립트"""

import asyncio
from url_collector import URLCollector
from robots_scanner import RobotsScanner
from result_formatter import ResultFormatter

async def main():
    # URL 수집
    collector = URLCollector()
    collector.add_urls_from_list([
        "https://example.com",
        "https://test.com"
    ])
    
    # 스캔
    scanner = RobotsScanner(timeout=5, max_concurrent=5)
    results = await scanner.scan_multiple(collector.get_base_urls())
    
    # 결과 필터링
    sites_with_sitemaps = [
        r for r in results 
        if r.exists and len(r.sitemaps) > 0
    ]
    
    print(f"Sitemap이 있는 사이트: {len(sites_with_sitemaps)}개")
    
    # 저장
    formatter = ResultFormatter(results)
    formatter.save_to_file("filtered_results.json")

asyncio.run(main())
```

### 예제 8: 에러 처리 예제

```python
import asyncio
from robots_scanner import RobotsScanner

async def scan_with_retry():
    scanner = RobotsScanner(
        timeout=10,
        max_concurrent=10,
        retry_attempts=3,
        retry_delay=1.0
    )
    
    results = await scanner.scan_multiple([
        "https://valid-site.com",
        "https://invalid-site-12345.com",
        "https://timeout-site.com"
    ])
    
    for result in results:
        if result.error:
            print(f"❌ {result.url}: {result.error}")
        else:
            print(f"✅ {result.url}: {result.status_code}")

asyncio.run(scan_with_retry())
```

---

## 문제 해결

### 일반적인 문제 및 해결 방법

#### 1. SSL 인증서 오류

**문제**: `SSLError: certificate verify failed`

**해결 방법**:
```python
# 코드에서 SSL 검증 비활성화 (개발 환경에서만)
import ssl
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
```

또는 프로그램이 자동으로 처리합니다.

#### 2. 연결 타임아웃

**문제**: `TimeoutError` 또는 `asyncio.TimeoutError`

**해결 방법**:
```bash
# 타임아웃 증가
python main.py --file urls.txt --timeout 20
```

#### 3. Too Many Requests (429)

**문제**: HTTP 429 상태 코드

**해결 방법**:
```bash
# 동시 요청 수 줄이기
python main.py --file urls.txt --concurrent 5
```

#### 4. 메모리 부족

**문제**: 대량의 URL로 인한 메모리 부족

**해결 방법**:
- URL 리스트를 여러 파일로 분할
- 동시 요청 수 줄이기
- 배치 처리 사용

#### 5. ImportError

**문제**: `ModuleNotFoundError: No module named 'aiohttp'`

**해결 방법**:
```bash
pip install aiohttp
# 또는
pip install -r requirements.txt
```

#### 6. URL이 유효하지 않음

**문제**: URL이 수집되지 않음

**해결 방법**:
- URL 형식 확인 (`http://` 또는 `https://` 필수)
- 파일 인코딩 확인 (UTF-8 권장)
- `--verbose` 옵션으로 상세 정보 확인

#### 7. 권한 오류

**문제**: 출력 파일에 쓸 수 없음

**해결 방법**:
```bash
# 다른 경로에 저장
python main.py --url https://example.com --output /tmp/results.json

# 또는 현재 디렉토리
python main.py --url https://example.com --output ./results.json
```

---

## FAQ

### Q1: 최대 몇 개의 URL까지 스캔할 수 있나요?

**A**: 이론적으로 제한이 없지만, 실제로는 시스템 리소스와 네트워크 대역폭에 따라 달라집니다. 1000개 이상의 URL을 스캔할 때는 `--concurrent` 값을 조정하고 배치 처리를 권장합니다.

### Q2: robots.txt가 없는 사이트는 어떻게 처리되나요?

**A**: HTTP 404 상태 코드로 기록되며, `exists: false`로 표시됩니다. 이는 에러가 아니라 정상적인 결과입니다.

### Q3: 결과 파일의 인코딩은 무엇인가요?

**A**: 모든 출력 파일은 UTF-8 인코딩으로 저장됩니다.

### Q4: 재시도 메커니즘은 어떻게 작동하나요?

**A**: 기본적으로 3번 재시도하며, 각 재시도 사이에 1초 대기합니다. 이는 `ScannerConfig`에서 조정할 수 있습니다.

### Q5: 특정 User-agent만 스캔할 수 있나요?

**A**: 아니요, 스캐너는 모든 User-agent 정보를 수집합니다. 결과에서 특정 User-agent만 필터링하려면 후처리가 필요합니다.

### Q6: HTTPS만 지원하나요?

**A**: HTTP와 HTTPS 모두 지원합니다. URL에 프로토콜을 명시하면 됩니다 (`http://` 또는 `https://`).

### Q7: 출력 JSON을 다른 형식(CSV 등)으로 변환할 수 있나요?

**A**: 현재는 JSON만 지원합니다. Python의 `pandas` 라이브러리를 사용하여 JSON을 CSV로 변환할 수 있습니다:

```python
import pandas as pd
import json

with open('results.json') as f:
    data = json.load(f)

df = pd.DataFrame(data['results'])
df.to_csv('results.csv', index=False)
```

---

## 추가 리소스

### 문서
- [README.md](README.md) - 프로젝트 개요
- [PROJECT_ARCHITECTURE.md](PROJECT_ARCHITECTURE.md) - 상세 아키텍처
- [CHANGELOG.md](CHANGELOG.md) - 변경 이력

### 참조
- [robots.txt 사양](https://www.robotstxt.org/robotstxt.html)
- [aiohttp 문서](https://docs.aiohttp.org/)
- [Python asyncio 문서](https://docs.python.org/3/library/asyncio.html)

### 예제 파일
- `example_usage.py` - 프로그래밍 방식 사용 예제
- `sample_urls.txt` - 샘플 URL 목록
- `example_output.json` - 출력 예제

---

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

---

## 연락처

문제 신고, 기능 요청, 기여는 프로젝트 저장소의 Issues를 이용해 주세요.

---

**최종 업데이트**: 2024년 1월  
**버전**: 1.0.0
