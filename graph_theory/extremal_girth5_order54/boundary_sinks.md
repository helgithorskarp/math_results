# Every degree-eight vertex is a sink in the thirteen-vertex boundary

Let `G` be a 54-vertex, 187-edge graph without a triangle or quadrilateral, with exactly 13 vertices of degree eight. A *sink* is a vertex from which every vertex is within distance two.

**Theorem. All 13 degree-eight vertices are sinks. Moreover, the characteristic polynomial of the adjacency matrix is divisible by `(X²+X−7)^12`.**

The degree reduction and weighted gap identity in [proof.md](proof.md) are prerequisites. They import the published upper bound `ex(53,{C3,C4})≤181`. This theorem strengthens the earlier conclusion of at least 12 sinks; it does not exclude the boundary or improve `ex(54,{C3,C4})` numerically.

## A local weighted identity

Keep `w_v=d(v)−6`, `s_v=sum_{u~v}w_u` and `S=sum_v w_v=50`. Write `F(v)` for the vertices at distance greater than two from `v`, and `f_v=sum_{u in F(v)}w_u`. Uniqueness of paths of length at most two gives

\[
\sum_{u\sim v}s_u=S-s_v+(d(v)-1)w_v-f_v. \tag{1}
\]

Indeed, in the left side the starting vertex has multiplicity `d(v)` and each distance-two vertex has multiplicity one. The sum of weights at distance two is `S−w_v−s_v−f_v`.

## Excluding the exceptional vertex

Suppose a degree-eight vertex `t` is not a sink. The previous lemma proves that it is the only such degree-eight vertex, `s_t=4`, and `F(t)={x}`. The vertex `x` has degree six or seven and all its neighbors have degree seven.

If `d(x)=7`, the gap nine is exhausted by `q8(s_t)=5` and the weighted distant pair `{t,x}`. Consequently every other local gap term is zero, `s_x=7`, and `f_x=2`. Every neighbor `y` of `x` has degree seven and satisfies `s_y in {7,8}`. Equation (1) would give

\[
49\le\sum_{y\sim x}s_y=50-7+6-2=47,
\]

which is impossible.

Now suppose `d(x)=6`. The previous equality analysis gives `s_x=6`, `U=0`, and zero local gap at every vertex except `x` and `t`. Thus:

* Every degree-six vertex other than `x` has `s=8`.
* Every degree-seven vertex has `s=7` or `s=8`.
* Every degree-eight vertex other than `t` has `s=5`.

Since `t in F(x)`, we have `f_x≥2`. All six neighbors of `x` have degree seven. Applying (1) gives

\[
42\le\sum_{y\sim x}s_y=50-6-f_x\le42.
\]

Hence `f_x=2` and all six neighbors of `x` have `s_y=7`.

Fix one such neighbor `y`. Let `(a,b,c)` count its neighbors of degrees `(6,7,8)`. The equations `a+b+c=7` and `b+2c=s_y=7` give `a=c` and `b=7−2c`. Because `x` is a neighbor of `y`, `c=a≥1`. The vertex `y` is not adjacent to `t`, since otherwise `dist(x,t)≤2`.

The condition `U=0` implies `f_y=0`: a distant vertex of positive weight would make a positive contribution to `U`, since `w_y=1`. Let `B_y` count the degree-seven neighbors of `y` with `s=8`. Counting the left side of (1) by degree classes, with `x` the unique degree-six exception, gives

\[
\sum_{u\sim y}s_u
=8a-2+7b+B_y+5c
=47-c+B_y.
\]

Equation (1) also gives this sum as `50−7+6=49`. Therefore

\[
B_y=c+2\le b=7-2c,
\]

so `c≤1`. Thus every neighbor of `x` has exactly one degree-eight neighbor. Only six degree-eight vertices can then be within distance two of `x`, because `x` itself has only degree-seven neighbors. But the 12 degree-eight sinks other than `t` must all be within distance two of `x`. This contradiction excludes the degree-six case and proves that all 13 degree-eight vertices are sinks.

## Spectral consequence

Let `A` be the adjacency matrix, `T=V8`, and `H=A[T,T]`. The earlier local ball bound shows that `H` has maximum degree at most two. Write `p(X)=X²+X−7`. For each `t in T`, the sink property and absence of triangles and quadrilaterals give

\[
p(A)e_t=\mathbf1.
\]

Consequently the 12-dimensional space

\[
W=\{x:\operatorname{supp}(x)\subseteq T,\ \mathbf1^Tx=0\}
\]

lies in `ker p(A)`. The two roots `alpha=(-1+sqrt(29))/2` and `beta=(-1-sqrt(29))/2` lie outside `[-2,2]`. Since `A` is real symmetric, `ker p(A)` is the direct sum of its alpha and beta eigenspaces.

Orthogonal projection from `W` onto either eigenspace is injective. For example, a vector in the kernel of projection onto the alpha eigenspace would be a beta eigenvector supported on `T`, making its restriction a beta eigenvector of `H`. This is impossible because every eigenvalue of `H` lies in `[-2,2]`. The same argument applies with the roots interchanged.

Both eigenspaces therefore have dimension at least 12, proving divisibility by `p(X)^12`. This uses elementary spectral linear algebra as an auxiliary consequence of the combinatorial sink theorem; it is not an exclusion of the remaining graphs.

## Verification and scope

Run `python3 verify_boundary.py`. The local weighted identity is checked directly on existing graph controls. An exact rational rank calculation on the existing 185-edge fixture, whose four degree-eight vertices are independent sinks, gives nullity six for `A²+A−7I`, attaining the analogous lower bound `2(4−1)`. The general theorem rests on the written proof, not an extrapolation from that control.

The weighting and boundary deductions are new to this campaign; historical priority is not established. The underlying two-path count and Moore-graph polynomial method are standard. The target remains `185≤ex(54,{C3,C4})≤187`.
