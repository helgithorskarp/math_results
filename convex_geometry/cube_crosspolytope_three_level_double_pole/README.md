# A minimal three-level double-pole missing wall

This directory gives an exact counterexample to extending two-level
higher-pole rigidity to three distinct active weights.

Let \(\alpha\) be the unique root in
\((127/200,637/1000)\) of

\[
P(x)=x^{10}-3x^9+4x^8-4x^7+5x^6-7x^5
     +5x^4-4x^3+4x^2-3x+1,
\]

and put

\[
\beta=\frac{\alpha(1-\alpha^6)}{1+\alpha^7},
\qquad
B=\frac{2\alpha\beta}{1-\alpha}.
\]

For the active weights \((1,1,\alpha,\alpha,\beta)\), the candidate wall
\(s=2\beta\) receives exactly two structural rows.  Both arise from poles
of multiplicity two, and their coefficients of \(H_3\) and \(H_4\) cancel.
Thus the whole wall disappears.  Numerically,

\[
(\alpha,\beta,B)
=(0.635988208014771,\ 0.569915848324062,\ 1.991472623005279).
\]

This phenomenon is dimension-minimal: two different double-pole suppliers
and a third distinct weight require at least \(2+2+1=5\) active
coordinates.  See [PROOF.md](PROOF.md) for the theorem and exact derivation.

## Reproduce

The independent checker uses only CPython 3.11 or later:

~~~sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py > actual-verification.json
diff -u EXPECTED_VERIFICATION.json actual-verification.json
~~~

The full symbolic reconstruction pins SymPy 1.13.3:

~~~sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python derive.py > actual-derivation.json
diff -u EXPECTED_DERIVATION.json actual-derivation.json
sha256sum -c SHA256SUMS
~~~

Expected statuses are `THREE_LEVEL_DOUBLE_POLE_MISSING_WALL_VERIFIED` and
`THREE_LEVEL_DOUBLE_POLE_MISSING_WALL_DERIVED`.
