#!/usr/bin/env python3
"""Validator for lf-8490: fix elemental function returning derived type in array context.

The test file is injected from the fixed commit since it was added by the PR.
Acceptance: lfortran compiles and runs the test without errors.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

TEST_FILE = "integration_tests/submodule_13.f90"
INJECTED_TEST = """\
module submodule_13_mod
  implicit none

  private
  public :: string_t
  public :: operator(.separatedBy.)

  type string_t
    private
    character(len=:), allocatable :: string_
  contains
    procedure :: bracket
  end type string_t

  interface string_t
    elemental module function from_default_integer(i) result(string)
      implicit none
      integer, intent(in) :: i
      type(string_t) :: string
    end function from_default_integer
  end interface

  interface
    elemental module function bracket(self, opening, closing) result(bracketed_self)
      implicit none
      class(string_t), intent(in) :: self
      character(len=*), intent(in), optional :: opening, closing
      type(string_t) :: bracketed_self
    end function bracket
  end interface

  contains

    elemental module function bracket(self, opening, closing) result(bracketed_self)
      class(string_t), intent(in) :: self
      character(len=*), intent(in), optional :: opening, closing
      type(string_t) :: bracketed_self

      if (present(opening) .and. present(closing)) then
          bracketed_self%string_ = opening // self%string_ // closing
      else
          bracketed_self%string_ = self%string_
      end if
    end function bracket

end module submodule_13_mod


program submodule_13
  use submodule_13_mod, only : string_t
  implicit none

contains

  pure function markdown_table(row_header, column_header, body_cells, side_borders) result(lines)
    integer, parameter :: first_body_row = 3
    type(string_t), intent(in) :: row_header(first_body_row:), column_header(:), body_cells(first_body_row:,:)
    logical, intent(in) :: side_borders
    character(len=1), parameter :: column_separator = "|"
    integer, parameter :: num_rule_lines = 1
    type(string_t) :: lines(size(body_cells,1) + num_rule_lines)

    if (side_borders) lines = lines%bracket(column_separator)
  end function markdown_table

end program submodule_13
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

    print("PASS: submodule_13 compiled and ran successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
