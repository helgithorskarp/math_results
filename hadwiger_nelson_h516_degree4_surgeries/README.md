# Four degree-four surgeries reach abstract order 508 but fail plane realization

Every graph in the following complete family has exactly 508 vertices and
chromatic number at least five, but none has an injective unit-distance
realization in the Euclidean plane. The family contains 53,276 **labelled surgery
choices**, not necessarily that many isomorphism classes. This is a finite
construction-family exclusion, not a smaller five-chromatic unit-distance graph.

Start with the accepted 516-vertex, 2,538-edge graph specified by negative core
52 in the [H560 global decision](../hadwiger_nelson_heule560_global_decision),
with its [independent review](../hadwiger_nelson_heule560_global_decision_review1).
Its vertex set is `mandatory_vertices` from
`hadwiger_nelson_heule632_minimize/boundary.json`, together with the optional
vertices selected by mask `410114573119741915` in the global decision's
`optional_order`. The source is reproduced in [SOURCE.json](SOURCE.json).
Labels retain their original H632 meaning.

Choose four original degree-four vertices with pairwise disjoint **closed**
stars. At each centre, delete the centre and identify an unordered nonadjacent
pair of its four neighbours. Preserve every other edge, remove duplicate
edges, and use the smaller host label for the identified pair. There are ten
centres, 87 compatible quadruples, and 53,276 choices of pairs. Every result
has 516 − 4 − 4 = 508 vertices.

## Why the chromatic gate is positive

If a graph G is not four-colourable, v has degree four, and u,w are nonadjacent
neighbours of v, then `(G−v)/(u=w)` is not four-colourable. A hypothetical
four-colouring of this quotient pulls back to G−v with u,w the same colour.
The four neighbours of v therefore use at most three colours, and the
colouring extends to v, a contradiction. Disjoint closed stars ensure that
the four operations leave each remaining centre and its four distinct
neighbours intact, so the argument iterates. This elementary reduction is
not claimed as a new general graph-colouring theorem.

This changes edge constraints before asking for a new drawing. It is not an
induced-subgraph search or an edge-preserving map of the original H516 or
H510 graph. The inherited conclusion is **chromatic number at least five**;
a five-colouring of a source graph need not descend through identification.

For an additional direct check of the positive source, one fresh Glucose42
query refuted its four-colouring CNF in 4.45 seconds and 58,584 conflicts,
within the frozen 300-second, 500,000-conflict cap. DRAT-trim verified the
proof; the strict positive-hint LRAT checker independently accepted its
44,366 retained additions and 3,328,915 hints. No target-graph colouring query
was necessary. The source proof is supplemental to the previously reviewed
source, and is distinct from the geometric exclusion below.

## Complete geometric certificate

Two distinct points in the plane have at most two common points at distance
one from both. Thus an injective plane unit-distance graph cannot contain
K(2,3), whether induced or not.

The C++ producer constructs every **final** quotient graph and finds such a
subgraph. The [certificate](certificate.json) lists just 43 witnesses. Each
witness `[a,b,c,d,e]` requires the six edges from `{a,b}` to `{c,d,e}`. For
every surgery choice, at least one listed witness survives with five distinct
vertices and all six required edges. No intermediate-graph rejection is used:
later surgery could otherwise remove or identify a witness vertex.

The independent standard-Python [checker](verify.py) derives the complete
family from the source adjacency. It tests final-quotient edges by inverse
fibres in the original graph, without importing or executing the C++ producer.
It also checks all 132,870 source point pairs with expanded exact radical
norms. The source coordinates are integer numerators over 96 in the real basis
`[1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165)]`,
separately for x and y. All 516 points are distinct and exactly 2,538 pairs
have squared distance one.

The checker covers all 53,276 cases with zero survivors and rejects four
mutated certificates. Normal and `python3 -O` runs give identical receipts.
This is independent computational validation within the same research pass,
not an external peer review or a proof-assistant formalization.

Certificate: 3,127 bytes; SHA256
`e4b9aefa91795174669da14e3b18ef717ba28ebab2c5338be90095b26af9203a`.
Source: 48,097 bytes; SHA256
`3f60fe94c7cd3d9c70b7cc52124fa185d4b46d54bb59b21bca0c45d2b181fd51`.

## Reproduction

From the repository root, with standard Python 3.11 or later:

```sh
python3 -B hadwiger_nelson_h516_degree4_surgeries/verify.py --work /tmp/h516-surgery-check
python3 -O -B hadwiger_nelson_h516_degree4_surgeries/verify.py --work /tmp/h516-surgery-check-O
```

Expected: 87 compatible quadruples, 53,276 covered labelled cases, 43
witnesses, zero survivors, and four rejected bad certificates. The exact
receipt is in [expected.json](expected.json). No solver is needed to check
the geometric exclusion.

To regenerate the source from the existing repository inputs and rerun the
producer (requires a C++17 compiler):

```sh
python3 -B hadwiger_nelson_h516_degree4_surgeries/regenerate_source.py --output /tmp/h516-surgery-source/SOURCE.json
python3 -B hadwiger_nelson_h516_degree4_surgeries/produce.py --work /tmp/h516-surgery-producer
```

The source regeneration calls only the older input loader, not its
homomorphism propagation. It compares the regenerated source byte for byte.
The producer likewise compares the regenerated compact certificate.

Optional fresh reproduction of the supplemental source refutation requires
`python-sat==1.9.dev15`, Glucose42, DRAT-trim revision
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, and the strict LRAT source already
published in this repository. Use a new work directory. This campaign ran the
solver once; no second solve or cap extension was used for validation.

```sh
python3 -B hadwiger_nelson_h516_degree4_surgeries/source_gate.py prepare --work /tmp/h516-source-proof
python3 -B hadwiger_nelson_h516_degree4_surgeries/audit_cnf.py --work /tmp/h516-source-proof
python3 -B hadwiger_nelson_h516_degree4_surgeries/source_gate.py solve --work /tmp/h516-source-proof
drat-trim /tmp/h516-source-proof/source.cnf /tmp/h516-source-proof/source.drat -L /tmp/h516-source-proof/source.lrat -t 300
g++ -O3 -std=c++17 hadwiger_nelson_vnd_case10_verified_gate/strict_lrat.cpp -o /tmp/h516-strict-lrat
/tmp/h516-strict-lrat /tmp/h516-source-proof/source.cnf /tmp/h516-source-proof/source.lrat
```

The CNF has 2,064 variables and 10,671 clauses: one four-colour at-least-one
clause per vertex, four inequality clauses per edge, and three sound triangle
pins. At-most-one clauses are unnecessary: choose one allowed colour per
vertex from any model. `audit_cnf.py` checks every clause and the actual
triangle. Accept the source refutation only after both proof checkers succeed.
The runner's `proof_verified: false` correctly means its solver answer alone
has not checked the proof. The committed receipt records the later checks.
Do not substitute the legacy `lrat-check` executable; its empty-clause defect
is documented in
[the VND strict-checker package](../hadwiger_nelson_vnd_case10_verified_gate).

CNF SHA256:
`1a9f7b317df35a92cb4a730a98c828743cd9993b522b083e44b2943bd5a4ee0a`.
The original 13,075,894-byte DRAT and 22,268,047-byte LRAT files remain outside
Git; their hashes, exact solver statistics, and checking receipts are in
`expected.json`. No large proof, exhaustive per-case dump, or binary is
published. Solver proof bytes may vary across versions; independent acceptance
against the exactly audited CNF is the relevant test.

## Boundary and handoff

The frozen family is closed. No rhombus/Gram realization stage was entered,
and no family expansion was made. This result does not cover noninjective
further images of the modified graphs, overlapping closed stars, different
numbers of surgeries, or different sources. These are scope limits, not
recommendations to begin a parameter ladder.

The positive target-scale reduction produced abstract 508-vertex graphs but
no admissible planar candidate. Preserve this certificate, leave this family,
and require a materially different geometric mechanism before another major
phase. The team's H510 near-injective closure and rational-comb work remain
separate. No unit-distance graph on at most 508 vertices with chromatic number
five is established here.
