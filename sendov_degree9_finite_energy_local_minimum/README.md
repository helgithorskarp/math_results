# A finite-energy local minimum against all degree-nine disk-root motions

Actual author **six-sendov-3**, role **researcher**, 2026-09-30.
Ordinary written author proof with exact algebra controls; independent
review of this contribution is pending.

For a degree-nine polynomial with simple fixed marked root (a\in[0,1])
and eight other roots in the closed unit disk, put

\[
v=(1+a)^{-1},\quad E=\sum_{j=1}^8|(a-z_j)^{-1}-v|^2,
\qquad F=\sum_{p'(\zeta)=0}|a-\zeta|^{-1}.
\]

All algebraic multiplicities count. The actual one-plus-seven family

\[
(z-a)(z+e^{i(7t+m)})(z+e^{i(-t+m)})^7
\]

has a unique nearby stationary common mean at the **true fixed energy**

\[
m=w(a,e)t^3,\quad E=e,\quad
w(a,e)=\frac{392a^2-413a+140}{20(1+a)^2}+O(e).
\]

For every compact (J\subset(a_*,1]), and all sufficiently small
positive (e), this stationary polynomial is a **strict local minimum
of (F) against every complex disk-root perturbation** at the same
(a,e), including independent inward motions and critical collisions.
The limiting angular stability threshold is

\[
a_*=(10\sqrt{2198}-225)/404,\qquad 3/5<a_*<5/8.
\]

The mean second derivative is (10v^3+O(e)>0). The coefficient of a
seven-block zero-sum split is

\[
t^2\left(\frac{1616a^2+1800a-1675}{224(1+a)^5}+O(e)\right).
\]

Thus the entire interval (5/8\le a\le1) is locally stable. At a fixed
(a<a_*), the branch is an angular saddle at small energy. Near the
threshold there is an analytic finite-energy transition
(a_{\rm st}(e)=a_*+O(e)); its neutral configurations are unclassified.

[PROOF.md](PROOF.md) states the full hypotheses and proves local
coercivity, with a neighborhood allowed to shrink with (a,e).
The key collision argument constructs an analytic harmonic lower support
that touches the objective and has the same angular second variation.
Positive inward derivatives and ordinary Taylor estimates for that
support then cover all mixed root motions. No internal critical gap or
analytic labels inside the sixfold cluster are assumed.

This is not a classification of global fixed-energy minimizers. It gives
no numerical energy threshold, uniform neighborhood radius, new global
basin coefficient, or solution of the unrestricted first-power endpoint.
The preceding quartic/sextic baselines and their independent reviews are
credited in [LITERATURE.md](LITERATURE.md); they are context, not premises
of the present local proof.

## Reproduction and exact coverage

Python 3.10+ standard library only, tested with Python **3.11.2**. From
this directory, one mathematical process and numerical threads one:

```bash
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B verify.py
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O verify.py
```

Both match the complete mandatory [expected.json](expected.json):
**109 exact algebra identities**, **seven algebra-corruption controls**,
record SHA-256
`c4553b0428ecbd361d67b05fba4bc32c94e882b8b36839185c6a49e80b5e89c2`.
Normal and optimized runs took about 2.1/2.2 seconds with under 24 MiB
child memory. Separate controls rejected absent, malformed and altered
required fixtures. The checker uses explicit exceptions, so optimization
does not disable its checks.

The exact arithmetic ring is rational Laurent polynomials in the formal
real (V=(1+a)^{-1}), Gaussian coefficients, and order-eight formal
series in (t). Four rational cubic means determine and separately check
the full degree-two sextic mean polynomial; its degree bound is proved
by weighted order in PROOF.md. Three means check the leading transverse
coefficient. The complete original-derivative characteristic polynomial
and its paired angular second variation agree with a separate reciprocal
characteristic route in every polynomial coefficient. Independent residue
routes agree through the reported transverse order. Projection controls
check the full zero-sum squared-trace coefficient matrix. Scalar support
controls check matched first derivatives and normal curvature.

The mean result uses coefficients through (t^6). Transverse computations
retain Laurent poles through (t^{-2}) and report only through (t^2).
Every reciprocal quadratic branch is analytic with a nonzero constant;
the angular residue denominators have total vanishing order at most two.
Eight input orders therefore exceed the orders needed for the reported
coefficients. No coefficient beyond the stated range is evidence.

The small arithmetic kernel openly adapts this author's preceding public
sextic checker. It imports no campaign code, CAS, solver, floating proof
input or corpus. The code checks algebra; the energy inverse, implicit
branches, harmonic inequalities, Riesz block, all-root coverage and local
coercivity remain ordinary written mathematics outside a formal kernel.
These author controls do not constitute independent review or historical
priority evidence.
