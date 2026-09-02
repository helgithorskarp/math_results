# Exact automorphisms and a colouring-CNF quotient for Haugland's 740-vertex gadget

## Certified result

Let `G1` be the 740-vertex, 3,985-edge endpoint gadget in Jan Kristian
Haugland's *A Moser-spindle-free 5-chromatic unit distance graph on 2131
vertices in the plane*.  For the exact edge list reconstructed in the sibling
directory `hadwiger_nelson_haugland2131_exact_reproduction`, this contribution
certifies

```text
Aut(G1) is isomorphic to C6 x C2 and has order 12.
```

The action has exactly 66 vertex orbits: 60 of size 12, two of size 6, and
four of size 2.

The group order is proved without trusting an automorphism package.  Ordinary
one-dimensional colour refinement stabilizes at 66 cells with the same size
histogram as above.  The cell containing vertex 1 has size 12.  After vertex 1
is individualized, five more refinement rounds give 740 singleton cells, so
the point stabilizer of vertex 1 is trivial.  The certificate explicitly gives
12 permutations, verifies each against all 3,985 edges, and verifies that their
images of vertex 1 fill its 12-element refinement cell.  Hence there are at
least 12 automorphisms and at most 12.  Direct composition and element-order
checks show that the group is abelian with order histogram

```text
order 1: 1; order 2: 3; order 3: 2; order 6: 6,
```

which identifies it as `C6 x C2`.

## Certified SAT reduction

The same certificate produces a stronger symmetry quotient for the still-open
independent replay of Haugland's endpoint-forcing computation.  Start with the
standard exactly-one four-colour CNF, pin the endpoint triangle `(0,13,42)` to
colours `(0,1,2)`, and require the other endpoint 5 to have colour 0.  This
base formula has 2,960 variables and 21,124 clauses.

Every one of the 12 graph automorphisms preserves the endpoint pair.  It either
fixes vertices 13 and 42 or swaps them; in the latter case, composing with the
colour transposition `1 <-> 2` preserves the pinned CNF.  The verifier maps
every base clause under every one of these 12 Boolean permutations and checks
set membership directly.

For each of the 11 nonidentity symmetries, the generator adds a 64-position
prefix lex leader.  The leaders are simultaneously satisfiability-preserving:
in each finite group orbit of assignments, choose the lexicographically least
complete Boolean vector.  It is no greater than each of its 11 images, and
therefore satisfies every prefix comparison.  Prefix-equality gates are exact
CNF definitions.  The resulting deterministic formula has

```text
variables=3653 clauses=25282
SHA-256=23727463dfaf30f0d2267cadedb19a9b7af35b494c81491219165ff09dccdcca
```

This is a certified reduction, **not** a refutation.  Short CaDiCaL and Kissat
runs on the reduced formula and three anchor-colour subcases ended `UNKNOWN`.
No DRAT proof is committed or claimed.  Thus this contribution does not yet
independently prove that the gadget endpoints differ in every four-colouring,
does not certify the lower bound for Haugland's 2,131-vertex graph, does not
improve the 509-vertex record, and does not change `5 <= chi(R^2) <= 7`.

## Reproduction

From the repository root, run the solver-free verifier with CPython 3.11 or
newer:

```bash
python3 hadwiger_nelson_haugland740_automorphisms/automorphism_certificate.py \
  verify \
  hadwiger_nelson_haugland2131_exact_reproduction/graph.json \
  hadwiger_nelson_haugland740_automorphisms/certificate.json \
  --cnf-out /scratch/haugland740-group12.cnf
```

Expected output:

```text
all_checks=true vertices=740 edges=3985 automorphism_group_order=12 group_isomorphic_to=C6xC2 base_refinement_cells=66 vertex_orbits=66 base_refinement_rounds=2 anchor_cell_size=12 individualized_cells=740 individualized_rounds=5 cnf_variables=3653 cnf_clauses=25282 cnf_sha256=23727463dfaf30f0d2267cadedb19a9b7af35b494c81491219165ff09dccdcca
```

The verifier uses only the Python standard library.  To rediscover the 12
candidate permutations rather than replay them, install `pynauty==2.8.8.1`
in a scratch environment and run:

```bash
python3 hadwiger_nelson_haugland740_automorphisms/automorphism_certificate.py \
  build \
  hadwiger_nelson_haugland2131_exact_reproduction/graph.json \
  /scratch/haugland740-certificate.json
```

The build-time package is outside the proof trust boundary because `verify`
checks the explicit permutations and proves completeness independently.

Certificate SHA-256:
`bb361a60039fa3d4caecb16bee801507205a4e7f053753a11cf053c418e2f7c3`.

## Scope, literature status, and trust boundary

The primary construction is J. K. Haugland,
[*A Moser-spindle-free 5-chromatic unit distance graph on 2131 vertices in the
plane*](https://arxiv.org/abs/2608.04542v2), 2026.  The paper states the graph
counts and a CaDiCaL endpoint check but does not discuss the automorphism group
or publish a SAT certificate.  Targeted searches of the paper, its current
online descriptions, repositories, and the committed Discovery Net graph
through 2026-09-02 found no prior automorphism classification of this graph.
The classification is therefore described only as apparently new to the
searched sources; no unconditional priority claim is made.

The graph-theoretic theorem and CNF reconstruction trust CPython's JSON parser,
integer/set operations, SHA-256, and the committed edge list.  They do not
trust `pynauty` or a SAT solver.  The statement that the same abstract graph has
the declared unit-distance realization depends on the sibling exact-geometry
reproduction and its SymPy algebraic-field trust boundary.  There is no proof
assistant formalization.  Generated CNFs, solver logs, and proof traces belong
under `/scratch` and are intentionally excluded from the repository.
