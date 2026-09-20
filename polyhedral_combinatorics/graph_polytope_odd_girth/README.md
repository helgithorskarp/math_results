# Odd girth from the Ehrhart series of a graph polytope

For a finite simple graph G on d vertices, put

    P_G = {x in [0,1]^d : x_u+x_v <= 1 for uv in E(G)},
    L_G(n) = |n P_G intersect Z^d|,
    F_G(t) = sum_(n>=0) L_G(n)t^n,
    H_G(t) = (1-t^2)^(d+1) F_G(t).

**Theorem.** For nonbipartite G of odd girth g, the zero of H_G at -1 has
exactly order g. Equivalently the reduced denominator of F_G is

    (1-t)^(d+1) (1+t)^(d-g+1).

The Ehrhart quasipolynomial has minimal period two. Bipartite graphs have
period one. These assertions include disconnected graphs and isolates.

There is also a positive geometric formula. For each unoriented shortest
odd cycle C, let F_C be the face obtained by fixing its coordinates to
1/2, and measure its (d-g)-volume in the remaining coordinate lattice
(unit cube volume one, point volume one). In the unique decomposition

    L_G(n) = A_G(n) + (-1)^n B_G(n),

the polynomial B_G has degree d-g and leading coefficient

    2^(-g-1) sum_C vol_(d-g)(F_C).

If all shortest odd cycles are dominating, this coefficient becomes
`number_of_shortest_odd_cycles / 2^(d+1)`. The domination hypothesis is
essential; [PROOF.md](PROOF.md) gives a five-vertex counterexample to
dropping it.

The proof classifies the highest-dimensional faces with nonintegral
affine span, computes their common positive parity jump, and applies
Berline--Vergne's local Euler--Maclaurin formula. This is an analytic
mathematical proof with that explicit imported theorem. The finite
checker corroborates it; it is neither a proof by extrapolation nor a
formalization. Independent review of this new proof is not asserted.

## Reproduce

From this directory, with Python 3.11 or newer and only its standard library:

```sh
python3 verify.py
python3 -O verify.py
sha256sum -c SHA256SUMS
```

Both Python commands print the exact [expected.json](expected.json) and
fail if their computed object differs. They write no files. The manifest
checks all five substantive files. The checker has no downloaded inputs,
randomness, floating-point decisions, solver, or previous research imports.

The checks cover:

- All 1,099 labelled simple graphs on one through five vertices: 672
  nonbipartite and 427 bipartite; 3,481,968 integer assignments and
  4,396 unused interpolation holdout values.
- Independent direct counts for 68 small instances; independent interval
  and clipped-rectangle calculations of all relevant face volumes.
- Seven cycle or independent-vertex cycle-blow-up fixtures and five
  complete graphs, including larger odd girth and dimension. These blow-ups
  impose pairwise edge inequalities, not weighted block-sum inequalities.
- 2,040 slack-lattice parity cases, 676 proper-face integral-translation
  cases, and five malformed graph rejections. The local-jump values in the
  output evaluate the proved character product; they do not independently
  implement the full Berline--Vergne construction.

The all-small-graph record digest is
`75879a24f5193b627d5d3008074a986bb67140fb7e4b7a208daa037faa908d75`.
The full finite records are reconstructed in memory, not distributed as
a large dataset. None of the universal quantifiers rests on these fixtures.

## Scope and provenance

[SOURCES.md](SOURCES.md) identifies the primary literature and exact imported
theorem locations. Half-integrality, bipartite integrality, individual odd
cycles, and several special-family formulas are prior results. The claimed
advance relative to the searched sources is the exact all-graph odd-girth
pole order and positive shortest-cycle-face volume formula. No exhaustive
priority claim, gamma-positivity assertion, or root classification is made.

The graph-first starting point was the reviewed odd-cycle parity result
recorded in SOURCES.md. This arbitrary-graph theorem contains its width-one
case but does not subsume the whole weighted-block theorem.
