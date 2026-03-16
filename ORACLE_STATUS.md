# Oracle Verification Status

Verified: 13/20

## PASS (13 tasks ready)
- lf-5987-implicit-dealloc-exit
- lf-7100-classtype-polymorphic
- lf-7900-externalsym-binop
- lf-8150-optional-nested
- lf-8345-implied-do-param
- lf-8352-string-alloc-temp
- lf-8401-array-constructor-verify
- lf-8405-reshape-cast
- lf-8409-select-type-member
- lf-8412-string-nullify
- lf-8431-array-reshape
- lf-8481-complex-array-member
- lf-8490-elemental-array-derived

## FAIL - base passes (4 tasks, need replacement)
- lf-8200-struct-implied-do (exists pattern - test works without fix)
- lf-8373-select-type-associate (exists pattern)
- lf-8390-nested-struct-global (exists pattern)
- lf-8504-complex-implicit-cast (inject but base already handles it)

## FAIL - fixed fails validation (3 tasks, validator bug)
- lf-8100-allocatable-print (embedded test content likely wrong)
- lf-8421-string-bindc (needs C file too, validator incomplete)
- lf-8437-struct-alloc-assign (embedded test content likely wrong)
