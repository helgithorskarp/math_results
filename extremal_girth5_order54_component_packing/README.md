# Uniform packing of high path components at order 54

Let `G` be a simple graph on 54 vertices with 187 edges and girth at least
five.  Import the exact order-53 upper bound 181.  Deleting one vertex and
using the radius-two ball bound then gives

\[
d(v)\in\{6,7,8\}\quad(v\in V(G)).
\]

Put

\[
T=V_8(G),\qquad z=|T|,\qquad H=G[T].
\]

The degree equations give `|V_6(G)|=z+4`.  This note proves a uniform
packing inequality for any one or two high paths of orders at most three,
then specializes it to path components.  It extends the preceding two-`P3`
packing result and gives new restrictions on the still unresolved
single-`P3` and matching classes.

## Component-packing theorem

For a high vertex `t`, define

\[
a(t)=|\{v:\operatorname{dist}(t,v)>2\}|,
\qquad L(t)=N(t)\cap V_6(G).
\]

For a path `P` in `H`, put

\[
A_P=\sum_{t\in V(P)}a(t),\qquad
E_P=\sum_{t\in V(P)}\bigl(d_H(t)-d_P(t)\bigr).
\]

Thus `E_P` counts the high incidences leaving the displayed path, with an
edge joining two displayed paths counted once at each end.  For two
vertex-disjoint paths `P,Q`, let `q(P,Q)` be the number of cross-pairs
`(t,u) in V(P) times V(Q)` for which `t,u` are neither adjacent in `H` nor
have a common high neighbor.

**Path-packing theorem.**  Suppose `P` is a path of order `r` in `H`, where
`1 <= r <= 3`.  Then

\[
z\ge 5r-6+A_P+E_P.                                         \tag{1}
\]

If `P,Q` are vertex-disjoint high paths of orders `r,s <= 3`, then

\[
z\ge 5(r+s)-8-q(P,Q)+A_P+A_Q+E_P+E_Q.                    \tag{2}
\]

In particular, if `C=P_r` and `D=P_s` are distinct components, then

\[
\boxed{\ z\ge 5(r+s)-rs-8+A_C+A_D.\ }                    \tag{3}
\]

The deficit-free component thresholds in (3) are:

| components | threshold on `z` |
|---|---:|
| `P1, P1` | 1 (the trivial vertex count raises this to 2) |
| `P1, P2` | 5 |
| `P1, P3` | 9 |
| `P2, P2` | 8 |
| `P2, P3` | 11 |
| `P3, P3` | 13 |

### Proof

For `t in T`, let `x_i(t)` be the number of its degree-`i` neighbors and
write `h(t)=d_H(t)`.  The girth condition makes the radius-two ball a tree
through distance two, so

\[
54-a(t)=|B_2(t)|=1+\sum_{u\sim t}d(u)
             =49+x_7(t)+2x_8(t).
\]

Together with `x_6+x_7+x_8=8` and `x_8=h(t)`, this gives

\[
|L(t)|=x_6(t)=3+a(t)+h(t).                                 \tag{3}
\]

If `P=P_r` for `r<=3`, the sets `L(t)`, `t in P`, are pairwise disjoint.
Sets belonging to adjacent high vertices cannot meet, since a common
neighbor would make a triangle.  For the two endpoints of a `P3`, the high
center is already one common neighbor, so a degree-six common neighbor would
make a quadrilateral.  By the definition of `E_P`,
`sum_{t in P}h(t)=2(r-1)+E_P`.  Hence

\[
|U_P|:=\left|\bigcup_{t\in P}L(t)\right|
       =5r-2+A_P+E_P.                                      \tag{4}
\]

Because `U_P` lies in the `z+4` degree-six vertices, (4) gives (1).

Now take vertex-disjoint paths `P,Q`.  If a cross-pair is adjacent, its
`L`-sets are disjoint by triangle-freeness.  If it has a common high
neighbor, a degree-six common neighbor would make a quadrilateral.  Every
other cross-pair has at most one common neighbor.  The cross-intersections
are mutually disjoint because the `L`-sets are internally disjoint within
each displayed path.  Therefore

\[
|U_P\cap U_Q|\le q(P,Q).
\]

Using (4) for both paths,

\[
z+4\ge |U_P\cup U_Q|
\ge (5r-2+A_P+E_P)+(5s-2+A_Q+E_Q)-q(P,Q),
\]

which rearranges to (2).  For distinct components, `E_P=E_Q=0` and every
cross-pair is eligible, so `q(P,Q)=rs`; this gives (3).  Taking `r=s=3`
and merely using `q(P,Q)<=9` recovers the preceding two-`P3` theorem even
when the displayed paths are not initially components.

## Equality signature

When equality holds in the component bound (3), every intermediate
inequality is an equality:

- the `rs` cross-intersections are all singletons;
- `U_C union U_D` is the whole of `V_6(G)`;
- a vertex `t` inside `C` has exactly
  `3+a(t)+d_C(t)-s` degree-six neighbors private from `U_D`;
- symmetrically, a vertex `t` of `D` has
  `3+a(t)+d_D(t)-r` private points.

At the deficit-free threshold, a complete sharp set-system signature is
obtained from an `r`-by-`s` grid: each row and column receives the indicated
number of private points.  This realizes the set inequality exactly for all
six unordered pairs `(r,s)`.  It is not a claim that the entire graph is
realizable.

## Structural consequences

The preceding high-path theorem establishes that for `z<=12`, every
component of `H` is `P1`, `P2`, or `P3`, and for `z<=8` the graph `H` is a
matching with isolates.  Equations (1) and (3) therefore imply:

1. For `z<=4`, the high graph is edgeless.  Indeed a `P2` needs `z>=4` by
   (1), while at `z=4` either of the two remaining high vertices forms a
   `P1` component and (3) requires `z>=5`.
2. For `5<=z<=7`, the high graph has at most one edge, since two `P2`
   components require `z>=8`.
3. At `z=5`, if the high graph has an edge, every high vertex is a
   radius-two sink: applying the equality case to that `P2` and each `P1`
   forces every involved deficit to vanish.
4. At `z=8`, if the high graph has at least two edges, every endpoint of a
   high edge is a sink, and every chosen pair of edges has the sharp
   2-by-2 grid signature on the twelve degree-six vertices.
5. At `z=9` or `z=10`, if `H` has a `P3`, every other high vertex is
   isolated.  The `z=10` assertion is new: a simultaneous `P3` and `P2`
   would require `z>=11`.
6. At `z=11`, coexistence of a `P3` and a `P2` is an equality case.  All
   five vertices are sinks; their degree-six neighborhoods form a complete
   3-by-2 intersection grid and cover all fifteen degree-six vertices.

More generally, (3) bounds the sum of the deficits on any selected pair of
components by `z-[5(r+s)-rs-8]`.  This is a quantified restriction rather
than a finite list of searched instances.

These conclusions remove whole high-component classes but do not decide a
complete degree class and do not improve the numerical interval
`185 <= ex(54,{C3,C4}) <= 187`.

## Reproduction and status

Run, using CPython 3.11 or later and no third-party packages,

```sh
python3 verify.py
```

and compare the output with [`EXPECTED_OUTPUT.json`](EXPECTED_OUTPUT.json).
The script constructs all six sharp grid signatures directly from their
definitions, checks every internal disjointness and cross-intersection
condition, verifies the threshold formula and private-part sizes, and
rejects a deliberately malformed double intersection.  It audits the
finite equality table; the universal result rests on the written proof.

The [Afzaly--McKay extremal catalogue](https://users.cecs.anu.edu.au/~bdm/data/extremal.html)
was refreshed on 2026-09-21 and still lists the exact value 181 at order 53
and only the lower bound 185 at order 54.  The 2025 construction paper of
[Goedgebeur, Jooken, Joret and Van den Eede](https://arxiv.org/abs/2508.05562)
does not settle order 54.  A targeted search found no published version of
this component-packing statement; no historical priority claim is made.

The imported degree reduction and earlier high-path theorem are available
in the repository at
[`proof.md`](../graph_theory/extremal_girth5_order54/proof.md) and
[`high_path_theorem.md`](../graph_theory/extremal_girth5_order54/rooted_completion/high_path_theorem.md).
The preceding two-`P3` special case is
[`extremal_girth5_order54_two_p3_packing`](../extremal_girth5_order54_two_p3_packing/).
