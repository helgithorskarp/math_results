# Proof

All complexes here are finite abstract simplicial complexes. A closed
triangulated surface is connected, each edge has two incident triangular
facets, and each vertex link is a circle. Put `f=f_2(T)` and `G=(sd T)^(1)`.
Vertices of `G` are all nonempty faces of `T`; **every strict containment** is
an edge. Thus its triangles are precisely the `6f` flags `(v,e,F)` with
`v in e subset F`. Packings are graph-edge-disjoint; covers consist of graph
edges. Coefficients of chains are `F_2` unless stated otherwise.

## 1. The previously established orientation identity

We recall the proof so that the topological bridge has a self-contained
combinatorial foundation. The identity and the following hexagon argument
belong to the earlier [orientation-gap package](../barycentric_triangle_orientation_gap/PROOF.md).

The six flags in one facet have triangle-conflict graph `C_6`. Its two
independent triples correspond to the two cyclic orientations of that facet:
select `(v,e,F)` when `v` is the initial endpoint of its oriented boundary
edge `e`. Triples in adjacent facets are compatible exactly when the induced
orientations of their shared edge are opposite.

Let `kappa` be the minimum number of facets one must delete to admit coherent
orientations on all remaining facets. Every packing uses at most three flags
per facet, and the facets using three admit coherent orientations. At least
`kappa` facets therefore use at most two flags, proving `nu <= 3f-kappa`.

Conversely select the three orientation flags in a coherent complement of a
minimum deletion set. Reinsert each deleted facet with two flags. Each of
its three sides has just one neighboring facet, whose packing can forbid at
most one of that side's two flags. At least three vertices of its `C_6` remain
available. They contain an independent pair because `C_6` has no triangle.
Inserting that pair preserves the packing, so `nu >= 3f-kappa`.

There is a cover of size `3f`: all containment edges `(v,F)`. Every graph edge
belongs to exactly two flag triangles, so assigning weight `1/2` to every
flag is a fractional packing of size `3f`. Weak LP duality gives

```text
tau = tau* = nu* = 3f,            nu = 3f-kappa.                 (1)
```

Fix reference orientations on the facets. Let `delta` be the minimum number
of inconsistent shared edges over all facet orientations. Deleting one
incident facet per inconsistent edge shows `kappa <= delta`. Starting with
an optimal coherent deletion complement, orient deleted facets one at a time
by majority among their already oriented neighbors. There are at most three
such neighbors, so each insertion creates at most one inconsistency. Each
edge is counted only on inserting its later endpoint. Hence `delta <= kappa`.
This subcubic equality is also Sivaraman's prior frustration theorem [S2].

## 2. Characteristic-cycle formula on every closed surface

Sum the reference-oriented facets as an integral 2-chain `U`. Every edge
coefficient in `boundary U` is zero or `+/-2`. Therefore

```text
z0 = (boundary U)/2
```

is an integral 1-cycle: integral chain groups are torsion-free and
`2 boundary z0=0`. Its reduction modulo two is exactly the set `X0` of
inconsistent edges. Flipping the orientations of a subset `A` of facets
toggles precisely its mod-2 boundary. The possible inconsistent sets are
therefore exactly

```text
X0 + im(boundary_2).                                          (2)
```

In particular all are cycles and their common homology class is intrinsic.
It is `PD(w1(T))`: along any closed dual curve transverse to the primal edges,
local orientation transport reverses precisely at crossings of inconsistent
edges. Its mod-2 intersection with `X0` thus evaluates the orientation
character `w1` on that curve. This is the defining cellular intersection
description of Poincare duality. It also proves directly that the class
vanishes exactly when a coherent global orientation exists.

Combining (1), `delta=kappa`, and (2) proves the claimed general identity

```text
tau(G)-nu(G) = min{|X| : X in Z_1(T;F_2), [X]=PD(w1(T))}.       (3)
```

A minimizing support has at most one edge on the boundary of each triangle:
otherwise toggling that triangle changes its cardinality by `3-2r<0`, where
`r>=2` is the number of its selected edges. Its edges thus form a matching
in the facet dual. This observation makes the reconstruction below explicit.

## 3. Projective-plane optimization and witnesses

For `T` triangulating `RP^2`, `H_1(T;F_2)` has dimension one and `PD(w1)` is
its nonzero element. Decompose a nonzero cycle into edge-disjoint simple
cycles. At least one summand has nonzero homology. A minimum nonzero cycle
is consequently a single simple cycle. On `RP^2`, a simple cycle is
homologically nonzero exactly when it is noncontractible. Writing `s` for
the shortest such length, (3) becomes

```text
tau=3f,                       nu=3f-s.                        (4)
```

Here is a complete polynomial algorithm, using standard homology-cover
shortest paths rather than claiming a new shortest-cycle technique [S5].

1. Form `X0` and the binary boundary matrix `B2`. Solve for an edge cochain
   `lambda` such that `lambda B2=0` and `lambda(X0)=1`. A solution exists
   since `X0` is not a boundary. Because the homology dimension is one,
   `lambda(X)=1` exactly for nonzero homology cycles.
2. Build the two-sheet graph with vertices `(v,b)`, `b in F_2`, and edges
   `(u,b)--(v,b+lambda(uv))`. Run BFS from `(v,0)` to `(v,1)` for every base
   vertex `v`. A lifted path projects to a closed walk of odd `lambda` value;
   conversely every such walk lifts between those endpoints. The minimum
   distance is therefore `s`. A minimizing projected walk is simple: a
   repeated vertex would split it into two shorter closed walks, at least
   one with odd value, contradicting global minimality.
3. For the minimizing cycle `X`, solve `B2 a = X+X0`. Flip the facets in `a`.
   The inconsistent edges are exactly `X`. By the last paragraph of section
   2 their dual edges form a matching. Delete one incident facet per edge;
   these are `s` distinct facets, and their complement is coherent. Apply
   the hexagon completion from section 1 to obtain `3f-s` packing triangles.

The cover `(v,F)` has size `3f`. The cocycle, shortest-path labels, cycle,
orientation flips, and final packing supply exact checks at each bridge.
Gaussian elimination takes at most cubic time in the input size; all the
BFS runs together take `O(v(v+e))=O(f^2)` time. No enumeration of facet
orientations is needed by this algorithm. The exhaustive orientation checks
in `verify.py` are separate corroboration on small fixtures.

## 4. A small-order reduction using a published classification

We use Katzman/Adamaszek's theorem [S3]: a flag complex on at most ten vertices
has torsion-free integral `H_1`; exactly four eleven-vertex graphs have clique
complexes with torsion. The four graph6 records, from the primary source,
are included in `fixtures.json`. Classification completeness is an external
published computer-assisted input, not a claim reproduced here.

Suppose a projective-plane triangulation has no essential 3-cycle. Every
nonfacial graph triangle is then contractible and bounds a disk. Replace
the triangulated disk by a single face. Because the triangle was nonfacial,
its disk contains an interior vertex; so the operation reduces the vertex
count. It preserves the surface and retains a subgraph of the old graph.
The replacement is homeomorphic relative to the boundary, so essential
cycles in the new triangulation remain essential in the original one.
Repeat until every graph triangle is facial.

The resulting triangulation is flag. Indeed, a `K_4` would have all four
triangles facial, giving a tetrahedral sphere component, impossible in a
connected projective plane; larger cliques contain `K_4`. Its integral
`H_1` is `Z/2`, so the classification implies at least eleven vertices.
Consequently every projective-plane triangulation on at most ten vertices
has edgewidth three.

If the original triangulation has eleven vertices, either it already has
an essential triangle or the final flag triangulation must be one of the
four classified graphs. Two records have edges in more than two triangles
and cannot be surface triangulations. The other two have twenty faces and
an essential 4-cycle. Explicitly, in graph6 order the surface records are

```text
JCpVTqu\rZ?      essential cycle 0,3,9,6,0
JCR`upvvd]?      essential cycle 0,3,6,10,0.
```

The backslash in the first record is literal. Their nonzero cocycles are
in `expected.json`; the checker verifies the cycle edges, even evaluation
on every triangular boundary, and odd evaluation on the displayed cycle.
It also checks vertex links and Euler characteristic. Thus

```text
n<=10  =>  s=3;                 n=11  =>  s<=4.               (5)
```

## 5. Sharp uniform ratio, including all equality cases

We use the classical projective-plane systolic estimate `s<=2 sqrt(n)` of
Liu–Pelsmajer [S4, Theorem 5]. Only that weaker estimate is required.
For clarity, the cut-disk path lemma in their section 5 suffices: cut along
a shortest essential `s`-cycle; their Lemma 27 supplies disjoint level paths
with at least `2j+1` vertices, for `0<=j<=floor(s/2)`. Retain only levels
`j<=r=floor((s-1)/2)`. Their union lies in a radius-`r` ball in the cut disk.
Projection back to `T` is injective there: two distinct copies of a boundary
vertex would give a path between those copies of length at most `2r<s`,
contradicting shortest essential length. Hence
`n >= sum_{j=0}^r (2j+1) = (r+1)^2`, which implies `s<=2 sqrt(n)`.
This avoids any counting of identified vertices at distance exactly `s/2`.

Euler characteristic and edge-facet incidence give `f=2n-2`, `e=3n-3`.
Simplicity gives `3n-3 <= n(n-1)/2`, whence `n>=6`.
We prove `s<=3f/10 = 3(n-1)/5`, with equality only at `n=6`.

* For `6<=n<=10`, (5) gives `s=3`, so equality holds precisely at `n=6`.
* For `n=11`, (5) gives `s<=4<6`.
* For `n=12,13`, the integer bound `s<=floor(2 sqrt(n))` gives respectively
  `s<=6<33/5` and `s<=7<36/5`.
* For `n>=14`, `2 sqrt(n)<3(n-1)/5`: after squaring, the difference is
  `9(n-1)^2-100n`. It is `121>0` at `n=14`, and its increment when `n`
  increases by one is `18n-109>0`.

Equation (4) now yields `nu>=27f/10` and therefore

```text
tau(G)/nu(G) <= 10/9,
with equality if and only if T has six vertices.              (6)
```

The ten facets in `fixtures.json` give an actual six-vertex projective
plane: the checker verifies its closed surface links and Euler
characteristic one. Its essential triangle, 27-triangle packing, and
30-edge cover certify attainment. Thus (6) is a sharp theorem on the
entire specified class, not an asymptotic estimate or a table.

## 6. Order of the deficit and a source countercheck

The preceding upper bound immediately gives
`tau-nu=s<=2 sqrt(n)=sqrt(2f+4)`.
Its square-root order cannot be reduced. Take the uniform triangular
`k`-grid refinement `T_k` of the six-vertex projective plane, so `f_k=10k^2`.
This familiar construction appears in [S4]; we need no asserted exact
systole for it.

Here is an elementary lower bound. For each original vertex `v`, its global
piecewise-linear barycentric coordinate `b_v` changes by at most `1/k` along
a refinement edge. At any refinement vertex `p`, some `b_v(p)>=1/3`.
If a cycle through `p` has length `L<2k/3`, every point on it is at graph
arc distance at most `L/2` from `p`, so `b_v>0` all around the cycle.
It lies in the original open star of `v`, a disk, and is contractible.
Thus `s(T_k)>=2k/3`. Subdividing an original essential triangle gives
`s(T_k)<=3k`. In particular

```text
2k/3 <= tau(G_k)-nu(G_k) <= 3k,
1/(45k) <= tau(G_k)/nu(G_k)-1 <= 1/(10k-1).                   (7)
```

These inequalities prove the claimed optimal orders without guessing an
exact formula or importing one from a parameter table.

There is a useful correction to the illustrative exact value in [S4].
For `k=2`, write `m_ab` for the midpoint of original edge `{a,b}`. The cycle

```text
m_02, m_01, m_13, m_34, m_24, m_02
```

has five refinement edges, lying respectively in the original faces
`012,013,134,234,024`. It is homotopic, by moving across those faces, to
the original cycle `0,1,3,4,2,0`. The original edge cochain supported on
`14,15,23,25,34` evaluates evenly on every facet boundary and oddly on
this cycle. It is therefore essential. This explicitly disproves the
claimed value `3k=6` for this refinement; the exact cover calculation gives
edgewidth five. The source's vertex count also must be `5k^2+1` by Euler's
formula. The standard icosahedron/antipode construction and its quotient
isomorphism to our fixture are checked in `verify.py`, so the countercheck
does not depend on an unspecified alternative six-vertex triangulation.
The general upper bound used in section 5 is a separate statement.

## 7. Why the characteristic class cannot be omitted

For orientable surfaces it vanishes, so (3) gives `tau=nu`, even on a torus
with essential cycles. The supplied connected sum of two six-vertex
projective planes is a nine-vertex, eighteen-facet Klein bottle. Exact
enumeration of its `2^17` orientation supports gives characteristic minimum
four, while a nonboundary triangle exists. Thus replacing `PD(w1)` in (3)
by an arbitrary nonzero homology class, or replacing its minimum by ordinary
edgewidth on all nonorientable surfaces, is false.

All general assertions above follow from the proof and the precisely named
literature inputs. The fixture computations check implementations, finite
source data, extremal attainment, and the stated scope obstruction; they do
not stand in for an unperformed triangulation census.
