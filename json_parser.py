"""
JSON 파서 모듈
JSON 문자열 파싱, 유효성 검사, 예쁜 출력을 제공합니다.
"""

import json
from typing import Any, Dict, List, Union


def parse_json(text: str) -> Union[Dict, List, None]:
    """JSON 문자열을 파이썬 객체로 변환합니다.
    
    Args:
        text: JSON 형식의 문자열
        
    Returns:
        파싱된 파이썬 객체 (dict 또는 list)
        
    Raises:
        ValueError: JSON 파싱 실패 시
    """
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON 파싱 실패: {e}")


def validate_json(text: str) -> bool:
    """JSON 문자열의 유효성을 검사합니다.
    
    Args:
        text: 검사할 JSON 문자열
        
    Returns:
        True: 유효한 JSON
        False: 유효하지 않은 JSON
    """
    try:
        json.loads(text)
        return True
    except (json.JSONDecodeError, TypeError):
        return False


def pretty_print(data: Any, indent: int = 2) -> str:
    """파이썬 객체를 예쁜 JSON 문자열로 변환합니다.
    
    Args:
        data: 파이썬 객체 (dict, list 등)
        indent: 들여쓰기 공백 수 (기본값: 2)
        
    Returns:
        예쁘게 포맷팅된 JSON 문자열
        
    Raises:
        TypeError: JSON으로 변환할 수 없는 타입인 경우
    """
    try:
        return json.dumps(data, indent=indent, ensure_ascii=False, sort_keys=True)
    except (TypeError, ValueError) as e:
        raise TypeError(f"JSON 변환 실패: {e}")


if __name__ == "__main__":
    # 테스트 코드
    print("=" * 50)
    print("JSON 파서 모듈 테스트")
    print("=" * 50)
    
    # 테스트 데이터
    test_json_valid = '{"name": "베타", "age": 25, "skills": ["Python", "AI"]}'
    test_json_invalid = '{"name": "베타", "age": 25, "skills": ["Python", "AI"'
    
    # 1. parse_json 테스트
    print("\n1. parse_json() 테스트:")
    try:
        parsed = parse_json(test_json_valid)
        print(f"   ✓ 파싱 성공: {parsed}")
    except ValueError as e:
        print(f"   ✗ 파싱 실패: {e}")
    
    # 2. validate_json 테스트
    print("\n2. validate_json() 테스트:")
    print(f"   유효한 JSON: {validate_json(test_json_valid)}")
    print(f"   유효하지 않은 JSON: {validate_json(test_json_invalid)}")
    
    # 3. pretty_print 테스트
    print("\n3. pretty_print() 테스트:")
    test_data = {
        "name": "베타",
        "version": "1.0",
        "features": ["파싱", "검증", "출력"],
        "active": True
    }
    print(pretty_print(test_data))
