"""PostToolUse hook: run pytest and ruff after every file edit (CLAUDE.md rule f).

Reports the results back to Claude as additional context and shows a one-line
summary to the user. It never blocks the edit: red tests are reported, not enforced.
"""

import json
import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[2]
MAX_OUTPUT_CHARS = 3000


def run(args: list[str]) -> tuple[int, str]:
    result = subprocess.run(
        [sys.executable, "-m", *args],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    output = (result.stdout + result.stderr).strip()
    if len(output) > MAX_OUTPUT_CHARS:
        output = "...\n" + output[-MAX_OUTPUT_CHARS:]
    return result.returncode, output


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        payload = {}
    edited = payload.get("tool_input", {}).get("file_path", "?")

    pytest_code, pytest_out = run(
        ["pytest", "-q", "--no-header", "--tb=line", "-p", "no:cacheprovider"]
    )
    ruff_code, ruff_out = run(["ruff", "check", "."])

    pytest_status = "PASS" if pytest_code == 0 else "FAIL"
    ruff_status = "PASS" if ruff_code == 0 else "FAIL"
    pytest_summary = pytest_out.splitlines()[-1] if pytest_out else ""

    context = (
        f"[post-edit checks] after editing {edited}\n"
        f"pytest: {pytest_status} (exit {pytest_code})\n{pytest_out}\n\n"
        f"ruff check: {ruff_status} (exit {ruff_code})\n{ruff_out}"
    )
    print(
        json.dumps(
            {
                "systemMessage": f"pytest {pytest_status}: {pytest_summary} | ruff {ruff_status}",
                "hookSpecificOutput": {
                    "hookEventName": "PostToolUse",
                    "additionalContext": context,
                },
            }
        )
    )


if __name__ == "__main__":
    main()
