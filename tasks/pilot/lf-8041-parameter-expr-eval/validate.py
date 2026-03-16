#!/usr/bin/env python3
"""Validator for lf-8041: fix compile-time evaluation of parameter expressions.

The test file is injected from the fixed commit since it was added by the PR.
Acceptance: lfortran compiles and runs the test without errors.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

TEST_FILE = "integration_tests/intrinsics_391.f90"
INJECTED_TEST = """\
program intrinsics_391
    implicit none
    integer,parameter::  kr1 = selected_real_kind(1), maxkr = 3, &
        skr2 = selected_real_kind(precision(1.0_kr1)+1), &
        kr2  = merge(skr2,kr1, skr2>0),                &
        skr3 = selected_real_kind(precision(1.0_kr2)+1), &
        kr3  = merge(skr3,kr2, skr3>0),&
  ! kr3 = skr3 if that's a valid real kind, kr2 if not
        allkr(maxkr+1) = [kr1,kr2,kr3,kr3] ,&
        nkr = minloc(abs(allkr(1:maxkr)-allkr(2:maxkr+1)),1)
    integer :: result1(4), result2
    integer, parameter:: allkr1(4) = [-1,2,-3,4]
    integer, parameter :: nkr1(4) = abs(allkr1(1:4))
    integer,parameter:: nkr2 = sum(abs(allkr1(1:3)))
    print *, nkr1
    result1 = nkr1
    if (any(result1 /= [1, 2, 3, 4])) error stop
    print *, nkr2
    result2 = nkr2
    if (result2 /= 6) error stop
    print *, nkr
    call realkinds(nkr)
contains
    subroutine realkinds( nkr)
      integer,intent(in)::nkr
      integer :: n
      print "(A,I0)",'precision(1.0_kr1) = ',precision(1.0_kr1)
      if(nkr>=2) print "(A,I0)",'precision(1.0_kr2) = ',precision(1.0_kr2)
      if(nkr>=3) print "(A,I0)",'precision(1.0_kr3) = ',precision(1.0_kr3)
      write(*,"(A,I0,A)",advance='no') &
          'Number of different real kinds = ',nkr,', real kinds:'
      print "(*(1X,I0))",allkr(1:nkr)
      print "(3A)",'There ',merge('may be','are no',nkr>=maxkr),' more real kinds'
    end subroutine realkinds
end program intrinsics_391
"""


def main() -> int:
    workspace = Path(sys.argv[1])
    lfortran = workspace / "build" / "src" / "bin" / "lfortran"
    test_path = workspace / TEST_FILE

    if not lfortran.exists():
        print(f"FAIL: lfortran binary not found at {lfortran}")
        return 1

    if not test_path.exists() or "selected_real_kind" not in test_path.read_text():
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

    print("PASS: intrinsics_391 compiled and ran successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
