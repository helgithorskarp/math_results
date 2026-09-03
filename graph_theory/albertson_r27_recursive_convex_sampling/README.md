# Recursive convex sampling closes two Albertson `r=27` rows

This note proves a universal 50-vertex crossing-number inequality and uses it
to eliminate the 714- and 715-edge rows in the remaining order-53 frontier of
Albertson's conjecture.  Combined with the independently established
order-54 closure, only the row `(n,m)=(53,713)` remains.

## Result

Every simple graph `H` with 50 vertices and `q` edges satisfies

```text
cr(H) >= 26q - 11706.                              (1)
```

Consequently, every 53-vertex simple graph `G` with `m` edges satisfies

```text
cr(G) >= ceil(
    (26m binom(51,48) - 11706 binom(53,50)) / binom(49,46)
).                                                  (2)
```

At the three frontier edge counts, the unrounded values in (2) are

| `m` | rational bound | integer conclusion |
|---:|---:|---:|
| 713 | `55914547/9212` | `cr(G) >= 6070` |
| 714 | `14046318/2303` | `cr(G) >= 6100` |
| 715 | `56455997/9212` | `cr(G) >= 6129` |

Since the standard drawing gives `cr(K_27) <= Z(27)=6084`, the last two rows
cannot contain a counterexample.  The stronger full recursion computed by the
verifier gives floors `6071, 6100, 6130` at the three rows, respectively, but
the reusable line (1) already supplies the claimed eliminations.

## Convex induced-sampling lemma

Let `f(q)` be an integer lower bound for the crossing number of every simple
`s`-vertex graph with `q` edges.  Let `f_bar` be the greatest convex
piecewise-linear function on `[0,binom(s,2)]` whose value at every integer
`q` is at most `f(q)`.  Then every simple `n`-vertex, `m`-edge graph satisfies

```text
cr(G) >= ceil(
    binom(n,s) / binom(n-4,s-4)
    * f_bar(m s(s-1) / (n(n-1)))
).                                                  (3)
```

To prove (3), fix a crossing-minimal good drawing and sum over all induced
`s`-vertex subdrawings.  Every crossing occurrence survives in
`binom(n-4,s-4)` samples and every edge survives in `binom(n-2,s-2)` samples.
If `q_S` is the edge count of a sample, then

```text
sum_S q_S / binom(n,s) = m s(s-1)/(n(n-1)).
```

The inherited drawing of each sample has at least `f(q_S)` crossings.
Because `f_bar(q_S) <= f(q_S)`, Jensen's inequality for the convex function
`f_bar` gives (3).  No assertion is made that the edge-count distribution of
the samples is arbitrary; replacing it by its mean is a relaxation in the
lower-bound direction.

## Exact recursive certificate

For `n>=4` and `0<=m<=binom(n,2)`, start with the integer-rounded maximum

```text
F_n(m) >= max(
    0,
    ceil(m - 3(n-2)),
    ceil(7m/3 - 25(n-2)/3),
    ceil(37m/9 - 155(n-2)/9),
    ceil(5m - 203(n-2)/9)
).
```

Proceed in increasing order of `n`.  For every `4<=s<n`, apply (3) using the
already computed table `F_s`, and define `F_n(m)` to be the maximum of the
base value and all these sampled values.  Induction on `n` proves that every
entry is a universal crossing-number lower bound.

The dependency-free verifier performs this recursion with exact rational
arithmetic through order 53.  It constructs every lower convex hull in two
different ways (an orientation-based monotone chain and pooled adjacent
secant slopes), compares the hulls, checks convexity and the minorant
inequality at every integer edge count, and finally verifies

```text
F_50(q) >= 26q-11706  for all 0<=q<=1225.
```

Equality in this computed comparison occurs exactly for
`q in {633,634,635,636,637,638,639}`.  This exhaustive finite check is the
computer-assisted part of (1); the sampling lemma and its induction bridge
are deductive.

## Reproduction and trust boundary

Run with CPython 3.9 or later:

```sh
python3 verify.py
```

The expected first line is

```text
PASS recursive convex induced-sampling audit
```

The final table digest is
`55da0a3d413620951dba0ac52618fa24f09d59de43a0c7e8a0f3927283036f43`.

The script uses only arbitrary-precision integers, `fractions.Fraction`, and
binomial coefficients.  It uses no floating point, solver, randomness,
network access, generated input, or imported project code.  Its trust boundary
is CPython exact arithmetic, the four imported universal linear inequalities,
and the standard good-drawing normalization.  The two hull algorithms are an
internal independent check of the finite convexification; they do not
independently reprove the imported crossing inequalities.

## Sources and novelty scope

* A. Büngener and M. Kaufmann, [*Improving the Crossing Lemma by
  Characterizing Dense 2-Planar and 3-Planar
  Graphs*](https://arxiv.org/abs/2409.01733v2), Theorem 6, for the
  `37/9` and `5` inequalities.  Their theorem is unconditional for every
  simple graph with more than two vertices.
* J. Pach, R. Radoičić, G. Tardos, and G. Tóth, [*Improving the Crossing
  Lemma by Finding More Crossings in Sparse
  Graphs*](https://doi.org/10.1007/s00454-006-1264-9), for the `7/3`
  inequality.  The planar bound is Euler's formula.
* A. Sadhu, [*Albertson's Conjecture Holds for `r` at Most
  26*](https://arxiv.org/abs/2609.01682v1), for the September 2026 frontier
  and `Z(27)=6084`.
* The preceding [two-scale order-54
  closure](../albertson_r27_order54_two_scale_sampling/README.md), which
  removes the other surviving order independently.

One-stage integer-aware sampling and two particular deletion iterations were
already present in earlier frontier notes.  The contribution here is closure
of the rounded bounds under arbitrary finite recursive induced sampling,
organized by exact convex minorants; its 50-vertex supporting line; and the
resulting elimination of the last two higher-edge order-53 rows.  Targeted
searches of the cited literature and the committed Discovery Net found no
prior statement of this recursion, line, or consequence.  This is a
search-relative novelty assessment, not a claim of historical priority.

This result does not prove Albertson's conjecture for `r=27`.  The remaining
analytic gap at `(53,713)` is 13 crossings under the full recursion:
`F_53(713)=6071<6084`.
