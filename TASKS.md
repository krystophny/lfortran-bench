# LFortran Bench Task Candidates

20 candidates from merged PRs before September 2025. All fix compiler bugs
in C++ code with clear test cases.

## Selected Tasks

### Semantics / Type System
1. **PR #8504** (7 files) - Fix implicit cast for complex numbers
2. **PR #8356** (4 files) - Fix proper logical operation for like datatypes
3. **PR #8373** (3 files) - Handle Associate for class(*) vars
4. **PR #7100** (3 files) - Implement ClassType to ClassType polymorphic arg conversion
5. **PR #8200** (2 files) - Get correct struct symbol from implied do loop

### Array Operations
6. **PR #8490** (3 files) - Fix calling elemental function on array of derived types
7. **PR #8481** (4 files) - Fix complex array member access (%re and %im)
8. **PR #8431** (4 files) - Handle some cases of array reshape
9. **PR #8405** (4 files) - Handle using reshape with casting
10. **PR #8401** (2 files) - Fix verify condition for compile-time constant arrays

### String / I/O
11. **PR #8421** (5 files) - Handle string array passed to BindC function call
12. **PR #8412** (3 files) - Handle string pointer in nullify()
13. **PR #8352** (5 files) - Create allocatable temporary if string len is runtime
14. **PR #8413** (6 files) - Support keyword arguments for get_command_argument

### Code Generation
15. **PR #8390** (4 files) - Handle nested structconstructor in declaring global vars
16. **PR #8345** (9 files) - Handle compile-time evaluation of implied-do loops for parameter arrays
17. **PR #7900** (3 files) - Correct ExternalSymbol condition for FunctionCall in IntegerBinOp

### Struct / Derived Types
18. **PR #8150** (3 files) - Handle optional args in nested subroutines
19. **PR #8100** (9 files) - Fix printing for allocatable scalars
20. **PR #5987** (3 files) - Insert implicit_deallocate before exit only in block constructs

## Implementation Notes

- Each task needs: base_commit (parent of merge), fixed_commit (merge commit)
- Setup: cmake configure + ninja build (incremental, ~2-3 min)
- Acceptance: run the specific integration test added by the PR
- Most PRs add a test in `integration_tests/` - use that as the validator
