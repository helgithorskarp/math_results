# Parametric cube--crosspolytope diagonal sections

For \(\rho>0\), put \(N=n+1\),

\[
H_N=\{x\in\mathbb R^N:\textstyle\sum_i x_i=0\},\qquad
K_{N,\rho}=[-1,1]^N+\rho N B_1^N,
\]

and define the normalized diagonal-section constant

\[
D_n(\rho)=\frac{n!}{\sqrt N\,N^n}|K_{N,\rho}\cap H_N|_n.
\]

The [proof](PROOF.md) establishes a full Poincare expansion for every
fixed \(\rho>0\), locally uniformly in the parameter. If \(r>0\) is the
unique solution of

\[
\rho=\frac1{r(r+1)},
\]

then

\[
D_n(\rho)=\kappa(r)\frac{\beta(r)^n}{\sqrt n}
\left(1+\frac{\gamma_1(r)}n+O_\rho(n^{-2})\right),
\]

where the proof gives expansions to every fixed order and

\[
\beta(r)=\frac{2(r+1)}r\exp\!\left(-\frac r{r+1}\right),
\quad
\kappa(r)=\frac{\beta(r)}{r\sqrt{2\pi v(r)w(r)}}.
\]

Writing \(P=r^3+3r^2+6r+6\), the first relative correction is

\[
\gamma_1(r)=\frac{
30r^{10}+28r^9+150r^8+918r^7-873r^6-9504r^5
-18045r^4-16740r^3-8370r^2-2160r-270}
{60(2r+1)^3P^2}.
\]

At \(\rho=1\), this recovers the sharp simplex projection constant and
its coefficient

\[
-\frac{237}{20}+\frac{284}{15}\frac{\sqrt5-1}{2}.
\]

For other values of \(\rho\), \(D_n(\rho)\) is a natural normalized
section volume; no projection-extremum interpretation is asserted.

## Reproduce

From this directory, using CPython 3.11 or later and its standard library:

~~~sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py > actual.json
diff -u EXPECTED.json actual.json
PYTHONDONTWRITEBYTECODE=1 python3 -O verify.py > actual-optimized.json
diff -u EXPECTED.json actual-optimized.json
sha256sum -c SHA256SUMS
~~~

Expected status: `PARAMETRIC_SECTION_CORRECTION_VERIFIED`.
Expected standard-output SHA-256:

~~~text
4d1dfe365d52c189e088516fba5e3a4269bbd9b992efcdf4ecf688535587f337
~~~

The checker derives the moments and cumulants as rational functions by two
different exact combinatorial algorithms, verifies the displayed formula,
and compares three parameter specializations with exact finite section
volumes. The finite computations corroborate the coefficient algebra; the
uniform asymptotic remainder is proved in `PROOF.md`. Only the diagnostic
finite volumes import the adjacent repository's independently documented
`simplex_envelope_asymptotics/exact_section.py`; the rational-function
derivation itself is self-contained and uses no external package.

See [SOURCES.md](SOURCES.md) for dependencies and the bounded literature
search.
