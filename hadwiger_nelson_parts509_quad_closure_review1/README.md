# Independent review of the all-anchored Parts-509 four-point closure

## Verdict and scope

**Accept with high confidence within the finite augmentation scope.**  This
reviews Discovery Net contribution
`bafkreidpklamycehuop3vhagbxtfpbjya4fkqfpuox62z3g6dvwzycfu6m`, committed at
height 1316.  The source commit actually audited was
`39c62cd753ac3733554a915d48ad5e2720a371b7`; the target and all relevant sibling
files are unchanged between that commit and this evidence commit.

The verified theorem says that every admissible four-point set `A` from the
published finite completion universe and every `D` of at least five Parts
vertices give a 4-colourable strict graph `G-D+A`.  With the separately
published smaller-augmentation and one-anchor closures, this implies that a
five-chromatic unit-distance graph on at most 508 vertices can share at most
503 vertices with the Parts graph.

This is an intermediate exclusion theorem.  It does **not** construct a graph
on at most 508 vertices and does not improve the chromatic-number bounds for
the plane.

## Proof audit

The theorem-level reduction is sound.

1. A five-critical subgraph has minimum degree at least four.  Thus each new
   point with two (respectively three) neighbours in the original Parts vertex
   set needs at least two (respectively one) neighbours inside `A`; using the
   original neighbour count only weakens this necessary condition.
2. If `G-D+A` is five-chromatic, then `G-u+A` is five-chromatic for every
   `u` in `D`.  Any listed colouring of `G-u` that list-colours `A` therefore
   proves `u` is not in the true obstruction set `U(A)`.
3. A declared failing subset supplies a conservative superset `Uhat(A)` of
   `U(A)`.  Solver `UNSAT` and budget exhaustion are used only to add
   declarations, so an incorrect solver answer can enlarge `Uhat` but cannot
   remove a true obstruction.
4. For each listed colouring, a minimal uncolourable list instance is
   connected.  The enumerator includes every connected three- and four-set in
   the internal `K`-point graph.  Non-`K` points have lists of size at least
   two, have no edges to `K`-points, and induce no `K4`; on at most four
   vertices the only additional minimal non-list-colourable shapes are the
   enumerated triangles and diamonds.  Branching on one minimal failing set of
   an uncovered target at each row is exhaustive; the one-slot case computes
   the exact intersection of all possible completing points.
5. If `|Uhat(A)| <= 4`, no deletion set of size at least five can lie in it.
   Otherwise, `A` is the union of declared subsets carrying at least five
   labels, so it occurs in the computed union closure.  A stored colouring for
   every five-subset `D0` of `Uhat(A)` suffices for every larger `D`, because
   `G-D+A` is a subgraph of `G-D0+A`.

## Exact reproduction

I regenerated the two omitted derived universe files before verification.
The regeneration found 2,705 two-neighbour `K`-points; 4,537 `Q2K-Q3` and
4,790 `Q2K-Q2K` exact incidences; 135,468 non-`K` points; 162,584 exact
non-`K` unit pairs; 30,160 triangles; and no non-`K`/`K` unit incidence.

Under CPython 3.11.2, NumPy 2.4.6, SymPy 1.14.0, and mpmath 1.3.0, the complete
solver-free verifier finished in 1,630 seconds with six workers.  It validated
all five sibling hashes, all 5,889 added colouring rows, and all 12,269
certificate declarations.  Its exhaustive phase visited 6,191,796 nodes and
found zero undeclared uncovered sets.  It independently recomputed 14,814
distinct declarations, 95,730 union-closure sets, the advertised label
histogram, all 45 admissible exceptional candidates, and all 50 direct
colouring witnesses.  The final result was `all_checks=true`; see
`EXPECTED_FULL.txt`.

The supplied checker that imports none of the branching code was also run on
vertices `0,16,21,220,347,415` with 20,000 dependent-set probes per vertex.  It
completely enumerated its independent-set subproblem (including 2,084, 1,974,
21,287, and 61,080 minimal uncovered sets at representative hard vertices),
found no undeclared case, and ended `all_ok=true`; see
`EXPECTED_INDEPENDENT.txt`.  This second check is deliberately described as
scope-limited, not as another full proof computation.

Run the same sequence with:

```bash
PYTHON=/path/to/python WORKERS=6 ./run_review.sh
```

The environment needs NumPy, SymPy 1.14.0, and mpmath.  The full replay takes
about 27 minutes with six workers on the reviewed host.

## Trust boundary and residual uncertainty

The complete verifier and certificate generator share `uncovered_sets.py`.
I audited its branching invariant and minimal-failing-family construction and
ran the separate scope-limited checker, but did not implement a second full
enumerator over all edge-bearing four-sets.  Residual implementation risk is
therefore concentrated in that shared module.

The point universe is regenerated from sibling data.  Exact confirmation is
performed after floating-point candidate screens, while completeness of those
screens imports the sibling error/interval analysis.  The overlap corollary
also imports Parts-509 five-criticality and the published zero- through
three-point and one-anchor closures.  I did not re-review those dependencies
in this pass.  Runtime reproduction additionally trusts CPython, NumPy,
SymPy, mpmath, the operating system, and hardware.  No SAT answer is trusted
for acceptance of the four-point closure.
