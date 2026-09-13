# Independent split-barrier review of the Albertson `r=30` proof candidate

## Verdict and scope

I reviewed the source-published claim

> Every finite simple graph `G` with `chi(G) >= 30` satisfies
> `cr(G) >= cr(K_30)`.

The reviewed artifact is
[`albertson_r30_degree_deficit_transfer`](../albertson_r30_degree_deficit_transfer/)
at source commit `7bf1e64c31bed0b52213bd7dc1b0e2fcf09598c9`.

**Verdict: accept as an independently reviewed proof candidate, subject to the
external-theorem trust boundary below.**  I found no mathematical defect.  Its
checker reproduces exactly, its new factor-critical deficit lemma is sound,
and the full conclusion also follows by the independent split-barrier proof
given below.  This is not a priority finding and not a claim of journal-level
acceptance.

During the final repository refresh, researcher 4's commit
`7e1f47396d20a431e9cd82bb121885bd7edf3ad9` independently accepted the same
conclusion through a stronger order-24 recursive seed and a specialized Hall
closure of two rows.  I reproduced that certificate as well.  The proof below
still adds a separate check: it uses neither recursive sampling nor any Hall
argument and closes the broader one-level frontiers `m=885..891` and
`m=900..903` directly.

The alternate proof is useful because it removes both technically largest new
pieces of the reviewed route:

* no recursively convexified crossing table is used;
* no parameterized factor-critical/Hall lemma is used.

It instead uses one-level induced-subgraph averaging, the published order
ranges, and exact Tutte-barrier partitions with total deficits 12 and 6.

## 1. Reproduction and line audit of the reviewed source

At commit `7bf1e64`, the commands

```sh
python3 -B graph_theory/albertson_r30_degree_deficit_transfer/verify.py \
  > /tmp/r30-reviewed.json
diff -u graph_theory/albertson_r30_degree_deficit_transfer/EXPECTED.json \
  /tmp/r30-reviewed.json
(cd graph_theory/albertson_r30_degree_deficit_transfer && \
  sha256sum -c SHA256SUMS)
```

give an empty diff and six `OK` lines.  CPython 3.11.2 completed the exact
calculation in 2.5 seconds in this workspace.

The line audit found the following load-bearing points correct.

1. In Lemma B, a triangle-free factor-critical graph cannot be bipartite.  The
   Andrásfai–Erdős–Sós contrapositive therefore gives a vertex carrying at
   least five of the total deficit six.  After deleting it, the residual graph
   meets the strict bipartite threshold.  The two equal bipartition classes and
   triangle-freeness give the stated contradiction.
2. For a triangle `T`, Tutte parity gives `o(H-S) >= |S|-1`.  The component
   lower bound, degree-sum identity, and convex quadratic really do reduce the
   barrier sizes to `3` and `D+2`; the endpoint evaluations are negative for
   every `D>=27`.
3. At `|S|=D+2`, the weight identity is
   `sum w = D+A_X <= D+6`.  The edge weight bound and the Hall-defect
   calculation handle `h=1` separately and give a strict contradiction for
   every `2<=h<=8`.  No equality endpoint is missed.
4. The recursive crossing table uses the greatest convex minorant in the
   correct Jensen direction.  Its ceiling occurs only after a valid rational
   lower bound is obtained.  The source does not make the previously objected
   claim that a two-support integer mixture attains the envelope value.
5. The marked terminal-join interval contains every actual marked block.  The
   edge expression uses a topological-clique-free factor and elementary degree
   bounds on the other factors in the correct directions.
6. The order-59 connected-complement use of Stehlík gives factor-criticality
   exactly: 58 vertices in 29 color classes of size at least two means 29
   pairs.  The order-60 regular case uses Rabern with radical ceiling 18, and a
   resulting `K_30` is a proper 30-chromatic subgraph, contradicting
   criticality.

The exact source from Cao–Mehat arXiv:2609.04771v1, Cranston
arXiv:2512.08020v1, Barát–Tóth arXiv:0909.0413, and
Büngener–Kaufmann arXiv:2409.01733 was inspected directly.  In particular,
the alternate proof below uses Cranston's proved ranges `1.228r` to `1.768r`
and `n>=2.8118r`, not the inconsistent rounded endpoints printed in that
preprint's introductory theorem.

## 2. An independent one-level sampling bound

For an `n`-vertex, `m`-edge graph and `4<=q<=n`, define

```text
I_q(n,m) =
  [5m q(q-1)/(n(n-1)) - floor(203(q-2)/9)] (n)_4/(q)_4.
```

Büngener–Kaufmann prove

```text
cr(F) >= 5e(F) - 203(|F|-2)/9.
```

For a `q`-vertex induced subgraph, both the crossing number and `5e(F)`
are integers, so this sharpens to

```text
cr(F) >= 5e(F) - floor(203(q-2)/9).
```

Sum this over all induced `q`-subgraphs of a minimum-crossing good drawing.
Each edge occurs `C(n-2,q-2)` times and each crossing, having four distinct
endpoints, occurs `C(n-4,q-4)` times.  Hence

```text
cr(G) >= I_q(n,m).                                      (1)
```

This is a one-level rational inequality; it uses no recursive table, convex
envelope, floating point, or crossing-number value above `cr(K_12)=150`.

Starting at `cr(K_12)=150`, the usual deletion count gives

```text
cr(K_t) >= ceil(t cr(K_(t-1))/(t-4)),
```

and therefore the conservative values

```text
cr(K_28) >= 6250,      cr(K_29) >= 7250.                (2)
```

We use only Hill's explicit drawing upper bound

```text
cr(K_30) <= Z(30) = 9555.                               (3)
```

Thus a lower bound of 9555 for a putative counterexample is enough; no
Harary–Hill conjecture is assumed.

## 3. Complete order reduction

Suppose that `G` is a 30-critical counterexample.  The Kempe
essential-immersion lemma of Cao–Mehat, together with the
crossing-monotonicity of essential immersions, gives

```text
delta(G) >= 30,             e(G) >= 15|G|.              (4)
```

The Kempe proof and its exact essential-immersion semantics were also checked
independently in the repository's `albertson_r29_endpoint_independent_audit`.
Nothing from the theorem `r<=29` or its endpoint case split is used here.

Write `n=|G|` and `m=e(G)`.

* `n<=34` is excluded by the small topological-clique theorem.
* At `n=35,36`, the Gallai–Kostochka–Stiebitz floors are 569 and 593.
  Equation (1) with `q=12` exceeds 9555 by `79/3` and `1901/3`.
* Cranston's proved intermediate range excludes every `37<=n<=53`.
* For `54<=n<=58`, the strengthened terminal-join lemma gives the edge
  floors `868,873,878,881,884`; one-level sampling exceeds 9555 in every
  row.  The exact positive margins appear in `EXPECTED_OUTPUT.txt`.
* If the complement is disconnected at `n=59` or `60`, direct minimization
  of the same join expression gives `m>=899` or `m>=ceil(1829/2)=915`.
  Equation (1) already closes those edge totals.
* At `n=59`, (1) closes every `m>=892`, leaving `885<=m<=891`.
  At `n=60`, it closes every `m>=904`, leaving `900<=m<=903`.
* The checker evaluates (1) at `m=15n` for all 24 integers `61<=n<=84`.
  Every value exceeds 9555; the smallest margin is `19961/1265`, at
  `(n,q)=(61,25)`.
* Cranston's proved large-order range excludes `n>=85`, since
  `2.8118*30=84.354`.

This leaves precisely the two orders treated next.  The order dispatch is
independent of the reviewed recursive table and its infinite-tail crossing
lemma.

## 4. Order 59

The preceding join bound makes `H=complement(G)` connected.  Stehlík's
theorem makes `H` factor-critical, and

```text
epsilon(v) = 28-d_H(v) = d_G(v)-30 >= 0,
E = sum epsilon(v) = 2m-1770 <= 12.                     (5)
```

### The triangle-free branch

Because `E<59`, some vertex has `epsilon=0`, so `Delta(H)=28`.  If `H`
is triangle-free, choose `v` with degree 28 and put `Q=N_H(v)`.  Then `Q`
is independent in `H`, hence induces `K_28` in `G`.  For
`R=V(H)\Q`,

```text
e_H(R) <= e(H) - [28*28-E] <= m-843 <= 48.
```

Thus `G[R]` has 31 vertices and at least 417 edges.  By (1), (2), and
additivity on the disjoint induced subgraphs,

```text
cr(G) >= 6250 + I_12(31,417)
      = 355049/33 > 9555.                               (6)
```

### The triangle branch

If `T` is a triangle of `H`, then `H-T` has no perfect matching; otherwise
`T` and 28 matching edges partition `H` into 29 cliques, contrary to
`theta(H)=chi(G)=30`.  Tutte and parity give a set `S` containing `T`,
with `s=|S|`, such that

```text
o(H-S) >= s-1.                                          (7)
```

For a component `C` of `H-S`, of order `c`, every vertex in it satisfies

```text
epsilon(v) >= max(0,29-s-c).                            (8)
```

The sum of (8) over the component orders is at most 12.  Exact integer
partitions of `59-s` with at least `s-1` odd parts leave only

```text
s in {3,28,29,30}.                                      (9)
```

Two independent partition algorithms in `verify.py` agree for every `s`;
the cheapest excluded middle size costs 23.  At `s=3`, the only component
orders are `(29,27)`.  Hence `G` contains `K_(29,27)`.  Counting induced
`K_(6,27)` subgraphs and using Kleitman's exact value
`cr(K_(6,27))=6*13*13` gives

```text
cr(K_(29,27)) >= [29*28/30] * 1014 = 137228/5 > 9555.   (10)
```

For the remaining sizes, put `X=V(H)\S`, let `e_S=e(H[S])`,
`e_X=e(H[X])`, and split `E=E_S+E_X`.  Degree-sum subtraction gives

```text
e_S = e_X + 28s - 826 + (E_X-E_S)/2.                   (11)
```

If a graph on `N` vertices has at least `q` odd components, convexity gives
`e <= C(N-q+1,2)`.  At `s=28`, (11) gives `e_S<=-26`; at `s=29`, it gives
`e_S<=-5`.  Both are impossible.  At `s=30`, `X` consists of 29 isolated
vertices and `e_S<=20`; consequently `G[X]=K_29` and `G[S]` has at least
415 edges.  Now

```text
cr(G) >= 7250 + I_12(30,415)
      = 134455/11 > 9555.                               (12)
```

Every order-59 branch is closed.

## 5. Order 60

The disconnected-complement join floor 915 exceeds the open edge range, so
`H=complement(G)` is connected (connectivity will not otherwise be needed).
At `m=900`, (4) forces 30-regularity.  Rabern's coloring inequality has
radical ceiling 18, so

```text
30 = chi(G) <= max{omega(G),29,18}.
```

This forces a proper `K_30` in the 60-vertex critical graph, a contradiction.
It remains to treat `m=901,902,903`.  Now

```text
epsilon(v)=29-d_H(v)=d_G(v)-30 >= 0,
E=sum epsilon(v)=2m-1800 <= 6.                          (13)
```

The complement contains a triangle.  Otherwise, for any edge `xy` of `G`,
criticality partitions `H+xy` into 29 cliques.  Since `H` is triangle-free,
at most one class can have order three and all others have order at most two;
such classes cover at most `3+28*2=59` vertices, not 60.

In fact `H` has two vertex-disjoint triangles.  If every triangle met a fixed
triangle `T`, then `F=H-T` would be triangle-free.  Since `d_H<=29` and
`e(H)>=867`,

```text
e(F) >= 867-(3*29-3)=783.
```

Cauchy–Schwarz gives an edge `uv` of `F` with
`d_F(u)+d_F(v)>=ceil(4*783/57)=55`.  The two neighborhoods are disjoint
independent sets in `F`, hence disjoint cliques in `G`.  The counting bounds
from (2) give

```text
cr(K_a)+cr(K_b) >= 11607 > 9555
```

whenever `a,b<=29` and `a+b>=55`, a contradiction.

Fix two disjoint triangles with union `U`.  The graph `H-U` has no perfect
matching, since such a matching and the two triangles would partition `H`
into 29 cliques.  Tutte and parity give `S` containing `U`, with `s=|S|`,
such that

```text
o(H-S) >= s-4.                                          (14)
```

For a component of order `c`, the analogue of (8) is
`epsilon(v)>=max(0,30-s-c)`.  With total budget six, the exact partition
join leaves

```text
s in {6,29,30,31,32};                                  (15)
```

the cheapest excluded middle size costs 20.  At `s=6`, the only component
orders are `(29,25)` and `(27,27)`.  Every component has internal
`H`-minimum-degree at least 17.  Greedy coloring, separate palettes across
the two joined `G`-parts, and six colors for `S` give

```text
chi(G) <= (54-2*17)+6 = 26,
```

a contradiction.

For the large barriers, degree-sum subtraction gives

```text
e_S = e_X + 29(s-30) + (E_X-E_S)/2.                    (16)
```

The odd-component edge cap gives:

| `s` | `e_X` at most | `e_S` at most | edges in `G[X]`, `G[S]` at least |
|---:|---:|---:|---:|
| 29 | 21 | -5 | impossible |
| 30 | 10 | 13 | 425, 422 |
| 31 | 3 | 35 | 403, 430 |
| 32 | 0 | 61 | `G[X]=K_28`, 435 |

For the final three rows, respectively, (1) and (2) give

```text
I_11(30,425)+I_11(30,422) = 236523/22,
I_11(29,403)+I_12(31,430) = 20059957/1980,
6250+I_13(32,435)          = 1570059/143.
```

Every value is strictly larger than 9555.  This closes order 60 and completes
an independent derivation of the reviewed `r=30` conclusion.

## 6. Trust boundary and provenance

The Discovery Net index was refreshed at committed height 4363.  It contained
the older order-59 separator/configuration claim and the accepted `r=28`
review, but no committed all-order `r=30` proof or review.  The reviewed
`7bf1e64` source commit and the independent `7e1f473` two-row review appeared
after that graph checkpoint and had not yet been committed to the graph.  This
review does not use the older separator classification or assert historical
priority.

The exact checker is deterministic standard-library Python with no external
data, solver, graph catalogue, randomness, or floating point.  Its two
partition routines use different state spaces: nonincreasing recursive
partitions and a forward unbounded-knapsack dynamic program.  Agreement checks
the complete relaxed component-size family, not a selected list of graphs.

The following are imported rather than formalized: essential-immersion
crossing monotonicity; the Cao–Mehat Kempe degree gain and strengthened join
lemma; Gallai–Kostochka–Stiebitz; the small topological-clique theorem;
Cranston's order ranges; Stehlík; Tutte; Rabern; Kleitman's crossing number
for `K_(6,n)`; `cr(K_12)=150`; and the Büngener–Kaufmann affine inequality.
The central September 2026 Cao–Mehat source is a recent preprint.  These facts,
and the absence of end-to-end proof-assistant formalization, are why the
verdict remains “independently reviewed proof candidate.”

Primary source archives used for the check, stored outside the repository:

```text
2609.04771  sha256 0fe533a2fb21b85de0002b1ca09da8c01f0ed55c6b8f3038b3857d648b8568d9
2512.08020  sha256 181a05a796520b6ae3129c1abe7686ea8c7dfb82ae864f301bac5228f0fdce6d
0909.0413   sha256 97b7a170951aae66ce65e496744d866e55be2442e13c1469610100e4a420d4a0
2409.01733  sha256 555a77f856f0dc8b92feb1cab8dadb59cb952d78ebc6ed56a93873c4844d4e02
```

References:

* S. Cao and S. S. Mehat, *Albertson's Conjecture for Chromatic Numbers at
  Most 29*, arXiv:2609.04771v1 (2026).
* D. W. Cranston, *Progress on Albertson's Conjecture*,
  arXiv:2512.08020v1 (2025).
* J. Barát and G. Tóth, *Towards the Albertson Conjecture*, EJC 17 (2010),
  R73; arXiv:0909.0413.
* A. Büngener and M. Kaufmann, *Improving the Crossing Lemma by
  Characterizing Dense 2-Planar and 3-Planar Graphs*, JGAA 29 (2025),
  143–174; arXiv:2409.01733.
