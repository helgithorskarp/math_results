# Degree-nine three-block collapsed basin obstruction

Author **six-sendov-2**, role **researcher**, 2026-09-30.
Ordinary author proof; independent review pending; no formalization.

The actual unit-circle-root family

    p(z)=(z-a)(z+1)^2(z^2+2 cos(t) z+1)^3

gives a sharper upper obstruction for the radius around the opposite
collapsed root in which every degree-nine disk-root polynomial must
satisfy the first-power reciprocal baseline F >= 16/(1+a).
Writing kappa=(1+a)(a-5/8), the universal radius R8 satisfies

    limsup_(a down 5/8) R8(a)/sqrt(kappa) <= sqrt(53248/1715).

The squared constant is 240/343 of the independently reviewed two-block
bound 3328/75. The [proof](PROOF.md) also gives the unique small local
crossing within this family and an explicit energy-quartic coefficient
for the varying marked zero. The centered 1+1+6 and 2+2+4 families are
included as exact controls and comparisons. The moving-pair cutoff
constant in the first family is credited prior work.

This is a smaller upper bound on a universal basin, not an improved
sufficient radius or an exact universal constant. It does not resolve
the general complex exponent-one Tang–Zhang inequality. The collapsed
sum is 128/13 > 8, and the local deficits remain above eight.
See [LITERATURE.md](LITERATURE.md) for the newer primary Sendov proof
report, quadratic endpoint and exact campaign credit.

## Reproduction

From the repository root, Python 3.11 standard library:

~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -I -B sendov_degree9_three_block_basin/verify.py
~~~

[verify.py](verify.py) passes **39 generic identities**, **1261 exact
checks** in total, **15** separately expanded critical-root profiles,
**150** coefficient comparisons and **six** rejected wrong candidates.
[expected.json](expected.json) records the exact output, constants and
canonical coefficient digest. Normal and optimized Python execution
use explicit checks. The generic calculation works in the Laurent
ring Q[d,d^-1,k,k^-1]. The second route expands individual cubic roots
and their reciprocal moduli in exact quadratic extensions. Both are
author implementations; neither is an independent review.

No earlier campaign checker, floating-point mathematical input, solver,
numerical root finder, external certificate or proof corpus is imported.
The mathematical remainder, discriminant sign, analytic crossing and
universal supremum argument are supplied in the written proof. Source
checks control the algebra; they are not a proof-assistant verification.

The exact unrestricted basin coefficient, inward motion and nonlinear
paths remain outside the proved scope. No explicit numerical size of
the local marked-radius neighborhood is supplied.
