# 이 파일을 저장하면 자동으로 포매팅됩니다!

import os
import sys
from typing import List, Dict, Optional
import json


def poorly_formatted_function(x, y, z):
    result = x + y + z
    return result


class BadlyFormattedClass:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def display_info(self):
        print(f"Name: {self.name}, Age: {self.age}")


# 긴 줄 테스트
very_long_string = "이것은 매우 매우 매우 매우 매우 매우 매우 매우 매우 매우 매우 매우 매우 매우 매우 긴 문자열입니다"

# 리스트 포매팅
my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

# 딕셔너리 포매팅
my_dict = {"key1": "value1", "key2": "value2", "key3": "value3", "key4": "value4"}

# 함수 호출
result = poorly_formatted_function(1, 2, 3)
print(result)

# 조건문
if result > 5:
    print("Greater than 5")
else:
    print("Less than or equal to 5")


# 저장하면 다음과 같이 변경됩니다:
# - import 정렬
# - 함수와 클래스 주변 공백 추가
# - 콤마 뒤 공백 추가
# - 긴 줄 자동 줄바꿈
# - 일관된 들여쓰기
