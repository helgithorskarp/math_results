# Independent two-row certificate and closure for Albertson `r=30`

This note independently supports the `r=30` conclusion of the proof candidate
at commit `7bf1e64c31bed0b52213bd7dc1b0e2fcf09598c9`.  It uses a different,
stronger crossing-number seed to reduce the problem to two rows, then closes
those rows with a specialized Tutte--Hall argument.

> **Theorem (relative to the imported results below).** If the `r=30`
> assertion fails—that is, some graph has chromatic number at least 30 and
> crossing number below `cr(K_30)`—then it contains a 30-critical
> counterexample `G` satisfying
>
> ```text
> |V(G)| = 59,   |E(G)| in {886,887}.
> ```
>
> Its complement `H` is connected, factor-critical, and anti-tight in the
> sense defined below.  Moreover `Delta(H)<=28`, its total degree deficit
> `sum_v(28-d_H(v))` is respectively 2 or 4, `H` contains a triangle, and
> `H-T` has no perfect matching for every triangle `T` of `H`.

The result transfers the reviewed universal local fact
`cr(24,132)>=165` into the `r=30` problem by exact recursive convex sampling.
It does not use the disputed `r=29` catalogue or barrier enumeration.

> **Corollary.** Subject to the named published inputs and the independently
> reviewed order-24 endpoint, every graph of chromatic number at least 30 has
> crossing number at least `cr(K_30)`.

The verdict is **accept the r=30 conclusion by an independent route**.  This
artifact does not independently validate the proof candidate's stronger
parameterized lemma for every `D>=27` and deficit at most 6; it proves only
the `D=28`, deficits 2 and 4 specialization actually reached here.

## 1. Order and edge dispatch

Write `n=|V(G)|`, `m=|E(G)|`, and

```text
Z(30) = floor(30/2) floor(29/2) floor(28/2) floor(27/2) / 4
      = 9555.
```

The standard drawing gives `cr(K_30)<=9555`, so a crossing lower bound of
9555 is enough.  Cao and Mehat's branch-clean essential-immersion lemma says
that a critical counterexample at chromatic number `r` has minimum degree at
least `r`; hence here `m>=15n`.

The Barát--Tóth small-order theorem excludes `n<=34`.  Cranston's proved
intervals

```text
1.228r <= n <= 1.768r,       n >= 2.8118r
```

exclude `37<=n<=53` and `n>=85`.  The only orders requiring arithmetic are

```text
35, 36, and 54,...,84.
```

At each such order the certificate takes the maximum of `15n`, the
Gallai--Kostochka--Stiebitz floor when applicable, and Cao--Mehat's
strengthened Gallai-join floor when applicable.  The exact recursive
crossing table through order 60, and one-stage integer-aware sampling above
60, then give:

| order(s) `n` | edge floor at the exceptional order | certified crossing floor | conclusion |
|---:|---:|---:|---|
| 35 | 569 | 10092 | closed |
| 36 | 593 | 10601 | closed |
| 54 | 868 | 11220 | closed |
| 55 | 873 | 10873 | closed |
| 56 | 878 | 10575 | closed |
| 57 | 881 | 10195 | closed |
| 58 | 884 | 9841 | closed |
| 59 | 885 | 9454 | `m=885,886,887` survive crossing bounds |
| 60 | 900 | 9575 | closed |
| 61 | 915 | 9571 | closed |
| 62,...,84 | per-order `15n` floor | at least 9689 | closed |

Every per-order floor, sampling parameter, exact rational value, and closure
threshold is in [`certificate.json`](certificate.json).  In particular, the
strong table at order 59 is

| `m` | recursive lower bound `F_59(m)` |
|---:|---:|
| 885 | 9454 |
| 886 | 9490 |
| 887 | 9525 |
| 888 | 9561 |

Thus recursive sampling closes at 888 and leaves exactly three rows before a
coloring argument.

If `m=885`, then `2m=59*30`; since `delta(G)>=30`, the graph is 30-regular.
Rabern's inequality has its order term equal to 18 because

```text
53^2 < 48*59+73=2905 < 54^2.
```

It therefore gives

```text
30=chi(G) <= max{omega(G),29,18},
```

so `G` contains a `K_30`.  This is a proper 30-chromatic subgraph of the
59-vertex critical graph, a contradiction.  Only `(59,886)` and `(59,887)`
remain.

## 2. The recursive crossing certificate

For each order `s` and edge count `q`, start with the integer-rounded maximum
of the four universal inequalities

```text
0,
q-3(s-2),
7q/3-25(s-2)/3,
37q/9-155(s-2)/9,
5q-203(s-2)/9.
```

The reviewed `r=27` chain proves `cr(24,132)>=165`.  The `37/9` inequality
below 132 edges and Ackerman's simple 4-planar deletion theorem above it then
give the universal order-24 seed

```text
cr(J) >= max(0,5|E(J)|-495).                         (1)
```

Let `F_s(q)` be an already certified integer table and let `bar(F_s)` be its
greatest convex piecewise-linear minorant.  Summing over all induced
`s`-vertex subdrawings and applying Jensen's inequality gives, for every
`n`-vertex, `m`-edge simple graph,

```text
cr(G) >= ceil(
  C(n,s)/C(n-4,s-4)
  * bar(F_s)(m*s*(s-1)/(n*(n-1)))
).                                                    (2)
```

Every crossing is counted `C(n-4,s-4)` times.  The average induced edge
count is `m*s*(s-1)/(n*(n-1))`, and convexity makes replacing the actual
edge-count distribution by this average a valid relaxation in the lower
direction.  Closing the base bounds and (1) under (2), for every `4<=s<n`,
defines the table used here.

The producer hashes every entry `n:m:F_n(m)` through order 60:

```text
8d15e75fbb647b6cd6899bd4466ec0ce7a0185e23a918a878bdfd3aebfb6b115
```

As a frozen control, the prefix through order 53 is

```text
79e615e691c84d697b2dbc3d6fded0d9657c37d3f91f4bebc1a61097fb39f7f6,
```

exactly the digest previously obtained by two independent implementations
in the reviewed `r=27` propagation.  It also reproduces `F_53(713)=6089`.

`generate_certificate.py` constructs every lower hull both by an
orientation-based monotone chain and by pooled adjacent slopes.
`verify_certificate.py` imports none of that code: it rebuilds all tables by
recursive exact QuickHull splits, uses falling-factorial incidence ratios,
audits every hull pointwise, and checks every field of the compact JSON
certificate.  Assertions use integers and `Fraction`, never floating point.

## 3. Complement receiver at the two rows

At order `2r-1=59`, Cao--Mehat's join lemma gives `m>=r^2-1=899` if the
complement is disconnected.  Hence the two survivors, with at most 887
edges, have connected complement `H`.

Stehlík's theorem supplies, for every vertex `v`, a 29-coloring of `G-v` in
which every class has at least two vertices.  There are exactly 58 vertices,
so all 29 classes are pairs.  Equivalently, `H-v` has a perfect matching for
every `v`; thus `H` is factor-critical.

Call this situation **anti-tight** when no perfect matching `M` of `H-v`
contains an edge `xy` with both endpoints in `N_H(v)`.  Anti-tightness is
forced here: otherwise `vxy`, together with the other 28 edges of `M`, is a
partition of `H` into 29 cliques and hence a 29-coloring of `G`.

Since `delta(G)>=30`, `Delta(H)<=28`.  The two exact degree possibilities are
compactly described by deficit partitions:

| `m(G)` | `m(H)` | `sum(28-d_H)` | possible nonzero deficit partitions |
|---:|---:|---:|---|
| 886 | 825 | 2 | `2`; `1+1` |
| 887 | 824 | 4 | `4`; `3+1`; `2+2`; `2+1+1`; `1+1+1+1` |

For example, deficit partition `3+1` means degrees
`(28^57,27,25)`.  In all cases `delta(H)>=24>2*59/5`.  If `H` were
triangle-free, the Andrásfai--Erdős--Sós theorem would make it bipartite,
which is incompatible with factor-criticality on 59 vertices.  So `H`
contains a triangle.  Finally, if a triangle `T={x,y,z}` had a perfect
matching in `H-T`, adjoining edge `yz` would violate anti-tightness for `x`.
Therefore `H-T` has no perfect matching for every triangle `T`.  This is the
finite structural receiver left for a subsequent barrier or obstruction
argument in the numerical certificate.

## 4. Specialized deficit closure

We now close that receiver without a graph catalogue.  The following lemma is
a deliberately narrower version of the concurrent proof candidate's general
deficit lemma.

> **Specialized lemma.** Let `H` be a factor-critical graph on 59 vertices
> with maximum degree at most 28 and total deficit
> `A=sum_v(28-d_H(v))` in `{2,4}`.  Then `H` has a clique partition with at
> most 29 parts.

We already know that `H` contains a triangle.  Suppose for contradiction that
its clique-partition number exceeds 29.  For a triangle `T`, a perfect
matching of `H-T` would combine with `T` to give 29 cliques.  Tutte's theorem
therefore supplies a set `S` containing `T`, with `s=|S|`, such that

```text
odd(H-S) >= s-1,                  3 <= s <= 30.       (3)
```

Every component outside `S` has order at least `29-A-s`; every odd component
has order at least the least positive odd integer no smaller than that.  This
size condition, followed by the exact degree-sum identity

```text
2e(H[S]) = 2e(H-S) + 28(2s-59) + A_X-A_S,            (4)
```

leaves only `s=3` and `s=30`.  The finite checker exhausts every integer
`3<=s<=30` separately for `A=2,4`.  In (4) it uses the valid extremal cap

```text
e(H-S) <= C(61-2s,2),
```

obtained by concentrating all vertices beyond the required `s-1` components
in one component.  It also relaxes `A_X-A_S` upward to `A`, so no realizable
case is lost.

For `s=3`, each outside component has internal `H`-degree at least
`25-A`.  Coloring its complement greedily and using separate palettes for
the at least two components gives

```text
theta(H) <= 59-2(25-A),
```

which is 13 or 17, a contradiction.

It remains that `s=30`.  Then (3) forces the outside set `X` to be an
independent set of order 29.  For `u in S`, put

```text
w(u)=28-d_X(u)=a(u)+d_{H[S]}(u),
```

where `a(u)=28-d_H(u)`.  Degree sums give

```text
sum_{u in S} w(u) = 28+A_X <= 28+A.                  (5)
```

There is an edge `yz` in `H[S]`, since (4) and `A<=4` make its edge count
positive.  The internal edges incident with `y,z` are at most all internal
edges, so

```text
w(y)+w(z) <= (28+A)/2+1 <= 17.                       (6)
```

Thus `d_X(y)+d_X(z)>=39>29`; choose a common neighbor `x`.  Delete triangle
`xyz`.  Between `X'=X-{x}` and `S'=S-{y,z}` are two sets of order 28, and
every `X'` vertex has at least `28-A-2` neighbors in `S'`.

If Hall fails on `Q subset X'`, put `t=|Q|` and `h=29-t`.  Then
`1<=h<=A+2`, and at least `h` vertices of `S'` have at most `h` neighbors in
the original `X`.  Their weights cost at least `h(28-h)`.  For every
`2<=h<=A+2`, the exact costs recorded in the certificate exceed the total
budget `28+A` in (5).  If `h=1`, the exceptional vertex has weight at least
27.  With no internal neighbor its weight is a deficit at most `A`; with an
internal neighbor (6) bounds it by at most 17.  Both alternatives are
impossible.  Hall supplies a perfect matching between `X'` and `S'`.

That matching, together with triangle `xyz`, partitions `H` into 29 cliques,
the final contradiction.  The specialized lemma closes both certified rows,
and the critical-subgraph reduction proves the corollary.

### Relation to the concurrent proof candidate

The candidate in
[`albertson_r30_degree_deficit_transfer`](../albertson_r30_degree_deficit_transfer/PROOF.md)
uses only the older crossing bases, reaches deficits `0,2,4,6`, and proves a
general lemma for all `D>=27`.  This review instead imports the already
reviewed order-24 endpoint, reaches only deficits 2 and 4, independently
rebuilds the recursive tables with two implementations, and proves the
shorter specialization above.  Agreement on the r=30 conclusion is therefore
not agreement between two executions of the candidate's code or its exact
case split.

## Reproduction

CPython 3.11 or later is sufficient; there are no third-party dependencies.
From this directory run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 generate_certificate.py \
  --output certificate.replayed.json
diff -u certificate.json certificate.replayed.json
PYTHONDONTWRITEBYTECODE=1 python3 verify_certificate.py certificate.json
sha256sum -c SHA256SUMS
```

The exact expected terminal lines are in [`EXPECTED_OUTPUT.txt`](EXPECTED_OUTPUT.txt).
On the reference machine the two table constructions together take under one
minute.

## Imported results and trust boundary

- S. Cao and S. S. Mehat,
  [*Albertson's Conjecture for Chromatic Numbers at Most
  29*](https://arxiv.org/abs/2609.04771), for the branch-clean immersion,
  minimum-degree gain, strengthened join estimate, exact order reduction
  ingredients, Stehlík and Rabern statements.  The downloaded manuscript
  source used here has SHA-256
  `d9e9542222395ee911c912d6c7aa2dae54046c6817d18e41713bf06410e9e2d7`.
  The general degree-gain and terminal-join bridge is also rederived in
  [researcher 1's independent source
  audit](../../albertson_r29_endpoint_independent_audit/REVIEW.md), Section 1,
  at commit `891bd89b21fcfe1a28e9a82c3a6b86f6a36553b2`.
- D. W. Cranston,
  [*Progress on Albertson's Conjecture*](https://arxiv.org/abs/2512.08020v1),
  for the proved order intervals (using `1.228`, `1.768`, and `2.8118`).
- A. Büngener and M. Kaufmann,
  [*Improving the Crossing Lemma by Characterizing Dense 2-Planar and
  3-Planar Graphs*](https://arxiv.org/abs/2409.01733v2), and J. Pach et al.,
  [*Improving the Crossing Lemma by Finding More Crossings in Sparse
  Graphs*](https://doi.org/10.1007/s00454-006-1264-9), for the universal
  crossing inequalities.
- E. Ackerman,
  [*On topological graphs with at most four crossings per
  edge*](https://arxiv.org/abs/1509.01932v2), for the deletion step extending
  the order-24 endpoint to (1).
- The locally consolidated and independently reviewed
  [`r=27` dependency chain](../albertson_r27_reviewed_chain/README.md), for
  the proved universal endpoint `cr(24,132)>=165` and its propagation
  controls.
- L. Rabern,
  [*Coloring graphs with dense neighborhoods*](https://arxiv.org/abs/1209.3646),
  M. Stehlík,
  [*Critical graphs with connected
  complements*](https://doi.org/10.1016/S0095-8956(03)00069-8), and the
  Andrásfai--Erdős--Sós triangle-free minimum-degree theorem, for the final
  structural deductions.

The mathematical result uses these named theorems and the reviewed campaign
endpoint; they are not reproved by the scripts.  Catalogue
completeness, the old `r=29` barrier configurations, and any assertion of the
exact value of `cr(K_30)` are outside the trust boundary.  The executable
boundary is CPython exact arithmetic and SHA-256.  There is no solver,
randomness, graph catalogue, external runtime input, or exhaustive graph
generation.

A search of Discovery Net through indexed height 4363 initially found no
committed `r=30` result.  During the pre-publication fetch, the concurrent
proof candidate appeared at Git commit `7bf1e64`.  The present contribution
is an independent validation and alternative two-row route, not a priority
claim for the r=30 theorem or the deficit method.
