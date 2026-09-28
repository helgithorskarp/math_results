# A four-residual route to weighted two-geodesic separators

For a graph with unit edge lengths, a *geodesic* is a shortest path in the
original graph; singleton paths count. A vertex-mass half separator leaves
every component with at most half the total nonnegative vertex mass. The
paths are chosen before deletion.

## All-order descent lemma

**Four-residual lemma.** Suppose two ambient geodesics \(P,Q\) of a graph
\(F\) have the property that every component of
\(F-(V(P)\cup V(Q))\) has at most four vertices. Then every spanning
subgraph \(H\subseteq F\) that retains all edges of \(P\cup Q\) has a
two-geodesic half separator for **every** nonnegative real vertex-mass
assignment on \(H\).

Indeed, retained paths stay geodesic: edge deletion cannot shorten their
endpoint distances. Every component left by deleting their vertices in
\(H\) is contained in one of the four-vertex components in \(F\). If the
primary pair does not half-balance a mass assignment, there is a unique
remaining component \(C\) with more than half the mass. It has at most four
vertices. Pair its vertices arbitrarily and take shortest paths in \(H\)
between the paired vertices, using a singleton path if needed. These at
most two paths contain \(C\). After their deletion, every remaining
component lies outside \(C\), whose total mass is less than half. This
also covers disconnected \(H\), zero masses, and paths that leave \(C\).

This gives a **weighted witness-edge induction**. Write \(B(F)\) for the
statement that every spanning subgraph of \(F\) has the weighted property
for every mass assignment. If \(P,Q\) are four-residual in \(F\), and
\(B(F-e)\) is known for every edge \(e\) used by \(P\cup Q\), then
\(B(F)\) follows: a spanning subgraph retaining all used edges is handled
above; one missing \(e\) is a spanning subgraph of \(F-e\). Edge count
strictly decreases. In particular, a graph whose components each have at
most eight vertices satisfies \(B(F)\): in a heavy component, cover its
four largest-mass vertices with two geodesics. This is an all-order
certification rule, with no planarity assumption.

## Exact order-16 result

**Computer-assisted finite theorem.** Every 16-vertex simple planar
triangulation with no vertex set of size four whose deletion leaves
components of size at most eight, and with diameter at most three, has a
four-residual pair of ambient geodesics. There are exactly **537,814**
isomorphism classes in this family. Consequently each graph in this family
has a two-geodesic half separator for every nonnegative real vertex-mass
assignment with unit edge lengths. The same conclusion holds for each
spanning subgraph retaining the edges of one four-residual witness pair.

This is a mass-independent witness property on the difficult triangulations
from the [order-16 unweighted census](../planar_two_geodesic_edge_deletion16/README.md).
It does **not** certify the weighted property for every spanning subgraph of
these triangulations: when a witness edge is absent, the weighted induction
requires a certificate for that edge-deleted child. It does not settle
[Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).

## Reproduction and trust boundary

The [plantri 5.8 guide](https://users.cecs.anu.edu.au/~bdm/plantri/plantri-guide.txt)
lists 17,490,241 order-16 triangulations. The plantri 5.8 source tarball
used here had SHA-256
`e78a944116fec9f2c9f5e484206276cc2b0043bae803e9815f4b2683614629b8`.
With GCC 12.2.0 and standard C++17, from the repository root:

```sh
g++ -O3 -std=c++17 -Wall -Wextra -pedantic -o /tmp/planar-hard-filter \
  graph_theory/planar_two_geodesic_edge_deletion15/filter_hard.cpp
g++ -O3 -std=c++17 -Wall -Wextra -pedantic -o /tmp/planar-four-residual \
  graph_theory/planar_two_geodesic_four_residual_mass/check.cpp
set -o pipefail
plantri -g 16 | /tmp/planar-hard-filter 16 | /tmp/planar-four-residual
```

The filter prints to stderr:

```json
{"total":17490241,"no_four_cut":614713,"no_four_cut_diameter_at_most_three":537814}
```

The checker, which rejects a truncated selected stream, prints:

```json
{"hard_roots":537814,"failures":0}
```

The filter validates graph6 syntax, triangulation edge count, every
four-vertex cut, and diameter at most three. The separate `check.cpp`
validates graph6 syntax and edge count again, recomputes BFS distances,
enumerates all ambient geodesics of lengths zero through three, and tests
all pairs against the four-vertex residual bound. Path masks suffice because
only vertex deletion is tested. It does not construct a plane embedding for
each record; planarity and complete nonisomorphic enumeration depend on
plantri. The written lemma, rather than the computation, gives the
all-masses implication.

As an independent path-enumeration control, a Python checker based on
generic breadth-first search and recursive geodesic traversal checks the
399 hard triangulations in plantri residue 0/1000:

```sh
plantri -g 16 0/1000 | /tmp/planar-hard-filter 16 > /tmp/planar-four-residual-sample.g6
PYTHONDONTWRITEBYTECODE=1 python3 \
  graph_theory/planar_two_geodesic_four_residual_mass/audit_sample.py \
  /tmp/planar-four-residual-sample.g6 --expected 399
```

Expected SHA-256 of that stream:
`a1ee18fc00018b938e76cf40925df78f5b69d86f41788babceb04af139e69c92`.
The Python audit checks all geodesic pairs in each sample graph rather than
reusing the C++ length-three path generator. No large raw stream or witness
dump is required or published.
