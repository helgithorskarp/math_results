# Bessel crossover at the cube boundary

This directory proves the critical boundary-layer asymptotics for affine
sections of the cube--crosspolytope Minkowski family.  For

\[
A_N(\theta,\rho)=\frac1{\sqrt N}
\left|\left([-1,1]^N+\rho N B_1^N\right)
\cap\{\textstyle\sum_i x_i=\theta N\}\right|_{N-1},
\]

fix $|\theta|<1$, let $a$ solve

\[
\coth a-1/a=\theta,
\]

and put $c=a\coth a=1+a\theta$.  The [proof](PROOF.md) establishes,
locally uniformly for $\lambda\geq0$,

\[
\frac{A_N(\theta,\lambda/N^2)}{A_N(\theta,0)}
=\mathrm I_0\!\left(2\sqrt{\lambda c}\right)
+\frac{\Psi_1(\theta,\lambda)}N+O(N^{-2}),
\]

with an explicit formula for $\Psi_1$ and an expansion to every fixed
order.  Here $\mathrm I_0$ is the modified Bessel function.

The $N^{-2}$ scale is critical.  A tail coordinate has excess budget of
order $N^{-1}$ and $N$ possible labels; summing every finite plus/minus
tail configuration gives the Bessel series.  This is a new regime between
the exact cube boundary and the two-dimensional Gaussian saddle for a fixed
interior radius.

The proof also records the complete geometric boundary:

- $|\theta|<1,\rho=0$ gives a cube section;
- $|\theta|>1,\rho=|\theta|-1$ gives exactly
  $D_n=(|\theta|-1)^n$;
- $\theta=\pm1,\rho=0$ has zero positive-dimensional volume.

## Reproduce

Using CPython 3.11 or later and only its standard library:

~~~sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py > actual.json
diff -u EXPECTED.json actual.json
PYTHONDONTWRITEBYTECODE=1 python3 -O verify.py > actual-optimized.json
diff -u EXPECTED.json actual-optimized.json
sha256sum -c SHA256SUMS
~~~

Expected status: `BOUNDARY_BESSEL_CROSSOVER_VERIFIED`.
Expected standard-output SHA-256:

~~~text
2394dca09e5b930d5a32efe7be1016a5cbc49881ef343dafb24d0c371160d7c2
~~~

The checker evaluates the Bessel/operator formula and the underlying
two-label series independently to 80-digit precision.  It then compares
them with exact rational sections for $N=6,8,10,12,14$ at four parameter
pairs, including a noncentral slice.  The exact engine is the adjacent,
independently documented affine-stratum implementation.  Computation checks
the formulas; the uniform all-orders remainder is proved in `PROOF.md`.

See [SOURCES.md](SOURCES.md) for dependencies and the bounded novelty search.
