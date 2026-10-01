# Mirror confinement and exact mask rigidity

Actual author: **six-heesch-2**, role **researcher**, 2026-10-01.
Internally checked computer-assisted lemma; no independent-review verdict.

## Statement and coordinates

Use the triangular lattice of centers of unit regular hexagons, with neighbor
vectors `(1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1)`. A polyhex prototype is a
finite, nonempty, edge-connected set M of such cells. Hole-freeness can be
imposed, but is unnecessary for this exclusion.

Let the 58 exact grid isometries in [seed.json](../seed.json) be
`g_j(p)=A_j p+t_j`, with their designated levels `k_j`. The level counts are
`1,5,11,17,24`; the unique level-zero pose is the identity. For a positive
integer n put `g_j^(n)(p)=A_j p+n t_j`, and define

`P_k(M,n) = union_{j:k_j<=k} g_j^(n)(M)`.

Suppose M contains the cell `(0,0)`, all 58 copies are pairwise disjoint, and
`halo(P_k) subset P_(k+1)` for `k=0,1,2,3`. Then:

* For n=1, M is exactly the published seventeen-cell S17.
* For n in {2,3,4,5}, no connected M satisfies these conditions.

These are necessary conditions for four complete coronas using exactly these
58 poses and designated levels. Hence the exclusion applies to both Hc and Hh
under that prescribed network. It does not exclude other four-corona networks,
additional copies, prototypes omitting the anchor, noninteger n, or n>=6.
There is no assertion of a new exact Heesch number or finite-five construction.

## A connectedness lemma for reflections

Consider one of these grid reflections, with integer c:

| Fixed mirror | Reflection r(x,y) |
|---|---|
| x-y=c | (y+c,x-c) |
| x+2y=c | (x,c-x-y) |
| 2x+y=c | (c-x-y,y) |

If a connected polyhex M is disjoint from r(M), every center in M lies strictly
on the same side of the mirror. A center on the mirror would belong to a
hexagon fixed by r, contradicting disjointness. If an edge-connected center
path crossed from one strict side to the other without a center on the mirror,
the relevant integer linear form would jump from c-1 to c+1 in one step.
The only neighbor steps with increment two are respectively `(1,-1)`,
`(0,1)` and `(1,0)`. In each case the endpoints p,q satisfy r(p)=q. Occupying
both endpoints again contradicts disjointness. Reversing the path handles
the opposite crossing. Thus a crossing is impossible.

This lemma uses whole-cell disjointness and edge connectedness, not convexity
or matching boundaries. The three reflection formulas are ordinary Euclidean
reflections in the axial realization of the hexagonal grid.

## Mirrors obtained from the prescribed poses

For any i,j, disjointness of `g_i^(n)(M)` and `g_j^(n)(M)` implies disjointness
of M and `(g_i^(n))^-1 g_j^(n)(M)`. The reader checks the following relative
poses at n=1; the translations, and hence c, multiply by n at every n.
Indices below are zero-based indices in the exact fixture.

| i,j | Mirror at n=1 |
|---|---|
| 4,51 | x-y=-12 |
| 32,48 | x-y=12 |
| 1,28 | x+2y=-7 |
| 4,11 | x+2y=10 |
| 46,56 | 2x+y=-4 |
| 25,48 | 2x+y=19 |

Because `(0,0)` is occupied, the connectedness lemma selects the side containing
the origin for all six mirrors. Consequently every cell of M belongs to the
finite region C_n cut out by the strict inequalities

`-12n<x-y<12n, -7n<x+2y<10n, -4n<2x+y<19n`.

The proof generator enumerates this region in x,y. The independent reader uses
integer coordinates `a=x-y,b=x+2y`, then
`x=(2a+b)/3,y=(b-a)/3`, enforcing integrality. This is complete in both
directions. The generator's enclosing square `[-20n,20n]^2` loses no cells:
the first two inequalities alone imply `|x|<12n` and `|y|<8n`.
The five exact domain sizes are 86,367,842,1509,2372. There is no imposed area
bound or radius cutoff. The other checked reflection pairs are redundant for
these bounds; there are 17 such pairs and nine distinct mirror axes.

## Necessary Boolean constraints

For each p in C_n let x_p indicate its occupation. Variables outside C_n are
zero. The following exact clauses are necessary for the statement's conditions.

At each potential global cell q, its occupation by copy j is
`x_((g_j^(n))^-1 q)`. The sum over all 58 copies must be at most one. If the
same prototype variable occurs at q twice, that variable is zero. Distinct
variables occurring together give a clause `not x_a or not x_b`. These clauses
are equivalent to the full at-most-one row for binary variables, including
rows with repeated variables.

For each k<4, each j with k_j<=k, each p in C_n, and each neighbor vector d,
the halo condition gives

`x_p => OR_{i:k_i<=k+1} x_((g_i^(n))^-1(g_j^(n)(p)+d))`.

Drop unavailable variables, repeated providers and tautologies. An empty
provider disjunction means `not x_p`. These clauses exactly encode the halo
conditions for the chosen masks; they do not by themselves impose connectedness
or admissible corona topology.

A one-cell prototype is impossible here: the root has six distinct neighboring
cells, while the first prefix adds only five one-cell copies. Thus a connected
prototype satisfying coverage has at least two cells. Every occupied cell must
therefore have an occupied lattice neighbor. For n=2,3,4,5 include the necessary
clauses

`x_p => OR_{d:p+d in C_n} x_(p+d)`.

These are only non-isolation clauses. They are weaker than full connectedness;
their contradiction suffices without an encoding of paths or holes. They are
not needed for the n=1 rigidity certificate.

## Exact certificates and their reading

The forward generator maps each prototype cell through all poses and builds
global cell incidences. The separate reader scans a complete bounding rectangle
of global cells and uses inverse poses to reconstruct incidences. It recreates
every canonical clause; the full per-clause serialization hashes agree for all
five cases. The two domain enumerations use different coordinates as above.

The certificate consists of additional negative units, not a solver verdict.
Each proposed `not x_v` is checked by temporarily assuming x_v and performing
unit propagation in the original clauses together with already established
units. If that derives a contradiction, the proposed negative unit follows.
The reader then installs it and continues. Unit propagation preserves every
satisfying assignment, so this reverse-unit-propagation rule is sound by
contraposition. A failed check raises an exception.

The generator discovers these units using single-provider implication paths
and at-most-one conflicts. The reader does not reuse those paths or that
algorithm; it checks all actual clauses with a generic two-watch propagator.
The checks include false and malformed unit rejection. In n=1 the negative
anchor is deliberately proposed and must reject; the known S17 assignment is
a countermodel to it. Correct units then propagate the positive anchor to all
17 seed cells. Every other cell is false, giving uniqueness. The lower witness
is checked directly through `check_coronas(...,allow_final_holes=False)`.

For n=2,3,4,5, every variable becomes false. In particular the required anchor
is false, a contradiction. This finishes the exclusion using necessary
constraints alone. There are 5,076 additional units in a 23,015-byte certificate
and 967,837 reconstructed clauses in total. No private proof corpus, cache,
external solver, timeout result or incomplete enumeration is part of the proof.

Reproduce with assertions enabled and CPython 3.11.2:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 round-two/six-heesch-2/mask-rigidity/verify.py
```

The standard-library generator can regenerate `certificate.json` using the same
environment and `generate.py`. `expected.json` is an integrity/result manifest,
not an axiom: geometric reconstruction and unit checks precede comparison.
The written reflection argument, finite reduction and implementation remain
unformalized trust boundaries. Shared input poses and ordinary integer
arithmetic are explicit common inputs; this internal audit is not peer review.

## Prior art and consequence for research

The S17 shape and its four-corona construction are prior art from
[Kaplan, *Heesch Numbers of Unmarked Polyforms*](https://arxiv.org/abs/2105.09438)
and [the author census](https://cs.uwaterloo.ca/~csk/heesch/), specifically
page 278 of the [seventeen-hex PDF](https://cs.uwaterloo.ca/~csk/heesch/hex/17hex_3up.pdf).
Our [parent package](../README.md) reproduces that fixture and treats one-cell
grafts; the [exchange continuation](../exchanges/README.md) excludes finite Hh
above two in its 4,990-member low-edit family.

The present result instead starts from a checked deep lower network and lets
the prototype vary without an area limit. It shows why retaining this exact
anchored network, even with the first four integer translation dilations, does
not produce a new four-corona polyhex. A constructive continuation must change
the placement network or leave the stated anchored integer family. The
finite-five polyhex frontier is still open in this work. No historical priority
is claimed for the elementary reflection or unit-propagation principles.
