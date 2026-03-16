#!/usr/bin/env python3
"""Validator for lf-7900: fix size() on array of derived type from external module.

The test file is injected from the fixed commit since it was added by the PR.
Acceptance: lfortran compiles and runs the test without errors.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

TEST_FILE = "integration_tests/arrays_13_size.f90"
INJECTED_TEST = """\
module stdlib_sorting_arrays_13_size

    implicit none

    integer, parameter :: max_merge_stack = 93

    type run_type
        integer(8) :: base = 0
        integer(8) :: len = 0
    end type run_type

end module stdlib_sorting_arrays_13_size


module stdlib_sorting_sort_index_arrays_13_size

    use stdlib_sorting_arrays_13_size
    implicit none

contains


    module subroutine sort_index( item )
        real, intent(inout) :: item
        type(run_type) :: runs(0:max_merge_stack-1)
        print *, size(runs)
        if (size(runs) /= 93) error stop
    end subroutine sort_index

end module stdlib_sorting_sort_index_arrays_13_size

program arrays_13_size
    use stdlib_sorting_sort_index_arrays_13_size
    implicit none

    real :: item
    call sort_index(item)
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

    print("PASS: arrays_13_size compiled and ran successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
