# Superconnectivity of the strict Parts-509 graph

## Exact computer-assisted lemma

Let `G` be the strict unit-distance graph on Jaan Parts's 509 published
points: every pair at Euclidean distance exactly one is an edge.  Bind `G` by
the canonical 2,442-edge-list SHA-256

```text
5a95127767cb370f25f5865f057cab9b4a7ee9a72e2f73ad126ae390d71d487c
```

The six vertices of minimum degree four are

```text
D = {310, 313, 316, 319, 322, 325}.
```

Their neighborhoods, and hence the complete list of minimum vertex cuts, are

```text
N(310) = {150, 169, 287, 296}
N(313) = { 89,  90, 150, 153}
N(316) = {153, 158, 288, 291}
N(319) = { 93,  94, 158, 161}
N(322) = {161, 166, 292, 295}
N(325) = { 97,  98, 166, 169}
```

This directory certifies the following graph-theoretic facts.

1. The induced core `C = G - D` has 503 vertices, 2,418 edges, minimum
   degree 5, vertex connectivity 5, and edge connectivity 5.
2. `G` has vertex connectivity 4.  Its **only** minimum vertex cuts are
   the six pairwise distinct neighborhoods `N_G(v)` for `v` in `D`.
   Deleting any one of them leaves components of orders 1 and 504, with
   the singleton component equal to `{v}`.
3. `G` has edge connectivity 4.  Its **only** minimum edge cuts are the
   six stars of edges incident with vertices in `D`.

Thus `G` is super-vertex-connected and super-edge-connected in the explicit
sense above.  This is structural information about the existing 509-vertex
record construction.  It does not produce a smaller 5-chromatic graph and it
does not improve the bounds `5 <= chi(R^2) <= 7`.

## Why the certificate proves 5-connectivity

`certificate.json` chooses five distinct roots `R` in `C`.  For every root
`r` and every other core vertex `x`, it contains five `r`--`x` paths whose
internal vertex sets are pairwise disjoint.  There are 2,510 root-target
pairs and 12,550 paths in total.

Let `S` be any set of at most four core vertices and let `x` be any surviving
core vertex.  Some root `r` survives because `|R| = 5`.  If `x != r`, each
vertex of `S` can meet the interior of at most one of the five certified
`r`--`x` paths.  At least one complete path therefore survives in `C - S`.
Every surviving vertex is connected to `r`, so `C - S` is connected.  This
proves `kappa(C) >= 5`.  The checked minimum degree 5 gives
`kappa(C) <= 5`, hence `kappa(C) = 5`.  The standard inequalities

```text
kappa(C) <= lambda(C) <= delta(C)
```

then give `lambda(C) = 5` as well.

The six vertices in `D` are independent and have all four neighbors in `C`.
If at most four vertices are removed from `G`, the remaining core is
connected.  A surviving vertex `v` in `D` joins that core unless all four
vertices of `N_G(v)` were removed.  Consequently a four-set disconnects `G`
if and only if it is one of the six neighborhoods.  The identical argument
for edge deletion, using `lambda(C) = 5`, classifies the minimum edge cuts.

## Reproduce

From the root of a checkout of this repository, the main verifier needs only
CPython 3.11 or newer and the standard library:

```bash
python3 hadwiger_nelson_parts509_superconnectivity/verify_certificate.py
```

Expected summary:

```text
all_checks=true
core_order=503
core_size=2418
core_min_degree=5
certified_core_vertex_connectivity_lower_bound=5
exact_core_vertex_connectivity=5
exact_graph_vertex_connectivity=4
exact_graph_edge_connectivity=4
minimum_vertex_cuts=6
minimum_edge_cuts=6
root_target_pairs=2510
verified_paths=12550
path_vertex_occurrences=62649
```

An independent algorithmic cross-check uses NetworkX's global vertex- and
edge-connectivity routines rather than the stored paths:

```bash
python3 -m venv /scratch/parts509-connectivity-venv
/scratch/parts509-connectivity-venv/bin/pip install -r \
  hadwiger_nelson_parts509_superconnectivity/requirements.txt
/scratch/parts509-connectivity-venv/bin/python \
  hadwiger_nelson_parts509_superconnectivity/crosscheck_networkx.py
```

Regenerate the compact certificate (all generated environments should remain
under `/scratch`):

```bash
/scratch/parts509-connectivity-venv/bin/python \
  hadwiger_nelson_parts509_superconnectivity/generate_certificate.py
```

Two consecutive generations in the reported run produced byte-identical
certificates.  The committed `certificate.json` has SHA-256

```text
055582c87df462551f883f0295b8cb807f3cd13a45004640e71e1de1ecd5db33
```

and size 256,666 bytes.

## Scope and trust boundary

The primary connectivity proof is positive and solver-free.  The verifier
checks the exact graph hash, every path endpoint, every consecutive edge,
path simplicity, pairwise internal disjointness, all degree and core data,
the six explicit cuts, and certificate completeness using integer graph
incidence only.  NetworkX 3.5 is used to *find* paths and for a separate
global-connectivity cross-check, but it is not trusted by the main verifier.
The remaining implementation boundary is CPython's JSON parser, integer and
set operations, file I/O, and SHA-256 implementation.  The short deduction
from the checked path families to the complete cut classifications is not
formalized in a proof assistant.

This directory does not recheck algebraic coordinates, strict unit-distance
geometry, or 5-chromaticity.  Those facts are inherited from the sibling
`hadwiger_nelson_parts509_criticality` artifact.  The edge input is read from
the sibling exact-completion artifact and accepted only at the canonical hash
above.

## Prior-work and novelty scope

Parts's paper gives the 509-vertex, 2,442-edge strict construction and the
minimization framework, but does not appear to state the connectivity or
minimum-cut classification certified here:

- Jaan Parts, *Graph minimization, focusing on the example of 5-chromatic
  unit-distance graphs in the plane*, Geombinatorics 29(4) (2020), 137--166,
  <https://arxiv.org/abs/2010.12665>.

A targeted primary-literature and repository search through 2026-09-02 found
no published connectivity analysis of this exact graph.  The result is
therefore presented as a verified graph-level structural lemma and as
apparently new to the searched sources, not as an unconditional priority
claim.
