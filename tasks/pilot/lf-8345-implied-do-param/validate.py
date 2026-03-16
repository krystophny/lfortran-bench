#!/usr/bin/env python3
"""Validator for lf-8345: fix implied do loop in parameter array initialization.

The test file is injected from the fixed commit since it was added by the PR.
Acceptance: lfortran compiles and runs the test without errors.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

TEST_FILE = "integration_tests/implied_do_loops11.f90"
INJECTED_TEST = """\
program implied_do_loops11
    implicit none
    integer i
    integer, parameter:: nmax = 5, a(nmax) = [1,2,4,8,8], &
        b(nmax-1) = [ ( a(i)-a(i-1), i=2,nmax ) ]
    integer:: c(nmax-1) =  [ ( a(i)-a(i-1), i=2,nmax ) ]
    print "(A,5(1X,I0))", 'a =' ,a
    if (any(a /= [1,2,4,8,8])) error stop
    print "(A,4(1X,I0))", 'b = ',b
    if (any(b /= [1,2,4,0])) error stop
    print "(A,4(1X,I0))", 'c = ',c
    if (any(c /= [1,2,4,0])) error stop
    print "(A,4(1X,I0))", '? = ', ( a(i)-a(i-1), i=2,nmax )
    if (any([ (a(i)-a(i-1), i=2,nmax) ] /= [1,2,4,0])) error stop
end program implied_do_loops11
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

    print("PASS: implied_do_loops11 compiled and ran successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
