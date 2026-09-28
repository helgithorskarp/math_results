# Eight-vertex residual descent for weighted two-geodesic separators

All graphs below are finite and simple, have unit edge lengths, and may
carry arbitrary **nonnegative real vertex masses**. A singleton counts
as a shortest path. A path union is *half-balanced* if each component
left after its deletion has at most half the total mass.

## Dynamic mass lemma

**Theorem.** Let \(k\geq1\). In any connected graph \(D\) on at most
\(4k\) vertices, under any nonnegative masses, at most \(k\) shortest
paths of the ambient graph can be chosen so that every component of
\(D\) remaining after their deletion has mass at most half the mass
of \(D\).

**Proof.** Select the \(\min(2k,|D|)\) heaviest vertices of \(D\),
pair them arbitrarily, and join each pair by an ambient geodesic.
The selected vertices carry at least half the mass of \(D\), since
\(|D|\leq4k\). The chosen paths contain them, and deleting vertices
cannot merge components. \(\square\)

**Eight-residual template.** Let \(F\) be any graph and let
\(P_1,\ldots,P_k\) be \(F\)-geodesics such that every component of
\(F-\bigcup_i V(P_i)\) has at most \(4k\) vertices. Every spanning
subgraph \(H\subseteq F\) retaining all edges of these paths has a
half-balanced separator of at most \(k\) **\(H\)-geodesics**, for every
nonnegative mass assignment. Consequently, if this property is
already certified for every \(F-e\) where \(e\) lies on a designated
path, it holds for all spanning subgraphs of \(F\).

Indeed, retained paths stay geodesic when other edges are deleted.
If the primary union is unbalanced in \(H\), there is a unique
component \(D\) of \(H-\bigcup_i V(P_i)\) with mass greater than half
the total \(W\). It lies in an original residual component and has at
most \(4k\) vertices. Apply the dynamic mass lemma to \(D\), taking
geodesics in \(H\). Its remaining pieces weigh at most
\(w(D)/2\leq W/2\). Each component outside \(D\) weighs at most
\(W-w(D)<W/2\), and vertex deletion cannot join components. The
edge-deletion assertion follows by splitting spanning subgraphs of
\(F\) according to whether they retain every protected edge.

**Four-vertex guard corollary.** If \(S\subseteq V(F)\) has at most
\(2k\) vertices and every component of \(F-S\) has at most \(4k\)
vertices, then *every* spanning subgraph of \(F\) has the weighted
\(k\)-geodesic half property. In a connected heavy component of the
spanning subgraph, pair the vertices of \(S\) it contains and take
geodesics through them; the template argument applies to their
residuals. For \(k=2\), the guard has four vertices and its residual
components may have **eight** vertices. No planarity assumption is
needed. This strengthens the earlier
[five-vertex guard](../planar_two_geodesic_four_guard/README.md) and
supplies a reusable terminal rule for witness-edge induction.

The threshold \(4k\) is sharp for this general mass lemma: in the
unit-edge complete graph \(K_{4k+1}\) with uniform masses, \(k\)
geodesics cover at most \(2k\) vertices and leave a connected
component of order \(2k+1\), greater than half.

## Exact 20-vertex radius-eleven certificate

Apply the template to the published [20-vertex planar
triangulation](../planar_two_geodesic_template_radius20/README.md),
whose graph6 record and independently checked spherical rotation
system are in the linked source. All 425 geodesics and their 90,525
unordered pairs are enumerated. Exactly 1,759 pairs leave residual
components of order at most eight, with 1,759 different sets of path
edges. The minimum protected-edge count is five. One such pair is

```text
[0,1,6]   [3,10,19,15]
```

Its five path edges leave residual components of orders six and seven.
It certifies the weighted two-geodesic property for the triangulation
and every spanning subgraph retaining those five edges.

The checker then performs an exact transversal search on **all** 1,759
protected-edge sets. A deletion set that avoids every template must
meet each protected-edge set. At a partial deletion set, the search
chooses an unhit template and branches on each of its edges. No
transversal with at most eleven edges exists; memoization visits
3,632,861 distinct partial deletion sets. Therefore **all** spanning
subgraphs obtained by deleting at most eleven edges from this
triangulation have a weighted two-geodesic half separator. There are
\(\sum_{j=0}^{11}\binom{54}{j}=126{,}218{,}400{,}676\) such labeled
edge-deletion patterns. This extends the earlier
[radius-five certificate](../planar_two_geodesic_template_radius20/README.md).
It does **not** certify the remaining edge subgraphs or settle the
universal [Barbados Problem
31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).

## Reproduce

From the repository root, run:

```sh
python3 graph_theory/planar_two_geodesic_eight_residual/verify.py
```

The standard-library checker imports the graph and embedding audit
from `planar_two_geodesic_template_radius20/verify.py`, independently
enumerates its geodesics, tests every path pair, and searches the
template hypergraph. It requires Python 3.11 or later. Expected final
line:

```text
PASS: all edge deletions of size at most 11 retain a template
```

The all-order weighted statements are proved above; the finite
computation certifies only the specified 20-vertex graph and the
specified deletion radius. No priority claim is made for the dynamic
mass observation.
