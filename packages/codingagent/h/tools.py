"""
코딩 에이전트가 사용하는 도구들
- 파일 읽기/쓰기
- 디렉토리 목록 조회
- 터미널 명령 실행
- 파일 검색
"""

import os
import subprocess
from pathlib import Path
from typing import Optional

from langchain_core.tools import tool


@tool
def read_file(file_path: str) -> str:
    """파일의 내용을 읽어서 반환한다.

    Args:
        file_path: 읽을 파일의 경로 (상대 경로 또는 절대 경로)

    Returns:
        파일 내용 (라인 번호 포함)
    """
    try:
        path = Path(file_path).expanduser().resolve()
        if not path.exists():
            return f"Error: 파일이 존재하지 않음 - {file_path}"
        if not path.is_file():
            return f"Error: 파일이 아님 - {file_path}"

        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # 라인 번호 추가
        numbered_lines = []
        for i, line in enumerate(lines, 1):
            numbered_lines.append(f"{i:4}| {line.rstrip()}")

        return "\n".join(numbered_lines)
    except Exception as e:
        return f"Error: 파일 읽기 실패 - {e}"


@tool
def write_file(file_path: str, content: str) -> str:
    """파일에 내용을 쓴다. 파일이 존재하지 않으면 생성하고, 존재하면 덮어쓴다.

    Args:
        file_path: 쓸 파일의 경로
        content: 파일에 쓸 내용

    Returns:
        성공/실패 메시지
    """
    try:
        path = Path(file_path).expanduser().resolve()
        # 디렉토리가 없으면 생성
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        return f"Success: 파일 작성 완료 - {path}"
    except Exception as e:
        return f"Error: 파일 쓰기 실패 - {e}"


@tool
def edit_file(file_path: str, old_string: str, new_string: str) -> str:
    """파일에서 특정 문자열을 찾아 다른 문자열로 교체한다.

    Args:
        file_path: 수정할 파일의 경로
        old_string: 찾을 문자열 (정확히 일치해야 함)
        new_string: 교체할 문자열

    Returns:
        성공/실패 메시지
    """
    try:
        path = Path(file_path).expanduser().resolve()
        if not path.exists():
            return f"Error: 파일이 존재하지 않음 - {file_path}"

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        if old_string not in content:
            return f"Error: 찾을 문자열이 파일에 없음"

        # 몇 번 나타나는지 확인
        count = content.count(old_string)
        if count > 1:
            return f"Error: 찾을 문자열이 {count}번 나타남. 더 구체적인 문자열을 사용해야 함"

        new_content = content.replace(old_string, new_string)

        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)

        return f"Success: 파일 수정 완료 - {path}"
    except Exception as e:
        return f"Error: 파일 수정 실패 - {e}"


@tool
def list_directory(directory_path: str = ".") -> str:
    """디렉토리의 파일과 하위 디렉토리 목록을 반환한다.

    Args:
        directory_path: 조회할 디렉토리 경로 (기본값: 현재 디렉토리)

    Returns:
        파일 및 디렉토리 목록
    """
    try:
        path = Path(directory_path).expanduser().resolve()
        if not path.exists():
            return f"Error: 디렉토리가 존재하지 않음 - {directory_path}"
        if not path.is_dir():
            return f"Error: 디렉토리가 아님 - {directory_path}"

        items = []
        for item in sorted(path.iterdir()):
            if item.name.startswith("."):
                continue  # 숨김 파일 제외
            if item.is_dir():
                items.append(f"📁 {item.name}/")
            else:
                size = item.stat().st_size
                items.append(f"📄 {item.name} ({size:,} bytes)")

        if not items:
            return "디렉토리가 비어있음"

        return f"📂 {path}\n" + "\n".join(items)
    except Exception as e:
        return f"Error: 디렉토리 조회 실패 - {e}"


@tool
def run_command(command: str, cwd: Optional[str] = None) -> str:
    """터미널 명령을 실행하고 결과를 반환한다.

    Args:
        command: 실행할 명령어
        cwd: 명령을 실행할 디렉토리 (기본값: 현재 디렉토리)

    Returns:
        명령 실행 결과 (stdout + stderr)
    """
    try:
        working_dir = Path(cwd).expanduser().resolve() if cwd else Path.cwd()

        result = subprocess.run(
            command,
            shell=True,
            cwd=working_dir,
            capture_output=True,
            text=True,
            timeout=60,  # 60초 타임아웃
        )

        output_parts = []
        if result.stdout:
            output_parts.append(f"[stdout]\n{result.stdout}")
        if result.stderr:
            output_parts.append(f"[stderr]\n{result.stderr}")

        output = "\n".join(output_parts) if output_parts else "(출력 없음)"

        return f"Exit code: {result.returncode}\n{output}"
    except subprocess.TimeoutExpired:
        return "Error: 명령 실행 시간 초과 (60초)"
    except Exception as e:
        return f"Error: 명령 실행 실패 - {e}"


@tool
def search_files(pattern: str, directory: str = ".", file_extension: Optional[str] = None) -> str:
    """디렉토리에서 파일 이름 패턴으로 파일을 검색한다.

    Args:
        pattern: 검색할 파일 이름 패턴 (대소문자 구분 안 함)
        directory: 검색할 디렉토리 (기본값: 현재 디렉토리)
        file_extension: 파일 확장자 필터 (예: ".py", ".ts")

    Returns:
        검색된 파일 경로 목록
    """
    try:
        base_path = Path(directory).expanduser().resolve()
        if not base_path.exists():
            return f"Error: 디렉토리가 존재하지 않음 - {directory}"

        matches = []
        pattern_lower = pattern.lower()

        for path in base_path.rglob("*"):
            if path.is_file():
                # 숨김 파일/디렉토리 제외
                if any(part.startswith(".") for part in path.parts):
                    continue

                # 확장자 필터
                if file_extension and path.suffix.lower() != file_extension.lower():
                    continue

                # 패턴 매칭
                if pattern_lower in path.name.lower():
                    matches.append(str(path.relative_to(base_path)))

        if not matches:
            return "검색 결과 없음"

        return f"검색 결과 ({len(matches)}개):\n" + "\n".join(sorted(matches)[:50])
    except Exception as e:
        return f"Error: 파일 검색 실패 - {e}"


@tool
def grep_search(pattern: str, directory: str = ".", file_extension: Optional[str] = None) -> str:
    """파일 내용에서 정규식 패턴을 검색한다.

    Args:
        pattern: 검색할 정규식 패턴
        directory: 검색할 디렉토리 (기본값: 현재 디렉토리)
        file_extension: 파일 확장자 필터 (예: ".py", ".ts")

    Returns:
        매칭된 파일과 라인 목록
    """
    try:
        base_path = Path(directory).expanduser().resolve()

        # ripgrep 사용 시도, 없으면 grep 사용
        rg_available = subprocess.run(
            ["which", "rg"], capture_output=True
        ).returncode == 0

        if rg_available:
            cmd = ["rg", "--line-number", "--no-heading", pattern]
            if file_extension:
                cmd.extend(["--glob", f"*{file_extension}"])
            cmd.append(str(base_path))
        else:
            ext_filter = f"--include=*{file_extension}" if file_extension else ""
            cmd = f'grep -rn {ext_filter} "{pattern}" {base_path}'

        result = subprocess.run(
            cmd if isinstance(cmd, str) else cmd,
            shell=isinstance(cmd, str),
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.stdout:
            lines = result.stdout.strip().split("\n")[:30]  # 최대 30개
            return f"검색 결과:\n" + "\n".join(lines)
        else:
            return "검색 결과 없음"
    except subprocess.TimeoutExpired:
        return "Error: 검색 시간 초과"
    except Exception as e:
        return f"Error: 검색 실패 - {e}"


# 모든 도구 목록
ALL_TOOLS = [
    read_file,
    write_file,
    edit_file,
    list_directory,
    run_command,
    search_files,
    grep_search,
]
