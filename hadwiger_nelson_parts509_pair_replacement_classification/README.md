# Classification of the 63 Parts-509 pair replacements

## Exact result

Let `G` be Jaan Parts's strict unit-distance graph on 509 algebraic points.
The sibling two-point-augmentation certificate defines an exact set `Q3` of
1,158 completion points and, for every pair `A = {q1,q2}`, a set

```text
U(A) = {u in V(G) : G - u + A is not 4-colourable (declared)}.
```

Exactly 63 pairs in that certificate have `|U(A)| = 2`.  This directory
classifies all 63 graphs

```text
H(A) = G - U(A) + A,
```

each of which has 509 vertices.  Exact reconstruction and checked certificates
give:

- 60 graphs are not 4-colourable, hence are 5-chromatic;
- 3 graphs are 4-colourable, with explicit solver-free witnesses in
  `certificate.json`;
- none of the 63 added pairs is itself a unit-distance pair;
- the graph edge counts range from 2,442 to 2,450, with histogram
  `2442:21, 2443:24, 2444:11, 2445:3, 2450:4`.

The three 4-colourable cases, using completion-point and base-vertex indices
from the sibling certificates, are

```text
A = {43,60},   U(A) = {415,455}
A = {80,131},  U(A) = {220,300}
A = {144,190}, U(A) = {217,301}
```

Every one of the 60 non-4-colourable graphs is **5-vertex-critical**.  For a
retained base vertex `w`, deleting `w` gives `G - (U(A) union {w}) + A`, which
is 4-colourable by the sibling complete delete-three/add-two theorem.  Deleting
one of the two added points gives a delete-two/add-one graph, which is
4-colourable by the sibling complete one-point-swap theorem.  Thus every
one-vertex deletion is 4-colourable; adding the deleted vertex back raises the
chromatic number by at most one.  Combined with the checked non-4-colourability
certificate, this proves chromatic number exactly five and vertex-criticality.

This is a classification of 63 candidate instances, not a classification up
to graph isomorphism.  No claim is made that the 60 graphs are pairwise
nonisomorphic.  They tie the 509-vertex record; they do not improve it or the
bounds `5 <= chi(R^2) <= 7`.

## Exact geometry and positive certificates

`classify_pair_replacements.py` parses the 509 published coordinates with the
exact multiquadratic arithmetic from the vertex-criticality contribution.  It
then parses the relevant completion points as rational coefficient vectors in
`Q(sqrt(3),sqrt(5),sqrt(11))` and exactly rescans all 509 base points for each
of the 19 completion points used by the candidates.  The recomputed neighbour
sets must equal the committed lists.  All candidate edges are then rebuilt
from the 2,442 strict base unit pairs, the rescanned point incidences, and an
exact test between the two added points.  No floating-point number or tolerance
is used.

The independent checker imports none of the primary arithmetic or
classification code.  It parses the coordinates into SymPy's
`AlgebraicField`, recomputes all 129,286 base distances and all relevant
point-base and point-point distances there, rebuilds all candidate graphs and
CNFs, and directly checks the three stored 4-colourings.

## Non-4-colourability certificates

Each candidate has a canonical four-colour CNF with 2,036 variables.  For
every graph vertex it contains one at-least-one and six at-most-one clauses;
for every graph edge and colour it contains the usual incompatibility clause.
Three unit clauses pin distinct colours on a triangle, which is sound by colour
permutation.  Depending on the edge count, the CNFs have 13,334--13,366
clauses.

CaDiCaL `sc2021` generated a DRAT refutation for each of the 60 negative cases.
Every proof was replayed with `drat-trim`, which returned `s VERIFIED`.  The
aggregate audit was:

```text
verified_proofs=60
total_proof_bytes=966972547
total_core_lemmas=2996532
minimum_core_lemmas=39598
maximum_core_lemmas=61108
total_resolution_steps=199737608
```

The 60 CNF hashes, proof hashes, proof sizes, and checker statistics are in the
compact 26 KiB `certificate.json`.  In accordance with the repository policy,
the 923 MiB of DRAT files and all solver/checker logs remain under `/scratch`
and are not committed.  The source can rebuild every CNF byte-for-byte; the
proof hashes can be checked when the corresponding scratch files are still
available.

## Verification

Use CPython 3.11 or newer and keep the environment under `/scratch`:

```bash
python3 -m venv /scratch/parts509-pair-classification-venv
/scratch/parts509-pair-classification-venv/bin/pip install -r requirements.txt

/scratch/parts509-pair-classification-venv/bin/python \
  classify_pair_replacements.py verify certificate.json
/scratch/parts509-pair-classification-venv/bin/python \
  independent_check.py certificate.json
```

Expected summaries:

```text
all_checks=true candidates=63 colorable=3 solver_reported_unsat=60
used_completion_points=19 coloring_edge_checks=7330

all_checks=true base_unit_pairs=2442 used_completion_points=19 candidates=63 colorable=3 certified_not_4_colorable=60
coloring_edge_checks=7330 proof_bytes_hashed=0
```

To rebuild all CNFs under scratch:

```bash
/scratch/parts509-pair-classification-venv/bin/python \
  classify_pair_replacements.py verify certificate.json \
  --write-cnfs /scratch/parts509-pair-classification-cnfs
```

If the original proof files are available, the independent checker also
checks all 60 proof hashes and sizes:

```bash
/scratch/parts509-pair-classification-venv/bin/python \
  independent_check.py certificate.json \
  --proof-dir /scratch/parts509-pair-replacement-classification/proofs
```

## Search regeneration

The discovery search uses PySAT only to find the three positive witnesses and
to identify the 60 cases needing proofs:

```bash
/scratch/parts509-pair-classification-venv/bin/python \
  classify_pair_replacements.py search \
  /scratch/parts509-pair-classification-search.json \
  --solver cadical195
```

SAT models are decoded and checked against the exact graph before storage.
After external CaDiCaL and `drat-trim` runs, `attach-proofs` converts the search
manifest and checker logs into the compact final certificate.  Regenerated
DRAT proofs can differ and therefore need not have the committed hashes.

## Status and trust boundary

This is an exact computer-assisted structural result and a complete
classification of one finite candidate family selected by the earlier pair
closure.  Targeted literature and committed-graph searches through 2026-09-01
found no such classification; no priority or pairwise-nonisomorphism claim is
made, and earlier minimisation experiments may contain implicit overlap.

The primary geometry layer trusts the published Parts coordinate input,
CPython integer and rational arithmetic, SymPy 1.14.0 for parsing and radical
denesting, and the sibling multiquadratic-field implementation.  The
independent checker replaces the field implementation by SymPy's
`AlgebraicField`.  The three 4-colourability claims trust only explicit
colouring replay.  The 60 lower bounds trust the rebuilt CNF bridge and the C
implementation of `drat-trim`; CaDiCaL is only the proof generator.  The
5-vertex-criticality corollary additionally depends on the separately
certified one-point-swap and two-point-augmentation closure theorems.  No proof
assistant formalisation was performed.

## Context

- Jaan Parts, *Graph minimization, focusing on the example of 5-chromatic
  unit-distance graphs in the plane*, Geombinatorics 29(4) (2020), 137--166,
  <https://arxiv.org/abs/2010.12665>.
- Exact base reconstruction and vertex-criticality:
  `../hadwiger_nelson_parts509_criticality`.
- Complete one-point-swap closure:
  `../hadwiger_nelson_parts509_swap_closure`.
- Complete delete-three/add-two closure and the 63 candidate pairs:
  `../hadwiger_nelson_parts509_pair_closure`.
