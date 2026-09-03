# Integer-aware induced sampling at the Albertson `r=27` frontier

This note strengthens the sampled crossing-number calculation in Ankan
Sadhu's [September 2026 frontier
paper](https://arxiv.org/abs/2609.01682v1).  It does **not** prove Albertson's
conjecture for chromatic number 27.  Its contribution is a general rounding
lemma and an exact reduction of the remaining numerical gaps.

## Lemma

Suppose that every finite simple graph `H` with `v > 2` vertices and `e`
edges satisfies

```text
cr(H) >= a e - b(v-2),
```

where `a` is an integer.  If `G` has `n` vertices and `m` edges, and
`4 <= s <= n`, then

```text
cr(G) >= ceil(
    a m (n-2)(n-3) / ((s-2)(s-3))
  + ceil(-b(s-2)) n(n-1)(n-2)(n-3)
      / (s(s-1)(s-2)(s-3))
).
```

The inner ceiling is the point: it is applied to every induced `s`-vertex
subgraph before averaging.  In general it is stronger than applying the
continuous inequality to the average and rounding only once at the end.

### Proof

Fix a crossing-minimal good drawing of `G`.  For every `s`-element vertex set
`S`, let `m_S` be the number of edges of `G[S]`.  Since crossing number is an
integer and `a m_S` is an integer,

```text
cr(G[S]) >= a m_S + ceil(-b(s-2)).
```

Sum this inequality over all `S`.  Every edge occurs in
`binom(n-2,s-2)` induced subgraphs, while every crossing, whose two edges have
four distinct endpoints in a good drawing, occurs in `binom(n-4,s-4)` of
them.  Therefore

```text
cr(G) binom(n-4,s-4)
  >= a m binom(n-2,s-2) + ceil(-b(s-2)) binom(n,s).
```

Dividing, evaluating the two binomial ratios, and finally using the
integrality of `cr(G)` proves the formula.

## Application to the surviving cases

Büngener and Kaufmann proved the universal bound

```text
cr(H) >= 5e(H) - 203(v(H)-2)/9.
```

Thus `a=5`, `b=203/9`, and the inner constant is
`-floor(203(s-2)/9)`.  Optimizing over every `4 <= s <= n` gives:

| `n` | `m` | best `s` | unrounded rational bound | integer conclusion |
|---:|---:|---:|---:|---:|
| 54 | 726 | 24 | `10759164/1771 = 6075.191...` | `cr(G) >= 6076` |
| 53 | 713 | 24 | `31923025/5313 = 6008.474...` | `cr(G) >= 6009` |
| 53 | 714 | 24 | `32069650/5313 = 6036.071...` | `cr(G) >= 6037` |
| 53 | 715 | 23 | `1952535/322 = 6063.773...` | `cr(G) >= 6064` |

At `(n,m)=(54,726)`, the continuous sampled bound used in the frontier paper
is `977041/161 = 6068.577...`, whose integer consequence is `cr(G) >= 6069`.
Integer-aware sampling raises this to 6076.  Since `Z(27)=6084`, the remaining
integer deficit is 8 crossings.  It does not change the edge threshold: the
same method still closes at `m=727`.

For the order-53 cases, the continuous best integer conclusions are 6003,
6030, and 6058, respectively; the strengthened conclusions above are 6009,
6037, and 6064.  These cases remain open under this estimate.

## Reproduction

Python 3.9 or later is sufficient; there are no third-party dependencies.

```sh
python3 verify.py
```

The program uses only integer arithmetic and `fractions.Fraction`.  It checks
the lemma's two binomial-ratio forms against one another, exhaustively
optimizes all allowed sample sizes in each surviving case, and verifies every
fraction and ceiling displayed above.

## Sources and trust boundary

- Sadhu, [*Albertson's Conjecture Holds for r at Most
  26*](https://arxiv.org/abs/2609.01682v1), especially Lemma 2.2 and the
  residue after Theorem 1.3.
- Büngener--Kaufmann, [*Improving the Crossing Lemma by Characterizing Dense
  2-Planar and 3-Planar
  Graphs*](https://arxiv.org/abs/2409.01733v2), Theorem 6(b).

The imported mathematical input is Büngener--Kaufmann's linear crossing
bound and the published `r=27` frontier reduction.  The averaging and
integrality argument is proved above.  The executable trust boundary is
CPython's integer arithmetic and `fractions.Fraction`; the script uses no
floating point for assertions, solver, randomness, network access, or project
imports.
