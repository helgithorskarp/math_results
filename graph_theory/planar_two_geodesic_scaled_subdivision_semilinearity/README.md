# An exact scaling law for geodesic separators on a fixed skeleton

Fix a nonempty finite simple graph \(F=(V,E)\), positive integer lengths
\(L_e\), a fixed integer \(q\geq1\), and a fixed rational
\(0\leq\alpha\leq1\). Let \(F_k\) replace edge \(e\) by a unit path of
length \(kL_e\), for integer \(k\geq1\). A singleton is allowed as a
shortest path. Define \(B(k)\) to mean that **at most \(q\) shortest
paths in the full unit graph \(F_k\), with arbitrary interior endpoints**,
have a vertex union whose deletion leaves every connected component with
at most \(\alpha |V(F_k)|\) vertices.

**Theorem.** The set \(\{k\geq1:B(k)\}\) is effectively semilinear. In
particular it is ultimately periodic: there are computable integers
\(k_0\geq1\) and \(p\geq1\) such that \(B(k+p)\) and \(B(k)\) have the
same truth value for every \(k\geq k_0\). An explicit existential
Presburger formula for \(B(k)\) uses at most \(2q\) integer location
variables besides \(k\); all other disjunctions are finite and depend
only on \(F,L,q\). Thus a fixed scaled-subdivision family has a finite,
exact decision procedure, even when its unit graphs have unbounded
order. Planarity is preserved when \(F\) is planar, but is not needed
for the theorem.

For [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf),
take \(q=2\) and \(\alpha=1/2\). This theorem says that the success or
failure pattern along **one fixed, commonly scaled metric skeleton**
eventually repeats. It does not determine the pattern for the
[32-vertex skeleton and its marked subdivisions](../planar_two_geodesic_thirty_site_subdivision_guard/README.md),
and does not settle the question over all planar graphs.

## Finite formula construction

There are at most \(2q\) path endpoints. For each endpoint, choose a
base vertex of \(F\) or the interior of a base edge. On each edge,
choose a weak order of the endpoints placed there, including all
coincidences. These are finitely many **placement types** independent of
\(k\). In one type, put an integer coordinate \(x_i\) on each distinct
interior endpoint, measured from a fixed end of its edge. The conditions
that an endpoint is interior and that the chosen order holds are linear
integer inequalities in \(k,x_1,\ldots,x_r\), where \(r\leq2q\).

Split each base edge at its chosen endpoints. Call the resulting fixed
combinatorial graph \(H\). Each edge \(a\) of \(H\) represents a unit
chain of length \(\ell_a\), where \(\ell_a\) is an *affine integer form*
in \(k,x_1,\ldots,x_r\); the placement constraints enforce
\(\ell_a\geq1\). There are at most \(|V|+2q\) vertices and
\(|E|+2q\) edges in \(H\). Every simple path in \(F_k\) whose endpoints
are among the chosen endpoints contracts to a simple path in \(H\), and
every simple path in \(H\) expands uniquely to one in \(F_k\).

Enumerate a simple \(H\)-path \(P_j\) for each of the \(q\) requested
paths. Fewer than \(q\) paths can be padded with repeated singletons:
deleting extra vertices cannot worsen balance. Each selected path is a
shortest path **in the original full graph** exactly when

\[
 \sum_{a\in P_j}\ell_a\ \leq\
 \sum_{a\in R}\ell_a
 \quad\text{for every simple \(H\)-path \(R\) with the same endpoints.}
\]

This is a finite list of linear inequalities. The competing paths may
use the terminal vertices of other chosen paths; all such routes are
already present in \(H\).

To express balance, mark the vertices of \(H\) lying on one of the
\(P_j\) as deleted, and mark every \(H\)-edge traversed by a \(P_j\)
as deleted. For each **untraversed** edge \(a=uv\), make one auxiliary
vertex of weight \(\ell_a-1\), representing all its interior unit
vertices, and join it to whichever of \(u,v\) survive. Each surviving
vertex of \(H\) has weight one. The connected components of this
auxiliary graph have exactly the sizes of the residual components of
\(F_k\), apart from harmless zero-weight phantom components when
\(\ell_a=1\). The auxiliary topology is fixed for the placement and
path types. Each component weight is therefore affine in
\(k,x_1,\ldots,x_r\). Since

\[
 |V(F_k)|=|V|+\sum_{e\in E}(kL_e-1)
          =k\sum_eL_e+|V|-|E|,
\]

the bound \(w(C)\leq\alpha|V(F_k)|\) is another linear integer
inequality after clearing the fixed denominator of \(\alpha\).

Conjoin placement, geodesicity, and component inequalities; then
existentially quantify the location variables and disjoin over all
placement and path types. This is the promised effective existential
Presburger formula in the one free variable \(k\). The classical
[Ginsburg--Spanier semilinearity theorem](https://www.csa.iisc.ac.in/~deepakd/atc-common/ginsburg-spanier-PJM-1966.pdf)
and effective Presburger elimination yield a finite union of arithmetic
progressions and finite sets. That is the asserted ultimate
periodicity. For a particular skeleton, computing its preperiod and
period would turn verification at finitely many scales into a proof
about **all** its scales; no such computation is asserted here.

The construction also works for disconnected \(F\): only endpoint
pairs joined by an \(H\)-path can be selected. It can equally use any
fixed rational component threshold; the half threshold is the case
relevant to Problem 31.

## Reproducible check and scope

From the repository root, with Python 3.11+ and no third-party package:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_scaled_subdivision_semilinearity/verify.py
```

Expected output:

```text
skeletons=2 scales=1,2,3 configurations=576 geodesic_pairs=728 PASS
```

`verify.py` tests the central contraction and component-weight identity
on a diamond with a chord and a four-cycle, each at scales one through
three. For 576 deterministic four-endpoint placements it enumerates
simple paths in the refined graph, compares their lengths with
independently computed unit-graph distances, and checks the residual
component sizes of 728 pairs against explicit unit-graph deletion.
These small checks test the encoding. The all-scale theorem rests on
the finite-type proof and Presburger semilinearity, not on the sampled
scales. The procedure may be too large for a generic implementation on
the 32-vertex skeleton; no tractable bound or Problem 31 resolution is
claimed.
