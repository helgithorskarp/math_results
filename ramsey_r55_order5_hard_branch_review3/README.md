# Independent review of the hard order-five three-case reduction

Verdict: **accepted and independently verified**, conditional on the stated
hard-branch inputs and the earlier fixed-incidence theorem.  A hypothetical
hard-branch `(5,5;43)` graph with automorphism type `1^3 5^8` has red degree
profile

```text
20^6 21^32 22^5
```

and, after normalizing the mixed fixed triangle, falls into the three marked
incidence cases recorded in `MARKED_CASES.json`.

This is a necessary-condition reduction, not an order-five exclusion.  It
does not prove any marked case globally feasible, construct a 43-vertex
Ramsey graph, or address the low-deficiency branch.

Reviewed Discovery Net contribution:
`bafkreifhhnrj265pumlbwvuxy6coua4dqpdmfkg76g7iovgwpl4gyaki24`, source commit
`904481fabe87922b0a8b0e743674c4d0d452110e`.

## Mathematical audit

Normalize the three fixed vertices so `xy` is red, `xz,yz` are blue, and
their degrees are `(21,21,20)`.  Every moving orbit has five vertices.  The
hard-branch weight budget forces each moving degree into `20,21,22`; if `k`
moving cycles are noncentral, then

```text
W = 3+15k.
```

The allowed weight congruence, parity, and `W<=39` leave `k=0` or `2`.  For
`k=0`, the vertex identity at the degree-20 fixed vertex `z` gives
`t_R(z)+t_B(z)=200`.  Both local counts are multiples of five because the
mixed fixed triangle supplies no fixed pair inside either neighborhood.
Rounding the hard caps `(93,107)` down to `(90,105)` makes the sum at most
195, a contradiction.

Thus `k=2`, `W=33`, and the total excess above the hard local deficiencies is
five.  Divisibility at `z` already costs all five units, forcing

```text
(t_R(z),t_B(z))=(90,105),
```

and deficiency exactly seven in both colors at every other vertex.  The two
exceptional moving-cycle degree pairs `(20,20)`, `(20,22)`, `(22,22)` give
red/blue local-count sums `(4220,4375)`, `(4290,4305)`, `(4360,4235)`.
Triangle incidence makes each sum divisible by three, so only `(20,22)`
survives.  This yields 451 red edges and triangle totals `(1430,1435)`.

Writing `epsilon=d-21` and
`S(v)=sum_(w in N_R(v)) epsilon(w)`, the vertex identity gives `S(x)=S(y)=0`
and `S(z)=-5`.  Hence the exceptional low/high cycles `L,H` have equal
incidence at `x,y`, while `z-L` is red and `z-H` blue.  At a vertex of `L`,
the weighted sum is `k_LH-3`; exact local counts force zero, so `k_LH=3`.
The calculation at `H` gives the same value.  Every ordinary cycle `C_i`
satisfies

```text
k_iH-k_iL = c_z(i).
```

Applying these bit relations to the two inherited column multisets produces
four marked normal forms.  In the form `(h,column(L),column(H))=(1,7,3)`,
both cycles are red to `x,y`; any three red neighbors of an `L` vertex in
the red `C5` on `H` contain a red edge, completing a red `K5` with `x,y`.
The other three forms are exactly `(0,5,1)`, `(1,4,0)`, and `(1,5,1)`, with
the cycle indices recorded by the source handoff.

The row-sum, total-cross-degree, ordinary difference, and six fixed-cut
equations follow by literal edge incidence.  In particular, an intercycle
edge orbit has five edges, so the per-vertex cross degrees `k_ij` are symmetric
and lie between zero and five.  Re-deriving the fixed local counts gives cut
targets `(15-h,15-h,16,16,14,17)` in the stated order.

## Independent checks

[`independent_check.py`](independent_check.py) imports no target code.  It
counts degree assignments by multiplicity rather than iterating the target's
`3^8` product, reproducing the stages `6561 -> 129 -> 113`, the one one-defect
rejection, 56 triangle-divisibility rejections, and 56 labeled placements of
the unique surviving degree pair.

It directly enumerates the pair and triangle orbits, reconstructs the eight
labeled exceptional placements and their quotient under `x/y` exchange and
repeated-column permutations, and checks the excluded normal form.  For each
of the four marked forms, both internal `C5` steps, and all ten weight-three
cross words, it tests all 1,287 five-subsets of the 13-vertex induced graph.
Exactly 100 of the 160 assignments are locally Ramsey, with the word domains
matching `MARKED_CASES.json` exactly.

The checker also independently reconstructs every field of all three handoff
records.  As an additional consistency test not asserted by the source, it
supplies an explicit integer `k_ij` matrix satisfying the complete aggregate
row, difference, special-pair, total, and cut system for each marked case.
Their canonical SHA-256 is
`704afd0e7b41495eb856c0207c2b45104a7ced6505382c29c3bb4e3622186092`.
This proves that none of the three handoff cases disappears through an
immediate aggregate linear contradiction.

Those matrices are not graph witnesses.  Realizing each by simple circulant
cross words gives red/blue monochromatic-`K5` counts
`490/2065`, `1275/975`, and `1210/575`, respectively.  The explicit failure
counts guard against accidentally interpreting aggregate feasibility as the
Ramsey target.

The target checksum audit and both its normal and `-O` executions reproduce
the expected transcript and JSON byte-for-byte.

## Reproduction

From the repository root, using Python 3.11 or later and the standard library:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  ramsey_r55_order5_hard_branch_review3/independent_check.py \
  | cmp - ramsey_r55_order5_hard_branch_review3/EXPECTED_OUTPUT.txt
cd ramsey_r55_order5_hard_branch_review3
sha256sum -c SHA256SUMS
```

## Trust boundaries and uncertainty

The conclusion imports the exact local extrema, hard-branch weight/excess
identity, vertexwise neighborhood identity, and the two fixed-incidence
column patterns for the residual order-five action.  The latter theorem and
the one-defect localization have separate independent reviews, but this
checker does not reconstruct those upstream results from first principles.

The new bridge is rederived and its finite audit uses exact Python integer
arithmetic with no solver or external catalog.  It is not proof-assistant
formalized.  Most importantly, the three complete 43-vertex extensions remain
unsearched here; full monochromatic-five-set constraints, not these aggregate
equations, are the next unresolved boundary.
