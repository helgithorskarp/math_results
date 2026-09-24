# Exact universality at the ray boundary

This directory proves an exact finite-dimensional scaling law and its Bessel
limit for affine sections of the cube--crosspolytope Minkowski family.  Put

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

The [proof](PROOF.md) shows that, whenever $z\geq0$ and $mz/N<2$,

\[
\boxed{\frac{A_N(\theta,m(1+z/N^2))}{A_N(\theta,m)}=Q_N(z),}
\]

where the explicit polynomial $Q_N$ is independent of both $m$ and the sign
of $\theta$.  Thus the scaling collapse is exact, not merely asymptotic.
Moreover, locally uniformly for $z\geq0$,

\[
Q_N(z)=\mathrm I_0(2\sqrt z)
-\frac{\sqrt z\,\mathrm I_1(2\sqrt z)}N+O(N^{-2}),
\]

and there is an expansion to every fixed order.  Equivalently, for additive
thickness $\rho=m+\lambda/N^2$, the Bessel parameter is $z=\lambda/m$.
This resolves the ray-boundary component left open by the adjacent
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

Expected status: `RAY_BOUNDARY_UNIVERSALITY_VERIFIED`.
Expected standard-output SHA-256:

~~~text
81303586999ab3c83e2ba256337c503dd21b7dc073dfff3b299f896be89882bb
~~~

The checker evaluates $Q_N$ by exact rational arithmetic, compares it with
the independent general affine-stratum engine at twenty parameter triples,
tests offset and reflection universality, and verifies the Bessel leading
term and first correction independently to 80-digit precision.

See [SOURCES.md](SOURCES.md) for dependencies and the bounded novelty search.
