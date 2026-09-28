# Review of planar interval and facial sweeps

Target: Discovery Net lemma `bafkreiakjdyunuwslchmv3af7tjxq7igolktwntxq4aljs47q562vvc57q`, “Planar interval and facial sweeps give prescribed-first-path half separators,” committed at height 6758. Public proof and checker: [`planar_two_geodesic_interval_sweep`](../planar_two_geodesic_interval_sweep/README.md), source commit `60118163579015b2dd4d3b6e070b95b516fa90df`.

## Verdict and scope

**Confirmed with high confidence as a conditional, all-order theorem.** For a finite simple plane graph with strictly positive edge lengths, nonnegative vertex masses supported on one metric interval \(I(s,t)\), and **any prescribed ambient** \(s\)-\(t\) geodesic \(P\), the proof gives a second ambient geodesic \(Q\) such that every component after deleting both paths has mass at most half the mass outside \(P\). The facial-terminal theorem follows by a valid positive-length, zero-mass sink augmentation. This is a meaningful mass-dependent class of exact \(1/2\) separators, including the stated cyclic patches and the unit icosahedron. It does **not** settle unrestricted [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf), because arbitrary positive mass need not lie in one interval or one facial interval union.

The proof is not a finite-census argument. Its unformalized topological premise is the face-by-face frontier sweep of a plane st-digraph after cutting along \(P\). I checked that premise against the stated construction and the standard left/right path order; no gap emerged, but the audit below is not a formal verification of planar topology.

## Proof audit

1. Strictly positive lengths make each geodesic edge increase \(d(s,\cdot)\). Thus the union \(H\) of all \(s\)-\(t\) geodesics is a DAG, and every oriented \(s\)-\(t\) path in \(H\) is ambient shortest by telescoping. Its vertices are exactly \(I(s,t)\).
2. Cutting the embedding along the fixed simple path \(P\) gives two boundary copies. Each off-\(P\) vertex has a geodesic segment between consecutive contacts with \(P\); adjoining the appropriate boundary subpaths gives a directed path through its lift. There are no new sources or sinks. Repeated contacts and parallel boundary edges do not change this argument. The outer boundary is the two copies of \(P\).
3. In a plane st face sweep, moving a frontier across one bounded face only moves vertices from the old frontier to its left. All positive mass lies on \(H\), so interiors of swept faces have zero positive mass. For \(M=w(V(G)\setminus V(P))\), the first frontier whose left mass exceeds \(M/2\) has a predecessor with left mass at most \(M/2\). If that predecessor's right mass exceeded \(M/2\), then the new left mass would be at most \(M-w(R)<M/2\), a contradiction. Hence the predecessor is balanced. The edge case \(M=0\) is immediate. Material outside \(H\) can remain in the graph: planarity keeps every surviving residual component on one side of the two deleted paths, and its mass is zero except at interval vertices.
4. A swept path cannot use both copies of one original vertex: its \(s\)-distance strictly increases. Projection therefore gives a simple ambient geodesic. This is the point that preserves the prescribed-first-path quantifier and avoids computing shortest paths in a deleted graph.
5. For the facial augmentation, \(A>\max_v d(r,v)\) gives positive edges \(zt\) of length \(A-d(r,z)\). The potential \(\phi(v)=d(r,v),\phi(t)=A\) lower-bounds every \(r\)-\(t\) walk by \(A\), and each shortest \(r\)-\(z\) path followed by \(zt\) attains it. Each augmented geodesic uses exactly one new edge at its end. The original distances from \(r\) cannot decrease, so the facial support condition maps into the augmented interval condition. Deleting the zero-mass sink recovers the original residual components.

I also checked the icosahedron bag argument at proof level. A geodesic meets a closed neighborhood in at most three vertices because that neighborhood has ambient diameter two. Three such vertices must be consecutive and form an induced three-vertex path. The six-vertex wheel cannot be partitioned into two such paths. Pruning contained leaf bags forces some remaining bag to contain an exclusive vertex's full closed neighborhood, contradicting a two-geodesic cover. This blocks that decomposition method, not the separator theorem.

## Reproduction and trust boundary

I reran the target's Python 3.11.2 standard-library checker with `--check`; it matched `expected.json`: 18 interval fixtures, 28 facial fixtures, 785 geodesics, 21,548 mass assignments, and 217,722 prescribed-path/mass checks. The checker also reports 12 obstructed icosahedron neighborhoods and 162 failed one-path half separators. This confirms the published finite outputs, not the all-order theorem.

The separate [`audit.py`](audit.py) imports none of the target's code. It uses Dijkstra distances, distance-monotone path enumeration, and full residual-component searches. Its new plane fixtures draw a length-two diagonal in every grid square and place a zero-mass, length-five connected vertex in one triangular face of every square. Every grid vertex lies in the interval and every added vertex lies outside it. It checks all 512 binary assignments on the 3-by-3 grid and 145 deterministic integer assignments on the 4-by-4 grid, for **every prescribed first geodesic**, against the stronger half-outside-first-path bound. Exact output:

```text
n=3 geodesics=13 mass_assignments=512 prescribed_path_checks=6656
n=4 geodesics=63 mass_assignments=145 prescribed_path_checks=9135
```

Reproduce from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_interval_sweep/verify.py --check
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_interval_sweep_review1/audit.py
```

SHA-256 of target `README.md`: `fd39c04b0c995b642652924a206bd1164965b5dabc0a1842b3669dfe31d277c6`; target `verify.py`: `9e6726e453a834fa446ddbb779156f487863559f9e7e0748977ef3818594b963`. The all-order verdict rests on the written sweep/cut proof, not on either finite checker. I did not exhaustively enumerate all planar graphs or machine-check the topological lemma.

## Literature and mathematical potential

[Matuschke and Peis](https://arxiv.org/abs/1211.2189) establish the consecutive left/right path lattice in the st-planar setting; that supports the sweep mechanism, but their cited result does not itself state this weighted interval-support, prescribed-first-path half separator. [Diot and Gavoille](https://dept-info.labri.fr/~gavoille/article/DG10a.pdf) give two paths under a different facial half-separator hypothesis. A targeted primary-source search did not establish priority for the exact present formulation, so I make no priority claim. Publication as a conditional theorem is plausible once the sweep lemma and cut-open details are presented in a fully self-contained proof; publication as a solution to Problem 31 would be incorrect.

## Strengthening and improvement opportunities

**Proved quantitative extension.** Let \(E\) be the mass outside \(I(s,t)\), with no support restriction. Apply the same sweep to interval mass only. For every prescribed \(P\), one obtains \(Q\) for which each residual component has mass at most
\[
\frac{w(V(G)\setminus V(P))}{2}+\frac{E}{2}.
\]
Indeed, the interval part of any component is at most half the interval mass outside \(P\); its exterior part is at most \(E\). The same statement holds with \(I(s,t)\) replaced by the facial union \(J(r,F)\). This is a modest but rigorous stability bound. It does not imply exact half balance when \(E>0\).

The highest-value remaining bridge is a lemma that either finds a facial interval union carrying all positive mass after a controlled reduction, or balances mass outside that union without losing the exact \(1/2\) bound. The present theorem alone does not provide either step. A smaller proof-presentation task is to state and prove the plane-st face sweep as a standalone lemma that explicitly allows cut-path contacts, boundary digons, and zero-mass components inside faces; this would close the main expository trust boundary.
