# Oracle Verification Status

Verified: 17/20

## PASS (17 tasks ready)
- lf-5987-implicit-dealloc-exit
- lf-6943-findloc-2d-array (new replacement)
- lf-7039-extended-type-assign (new replacement)
- lf-7100-classtype-polymorphic
- lf-7222-operator-overload-multi (new replacement)
- lf-7900-externalsym-binop
- lf-8150-optional-nested
- lf-8345-implied-do-param
- lf-8352-string-alloc-temp
- lf-8401-array-constructor-verify
- lf-8405-reshape-cast
- lf-8409-select-type-member
- lf-8412-string-nullify
- lf-8421-string-bindc (fixed: now handles C file)
- lf-8431-array-reshape
- lf-8481-complex-array-member
- lf-8490-elemental-array-derived

## FAIL (3 tasks need replacement or fix)
- lf-7399-move-alloc-dealloc (replacement - base passes, bad task choice)
- lf-8100-allocatable-print (validator bug - wrong embedded test content)
- lf-8437-struct-alloc-assign (validator bug - wrong embedded test content)
