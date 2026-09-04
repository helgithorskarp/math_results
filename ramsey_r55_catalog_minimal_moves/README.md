# Minimal Ramsey-preserving moves in the known order-42 catalog

Every nonempty Ramsey-preserving edge-flip set of size at most six from a
known Ramsey(5,5,42) graph contains a Ramsey-preserving subset consisting of
either one edge or a matching of four edges. Each of the latter moves
deletes two red edges and adds two red edges, on eight distinct vertices.

For the 328 stored labeled parents there are exactly **2,200 inclusion-minimal
moves: 2,040 singletons and 160 balanced four-edge matchings**. Complementation
gives the result for the other 328 known orientations. The 47 KB
`MINIMAL_MOVES.tsv` records each minimal move and its target class. Here
“minimal” means having no proper nonempty Ramsey-preserving subset, not having
minimum distance to its target isomorphism class.

The existing exact transition maps give this finer inclusion census:

| exact flip count | valid moves | contain a valid singleton | contain a quartet but no valid singleton |
|---|---:|---:|---:|
| 1 | 2,040 | 2,040 | 0 |
| 2 | 5,568 | 5,568 | 0 |
| 3 | 8,632 | 8,632 | 0 |
| 4 | 8,408 | 8,248 | 160 |
| 5 | 6,224 | 5,968 | 256 |
| 6 | 6,384 | 6,256 | 128 |

## Consequence: monotone factorization of local moves

Let `G` be any known catalog orientation and suppose `G triangle S` is Ramsey,
where `triangle` denotes symmetric difference of edge sets and `|S|<=6`.
Then `S` can be partitioned into successive valid moves, each a singleton or
balanced four-edge matching. Every intermediate graph is Ramsey and in the
known catalog; no edge is flipped twice. There is at most one four-edge step.

Proof: if `S` is nonempty, the census supplies a minimal valid subset
`T subseteq S` of size one or four. The radius-six closure theorem puts
`G triangle T` back in the known catalog up to isomorphism. Relabel it to its
stored representative, applying the same relabeling to `S minus T` (and
complement if needed). The endpoint is still Ramsey and fewer flips remain,
so induction applies. At each step the chosen support is a subset of the
remaining original support, proving monotonicity. Two four-edge steps would
need at least eight flips.

This is stronger than merely saying that the endpoints lie in the same
connected component of a transition graph: the path uses only the prescribed
endpoint differences and does not revisit an edge.

## Consequence: a small necessary filter at radius seven

Let `M(G)` be the minimal-move list for a labeled catalog graph `G`. If `H` is
a Ramsey graph outside the known catalog and `H=G triangle S` with `|S|<=7`,
then no `T in M(G)` can satisfy `T subseteq S`.

Indeed, `G triangle T` is a known catalog graph. If `T subseteq S`, the
distance from that graph to `H` is `|S|-|T|<=6`, contradicting established
radius-six closure. Thus, with flip variables `x_e`, every possible new graph
in this seven-edit search obeys the clauses

```text
OR_{e in T} NOT x_e          for each T in M(G).
```

Only **2–9 clauses per parent** are needed. Their distribution is:

```text
clauses   2  3   4   5   6    7   8  9
parents   4  8  12  24  72  104  96  8
```

The filter preserves every possible *new* graph in this radius. It deliberately
discards many valid moves returning to the known catalog, so its output is
not a full transition enumeration. SAT of a residual formula would still
require direct graph validation and an isomorphism test; it would not by
itself establish a new catalog class or an order-43 witness. The stated
filter is justified through radius seven, not at arbitrary larger radii.

## Verification and reproduction

Run from this directory with Python 3.11 or later and the sibling artifacts:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 analyze_minimal_moves.py > /tmp/r55-minimal.out
cmp /tmp/r55-minimal.out EXPECTED_OUTPUT.txt
PYTHONDONTWRITEBYTECODE=1 python3 residual_cnf.py --self-test
sha256sum -c SHA256SUMS
```

The analyzer imports the sibling transition-map parser, which pins all five
input maps by SHA-256 and checks their counts and schema. For every recorded
move it enumerates all proper nonempty subsets and tests membership in that
parent's complete transition list. It separately verifies that every one of
the 37,256 recorded moves contains a discovered minimal support. It then
reconstructs all 2,200 minimal graphs and directly checks the absence of a
five-clique in both colors, checks all 2,240 nonempty proper subsets of the
quartets for invalidity, and checks their disjoint endpoints and color balance.
The certificate is reproduced byte for byte; its SHA-256 is
`27bfe713c711ab319bb9eb909cec997049e48c68e22539bbb54f543daea68896`.

`residual_cnf.py` emits a nonzero, at-most-seven-flip Ramsey formula with the
minimal-support clauses. It uses 861 primary variables in graph6 pair order:
`x_(u,v)=v*(v-1)/2+u+1` for `u<v`. Eight forward threshold levels enforce the
cardinality bound. At least eight selected flips force the forbidden final
level by induction; conversely exact prefix counts satisfy all counter clauses
whenever the weight is at most seven. Thus auxiliary nonuniqueness changes no
allowed primary assignment.

For each five-set with original present edges `P` and absent edges `A`, the
clique clause is `OR(P) OR NOT(A)`, emitted when `|A|<=7`; the independent-set
clause has the opposite polarities and is emitted when `|P|<=7`. Omitted
homogeneous patterns need more than seven flips. A final positive disjunction
of all 861 variables excludes the unchanged parent. Arithmetic uses Python
integers. The self-test checks all 1,024 primary assignments on a five-vertex
cycle at four radii against direct triangle tests, nonzero weight and forbidden
subset membership, using canonical threshold extensions. All 4,096 cases pass,
including three positive cases. Counter soundness for arbitrary extensions is
the induction argument above, not an inference from these canonical tests.

## Bounded parent-0 pilot: UNKNOWN

Generate the pilot instance:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 residual_cnf.py --parent 0 --output /tmp/r55-residual0.cnf
cadical --no-colors -t 600 -c 100000 /tmp/r55-residual0.cnf /tmp/r55-residual0.drat
```

Expected generator output:

```text
parent=0 variables=7749 clauses=1643567 minimal_blocks=7 sha256=5c0c39228e96fa9ad7324f05c13dd9ab8c09329099528b0a124390b7f4f478b4
```

CaDiCaL 3.0.1 reached the declared conflict limit after about 46 wall seconds
and returned **UNKNOWN**, exit code 0. No SAT witness or checked UNSAT proof
resulted. The DRAT file is an incomplete trace and is not a certificate.
`PILOT.json` records the exact solver build, limits, input hash, resources and
output status. Bulky CNF, trace and solver log remain in local checkpoint
storage. This pilot establishes no radius-seven exclusion and no speedup over
the earlier full parent-0 enumeration. The bounded unit was not extended into
a catalog-wide search. The local process additionally had an 8 GiB address-space
limit and a 2 GiB per-file limit; neither was reached.

## Provenance, novelty, and trust

This is an exact synthesis of the published
[radius-two](../ramsey_r55_catalog_edge_radius2_classification),
[radius-three](../ramsey_r55_catalog_edge_radius3_classification),
[radius-four](../ramsey_r55_catalog_edge_radius4_classification),
[radius-five](../ramsey_r55_catalog_edge_radius5_classification) and
[radius-six](../ramsey_r55_catalog_edge_radius6_classification) maps.
It inherits their explicit solver/completeness and target-identification
trust boundaries. Direct checks certify the listed minimal moves and their
minimality; absence of any further minimal move through six still depends on
the completeness of those maps. The monotone-factorization and new-graph
filter arguments additionally use their catalog-closure conclusions.

The catalog is from [McKay's ANU archive](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html).
McKay and Radziszowski describe heuristic and exhaustive neighborhood work in
[*Subgraph counting identities and Ramsey numbers*](https://users.cecs.anu.edu.au/~bdm/papers/r55.pdf),
section 4, and present catalog completeness as a conjecture. Searches of those
primary sources and the committed graph through 2026-09-04 found no explicit
inclusion-minimal 1/4-move classification; no historical priority is claimed.

The theorem concerns only the known catalog neighborhood. It neither proves
catalog completeness nor improves the lower bound for `R(5,5)`. It is distinct
from team-r55-3's degree-specific singleton distance-eight result: no target
degree multiset is imposed here.
