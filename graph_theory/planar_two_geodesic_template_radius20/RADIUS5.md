# A five-edge frontier for guarded geodesic descent

Let \(F\) be the connected 20-vertex planar triangulation and let
\(B_w(H)\) denote the two-geodesic half-balance property for **every**
nonnegative vertex-mass assignment, as defined in the [four-edge
certificate](README.md). All edges have unit length. The question behind
this work is [Barbados 2026 Problem
31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).

**Exact finite theorem.** Every spanning subgraph \(F-D\) with at most
five deleted edges has \(B_w\). There are
\(\sum_{k=0}^{5}\binom{54}{k}=3{,}505{,}051\) such labelled graphs.
This strengthens the four-edge result by using child-specific
geodesics; it does not establish \(B_w^*(F)\) or the universal planar
statement.

## Minimal-transversal frontier

For any graph with valid guarded templates whose protected edge sets
form a family \(\mathcal E\), every deletion \(D\) either misses a member
of \(\mathcal E\), in which case that template certifies \(B_w(F-D)\),
or contains a minimal transversal of \(\mathcal E\). Consequently a
radius-\(r\) proof needs to check only descendants of minimal
transversals \(T\), with at most \(r-|T|\) further deletions. This is an
exact combinatorial reduction; it does not assume that weighted
half-balance is monotone under arbitrary edge deletion.

For the 21 templates in [`certificates.json`](certificates.json), the
unique transversal through size four is the star
\(\delta_F(12)=\{(4,12),(5,12),(11,12),(12,13)\}\). Among the
\(\binom{54}{5}=3{,}162{,}510\) five-edge deletions, exactly 2,665 hit
every root template: 50 contain that star and 2,615 are new minimal
transversals. The verifier obtains these counts by enumerating all
five-edge masks; no generated list is trusted.

In 2,659 of these 2,665 child graphs, two **child-graph geodesics**
leave only residual components of order at most five. The verifier
reconstructs and checks one pair for each child. The local five-vertex
non-\(K_5\) condition is checked as well, so the all-order
[hybrid residual lemma](../planar_two_geodesic_hybrid_residual20/README.md)
gives \(B_w\) for every vertex-mass assignment.

The remaining six deletions are the star plus one of
\((0,4),(2,9),(5,6),(9,17),(14,19),(16,19)\). The single
[`radius5_star.json`](radius5_star.json) template is checked in
\(F-\delta_F(12)\). Its primary residual orders are \(1,5,6\), its
secondary pair covers the six-vertex component, and its 12 protected
edges avoid all six listed edges. The template therefore survives each
of those six further deletions. This closes the radius-five frontier:

| Five-edge class | Number | Certificate |
| --- | ---: | --- |
| Misses a root protected set | 3,159,845 | Published root template |
| Hits every root set, has a five-residual child pair | 2,659 | Recomputed and checked child pair |
| Hits every root set, uses the star-child template | 6 | One compact hybrid certificate |

The six are exactly the five-edge children for which the verifier finds
no five-residual pair. This last classification depends on complete
child-geodesic enumeration; the positive theorem only needs the
verified witnesses and complete deletion-mask coverage.

## Reproduce

From the repository root, with Python 3.11 or later and only the
standard library:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  graph_theory/planar_two_geodesic_template_radius20/verify_radius5.py
```

The final three lines are:

```text
five-edge cases: root templates 3159845 five-residual children 2659 star fallback 6
total certified deletion patterns through radius five: 3505051
PASS radius five
```

The checker first reruns [`verify.py`](verify.py), including the planar
rotation audit and every radius-four deletion. It then checks the
new star-child certificate, enumerates all 3,162,510 five-edge masks,
and verifies each child-specific path against exact breadth-first
distances. Geodesic paths are generated deterministically, but their
validity and residual components are checked again before they count
as witnesses. The proof does not sample vertex weights. The finite
calculation uses the written [all-order lemma](../planar_two_geodesic_hybrid_residual20/README.md)
for the universal mass quantifier. Deletions of six or more edges remain
outside this certificate.
