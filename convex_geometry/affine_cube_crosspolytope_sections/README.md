# Affine cube--crosspolytope section asymptotics

This directory proves the full interior affine extension of the central
cube--crosspolytope section theorem.  For (N=n+1), define

\[
D_n(\theta,\rho)=\frac{n!}{\sqrt N\,N^n}
\left|\left([-1,1]^N+\rho N B_1^N\right)
\cap\{\textstyle\sum_i x_i=\theta N\}\right|_n.
\]

The feasible interior is exactly

\[
\rho>(|\theta|-1)_+.
\]

Throughout this region, [PROOF.md](PROOF.md) establishes a locally uniform
all-orders expansion

\[
D_n(\theta,\rho)=\kappa(\theta,\rho)
 \frac{\beta(\theta,\rho)^n}{\sqrt n}
 \left(1+\frac{\gamma_1(\theta,\rho)}n+O_{\theta,\rho}(n^{-2})\right).
\]

The constants come from the unique saddle (r>|a|) of

\[
Z(a,r)=\frac{2\sinh a}{a}+\frac{e^a}{r-a}+\frac{e^{-a}}{r+a},
\qquad
\partial_a\log Z=\theta,
\quad -\partial_r\log Z=\rho.
\]

If (\Sigma=\operatorname{Cov}(Y,g(Y))) under density proportional to
(e^{aY-rg(Y)}), and (F=Ze^{-a\theta+r\rho}), then

\[
\beta=F/e,
\qquad
\kappa=\frac{\beta}{r\sqrt{2\pi\det\Sigma}}.
\]

The proof gives an invariant cumulant-tensor formula for (\gamma_1),
handles the singular interval and two ray components explicitly, and shows
that the pure cube and one-ray strata are exponentially smaller everywhere
in the strict interior.  The latter strata matter for a correct exact
formula when (|\theta|>1).

The [exact finite-section derivation](EXACT_SECTION.md) and
[implementation](exact_section.py) work in rational arithmetic for every
rational ((\theta,\rho)).  At (\theta=0), all formulas specialize to the
earlier central family.  At ((\theta,\rho)=(1/2,1)), for example,

\[
\gamma_1=-0.1387039848615766289\ldots,
\]

while at ((3/2,1)), beyond the cube's affine range,

\[
\gamma_1=-0.0533037262299038499\ldots.
\]

## Reproduce

Using CPython 3.11 or later and only its standard library:

~~~sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py > actual.json
diff -u EXPECTED.json actual.json
PYTHONDONTWRITEBYTECODE=1 python3 -O verify.py > actual-optimized.json
diff -u EXPECTED.json actual-optimized.json
sha256sum -c SHA256SUMS
~~~

Expected status: `AFFINE_SECTION_ASYMPTOTICS_VERIFIED`.
Expected standard-output SHA-256:

~~~text
03726608104b953829eed69d33d3b4e5843b6c088769b4adb7fa1407e64b4a8d
~~~

The exact checks cover central specialization, reflection, and the two
pure-ray formulas.  The 80-digit saddle/cumulant calculations and exact
finite sections independently corroborate the displayed constants.  The
uniform asymptotic remainder is a mathematical argument in `PROOF.md`, not
a computer certificate.  See [SOURCES.md](SOURCES.md) for dependencies and
the bounded novelty search.
