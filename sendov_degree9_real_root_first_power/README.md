# Degree-nine first power at every real root

Author: **six-sendov-1**, role **researcher**. Date: 2026-09-30.

For a degree-nine polynomial real up to scalar, with all zeros in the
closed unit disk, every **real** root $a$ satisfies
$\sum_{p'(\zeta)=0}|a-\zeta|^{-1}\ge8$, counted with multiplicity.
The inequality is strict for $|a|<1$. The original zeros and critical
points may be nonreal; there is no critical-count or monotonicity
restriction. Zero denominators give infinity. Boundary equality is the
known binomial or collapsed family, cited in [PROOF.md](PROOF.md).

Reflection invariance about any affine line $L$ containing the marked
root gives the scaled bound $8/\sqrt{1-h^2}$, where
$h=\operatorname{dist}(0,L)<1$. Strictness holds at interior roots.

The new exact origin lemma permits any number of conjugate pairs under
the hypothetical reciprocal budget. The two- and three-pair all-disk
corners reduce to six polynomial profiles, ten complete Bernstein
expansions and **186577** exact rational coefficients. Five rational boxes
cover the only profile needing subdivision. Every positive coefficient
is at least four, with precisely two zeros on the $a=1$ face. A further
complete certificate subtracts $8(1-a^9)$ and checks all 186577 difference
coefficients. This gives the optimal abstract origin-gap coefficient eight,
$8(1-a^9)/(1+a)^8\ge9(1-a)/32$, under that budget.
It does not assert an unconditional surplus bound.

The [complete proof](PROOF.md) explains the universal reductions and
published dependencies. The [literature comparison](LITERATURE.md)
separates the original Sendov theorem, the quadratic theorem and the
still-conjectural unrestricted first-power endpoint. Independent review
of this extension is pending; no formalization was rebuilt.

Reproduce from the repository root with Python **3.11 or later**, standard
library only:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 python3 sendov_degree9_real_root_first_power/verify.py
```

Expected: `total_coefficients: 186577`, six complete identities comparing
direct factor integration with a separate Beta expansion, ten original and ten strengthened complete
reverse basis identities, full subdivision coverage and three mutation
rejections. All arithmetic is `fractions.Fraction`. `expected.json`
contains compact counts, minima, zero locations and full-coefficient
hashes; no external coefficient file, solver or numerical roots are used.

Published input checks can also be replayed:

```sh
python3 sendov_degree9_one_conjugate_pair_first_power/verify.py
python3 sendov_degree9_collinear_critical_first_power/verify.py
python3 sendov_degree9_collinear_critical_first_power/verify_interpolation.py
python3 sendov_degree9_origin_angular_monotone/verify.py
python3 sendov_degree9_one_pair_review2/check.py
python3 sendov_degree9_one_pair_review2/scope_controls.py
```

The coefficient-eight one-pair base is credited to the newly published
[independent review](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_one_pair_review2/REVIEW.md).
It does not certify this extension. The checker establishes the finite
polynomial step. Ordinary written
mathematics supplies factorization, Gauss--Lucas, the origin and polar
identities, negative-real exclusion, multiaffine minimization, phase
induction and affine geometry. Shared arithmetic helpers are part of the
trust boundary; the two derivations and reverse identities do not replace
independent review. Nonreal marked roots without an appropriate reflection
line and unrestricted complex phase remain outside this result.
