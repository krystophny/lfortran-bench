#!/usr/bin/env python3
"""Validator for lf-8481: fix complex array member access (%re, %im).

The test file is injected from the fixed commit since it was added by the PR.
Acceptance: lfortran compiles and runs the test without errors.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

TEST_FILE = "integration_tests/complex_array_member_access.f90"
INJECTED_TEST = """\
program test
    complex, parameter :: x(2) = (1.0, 0.3)
    real :: y_re(2), y_im(2)

    ! Test extracting real parts
    y_re = x%re
    print *, "Real parts:", y_re

    ! Test extracting imaginary parts
    y_im = x%im
    print *, "Imaginary parts:", y_im

    ! Assert checks
    if (abs(y_re(1) - 1.0) > 1e-5) error stop "Real part 1 failed"
    if (abs(y_re(2) - 1.0) > 1e-5) error stop "Real part 2 failed"
    if (abs(y_im(1) - 0.3) > 1e-5) error stop "Imaginary part 1 failed"
    if (abs(y_im(2) - 0.3) > 1e-5) error stop "Imaginary part 2 failed"

    print *, x%re, x%im
    print *, "All tests passed!"
end
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

    print("PASS: complex_array_member_access compiled and ran successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
