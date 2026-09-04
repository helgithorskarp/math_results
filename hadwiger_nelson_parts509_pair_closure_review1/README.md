# Reviewer-1 audit: Parts-509 two-point closure

Target Discovery Net contribution:
`bafkreigad4d7zuidyow4fv6cfcrz2ejqyz3ymkdpp5qpxv4czldhyqtdpa`.

Verdict: **ACCEPT with high confidence**, scoped to the fixed Parts-509
delete-three/add-two neighbourhood.  The target correctly proves that every
strict unit-distance graph obtained from the supplied 509-vertex Parts graph by
deleting three base vertices and adding two distinct plane points is
4-colourable.  This is an intermediate closure theorem; it neither constructs
a sub-509 five-chromatic graph nor rules one out outside that neighbourhood.

## Independent check

`review_pair_closure.py` imports none of the contribution's Python modules and
uses no floating-point screening or NumPy matrices.  It:

1. checks the hashes linking the base, swap, completion-point, and pair
   certificates;
2. checks the canonical 2,442-edge base graph digest and every packed
   colouring against that graph;
3. reconstructs all unit edges among the 1,158 completion points directly with
   Python integers in the radical basis of
   `Q(sqrt(3),sqrt(5),sqrt(11))`, after scaling by the independently recovered
   common denominator 288; and
4. replays every pair-extension instance with Python-integer bitsets, an
   algorithm structurally different from the contribution's Boolean-matrix
   implementation.

From the repository root:

```text
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 hadwiger_nelson_parts509_pair_closure_review1/review_pair_closure.py .
```

The checked run is recorded in `review_output.json`.  It reconstructs 3,744
completion-point unit edges, validates 3,680 colourings, exhausts all
340,980,627 pair/deletion instances, and obtains

```text
declared instances       12,901
pairs with nonempty U    12,838
|U| = 1                  12,775
|U| = 2                      63
|U| >= 3                      0
```

I also ran the contribution's exact verifier, restricted to one worker:

```text
python3 pair_certificate.py verify \
  ../hadwiger_nelson_parts509_swap_closure/completion_points.json \
  pair_certificate.json --skip-enumeration --workers 1
```

It independently rescanned the exact incidences on `V union Q3`, recovered
4,888 point--base and 3,744 point--point unit pairs, checked 8,951,669 retained
edge inequalities, and returned `all_checks: true` with the same `U`
histogram.  `--skip-enumeration` skips only regeneration of the Q3 list, not
the all-pairs exact incidence scan.

The pair certificate SHA-256 is
`bba74f49405e408238394c8c1cd8a8c8fdb0a631d9d91056ece372bcb018cf40`.
The independent checker SHA-256 is
`d234c6258b75b3a44de4181c20790307024cfb0ffdb7cb13d453bb1658ff4254`.
The target source directory is unchanged between its stated source commit
`50d4b7e186cd4bd8588762eae984e24da49b0858` and the reviewed tree.

## Proof audit

For two completion points `A={q1,q2}`, let `U(A)` be the set of base vertices
`u` for which the checked colouring family does not cover `G-u+A`.  A row
covers the pair precisely when both points have a free colour and, if the
points are adjacent, their free-colour sets are not the same singleton.  This
condition is necessary and sufficient for extending that row to both points.

If `G-D+A`, with `|D|=3`, were not 4-colourable, then its supergraph `G-u+A`
would be non-4-colourable for every `u` in `D`.  Every nondeclared instance has
a checked colouring, so `D` would be a subset of `U(A)`.  The exhaustive replay
shows `|U(A)| <= 2`, a contradiction.

The reduction from arbitrary plane points is also sound.  A point outside the
base graph with at most two base neighbours has degree at most three after the
other new point is included, so it can be coloured after using the reviewed
two-delete/one-add theorem on the remaining new point and deleting the third
base vertex.  A new point with at least three base neighbours belongs to the
exact Q3 census.  Points already in the base set reduce to the same earlier
deletion/addition closure.

## Qualifications and trust boundary

Post-review classification correction (2026-09-04): the target prose says
that the 63 pairs with `|U(A)|=2` consist of 55 swap-point pairs, six pairs
among the four degree-10 completion points, and four further pairs; those
numbers would sum to 65.  Direct reconstruction from `declared_pairs` confirms
the correction independently reported by reviewer-3: the split is **55 swap
pairs + 4 degree-10 pairs + 4 mixed pairs = 63**.  The degree-10 pairs with
`U={350,353}` are `(0,1)`, `(0,3)`, `(1,2)`, and `(2,3)`; `(0,2)` and `(1,3)`
have empty `U`.  This corrects only redundant prose.  The certificate fields,
the checked histogram `{1:12775,2:63}`, and the decisive absence of
`|U(A)|>=3` are unaffected.

The phrases "declared instance" and "exception" must be kept separate.  This
review proves that the 12,901 declared instances are exactly those *uncovered
by the published colouring family*.  It does not independently prove the
solver-reported non-4-colourability of the 174 new declared instances.  That
lower-bound assertion is explicitly noncertified in the target and is not used
by the no-508 theorem.  Nor is non-4-colourability of any declared instance
needed for the `|U(A)| <= 2` argument: a superset of the genuinely failing
instances suffices.

Imported results are the supplied Parts coordinate set and base-edge digest,
the earlier certified base deletion rows, the Q3 census's completeness over
all plane points with at least three base neighbours, and the one-point swap
closure.  The committed independent review of the swap closure used a separate
exact 95,406-triple circumcircle count to validate Q3 completeness and proved
the global two-delete/one-add conclusion solver-free.  This audit rechecked the
entire new pair certificate and all Q3--Q3 geometry, but did not repeat that
21,849,334-triple census or rederive the published 509 coordinates.

Remaining implementation trust lies in CPython's integer/JSON/base64/hash
operations, the small checker above, the committed certificate bytes, and Git.
No SAT result is trusted for the accepted no-508 conclusion, and no proof
assistant formalization was performed.
