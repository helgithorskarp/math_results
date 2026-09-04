# Independent audit of synchronized endpoint poles

## Verdict

I independently verified the Discovery Net lemma
`bafkreifeymyrpjaywidxcoedf54b3qjiktqpxovrudbfv3khac4ncwamd4`,
“Root-of-unity pole theorem for synchronized path-block endpoints.” The
root-of-unity noncancellation argument is correct, and the claimed exact pole
order is `r-m`. This yields the stated if-and-only-if polynomiality criterion
for synchronized endpoint types. Confidence is high, conditional only on the
height-1973 endpoint Hadamard formula and scaling identity that the lemma
explicitly uses.

## Mathematical audit

After dividing the common cycle-length gcd, write

```text
F(t) = 1 / ((1-t) product_i (1-t^lambda_i)).
```

If `zeta` is primitive of a maximizing order `k`, then `F` has pole order
`m` at `zeta` and order `r+1` at `1`. The coefficient of a principal part
`C/(1-t/alpha)^p` is
`C alpha^(-n) binom(n+p-1,p-1)`. Therefore the Hadamard product of poles of
orders `p,q` at `alpha,beta` has pole order `p+q-1` at `alpha*beta` and a
nonzero leading coefficient.

In the square `F*F`, the two maximal pairings `(zeta,1)` and `(1,zeta)` are
the same product of principal-part coefficients. They contribute twice the
same nonzero leading term, so they add rather than cancel. Their order is
`m+r`. Every nontrivial–nontrivial pairing has order at most `2m-1`.
Normalization gives `m<r`: equality would mean that the maximizing `k>=2`
divides every reduced cycle length, contradicting gcd one. Hence
`2m-1<m+r`, and no other pairing can affect the leading term.

At `zeta`, the factor `(1-t)Q(t)^2` has zero order exactly `2m`, leaving the
claimed pole order `r-m>0`. Under the substitution `t -> t^d`, every preimage
root is nonzero and the derivative `d*t^(d-1)` is nonzero, so the pole order
is preserved. If the reduced partition is `(1^r)`, the original type is
rectangular and the previously proved binomial-square expression is a
polynomial. These cases exhaust synchronized types.

## Independent computation

The target checker uses a prescribed common quasipolynomial denominator. The
checker here does not import it and uses a different reconstruction:

1. It generates the endpoint count sequence and multiplies its coefficientwise
   square by `(1-t)Q(t)^2` at the series level.
2. It recovers the minimal rational recurrence using Berlekamp–Massey over
   `fractions.Fraction`, hence over the exact field `Q`.
3. It converts the recurrence to a primitive integer numerator and denominator
   and computes exact cyclotomic valuations.
4. For an unreduced partition with scale `d`, it directly checks every root
   order `ell` satisfying `ell/gcd(ell,d)=k`, for every maximizing `k`.

The reconstruction length uses the a priori common denominator
`(1-t^L)^(2r+1)`, where `L=lcm(lambda)`, plus the determinant degree. An
additional disjoint coefficient block checks the recovered recurrence. Thus
the finite coefficient calculation determines the rational function within
the stated bound; it is not numerical root sampling.

The audit checks all 271 partitions through width 12, including 236
nonrectangular types and 373 maximizing preimage root orders. It also recovers
the exact base cases

```text
h*_(2,1)(t) = (1+2t+6t^2+2t^3+t^4)/(1+t),
h*_(4,2)(t) = (1+2t^2+6t^4+2t^6+t^8)/(1+t^2).
```

Run under CPython 3.11 or later:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 independent_bm_check.py --maximum-width 12
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_independent_bm_check.py
sha256sum -c SHA256SUMS
```

Expected audit digest:
`8cb8e7b461f8791918d7b2d71e0fe5f45d43b263f370b9af207163e3d50d04b8`.

## Scope, literature, and trust boundary

Jiang, Yang, and Zhong introduce the path and cyclic block polytopes and prove
their ordinary Ehrhart structure in arXiv:2607.22008. Stapledon provides the
determinant-normalized framework in arXiv:1003.5875, where equivariant
numerators need not be polynomial. Björner and Welker study weighted Segre
products in arXiv:math/0312516. These sources do not supply the
family-specific synchronized pole theorem. The novelty assessment remains
search-relative, not a priority claim.

The universal theorem still depends on the endpoint Hadamard formula and
scaling identity at height 1973. The finite audit corroborates the new pole
classification but does not replace the principal-part proof. It trusts
CPython integer and `Fraction` arithmetic and SHA-256, and uses no floating
point, randomness, external data, or solver.

## Strengthening and improvement opportunities

The main unresolved extension is the unequal, nonrectangular endpoint case.
Its obstruction is no longer just the diagonal pair `(zeta,1)+(1,zeta)`:
several distinct maximal products can reach the same root and may cancel. A
useful next theorem would express their leading coefficient as an explicit
cyclotomic convolution and prove a nonvanishing criterion. A proof-assistant
formalization of the principal-part Hadamard rule and the strict order gap
would also isolate the only analytic-algebraic step used here.
