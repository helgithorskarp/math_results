# A second-moment barrier for four-deletion sampling at Albertson `r=27`

This note locates a limitation of the induced-deletion route for the sole
surviving Albertson frontier row

```text
|V(G)|=53,  |E(G)|=713,  chi(G)=27.
```

It is a method-limit theorem, not a proof of Albertson's conjecture.  The
current recursively closed order-49 crossing table, even when combined with
the exact first **and second** moments of all four-vertex-deletion edge
counts, can certify at most `cr(G)>=6073`.  The target is `Z(27)=6084`.
Thus a successful four-deletion argument must use higher-order incidence
realizability or a stronger local crossing bound, rather than only degree
squares.

## Setting and strengthened numerical hypotheses

Let `G` be a hypothetical counterexample in the displayed row, and put

```text
x_v=d_G(v)-26,  h=|{v:x_v>0}|.
```

Criticality and the handshake lemma give

```text
x_v>=0,  sum_v x_v=48.
```

The committed structural frontier gives `h>=18`.  Moreover, the complement
`H` is factor-critical.  It has minimum degree at least two: if `u` had the
unique neighbour `v`, then `H-v` would have the isolated vertex `u` and could
not have a perfect matching.  Hence

```text
0<=x_v=26-d_H(v)<=24.                              (1)
```

For a four-set `T`, write `q_T=|E(G-T)|`.  Then

```text
q_T=713-sum_{v in T}d_G(v)+e_G(T)
   =609-sum_{v in T}x_v+e_G(T).                    (2)
```

At least 14 positive excesses remain outside `T`, so the excess inside `T`
is at most 34.  Together with `0<=e_G(T)<=6`, this gives

```text
575<=q_T<=615.                                     (3)
```

## The two exact moments

Put

```text
S0 = C(53,4),
S1 = sum_T q_T,
S2 = sum_T C(q_T,2),
A  = sum_v C(d_G(v),2).
```

Every edge survives `C(51,4)` four-deletions.  An unordered pair of adjacent
edges spans three vertices and survives `C(50,4)` deletions, while a disjoint
pair spans four vertices and survives `C(49,4)`.  Therefore

```text
S1 = 713 C(51,4),
S2 = A C(50,4)+(C(713,2)-A)C(49,4).                (4)
```

Writing `B=sum_v C(x_v,2)`, the identity
`C(26+x,2)=C(26,2)+26x+C(x,2)` gives

```text
A=18473+B.                                         (5)
```

Under (1), `sum x_v=48`, and `h>=18`, convexity shows that `B` is at most

```text
C(24,2)+C(8,2)=304,
```

attained in the numerical relaxation by

```text
(x_v)=0^35,1^16,8,24.                              (6)
```

The minimum is zero, attained by `0^5,1^48`.  The verifier enumerates all
298 feasible values of `B` (not every integer from 0 through 304 occurs).

## Sharp moment relaxation

Let `F_49(q)` be the current recursively closed integer lower bound for the
crossing number of every 49-vertex, `q`-edge graph, including the presently
available simple 5-planar slope-6 line.  Restriction of a crossing-minimal
good drawing gives

```text
C(49,4) cr(G) >= sum_T F_49(q_T).                  (7)
```

For each feasible `B`, relax the multiplicities of the integer values
`q_T in {575,...,615}` to nonnegative real numbers, retaining exactly the
three constraints (4) and `sum_T 1=S0`.  This is the strongest possible
lower bound on the right side of (7) that uses only this support and the
first two moments.

The relaxation is solved exactly by matching primal and dual certificates.
For `0<=B<=11`, the primal is supported on `q=608,610,615` and the dual is
the quadratic minorant

```text
P_0(q)=q^2/35-49q/5-1571/7 <= F_49(q).
```

For `12<=B<=304`, the primal is supported on `q=575,608,615` and the dual is

```text
P_1(q)=593q^2/9240-70417q/1320+1007883/77
      <=F_49(q).
```

Both pointwise inequalities are checked at all 41 integer arguments.  The
three primal weights are obtained by solving (4); they are nonnegative on
the stated ranges and have the same objective as the corresponding dual.
Weak duality in both directions therefore proves exact optimality.

The optimum increases with `B` and is largest at `B=304`.  After division by
the crossing multiplicity, its exact value is

```text
742965030571 / 122358390 = 6072.039935888...
```

and hence it yields only

```text
cr(G)>=6073.                                       (8)
```

This is eleven crossings below 6084.

## An integral obstruction

The limitation is not caused by fractional sample multiplicities.  For the
relaxed degree multiset (6), the following **integer** distribution has the
exact values of `S0,S1,S2` from (4)--(5):

| `q` | number of four-sets |
|---:|---:|
| 575 | 8,153 |
| 607 | 1,024 |
| 608 | 224,909 |
| 615 | 58,739 |

Its local-table sum is

```text
1,286,520,178,
```

so (7) would again give only `cr(G)>=6073`.  The least integer sum that would
certify 6084 is

```text
6083 C(49,4)+1 = 1,288,841,709,
```

leaving a gap of `2,321,531` local crossings.

No graph-realizability claim is made for (6) or for the displayed
distribution.  That is exactly the point of the barrier: (1)--(5), sample
integrality, and the entire current order-49 table do not distinguish this
obstruction from a genuine survivor.  Any successful continuation must add
constraints coupling particular four-sets to their incidences (or improve
the local table).

## Reproduction and trust boundary

Run with CPython 3.9 or later; there are no third-party dependencies:

```sh
python3 verify.py
python3 independent_check.py
```

The primary checker reconstructs the full recursive table through order 53,
constructs its lower convex hull in two ways, enumerates all feasible degree
square values, and verifies the explicit primal-dual certificates.  The
independent checker uses a separately organized partition enumeration and
enumerates every pointwise feasible quadratic through three local-table
points; it recovers the same optimum and integral obstruction.

Both use exact integer and `fractions.Fraction` arithmetic.  There is no
floating point, solver, randomness, generated input, external data, or
project import.  The scripts certify the finite recursion and optimization;
the good-drawing restriction, moment double counts, factor-critical degree
cap, and LP-duality bridge are deductive.

The imported mathematical boundary consists of the universal crossing lines
used by the recursive table, Sadhu's September 2026 `(53,713)` frontier, the
committed factor-critical-complement lemma, and the committed theorem
`h>=18`.

## Sources and novelty scope

- A. Sadhu, [*Albertson's Conjecture Holds for `r` at Most
  26*](https://arxiv.org/abs/2609.01682v1), for the connected-complement
  order-53 frontier.
- A. Büngener and M. Kaufmann, [*Improving the Crossing Lemma by
  Characterizing Dense 2-Planar and 3-Planar
  Graphs*](https://doi.org/10.7155/jgaa.v29i3.3000), for the strongest
  universal linear inputs to the recursive table.
- A. Büngener, J. Franz, M. Kaufmann, and M. Pfister, [*A First View on the
  Density of 5-Planar Graphs*](https://arxiv.org/abs/2505.24364v3), for the
  simple 5-planar density input.
- The preceding [recursive convex-sampling
  certificate](../albertson_r27_recursive_convex_sampling/README.md),
  [three-deletion barrier](../albertson_r27_deletion_depth_barrier/README.md),
  [factor-critical complement reduction](../albertson_r27_complement_matchings/README.md),
  and [`h>=18` structural closure](../albertson_r27_order53_h14_h16_closure/README.md).

Targeted primary-literature and committed-graph searches found no prior
statement of this exact four-deletion moment barrier.  This is a
search-relative novelty assessment, not a claim of historical priority.
