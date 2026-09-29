# Factorial-size integer witnesses for weighted two-geodesic obstructions

The [weighted reduction](../planar_two_geodesic_weighted_reduction/README.md)
shows that a weighted planar obstruction to the two-geodesic half-separator
question yields an unweighted one. Here is an **explicit finite bound** on the
edge lengths and vertex masses needed at a fixed number of vertices. This
turns the weighted search on each fixed planar order into a finite exact
decision problem. It does not bound the order of a first obstruction and does
not settle [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).

A geodesic is a simple shortest path in the original graph, including a
singleton. Half balance means that every component after deleting the union
of at most two geodesics has mass at most half the original total mass.

## Quantitative witness theorem

**Theorem.** Fix `n >= 3` and set `m=3n-6`. If any planar graph on at most `n`
vertices, with nonnegative real edge lengths and nonnegative real vertex
masses, has no half-balanced union of at most two geodesics, then there is a
simple planar triangulation on some `r <= n` vertices, with `q=3r-6` edges,
with the following properties:

* its edges have positive integer lengths at most `q! <= m!`;
* its vertices have positive integer masses at most `r! <= n!`;
* every pair of vertices has a unique geodesic;
* no union of at most two geodesics is half-balanced.

The bounds are deliberately coarse. They depend only on the number of
variables, not on the number of simple paths or separator pairs. No search
through all integer assignments is claimed to be practical.

There is also an explicit unweighted consequence. Put

```
Bmax = n + 3m(2m! - 1)
F(n) = Bmax + (Bmax + 1)n(n!).
```

Under the theorem's premise, the construction in the weighted reduction
produces a simple unweighted planar obstruction with at most `F(n)` vertices.
Thus, for each fixed `n`, a complete finite search of triangulations and
integer assignments within the stated boxes decides whether a weighted
obstruction of order **at most** `n` exists. This is a finite-order theorem, not a
uniform decision procedure for the unrestricted question.

## Proof

We first use the qualitative steps proved in the weighted reduction. A
disconnected obstruction has a component carrying more than half the total
mass; that component is itself an obstruction. Perturb lengths to positive
generic real values without making any formerly nonshortest simple path
shortest, then perturb masses to positive values while keeping each of the
finitely many failed path pairs failed. Extend an embedding of the connected
graph to a triangulation, assigning every new edge a length greater than the
sum of old lengths. These new edges lie on no geodesic, and their addition
can only merge residual components. We therefore obtain a triangulation
`T` with positive lengths, positive masses, unique geodesics and the same
failure. Its order is `r <= n` and its edge count is `q=3r-6`.

We compress its lengths without changing the unique geodesic pattern. For
each vertex pair `s,t`, let `P_st` be its unique geodesic. Introduce a
variable `x_e` for each edge. Impose

```
x_e >= 1                                      for every edge e,
sum_(e in Q) x_e - sum_(e in P_st) x_e >= 1    for every simple s-t path Q != P_st.
```

The original length vector, after a sufficiently large positive scaling,
satisfies this finite system. Every coefficient is in `{-1,0,1}`. Among its
solutions minimize `sum_e x_e`. A minimum exists because all coordinates
are at least one, and a minimizing face has a vertex. At that vertex `q`
linearly independent tight inequalities give an invertible integer matrix
`A` and right-hand side consisting entirely of ones. Cramer's rule gives
`x_e=det(A_e)/det(A)`. Multiply the entire vector by `|det(A)|`. The resulting
edge lengths are positive integers, still satisfy all geodesic comparisons
strictly, and each is at most `q!`: every determinant involved is of a
`q` by `q` matrix with entries in `{-1,0,1}`, so the Leibniz formula has at
most `q!` nonzero terms of absolute value one. The unique geodesics are
exactly the `P_st`.

Now keep this path system fixed. For each union of at most two of its paths,
choose one residual component `C` that was heavier than half the total mass
in `T`. Introduce a variable `y_v` for each vertex and impose

```
y_v >= 1                                      for every vertex v,
2 sum_(v in C) y_v - sum_(v in V(T)) y_v >= 1  for every chosen C.
```

The original positive masses, after scaling, satisfy these inequalities.
The same minimizing-vertex and Cramer argument applies in dimension `r`:
the heavy-component rows have entries `+1` on `C` and `-1` elsewhere.
Multiplying the minimizing vertex by its basis determinant yields positive
integer masses at most `r!`. Every selected `C` remains strictly heavier
than half the total, so every geodesic pair still fails. This proves the
theorem. The empty path family, if allowed, can be included among the
finitely many rows; its failure is automatic in a connected positive-mass
obstruction.

To obtain `F(n)`, double every integer edge length so it is at least two.
The [explicit three-parallel-path construction](../planar_two_geodesic_weighted_reduction/README.md)
for two geodesics has core order
`B=r+3 sum_e(2x_e-1) <= Bmax`, total vertex mass
`A=sum_v y_v <= n(n!)`, and final unweighted order
`N=B+(B+1)A <= F(n)`. Its proof protects each original edge with three
replacement paths and realizes masses by pendant leaves. Thus its output is
an unweighted planar obstruction. `□`

## Exact reproducible controls

Run from the repository root with Python 3.11 or later, standard library
only:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_bounded_weighted_witness/verify.py
```

The checker constructs every simple path of a five-edge diamond and derives
its path-comparison rows from an integer metric. It independently enumerates
the vertices of that small rational polyhedron with exact Gaussian
elimination, scales a minimizing vertex by its basis determinant, and verifies
all path comparisons and the `5!` bound. It also checks directly that the
unit-edge `K_9` with unit masses is a **nonplanar** weighted obstruction:
all its geodesics are singletons or edges and all 1,035 unordered pairs of
45 paths fail half balance. For that control, the mass inequalities selected
from all path pairs are checked by the all-one integer vector, within the
`9!` bound. `K_9` is only a logic control; it is not a planar witness.

The proof, rather than either finite control, establishes the arbitrary
finite-order compression theorem. The checker uses no solver or floating
point arithmetic. The factorial bounds are sufficient, not claimed sharp;
no historical priority claim is made for this elementary polyhedral
compression.
