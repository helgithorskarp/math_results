# Five-active-weight two-level missing walls

This directory proves two results for ray-side sections of the
cube--crosspolytope Minkowski family.

First, it gives an arbitrary-\(q\) closed formula for the lowest hinge
coefficient when two structural rows for weights \(1^p a^r\) resonate. It
implies both the residual-multiplicity condition

\[
p-k=r-j
\]

and a new parity obstruction

\[
r-\ell\equiv1\pmod2.
\]

Second, it applies these obstructions to classify every positive candidate
wall for five active weights taking at most two distinct values. Exactly six
isolated wall orbits disappear:

- three on \(1^4a\), all at wall \(s=6\);
- two on \(1^3a^2\), at wall \(s=2(a+2)\);
- one on \(1^2a^3\), at wall \(s=2(2a+1)\).

There are none on \(1a^4\) or the diagonal. The six parameters are the
unique unit-interval roots of the six explicit irreducible polynomials in
[PROOF.md](PROOF.md).

## Reproduce

The independent checker needs only CPython 3.11 or later:

~~~sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py > actual-verification.json
diff -u EXPECTED_VERIFICATION.json actual-verification.json
~~~

The symbolic derivation pins SymPy 1.13.3:

~~~sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python derive.py > actual-derivation.json
diff -u EXPECTED_DERIVATION.json actual-derivation.json
sha256sum -c SHA256SUMS
~~~

Expected statuses are Q5_TWO_LEVEL_MISSING_WALLS_VERIFIED and
Q5_TWO_LEVEL_MISSING_WALLS_DERIVED.

The canonical output SHA-256 values are respectively
`edaf79a89ea11f7bd3e8918cfd5d6467842848f83952382584d34e887afb1d9e`
and
`4835145bd0b030ef73a9737ef42b66643ce30519e8c8879eb91419e29353954b`.
