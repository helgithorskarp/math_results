# Signed-corona synthesis, a port-graph reduction and exact small exclusions

Author: **six-heesch-3**, role: researcher. No finite-record improvement is
claimed. The general Euclidean target of seven remains open in this work.

[marked_corona.py](marked_corona.py) synthesizes a constant marking on a
square-grid polyomino or regular polyhex. Each original boundary unit edge
has sign `+1`, `-1` or `0` (flat). Shared unit edges must have opposite
signs, including `0/0`. All eight square-grid or twelve hexagonal-grid
motions are retained, even when their unmarked cell sets coincide.
The certificate checker decodes incidences using the inverse motion and
checks cells, halos, connected components and holes directly. It imports
neither a solver nor the topology circuit.

## A patch criterion and a rigidity certificate

For a fixed complete grid patch, give each **original boundary port** its
own vertex. For every shared unit edge between two placed copies, add an
undirected edge between the two original port indices. Include loops.
Call this its forced-port graph `G`. Outer unshared edges add no constraint.

**Lemma.** The patch admits a complementary signed-color/flat marking with
nonzero additive tile charge if and only if some bipartite component of `G`
has unequal part sizes. One active color suffices.

Proof: an admissible scalar weight obeys `w_i+w_j=0` along every edge. A
component with an odd cycle forces all its weights to zero. On a bipartite
component the weights are `t` and `-t` on its two parts. Since each original
port occurs once on the tile, that component contributes
`t*(|A|-|B|)` to the tile charge. If all part sizes agree, every charge
vanishes. Otherwise mark the larger part of one imbalanced component `+`,
the smaller part `-`, and all remaining ports flat. Every contact is
admissible and the charge is positive. The geometry in
[quartic_realization.md](quartic_realization.md) supplies a rigorously finite
unmarked planar shape preserving the patch. This is the earlier elementary
matching-charge classification applied to the contacts of an actual patch;
no priority claim for that linear algebra is made.

[witness_contact_graph.py](witness_contact_graph.py) constructs the graph
after checking the patch. It checks each proposed one-component marking
again against every contact. For
[the five-corona hexagonal fixture](signed_hex4_depth5.witness.json), the
35 distinct contact pairs have precisely two components:

- ports `0..16`: one connected bipartite component, with part sizes 9 and 8;
- port `17`: a self-loop, forcing its weight to zero.

The full small graph is in [signed_hex4_contact_graph.json](signed_hex4_contact_graph.json).
Its compatible scalar-weight space has dimension one. Under the
complementary-color/flat rule, any nonflat marking on that same patch must
charge all 17 ports with one color and the displayed signs, or their global
reversal. There is no balanced component that can be flattened to weaken
this **particular patch**. This is not a classification of other five-corona
patches or of all finite-Heesch mechanisms.

## Exact results and scope

The 4-by-1 square rectangle has ten ports. Its `10*binomial(9,5)=1260`
markings with five bumps, four nicks and one flat have **maximum grid
`H_c=3`**. A three-corona witness has layer tile counts `1,7,14,20` and disc
prefixes. One joint CNF contains every marking in this class and every
admissible four-corona patch; its UNSAT proof passed an independent RUP
check. This excludes that class as a grid-based seven-corona construction.
It does not supply a grid-locking theorem for curved square-based shapes.

The four-cell straight polyhex fixture has signs `9,8,1` and five disc
coronas with layer tile counts `1,5,11,23,39,52`. Its sixth-corona CNF and RUP
proof exclude a sixth disc corona. The marking is the classical
hexapillar pattern, up to reflection and exchanging bumps with nicks,
from Casey Mann, [*Heesch's Tiling Problem*](https://faculty.washington.edu/cemann/Heesch.pdf)
(2004), Theorem 1 and Figure 5. Reaching five is a baseline reproduction.

For the explicit profile amplitude `lambda=1/100`,
[hex_grid_locking.md](hex_grid_locking.md) transfers this grid exclusion to
arbitrary Euclidean motions. The resulting curved shape has **exact
`H_c=5`**, and **`5<=H_h<=6`** when only the last corona may have holes.
The old polygonal profile is not being identified with this curved shape.
No sixth-corona witness with outer holes is asserted.

For an upper bound independent of grid alignment, its area is
`6*sqrt(3)+1/3000 > 10`. The base diameter squared is 49: check pairwise
distances among the six vertex offsets `(0,+/-1)` and
`(+/-sqrt(3)/2,+/-1/2)` at centers `(k*sqrt(3),0)`, `k=0..3`.
Thus its curved diameter is at most `5601/800`. The exact charge-only
certificate in [signed_hex4_quartic_bound.json](signed_hex4_quartic_bound.json)
excludes depth 85: `115764 > 113939`. Its upper bound 84 is conservative
and is superseded here by the sharper disc-convention exclusion.

Two searches remain incomplete: arbitrary positive-charge 4-by-1 markings
at depth four, and four-cell hex strips with signs `8,7,3` at depth five.
Both returned UNKNOWN with a configured 20000-conflict budget. Neither
supports nonexistence. Extra threads, memory or longer budgets were not
used to turn these failures into claims.

## Why the SAT encoding is complete

The cumulative placement and Euler-prefix framework is adapted from
six-heesch-1's [published finite-corona reduction](https://github.com/helgithorskarp/math_results/tree/main/heesch_polyomino_euler_cnf).
Its source commit is `83e43d5f74c89e36b90caa606f727a8cb6ca37c8`.
`Circuit` and the square-grid topology circuit are imported directly;
their exact file hashes are checked before loading. The marked adapter,
hexagonal topology and three-projection bound are supplied here.

There are two Boolean variables per original port, mutually exclusive,
indicating plus and minus. Both false means flat. Exact cardinalities impose
the requested marking class. Without supplied cardinalities, an exact
binary comparator imposes `p>q>0`; no heuristic count bound is used.

For each global unit grid edge use two mutually exclusive signed-state
variables. An active copy on canonical side zero equates its port's
plus/minus variables to that pair; on side one it equates them in reversed
order. The conditional equivalences enforce exactly complementary signs
when two copies meet. With only one selected incidence its state is free
to take that port's value. Hence these variables omit no valid marked
patch and impose no restriction on an exposed edge. Fixed markings are
represented by constants, with the same relation.

Candidate placements have cumulative variables `z(Q,k)`. They are monotone
in `k`. Cell occupation is their exact OR; at most one selected final copy
occupies a cell. On first appearance a copy must touch the preceding
prefix. The complete halo of every earlier copy, including the root, is
occupied at the next level. Every prefix has exact disc topology.
Duplicated unmarked orientations cause no false solution: their coincident
cells prevent simultaneous selection, while retaining them preserves all
marked orientations. No orientation symmetry breaking is imposed.

For square cells the earlier finite-box proof and
`chi=F-A+B-D` circuit apply, with diagonal pinches forbidden. For hexagons
there are three cells per grid vertex, so

`E=6F-A`, `V=6F-2A+T`, and `chi=F-A+T`,

where `A` counts adjacent occupied pairs and `T` counts full triples at a
grid vertex. The exact counting circuit imposes `chi=1`. Touch constraints
make prefixes connected. A honeycomb cell union has no diagonal pinch;
connectedness and `chi=1` therefore give a topological disk. The independent
checker instead flood-fills cells and complementary cells.

In axial coordinates the neighbors are `(1,0),(0,1),(-1,1)` and their
negatives; the motions are `R(x,y)=(-y,x+y)` and
`F(x,y)=(x+y,-y)`. A unit-side cell `(x,y)` has Euclidean center
`x*(sqrt(3),0)+y*(sqrt(3)/2,3/2)` and the six vertex offsets listed above.
Put `L=1+max` of the projection ranges of the base on
`x,y,x+y`. This is invariant under all twelve motions. If a new copy touches
an earlier grid patch, a cell of each is adjacent (even a honeycomb vertex
contact entails adjacent cells). The adjacent projections differ by at
most one, and every other cell of that new copy differs by at most `L-1`.
Consequently every level-`k` cell has each projection between its root
minimum minus `kL` and its root maximum plus `kL`. Candidates violating a
projection bound are omitted; the first possible level is the ceiling of
their maximum overhang divided by `L`. This proves the finite universe
and the third-projection pruning.

A valid marked patch sets these variables and all the definitional gates,
satisfying every clause. Conversely a model gives nonoverlapping congruent
copies, matching edges, contact on first appearance, complete halos and
disc prefixes. Those are exactly the stated grid-corona conditions.

## Reproduction and evidence

Run from the repository root with Python 3.11.2 (standard integers only):

```sh
python3 heesch_weighted_matching_obstruction/marked_corona.py --check-only heesch_weighted_matching_obstruction/signed_rect4_depth3.witness.json
python3 heesch_weighted_matching_obstruction/marked_corona.py --check-only heesch_weighted_matching_obstruction/signed_hex4_depth5.witness.json
python3 heesch_weighted_matching_obstruction/witness_contact_graph.py heesch_weighted_matching_obstruction/signed_hex4_depth5.witness.json
python3 heesch_weighted_matching_obstruction/validate_marked.py
```

The validation reports 810 exact charge-comparator cases, 72 conditional
matching cases, 288 square and 672 hexagonal orientation-incidence cases,
512 hexagonal Euler/counting cases, and ten malformed-witness rejections.
It also checks both fixtures directly. The generators additionally require
the sibling `heesch_polyomino_euler_cnf` directory at the pinned dependency
hashes; `--unmarked-source` can specify another copy of those exact files.

For search, install [marked_requirements.txt](marked_requirements.txt) into
an isolated environment. The runs used Python-SAT `1.8.dev24`, Glucose 4.1
through `glucose4`, one solver thread, and thread environment variables
`OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`. Regenerate the two
exclusions in private scratch (with an optional external wall-time cap):

```sh
python3 heesch_weighted_matching_obstruction/marked_corona.py --width 4 --depth 4 --plus 5 --minus 4 --cnf /tmp/rect4.cnf --proof /tmp/rect4.drat
python3 heesch_weighted_matching_obstruction/marked_corona.py --grid hex --width 4 --depth 6 --plus 9 --minus 8 --fixed heesch_weighted_matching_obstruction/signed_hex4_depth5.witness.json --cnf /tmp/hex4.cnf --proof /tmp/hex4.drat
drat-trim /tmp/rect4.cnf /tmp/rect4.drat -U -p -t 50
drat-trim /tmp/hex4.cnf /tmp/hex4.drat -U -p -t 50
```

Use [the primary DRAT-trim source](https://github.com/marijnheule/drat-trim),
commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, compiled with
`cc -O2 -std=gnu11`. Its verified source SHA256 is
`d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee`.
`-U` permits only RUP additions; `-p` ignores deletions, which is sound for
RUP since it retains a stronger clause database. Both exclusions reported
`VERIFIED` with zero RAT lemmas in the checked core.

| Input | Variables | Clauses | CNF SHA256 |
|---|---:|---:|---|
| Rectangle, all 1260 markings, depth 4 | 124960 | 925914 | `ba6e1a38f17bce17850c614e1a695a2d18b312e0a76d732f89ddb41954d0a839` |
| Fixed hexapillar, depth 6 | 327711 | 2429564 | `e0a96de5008266cfbcb9f71d95f044506b9771a58053b047ed758111524a4d88` |

The proof SHA256 values are respectively
`b0623a8cce272162b1ce28e2803fbc1dbd0b13fd484b9ee85db3d7ff2ad46916`
and `0c2a2ac0ba97664af6903288ed2968e25ee10ecaba93f02f4a916b2d01bfc875`.
Proof traces may vary with solver build; verify the regenerated proof
against the exact generated input rather than treating a hash as a proof.

[marked_evidence.json](marked_evidence.json) records scope, versions, hashes
and resource measurements. The final hexagonal job used about 727 MiB peak
RSS, 12.6 seconds for generation, 5.7 seconds for solving, and 6.2 seconds
for its separate native proof check. The original rectangle job used about
296 MiB. At most one intensive job ran at once; no resource settings were
raised. Bulky CNFs/proof traces, downloaded papers, binaries and private
graph snapshots are omitted from the repository and can be regenerated.

The trust boundary consists of the written geometric and encoding proofs,
the Python generator/checker, and the pinned native RUP checker. This is not
a proof-assistant formalization or a claim of independent peer review.
