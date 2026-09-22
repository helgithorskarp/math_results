# Order ideals and exact illumination of join zonotopes

Let `i(G)` denote the number of independent vertex sets of a finite simple
graph `G`, **including the empty set**. For a finite poset `P`, let `J(P)`
be its order ideals, including the empty and full ideals, and let `G(P)`
be its comparability graph: two distinct elements are adjacent exactly
when they are comparable. A join `G_1 vee ... vee G_k` retains the edges
inside each factor and includes every edge between different factors.

For a connected graph `G=(V,E)`, `N=|V|>=2`, and strictly positive real
edge weights `w`, work in the `(N-1)`-dimensional space

\[
 H=\{x\in\mathbb R^V:\sum_v x_v=0\},\qquad
 Z_G(w)=\sum_{ab\in E}[-w_{ab}(e_b-e_a),w_{ab}(e_b-e_a)].       \tag{1}
\]

The choice of endpoint order in a segment is immaterial. All interiors
and directions are relative to `H`. A nonzero direction `u` illuminates
`x` when `x+t u` is interior for some `t>0`. The ordinary illumination
number `I` is the least size of a direction set illuminating the boundary.
Its fractional version `I_f` is the infimum of the total mass of a finite
nonnegative Borel measure on the unit sphere of `H` assigning mass at
least one to the illuminating directions of each boundary point.

**Theorem A (exact join formula).** For finite nonempty posets
`P_1,...,P_k`, `k>=2`, let `G=G(P_1) vee ... vee G(P_k)`. Then, for every
strictly positive choice of the weights,

\[
 I(Z_G(w))=I_f(Z_G(w))=i(G)-1
              =\sum_{j=1}^k\bigl(|J(P_j)|-1\bigr).          \tag{2}
\]

There are explicit illuminating directions and an explicit pairwise
antipodal set of vertices of this cardinality. Thus (2) is also the maximum
size of a pairwise antipodal subset of the boundary. Here antipodal means
lying on opposite parallel supporting hyperplanes; the supporting faces
need not be singletons.

Two separate statements give the proof and are useful beyond this class.

**Theorem B (order-ideal lower certificate).** If the comparability graph
of a finite poset `P` is connected and has at least two vertices, then

\[
                 I_f(Z_{G(P)}(w))\ge |J(P)|-1=i(G(P))-1.    \tag{3}
\]

An explicitly constructed set of `|J(P)|-1` vertices is pairwise antipodal.

**Theorem C (common-neighbor upper certificate).** If every nonempty
independent set `S` of a connected graph `G` has a common neighbor outside
`S`, then

\[
                         I(Z_G(w))\le i(G)-1.              \tag{4}
\]

Consequently equality holds for every connected comparability graph
satisfying this common-neighbor condition. Nontrivial joins of comparability
graphs give a direct structural class with this property.

The arguments below prove the universal statements. The accompanying
exact finite checker corroborates the certificates, without replacing
the proofs or constituting independent review or formal verification.
Classical inputs and the novelty boundary are recorded in
[SOURCES.md](SOURCES.md).

## 1. Orientation and support conventions

For an acyclic orientation `D` of `G`, write

\[
                  v_D=\sum_{a\to b}w_{ab}(e_b-e_a).         \tag{5}
\]

A covector strictly increasing along its edges uniquely exposes `v_D`.
Such a covector exists by topological sorting. Conversely a covector
exposing a vertex can be chosen off every edge hyperplane, so (5) gives
all vertices. Distinct acyclic orientations give distinct vertices: a
strict covector for one of them yields a strictly smaller value at the
endpoint sum of the other. Positivity of every edge weight is used.

Directly from the segment sum, the normal cone at `v_D`, modulo constant
vectors, is

\[
                   f_a\le f_b\quad(a\to b\text{ in }D).    \tag{6}
\]

Indeed each segment must separately attain its support value. An upper
set of `D` is a set closed under following directed edges. Successive
upper level sets express every covector in (6) as a constant plus a
nonnegative sum of indicators of nonempty proper upper sets. A
nonconstant covector uses at least one positive coefficient. Thus the
standard strict-normal criterion for illumination gives

\[
 u\text{ illuminates }v_D
 \quad\Longleftrightarrow\quad
 \sum_{v\in U}u_v<0\quad\text{for every nonempty proper upper set }U.
                                                               \tag{7}
\]

Illuminating all vertices suffices for the whole boundary: the normal
cone of a face is contained in the normal cone of any of its vertices.
These conventions and facts are classical graphical-zonotope geometry.
They also show why changing positive weights does not change illumination
conditions; affine equivalence of the resulting bodies is not asserted.

For any covector `f`, the support function is

\[
                 h_Z(f)=\sum_{ab\in E}w_{ab}|f_b-f_a|.      \tag{8}
\]

For nonconstant `f`, connectedness and positive weights imply `h_Z(f)>0`.
In particular the inequalities

\[
 x(U)\le h(U):=\sum_{ab\in\delta(U)}w_{ab}
 \quad(\varnothing\ne U\subsetneq V),\qquad x\in H           \tag{9}
\]

describe `Z_G(w)`. To see sufficiency, decompose any `f` into its successive
upper level-set indicators; its support (8) decomposes with the same
nonnegative coefficients into the cut supports in (9). Thus (9) implies
every support inequality. Strict satisfaction of all inequalities (9)
characterizes the interior. The checker uses these direct weighted
inequalities rather than the combinatorial proofs of the next sections.

## 2. Order ideals give antipodal vertices

Fix `P` as in Theorem B. For each order ideal `A`, orient each comparability
edge as follows: inside `A` and inside `V\A`, follow the poset order; across
the cut, reverse the poset order. Explicitly, for `a<_P b`, orient `a->b`
unless `a in A` and `b notin A`, in which case orient `b->a`. The other
crossing possibility is excluded because `A` is an ideal. Denote this
orientation by `D_A`. It is acyclic: take a linear extension of `V\A`
first, followed by a linear extension of `A`.

The empty and full ideals give the same orientation. Retain all proper
ideals, including the empty one. For two distinct retained ideals `A,B`,
set

\[
                     f=\mathbf1_{A\setminus B}
                           -\mathbf1_{B\setminus A}.       \tag{10}
\]

We claim that `f` is weakly increasing along `D_A` and weakly decreasing
along `D_B`. Put

\[
 C=A\cap B,\quad X=A\setminus B,\quad Y=B\setminus A,
 \quad O=V\setminus(A\cup B).
\]

No element of `X` is comparable to an element of `Y`: either comparison
would violate one of the two ideal conditions. Relations between distinct
remaining classes can only have the poset directions shown below.
Within a class the covector is constant.

| Poset relation | Edge in `D_A` | Values of `f` along it | Edge in `D_B` |
|---|---|---|---|
| `C < X` | `C -> X` | `0 -> 1` | `X -> C` |
| `X < O` | `O -> X` | `0 -> 1` | `X -> O` |
| `C < Y` | `Y -> C` | `-1 -> 0` | `C -> Y` |
| `Y < O` | `Y -> O` | `-1 -> 0` | `O -> Y` |
| `C < O` | `O -> C` | `0 -> 0` | `O -> C` |

This proves the claim. The covector (10) is nonconstant: if constant zero
then `A=B`, while constant `1` or `-1` would require one ideal to be all
of `V`, which was excluded. Equations (5) and (8) now give

\[
                   f(v_{D_A})=h_Z(f)>0,
           \qquad f(v_{D_B})=-h_Z(f)<0.                    \tag{11}
\]

Hence all retained vertices are distinct and every pair is antipodal.
A single direction cannot illuminate both members of an antipodal pair:
it would have to satisfy both `f(u)<0` and `f(u)>0`. Their illuminating
direction sets are therefore pairwise disjoint. Every feasible fractional
measure gives at least one unit of mass to each such set, proving (3).
The identity `|J(P)|=i(G(P))` is the elementary bijection taking an ideal
to its maximal elements, an antichain; its inverse takes an antichain to
its downward closure.

This proves Theorem B independently of the join hypothesis.

## 3. A concentrated negative coordinate illuminates each source class

Assume Theorem C's hypothesis. For each nonempty independent set `S`,
choose a vertex `r=r(S)` adjacent to every element of `S`. Let `s=|S|` and
define an integer vector

\[
 u^S_v=
 \begin{cases}
 N,&v\in S,\\
 -Ns+N-s-1,&v=r,\\
 -1,&v\notin S\cup\{r\}.
 \end{cases}                                               \tag{12}
\]

Its sum is zero; its coordinates on `S` are positive and all other
coordinates are negative. In particular `u^S` is nonzero. Different `S`
give different positive-coordinate sets, so the resulting rays are distinct.

Let `D` be any acyclic orientation whose sources are exactly `S`. Sources
form a nonempty independent set. Consider a nonempty proper upper set `U`.
If `U` avoids `S`, all coordinates in its sum are negative. If `U` meets
`S`, the edge from any source in `U` to `r` forces `r in U`. Also `U` cannot
contain all sources: every vertex of a finite acyclic digraph is reachable
from a source, so an upper set containing all sources would be `V`.
Consequently `|U cap S|<=s-1`, and

\[
 u^S(U)\le N(s-1)+(-Ns+N-s-1)=-s-1<0.                     \tag{13}
\]

All other included coordinates only decrease this upper bound. Equation
(7) proves that `u^S` illuminates every vertex with source set `S`.
Selecting (12) for all nonempty independent sets proves (4), and hence
Theorem C. This uses a particular vector with a large negative coordinate;
it does not claim that the entire source-sign cone illuminates the vertex.

## 4. Matching the bounds for joins

Let `P=P_1 op ... op P_k` be the ordinal sum: retain the orders inside the
factors and declare every element of an earlier factor less than every
element of a later factor. Its comparability graph is exactly the join
in Theorem A, and is connected because `k>=2` and each factor is nonempty.
Every nonempty independent set of this join lies in one factor; any vertex
of a different factor is a common neighbor. Theorems B and C therefore give

\[
                  i(G)-1\le I_f(Z_G(w))\le I(Z_G(w))
                                      \le i(G)-1.
\]

An independent set is either empty or a nonempty independent set of one
factor, proving the last expression in (2). The lower certificate and
upper cover are explicit in (10)--(12). Any pairwise antipodal boundary
set has cardinality at most the number of directions in this cover, since
each direction illuminates at most one of its points. This proves all
assertions of Theorem A.

Taking the `P_j` to be antichains recovers the earlier complete multipartite
formula `sum_j(2^|P_j|-1)`. The new ingredient is compatibility with internal
comparability edges: the ideal-cut orientations replace the earlier cyclic
part construction, and (12) replaces its full source-sign-cone argument.

## 5. A count-preserving reduction and exact counting complexity

Let `H` be any bipartite graph on `n>=1` vertices, with specified bipartition
`L,R`. Give it the height-at-most-two poset order whose strict relations are
`a<b` for edges `ab` with `a in L,b in R`. This is transitive and its
comparability graph is exactly `H`; isolated vertices cause no difficulty.
Join it to a new universal vertex `r`. Formula (2), with one singleton
factor, yields

\[
                  I(Z_{K_1\vee H})=I_f(Z_{K_1\vee H})=i(H). \tag{14}
\]

Delete coordinate `r` from the sum-zero space. This is a linear isomorphism
onto `R^n`, with inverse `x_r=-sum_{i=1}^n x_i`. It maps the segments at
the universal vertex to coordinate segments and retains the other edge
differences. Linear isomorphisms preserve both illumination numbers:
they biject direction rays, and transporting a measure on normalized rays
preserves its mass and illumination constraints. Thus the full-dimensional
unit-weight zonotope

\[
 B_H=[-1,1]^n+
       \sum_{ij\in E(H)}[-(e_i-e_j),e_i-e_j]               \tag{15}
\]

satisfies `I(B_H)=I_f(B_H)=i(H)`.

**Corollary D.** In the graph-indexed family (15), computing either exact
illumination number is `#P`-complete under polynomial-time Turing reductions.
The input is a bipartite graph (a bipartition can be supplied or computed),
and the body is represented by its `n+|E(H)|` integer segment generators,
each supported on at most two coordinates. No vertex or facet expansion
is part of the input.

For hardness, use the classical exact `#BIS` theorem of Provan--Ball
(1983), the Theorem on p.779, item 2. Their reduction convention permits
polynomially many oracle calls; see the definition on p.779 and the
interpolation reduction on pp.782--783. The transformation `H -> B_H` is
polynomial in the graph size and preserves the count exactly by (14)--(15).
For membership, an `n`-bit subset is a witness and is accepted exactly when
it is independent in `H`. There are exactly `i(H)` accepted witnesses.
Malformed or nonbipartite input encodings can be assigned output zero,
so this also defines a total `#P` function with the promised geometric
interpretation on valid inputs. The zero-vertex counting instance has
known value one and may be handled without an oracle.

This corollary concerns the stated compact input class, in growing
dimension. It does not assert `#P` membership for general illumination
problems, parsimonious completeness of `#BIS`, or any approximation
hardness. The known counting hardness is an input, not a new result.

## 6. Scope controls

Connected comparability graphs need not satisfy equality in (3): the
six-cycle is a height-two comparability graph with `i(C_6)=18`, while the
previously established circuit-zonotope formula gives
`I(Z_C6)=I_f(Z_C6)=binom(6,3)=20>17`. Its independent set of three alternating
vertices has no common neighbor, so Theorem C does not apply. Conversely
Theorem C does not require comparability, but Theorem B does; no equality
formula for arbitrary joins is claimed.

Connectedness, the stated ambient space, and strict positivity of all
weights are part of the hypotheses. Removing zero-weight edges can change
the answer (and even the dimension). The earlier theorem characterizing
when the entire source-sign cone works is not contradicted by (12).
No product formula, tensor-power limit, or illumination conjecture is used.

The finite checker uses direct weighted generator sums, all subset support
inequalities, exact positive interior steps, and both permutation-based
and edge-orientation enumeration. It checks the ideal covectors at the
support-function level, ideal/antichain bijections, source directions and
the bipartite reduction. Rejection controls test the strict inequalities
and hypotheses. Its standard-library integer/rational computations are
corroboration; the all-order proof above carries the mathematical claim.
Independent review and historical priority remain unclaimed.
