#!/usr/bin/env python3
"""Validator for lf-8373: fix select type with pointer association.

The test file is injected from the fixed commit since it was added by the PR.
Acceptance: lfortran compiles and runs the test without errors.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

TEST_FILE = "integration_tests/select_type_11.f90"
INJECTED_TEST = """\
program select_type_11
    implicit none
    integer, save :: arr(3) = [1, 2, 3]

    print *, "Before:", arr
    call update_any(arr)
    print *, "After: ", arr
    if(arr(1) /= 10) then
        print *, "Test failed: arr(1) should be 10, but is ", arr(1)
    else
        print *, "Test passed: arr(1) is ", arr(1)
    end if
contains

    subroutine update_any(generic)
        class(*) :: generic(:)
    integer, pointer :: xx(:)

        select type(generic)
        type is (integer)
            xx => generic
            xx(1) = 10
        end select
    end subroutine update_any

end program select_type_11
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

    print("PASS: select_type_11 compiled and ran successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
