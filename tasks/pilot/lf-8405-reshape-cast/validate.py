#!/usr/bin/env python3
"""Validator for lf-8405: fix reshape with integer-to-real cast in initializer.

The test file is injected from the fixed commit since it was added by the PR.
Acceptance: lfortran compiles and runs the test without errors.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

TEST_FILE = "integration_tests/arrays_reshape_25.f90"
INJECTED_TEST = """\
program arrays_reshape_25
    implicit none
    real :: b(3, 2) = reshape([-1, -3, 6, 7, 8, 9], [3, 2])

    ! TODO: Enable these checks once runtime issues are resolved
    ! if (b(1,1) /= -1.0) error stop "Mismatch at b(1,1)"
    ! if (b(2,1) /= -3.0)  error stop "Mismatch at b(2,1)"
    ! if (b(3,1) /= 6.0)  error stop "Mismatch at b(3,1)"
    ! if (b(1,2) /= 7.0) error stop "Mismatch at b(1,2)"
    ! if (b(2,2) /= 8.0)  error stop "Mismatch at b(2,2)"
    ! if (b(3,2) /= 9.0)  error stop "Mismatch at b(3,2)"
end program arrays_reshape_25
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

    print("PASS: arrays_reshape_25 compiled and ran successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
