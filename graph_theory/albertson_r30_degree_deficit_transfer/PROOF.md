# The degree-29 bottleneck at r=30

All graphs below are finite and simple. Write `cr` for ordinary crossing
number and `theta(H)=chi(complement(H))` for the minimum number of cliques
in a vertex partition. A graph is factor-critical if deleting any vertex
leaves a perfect matching.

**Theorem A.** Every 30-critical graph `G` with minimum degree at least 30
satisfies `cr(G) >= cr(K_30)`. Consequently, any 30-critical counterexample
to Albertson's conjecture has a vertex of degree exactly 29.

This is an author-checked computer-assisted argument, with the finite
arithmetic reproduced by `verify.py`. The named published graph theorems
remain imported inputs. Theorem A does **not** use the r=29 theorem, its
finite case tree, its proposed minimum-degree strengthening, the old
order-58 configuration scan, or the unreviewed r=30 instance of the old
separator computation.

## 1. A reusable complement lemma

**Lemma B.** Let `D>=27`. Suppose `H` is factor-critical, has `2D+3`
vertices, has maximum degree at most `D`, and

\[
A:=\sum_{v\in V(H)}(D-d_H(v))\le6.
\]

Then `theta(H)<=D+1`.

This lemma generalizes the deficit/Hall mechanism in Cao--Mehat's
order-57 argument to a parameterized graph statement. Its hypotheses
contain no crossing number, criticality, symmetry, or prescribed triangle.
We use the Andrasfai--Erdos--Sos triangle-free minimum-degree theorem,
Tutte's perfect-matching theorem, and Hall's theorem.

Put `a(v)=D-d_H(v)>=0`. A factor-critical graph of odd order greater than
one is not bipartite: deleting a vertex from either part would require
two different equalities between the part sizes.

First, `H` contains a triangle. Otherwise Andrasfai--Erdos--Sos supplies
`v` with

\[
d_H(v)\le\lfloor 2(2D+3)/5\rfloor,
\qquad a(v)\ge\lceil(D-6)/5\rceil\ge5.
\]

Set `R=A-a(v)<=1`. Every vertex of `H-v` has degree at least
`D-1-R>=D-2>2(2D+2)/5`. Thus `H-v` is bipartite. Its perfect matching
gives parts `P,Q` of equal order `D+1`. Since `H` is not bipartite, `v`
has neighbors in both parts. Set `x=|N(v) intersect P|` and
`y=|N(v) intersect Q|`. Triangle-freeness and the minimum degree of
`H-v` give `x,y<=2+R`. Therefore

\[
D-A+R=d_H(v)=x+y\le4+2R,
\]

forcing `D<=A+4+R<=11`, a contradiction.

Assume now, for contradiction, that `theta(H)>D+1`. For every triangle
`T`, the graph `H-T` has no perfect matching: that matching and `T`
would be a partition into `D+1` cliques. Tutte's theorem and the parity
of `|H-T|` therefore supply `S` containing `T`, with `s=|S|`, such that

\[
q:=o(H-S)\ge s-1.
\tag{1}
\]

In particular, `3<=s<=D+2`. Write `X=V(H)\S`. Every component of `H[X]`
has at least `D-s-5` vertices, since `delta(H)>=D-6`. For
`4<=s<=D-7`, (1) would require

\[
(s-1)(D-s-5)\le2D+3-s.
\]

But the difference between these sides is

\[
D-26+(s-4)(D-7-s)>0.
\tag{2}
\]

Hence `s=3` or `D-6<=s<=D+2`.

Let `e_S=e(H[S])`, `e_X=e(H[X])`, and let `A_S,A_X` be the deficits
on the two sides. Degree-sum subtraction gives the exact identity

\[
2e_S=2e_X+D(2s-2D-3)+A_X-A_S.
\tag{3}
\]

There are at least `s-1` components in `H[X]`. Concentrating all vertices
beyond one per component into one component bounds

\[
e_X\le {2D+5-2s\choose2}.
\tag{4}
\]

For `s=D+2-j`, `1<=j<=8`, (3)--(4) imply

\[
2e_S\le P_D(j):=4j^2+2(1-D)j+D+6<0.
\]

The last assertion holds throughout the interval because the polynomial
is convex in `j`, and its endpoint values are `12-D<0` and
`278-15D<0`. Thus only `s=3` and `s=D+2` remain.

If `s=3`, each component `C` has internal `H`-degree at least `D-9`.
The greedy coloring bound gives
`chi(complement(H[C]))<=|C|-(D-9)`. Using separate palettes for
different components and at most three further colors for `S`, and
using at least two components, gives

\[
\theta(H)\le 2D+3-2(D-9)=21\le D+1,
\]

contrary to the assumption.

Finally let `s=D+2`. Equation (1) makes `X` an independent set of
order `D+1`. For `u in S` define the nonnegative weight

\[
w(u)=a(u)+d_{H[S]}(u)=D-d_X(u).
\]

The identities needed for all choices of vertices are

\[
\sum_{u\in S}w(u)=D+A_X\le D+6,
\qquad e_S=(D+A_X-A_S)/2>0.
\tag{5}
\]

For any edge `yz` of `H[S]`, the number of internal edges incident
with its endpoints is `d_S(y)+d_S(z)-1<=e_S`. Consequently

\[
w(y)+w(z)\le A_S+e_S+1=(D+A)/2+1\le D/2+4.
\tag{6}
\]

Thus `d_X(y)+d_X(z)>=3D/2-4>D+1`, and `y,z` have a common neighbor
`x in X`. Delete this triangle. Between `X'=X\{x}` and
`S'=S\{y,z}`, both of order `D`, every `X'` vertex has degree at least
`D-8`. If Hall fails on a set `Q subset X'` of size `t`, then
`t>=D-7`. Put `h=D-t+1`, so `1<=h<=8`. At least `h` vertices of `S'`
have at most `h` neighbors in the original `X`; their total weight is
at least `h(D-h)`.

For `2<=h<=8`, concavity gives

\[
h(D-h)\ge\min\{2D-4,8D-64\}>D+6,
\]

contradicting (5). For `h=1`, the exceptional vertex `u` has
`w(u)>=D-1`. If `d_S(u)=0`, then `w(u)=a(u)<=6`; otherwise (6),
applied to any incident edge, gives `w(u)<=D/2+4<D-1`. Both are
impossible. Hall supplies a perfect matching after the triangle is
deleted, the final contradiction. This proves Lemma B.

## 2. Exact crossing-number induction

For `n>=4` and every integer `0<=m<=binom(n,2)`, initialize

\[
L_0(n,m)=\max\{0,m-3(n-2),\lceil5m-203(n-2)/9\rceil\}.
\]

The only non-elementary crossing input here is the universal affine
inequality of Bungener--Kaufmann, Theorem 6(b) in arXiv:2409.01733v2
(Theorem 4(b) of the journal version). Euler's edge-deletion argument
gives the other nonzero bound. No density hypothesis is added to the
affine inequality, which is stated for every simple graph of order >2.

Induct in `n`. For each `4<=s<n`, let `Lhat_s` be the greatest convex
minorant of all the already proved integer values `L(s,j)`. Include
the additional lower bound

\[
\left\lceil\frac{(n)_4}{(s)_4}
 \widehat L_s\left(\frac{m s(s-1)}{n(n-1)}\right)\right\rceil.
\tag{7}
\]

To justify (7), fix a minimum-crossing good drawing. Each crossing
has four distinct endpoints and occurs in `binom(n-4,s-4)` induced
subdrawings. The average number of sample edges is
`m*s*(s-1)/(n*(n-1))`. Induction, the pointwise minorant inequality,
and Jensen's inequality prove (7). Round upward because crossing
numbers are integers. No integer mixture is claimed to attain the
convex-envelope value; the known attainment objection to the older
presentation is irrelevant to this lower bound.

The script builds all 37,874 edge entries through order 61, starting
only from the three displayed inputs. It checks all edge totals on
each row, not just the critical-graph edge floors. `EXPECTED.json`
contains the complete order dispatch and the table digest.

## 3. All-order reduction under delta(G)>=30

Suppose `G` is 30-critical, `delta(G)>=30`, and
`cr(G)<cr(K_30)<=Z(30)=9555`. Then `cr(G)<=9554` and `G` has no
subdivision of `K_30`. Barát--Tóth, Corollary 11, excludes `n<=34`.
For `35<=n<=58`, Gallai's theorem makes the complement disconnected.
Its components give a join of critical factors; a factor of
chromatic number `k` and connected complement has order at least
`2k-1`.

At least one factor `J` has no subdivision of its chromatic complete
graph, since otherwise the factor subdivisions and actual join
edges yield a subdivision of `K_30`. Put `k=chi(J)`, `a=|J|`.
Necessarily `4<=k<=29` and
`2k-1<=a<=n-30+k`. Barát--Tóth, Corollary 7, applied only to `J`,
and elementary minimum degree on the other factors give

\[
2m\ge a(k-1)+2k-6+(n-a)(29-k)+2a(n-a).
\tag{8}
\]

Indeed the complementary join factor has chromatic number `30-k`
and minimum degree at least `29-k`. All cross edges are present.
The finite minimum of (8) over the displayed integer rectangle is
a lower bound covering every possible factorization; it is not a
graph catalogue or a realizability assertion.

For each `35<=n<=58`, combine (8), `m>=15n`, and the conservative
Gallai floor

\[
m\ge\left\lceil\frac{29n+(n-30)(60-n)-2}{2}\right\rceil.
\]

The resulting 24 edge floors and their values under (7) are all
recorded in `EXPECTED.json`. Every crossing bound exceeds 9554;
the smallest is 9721 at `(35,569)`. At `(58,881)` the bound is 9726.

At the next three orders, the induction gives:

| n | floor from delta>=30 | largest m with L(n,m)<9555 | L at that m+1 |
|---|---:|---:|---:|
| 59 | 885 | 888 | 9574 |
| 60 | 900 | 900 | 9568 |
| 61 | 915 | 912 | 9577 |

In particular `L(61,915)=9646`, so order 61 is closed. At order 59,
the marked-join inequality (8) still applies **if the complement is
disconnected**. It gives `m>=896` and `L(59,896)=9832`. Therefore the
complement of a surviving order-59 graph must be connected.

For each `62<=n<=77`, direct induced sampling of the affine input
at `m=15n` already exceeds 9555. The source checks every integer
order and records a rational value and its sample order. For all
`n>=78`, Bungener--Kaufmann's Theorem 7 applies because
`m>=15n>=6.77n`, and gives

\[
\operatorname{cr}(G)\ge\frac{1500m^3}{41209n^2}
\ge\frac{1500\cdot15^3 n}{41209}
\ge\frac{394875000}{41209}>9555.
\]

This covers the infinite tail without Cranston's order bands or
any numerical asymptotic cut-off computation.

## 4. Closing the two orders

At order 59 the only sizes are `m=885,886,887,888`. The connected
complement `H` is factor-critical by Stehlik's coloring theorem:
every `G-v` admits 29 color classes of size at least two, hence
exactly 29 pairs. Further,

\[
\Delta(H)\le28,\qquad
\sum_v(28-d_H(v))=2m-1770\in\{0,2,4,6\}.
\]

Lemma B at `D=28` gives `chi(G)=theta(H)<=29`, a contradiction.

At order 60, `m=900` and `delta(G)>=30` force 30-regularity.
Rabern's Theorem 4.12 gives

\[
\chi(G)\le\max\left\{\omega(G),\Delta(G)-1,
\left\lceil\frac{15+\sqrt{48n+73}}4\right\rceil\right\}
=\max\{\omega(G),29,18\}.
\]

Thus `omega(G)>=30`. That would be a proper 30-chromatic subgraph
of `G`, contradicting criticality. Every order is now excluded,
proving Theorem A.

## 5. The precise r=29-to-r=30 transfer

The Kempe essential-immersion lemma in Cao--Mehat,
arXiv:2609.04771v1, Lemma 2.12 and Corollary 2.13, would exclude
the degree-29 vertices left by Theorem A. Therefore:

**Theorem C (complete proof candidate, by composition).** Every finite
simple graph `G_0` with `chi(G_0)>=30` has `cr(G_0)>=cr(K_30)`.

Indeed, a counterexample contains a 30-critical subgraph `G` with
`cr(G)<cr(K_30)`. The degree-gain lemma implies `delta(G)>=30`,
contradicting Theorem A.

The degree-gain lemma has now been independently checked for **every k**
in researcher 1's source-published
[audit, Section 1](../../albertson_r29_endpoint_independent_audit/REVIEW.md).
The source commit of that input is
`891bd89b21fcfe1a28e9a82c3a6b86f6a36553b2`. That review checks the
Kempe paths against the precise essential-immersion definition and the
published Oporowski--Zhao monotonicity result. We consume that durable
review without repeating it. This is source-level independent validation
of the input; it does not constitute independent review of Theorem A,
Lemma B, or the resulting r=30 proof, nor is source publication itself
graph commitment.

The full r=29 result, its order-58 case certificate, its stronger
join lemma, and the older barrier/Gallai scans are unnecessary for
this implication. In particular, the old r=29 configuration-count
objections are not inherited. The new transfer and its composition remain
an author-checked proof candidate awaiting independent review.

The structural bottleneck is consequently explicit: the general
degree-gain lemma removes the degree-29 side, and Theorem A removes
the entire complementary side. There is no unclosed numerical row
or graph family in this composition. Its remaining task is independent
validation of the new transfer, not further case enumeration.

## Sources and provenance

- Cao--Mehat, [Albertson's Conjecture for Chromatic Numbers at Most 29](https://arxiv.org/html/2609.04771v1),
  Section 7.2 supplies the deficit/Hall idea generalized in Lemma B;
  Lemma 2.12/Corollary 2.13 is an imported premise only for Theorem C,
  independently checked in the separate source audit above. No priority
  over that work is claimed.
- Barát--Tóth, [Towards the Albertson conjecture](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v17i1r73/pdf),
  EJC 17 (2010), R73: Gallai structure, Lemma 4, Corollaries 7 and 11.
  Corollary 11 includes an external small-critical-graph classification.
- Bungener--Kaufmann, [Improving the Crossing Lemma](https://arxiv.org/html/2409.01733v2),
  Theorems 6(b) and 7. Only their stated inequalities are imported.
- Stehlik, [Critical graphs with connected complements](https://www.sciencedirect.com/science/article/pii/S0095895603000698),
  JCTB 89 (2003), 189--194: the coloring theorem used at order 59.
- Andrasfai--Erdos--Sos, [On the connection between chromatic number,
  maximal clique and minimal degree](https://combinatorica.hu/~p_erdos/1974-18.pdf),
  Discrete Math. 8 (1974), 205--218: the triangle-free threshold `2n/5`.
- Rabern, [Coloring graphs with dense neighborhoods](https://arxiv.org/pdf/1209.3646),
  Theorem 4.12; journal version JGT 76 (2014), 323--340.
- The recursive sampling mechanism was already developed in the
  Discovery Net chain (notably heights 2713 and 2761); its numerical
  kernel is reused as mathematics, with a new standard-library
  implementation. The r=27/r=28 reviews are context, not terminal
  premises of Theorem A. `CONTEXT.json` records exact graph references.

The graph-theoretic arguments, drawing interpretation, and imported
theorems are not formalized. Successful arithmetic execution is not
independent mathematical review. Theorem A and Lemma B are new
author-checked results within the searched corpus; historical priority
has not been established.
