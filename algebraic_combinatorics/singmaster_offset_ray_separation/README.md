# Strict Pascal rays separate proportional Singmaster offset curves

For positive integers `a,b` and integers `x>=y>=0`, put

```text
D = floor((x-y)/(a+b)),
U_r = binom(x-ar, y+br)       (0 <= r <= D).
```

These are the binomial coefficients encountered while moving from `(x,y)`
in the offset direction `(-a,+b)`.

## Theorem

The positive sequence `U_0,...,U_D` has strictly decreasing successive
ratios.  Equivalently, whenever `1 <= r < D`,

```text
U_r^2 > U_(r-1) U_(r+1).
```

Consequently:

1. every integer occurs at most twice on an inward Pascal ray;
2. if `U_m=U_0` for some `m>=1`, then

   ```text
   U_r > U_0  for 0<r<m,
   U_r < U_0  for m<r<=D;
   ```

3. for a fixed positive direction `(a,b)`, the natural-number loci

   ```text
   E_m(a,b) = {
       (x,y): binom(x,y)=binom(x-ma,y+mb)
   }
   ```

   are pairwise disjoint as `m=1,2,...` varies (with the binomial
   coefficients required to be defined).

The last statement gives a uniform separation theorem for proportional
fixed-offset curves in Jenkins's approach to repeated binomial coefficients.
In particular, all equal-offset curves

```text
binom(x,y)=binom(x-d,y+d),     d=1,2,...,
```

are pairwise disjoint in the natural Pascal triangle.  This does **not** say
that the individual curves with `d>=3` have no natural points.

## Proof

Write

```text
n_r = x-ar,
k_r = y+br,
l_r = n_r-k_r = x-y-(a+b)r.
```

For `0<=r<D`, factorial cancellation gives

```text
q_r := U_(r+1)/U_r
     = (l_r)_(a+b) / ((n_r)_a (k_r+1)^(b))
     = product_(i=0)^(a-1) (l_r-i)/(n_r-i)
       product_(j=0)^(b-1) (l_r-a-j)/(k_r+j+1),                 (1)
```

where `(z)_s=z(z-1)...(z-s+1)` and
`(z)^(s)=z(z+1)...(z+s-1)`.  All displayed factors are positive.

Every factor in the first product strictly decreases with `r`.  Indeed, the
cross-multiplied numerator of

```text
(l_r-i)/(n_r-i) - (l_(r+1)-i)/(n_(r+1)-i)
```

is

```text
(a+b)(n_r-i)-a(l_r-i)
  = a k_r + b(n_r-i) > 0.                                    (2)
```

Every factor in the second product also strictly decreases: on replacing
`r` by `r+1`, its positive numerator drops by `a+b` while its positive
denominator rises by `b`.  Thus `q_(r+1)<q_r`.  Since

```text
U_r^2/(U_(r-1)U_(r+1)) = q_(r-1)/q_r,
```

strict log-concavity follows.

The logarithms `log U_r` therefore form a strictly concave finite sequence.
A horizontal line can meet a strictly concave sequence at no more than two
indices, proving the raywise multiplicity assertion.  If `U_0=U_m`, strict
concavity puts every intermediate term strictly above their common value.
For `r>m`, apply strict concavity to the indices `0,m,r`: because the middle
value equals the value at zero, the value at `r` must be strictly smaller.
This proves the sign statement.  Finally, a common point of `E_m(a,b)` and
`E_s(a,b)`, with `0<m<s`, would give the forbidden threefold equality
`U_0=U_m=U_s`.

## Relation to prior work

Belbachir and Szalay proved that binomial coefficients on an arbitrary
Pascal ray form a log-concave, hence unimodal, sequence.  That theorem is an
essential prior-art boundary: ray log-concavity by itself is not new here.
The result above supplies strictness for the offset direction `(-a,+b)`, an
explicit factorwise proof, and the proportional-curve separation and sign
corollaries.

Jenkins studies the curves

```text
binom(x,y)=binom(x-a,y+b)
```

and explicitly identifies control of common intersections as relevant to
Singmaster's conjecture.  The theorem here controls all intersections among
curves whose offset vectors lie on one positive rational ray.  It does not
control intersections between nonproportional offset vectors and therefore
does not prove Singmaster's bounded-multiplicity conjecture.

See [SOURCES.md](SOURCES.md) for the primary-source and search boundary.

## Reproduction

Only CPython's standard library is required (tested with CPython 3.11.8):

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
diff -u EXPECTED_OUTPUT.txt <(PYTHONDONTWRITEBYTECODE=1 python3 verify.py)
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
sha256sum -c SHA256SUMS
```

The verifier uses arbitrary-precision integers and exact rational arithmetic.
It independently evaluates binomial coefficients from `math.comb`, checks
the factorial ratio formula, checks strict ratio descent and strict
log-concavity on a bounded parameter box, audits the level-set/sign
consequences, and includes the classical `3003` collision.  These finite
checks audit the formulas and boundary conventions; the universal theorem
rests on the proof above.

## Scope

This result does not classify the natural points of any unsolved individual
offset curve, prove complex nonsingularity of the algebraic curves, bound
intersections of nonproportional offset curves, or settle Singmaster's
conjecture.  An exact low-degree computer-algebra probe of complex
nonsingularity motivated the search but is outside the theorem and evidence
boundary.
