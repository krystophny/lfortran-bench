#!/usr/bin/env python3
"""Validator for lf-8409: fix select type with allocatable class member.

The test file is injected from the fixed commit since it was added by the PR.
Acceptance: lfortran compiles and runs the test without errors.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

TEST_FILE = "integration_tests/select_type_12.f90"
INJECTED_TEST = """\
module container_mod
    type, abstract :: base
    end type base
    type, extends(base) :: child
        integer :: x = 42
    end type child
    type :: container
        class(base), allocatable :: val
    end type container
end module container_mod

program select_type_12
    use container_mod
    type(container) :: c
    type(child) :: ch
    integer :: t
    class(container), allocatable :: self
    allocate(self)
    allocate(child::self%val)
    select type(val => self%val)
    type is(child)
        print *, "child%x =", val%x
        t=val%x
    end select
    if(t /= 42) then
        print *, "Error: t should be 42, but is", t
    else
        print *, "Success: t is", t
    end if
end program select_type_12
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

    print("PASS: select_type_12 compiled and ran successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
