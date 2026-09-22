# Illumination of complete multipartite graphical zonotopes

Let a finite vertex set `V` be partitioned into nonempty parts
`V_1,...,V_k`, where `k>=2`, `|V_i|=n_i`, and `N=sum_i n_i`.
Let `G=K_(n_1,...,n_k)` be the complete multipartite graph on these parts.
Give every edge `e` a strictly positive real weight `w_e` and define

\[
 H=\{x\in\mathbb R^V:\sum_{v\in V}x_v=0\},\qquad
 Z_G(w)=\sum_{ab\in E(G)}[-w_{ab}(e_b-e_a),w_{ab}(e_b-e_a)].
 \tag{1}
\]

The choice of ordering for the endpoints of an undirected edge does not
affect its segment. Since `G` is connected, `Z_G(w)` has dimension `N-1`
and is full-dimensional in `H`. All interiors and illumination directions
are relative to `H`.

A nonzero direction `u` illuminates `x` if `x+t u` is interior for some
`t>0`. Write `I(Z)` for the least number of directions illuminating every
boundary point. The fractional number `I_f(Z)` is the infimum of the total
mass of a finite nonnegative Borel measure on the unit sphere of `H` which
assigns mass at least one to the illuminating directions of each boundary
point. Two boundary points are *antipodal* here if they lie on opposite
parallel supporting hyperplanes; the supporting faces need not be singletons.

**Theorem 1.** For every positive choice of the weights in (1),

\[
                  I(Z_G(w))=I_f(Z_G(w))=
                  \sum_{i=1}^k(2^{n_i}-1).                 \tag{2}
\]

For each nonempty subset `S` of one part use the direction

\[
                  d_S=N\mathbf1_S-|S|\mathbf1_V.           \tag{3}
\]

These directions illuminate the boundary and work for all positive weights.
There is an explicit antipodal set of the same cardinality, indexed by the
same subsets, which certifies both lower bounds. Consequently this is also
the largest cardinality of an antipodal subset of the boundary.

**Theorem 2 (scope of the source-cone method).** Let `G` be any connected
simple graph on `N>=2` vertices. For an acyclic orientation `D`, let `S(D)`
be its sources and put

\[
 Q_D=\{u\in H:u_s>0\ (s\in S(D)),\quad
                    u_v<0\ (v\notin S(D))\}.              \tag{4}
\]

Every direction in `Q_D` illuminates the vertex corresponding to `D`, for
every acyclic orientation `D`, **if and only if** `G` is complete
multipartite. This statement holds for each positive edge weighting, with
the same characterization. It concerns the entire sign cone (4), not just
the particular vector (3), and is not a classification of all graphs for
which a numerical illumination formula might hold.

The proofs below are complete mathematical arguments. The finite exact
checks in [verify.py](verify.py) corroborate them; they do not replace the
universal quantifiers or constitute independent peer review or formalization.

## 1. Standard normal cones in orientation language

This section recalls classical graphical-zonotope facts, with conventions
fixed for the proof. The normal-fan/acyclic-orientation correspondence and
positive-generator-rescaling invariance are prior work, as recorded in
[SOURCES.md](SOURCES.md).

If `D` is an acyclic orientation, orient its edges from tail `a` to head `b`
and set

\[
                 v_D=\sum_{a\to b}w_{ab}(e_b-e_a).         \tag{5}
\]

A vector `f` which strictly increases along every oriented edge exposes
this vertex: each summand in (1) has its unique maximizing endpoint as in
(5). Such an `f` exists by a topological ordering. The normal cone at `v_D`,
viewed modulo constant vectors, is exactly

\[
                 f_a\le f_b\quad\text{for every }a\to b.
 \tag{6}
\]

Indeed equality of a sum of the segment support values with its maximum
requires equality separately on every segment. Strict positivity of the
weights is used here. Conversely every vertex can be exposed by an `f`
avoiding the finitely many edge hyperplanes `f_a=f_b`, so all vertices
occur in (5). Different acyclic orientations give distinct vertices: a
strictly increasing `f` for one orientation gives a strictly smaller
support value at the endpoint sum of any other orientation.

A set `U` is an *upper set* of `D` if `a in U` and `a->b` imply `b in U`.
For every nonempty proper upper set, `1_U` belongs to (6) and is nonzero
modulo constants. Every nonconstant vector in (6) is a constant vector
plus a nonnegative linear combination of these upper-set indicators, with
at least one positive coefficient: use its successive distinct coordinate
levels and their upper level sets. It follows that

\[
 u\text{ illuminates }v_D
 \quad\Longleftrightarrow\quad
 u(U):=\sum_{v\in U}u_v<0
 \text{ for every nonempty proper upper set }U.            \tag{7}
\]

Here we used the usual polytope criterion that a direction illuminates a
point exactly when it strictly decreases all its nonzero outward normals.
One may equivalently test the finitely many active facet inequalities.
This criterion also shows that illuminating every vertex illuminates the
whole boundary: the normal cone of any face is contained in that of any
one of its vertices. The formulas are independent of the positive weights,
which is the familiar normal-fan invariance, not affine equivalence of the
weighted bodies.

For the lower certificate it is useful to record, directly from (1),

\[
 \max_{x\in Z_G(w)}x(U)=h(U):=\sum_{ab\in\delta(U)}w_{ab},
 \qquad \min_{x\in Z_G(w)}x(U)=-h(U).                     \tag{8}
\]

The point `v_D` attains the maximum when every crossing edge points into
`U`, and the minimum when every crossing edge points out of `U`.
The inequalities `x(U)<=h(U)` for all nonempty proper `U`, together with
`x in H`, describe the entire zonotope. To check sufficiency, decompose
an arbitrary covector into its upper level-set indicators. The same
decomposition of `sum_ab w_ab*|f_b-f_a|` is the corresponding sum of the
cut supports `h(U)`, so these inequalities imply every support inequality.
Strict satisfaction of all of them characterizes its interior in `H`.

## 2. Sources give the upper bound

The sources `S` of an acyclic orientation of a complete multipartite graph
are a nonempty independent set, hence lie in a single part, say `V_i`.
Fix any `s in S`. Every vertex outside `V_i` is an out-neighbor of `s`.
Every nonsource `a in V_i` has an incoming edge from outside `V_i` and is
therefore reachable from `s` in two steps. No source other than `s` is
reachable from `s`. Thus

\[
                   \operatorname{Reach}_D(s)
                   =\{s\}\cup(V\setminus S).             \tag{9}
\]

Let `U` be a nonempty proper upper set and `u in Q_D`. If `U` contains no
source, all its coordinates of `u` are negative, so `u(U)<0`. If `U`
contains a source, (9) implies that it contains every nonsource. Its
nonempty complement is then a subset of `S`, and
`u(U)=-u(V\U)<0`. Equation (7) proves the forward assertion of Theorem 2.

In particular (3) lies in `Q_D`. For each possible source set it is already
in our selected direction set. There are `2^{n_i}-1` nonempty subsets of
`V_i`, and different such subsets give different positive-coordinate sets
and hence different rays. We have proved

\[
                  I_f(Z_G(w))\le I(Z_G(w))
                            \le\sum_i(2^{n_i}-1).         \tag{10}
\]

No small perturbation or genericity of the weights is required. At every
active upper-set support, the integer direction (3) has a strict negative
margin: it is `-|S|*|U|` when `U` avoids `S`, and otherwise it is
`-(N-|S|)*|V\U|`.

## 3. A cyclic antipodal certificate

Fix once and for all a cyclic order of the parts. For each nonempty
`S subseteq V_i`, let `D_(i,S)` orient every edge forward in the block order

\[
      S,\ V_{i+1},\ V_{i+2},\ldots,\ V_{i-1},\ V_i\setminus S,
 \tag{11}
\]

where indices are cyclic and an empty last block is omitted. The blocks
are independent sets, so (11) specifies an acyclic orientation without
choosing orders inside the blocks. Its sources are exactly `S`. Therefore
all `M=sum_i(2^{n_i}-1)` vertices `v_(i,S)` are distinct.

We show that every pair is antipodal.

**Two subsets of the same part.** If `S != T` are subsets of `V_i`, pick
`a in S triangle T`. At one of the two orientations all edges at `a` point
out, and at the other they all point in. The coordinate functional `x_a`
has values `-h({a})` and `h({a})` at the corresponding vertices. Its support
width is positive since `G` is connected. Equation (8) gives the opposing
supporting hyperplanes.

**Subsets of different parts.** Take `S subseteq V_i` and `T subseteq V_j`,
where `i != j`. Traverse the fixed cyclic order from `i` to `j` and put

\[
 L=S\ \cup\!\!\bigcup_{i<_{\rm cyc}\ell<_{\rm cyc}j}V_\ell
       \ \cup\ (V_j\setminus T),\qquad R=V\setminus L.    \tag{12}
\]

In (11) for `(i,S)`, every edge crossing between `L` and `R` points from
`L` to `R`. Although `V_j` is split between the two sets, it has no internal
edges. In (11) for `(j,T)`, every crossing edge points from `R` to `L`;
now the potentially split intermediate part is `V_i`, again with no
internal edges. Consequently

\[
                 v_{(i,S)}(L)=-h(L),\qquad
                 v_{(j,T)}(L)=h(L).                      \tag{13}
\]

Both sides of the cut are nonempty: `S subseteq L` and `T subseteq R`.
In fact the edges between `S` and `T` already give `h(L)>0`. This proves
antipodality for all strictly positive weight assignments.

No single direction illuminates two points on opposite supporting
hyperplanes: it would have to strictly decrease a nonzero functional and
its negative. Thus the `M` illuminating-direction sets of our certificate
vertices are pairwise disjoint. A feasible fractional illuminating measure
has mass at least one on each, and therefore has total mass at least `M`.
Together with (10), this proves Theorem 1. The same reasoning bounds any
antipodal subset of the boundary by the size of our illuminating set, so
the exhibited antipodal set is maximum.

## 4. The exact obstruction to the full sign-cone method

A graph is complete multipartite precisely when it has no induced triple
consisting of one edge and an isolated vertex. For completeness, absence
of such a triple makes nonadjacency, with equality included, an equivalence
relation: a failure of transitivity is exactly such a triple. Its classes
are the independent parts, and all edges between different classes exist.

Suppose now that a connected graph is not complete multipartite. Choose
vertices `a,b,c` with `ab` an edge but `ac,bc` nonedges. Orient all edges
forward in a total order beginning

\[
                              a,c,b,\ldots .              \tag{14}
\]

Let `S` be the sources and `s=|S|`. Then `a,c in S` and `b notin S`.
The upper set `R=Reach_D(c)` does not contain `a` or `b`: a directed path
can only increase in the order (14), and the direct edge `cb` does not
exist. It also contains no source except `c`.

Define an integer direction by

\[
 u_c=N,\qquad u_b=-2s,\qquad
 u_v=1\ (v\in S\setminus\{c\}),\qquad
 u_v=-1\ (v\notin S\cup\{b\}).                           \tag{15}
\]

Its coordinate sum is
`N+(s-1)-2s-(N-s-1)=0`, and its positive coordinates are exactly `S`.
Thus `u in Q_D`. But

\[
                         u(R)=N-(|R|-1)>0.                \tag{16}
\]

The nonempty proper upper set `R` violates (7). This obstruction works for
every positive weighting, because its cut remains an active supporting
functional at `v_D`. It proves the converse of Theorem 2.

## 5. Scope and verification

The theorem specializes to `2^m+2^n-2` for `K_(m,n)` and to `N` for the
ordinary weighted complete-graph permutohedron. The prior two-hub formula
`2^n+2` is recovered at `m=2`; it is credited as an existing graph result,
not republished as a new special case. Stars give the classical
parallelotope value. The contribution is the complete multipartite
formula, its source-based optimal cover, cyclic antipodal certificate,
and the exact characterization of the full source-sign-cone method.

Strict positivity is essential. Deleting one edge of `K_(2,2)` gives a
tree whose three-dimensional zonotope is a parallelotope with illumination
number eight, rather than six. One-part edgeless graphs, arbitrary graphs,
and statements about strict antipodality are outside Theorem 1. Theorem 2
does not say that every individual source-sign direction fails outside
the class; it supplies one explicit violating orientation and direction.

The checker reconstructs weighted vertices and supporting cuts directly,
independently of the reachability proof. It verifies every active cut and
an explicit positive rational interior step, the opposing support values
for every certificate pair, and the invariance under three positive weight
assignments. Topological-order enumeration is compared with exhaustive
edge orientations and cycle rejection in the small cases. The obstruction
in Theorem 2 is separately checked on every connected labelled graph
through five vertices. Tangent/reversed directions and invalid inputs are
rejected. These finite checks use exact integers and rational arithmetic,
with no solver, external dataset, random sampling or floating-point trust
boundary. Historical priority and independent review remain unclaimed.
