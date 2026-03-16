#!/usr/bin/env python3
"""Validator for lf-8401: fix ASR verify condition for compile-time constant arrays.

The test file is injected from the fixed commit since it was added by the PR.
Acceptance: lfortran compiles and runs the test without errors.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

TEST_FILE = "integration_tests/arrays_constructor_01.f90"
# Test content from the fixed commit (PR #8401 adds implied-do array constructor test)
INJECTED_TEST = """\
program arrays_constructor_01
    implicit none
    character(5) :: str = "Hello"
    integer :: i = 1, ios, j
    type :: MyClass
        integer :: value
    end type MyClass
    type(MyClass) :: v1, v2, v3, arr(3)
    character(4), parameter :: arr1(1:2,1:2)=reshape(['a ', '1 ', 'b ', '2 '], [2,2])
    integer, parameter :: lpunc = 4

    character:: input(lpunc) = &
        [("2",i=1,lpunc)]

    print *, ["aaa", "aaa"]
    print *, [str(i+1:i+1), str(i:i)]
    print *, ["aaa", str(i+1:i+3), "aaa"]
    print *, [str(i+1:i+3), "aaa"]
    arr = [MyClass :: v1, v2, v3]
    print *, arr


    print*, arr1
    if (any(arr1 /= reshape(['a ', '1 ', 'b ', '2 '], [2,2]))) error stop

    print *, input
    if (any(input /= ['2', '2', '2', '2'])) error stop
end program arrays_constructor_01
"""


def main() -> int:
    workspace = Path(sys.argv[1])
    lfortran = workspace / "build" / "src" / "bin" / "lfortran"
    test_path = workspace / TEST_FILE

    if not lfortran.exists():
        print(f"FAIL: lfortran binary not found at {lfortran}")
        return 1

    # Inject test file if it doesn't exist (base commit doesn't have it)
    if not test_path.exists() or "lpunc" not in test_path.read_text():
        test_path.parent.mkdir(parents=True, exist_ok=True)
        test_path.write_text(INJECTED_TEST)

    # Compile and run
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

    print("PASS: arrays_constructor_01 compiled and ran successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
