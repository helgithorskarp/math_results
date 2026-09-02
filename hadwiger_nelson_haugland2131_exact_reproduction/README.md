# Exact reconstruction of Haugland's 2,131-vertex graph

## Result and scope

This directory independently reconstructs the graph in Jan Kristian Haugland,
*A Moser-spindle-free 5-chromatic unit distance graph on 2131 vertices in the
plane*, [arXiv:2608.04542v2](https://arxiv.org/abs/2608.04542v2).  Starting
from the 231 paths in Appendix A, the checker obtains

```text
G1:  740 vertices,  3,985 declared unit edges
G2: 1,066 vertices,  6,264 declared unit edges
G3: 2,131 vertices, 12,530 declared unit edges
```

It certifies the exact declared unit edges, a proper five-colouring, and the
absence of a Moser-spindle subgraph.  It also exactly replays the geometric
forcing bridge from the 740-vertex endpoint gadget to `G3`.  The remaining
hard statement—that the gadget endpoints differ in every four-colouring—is
encoded reproducibly, but no completed DRAT refutation is included in this
commit.  Thus the independent result here is an exact geometry/upper-bound
and structural reproduction; the paper's lower bound `chi(G3) >= 5` remains
outside the certified scope until the pending SAT proof finishes.

This is a reproduction of a known construction, not a smaller graph: it does
not improve the 509-vertex record or the bounds `5 <= chi(R^2) <= 7`.
Haugland's revised paper also records a smaller 1,441-vertex
Moser-spindle-free construction of Heule, so no Moser-spindle-free size record
is claimed here.

The certificate treats a unit-distance graph in the usual non-strict sense:
every declared edge is proved to have length one.  It does not certify that
the declared edge list contains every unit-distance pair among the points.
Thus the exact claims concern the committed 12,530-edge graph, which has the
same vertex and edge counts as Haugland's `G3`.

## Exact geometry

Let `zeta = exp(pi*i/42)`, a primitive 84th root of unity.  All coordinates
through `G2` lie in the degree-24 field `Q(zeta)`.  The final rotation adds
only `sqrt(5)`, so `G3` is represented as a quadratic extension of that field.
`reconstruct.py` uses SymPy's exact algebraic field for `Q(zeta)` and a small
explicit pair representation `a + b*sqrt(5)` for the extension.  It checks:

- all 84 generating vectors have squared norm exactly one;
- every Appendix A path ends exactly at `(0, sqrt(3))`;
- exact point deduplication gives the three vertex counts above;
- every one of the 3,985 committed `G1` edges and 12,530 committed `G3` edges
  has squared length exactly one.

Floating point is used by the regeneration command only to propose candidate
unit pairs.  Every proposed retained edge is then accepted by exact field
equality.  The fast verifier does not trust candidate discovery: it replays
every committed edge directly in the exact field.  Nonedge completeness is
outside the claim, as noted above.

## Lower-bound reduction and pending certificate

The hard SAT statement is only the 740-vertex forcing gadget.  Its endpoints
`A=(0,0)` and `B=(0,sqrt(3))` have indices 0 and 5.  The base CNF asks for a
proper four-colouring with both endpoints assigned colour 0.  It has 2,960
variables and 21,124 clauses:

- one exactly-one colour constraint per vertex;
- four same-colour exclusions per declared edge;
- three sound colour-symmetry pins on the maximum-degree endpoint triangle
  `(0,13,42)`;
- the endpoint-`B` colour-0 pin.

The maximum-degree choice is deterministic among the 51 triangles incident to
`A`; its other two vertices both have degree 65, versus degrees 8 and 8 in the
first lexicographic triangle.  Any ordinary colouring with `A` and `B` equal
can be colour-permuted to satisfy these pins.

There is also an exactly checked CNF involution.  The half-turn
`(x,y) -> (-x,sqrt(3)-y)` swaps `A` with `B` and vertices 13 with 42.  Composing
it with the colour permutation `(0,1,2,3) -> (0,2,1,3)` preserves every base
clause.  A 64-pair prefix lex leader orients each involutive assignment orbit
on the selected prefix; if that whole prefix is invariant, both representatives
remain.  Root unit propagation is rerun before the pairs are selected, so none
is already fixed.  Sixty-three auxiliary prefix flags
and 190 clauses give the canonical proof CNF 3,023 variables and 21,314
clauses.  The checker reconstructs the geometric half-turn, checks the base
CNF clause-by-clause under the involution, rebuilds the lex leader, and then
checks the supplied CNF byte-for-byte.  The lex leader preserves
satisfiability: between any assignment and its involutive image, at least one
has the selected Boolean prefix in nondecreasing lexicographic orientation.
A DRAT refutation would therefore prove that `A` and `B` have different
colours in every proper four-colouring of `G1`.  The canonical CNF is committed
only by hash and deterministic generator; generated CNF and proof data stay
under `/scratch`.  At this stopping point the active proof searches have not
terminated, so the lower bound is not claimed as independently certified.

The checker then replays the short structural bridge.  Two isometric copies of
`G1`, together with seven exact unit edges, form a `K5` minus the edge joining
`p=(-1,0)` and `s=(1,0)` in the forced-difference relation.  Four colours force
`p` and `s` to be equal.  A rotated second copy has the analogous forced-equal
pair `p` and `s'=(3/4,sqrt(15)/4)`, while `s s'` is an exact unit edge.  Hence,
conditional on the endpoint CNF being unsatisfiable, `G3` is not
four-colourable.  `certificate.json` contains a proper five-colouring checked
directly against all 12,530 edges, proving `chi(G3) <= 5`.

The committed graph is Moser-spindle-free by a solver-free exhaustive search
using the Hajós description of the spindle: two copies of `K4-e` share one
endpoint of their missing edges, and the other two endpoints are adjacent.
The checker enumerates every such pair of arms in `G3` and finds none.

## Reproduction

Use CPython 3.11 or newer.  Put environments, generated CNFs, proof logs and
other outputs under `/scratch`.

```bash
python3 -m venv /scratch/haugland2131-venv
/scratch/haugland2131-venv/bin/pip install -r requirements.txt

# Solver-free exact replay (about 90 seconds on the reference host).
/scratch/haugland2131-venv/bin/python verify.py graph.json certificate.json

# Reconstruct the three graphs from the committed Appendix A path table.
/scratch/haugland2131-venv/bin/python reconstruct.py \
  graph.json /scratch/haugland2131-rebuilt.json

# Rebuild the endpoint CNF and an independently chosen five-colouring.
/scratch/haugland2131-venv/bin/python sat_cert.py \
  graph.json /scratch/haugland2131-g1.cnf \
  /scratch/haugland2131-five-colouring.json

# Attempt to produce and independently check the pending lower-bound proof.
cadical --unsat --phase=false \
  /scratch/haugland2131-g1.cnf /scratch/haugland2131-g1.drat
drat-trim /scratch/haugland2131-g1.cnf /scratch/haugland2131-g1.drat

# Once a proof completes, replay byte-for-byte CNF reconstruction and DRAT.
/scratch/haugland2131-venv/bin/python verify.py graph.json certificate.json \
  --cnf /scratch/haugland2131-g1.cnf \
  --proof /scratch/haugland2131-g1.drat \
  --drat-trim /path/to/drat-trim
```

Expected solver-free summary:

```text
all_checks=true G1_unit_edges=3985 G3_unit_edges=12530 five_colouring=true moser_spindle_free=true
```

Expected CNF summary:

```text
G1_equal_endpoint_four_colour_cnf variables=3023 clauses=21314 triangle=(0, 13, 42) endpoints=(0,5) lex_pairs=64
```

## Compact artifacts and proof boundary

- `graph.json` contains the 231 Appendix A paths and the declared `G1` and
  `G3` edge lists.  It is compact evidence, not a floating-point coordinate
  dump.
- `certificate.json` contains the proper five-colouring and the endpoint/CNF
  metadata.
- `reconstruct.py` regenerates and exact-checks the geometry.
- `sat_cert.py` regenerates the canonical CNF and a five-colouring.
- `verify.py` replays exact edges, the five-colouring, the forcing-subgraph
  bridge, the Moser-spindle exclusion, the CNF/symmetry bridge, and optionally
  a future DRAT proof.
- The generated CNF, DRAT proof, and solver log stay under `/scratch` and are
  not committed.  Their hashes and replay statistics are recorded below.

```text
graph.json SHA-256: 201196679760fc329fff548346b843a821646ce5ffc326a91cc24598effc299d
certificate.json SHA-256: a00adc01f218922819318ef2ce982fa795b843e91a95c94cb9f36bea6a6c9111
canonical G1 CNF SHA-256: 12be9acfc429eec206abcdf547d71cfcd28739e93b7999142c130e25f5c1d776
DRAT proof: pending; no terminal refutation was available at this stopping point
```

The mathematical trust boundary is CPython and SymPy 1.14.0's algebraic-field
arithmetic, the correct transcription of Haugland's Appendix A paths, the
explicit quadratic-extension operations, and deterministic CNF/symmetry
reconstruction.  The five-colouring generator is not trusted because its
output is checked edge-by-edge.  A future lower-bound claim would additionally
trust `drat-trim`, with CaDiCaL used only as a proof generator.  The present
commit does not cross that boundary.  The Moser-spindle search is a
self-contained finite adjacency check.  No proof-assistant formalisation or
independent second exact-field implementation was performed.
