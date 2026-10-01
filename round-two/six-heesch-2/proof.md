# Pair-centered interior-contact peeling

Researcher: **six-heesch-2**. This is a finite reduction for unmarked polyhexes,
with all Euclidean rigid motions and reflections allowed. Its computation is
an upper-bound test, not a constructive corona algorithm.

Let `S` be a connected hole-free union of unit regular hexagons. Its cell
coordinates use the center basis `(sqrt(3),0),(sqrt(3)/2,3/2)` when hexagon sides
have length one. The six neighbor differences
are `(1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1)`. All twelve grid orientations
and all integer translations are permitted.

For a finite cell set `C`, define `halo(C)` to be the cells outside `C` sharing
an edge with a cell of `C`. A *contact* is a disjoint congruent grid copy meeting
this halo. In the honeycomb grid, two distinct cells sharing a vertex also
share an edge, so this contact definition includes boundary-point contacts.

## Geometric bridge

Every boundary vertex of a polyhex has angle 120 or 240 degrees, and each
boundary edge has length one. Suppose an old polyhex patch is entirely inside
a larger finite packing of polyhexes. A corner meeting the interior of an old
edge would use 120+180 degrees and leave an impossible 60-degree sector, or
use 240+180 degrees and overlap. A corner of the old patch cannot meet a
smooth boundary point either, for the same angle reason. Thus a positive-length
contact matches complete unit edges. Such an edge identifies the same regular
hexagons on its two sides and fixes the ambient honeycomb grid.

At an old boundary vertex the filled angle list is either `(120,240)` or
`(120,120,120)`. Its 120-degree hexagon sectors are fixed by the old copy;
each new copy occupies one or two of those very sectors. It therefore contains
a cell of the same grid and shares that grid. This includes a new copy that
initially contacts only at a boundary point. Induction over complete coronas
locks every copy, including the last corona, to the initial grid.

This is the local version of the standard full-tiling polyhex angle argument;
grid locking is not claimed as new. The previously published
[polyhex growth source](../../heesch_polyhex_bridge_growth/README.md) states
the edge and vertex-sector argument and attributes the full-tiling version to
Paul Church, *Snakes in the Plane* (2008), Proposition 2.2.1.1.

Consequently a negative result below excludes arbitrary real translations,
rotations and reflections. No grid-only hypothesis is silently added to a
geometric upper-bound claim.

## Complete finite contact universe

Let `E_0` be all contacts with `S`, represented as whole cell footprints.
For each orientation `O` and each halo cell `q` and oriented cell `p`, test
translation `q-p`. Keep the disjoint footprints. Any contact covers some such
`q` by some such `p`, so the enumeration is complete. It is finite.

Transport a domain `E` from `S` to another copy `A` by any isometry taking
`S` to `A`. Domains are closed under stabilizers of `S`, making this independent
of the chosen isometry. They are reciprocal: if `B` is allowed next to `A`,
`A` is allowed next to `B`. Both properties are checked explicitly by the code.

A packing is `E`-compatible if every contacting pair, transported back to the
root, belongs to `E`. Noncontacting pairs have no domain restriction, while all
whole footprints must be disjoint.

For `r>=0`, retain `B in E_r` in `E_(r+1)` precisely when the two fixed copies
`S,B` admit a finite `E_r`-compatible packing that covers `halo(S union B)`.
The added copies can all be required to touch `S` or `B`: any copy covering a
required halo cell does so. Copies that cover no required cell can be omitted.
Thus the union of the two transported finite contact domains is a complete
candidate pool. Testing full footprints and all contacting pairs gives the
exact finite decision. Holes in this local packing are allowed.

The definitions preserve stabilizer closure and reciprocity and yield a
nested sequence of finite domains. Stabilization is not evidence of a plane
tiling or of an infinite Heesch number.

**Lemma.** In a complete `H`-corona packing, every contacting pair whose two
corona levels are at most `H-r` belongs to `E_r`.

*Proof.* At `r=0`, grid locking and disjointness put every contact in `E_0`.
Suppose the statement holds at `r`. Consider a pair `A,B` with levels at most
`H-r-1`. Their boundaries are covered by the next cumulative prefix. Retain
only copies covering a halo cell of `A union B`, together with `A,B` themselves.
Each retained new copy touches `A` or `B`; hence its level is at most `H-r`.
Every contacting pair in this subpacking therefore belongs to `E_r` by the
induction hypothesis. This supplies the local packing needed for `E_(r+1)`.
Transporting it to the root proves the claim. No hole exclusion was used. □

**Corollary.** If the root cannot be surrounded by a disjoint `E_r`-compatible
packing of allowed neighbors, then `H_h(S)<=r` and `H_c(S)<=r`.

*Proof.* An `(r+1)`-corona packing has a first corona. Every copy in that first
corona has level at most one, which equals `H-r` when `H=r+1`. The lemma puts
all its contacts, including contacts between first-corona copies, in `E_r`.
It would supply the allegedly nonexistent root surround. □

The corollary does not require the local pair surrounds to fit together into
global coronas. A positive local test is only a necessary condition.

The same test separately excludes a plane tiling: every pair of a plane tiling
belongs to every `E_r`, by induction using its actual finite set of neighboring
copies. Bounded tile diameter and positive tile area give local finiteness.
A root then has an `E_r`-compatible surround for every `r`, contradicting the
negative root test. This closes the convention that plane tilers have infinite
Heesch number independently of any topology assertion about contact balls.

## Safe first-round prefilter

Let `F` be the contacts occurring in at least one full surround of the root,
without restricting the final topology. In a successful two-root test at round
one, each fixed tile is surrounded. Thus both directed versions of the fixed
contact lie in `F`. It is safe to test only the reciprocal part of `F` at round
one. The *candidate neighbors* in these tests still come from all of `E_0`.
Restricting those neighbors to `F` would impose an extra interiority obligation
and would invalidate the stated depth bound. The implementation keeps these
two sets separate.

## Exhaustive decision and resource boundary

`cover.py` represents required cells and candidate conflicts by integer bitsets.
For an uncovered required cell, it branches over every still-compatible copy
covering it. Selecting a copy deletes all conflicting copies and its covered
required cells. A branch succeeds exactly when no required cell remains.
An exhausted tree therefore decides nonexistence in this finite universe.
Memoization stores only failed states `(available,remaining)`, which completely
determine all future choices. The minimum-remaining-choices rule changes branch
order, not coverage.

The node guard throws `Incomplete`; it never returns a negative answer. There
are no native solvers, floating-point exclusions or timeout-based verdicts.

Every negative `find` call in the published replay is checked by `audit.py`.
It rebuilds coverage and whole-footprint conflicts through cell incidence,
instead of the searcher's pair-intersection loops. For restricted contact
domains it uses direct neighbor incidence and freshly reconstructed relative
isometries, instead of the searcher's halo sets and precomputed frames.
It checks the entire failed-state DAG in increasing remaining-cell count.
A failed state is accepted only when some uncovered cell has no legal copy,
or every legal copy leads to an already checked failed state. Selecting a copy
covers that chosen cell, so the remaining-cell count strictly decreases and
the justification is acyclic. This certifies rejection independently of the
search order and memoization decisions. Every positive decision is also checked
directly for coverage and pairwise compatibility. A fabricated rejection of a
satisfiable one-cell instance must be rejected by the auditor.

The auditor checks all negative first-surround support tests, as well as the
pair and final-root rejections. Certifying only the final root rejection would
not validate a domain produced by unchecked contact exclusions. Raw rejection
DAGs are transient and regenerated by the source; they are not a published
proof corpus.

The geometric argument, exact Python implementation and auditor remain
unformalized trust boundaries. The two implementations share the integer
isometry primitives. Internal auditing is not an independent peer review.
