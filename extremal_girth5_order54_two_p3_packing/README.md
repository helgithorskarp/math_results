# Two high paths force the thirteen-high boundary

This note gives a human proof of a structural restriction on a hypothetical
54-vertex, 187-edge graph of girth at least five.  Write

\[
T=V_8(G),\qquad z=|T|,\qquad H=G[T],
\]

and suppose, as follows from the known order-53 upper bound and the
[published degree reduction](../graph_theory/extremal_girth5_order54/proof.md),
that every vertex of `G` has degree 6, 7, or 8.  The degree equations then give

\[
|V_6(G)|=z+4.
\]

The result strengthens the existing high-path restriction: throughout the
remaining range `z <= 12`, the high graph `H` has **at most one** three-vertex
path component.  No enumeration or solver certificate is used.

## Packing theorem

For a high vertex `t`, put

\[
a(t)=|\{v:\operatorname{dist}(t,v)>2\}|,
\qquad L(t)=N(t)\cap V_6(G),
\qquad h(t)=d_H(t).
\]

**Theorem.**  If `H` contains two vertex-disjoint two-edge paths

\[
P=t_1t_2t_3,\qquad Q=u_1u_2u_3,
\]

then

\[
z\ \ge\ 13+
\sum_{i=1}^3 a(t_i)+\sum_{j=1}^3 a(u_j)
+\sum_{i=1}^3\bigl(h(t_i)-d_P(t_i)\bigr)
+\sum_{j=1}^3\bigl(h(u_j)-d_Q(u_j)\bigr).                 \tag{1}
\]

In particular, two vertex-disjoint high `P3`s force `z >= 13`.

Here the paths need not initially be components of `H`; the last two sums
measure their extra high incidences.

### Proof

The radius-two ball around an eight-vertex is a tree through distance two,
because `G` has no triangle or quadrilateral.  If `x_i` denotes the number
of degree-`i` neighbors of `t`, then

\[
x_6+x_7+x_8=8,\qquad
|B_2(t)|=1+\sum_{v\sim t}d(v)=49+x_7+2x_8.
\]

Since `x_8=h(t)` and `|B_2(t)|=54-a(t)`, elimination gives

\[
|L(t)|=x_6=3+a(t)+h(t).                                  \tag{2}
\]

The three sets `L(t_1),L(t_2),L(t_3)` are pairwise disjoint.  Consecutive
path vertices cannot have a common neighbor because that would form a
triangle.  The two endpoints cannot have a common degree-six neighbor
because they already have the common neighbor `t_2`, and the two common
neighbors would form a quadrilateral.  Hence, with
\(U_P=L(t_1)\cup L(t_2)\cup L(t_3)\), equation (2) gives

\[
|U_P|=13+\sum_i a(t_i)+
\sum_i\bigl(h(t_i)-d_P(t_i)\bigr).                        \tag{3}
\]

The analogous formula holds for `U_Q`.

Within each path family the three sets are disjoint.  For every `i,j`,
the two high vertices `t_i,u_j` have at most one common neighbor: two
would form a quadrilateral.  Consequently the nine cells

\[
L(t_i)\cap L(u_j)\quad(1\le i,j\le3)
\]

are mutually disjoint and each has size at most one.  Thus
\(|U_P\cap U_Q|\le9\).  Both unions lie in `V_6(G)`, so (3) and its
counterpart for `Q` imply

\[
z+4=|V_6(G)|
\ge |U_P\cup U_Q|
\ge |U_P|+|U_Q|-9.
\]

Rearrangement is exactly (1).  This proves the theorem.

## Sharp boundary signature

Suppose `z=13`.  Equality in (1) is then forced.  Therefore:

- all six path vertices are radius-two sinks (`a=0`);
- none of the six vertices has a high neighbor outside its displayed path,
  so the paths are components of `H`;
- every one of the nine intersections \(L(t_i)\cap L(u_j)\) is a
  singleton;
- the two 13-point unions cover all 17 degree-six vertices;
- outside their 3-by-3 intersection grid, their row-private and
  column-private parts have sizes `1,2,1`.

The underlying set inequality is sharp: a 3-by-3 grid, one private point
in each endpoint row/column, and two private points in each center
row/column gives exactly 17 points.  This is only a sharp set-system model,
not a claim that a graph realizing it exists.

## Consequence for the order-54 frontier

The existing
[high-path theorem](../graph_theory/extremal_girth5_order54/rooted_completion/high_path_theorem.md)
proves that when `z <= 12`, every component of `H` is `P1`, `P2`, or `P3`.
Combining it with (1) gives the complete uniform normal form

\[
H=mP_2+(z-2m)P_1
\]

or

\[
H=P_3+mP_2+(z-3-2m)P_1.
\]

Thus there is at most one `P3` for every `z <= 12`.  This replaces the
previous weaker `z=11` conclusion allowing two `P3` components and removes
every multiple-`P3` branch from the unresolved `z=9,10,11` completion
framework.  It also supplies a human exclusion of all multiple-`P3`
high-graph cases in the already certified `z=12` layer.

The numerical problem remains open: this note does not decide whether a
187-edge graph exists and does not improve the published interval
`185 <= ex(54,{C3,C4}) <= 187`.

## Reproducibility and status

Run

```sh
python3 verify.py
```

with CPython 3.11 or later.  The output must match
[`EXPECTED_OUTPUT.json`](EXPECTED_OUTPUT.json).  The standard-library
script checks the sharp 17-point signature, all stated cardinalities, the
nine cross intersections, and rejection of a deliberately malformed
two-point intersection.  It is a finite audit of the equality example and
boundary arithmetic; the universal theorem rests on the written proof.

The primary Afzaly--McKay extremal catalogue was checked on 2026-09-21 and
still lists only the lower bound 185 at order 54, while listing the exact
value 181 at order 53:
<https://users.cecs.anu.edu.au/~bdm/data/extremal.html>.
The recent construction paper of Goedgebeur, Jooken, Joret and Van den Eede
concerns improved lower bounds, principally for orders 74 through 198:
<https://arxiv.org/abs/2508.05562>.
No historical priority claim is made for the packing observation.
