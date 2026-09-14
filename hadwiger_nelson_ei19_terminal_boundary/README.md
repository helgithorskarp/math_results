# EI19: the complete ten-terminal four-colour relation is neutral

For the exact 19-point, 35-edge support defined here, every proper four-colouring
of its ten degree-three vertices extends to a proper four-colouring of the whole
support. There are **4,320 patterns modulo colour renaming**, of which 360 use
three colours and 3,960 use four. None is excluded beyond the bare terminal
edges. These correspond to **103,680 labelled terminal colourings**.

This closes the selected EI19 interface as a small physical forcing source.
Deleting internal vertices cannot produce an obstruction on these terminals:
restrict each of the positive full-support colourings. No copies, phases, or
larger hosts were generated after this neutral relation was established. No
sub-509 candidate, useful forcing core, or qualifying construction milestone
was obtained. This is a fixed-interface result, not a lower bound on arbitrary
unit-distance constructions or a classification of every EI19 interface.

## Exact support and terminals

The input [geometry_certificate.json](geometry_certificate.json) defines one
exact real support by polynomial equations and a rational isolating box. Fix
vertices 0 and 1 at `(0,0)` and `(1,0)`. The other 34 coordinates are the unique
solution in the box of radius `10^-25` about the 50-decimal rational midpoint
table, satisfying the 34 listed non-anchor squared-unit-edge equations. The
certificate contains an approximate inverse matrix with rational entries; all
verification arithmetic is exact integer/rational arithmetic.

[geometry.py](geometry.py) proves that this root exists, that all 19 points are
distinct, and that its complete physical unit graph has exactly the 35 listed
edges. It examines all 171 unordered pairs; the other 136 pairs are proved
nonunit. Approximate coordinates are not treated as exact coordinates.

The graph is the known triangle-free Exoo–Ismailescu EI19 graph. Vertex order is
`(A,B,p0,...,p16)` in the EI19 construction in
[Parcly Taxel's Shibuya source](https://github.com/Parcly-Taxel/Shibuya/blob/master/shibuya/graphs/pegg.py).
The exact-coordinate literature includes
[Silva Filho, arXiv:2607.19995v3](https://arxiv.org/abs/2607.19995v3).
The support and its four-chromaticity are prior art; no new graph, coordinate
field theorem, or priority claim is made. Our proof uses the explicit certificate
and checks below, not the preprint's field-theoretic assertions.

The terminal and interior orders are

```
T = (0,1,3,6,9,14,15,16,17,18)
I = (2,4,5,7,8,10,11,12,13).
```

The terminal graph is the disjoint union of the path `3-0-1-6`, the isolated
vertex `9`, and the cycle `14-15-17-18-16-14`. In particular, there are no hidden
palette, monochromaticity, or distinct-colour assumptions in the relation.

## Geometry proof

Let `F` be the vector of the 34 squared-distance equations minus one, `m` the
rational midpoint vector, `r=10^-25`, `J=DF`, and `A` the rational matrix in the
certificate. In the induced infinity norm the checker computes exactly

```
beta = ||I - A J(m)|| < 1
eta  = beta + 16 r ||A|| < 10^-21
||A F(m)|| + eta r < 10^-46 < r.
```

Each row of `J` has at most four nonzero entries. Moving within the box changes
each entry by at most `4r`, hence `||J(x)-J(m)|| <= 16r`. Consequently
`Phi(x)=x-A F(x)` is a contraction on the box and maps it strictly into itself.
The contraction theorem gives its unique fixed point. Since `beta<1`, the
square matrix `A J(m)` is invertible, and so is `A`. Thus that fixed point is
exactly a real zero of `F`, and it is the unique zero in the box.

For a midpoint difference `d=(dx,dy)`, perturbing both endpoints inside their
boxes changes the squared distance by at most

```
4 r (|dx|+|dy|) + 8 r^2.
```

Every pair's squared distance is bounded below by `1/100`. Every unlisted pair
has squared distance separated from one by more than `1/100`. The listed edge
equalities follow from the root equations (and the fixed anchor edge). Thus
collision exclusion and complete contact reconstruction apply to the exact
root, with no tolerance-based edge decisions in the proof.

## Relation certificate and completeness

[completions.txt](completions.txt) has one nine-digit interior colouring for each
proper terminal pattern, in lexicographic restricted-growth order. A restricted-
growth word starts at zero and introduces colours in order of first appearance,
using at most four colours. [verify.py](verify.py) enumerates these words, checks
the terminal edges, fills the nine remaining vertices, and directly checks all
35 edge inequalities for every row. The certificate is 43,200 bytes and requires
no SAT solver to verify.

The independent counting formula for the bare terminal graph is

```
P_T(4) = (4 * 3^3) * 4 * (3^5 - 3) = 103680 = 24 * 4320.
```

Every proper terminal colouring uses at least three colours because of the odd
cycle, so colour permutations act freely and every class has 24 elements.
There are exactly 360 three-colour classes and 3,960 four-colour classes. This
establishes that the checked relation is complete, rather than a sample of pin
assignments.

[direct_audit.py](direct_audit.py) supplies a separate algorithmic check. It
reads no completion certificate, imports no SAT solver, and performs no colour-
symmetry pruning. It directly enumerates all 103,680 labelled proper pin
assignments and extends each by finite domain backtracking. All succeed; the
returned words pass 3,628,800 edge inequalities. Its separate exhaustive
three-colour search fails in 1,048 recursive nodes, checking the known `chi=4`
status. This is author-side validation, not an independent-author review.

The abstract attachment consequence is precise: adjoining this support to a
four-colourable graph only along these terminals, with no other cross-edges or
identifications and with the terminal edges already respected, preserves four-
colourability. For a complete physical unit graph those extra-contact conditions
must actually be checked. We do not exclude compositions with new contacts to
internal points or a different interface. In particular, the neutral relation
provides no forcing premise to which an at-most-508 composition budget could be
assigned; no hypothetical copy-count budget is advertised as a construction.

## Reproduction

From this directory, with Python 3.11 or later and its standard library:

```bash
python3 -B verify.py
python3 -B direct_audit.py
python3 -B controls.py
python3 -O -B verify.py
sha256sum -c SHA256SUMS
```

Expected main status: `EXACT EI19 TEN-TERMINAL RELATION IS NEUTRAL`.
See [EXPECTED.json](EXPECTED.json) and [VALIDATION.json](VALIDATION.json) for
exact outputs and the author run. The main replay is under one second; the
labelled direct audit took about seven seconds on the author machine. Eight
corruptions of geometry and colouring certificates are rejected without relying
on file hashes. Normal and assertion-disabled main replay agree.

Optional regeneration uses `python-sat==1.8.dev24` with CaDiCaL195, as pinned in
[requirements-discovery.txt](requirements-discovery.txt):

```bash
python3 -B generate_colours.py /tmp/ei19-completions.txt
cmp completions.txt /tmp/ei19-completions.txt
```

The encoding has exactly one Boolean colour among four at each of 19 vertices,
edge clauses forbidding equal colours at every physical unit edge, and the ten
positive pin literals. It is sound and complete for ordinary four-colouring;
there are no additional symmetry clauses. The solver only produces positive
models, which are decoded and directly checked. Exact regeneration matched the
committed certificate. SAT soundness is not a premise of the theorem.

Certificate SHA-256 values:

- Geometry: `59e5ead5664daebcc2a68d83c14320976723b69eac7a566a5b4256946ae66fc4`
- Completions: `f295ca7bee83a5ea5460df1c1dab0ac61c0a7c871ee42205a1ad0552aa681baa`
- Full reconstructed colouring stream: `1f34b5098f8117eab4c22eb9e16e1233f749dc1230f2ea591c58920eafd2ab0e`

The trust boundary is the elementary contraction/coverage arguments, source
transcription, these small checkers, Python exact arithmetic and ordinary
hardware. There is no proof-assistant formalization or external-author review.
No large artifact or external numerical input is needed for verification.

## Research context

The bounded live literature refresh on 2026-09-14 retained 509 vertices and
2,442 edges as the working published record:
[Parts, arXiv:2010.12665v2](https://arxiv.org/abs/2010.12665v2), also identified as
the record in [Haugland, arXiv:2608.04542v4](https://arxiv.org/abs/2608.04542v4).
That search is not proof of absence of unpublished or unindexed improvements.
This package makes no record claim.

The selected ten-terminal source is retired at this boundary. The neutral
relation and all smaller retained internal cores cannot supply its proposed
forcing premise. Choosing other terminals or changing physical contacts would
be a new investigation, not an implication of this census.
