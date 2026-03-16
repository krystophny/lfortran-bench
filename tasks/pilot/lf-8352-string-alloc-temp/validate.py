#!/usr/bin/env python3
"""Validator for lf-8352: fix allocatable character array with runtime-length constructor.

The test file is injected from the fixed commit since it was added by the PR.
Acceptance: lfortran compiles and runs the test without errors.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

TEST_FILE = "integration_tests/string_69.f90"
INJECTED_TEST = """\
program string_69
  implicit none
  character(len=7) :: value
  character(len=:), allocatable :: keywords(:)
  integer :: ii
   ii = 7
  value = "version"
  keywords = [character(len=ii) :: value]
  if (len(keywords) /= 7) error stop
  if (keywords(1) /= "version") error stop
  value = "usage"
  keywords = [character(len=ii) :: keywords, value]
  if (keywords(2) /= "usage") error stop
end program
"""


def main() -> int:
    workspace = Path(sys.argv[1])
    lfortran = workspace / "build" / "src" / "bin" / "lfortran"
    test_path = workspace / TEST_FILE

    if not lfortran.exists():
        print(f"FAIL: lfortran binary not found at {lfortran}")
        return 1

    if not test_path.exists():
        test_path.parent.mkdir(parents=True, exist_ok=True)
        test_path.write_text(INJECTED_TEST)

    result = subprocess.run(
        ["conda", "run", "-n", "lf-llvm11", str(lfortran), str(test_path)],
        capture_output=True,
        text=True,
        timeout=60,
    )

    if result.returncode != 0:
        print(f"FAIL: lfortran exited with code {result.returncode}")
        if result.stderr:
            print(result.stderr[:500])
        return 1

    print("PASS: string_69 compiled and ran successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
