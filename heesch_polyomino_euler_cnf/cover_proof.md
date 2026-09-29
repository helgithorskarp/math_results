# Rooted metric covering obstructions for square-grid coronas

six-heesch-1 — researcher — 2026-09-29.

All copies in this note are translations, quarter turns, or reflections of one
disc polyomino on a common unit square grid. A cell is a closed unit square;
distinct copies have disjoint cell interiors. Nothing in this reduction excludes
coronas using arbitrary off-grid rigid motions.

Here Hc requires a closed disc at every prefix. Hh requires disc prefixes before
the last, and permits holes and corner pinches in the last prefix, exactly as
the supplied `--holes-last` checker option does. All upper bounds also apply
to more restrictive final-prefix conventions. The covering implication itself
does not require any of these topology conditions.

Let P be the finite set of cell coordinates of the prescribed central copy,
let m=|P|, and let d be its cell-coordinate Chebyshev diameter. Write

\[
B_r=\{-r,\ldots,r\}^2,\qquad R_r=P+B_r.
\]

A rooted covering of radius r is a finite packing of congruent copies containing
the prescribed P and occupying every cell of R_r. The packing can extend outside
R_r. It need not have corona ranks, admissible prefix topology, or even a
connected union. Define C(P) as the largest coverable integer radius, or infinity
if every radius is coverable.

## The upper-obstruction implication

Suppose X_k is the occupied prefix through a complete k-corona. Complete
surrounding on the square grid means

\[
X_{k+1}\supseteq X_k+B_1.
\]

Indeed every cell in the eight-neighbour halo of X_k must be occupied: an absent
side neighbour exposes an edge, and an absent diagonal neighbour exposes the
shared vertex. Conversely occupation of this entire halo places the closed
prefix in the interior of the next union. Since X_0=P, induction gives

\[
X_k\supseteq P+B_k=R_k.
\]

Consequently a complete H-corona patch supplies a rooted radius-H covering.
If radius r has no rooted covering, every such Heesch number is at most r-1.
This implication discards topology, so it holds with disc prefixes, with
connected hole-free pinched prefixes, and with holes allowed in the final
corona. A covering witness supplies no multi-corona lower bound.

At depth one there is a useful exception. From a covering of radius r>=1,
retain only noncentral copies meeting the root's eight-neighbour halo. The
halo remains covered and every retained copy touches the root. This is one
complete corona with holes permitted in the final corona. Thus C(P)>0 gives
Hh>=1, while C(P)=0 gives Hh=0. It gives no disc topology for the outer patch.

## A complete small candidate region

Consider any rooted covering of radius r. Delete all noncentral copies that
miss R_r. This preserves coverage of R_r and all nonoverlap conditions. Every
remaining noncentral copy Q meets R_r at some cell p. All its cell coordinates
are within d Chebyshev steps of p, even after a quarter turn or reflection.
Therefore

\[
Q\subseteq R_r+B_d=P+B_{r+d}.
\]

Normalize P so its minimum x and y coordinates are zero; write a,b for its
maximum coordinates and L=max(a+1,b+1), so d=L-1. Every relevant copy is inside

\[
[-r-d,a+r+d]\times[-r-d,b+r+d].
\]

If this envelope contains N' cells, N'=O((r+L)^2). There are at most 8N'
oriented translated copies in it. Enumerate exactly those that meet R_r and
do not overlap the prescribed central copy. This is complete for rooted
covering, regardless of how far a different corona construction extends.

The generator loops over each normalized orientation of width w and height h.
If a copy meets the target whose bounding coordinates are xmin,xmax,ymin,ymax,
its translation lies in [xmin-w,xmax] × [ymin-h,ymax]. The explicit intersection
test then removes copies missing the target. This loop and the preceding
metric argument give two descriptions of the same complete candidate set.

## Exact CNF and its trust boundary

Use one selection variable z_Q per candidate. For each cell p in R_r minus P,
add an at-least-one clause over candidates containing p. For **every** cell in
the entire candidate footprint, including cells outside R_r, impose at most
one selected candidate. All candidates overlapping P were already removed.

Any satisfying assignment therefore gives a nonoverlapping rooted covering.
Conversely a rooted covering can be trimmed as above, selects enumerated
candidates, and extends to the sequential at-most-one auxiliary variables.
This proves exact satisfiability equivalence. A proof of Boolean UNSAT thus
excludes r complete coronas through the previous implication.

With M candidates, the total footprint incidences are mM. Sinz's sequential
at-most-one encoding has size linear in these incidences. The coverage clauses
also have at most mM literal occurrences. Thus variables, clauses, and literal
occurrences are O(mN'). There are no corona-rank or topology variables. In
contrast, the complete witness generator in [proof.md](proof.md) uses an
O(H^2 L^2) cell box and an O(HNm) cumulative encoding. This asymptotic reduction
is for an upper-bound relaxation; it does not replace that witness generator.

`cover.py` writes exact DIMACS and decodes raw copies. Its independent geometric
checker verifies congruence, the prescribed root, all footprint overlaps, and
coverage by distance to P. `validate_cover.py` enumerates candidates a different
way, anchoring each tile cell at each target cell. A direct bitset exact-cover
backtracker provides decisions without a SAT encoding. Native solver UNSAT
remains untrusted until checked. A solver trace that is empty because the
input CNF already contradicts unit propagation is replaced by the single
empty proof clause; the proof checker must still verify that clause.

## Relation to plane tiling

If P has a grid tiling, every R_r is covered by finitely many tiles of a tiling
containing the prescribed root. Conversely, if every R_r has a rooted covering,
Boolean compactness gives a grid tiling containing P. Here is the precise
compactness application. Introduce a variable for every oriented translated
copy. Require the root, exclude all other root-overlapping copies, and require
each lattice cell to belong to exactly one selected copy. Each cell belongs to
only finitely many possible copies, at most 8m, so these are finite clauses.
Any finite subset of the clauses mentions finitely many cells that require
coverage. Choose r containing these cells and use a rooted radius-r covering,
with every omitted copy variable false. All overlap clauses are then satisfied
everywhere. Propositional compactness produces an assignment satisfying the
whole system, hence a tiling.

Thus every polyomino that does not tile on the grid has a finite radius
obstruction. The compactness principle, neighbourhood-cover idea, and generic
exact-cover CNF are standard; no historical priority is claimed for them.
This note supplies the explicit envelope and a reproducible upper-certificate
implementation alongside the previously published corona witness compiler.

## Periodic certificates used to filter searches

`periodic.py` searches for a small number of copies whose translates by the
lattice generated by (a,0),(b,c), with a,c>0 and 0<=b<a, tile the plane. The
certificate lists their raw cells. Its checker requires total area ac and
checks that no two listed cells have a difference in that lattice. Membership
for a difference (dx,dy) is exactly

\[
c\mid dy,\qquad a\mid dx-b(dy/c).
\]

The ac cells consequently represent each coset of the index-ac lattice once.
Their lattice translates partition all square-grid cells, proving a plane
tiling. This checker uses pair differences; the search uses residue bitmasks.
Failure of the periodic search is never an upper bound or a nontiling proof.

## Completeness of the three-cell growth family

The search family consists of disc polyominoes obtained by adding exactly three
square-grid cells to the attributed 17-cell seed in `kaplan17.json`, modulo
translations and all eight square-grid symmetries. Intermediate shapes are
allowed to have holes. Because the seed and final polyomino are side-connected,
the three added cells have an ordering in which each meets the seed or an
earlier added cell along a side. Such an ordering follows by growing a rooted
spanning forest on the three new cells, with the seed contracted to one vertex.
Therefore three successive side-boundary additions enumerate every final
shape. Normalization and set deduplication remove repeated growth paths;
only the final disc condition is tested.

An independent enumeration considers all triples in the taxicab-distance-three
neighbourhood of the fixed seed. Every connected three-cell addition lies
there: each added cell has a path to the seed through at most three new cells.
The pool contains 63 possible cells, hence 39,711 triples. Direct connectivity
testing leaves 1,237 connected triples. The final disc and independent symmetry
tests give exactly the same 1,233 free shapes as the growth-path enumeration.
The ordered compact family serialization has SHA256
`935192a6bead7d979d7ed60f3907e52278962940d9b3c008d18af94a85fc36ef`.

This is a precise family containing a congruent copy of the specified seed. It
does not enumerate all 20-ominoes, other seeds, or cell exchanges.

## Checked family result

The 1,233-member family has the following exact rooted covering radii. A finite
entry uses a radius-C covering and a radius-(C+1) UNSAT certificate; infinite
entries have checked lattice-periodic plane tilings.

| C(P) | Number | Consequence for grid Heesch numbers |
| --- | ---: | --- |
| 0 | 434 | Hc=Hh=0 |
| 1 | 308 | Hh=1, Hc<=1 |
| 2 | 74 | 1<=Hh<=2, Hc<=2 |
| 3 | 9 | 1<=Hh<=3, Hc<=3 |
| infinity | 408 | Periodic plane tilers |

The tiling certificates have 46 one-copy, 302 two-copy, and 60 four-copy
fundamental domains. Exact Hc and Hh values for C=2 and C=3 are undetermined.
Every finite member nevertheless has grid Hh<=3, so this growth family contains
no finite grid Heesch-number-four or -five improvement. Arbitrary-motion
upper bounds and other 20-cell families are outside the theorem.

The compact manifest contains formula hashes, preceding covering radii and
small periodic poses. `verify_growth.py` regenerates each formula, checks a
fresh solver proof with DRAT-trim, checks the preceding covering geometrically,
and extracts a first-corona construction where applicable. It reconstructs and
checks all periodic poses by pair differences. Budget exhaustion interrupts
verification and supplies no exclusion. Raw formulas and traces are omitted.

The attributed seven-cell Hc=Hh=1 input has a radius-two formula of 4,436
variables and 11,453 clauses, with an included 68-clause RUP proof. Its existing
disc-corona witness gives the lower bound. The attributed 17-cell Hc=Hh=3
input has C(P)=9: the included radius-nine covering occupies 765 cells in 45
copies; a checked radius-ten UNSAT trace excludes larger radii. That trace is
regenerated from source. The gap between C=9 and published Hh=3 illustrates
why metric coverage supplies no multi-corona construction. These reproductions
are not new Heesch records.

## Prior literature and scope

Kaplan's [Heesch Numbers of Unmarked Polyforms](https://arxiv.org/abs/2105.09438)
already develops grid-corona SAT and supplies the attributed tile inputs used
here. The existing finite-candidate and prefix-topology reduction is proved in
[proof.md](proof.md). Written mathematical reductions, exact Python, and the
certificate checker remain the trust base; these results are not formalized
in a proof assistant. No finite Heesch record improvement follows merely
from a rooted covering or from reproducing an existing tile's upper bound.
