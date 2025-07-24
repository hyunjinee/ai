#!/usr/bin/env python3
"""
색상 테스트 파일 - VS Code에서 예쁘게 보이는지 확인하세요!
이 파일은 다양한 Python 구문 요소를 포함합니다.
"""

# 임포트 - 보통 파란색/보라색
import os
import sys
from typing import List, Dict, Optional, Union, Any
from dataclasses import dataclass
from enum import Enum

# 상수 - 보통 대문자로 표시
API_KEY = "sk-1234567890"
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30.0


# Enum - 클래스명은 청록색
class Status(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


# 데이터클래스 - 클래스명과 데코레이터 색상 확인
@dataclass
class User:
    name: str  # 타입 힌트는 다른 색상
    age: int
    email: Optional[str] = None
    tags: Optional[List[str]] = None


# 함수 정의 - 함수명은 노란색
def calculate_fibonacci(n: int) -> int:
    """피보나치 수열 계산 - 독스트링은 다른 색상"""
    if n <= 1:
        return n
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)


# 클래스 정의 - 클래스명은 청록색
class ColorfulExample:
    """다양한 색상 요소를 보여주는 예제 클래스"""

    def __init__(self, name: str, value: float = 0.0):
        self.name = name  # self는 특별한 색상
        self.value = value
        self._private = "private"  # 언더스코어 변수
        self.__double_private = "very private"

    @property  # 데코레이터는 특별한 색상
    def formatted_value(self) -> str:
        return f"Value: {self.value:.2f}"  # f-string 내부도 확인

    @staticmethod
    def static_method(x: int, y: int) -> int:
        """정적 메서드 - 데코레이터와 함수명 색상 확인"""
        return x + y

    async def async_method(self, url: str) -> Dict[str, Any]:
        """비동기 메서드 - async/await 키워드 색상"""
        import aiohttp  # 함수 내부 임포트

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()


# 전역 변수와 상수
global_counter = 0
CONFIG = {
    "debug": True,  # 불린값 색상
    "host": "localhost",  # 문자열 색상
    "port": 8080,  # 숫자 색상
    "features": ["auth", "api", "websocket"],  # 리스트
}


# 조건문과 반복문
def control_flow_example(items: List[str]) -> None:
    """제어문 키워드 색상 확인"""
    # if, elif, else 키워드
    if len(items) == 0:
        print("No items")
    elif len(items) == 1:
        print(f"One item: {items[0]}")
    else:
        print(f"Multiple items: {len(items)}")

    # for, in 키워드
    for i, item in enumerate(items):
        if item.startswith("test"):
            continue  # continue 키워드
        elif item == "stop":
            break  # break 키워드
        else:
            print(f"{i}: {item}")

    # while 키워드
    count = 0
    while count < 10:
        count += 1

    # try, except, finally 키워드
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        print(f"Error: {e}")
    finally:
        print("Cleanup")


# 람다와 컴프리헨션
square = lambda x: x**2  # lambda 키워드
numbers = [1, 2, 3, 4, 5]
squared = [x**2 for x in numbers]  # 리스트 컴프리헨션
even_squares = {x: x**2 for x in numbers if x % 2 == 0}  # 딕셔너리 컴프리헨션


# 특수 메서드와 연산자
class MagicMethods:
    def __str__(self) -> str:
        return "Magic!"

    def __repr__(self) -> str:
        return "MagicMethods()"

    def __add__(self, other):
        return "Added!"


# 주석 종류
# 일반 주석 - 보통 회색/녹색
# TODO: 할 일 주석 - 일부 테마에서 하이라이트
# FIXME: 수정 필요 - 일부 테마에서 하이라이트
# NOTE: 메모 - 일부 테마에서 하이라이트

# 메인 실행부
if __name__ == "__main__":
    # 다양한 리터럴 색상
    integer = 42
    floating = 3.14159
    binary = 0b1010
    octal = 0o755
    hexadecimal = 0xFF00

    # 문자열 종류
    single = "Single quotes"
    double = "Double quotes"
    triple_single = """Triple single"""
    triple_double = """Triple double"""
    raw_string = r"Raw string \n"
    byte_string = b"Byte string"

    # 불린과 None
    is_true = True
    is_false = False
    nothing = None

    print("�� 색상이 예쁘게 보이나요? 🎨")
