# Cross-edge criticality of the Parts-509 decomposition

## Result

Let `G` be the strict unit-distance graph on Jaan Parts's 509 published
algebraic points.  As in the sibling interface certificate, split its vertices
as

```text
L = {0,...,373},       S = {374,...,508}.
```

There are 1,860 edges inside `L`, 552 inside `S`, and 30 edges between the two
parts.  The exact graph has 2,442 edges in total and chromatic number five.

**Theorem (exact computer-assisted).** Every one of the 30 cross edges is
chromatic-critical:

```text
chi(G - e) = 4                 for every cross edge e.
```

Consequently, if all internal edges of `L` and `S` are fixed and `C` is any
subset of the 30 cross edges, then

```text
L union S union C is not 4-colourable  iff  C contains all 30 cross edges.
```

In particular the full 30-edge coupling is the unique non-four-colourable
cross-edge subset.  All 19 `L`-side interface vertices and all 30 `S`-side
interface vertices are indispensable as cross-edge endpoints in this precise
sense.

The positive certificate is simple: for every cross edge `e`, at least one of
the committed rows is an explicit proper four-colouring of `G-e`, and the
checker tests it against all 2,441 retained edges and confirms that the two
endpoints of `e` have the same colour.  Since `chi(G)=5`, an edge deletion can
lower the chromatic number by at most one, so the displayed upper bound four is
also exact.  If `C` omits `e`, the same colouring remains proper after deleting
still more cross edges.

This is structural information about the existing 509-vertex record.  It does
not produce a graph on fewer vertices, improve the 2,259-edge non-strict record,
or change `5 <= chi(R^2) <= 7`.  The earlier 2,259-edge subgraph happens to keep
all 30 cross edges; the present result shows directly that none can be omitted
even when all 2,412 internal strict edges are retained.

## Complete one-edge leak classification

The sibling interface theorem gives exactly 20 restrictions of proper
four-colourings of `L` to its 19-vertex interface, modulo the colour permutations
fixing the origin's colour.  For each of these 20 classes and each of the 30
possible omitted cross edges, `certificate.json` classifies whether the class
extends across `S`—600 cases in all.

There are exactly 237 positive and 363 negative cases.  The positive cases have
explicit `S`-colouring witnesses.  The number of leaking edge deletions for
classes 0 through 19 is

```text
12, 13, 11, 18, 11, 16, 0, 7, 13, 17,
11, 17, 12, 18, 11, 14, 0, 11, 17, 8.
```

Thus exactly classes 6 and 16 withstand every single cross-edge deletion.
These are precisely the two interface classes in which all twelve reference
vertices have the origin's colour.  Every cross edge leaks between five and
eleven of the other 18 classes; the exact lists in both directions are stored
in the certificate.

For each negative case the program writes the canonical 540-variable CNF and a
CaDiCaL DRAT refutation.  A fresh run checked all 363 proofs with `drat-trim`:

```text
positive_cases=237
negative_cases=363
negative_proofs_checked=363
proof_bytes_checked=27953074
classes_with_no_single_edge_leak=[6, 16]
```

The classification's negative half depends on these proof checks and on the
separately certified completeness of the 20 interface classes.  The main
cross-edge-criticality theorem needs only the 30 positive deletion witnesses
and the earlier proof that `G` is not four-colourable.

## Exact geometry and certificate

`cross_edge_criticality.py` reconstructs all pair distances exactly from
`../hadwiger_nelson_parts509_criticality/parts509.vtx` using rational arithmetic
in `Q(sqrt(3),sqrt(5),sqrt(11))`; no floating-point comparison is used.  It
recovers the canonical strict edge hash

```text
5a95127767cb370f25f5865f057cab9b4a7ee9a72e2f73ad126ae390d71d487c
```

and the `1860 + 552 + 30` decomposition.  The input coordinate SHA-256 is

```text
770a585a6c1e1222355322707479cb826e9ada560279da904ef89c15c99ff0b5
```

The compact 298,973-byte certificate has SHA-256

```text
e08dbc6375407bd6a20dd5871f9690625dee105a50a01687281cba0a85668ceb
```

The colourability CNF has one at-least-one-colour clause per `S` vertex, four
same-colour exclusions per internal `S` edge, and one unary exclusion for each
retained cross edge after the `L` interface colours are fixed.  Explicit
at-most-one clauses are unnecessary: adjacent selected-colour sets are
disjoint, so selecting any one asserted colour per vertex gives an ordinary
proper colouring.

`independent_check.py` imports neither the generator nor the exact-coordinate
implementation.  It reads the independently committed canonical edge manifest,
rechecks all 20 `L` witnesses, rebuilds all 600 CNFs byte-for-byte, and checks
578,517 retained-edge inequalities in the 237 positive cases.  With a proof
directory it also hashes and independently replays every negative proof.

## Reproduction

From the repository root, a fast solver-free replay of all positive witnesses
and every CNF hash is:

```bash
python3 hadwiger_nelson_parts509_cross_edge_criticality/independent_check.py
```

Expected tail:

```text
all_checks=true
positive_cases=237 negative_cases=363
coloring_edge_checks=578517
cross_edges_individually_critical=30
classes_with_no_single_edge_leak=[6, 16]
negative_proofs_checked=0
```

To regenerate and proof-check the complete classification, install the pinned
Python dependencies in a scratch environment and keep all bulky output under
`/scratch`:

```bash
python3 -m venv /scratch/parts509-cross-venv
/scratch/parts509-cross-venv/bin/pip install -r \
  hadwiger_nelson_parts509_cross_edge_criticality/requirements.txt

/scratch/parts509-cross-venv/bin/python \
  hadwiger_nelson_parts509_cross_edge_criticality/cross_edge_criticality.py \
  generate /scratch/certificate.json \
  --work-dir /scratch/parts509-cross-proof-run \
  --cadical /path/to/cadical \
  --drat-trim /path/to/drat-trim

python3 hadwiger_nelson_parts509_cross_edge_criticality/independent_check.py \
  /scratch/certificate.json \
  --proof-dir /scratch/parts509-cross-proof-run/proofs \
  --drat-trim /path/to/drat-trim
```

The recorded run used PySAT 1.8.dev24's `cadical195` backend to find witnesses,
CaDiCaL `sc2021` to emit proofs, and `drat-trim` to check them.  The 363 DRAT
files total 27,953,074 bytes; the 600 generated CNFs, DRAT files, and solver
output remain under `/scratch` and are deliberately not committed.  Their
individual hashes and sizes are in `certificate.json`.

## Status, sources, and trust boundary

Parts's minimisation paper gives the 509-vertex construction and its `L/S`
assembly; Heule's earlier construction explains the rigid-interface mechanism.
Parts explicitly asks for the minimum number of connection edges in type-M
graphs and reports that a small `S` needs at least six auxiliary edges, with the
reference orbit full.  The present statement is narrower and more detailed: it
certifies individual criticality of this graph's 12 origin, 12 reference, and
6 auxiliary cross edges and classifies all 600 one-deletion/interface cases.  A
targeted search of Parts (2020), Heule (2018), de Grey (2018), and the
Polymath16 material found no such explicit classification.  The result is
therefore described only as apparently new to the searched sources; no priority
claim is made.

Primary references:

- J. Parts, *Graph minimization, focusing on the example of 5-chromatic
  unit-distance graphs in the plane*, Geombinatorics 29(4) (2020), 137–166,
  <https://arxiv.org/abs/2010.12665>.
- M. J. H. Heule, *Computing Small Unit-Distance Graphs with Chromatic Number
  5*, Geombinatorics 28(1) (2018), 32–50,
  <https://arxiv.org/abs/1805.12181>.
- A. D. N. J. de Grey, *The chromatic number of the plane is at least 5*,
  Geombinatorics 28(1) (2018), 18–31,
  <https://arxiv.org/abs/1804.02385>.

The exact-geometry layer trusts the published coordinate input, CPython integer
and rational arithmetic, SymPy 1.14.0 parsing, and the sibling multiquadratic
field implementation.  Positive colourability claims trust only direct witness
replay.  The exact 237/363 classification additionally trusts deterministic CNF
reconstruction, the stored proof bytes with their SHA-256 hashes, and the C
implementation of `drat-trim`; CaDiCaL is only a proof generator.  The bridge
from the 30 deletion witnesses to chromatic criticality depends on the sibling
exact proof that the same strict graph is five-chromatic.  No proof-assistant
formalisation was performed.
