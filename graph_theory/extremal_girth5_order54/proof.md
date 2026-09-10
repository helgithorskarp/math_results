# A weighted gap identity and its boundary cases

Current status: the [whole-boundary theorem](boundary_exclusion.md) excludes
every case with thirteen degree-eight vertices, improving the degree bound
to n8<=12. The proof and evidence below are preserved as earlier results.

The later [boundary refinement](boundary_sinks.md) excludes both exceptional alternatives in Section 3, proving that all 13 degree-eight vertices are sinks when `z=13`. The proof below supplies its prerequisites.

All graphs below are finite, simple and undirected. A *sink* means a vertex from which every vertex is at distance at most two. Distance between disconnected vertices is infinity.

## 1. Reduction to three degrees

Import the published value `ex(53,{C3,C4})=181` from the Afzaly–McKay catalogue linked in [README.md](README.md). If `G` has 54 vertices, 187 edges and no triangle or quadrilateral, deleting any vertex shows that its degree is at least six.

In a graph with no triangle or quadrilateral, the vertices encountered at distance one and two from a vertex `v` are distinct. Consequently

\[
|B_2(v)|=1+\sum_{u\sim v}d(u)\le54.
\]

Since the minimum degree is at least six, `6d(v)≤53`, and hence the maximum degree is at most eight. Writing `z=n8` and using the vertex and degree sums gives

\[
n_6=z+4,\qquad n_7=50-2z,\qquad n_8=z,\qquad 0\le z\le25. \tag{1}
\]

## 2. Exact weighted pair count

The following identity applies more generally whenever all degrees belong to `{6,7,8}` and there is no triangle or quadrilateral. Write

\[
w_v=d(v)-6,\quad S=\sum_v w_v=2e(G)-6|V(G)|,
\quad s_v=\sum_{u\sim v}w_u,
\]

and put

\[
U=\sum_{\{u,v\}:\operatorname{dist}(u,v)>2}w_uw_v.
\]

Each unordered pair is represented by precisely one of: an edge; a unique path of length two; or a pair counted in `U`. The absence of triangles makes the first two classes disjoint, and the absence of quadrilaterals makes the common neighbor unique. Therefore

\[
S^2-\sum_v w_v^2
=\sum_v w_vs_v+
\sum_v\left(s_v^2-\sum_{u\sim v}w_u^2\right)+2U.
\]

Because `sum_v sum_{u~v} w_u² = sum_u d(u)w_u²`, this becomes

\[
\sum_v(s_v^2+w_vs_v)+2U
=S^2+\sum_v(d(v)-1)w_v^2. \tag{2}
\]

Define

\[
q_6(s)=(s-8)^2,\quad q_7(s)=(s-7)(s-8),
\quad q_8(s)=(s-5)(s-9).
\]

For degree `6+w`, these polynomials are `s²+(w-16)s+c_w`, with `(c0,c1,c2)=(64,56,45)`. Also `sum_v s_v=7n7+16n8`. Subtracting `16 sum_v s_v` and adding `64n6+56n7+45n8` in (2) yields the exact identity

\[
\boxed{\quad \sum_v q_{d(v)}(s_v)+2U
=S^2-114S+64|V(G)|-19n_8.\quad} \tag{3}
\]

For the target parameters, `S=374-324=50`, so

\[
\boxed{\quad
\sum_{v\in V_6}(s_v-8)^2+
\sum_{v\in V_7}(s_v-7)(s_v-8)+
\sum_{v\in V_8}(s_v-5)(s_v-9)+2U=256-19z.
\quad} \tag{4}
\]

Every term on the left is nonnegative. The weights are nonnegative, the degree-seven factor is the product of consecutive integers, and for degree eight the local ball bound gives `48+s_v≤53`, or `s_v≤5`. Thus `256-19z≥0`, proving

\[
\boxed{n_8\le13.}
\]

This conclusion is conditional only on the explicitly imported order-53 bound; the pair identity itself is unconditional under its stated graph hypotheses. No linear-programming numerical output is used in the proof.

## 3. Degree-eight vertices and the extreme case

A degree-eight vertex has `|B2(v)|=49+s_v`, and is a sink exactly when `s_v=5`. A non-sink has `s_v≤4`, contributing at least five to (4). Hence

\[
\#\{\text{degree-eight sinks}\}\ \ge
\max\left(0,z-\left\lfloor\frac{256-19z}{5}\right\rfloor\right). \tag{5}
\]

In particular there are at least 2, 7 and 12 such sinks when `z=11,12,13`, respectively. Also every degree-eight vertex has at most two degree-eight neighbors, since each contributes two to `s_v≤5`. Thus the subgraph induced by `V8` is a disjoint union of paths and cycles of length at least five, allowing isolated vertices.

Suppose `z=13`. The gap in (4) is nine. Either all 13 degree-eight vertices are sinks, or there is exactly one non-sink `t`. In the latter case `s_t=4` because `q8(3)=12>9`. Thus exactly one vertex `x` is at distance greater than two from `t`.

We claim that `x` has no degree-eight neighbor. To see this, let `A` be the adjacency matrix, `D` the diagonal degree matrix, `J` the all-ones matrix, and `B` the zero-one matrix of pairs at distance greater than two. Uniqueness of paths of length at most two gives

\[
B=J-A^2-A+D-I.
\]

Taking the commutator gives, entrywise,

\[
(AB-BA)_{uv}=(d(u)-d(v))(1-A_{uv}). \tag{6}
\]

If `u` is any of the other degree-eight vertices, its row of `B` is zero because it is a sink. Column `t` of `B` has its sole nonzero entry at `x`. Equation (6) with `v=t` gives `A_ux=0`. Moreover `x` is not adjacent to `t`, by definition. This proves the claim. The vertex `x` cannot have degree eight, since it too would be a non-sink, so its degree is six or seven.

* If `d(x)=6`, then `s_x≤6`, so `q6(s_x)≥4`. Together with the contribution five from `t`, this exhausts the gap nine. Thus `s_x=6`, all six neighbors of `x` have degree seven, every other local `q` term is zero, and `U=0`.
* If `d(x)=7`, the distant pair `{t,x}` contributes two to `U` and hence four to (4). Again the gap is exhausted. In particular `q7(s_x)=0`; since `x` has no degree-eight neighbor, `s_x≤7`, forcing `s_x=7`. All seven neighbors of `x` have degree seven, every local `q` term except that of `t` is zero, and `U=2`.

These alternatives give explicit incidence restrictions for a subsequent graph-realization search. They do not themselves exclude either alternative or the case of 13 sinks.

## 4. A precise limit of aggregate counting

The companion certificate has 54 abstract vertices allocated among 15 neighbor-degree types, with degree counts `(17,24,13)`. Its integer edge counts between types satisfy the necessary constraints specified and checked in `verify.py`, including the simple-graph capacities between types. All its degree-eight types have `s=5` and its total local gap is nine.

Therefore these aggregate constraints, by themselves, cannot exclude `z=13`. The certificate does not assert that its entries can be realized simultaneously on individual vertices. The missing information is the compatibility of individual neighbor sets and the uniqueness of individual length-two paths. The next phase must address that information or supply another universal inequality.
