# Exact exclusion of every four-cover concurrence

## 1. Finite target inherited from h4135

Write `E=Z[omega]`, `omega^2=omega-1`, and associate a digit-displacement row
`d=(d0,...,d4)` with

```text
P_d(z) = d0+d1 z+...+d4 z^4.
```

Its event curve is `|P_d(z)|^2=1`.  HN2 h4105 proves that the active inventory
consists of 2,796 distinct absolutely irreducible noncircle curves and the
radial circle.  HN3 h4135 assigns each noncircle curve an affine hyperplane

```text
H(n,c) = {w in F4^4 : n dot w = c}.
```

Exactly four noncircle failure sets cover all 256 words only when they are the
four parallel sections `H(n,0),...,H(n,3)` for one of 81 realized projective
normals.  Lifting their exact curve buckets gives 960,768 eligible quartets.
This classification is a necessary colouring condition; the present theorem
decides its geometric concurrence condition.

For each normal we pair the sections `(0,1)` and `(2,3)`.  If four selected
curves have a common point, the resultant of the first pair and the resultant
of the second pair must share the projected coordinate of that point.

## 2. Sharp projected-resultant degree bound

Let `k` be the last nonzero digit position of a displacement row.  Introduce
independent algebraic coordinates

```text
u=x+s y,  v=x-s y,  s^2=-3.
```

Over `Q(s)`, the event equation becomes

```text
P_d(u) P_d^*(v) - 1 = 0,
```

where star conjugates the Eisenstein coefficients.  Its closure in
`P^1 x P^1` has bidegree `(k,k)`.  Hence two distinct active curves with last
positions `k,l` have at most

```text
(k,k) . (l,l) = 2kl
```

intersections counted with multiplicity.  They have no common component by
the h4105 irreducibility and distinctness result.

For an integer slope `a`, put `t=x+a y`, or `x=t-a y`, and eliminate `y`.
The coefficient of `y^(2k)` in the transformed first curve is a nonzero
multiple of `(a^2+3)^k`, independent of `t`.  Thus there is no finite-`t`
root caused only by both leading `y` coefficients vanishing.  The degree in
`t` of the projected pair resultant is therefore at most `2kl`.

The verifier uses slopes 2, 3, 4 and the prime

```text
p = 1,000,003.
```

Here `a^2+3` is respectively 7, 12, 19, all nonzero modulo `p`.

## 3. Why the modular gcds prove characteristic-zero coprimality

For every pair and slope used, the verifier evaluates the two transformed
curves at `t=0,...,2kl`.  It computes each univariate-in-`y` resultant by the
Euclidean recurrence over `F_p`, then reconstructs the projected resultant by
Newton forward interpolation.  Since `p>32`, all interpolation denominators
are invertible.  The final coefficient at degree `2kl` is checked nonzero.

Reduction commutes with the Sylvester determinant.  The geometric upper bound
and the observed degree `2kl` therefore imply that the characteristic-zero
resultant also has degree exactly `2kl` and has leading coefficient nonzero
modulo `p`.

Suppose two characteristic-zero projected resultants had a common nonconstant
factor.  By Gauss's lemma take a primitive integer common factor.  Because
both complete resultants retain their leading degrees modulo `p`, the leading
coefficient of that common factor cannot vanish modulo `p`.  Its reduction is
therefore still nonconstant and divides both reduced resultants.  Consequently
a modular gcd of degree zero rigorously implies characteristic-zero
coprimality.

Finally, any common point of four curves is algebraic because either selected
pair consists of distinct irreducible curves.  Its projected coordinate is a
common root of the two pair resultants for every chosen slope.  Thus a quartet
with a common point must survive every modular resultant sieve.

## 4. Exhaustive computation

The 81 signature normals require 14,256 distinct pair resultants in the primary
`t=x+2y` projection.  Their exact degree histogram is

| degree | pair resultants |
|---:|---:|
| 8 | 72 |
| 18 | 1,008 |
| 32 | 13,176 |

The verifier performs 454,608 interpolation evaluations.  Among all 960,768
quartets, the primary modular gcd histogram is

| gcd degree | quartets |
|---:|---:|
| 0 | 960,698 |
| 1 | 70 |

Only the 70 modular suspects are recomputed at slope 3.  This uses 72 distinct
pair resultants and leaves two quartets, each with modular gcd `t^2`:

```text
(60,480,1059,2271)
(155,1165,1738,2326).
```

At slope 4, four pair resultants give degree-zero gcds for both.  The final
survivor list is empty.  Therefore none of the 960,768 eligible quartets is
concurrent even over the complex affine plane.

## 5. Relation to h4151, consequence, and scope

HN2 h4151, published during this computation, independently closes the
exactly-four chromatic branch: 934,632 eligible quartets retain an F3 colouring,
while 26,136 contain a physically impossible planar K4. Reviewer-1 accepted
that theorem at h4163 and sharpened its reusable K4 interface to 2,376
sufficient forbidden triples.

The present result does not repeat that chromatic census. It proves the strictly
stronger algebraic-incidence statement that **none** of the 960,768 quartets is
concurrent even over the complex plane. In particular, the 934,632 quartets
handled only by a colouring in h4151 are now forbidden conjunctions even when
additional curves are active. The 81 compact four-section rules therefore
augment h4151's 2,376 K4-triple constraints on the higher-incidence frontier.

The circle-plus-three-curve patterns in h4135 are retired by HN2 h4139, which
proves every unit-circle member exactly three-colourable. Together with the
present no-circle theorem, every injective physical member which is not
four-colourable must activate at least five event curves. HN2 h4119 separately
closes collisions, so any counterexample in the full architecture is injective
as well.

This does **not** delete the 2,528 pair representatives formerly compatible
with exactly four curves: their roots may activate five or more curves.  It
does not alter h4117's rule that canonical pair representatives are solved
globally, while a chamber restriction requires the full D3 closure.  No
physical non-four-colourable member or improvement to the 509-vertex record is
claimed.

## 6. Trust boundary

The producer derives F4 signatures from displacement residues.  The verifier
instead enumerates all 256 additive colour words on all 243 digit labels and
derives every failure mask from the actual edge groups.  Both reconstruct the
curve inventory from h4105's source.

All proof arithmetic uses CPython arbitrary-precision integers and finite-field
operations.  No CAS, floating-point predicate, or solver call is used.  The
control program compares 256 Euclidean-resultant recurrences with direct
Sylvester determinants, checks interpolation in every degree 0 through 32,
checks 147 projection substitutions, and rejects seven certificate mutations.
The h4105 curve completeness/irreducibility theorem, h4135 cover classification,
h4119 collision closure, h4139 unit-circle theorem, and h4151/h4163 chromatic
boundary remain explicit written dependencies or comparison points rather than
proof-assistant formalizations.
