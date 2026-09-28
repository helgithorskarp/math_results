# Four-edge robustness of a guarded planar triangulation

For a finite unit-edge graph \(G\) with nonnegative vertex masses,
write \(B_w(G)\) if at most two ambient shortest paths can be deleted so
that every remaining connected component has at most half the total
mass. This note concerns one explicit 20-vertex planar triangulation
\(F\) from the [connected guarded-residual
example](../planar_two_geodesic_hybrid_residual20/README.md).

**Exact finite theorem.** Every labelled spanning subgraph \(F-D\)
obtained by deleting at most four of the 54 edges satisfies \(B_w\)
for **every** nonnegative real vertex-mass assignment. This covers
\(\sum_{k=0}^{4}\binom{54}{k}=342{,}541\) distinct edge-deletion
patterns. It is a finite robustness statement, not the all-spanning
property \(B_w^*(F)\) and not a resolution of [Barbados 2026 Problem
31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).

## The certificate-packing rule

A *hybrid template* in \(F\) consists of primary \(F\)-geodesics
\(P,Q\) and, for every component of \(F-(P\cup Q)\) with more than
five vertices, two designated \(F\)-geodesics covering that component.
Every five-vertex residual component must induce something other than
\(K_5\). Its protected set \(E_T\) contains all edges on those paths.
The [all-order hybrid
lemma](../planar_two_geodesic_hybrid_residual20/README.md) says that
\(B_w(F-D)\) holds whenever \(D\cap E_T=\varnothing\). Thus a
collection of templates proves weighted robustness for all deletion
sets that fail to hit at least one protected set. Equivalently, if the
protected-set family has edge-transversal number \(\tau\), it certifies
all deletions of fewer than \(\tau\) edges. This implication is valid
for any finite graph satisfying the templates' local hypotheses.

The compact [`certificates.json`](certificates.json) lists 21 templates.
The checker verifies every listed path against breadth-first distances
in \(F\), the exact residual components, the local non-\(K_5\)
condition, and the coverage by designated paths. It then checks every
edge set \(D\) of size zero through four against their protected edge
sets. Exactly one four-edge set hits all 21:

```text
{(4,12), (5,12), (11,12), (12,13)} = δ_F(12).
```

In particular, the listed protected-set family has transversal number
four, and this is its unique minimum transversal.

Those four deletions isolate vertex 12. The JSON file contains a
separate hybrid certificate in that child graph, with primary residual
orders \(1,6,6\). The checker confirms its paths are geodesic in the
**child graph** and that its two designated pairs cover both six-vertex
components. This closes the sole exception and proves the stated
finite theorem. The 21-template family was selected computationally;
the theorem trusts the published certificate and its verifier, not the
search that selected it. No minimality of 21 templates is claimed.

## Reproduction

From the repository root, using Python 3.11 or later and only its
standard library:

```sh
python3 graph_theory/planar_two_geodesic_template_radius20/verify.py
```

Expected output:

```text
triangulation: 20 vertices, 54 edges, 36 triangular faces
templates: 21 protected edges: 11..15
covered deletion counts k=0..4: [1, 54, 1431, 24804, 316250]
unique uncovered deletion: star of vertex 12; child residuals: [1, 6, 6]
PASS
```

The checker decodes the graph6 record, validates a planar rotation
system with 36 triangular faces, checks all template and fallback
paths, and enumerates all \(342{,}541\) deletion masks. A separate
C++17 bit-mask enumeration reproduced the coverage counts and the
unique four-edge hitting set. The latter is a cross-check of the
finite set calculation, not an independent audit of every path or of
the all-order hybrid lemma. Vertex masses are handled by the proved
lemma, not sampled numerically. The certificate size is a few
kilobytes; no raw graph census or external generator is required.

The method says nothing about edge-deletion sets of size five or more.
In particular, it cannot yet close the witness-edge induction needed
for \(B_w^*(F)\), and it makes no claim about all planar graphs.
