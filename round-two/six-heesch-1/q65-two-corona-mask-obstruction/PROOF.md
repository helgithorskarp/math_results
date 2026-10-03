# Fixed-mask periodicity implication

Actual author **six-heesch-1**, role **researcher**. Author-checked exact
computer-assisted lemma, independently unreviewed and unformalized. No
historical priority or finite-number record is claimed.

## Precise finite family

Let Q be the literal 65-cell Q65-P17 source in input.json. Each cell is a closed
unit square with the specified integer lower-left coordinate. Let U consist
of all integer cell coordinates at Chebyshev distance at most one from some
cell of Q. U has 123 sites. Choose ANY nonempty subset S of U; connectivity,
no holes, fixed area and interior-cell preservation are not assumed.

The nineteen fixed physical isometries are recovered from the literal
normalized D4 poses in input.json, grouped as 1 root, 6 first, 12 second copies.
For an original pose (o,x,y), transform the physical vertices of Q by its D4
matrix M. If its lower-left minimum is b, the physical isometry is
`z -> M z + (x,y)-b`. This fixes the actual map before S changes. Reordering
new source orientations or moving its minimum cannot change these maps.
The root is the identity. Put P_k equal to the union of the saved copies of S
through level k, k=0,1,2.

**Lemma.** If all nineteen copies have pairwise disjoint interiors and
`Moore(P_0) subset P_1`, `Moore(P_1) subset P_2` in cell coordinates, then the
eight maps in tiling.json and all their translations by `(22,6),(-6,22)` tile
the whole plane by copies of S. In particular |S|=65.

A pair of complete admissible disc coronas at exactly these physical motions
satisfies the hypotheses. Per-copy contact, source/prefix discs and arbitrary
alternative later placements are not additional premises needed by the
lemma. Any simple polyomino in this finite source/motion family is a plane
tiler and therefore cannot have a finite Heesch number. The implication is
also preserved by a common Euclidean isometry of the whole configuration.
No statement is made for sources outside U or changed early motions.

## Packing, halos and the exact failure predicate

Use Boolean x_p for selecting source site p in U. At every fixed copy, the
same x_p selects its physical image cell. For every pair of copies and every
coincident image cell from sites p,q, add `not x_p or not x_q`. If p=q this
becomes a unit forbidding a self-overlapping common site. These clauses
express whole-copy packing exactly, without an edge-registration inference
about other possible packings.

For each possible selected cell of P_k, k=0,1, and all nine neighboring cell
coordinates including itself, add `not x_p or OR x_q`, where the suppliers are
ALL saved copies through level k+1 that can cover that coordinate. A missing
supplier gives `not x_p`; a tautological row is safely omitted. Nonempty S is
one clause containing all 123 source variables. The cell conditions follow
from strict surrounds at these square-grid motions, including the boundary
vertices; arbitrary alternative copies elsewhere are not silently restricted.

Let L have generators `(22,6),(-6,22)`, index 520. Transform the eight actual
period representatives physically. In each of the 520 quotient cell classes,
let C_r be the sum of selected contributions. A source variable may have an
integer coefficient greater than one if several representatives hit the
same class. The proposed whole-plane tiling holds exactly when every C_r=1.

Introduce z_r for an allegedly bad row, C_r!=1. For each coefficient-one term
x_p in that row add
`not z_r or not x_p or OR(other distinct row variables)`.
There is no corresponding clause for a term with coefficient>=2. These
clauses say precisely that, when z_r is true, no coefficient-one term is
alone active. If C_r=0 all terms are false; if C_r>=2 at least two terms or a
higher coefficient are active. Finally require OR(z_r). Thus ANY source mask
whose specified period fails has an auxiliary assignment satisfying this
predicate, and no exactly-covered row can license z_r. This is an equivalence,
not a stronger heuristic filter.

The full canonical formula has 643 variables and 2859 clauses, SHA256
`aa183740e680950e521393b4f2111913bbe1f40600cc321ccab18f63c6574dcb`.
The solver-free reader reconstructs it independently via unordered copy
pairs, direct physical square vertices, and lattice-adjugate membership
rather than the producer's global owner table and HNF residue function.
It then replays proof.rup by reverse unit propagation, keeping every proved
clause. A RUP addition is valid because assuming its negation conflicts by
unit propagation with the preceding clauses; the final empty clause is a
refutation. No native solver verdict is trusted. No assignment satisfying
packing/halos/nonempty can fail the period predicate.

Every row therefore has C_r=1. Translating the eight copies by all L vectors
covers each unit grid cell exactly once; interiors are disjoint. Summing all
520 row counts gives 8|S|=520, hence |S|=65. This proves the lemma for every
one of the 2^123-1 nonempty masks, without explicit mask enumeration.

## Positive and scope controls

The original Q65 has two checked disc coronas and the specified plane tiling.
Removing the failed-period disjunction admits it. Removing nonempty admits
the empty mask with all z_r true. The reader verifies both satisfying
controls and rejects the damaged refutations. It also rejects a missing
final empty clause and replacement of the two-stage formula by the first
stage alone.

The counterexample fixture Q64R1 has 64 cells, one complete disc corona, and
seven total copies. Its raw source lies in U; after translating the source
origin, its physical first placements are exactly the prescribed maps. All
prefixes have a single simple oriented boundary cycle, no pinches/holes, full
halos and actual per-copy contacts. It fails the specified period tiling;
eight 64-cell copies cannot cover 520 distinct quotient cells exactly once.
Therefore a valid first corona alone does not imply this SAME period
conclusion. This is not proof that Q64R1 fails every other plane tiling or
that its global Heesch number is finite. The reader checks the exact source,
origin and all seven whole footprints, not just aggregate counts.

## Prior context and limitations

Q65's earlier plane-tiling finding 9946, source
`b5454f3b8fa8e9ad294695d4cd91f7dcda74d4c2`, is prior context and supplies the
literal source/motion template. Its four-corona predecessor 9888 only trapped
specified retained hosts and remains valid; this lemma does not turn those
local upper certificates into a shape-wide finite bound.

[Kaplan Section2.1](https://arxiv.org/html/2105.09438v1#S2.SS1) gives the corona
and plane-tiler conventions; [primary dataset](https://cs.uwaterloo.ca/~csk/heesch/)
and [paper](https://arxiv.org/abs/2105.09438) describe bounded enumerations,
not a universal all-size bound. The new source family, not a historical
record, is what is resolved here. The finite-five polyomino target is open.
A larger 183-site necessary two-corona formula reached the unchanged
3000-conflict UNKNOWN guard; no stronger conclusion follows.

Discovery used CPython3.11.2, PySAT1.8.dev24 and Glucose4, one native thread.
Reproduction needs Python>=3.10 and its standard library only. Exact integer
operations, the Boolean/physical-square bridge, lattice index, polygon
boundary topology and RUP implementation remain unformalized mathematical
trust boundaries. There is no independent peer-review verdict.
