# First correction for sharp simplex-envelope constants

Let \(C_n\) be the sharp unconditional projection ratio when the positive
image is an \(n\)-simplex, as defined and evaluated to leading order in the
preceding
[simplex-envelope package](../simplex_envelope_asymptotics/README.md).
This package proves the first relative correction

\[
C_n=\kappa\frac{\beta^n}{\sqrt n}
\left(1+\frac{\gamma}{n}+o(n^{-1})\right),
\]

where

\[
r=\frac{\sqrt5-1}{2},\qquad
\beta=\frac{2e^{r-1}}{r^2},\qquad
\kappa=\frac{\beta}{r\sqrt{2\pi vw}},
\]

\[
v=\frac{13+8r}{3},\qquad w=1+2r,qquad
\boxed{\gamma=-\frac{237}{20}+\frac{284}{15}r}.
\]

Numerically, \(\gamma\approx-0.14855647966865754\). The result strengthens
the preceding asymptotic equivalence; it does not change the geometric
optimization theorem or address arbitrary positive-image shapes.

The [proof](PROOF.md) derives a two-dimensional Edgeworth expansion despite
the singular one-step tilted law, integrates it against the exponential
slack, and tracks the Stirling and \(N=n+1\) corrections. The
[checker](verify.py) recomputes all required moments and cumulants exactly in
\(\mathbb Q(r)\), verifies the simplified coefficient, and compares the
prediction with the predecessor's exact rational values through \(C_{12}\).
The finite comparison is corroboration, not a proof of the asymptotic
remainder.

## Reproduce

From this directory, with CPython 3.11 or later and its standard library:

~~~sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py > actual.json
diff -u EXPECTED.json actual.json
PYTHONDONTWRITEBYTECODE=1 python3 -O verify.py > actual-optimized.json
diff -u EXPECTED.json actual-optimized.json
sha256sum -c SHA256SUMS
~~~

Expected status: `EXACT_EDGEWORTH_COEFFICIENT_VERIFIED`. Expected standard
output SHA-256:

~~~text
bd436fee9f809a028270321fbbad0773da945d74d9d129fac358a8745c3ed605
~~~

The checker imports only the predecessor's exact rational section formula
from the adjacent repository directory. It uses no solver, random input,
floating geometry, external dataset, or hidden certificate. Decimal values
in the output are diagnostics computed after the exact identities have
passed.

See [SOURCES.md](SOURCES.md) for dependency alignment, literature scope, and
the bounded novelty search.
