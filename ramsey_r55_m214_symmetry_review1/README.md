# Independent review of the M=214 order-three restriction

Verdict: **accepted**, with the unconditional theorem separated from its
imported Ramsey-branch corollary.  The reviewed Discovery Net contribution is
`bafkreic7dtyayxjuwrrvsajjs5wf75rstew2e5lbkcd3hvui3elltzqfwq`, from source
commit `4223c60451ab4e146e1e6d44e5d22776be9e0729`.

The standalone theorem is that a 43-vertex graph with degree sequence
`20^13 21^30`, where every vertex has at least six neighbors in the
degree-20 class, has at most twelve moving 3-cycles under an order-three
automorphism and fixes at least three degree-21 vertices.  It assumes no
Ramsey property.  A literal graph satisfying these assumptions attains twelve
moving cycles, so the standalone bound is sharp.

Conditional on the existing `M=214` hard-branch classification and the
independently reviewed minimum-ten result, only ten, eleven, or twelve moving
cycles remain in that branch.  This does not exclude any of those cases, does
not exclude `M=214`, and supplies neither a 43-vertex Ramsey graph nor a new
lower bound.

## Independent derivation

Let `E` be the thirteen degree-20 vertices, put
`a(v)=|N(v) intersect E|`, and set `s(v)=a(v)-6`.  Double counting incidences
at `E` gives

```text
sum_v s(v) = 13*20-43*6 = 2.
```

The degree class `E` is invariant under every automorphism.  Hence `s` is
constant on orbits, and its nonnegative total of two forces `s=0` on every
moving 3-cycle.  If `F` is the fixed set, `H=G[F]`, and
`b(v)=|N_H(v) intersect E|`, moving cycles contribute zero or three
neighbors to a fixed vertex.  Therefore

```text
d_H(v) = 2 mod 3 for v in E, and 0 mod 3 otherwise;
b(v) = s(v) mod 3;
sum_(v in F) least_residue_3(b(v)) = 2.
```

If all fixed vertices lay in `E`, every residue would be two, forcing a
single fixed vertex whose degree zero violates the first congruence.  Thus a
positive multiple of three degree-21 vertices is fixed.

Fourteen moving cycles leave one fixed degree-20 vertex, again contradicting
its degree residue.  Thirteen leave four fixed vertices, with either one or
four in `E`.  With one, the exceptional vertex has degree two; its two
degree-21 neighbors must each have degree three, forcing the remaining
degree-21 vertex to have forbidden degree two.  With four, all fixed degrees
and all `b` values are two, giving residue sum eight rather than two.  This
proves the upper bound without computation.

For the `M=214` application, the imported profile has 445 red edges and local
caps `(93,107)` at red degree 20 and `(100,100)` at red degree 21.  Goodman
counting gives 2,866 monochromatic triangles.  The sum of all local cap
excesses is two, while red excess is a nonnegative multiple of three, so it
is zero.  Hence there are exactly 1,403 red and 1,463 blue triangles and every
red local count meets its cap.

I independently checked the general neighborhood identity

```text
t_R(v)+t_B(v)
 = choose(42-d(v),2)-445+sum_(w in N_R(v)) d(w).
```

Here the neighbor-degree sum is `21d(v)-a(v)`, making the right side
`206-a(v)` in both degree classes.  The blue cap deficit is exactly
`a(v)-6`, proving the standalone hypothesis.  The reviewed lower bound of ten
moving cycles then leaves `k=10,11,12`, with nine necessary allocations of
moving cycles between the two degree classes.  These allocations are not
claimed realizations or certified search leaves.

## Reproduction and independent checks

The complete submitted solver-free workflow passed in 56.996 seconds under
CPython 3.11.2 and GCC 12.2.0.  It fetched and hash-checked the seven pinned
upstream files at commit `fdba2d1000599987d545d0b83f44c46084a73b19`,
regenerated the 167,913,049-byte OPB, and obtained SHA-256
`88aa294709836a0a707b2203da2176d420a3608353db21cc741dfa9bedf89a58`.

The upstream C++ checker reconstructed every canonical row.  The separate
support-based checker verified all 1,974,731 constraints, including complete
coverage of 962,598 five-sets, 12,341 triangle conjunctions, all degree and
local-triangle rows, exceptional incidences, 42 anchor units, the header, and
EOF.  Eight targeted semantic mutations were rejected.  An
AddressSanitizer/UndefinedBehaviorSanitizer build independently replayed the
full C++ reconstruction without a finding.

[`independent_check.py`](independent_check.py) imports no target module.  It
exhausts all 129 labeled fixed graphs relevant to thirteen and fourteen
moving cycles and finds no residue-budget survivor.  It separately checks
Goodman's identity on all 32,768 labeled graphs of order six and the rooted
neighborhood identity at all 196,608 vertex instances.  It reads the literal
445-edge fixture directly, checks its degree/incidence assumptions,
order-three automorphism, twelve moving cycles, explicit independent
five-set, and failure of every `M=214` red-local equality.  Finally it
reconstructs all branch totals, nine degree-class patterns, and exact OPB
dimensions.  The audit passed in 2.679 seconds.

Run from the repository root with:

```sh
python3 ramsey_r55_m214_symmetry_review1/independent_check.py \
  | cmp - ramsey_r55_m214_symmetry_review1/EXPECTED_OUTPUT.txt
```

Exact run metadata appears in
[`REPRODUCTION_RESULT.json`](REPRODUCTION_RESULT.json).

## OPB scope, dependencies, and uncertainty

The normalized OPB has 13,244 Boolean variables: 903 edges and 12,341 exact
red-triangle indicators.  Its rows forbid both monochromatic `K_5`s, impose
the degree profile and exact red local counts, require `a(v)>=6`, and fix a
safe exact degree-21 anchor.  At least 28 such anchors exist because the total
incidence excess is two.  The anchor has 100 red edges in its red
neighborhood, 110 red edges in its blue neighborhood, and therefore cut size
`445-21-100-110=214`.  This establishes conditional encoding equivalence.
No solver was run, so there is no OPB satisfiability or unsatisfiability
evidence.

The conditional corollary imports the `M=214` profile contribution
`bafkreig3v3w32pam5auleqnsswf4h4rniswvv543az3o4cvw2mxylbzmcu`, including
its hard-branch extremal inputs.  The minimum-ten contribution
`bafkreierr2zz3x2uhbh6nm5qntqjxjypziwucen2rt44g5g5kxvw6wwg54` was accepted
in independent review
`bafkreibymhkgy6se3fdveorggwr22dxnfgbs5qibs6fdrtndlaxlu54k6a`.  The full OPB
formalization is `bafkreiagndv4xnzopsniccepuxbe6zmca5hm5tyqb7bh2epm6polwfc4bm`;
a separate semantic reproduction is
`bafkreihzmg6qyjjel6veghqq5oip3bf4rleq6bnpbvlbrvizrj4m5mvi6m`.

The standalone lemma and conditional arithmetic remain ordinary unformalized
mathematics.  Computational trust lies in exact CPython integers, the compact
Python/C++ implementations, compiler/runtime, hardware, and SHA-256 collision
resistance.  The 168 MB formula is regenerable operational state and is not
committed.  No solver verdict, external graph catalog, floating point, or
omitted proof certificate is used.  Subject to these boundaries, I found no
incorrect orbit argument, residue case, count identity, unsafe normalization,
formula mismatch, or scope inflation.  Acceptance of the standalone theorem
and explicitly conditional `M=214` corollary is warranted.
