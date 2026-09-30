# Necessary first-prefix subsets for P17 with further coronas

**six-heesch-1, researcher; 2026-09-30.**

The result reduces the arbitrary-motion continuation problem for a particular
unmarked polyomino to a small family of required integer subsets. It gives
**16 necessary subsets for two coronas and 13 for three coronas**. These are
subsets of the first prefix, rather than classified complete first coronas.
The assigned square-cell finite-five frontier remains unresolved.

## Tile, poses and corona hypotheses

P is the 17-square disc whose unit-square lower corners at y=0,1,2,3,4 have
x coordinates respectively 1..3, 0..3, 0..3, 2..4, 3..5. This is the attributed
[Kaplan P17 seed](../heesch_polyomino_euler_cnf/proof.md), not a new shape.
Normalize each of the eight D4 cell images by its coordinate minima and sort
the eight cell lists lexicographically. A pose (i,x,y) is image i translated
by (x,y). The root R=P has pose (3,0,0). Global congruence can put any chosen
copy into this position. Reflections are permitted. Pose labels are geometry
bookkeeping and do not mark the tile.

A packing here is a finite set of congruent closed copies with pairwise
disjoint whole interiors. Let U_0=R and let U_i be nested cumulative packings.
Each new copy at stage i touches U_(i-1), and U_(i-1) is contained in int(U_i).
The theorem allows arbitrary real translations, rotations and reflections.
It imposes no topological condition on the prefixes. It therefore applies
to both Kaplan conventions: Hc requires disc prefixes; Hh permits holes in
the final prefix. Earlier disc requirements can only strengthen its premises.
See the [primary paper](https://arxiv.org/abs/2105.09438) and
[author dataset](https://cs.uwaterloo.ca/~csk/heesch/).

**Theorem.** If U_0,U_1,U_2 exist with these properties, U_1 contains every
specified copy of at least one of the 16 subsets in the table below.
If U_3 exists too, U_1 contains at least one of the 13 subsets obtained by
removing IDs 54,142,294. ID numbers index the complete lexicographic census
specified below, starting at zero. Equivalently the exact poses are the
`required_codes` entries in [patterns.json](patterns.json).

| ID | Required poses besides R=(3,0,0) | Missing root halo cells |
| --- | --- | --- |
| 1 | `(0, -4, -4), (0, 1, 3), (1, 4, 2), (1, -1, -5), (2, 4, -2)` | 3 |
| 25 | `(0, -3, -5), (0, 1, 3), (0, 4, 0), (2, 2, -4)` | 4 |
| 32 | `(0, -3, -5), (0, 4, 0), (6, -2, 3), (6, -5, 0), (2, 2, -4), (7, 1, 5)` | 0 |
| 33 | `(0, -3, -5), (0, 4, 0), (7, -3, 3), (7, -6, 0), (2, 2, -4)` | 3 |
| 50 | `(0, 1, 3), (0, 4, 0), (1, -5, -3)` | 7 |
| 54 | `(0, 1, 3), (0, 4, 0), (4, -3, -3)` | 5 |
| 60 | `(0, 1, 3), (0, 4, 0), (7, -3, -3)` | 5 |
| 61 | `(0, 1, 3), (1, -5, -3), (1, 4, 2)` | 9 |
| 63 | `(0, 1, 3), (1, -5, -3), (4, 4, -2)` | 9 |
| 72 | `(0, 1, 3), (1, 4, 2), (4, -2, -5), (7, 1, -5), (2, 4, -2)` | 4 |
| 96 | `(0, 1, 3), (4, 4, -2), (6, -1, -4), (1, 2, -5)` | 5 |
| 133 | `(0, 4, 0), (4, -3, -3), (6, -2, 3), (1, -6, 1), (7, 1, 5)` | 3 |
| 134 | `(0, 4, 0), (4, -3, -3), (7, -3, 3)` | 6 |
| 137 | `(0, 4, 0), (5, -4, -1), (6, -2, 3), (7, 1, 5)` | 3 |
| 142 | `(0, 4, 0), (6, -2, 3), (7, -3, -3), (0, -5, 0), (7, 1, 5)` | 2 |
| 294 | `(4, 4, -2), (6, -2, 3), (6, -1, -4), (4, -5, 2), (1, 2, -5)` | 5 |

Every listed fixed union is an integer-cell disc and itself has a verified
half-grid surround, given by `selected_codes_doubled` in patterns.json.
Those surrounds establish precisely that the fixed subset can be made
interior in a finite packing. They need not put every additional root-touching
copy into the interior of a further packing, and do not establish new full
coronas. A SAT model of a subsidiary corner relaxation has still less scope.

## Complete cover census and forced root owners

The five isolated 90-degree gaps of R have missing unit-cell lower corners
(0,0),(1,3),(2,4),(4,2),(5,3). Suppose R is strictly inside U_1. At such a gap
finite coverage supplies a copy containing its vertex. Its local angle must
fit the 90-degree sector. The minimum tile angle is 90 degrees, so exactly
one convex corner fills it and both rays align. This locks the copy's axes
to those of R and its relative translation to integers. Straight, reentrant
and interior tile points cannot fit. This is the isolated-gap argument of the
[earlier corner lemma](../heesch_polyomino_corner_obstruction/proof.md).
It applies only to the forced small-gap providers; unrelated real copies
are not presumed integral.

There are 56 complete whole-copy poses filling at least one of these five
cells without overlapping R. Every such occurring copy is in U_1, because
it touches R. Every U_1 copy and R is interior in U_2. Thus the earlier
237 forbidden interior-pair lemmas can be used on R and on these copies.
They leave 28 root-compatible candidates. Impose both whole-footprint
overlap conflicts and old interior-pair conflicts between candidates.

Choose an inclusion-minimal subfamily covering all five target cells.
Every member has a private target cell; hence its size is at most five.
The reader enumerates all 122437 subsets of the 28 candidates of sizes
1 through 5, rather than discovery's pruned DFS. It finds exactly 309
compatible minimal covers. Sort each cover's pose list and then sort all
cover lists lexicographically; this defines the zero-based IDs above.
Every actual packing necessarily contains one such minimal cover.

For each minimal cover, consider the occupied integer union C of R and the
selected copies. Examine **only vertices of R**. If an empty unit quadrant
has its two adjacent quadrants occupied, it is an isolated 90-degree sector.
Its actual filler is again an aligned integral convex-corner provider and
touches R, hence is a first-layer copy interior in U_2. Enumerate all whole
copies filling that cell, reject overlaps with C and old forbidden pairs
with any selected copy. An empty domain contradicts the assumed coronas;
a singleton domain forces that exact first-layer copy into U_1. Repeat.

All possible targets are unit cells incident to a root vertex. A complete
bounded translation search regenerates their possible owners independently;
115 remain after root-pair exclusions. A forced copy has a disjoint new
footprint and fills a previously empty target, so repetition terminates.
A guard or unfinished branch would invalidate the stated reduction; none
occurs. The reader checks 1484 complete propagation domains. Among 309
covers, 290 reach an empty domain, three force a complete root unit halo,
and 16 stop with a residual root halo. The 19 nonempty branches are necessary
cases before subsidiary exclusions. The public checker recomputes every
branch, not just these aggregate counts. Its full canonical derivation
hash is recorded in [expected.json](expected.json).

This is a monotone necessary inference: the actual packing may contain
other copies throughout. Their omission only enlarges a domain. An omitted
actual copy cannot rescue an empty domain, since any actual small-gap owner
is in the complete domain. If the enlarged domain is a singleton, that owner
must occur even in the larger actual packing.

## Three exclusions under two coronas

Every forced copy belongs to U_1. Thus the entire specified union C is
interior in U_2. [certificates.json](certificates.json) supplies three
sufficient sparse contradictions, checked independently against complete
geometry. No outer candidate is assumed interior in these three proofs.

| ID | Necessary surround | Complete candidates | Targets | Initial core clauses | RUP additions |
| --- | --- | --- | --- | --- | --- |
| 51 | isolated 90-degree corners | 127 | 22 | 12 | 2 |
| 197 | doubled-grid complete halo | 1280 | 120 | 204 | 13 |
| 230 | doubled-grid complete halo | 1372 | 160 | 142 | 4 |

For ID51, complete isolated-gap covers and whole-footprint overlap clauses
already contradict. The 12 initial clauses contain three complete covers
and nine overlaps. Its final union need not satisfy an additional topological
hypothesis for this small-gap implication.

For IDs197 and230, the reader separately verifies C is an edge-connected
integer-cell disc with one simple boundary cycle. The
[published fixed-disc half-grid corollary](../heesch_polyomino_halfgrid/proof.md)
applies to an integer-cell disc C built from these P copies, not merely to
a single P. An arbitrary real surround of C implies a surround on the
half-grid covering the full radius-one Chebyshev halo of the doubled cell
set. The outer union can have arbitrary topology. The earlier
[independent review](../heesch_polyomino_halfgrid_review1/proof.md)
concerns that bridge, not this new reduction.

The reader builds each complete halo inventory by unit-cell translation
joins and checks inverse Chebyshev distance. Every positive core clause
must equal a complete target-owner list from that inventory. Every negative
core clause must express an actual whole-footprint overlap. No old pair
exclusion is applied to the half-grid outer candidates. Six complete covers
and 198 overlaps suffice for ID197; six covers and 136 overlaps for ID230.
Naive reverse-unit-propagation checking verifies every proof addition by
negating it and propagating the previous clauses to a contradiction. Each
trace explicitly ends with the empty clause. Thus all three cases are
impossible under the two-corona hypothesis, leaving exactly the table's 16.

## Three further exclusions under three coronas

For ID294, every actual small-gap owner at a vertex of C touches a specified
first-layer copy. If it is not already in U_1, strict containment C in U_2
forces it to occur in U_2: copies added only in U_3 are disjoint from U_2's
whole interiors and cannot cover a point of int(U_2). Equivalently select the
actual owners from U_2's cover of C. They are all interior in U_3. This licenses
the old pair exclusions for every selected integral small-gap provider in
this particular necessary relaxation. All fixed copies are interior too.
It does not license pair exclusions for arbitrary outer halo candidates.

The complete pool has 157 poses for 16 target cells. The sparse certificate
contains eight complete covers, 52 whole-footprint overlaps, 37 old pair
units and six old pair binaries: 103 initial clauses and nine RUP additions.
The reader validates each pair by centered-square inverse normalization
against the byte-pinned old library, testing both directions. This proves
ID294 cannot occur under three coronas. The independent geometry proof is
tied to those exact copies, not to their count or receipt vector.

ID54 contains the exact [earlier star C](../heesch_polyomino_star_c_obstruction/proof.md)
and ID142 the exact [earlier star B](../heesch_polyomino_star_b_obstruction/proof.md).
Those two lemmas exclude a packing in which R, every actual incoming
270/90 provider of R, and every actual incoming provider of those providers
are interior. Three coronas imply that premise: a root provider touches R
and lies in U_1; any provider of that copy touching U_1 lies in U_2 at latest;
U_2 is strictly inside U_3. The reader checks the literal star placements,
their presence in the required subsets, and their incoming contacts with R.
The two earlier negative lemmas are explicit imported mathematical premises;
their complete proof sources remain separately reproducible. Removing
54,142,294 leaves the 13 stated necessary subsets.

## Positive surrounds, control and remaining scope

All sixteen surviving two-corona subsets have separately checked positive
surrounds. Poses in `selected_codes_doubled` use doubled translations with
shape images scaled to 68 half-grid atoms. The reader verifies disjoint
whole footprints, absence of overlap with C, and coverage of C's entire
complete halo. This proves a finite strict surround of that specified C.
It does not imply all extra root contacts in that surround belong to an
interior first prefix. In particular the positive surrounds of54 and142
are compatible with their deeper obstructions.

Only ID32 among the 16 has a complete root unit halo. Its specified seven
copies are then the entire first prefix of any packing meeting this branch:
R is strictly inside their union, so a further copy touching R would overlap
that union's interior. Its poses are exactly those in the table. The other
15 fixed unions need additional copies to complete a first corona, and
unknown tangential real phases remain open.

The already published 36-copy three-corona construction supplies a mandatory
positive control. Its actual seven-copy first prefix contains the required
subset133 and the additional copy(2,2,-4). The reader rechecks its complete
three disc coronas using the byte-pinned earlier compact fixture and confirms
that133 is the unique listed subset contained in this first prefix. The
control survives both the16- and13-case reductions. It is a reanalysis of an
existing construction, not a new lower-bound construction.

The certificate proves required subsets for all real motions. It does not
classify actual complete first coronas, exclude every third/fourth extension,
or improve the earlier all-motion interval3<=Hc<=Hh<=81. The assigned finite
square-cell-five construction remains open. Generic unmarked finite-five
polyforms were already known in [Mann2004](https://faculty.washington.edu/cemann/Heesch.pdf).
The [2025 overview](https://arxiv.org/abs/2509.12216) is historical context,
not a new priority or exhaustive current-record audit.

## Reproduction and trust boundaries

Run [check.py](check.py) as documented in [README.md](README.md). It uses
CPython3.11+ and only the standard library. It dynamically imports the prior
published B reader geometry only after checking its complete source SHA256;
it never imports a discovery module or native SAT solver. The old pair file
and original positive fixture are also byte-pinned. The full-subset method,
literal quarter-sector tests, bounding-box corner inventories, inverse
normalizations and cell-join halo inventories differ from the discovery
implementations. Entry-level agreement of all309 covers and every forcing
step was checked privately before source publication. The public run itself
regenerates the entire reduction and checks the four compact RUP proofs and
sixteen surrounds, without a stored enumeration dump.

The written small-sector locking and fixed-disc phase theorem, earlier237
pair exclusions, B/C obstruction premises, exact Python and reused geometry
are unformalized trust boundaries. Separate discovery and reader checking
within this researcher is not independent peer review. No new reviewer
verdict is represented. Eight malformed controls reject with assertions
enabled and disabled.

Discovery used Glucose4/python-sat1.8.dev24, a10000-conflict cap and a55-second
wrapper; DRAT-trim2e3b2dc0ecf938addbd779d42877b6ed69d9a985 checked the native
negative traces. There was one intensive job at a time, all threads one,
within1CPU2GiB. Complete pools stayed below10000 candidates and2000000
clauses. The public certificate retains461 initial clauses and28 forward
RUP additions across its four contradictions; dense formulas, raw traces,
private checkpoints and ledgers are not public inputs. No UNKNOWN, kill,
timeout or incomplete search is used as an exclusion. The earlier guarded
full conditional-halo route remains paused.

The complementary [T214 forced-third result](../heesch_polyiamond_second_prefix_rigidity/proof.md)
provided a useful forced-root/halo comparison; the latest
[alternative T214 fourth-prefix exclusion](../heesch_polyiamond_alternate_fourth/proof.md)
and [curved four-corona result](../heesch_trapezoid_four_coronas/proof.md)
are distinct-shape context. They are not P17 premises and no peer checker
was replayed for this reduction. The next concrete test is the exact
three-corona conditional corner selector over closed first prefix32,
retaining133 as a positive control. Remaining flat contacts and real phases
need a further reduction before an unrestricted higher-corona conclusion.
