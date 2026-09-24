# Quantitative rounding of a light fractional matching

All logarithms are natural. A hypergraph is **linear** if two distinct
hyperedges intersect in at most one vertex. Its hyperedges here have size
three. A fractional matching is a nonnegative vector `x_e` with
`sum_(e contains v) x_e <= 1` at every vertex. Its value is `W=sum_e x_e`.

**Lemma.** Let the hypergraph have at most `N>=1` vertices, and let
`0<epsilon<=1/2`. If

```text
max_e x_e <= epsilon^6 / [10^8 log(400N/epsilon^2)],        (1)
```

then it has an integral matching of size at least `(1-epsilon)W`.

The case `W=0` is immediate. In the process below, a state with zero
fractional value is terminal and contributes zero in all later rounds.

This is a quantitative version of the classical nibble mechanism. The
proof is included with constants; no asymptotic matching theorem is a
black-box premise. It concerns an ordinary unweighted matching, whose
size is compared with the supplied fractional value.

## 1. A concentration fact, including its proof

Let `F` depend on finitely many independent Bernoulli variables `X_j` of
success probabilities `p_j`. Changing coordinate `j` changes `F` by at
most `c_j`. Put `c=max c_j` and `V=sum_j p_j c_j^2`. Then, for `t>0`,

```text
Pr(F-E F >= t) <= exp[-t^2 / (2(V+ct/3))].                (2)
```

If `c=0`, the variable is constant and the assertion is immediate.
Otherwise expose the coordinates in a fixed order. The Doob martingale
increment has the form `(X_j-p_j)a_j`, where `a_j` is determined by
earlier exposures and `|a_j|<=c_j`. This follows by coupling the same
remaining coordinates in the two conditional expectations. Its absolute
value is at most `c`, its conditional mean is zero, and its conditional
second moment is at most `p_j c_j^2`.

For `0<lambda<3/c`, the exponential series and
`l!>=2*3^(l-2)` for every integer `l>=2` give

```text
E[exp(lambda D_j) | past]
 <= exp{lambda^2 p_j c_j^2 / [2(1-lambda c/3)]}.
```

Indeed, bound the absolute `l`th moment by `c^(l-2)` times the second
moment and sum the geometric series. Iterating conditional expectations
and applying Markov's inequality gives an upper bound
`exp[-lambda t+lambda^2 V/(2(1-lambda c/3))]`. Substitution of
`lambda=t/(V+ct/3)` proves (2) when `V>0`; the zero-variance case is
constant. This is the usual Bernstein martingale argument.

## 2. One round with equal survival probabilities

Set

```text
alpha=epsilon/10,  q=1-alpha,  eta=alpha^2,
L=log(400N/epsilon^2)=log(4N/eta).
```

In a current feasible state, write `delta=max x_e` and `W=sum x_e`.
Independently mark each hyperedge `e` with probability `alpha x_e`.
Accept every marked hyperedge disjoint from all other marked hyperedges.
These accepted edges form a matching. Remove every vertex belonging to
any marked edge, including edges involved in collisions.

To equalize vertex survival, compute

```text
r_v = product_(e contains v) (1-alpha x_e).
```

Since `r_v>=1-alpha sum_(e contains v)x_e>=q`, also take an independent
coin at each vertex, retaining that vertex with probability `q/r_v`.
A vertex survives the round precisely when it has no incident marked
edge and this coin retains it. Thus each vertex has survival probability
exactly `q`. These extra coins are mutually independent and independent
of all marks. Their deletion probabilities are at most `alpha`, because
`r_v<=1` implies `q/r_v>=q`.

On the induced surviving hypergraph set the **raw** new weights to

```text
x'_e = x_e / [q^2(1+eta)].                              (3)
```

If any surviving vertex has raw load greater than one, terminate the
process and set its future fractional value to zero. Keep all matching
edges already accepted, including this round's. Otherwise continue with
the feasible weights (3). This termination rule avoids assuming that
all rounds simultaneously succeed.

Let `M` be the number of accepted edges in this round. Conditional on
`e` being marked, a union bound over the other marked edges meeting it
gives acceptance probability at least `1-3alpha`. Consequently

```text
E M >= alpha(1-3alpha) W.                               (4)
```

Extra deletion coins do not reject an already accepted edge: its vertices
are removed in either event and remain available for that matching edge.

## 3. The dependent survival calculation

Fix a vertex `v` and condition on its survival. This fixes its retention
coin and all incident marks. Every other coordinate remains independent
with its original probability.

For `e={v,a,b}`, linearity says that `e` is the only hyperedge containing
both `v,a`, both `v,b`, or both `a,b`. After the conditioning, the remaining
coordinates determining survival of `a` and `b` are therefore disjoint.
Each has conditional survival probability `q/(1-alpha x_e)`. If

```text
F_v = sum_(e={v,a,b}) x_e 1_(a survives) 1_(b survives),
```

then

```text
E[F_v | v survives]
 = q^2 sum_(e contains v) x_e/(1-alpha x_e)^2
 <= q^2/(1-alpha delta)^2.                              (5)
```

Unconditionally, for a whole hyperedge `e`, the three survival events
share only its own mark. Multiplying their marginal probabilities
counts this common unmarked event three times instead of once. Hence

```text
Pr(all three vertices of e survive)=q^3/(1-alpha x_e)^2.
```

In particular the expected raw fractional value in (3) is at least
`qW/(1+eta)`. These identities explicitly account for dependence; the
three survival events are not independent.

## 4. Controlling the new capacities

Continue to condition on survival of `v`. Its other-neighbor set consists
of disjoint pairs, one pair for each incident hyperedge, by linearity.
Attach weight `w_a=x_e` to each neighbor `a` in that pair. Thus
`sum_a w_a<=2`, and each `w_a<=delta`.

Changing the mark of an edge `f` not incident with `v` changes `F_v` by
at most

```text
c_f = sum_(a in f and a a neighbor of v) w_a <= 3delta.
```

Its marking probability is `alpha x_f`. Therefore

```text
sum_f (alpha x_f)c_f^2
 <= 3delta sum_a w_a sum_(f contains a) alpha x_f
 <= 6alpha delta.
```

Changing the extra deletion coin at a neighbor `a` changes `F_v` by at
most `w_a`. These coins have deletion probabilities at most `alpha`, so
their contribution to `V` in (2) is at most `2alpha delta`. All other
coordinates have zero influence. Thus (2) applies conditionally with

```text
V<=8alpha delta,  c<=3delta.                            (6)
```

Suppose for the moment that

```text
delta <= alpha^4/(2000L).                              (7)
```

Our parameters give `alpha<=1/20`, `q>=19/20`, `L>1`, and hence
`delta<=alpha/8`. For `0<=z<=1/4`, `(1-z)^(-2)<=1+4z` (multiply by
`(1-z)^2` to check). Using `z=alpha delta`, equation (5) and the threshold
`F_v<=q^2(1+eta)` leave a margin at least

```text
q^2(eta-4alpha delta) >= q^2 eta/2 >= eta/3.
```

With `t=eta/3`, (6), `alpha<=1`, and `eta<=1`, the exponent in (2) is
at least `eta^2/(180delta)`. By (7) this is at least `L`. Thus

```text
Pr(raw load at v > 1 | v survives) <= exp(-L).
```

A union bound over at most `N` vertices shows that the probability `P_bad`
of terminating this round is at most `N exp(-L)=eta/4`.

The raw new fractional value is always at most `W/[q^2(1+eta)]`.
Deducting all its possible contribution on bad outcomes gives, for the
actual new fractional value (zero on termination),

```text
E W_next >= [q-P_bad/q^2]W/(1+eta)
          >= (1-alpha-2eta)W.                           (8)
```

For the last inequality, `q^2>=3/4` implies `P_bad/q^2<=eta/3`, and
`(1-alpha-eta/3)/(1+eta)>=1-alpha-2eta`. No independence between the bad
event and the objective was assumed.

## 5. Iteration and constants

Let `T` be the least positive integer with `q^T<=epsilon/2`. In any
unterminated state through these rounds,

```text
max x_e <= delta_0 q^(-2T)
         <= 5delta_0/epsilon^2
         <= epsilon^4/(2*10^7 L)
          = alpha^4/(2000L).
```

Here minimality gives `q^T>q epsilon/2`, and `4/q^2<5`.
The last inequality is exactly hypothesis (1). Thus (7) is available
in every round, including after any history with positive probability.

Put `b=1-alpha-2eta` and `a=alpha(1-3alpha)`. Equations (4) and (8),
with the fractional value kept zero after termination, imply

```text
E(total matching size) >= aW sum_(t=0)^(T-1) b^t
                       = [a/(1-b)](1-b^T)W.
```

Because `eta=alpha^2`,

```text
a/(1-b)=(1-3alpha)/(1+2alpha)>=1-5alpha=1-epsilon/2,
b^T<=q^T<=epsilon/2.
```

The expected size is at least `(1-epsilon/2)^2 W`, which is at least
`(1-epsilon)W`. Some outcome therefore supplies the matching in the
lemma. Every output is a matching: accepted edges are disjoint within a
round, and their vertices are removed before subsequent rounds.

For rational input weights and rational epsilon, all per-round
probabilities, rescalings, and capacity tests are rational. The proof is
a finite randomized existence argument. It does not claim a practical
implementation at the very large graph orders in the resulting Tuza
cutoff, or a derandomized polynomial-time algorithm.
