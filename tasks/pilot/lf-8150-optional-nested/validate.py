#!/usr/bin/env python3
"""Validator for lf-8150: fix present() for optional argument in nested subroutine.

The test file is injected from the fixed commit since it was added by the PR.
Acceptance: lfortran compiles and runs the test without errors.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

TEST_FILE = "integration_tests/intrinsics_392.f90"
INJECTED_TEST = """\
module bspline_sub_module
    contains
    subroutine check_inputs(nx)
        implicit none
        integer(4),intent(in),optional :: nx
        call check(nx)
        contains
            subroutine check(n)
                implicit none
                integer(4),intent(in),optional :: n
                print *, present(n)
            end subroutine check
    end subroutine check_inputs
end module bspline_sub_module

program intrinsics_392
    use bspline_sub_module
    implicit none
    integer(4) :: nx
    call check_inputs(nx)
end program intrinsics_392
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

    print("PASS: intrinsics_392 compiled and ran successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
