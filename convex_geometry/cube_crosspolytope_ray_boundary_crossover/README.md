# Exact Legendre law at the ray boundary

This directory proves an exact finite-dimensional special-function law,
global Bessel bounds, and an all-orders boundary expansion for affine
sections of the cube--crosspolytope Minkowski family.  Put

\[
A_N(\theta,\rho)=\frac1{\sqrt N}
\left|\left([-1,1]^N+\rho N B_1^N\right)
\cap\{\textstyle\sum_i x_i=\theta N\}\right|_{N-1}.
\]

For $|\theta|>1$, write $m=|\theta|-1$.  The smallest nonempty radius is
$\rho=m$, and

\[
A_N(\theta,m)=\frac{(mN)^{N-1}}{(N-1)!}.
\]

The [proof](PROOF.md) shows that throughout the complete first boundary
segment $m\leq\rho\leq m+2/N$,

\[
\boxed{\frac{A_N(\theta,\rho)}{A_N(\theta,m)}
=P_{N-1}\!\left(2\rho/m-1\right),}
\]

an exact identity in every finite dimension.  Under
$\rho=m(1+z/N^2)$, define

\[
Q_N(z)=P_{N-1}(1+2z/N^2).
\]

Then $Q_N(z)$ increases strictly with $N$ to
$\mathcal F(z)=I_0(2\sqrt z)$ for every $z>0$, with the global bounds

\[
0\leq\mathcal F-Q_N\leq\frac{K\mathcal F}{N}
+\frac{(K^3-K)\mathcal F}{3N^2},
\qquad
Q_N\leq\mathcal F((1-1/N)z),
\]

where $K=z\,d/dz$.  Locally uniformly for $z\geq0$,

\[
Q_N(z)=\mathrm I_0(2\sqrt z)
-\frac{\sqrt z\,\mathrm I_1(2\sqrt z)}N
+\frac{zI_0(2\sqrt z)-(2z+1)\sqrt z I_1(2\sqrt z)}{6N^2}
+O(N^{-3}).
\]

The transformed Legendre equation gives a differential recursion for every
higher coefficient.  Equivalently, for additive thickness
$\rho=m+\lambda/N^2$, the Bessel parameter is $z=\lambda/m$.  This resolves
and structurally classifies the ray-boundary component left open by the
adjacent
[cube-boundary crossover](../cube_crosspolytope_boundary_crossover/README.md).

## Reproduce

Using CPython 3.11 or later and only its standard library:

~~~sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py > actual.json
diff -u EXPECTED.json actual.json
PYTHONDONTWRITEBYTECODE=1 python3 -O verify.py > actual-optimized.json
diff -u EXPECTED.json actual-optimized.json
sha256sum -c SHA256SUMS
~~~

Expected status: `RAY_BOUNDARY_LEGENDRE_VERIFIED`.
Expected standard-output SHA-256:

~~~text
b42806a321eeba572d8630f5cf932292d78f2837f66f2c955c410afdf3063116
~~~

The checker evaluates the simplex integral, hypergeometric coefficients, and
Legendre recurrence by separate exact-rational paths; verifies the Legendre
differential equation coefficientwise; compares against the independent
general affine-stratum engine; and checks monotonicity, both global bounds,
and the first two Bessel corrections to 80-digit precision.

See [SOURCES.md](SOURCES.md) for dependencies and the bounded novelty search.
