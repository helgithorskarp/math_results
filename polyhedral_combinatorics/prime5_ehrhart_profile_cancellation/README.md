# Geometric realization of prime-index Ehrhart cancellation

This directory gives an explicit infinite family of rational octagons whose
four nonintegral vertices realize the complete codimension-two cancellation
predicted by the prime-index local Fourier formula at `p=5`.

For an integer `t>=1`, let `P_t={x in R^2:A x<=b(t)}`, with rows

```text
A = [( 1, 1), (-1, 4), (-1, 1), (-4,-1),
     (-1,-1), ( 1,-4), ( 1,-1), ( 4, 1)]

b(t) = [11t, 29t+1, 11t+1, 29t+1,
        11t+1, 29t+3, 11t+3, 29t].
```

Every row is primitive and every inequality is an actual facet.  Four
alternating vertices are integral.  The other four have active determinant
five and normalized local character profiles

```text
(1,1), (3,3), (4,4), (2,2).
```

Thus they realize all four diagonal profiles in `F_5^*`, with equal point
volumes.  Their nonzero Fourier modes cancel because

```text
sum_(a=1)^4 (1-zeta^a)^(-2)=0
```

for a primitive fifth root `zeta`.  Consequently `P_t` has denominator five
but Ehrhart period one, with

```text
L_(P_t)(n)
 = ((364t^2+50t-5)n^2 + (20t-1)n + 2)/2.               (1)
```

[PROOF.md](PROOF.md) establishes the construction, local profiles,
cyclotomic cancellation, formula (1), and a four-facet obstruction showing
why the most naive all-bad quadrilateral cannot realize this pattern.  No
claim is made that eight facets are minimal.

Period-one rational polygons of arbitrary denominator were already known.
The new scoped bridge here is that the abstract cancellation in the
[prime-index local Fourier criterion](../prime_index_ehrhart_fourier/) is
compatible with one polygon's normal fan, support numbers, and face
volumes.  See [SOURCES.md](SOURCES.md) for the prior-art boundary.

## Reproduce

Using Python 3.11 or newer and only the standard library:

```sh
python3 verify.py
python3 -O verify.py
sha256sum -c SHA256SUMS
```

The verifier uses exact rational and finite cyclotomic arithmetic.  It
checks the construction symbolically as a polynomial in `t`, proves all
nonincident facet slacks positive for every `t>=1`, and independently
counts 120 dilates for `1<=t<=6`.  Thirty residue polynomials are recovered
from counts and tested on 30 unused values.  These computations audit the
formulas; the universal claim rests on the written proof and the accepted
prime-index local theorem.

This result is unformalized and not yet independently reviewed.
