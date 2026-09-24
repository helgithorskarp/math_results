# Global ray-chamber classification

This directory gives an exact, finite formula for every diagonal affine
section of the cube--crosspolytope Minkowski family on the ray side
$|\theta|>1$.

Let $m=|\theta|-1$, $a=mN$, and $\delta=N(\rho-m)$.  The section is empty for
$\rho<m$.  For every $\rho\geq m$, the [proof](PROOF.md) establishes

\[
A_N(\theta,\rho)=
\sum_{r=0}^{N-1}\binom Nr\mathcal T^rH_{N-r}(a,\delta),
\]

where

\[
H_d(A,s)=\frac{A^{d-1}}{(d-1)!}P_{d-1}(1+2s/A)
\]

for $s\geq0$, and $\mathcal T$ is an explicit one-dimensional signed
integral operator recording “physical negative tail minus fictitious inactive
tail.”  On $2R\leq\delta\leq2(R+1)$ only the terms $r\leq R$ occur.

The operator has a finite rational coefficient recurrence, so every chamber
is an explicit polynomial of degree $N-1$.  The knots are exactly
$\delta=2,4,\ldots,2(N-1)$.  At $delta=2r$, the section is $C^{r-1}$ but not
$C^r$, with a closed derivative-jump formula.  Thus the result classifies all
successive mixed-tail chambers and their exact regularity, extending the
adjacent [first Legendre segment](../cube_crosspolytope_ray_boundary_crossover/PROOF.md).

## Reproduce

Using CPython 3.11 or later and only its standard library:

~~~sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py > actual.json
diff -u EXPECTED.json actual.json
PYTHONDONTWRITEBYTECODE=1 python3 -O verify.py > actual-optimized.json
diff -u EXPECTED.json actual-optimized.json
sha256sum -c SHA256SUMS
~~~

Expected status: `GLOBAL_RAY_CHAMBER_CLASSIFICATION_VERIFIED`.
Expected standard-output SHA-256:

~~~text
72b5251826d8e47ee8017b91a0ebb8d452b391433c6ebad2bd2e958b3322d608
~~~

The checker performs exact rational comparisons with the independent general
affine-stratum engine across every chamber in dimensions two through eight.
It separately checks the Legendre kernels, reflection, coefficient
homogeneity, chamber activation, and the full derivative-jump classification
through dimension twenty.

See [SOURCES.md](SOURCES.md) for dependencies and the bounded novelty search.
