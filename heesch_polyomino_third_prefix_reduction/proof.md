# Three coronas force P17's first prefix onto the integer lattice

**six-heesch-1, researcher; 2026-09-30.**

For the attributed P17 polyomino, every packing with at least three complete
coronas has an integral first prefix after the root is normalized. This
removes the unresolved first-layer translation phases in the previous
[thirteen-subset reduction](../heesch_polyomino_first_prefix_reduction/proof.md).
Six of its subsets are excluded, leaving seven. Four of the seven branches
also have a unique complete first prefix. The finite-five square-cell
construction target remains open.

## Tile, normalization and scope

P is the unmarked 17-square disc whose unit-square lower corners at
y=0,1,2,3,4 have x coordinates 1..3, 0..3, 0..3, 2..4, 3..5 respectively.
It is the [Kaplan seed](../heesch_polyomino_euler_cnf/proof.md).
Its eight normalized D4 cell images are sorted lexicographically, and a
pose (i,x,y) means image i translated by (x,y). R has pose (3,0,0).
Normalization places the selected root in this position by a global
congruence. Pose indices are bookkeeping and do not mark the shape.

A packing is a finite collection of congruent closed P copies with
pairwise disjoint whole interiors. All real rotations, translations and
reflections are permitted. Cumulative prefixes U_0=R,U_1,U_2,U_3 extend
one another as collections of copies, satisfy U_(i-1) subset int(U_i),
and add only copies touching U_(i-1). The results impose no topology
conditions, hence apply both to Kaplan's disc-prefix Hc and final-hole Hh
conventions. See the [primary paper](https://arxiv.org/abs/2105.09438)
and [author dataset](https://cs.uwaterloo.ca/~csk/heesch/).

**Theorem.** Under these three-corona premises, every copy in U_1 has one
of the eight D4 orientations and an integer translation relative to R.
U_1 contains every specified copy of at least one of the seven census
subsets with IDs **1,25,50,72,96,133,134** in the previous
[patterns.json](../heesch_polyomino_first_prefix_reduction/patterns.json).
If it contains subset 1,25,50 or133, its entire first prefix is the
corresponding complete packing given below. The other three branches are only
proved integral here; their complete first-prefix enumeration is not asserted.

With three coronas alone, the theorem does not align the second or third
prefix. For a longer chain, re-rooting gives the inner-prefix corollary below.
Neither statement establishes four coronas, an exact Heesch number or a new record. The
existing 36-copy three-corona construction is a positive control, not a
new construction. The earlier finite upper bound is not improved here.

## The contact-interiority principle

Suppose B is a finite packing, D extends it as a collection of copies,
and C subset int(B). Any D copy Q touching C must already belong to B.
Indeed a touching point lies in int(B), and every neighborhood of a point
of Q contains interior points of Q. A sufficiently small neighborhood is
inside int(B). The finite union of the polygonal boundaries of the B copies has empty
interior. Consequently the interior of Q meets the interior of a B copy.
Packing disjointness forces that copy to be Q. In particular, if
B subset int(D), every such Q is interior in D.

This principle needs no angle, orientation, translation, disc or
edge-to-edge assumption. It also applies at a contact consisting of only
one point. In this contribution C is the union of a specified integer
subset of U_1, B=U_2 and D=U_3. Thus every actual D copy touching C is
interior in D. A D copy touching R already belongs to U_1, by the same
principle with C=R and B=U_1.

## Exact small clauses from arbitrary real packings

A Boolean variable z_Q states that a specified whole integer-positioned
copy Q belongs to D. Only finitely many variables needed by a sparse
certificate are introduced. Their integer positions are possible
forced corner owners, not a restriction on arbitrary other copies of D.

The [published isolated-gap lemma](../heesch_polyomino_corner_obstruction/proof.md)
uses a missing unit quadrant at an integer vertex whose two neighboring
quadrants are occupied. A strict surround fills that 90-degree sector.
The smallest angle of P is 90 degrees, so an actual owner has a convex
corner there, both rays align, and its translation is integral. Its
whole corresponding unit cell is owned. Straight, reentrant and interior
points cannot fit into the sector. This argument applies even if the
opposite quadrant is empty.

Every initial clause has one of four explicitly checked reasons:

* **Fixed cover.** At an isolated gap of C, at least one whole integer
  copy avoiding C must own the missing unit cell. The positive clause
  contains every such possible owner, found by a complete bounding-box
  translation enumeration over all eight images.
* **Conditional cover.** A specified Q touching C is interior in D whenever
  it occurs. An isolated gap of C union Q is therefore covered. The clause
  is -z_Q OR all complete cell owners avoiding C. Owners overlapping Q
  remain in this enlarged domain; whole-copy overlap clauses can remove
  them when z_Q is true. No genuine owner is omitted.
* **Whole-copy overlap.** Copies with an intersecting integer-cell
  footprint cannot both occur, giving -z_Q OR -z_T.
* **Interior pair.** The
  [237 prior pair obstructions](../heesch_polyomino_corner_obstruction/proof.md)
  forbid certain relative placements when both copies are interior in the
  final packing. Here each variable in such a clause must physically
  touch C; a fixed partner is already in C. The contact-interiority
  principle licenses exactly this use. The reader checks the prior
  obstruction library under D4 transformations and in both directions.
  Unrelated outer fillers are never presumed interior.

For integer-cell copies avoiding C, sharing a unit-cell vertex with C
is equivalent to closed geometric contact. The reader checks this
literal contact condition. It need not trust discovery's incoming-pose
catalogue, transported orientations, SAT variable numbering or full
candidate inventory. Positive cover clauses still require the entire
geometric owner list, including owners outside the sparse table: omission
of even one makes the certificate invalid.

The preceding statements prove the necessary direction: every real
three-corona packing induces a satisfying assignment of all geometrically
validated initial clauses. Additional real copies, fractional phases or
other final topology cannot repair a contradiction in those clauses.

## Six two-surround exclusions

For each fixed union C with ID32,33,60,61,63 or137, the sparse clauses
contradict whenever C subset int(B) and B subset int(D) for nested finite
P packings. This stronger statement does not require C to be the entire
first prefix, nor B or D to be actual coronas. Its application to three
coronas excludes six cases from the prior thirteen-subset theorem.

| ID | Sparse poses | Initial clauses | RUP additions |
| --- | --- | --- | --- |
| 32 | 18 | 19 | 1 |
| 33 | 115 | 141 | 6 |
| 60 | 168 | 201 | 10 |
| 61 | 59 | 65 | 4 |
| 63 | 65 | 94 | 9 |
| 137 | 155 | 156 | 2 |

These six proofs use 676 necessary clauses and 32 forward RUP additions.
The completely closed root-halo branch32, which had a positive one-surround
fixture, is among them. The contradiction does not negate that earlier
one-surround witness; it excludes two further strict surrounds.

## Forced copies and integer halo coverage

Additional certificates entail the following exact copies whenever their
specified subset C has two further strict surrounds. Each listed copy
also touches R, so under the three-corona hypothesis it belongs to U_1.

| Subset | Forced additional poses |
| --- | --- |
| 1 | `(6,-4,2)` |
| 25 | `(3,-3,3), (7,-6,0)` |
| 50 | `(3,3,-3), (4,0,-6), (6,-4,2)` |
| 96 | `(6,-4,2)` |
| 133 | `(2,2,-4)` |
| 134 | `(3,2,5)` |

For 1,25,50 and133, these copies together with C cover the entire
radius-one Chebyshev unit-cell halo of R. The reader verifies that they
form a disc, avoid whole-copy overlaps, and all touch R. Their exact complete
prefixes are in [expected.json](expected.json). They respectively contain
7,7,7 and7 copies, including R. The prefix for133 equals the first prefix
of the independently rechecked older three-corona positive control.

For the three remaining branches72,96,134, the halo certificates entail a
positive disjunction for each unit cell of the root halo not in C.
Every copy in that conclusion covers the stated unit cell and touches R.
This proves that actual integer first-layer copies cover that cell;
it does not force a particular owner. There are 15 cell certificates,
covering all 4,5 and6 missing cells of the respective fixed subsets.

Choose the actual owners certified by these disjunctions. Together with
the fixed and forced copies, they give an integer subpacking J of U_1
covering the whole unit halo of R. Thus R subset int(J). Any further U_1
copy must touch R by the corona convention. The contact-interiority
principle applied to R and J says it must already belong to J. Therefore
U_1=J as a collection of copies, and every first-prefix copy is integral.
The same argument proves uniqueness in the four branches with forced
complete prefixes.

This is why coverage of the full root halo matters. An integral partial
subset with a positive surround would not alone rule out additional real
first-layer contacts. Here completeness of the halo rules them out.

## Re-rooting discretizes every prefix with two outer layers remaining

**Corollary.** If H >= 3 complete coronas exist under the same unrestricted
topology and real-motion premises, every copy of U_k is on the root's unit
square grid for 0 <= k <= H-2. Thus only the final two prefixes can still
contain fractional translations or orientations outside D4.

We first justify re-rooting without assuming that its new prefixes are discs.
Let A be any copy in U_j with j <= H-3, and consider the finite contact graph
of the copies of U_(j+3). Vertices are whole copies and an edge means nonempty
closed contact. Let F_r be the family of copies at graph distance at most r
from A, and N_r its closed union, for r=0,1,2,3. The contact-interiority
principle puts F_r in U_(j+r) as a subfamily, inductively: all copies touching a subfamily of
U_(j+r-1) already occur in U_(j+r), because the latter strictly surrounds it.
Moreover N_(r-1) is strictly inside N_r. Indeed it is compact and inside
int(U_(j+r)); every copy in U_(j+r) not touching it has positive distance
from it. Finitely many such distances have a positive minimum, so a small
neighborhood of N_(r-1) is covered entirely by copies of N_r. Empty sets of
noncontacting copies impose no additional restriction. New N_r copies touch
N_(r-1) by their graph distance. These are three admissible coronas about A,
with arbitrary topology, so the theorem puts every neighbor of A on A's grid.

Now induct on k <= H-2. The root is integral. Each new copy Q of U_k touches
some A in U_(k-1). Since k-1 <= H-3, A has the three re-rooted coronas just
constructed. The theorem therefore puts Q on A's grid. By induction A is
already on the root's grid; integer translations and D4 orientations compose,
so Q is on it as well. Older copies retain the induction hypothesis.

Consequently, an independently established finite grid-disc upper bound G
for this tile would give the real-motion bound Hc <= Hh <= G+2: if H >= G+3,
U_(G+1) would be a grid-disc prefix, contradicting that bound. This conditional
transfer uses a separately certified grid bound; this contribution does not
import an unchecked fourth-corona UNSAT verdict or improve the numerical
upper bound81. A general grid bound with holes allowed at every stage would
give the same transfer without any prefix topology assumption.

## Proof certificate and reproducibility

[check.py](check.py) uses only Python's standard library and pins the
bytes of the prior geometry implementation, pair library, positive fixture
and thirteen-subset inputs and checker. It replays that entire prior checker
before checking this contribution. New clauses are checked against literal
quarter-sector geometry, whole copies, complete independent bounding-box
owner inventories and inverse centered D4 pair transformations. Native
search's vertex anchoring and compiled pair classes are not used.

[certificates.json](certificates.json) stores small sufficient subformulas
and forward RUP traces. For each addition L, the reader assumes the
negation of all literals in L and performs naive exact unit propagation
on the preceding clauses. Contradictions end in the empty clause.
Entailment proofs end in their exact positive conclusion.

To obtain an entailment certificate from discovery, negate its proposed
positive conclusion G. A checked refutation of F together with these
negative unit assumptions is then lifted: replace each learned L by
L OR G, omit tautologies, and discard the negative input assumptions.
Under the negation of L OR G the prior lifted clauses reduce to the original
ones, so the forward RUP condition is preserved. The published reader
checks the resulting proof directly; it trusts no deduction from the
solver's verdict, assumption handling or preprocessing.

From the repository root, run:

```sh
python3 -B heesch_polyomino_third_prefix_reduction/check.py --expected heesch_polyomino_third_prefix_reduction/expected.json
python3 -O -B heesch_polyomino_third_prefix_reduction/check.py --expected heesch_polyomino_third_prefix_reduction/expected.json
python3 -B heesch_polyomino_third_prefix_reduction/check.py --controls
```

The first two commands must produce identical checked JSON. The third
rejects eight malformed certificate controls. All checks use explicit
exceptions and retain their meaning under Python optimization. CPython3.11+
is sufficient; the reported discovery/check environment is CPython3.11.2,
PySAT1.8.dev24/Glucose4 and drat-trim revision
2e3b2dc0ecf938addbd779d42877b6ed69d9a985. Solver threads are one;
native calls use a 10000-conflict budget, a 55-second process budget,
10000-candidate and 2000000-clause guards, and 30-second DRAT checks.
No UNKNOWN, guard, timeout or partial run is used as a negative result.
Raw native CNFs, DRAT deletion logs and full candidate corpora remain
private scratch; the compact geometric proofs are sufficient to reproduce
the stated lemmas. The combined evidence has 2045 necessary input clauses and
112 forward RUP additions across the six exclusions and twenty-four implications.

The written real-motion reduction and existing isolated-gap/pair lemmas
remain mathematical trust boundaries; the new result is not formalized
and has no independently requested or obtained reviewer verdict.
Same-author independent geometric checking is computational validation,
not independent peer review. The complete census of first-prefix integral
completions, certified grid upper bounds for the transferred problem, and the
final two real-motion layers remain concrete next frontiers.

## Literature and complementary work

The seven-subset statement depends on the previous thirteen-subset theorem.
The small-clause statements additionally use the prior isolated-gap and
interior-pair lemmas. The geometry reader and positive fixture come from
[the placement-sensitive B comparison](../heesch_polyomino_star_b_obstruction/proof.md);
its unrelated star exclusions are not premises of the new clause checks.
The earlier fixed-disc half-grid theorem is a transitive premise of the
thirteen-subset reduction, not a new deep-corona discretization here.

The method also builds on the complementary
[T214 prefix rigidity](../heesch_polyiamond_second_prefix_rigidity/proof.md)
and [sparse alternate-prefix obstruction](../heesch_polyiamond_alternate_fourth/proof.md)
of six-heesch-2. Those tile-specific results are not P17 premises.
The [curved-disc four-corona work](../heesch_trapezoid_four_coronas/proof.md)
of six-heesch-3 concerns a different shape family. Their published proofs
and durable reports were read; their checkers are not claimed replayed here.
The more recent [six-copy T214 localization](../heesch_polyiamond_six_copy_obstruction/proof.md),
[three-copy T214 forced-filler obstruction](../heesch_polyiamond_forced_pair/proof.md)
and [four-copy curved-disc obstruction](../heesch_trapezoid_four_copy_obstruction/proof.md)
retain the same distinction between first-extension occurrence and
second-extension interiority. Their source proofs were read in this resumed pass;
they supply complementary context, not premises for P17.
The broader unmarked-polyform finite-five threshold is already attained by
[Mann's known hexapillar](https://faculty.washington.edu/cemann/Heesch.pdf).
This contribution retains the specifically square-cell polyomino direction
and asserts no priority for a literature record.
