# Independent review of the UD9-3 complete equilateral-closure stop

**Verdict: accept as a strict complete-round, single-realization stop.**

The reviewed construction starts from one exact realization of Pegg's
9-point UD9-3 graph. At each round it adds both equilateral completions of
every unit edge, merges coincident points, and rebuilds the complete physical
unit-distance graph. An independent implementation reproduces the censuses:

| round | points | complete unit edges |
|---:|---:|---:|
| 0 | 9 | 15 |
| 1 | 24 | 45 |
| 2 | 50 | 108 |
| 3 | 91 | 209 |
| 4 | 140 | 333 |
| 5 | 196 | 486 |
| 6 | 267 | 677 |
| 7 | 346 | 891 |
| **8** | **432** | **1,134** |
| 9 | 533 | 1,415 |

Round 8 has chromatic number exactly four. Its embedded 9-point source has no
proper three-colouring and has 72 canonical proper four-colourings; the
target's literal 432-character word is proper on all 1,134 edges. Round 9 has
533 distinct physical points, so it exceeds the campaign's at-most-508 cap.

This accepts the conclusion that round 8 is the last **complete** closure
round under the cap and that this particular monolithic route does not yield
a five-chromatic record candidate. It is not an exclusion of selected-edge
closures, a partial ninth round, deletions, another UD9-3 realization, or any
other plane unit-distance construction.

## Independent checks

The review imports no target code. It reconstructs the source and closure in
the exact field Q(rho), where rho satisfies rho^2-rho+1=0. Its main
independence points are:

- dense 15-coefficient quadratic forms instead of the target's sparse
  polynomial representation;
- a row-weighted exact contraction bound instead of the target's coarser
  product norm;
- direct affine interval evaluation of all 234,874 pairs in rounds 8 and 9;
- canonical restricted-growth colour enumeration instead of DSATUR; and
- explicit closure-collision statistics at every round.

The exact contraction proof isolates one source root inside the stated
radius-10^-35 rational box. Symbolic norm identities prove all declared
directions unit. The all-pairs interval audit proves that every formal point
is physically distinct and that every undeclared pair is nonunit. The point
and edge stream hashes match the target.

Normal and optimized Python runs are byte-identical. The target producer also
regenerates its 2,699-byte certificate byte-for-byte with the pinned
mpmath/PySAT environment.

## Source integrity

The upstream Shibuya file was read at its pinned commit. Its UD9-3 function
constructs the same nine ordered points and delegates edge creation to an
all-pairs unit-distance test. Direct 100-digit evaluation matches the target's
ordered affine source within 1.1e-90 and gives exactly the same 15 unit pairs.
The exact review theorem is nevertheless self-contained and does not depend
on Shibuya's floating-point predicates.

## Reproduction

CPython 3.11 or later and only the standard library are needed for the
independent proof:

    cd hadwiger_nelson_ud93_equilateral_closure_stop_review1
    sha256sum -c SHA256SUMS
    python3 -B verify.py | diff -u EXPECTED.json -
    python3 -O -B verify.py | diff -u EXPECTED.json -
    python3 -B controls.py | diff -u VALIDATION.json -

The optional networked provenance check uses mpmath 1.3.0 (available in the
target producer environment):

    python3 -B source_check.py | diff -u SOURCE_EXPECTED.json -

The reviewed target is the sibling directory
hadwiger_nelson_ud93_equilateral_closure_stop at mathematical commit
9ac74f0c9858aa04d84a72e13f1b903f2dacb978.

The unrestricted comparison remains Jaan Parts's 509-point, 2,442-edge
five-chromatic plane unit-distance construction. This review produces no
five-chromatic graph and no record improvement.

Public source:
<https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_ud93_equilateral_closure_stop_review1>.

The trust boundary is the written contraction and closure arguments,
hash-pinned target bytes, this standard-library checker, CPython exact
integer/Fraction/JSON/SHA-256 operations, and ordinary hardware. Floating
point and SAT are used only for reproducible certificate production, not as
proof premises.
