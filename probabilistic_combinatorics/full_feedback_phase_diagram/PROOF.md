# Three transitions for universal full-feedback one-round resolution

All logarithms are natural. A graph is finite, simple, and labelled. In a
connected graph, the full directional response to a probe at `v` and target
`x != v` is the set of all neighbors of `v` on shortest `v,x` paths; the
response for `x=v` is `{v}`. A vertex resolves in one round when these
responses, as `x` ranges over all vertices, are distinct.

Write `U(G)` for the event that **G is connected and every vertex resolves
in one round**. This is stronger than the existence of a winning adaptive
one-probe strategy. In particular, failure of `U` gives no lower bound
greater than one for the adaptive game.

## 1. The complete probability law

Let `G ~ G(n,p)`, `q=1-p`, and put

```
S(n,p) = (n^3 p^2 / 2) exp(-np^2),
D(n,p) = (n^3 q^2 / 2) exp(-2nq).
```

**Theorem 1.** Uniformly for `log(n)/(2n) <= p <= 1`,

```
P(U(G)) = exp(-S(n,p)-D(n,p)) + o(1).                 (1)
```

Uniformly for `0 <= p < log(n)/(2n)`, `P(U(G))=o(1)`.
Here uniformity means that the supremum of the absolute error over the
specified interval tends to zero. This is an additive asymptotic formula,
not a relative approximation to very small probabilities.

Thus there are three transition windows:

| Scaling, for fixed real c or fixed a >= 0 | Limit of P(U) |
|---|---|
| `np^2 = 2 log n + log log n + c + o(1)` | `exp(-exp(-c))` |
| `nq = (log n)/2 + log log n + c + o(1)` | `exp(-exp(-2c)/8)` |
| `n^(3/2) q -> a` | `exp(-a^2/2)` |

In particular, as edge density increases, universal one-round resolution
appears at the first window, disappears at the second, and returns at the
third. Equation (1), together with the low-density clause, also covers all
intermediate regimes and arbitrary oscillating sequences of probabilities.

Let `B(G)` be the number of vertices that fail to resolve in one round
when G is connected; define `B(G)=n` when G is disconnected.

**Theorem 2 (critical defects).** In the three rows of the table,
respectively,

```
B(G) => 2 Poisson(exp(-c)),
B(G) =>   Poisson(exp(-2c)/8),
B(G) =>   Poisson(a^2/2).                              (2)
```

The first expression is twice one Poisson random variable. It is not a
Poisson variable of twice the mean. The defect pairs are asymptotically
vertex disjoint at the sparse transition. At either dense transition,
the defective probes are the centers of pairs of degree-one neighbors in
the complement, with no repeated center with high probability.

## 2. Deterministic defects and exact first moments

For a graph G define:

* `Z`: the number of unordered nonedges with no common neighbor;
* `X`: the number of unordered nonedges with exactly one common neighbor;
* `T`: the number of indices `(v,{x,y})`, where `x,y` are distinct
  nonneighbors of v and `N(v) intersect N(x) = N(v) intersect N(y)`;
* `Y`: the number of indices `(v,{x,y})` such that x and y each have
  degree one in the complement H, with their unique neighbor equal to v.

The common traces in T may have any size, including zero. A Y-index is
always a T-index, so `0<=Y<=T`. All unordered pairs are counted once.

If `{v,x}` is an X-pair with unique common neighbor w, then the response
at v to targets w and x is `{w}`. Thus X-pairs make both endpoints fail.
If a Y-index exists, either v is isolated in G or both x and y return
exactly `N_G(v)` at v: they are adjacent in G to every vertex except v.
Consequently `X>0` or `Y>0` implies failure of U.

If `Z=0`, every nonedge has a common neighbor, so G has diameter at most
two. Responses at a probe v then have the following exhaustive forms:
`{v}`, singletons `{x}` for neighbors x, and the common-neighbor traces
for nonneighbors x. They are all distinct exactly when v is neither an
endpoint of an X-pair nor the center of a T-index. In particular,

```
P(X=0) - E(Z+T) <= P(U) <= P(X=0),                    (3)
0 <= P(Y=0)-P(U) <= E(Z+X+T-Y).                      (4)
```

These inequalities do not assert that diameter two is necessary for U.
For example, the three-dimensional cube has U and diameter three.

For `n>=3`, set `b=1-p^2` and `a=1-2p^2q`. Independence of edges gives

```
E Z = binom(n,2) q b^(n-2),
E X = binom(n,2) q (n-2)p^2 b^(n-3),
E T = n binom(n-1,2) q^2 a^(n-3),
E Y = n binom(n-1,2) q^2 p^(2n-5).                  (5)
```

For T, after fixing the two nonedges vx,vy, an outside vertex w fails to
distinguish the traces with probability
`q+p(p^2+q^2)=a`. The required edge triples for distinct w are disjoint;
the edge xy is unrestricted. For Y, two complement edges are required
and exactly `2n-5` complement edges are forbidden. This includes xy.

We shall use the exact identity

```
a = p^2 + q^2(2p+1).                                (6)
```

## 3. Sparse defects: dependence, second moments, and Poisson law

Throughout this section suppose

```
log(n)/(2n) <= p <= sqrt(3 log(n)/n),
lambda=np^2,   M=(n^2 lambda/2) exp(-lambda).
```

Uniformly in this range, p tends to zero, `np^3=o(1)`, and

```
E X = (1+o(1)) M.                                   (7)
```

The relative estimate is valid even when M diverges or tends to zero.
It follows by expanding `log(1-p^2)=-p^2+O(p^4)` in (5).

### Exact two-event probabilities

Let `z=P({1,2} is an X-pair)`. For two distinct pairs sharing one endpoint,
the exact joint probability, for `n>=5`, is

```
A = q^2 [ (n-3)p^3 h^(n-4)
          + (n-3)(n-4)p^4 q^2 h^(n-5) ],
h = 1-2p^2+p^3.                                    (8)
```

The unique witnesses can be the same outside vertex (first term) or two
different vertices (second term). The forced nonedges prevent witnesses
inside the three distinguished vertices. For every other vertex, the
probabilities of witnessing both pairs, just either one, or neither are
`p^3`, `p^2q`, `p^2q`, and h.

For two pairs with disjoint endpoints put

```
b0=(1-p^2)^(n-4),
b1=(n-4)p^2(1-p^2)^(n-5).
```

The exact joint probability is

```
J = q^2 [ (q^4+4pq^3+2p^2q^2)b1^2
          +4p^2q^2 b0 b1 +4p^3q b0^2 ].             (9)
```

Indeed, inspect the four edges between the two endpoint pairs. Zero or
one edge, or either two-edge matching, gives no internal witnesses. The
four adjacent two-edge sets give one internal witness for exactly one
pair. The four three-edge sets give one witness for each pair. All four
cross edges give two witnesses and cannot occur in the event. Conditional
on these four edges, the outside witness counts for the two pairs are
independent binomials: their underlying edges have disjoint endpoints.

Equations (8)--(9) imply uniformly in the stated range

```
A/z^2 = O(1+1/(np)) = O(1),
J/z^2 <= 1+o(1).                                    (10)
```

For (8), divide the exponential factors by `(1-p^2)^(2n)` and use
`n[p^3-p^4]=o(1)`; the two prefactors have orders `1/(np)` and 1.
For (9), the ratio of b1 to `z/q` is
`[(n-4)/(n-2)](1-p^2)^(-2)=1+O(1/n+p^2)`.
Also `b0/b1=(1-p^2)/[(n-4)p^2]`, and the two additional terms after
division by b1 squared are `O(1/n)` and `O(1/(n^2p))`. The coefficient
of b1 squared is at most one. All error terms tend to zero uniformly.

There are `(n)_3` ordered overlapping pairs of pair-indices and
`(n)_4/4` ordered disjoint ones. Here `(n)_r` is a falling factorial.
Thus if M tends to infinity, (7)--(10) imply

```
Var(X)/(E X)^2 <= 1/(E X)+O(1/n)+o(1) -> 0.          (11)
```

In that case `P(X=0)->0` by Chebyshev's inequality.

### The finite-mean limit

Suppose `M->eta`, with `0<eta<infinity`. The lower bound on np and (7)
force

```
lambda = 2 log n + log log n - log eta + o(1).        (12)
```

To see why the small-lambda branch cannot occur, note that for lambda at
most one, `M >= c n log^2 n`; if lambda stays in a bounded interval above
one, M also diverges. Then take logarithms in the definition of M,
using `lambda<=3 log n`.

Fix k. In the factorial moment `E(X)_k`, first consider k pairs with all
`2k` endpoints distinct. For each outside vertex, the k witness indicators
use disjoint edges, so their k binomial counts are independent. Requiring
all edges among the `2k` endpoints to be absent gives a lower bound; just
requiring each outside count to be at most one gives an upper bound.
Since p tends to zero and lambda tends to infinity, both bounds are

```
(1+o(1)) [lambda exp(-lambda)]^k.
```

There are `(1+o(1))(n^2/2)^k` such ordered tuples.

It remains to bound tuples with overlapping endpoints, not assume their
independence. Regard their k pairs as the edges of a fixed simple graph
F on r vertices, where `r<=2k-1`. A given outside vertex witnesses at least
one F-edge with probability

```
s_F = k p^2 + O_k(p^3).
```

This follows from inclusion-exclusion: the intersection of two distinct
edge-witness events needs at least three edges from that outside vertex.
If all k pairs have exactly one common neighbor, at most k outside
vertices can witness any F-edge. Those outside events are independent.
Consequently the joint probability is at most

```
P(Bin(n-r,s_F)<=k)
  = O_k((1+lambda)^k exp(-k lambda))
  = O_k(n^(-2k)).                                   (13)
```

Here `np^3=o(1)` justifies the exponential estimate and (12) the last
bound. Summing over `O_k(n^(2k-1))` overlapping tuples is o(1).
Therefore `E(X)_k -> eta^k` for every fixed k, proving

```
X => Poisson(eta).                                  (14)
```

For completeness, the factorial-moment criterion used here and below
needs no independence assertion. The first moment gives tightness; the
next factorial moment gives uniform integrability of each lower moment.
Every subsequential limit therefore has factorial moments eta^k.
Tonelli's theorem gives its generating function at `1+t`, for `t>=0`, as
`sum eta^k t^k/k! = exp(eta t)`, which determines the Poisson law.

### Transfer to actual directional responses

If M is bounded, lambda is at least `2 log n` for all sufficiently large
n. This follows directly from the lower endpoint bound above and the
monotonicity of `lambda exp(-lambda)` for lambda greater than one.
By (5), uniformly along any such sequence,

```
E Z = (1+o(1)) M/lambda = o(1),
E T <= n^3 exp(-2 lambda+o(1)) = o(1).               (15)
```

When `M->0`, Markov's inequality also gives `X=0` with high probability;
when `M->eta>0`, apply (14); when M diverges, use (11) and the necessary
X-obstruction. Equation (3) now proves, uniformly over this whole sparse
range,

```
P(U)=exp(-M)+o(1).                                  (16)
```

Uniformity can be made explicit by a subsequence argument: from any
sequence violating uniform convergence, extract a subsequence on which
M converges in `[0,infinity]` and apply the corresponding case just proved.

At (12), the expected number of overlapping X-pairs is `O(n^3 z^2)=o(1)`
by (8)--(10). Together with (15) and the exact bad-vertex description
after (3), this gives `B=2X` with high probability and proves the first
line of (2).

## 4. Dense defects: two births of the same complement obstruction

Leaf-cherry counting and its disappearance scale are classical; see
Krivelevich--Kwan--Loh--Sudakov, Section 4.2, as credited in
[LITERATURE.md](LITERATURE.md). We give the needed counts explicitly.
The directional step is the reduction (17) from all trace collisions
to these complement defects.

Suppose `0<=q<=2 log(n)/n`, and put `t=nq` and

```
N=(n t^2/2) exp(-2t)=D(n,p).
```

Uniformly in this range, (5)--(6) imply

```
E(Z+X)=o(1),
E Y=(1+o(1))N,
E T/E Y = p^(-1)(a/p^2)^(n-3)
        = 1+O(q+nq^2)=1+o(1)                       (17)
```

when q is positive; at q=0 both T and Y vanish. The first estimate follows
from `1-p^2<=4 log(n)/n`. The second follows from
`log(1-q)=-q+O(q^2)`, with `nq^2=o(1)`. In particular, when N is bounded,
`E(T-Y)=o(1)`: all non-cherry trace collisions disappear in probability.
This is an asymptotic reduction, not a deterministic equivalence.

### Exact second moment and the diverging-mean case

For `n>=6`, direct counting gives

```
E(Y)_2 = [(n)_6+(n)_5]/4 * q^4 p^(4n-14)
          + (n)_4 q^3 p^(3n-9).                    (18)
```

Two distinct compatible cherry indices have either disjoint vertex sets,
the same center and disjoint leaf pairs, or the same center and exactly
one common leaf. These are the three terms. All other overlaps are
impossible: a degree-one leaf cannot belong to two centers or serve as
a center requiring degree at least two.

For N tending to infinity, divide (18) by `(E Y)^2`. The disjoint term
is `1+O(1/n+q)`, the same-center four-leaf term is `O(1/n)`, and the
three-leaf term has order

```
exp(t)/(nt) = 1/[sqrt(n) sqrt(2N)] = o(1).
```

The comparisons are uniform since `nq^2=o(1)`. Hence
`Var(Y)/(E Y)^2 -> 0`, so Y is positive with high probability. A Y-index
is always an actual failure of U, by Section 2.

### Finite-mean Poisson law

Let `N->eta`, where `0<eta<infinity`. In a compatible tuple of k distinct
Y-indices, every leaf has exactly one center; no center is a leaf. The
union is therefore a disjoint union of stars with b centers and ell
leaves. Its probability is exactly

```
q^ell p^[ell n-ell(ell+3)/2].                        (19)
```

The exponent counts all forbidden complement edges incident to the
leaves, subtracting the ell required center-leaf edges and counting
leaf-leaf edges only once. There are `O_k(n^(b+ell))` tuples of a fixed
incidence pattern. Since

```
sqrt(n) t exp(-t) -> sqrt(2eta),
```

their total contribution is `O_k(n^(b-ell/2))`.
Every center has at least two leaves. Unless the tuple consists of k
vertex-disjoint cherries, at least one center has at least three leaves:
distinct indices with the same center cannot use the same leaf pair.
Thus `ell>=2b+1`, and the overlapping contribution tends to zero.

The disjoint tuples number `(n)_(3k)/2^k`. Their probability is (19) with
`ell=2k`, so their contribution tends to eta^k. Therefore

```
Y => Poisson(eta).                                  (20)
```

If `N->0`, (17) and Markov's inequality show there are no defects with
high probability. If `N->eta>0`, use (4), (17), and (20); if N diverges,
use the second-moment argument. The same subsequence argument as before
proves the uniform formula

```
P(U)=exp(-N)+o(1),    0<=q<=2 log(n)/n.              (21)
```

When N has a finite positive limit, the total expected number of pairs
of cherries sharing a center tends to zero, as is also visible in (18).
With probability tending to one, `Z=X=T-Y=0` and all Y-centers are
different. The exact bad-vertex description gives `B=Y`. The assertion
also holds with B tending to zero when N tends to zero. This proves the
last two lines of (2).

## 5. The middle range and very sparse graphs

Consider

```
sqrt(3 log(n)/n) <= p <= 1-2 log(n)/n.               (22)
```

We show uniformly that `E(Z+X+T)=o(1)`, so U holds with high probability.
For `p<=1/2`, (5) bounds `E(Z+X)` by a constant times
`n^2(1+np^2)exp(-np^2)=o(1)`; for `p>=1/2`, it is bounded by
`O(n^3(3/4)^(n-3))`.

For T split into three ranges. If `p<=1/4`, then
`2np^2q>= (3/2)np^2 >= (9/2)log n`, and (5) gives o(1).
If `1/4<=p<=3/4`, the exponent has order n uniformly. If `p>=3/4`,
write `t=nq>=2 log n`. For `t<=log^2 n`, the bound in (17) for T is
`(1+o(1))n t^2 exp(-2t)/2=o(1)`. For `t>=log^2 n`,
`2np^2q>=9t/8`, and `n^3 exp(-9 log^2(n)/8)=o(1)` suffices.

Both S and D tend to zero uniformly in (22): use `np^2>=3 log n`,
`nq>=2 log n`, and the eventual decrease of `u exp(-u)` and
`u^2 exp(-2u)`. Also D tends to zero uniformly in the sparse range of
Section 3, and S tends to zero uniformly in the dense range of Section 4.
Combining (16), (21), and (22) therefore proves (1).

Finally, when `p<log(n)/(2n)`, let I be the number of isolated vertices.
Then `E I=nq^(n-1)>=n^(1/2-o(1))`. For distinct vertices their joint
isolation probability is `q^(2n-3)`, so

```
Var(I)/(E I)^2 <= 1/(E I)+(q^(-1)-1) -> 0
```

uniformly. Thus G is disconnected with high probability. This proves
the remaining clause of Theorem 1 without any assumption about the
directional responses in a disconnected graph.

Substitution of the three scalings into S and D gives the constants in
the table and (2). All limiting assertions now follow from proved
finite defect formulas and the dependence estimates above.

## 6. Status and trust boundary

This is a written probabilistic proof with a finite exact corroborating
audit, pending independent mathematical review. No simulation, numerical
fit, graph catalogue, solver, or proof assistant is a dependency. The
audit checks the deterministic response reductions and exact first and
second moments on small labelled graphs; it does not prove the limiting
theorems by enumeration. Sources, attribution, and the limited novelty
claim are recorded in [LITERATURE.md](LITERATURE.md).
