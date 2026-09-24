# Complete collision closure for two-level missing walls

This directory removes the final nongeneric exception from the two-level
missing-wall theorem for cube--crosspolytope ray sections.

For weights \(1^p a^r\), every same-family collision occurs at a rational
parameter \(a=s/t\).  Unit-row lowest degrees are spaced by \(s\), while
moving-row lowest degrees are spaced by \(t\).  The established two-jet
rigidity therefore settles every collision except a reciprocal parameter
\(a=1/t\) where a second unit row enters the next degree.  If \(t\) is even,
that row reinforces the nonzero two-jet remainder.  If \(t\) is odd, an odd
prime divisor of \(t\) prevents even the leading coefficients from
cancelling.

Consequently no multirow wall disappears.  Together with the earlier
isolated-wall theorem, [PROOF.md](PROOF.md) gives an exact
arbitrary-dimensional criterion for every two-level missing wall, including
all rational subset-sum collisions.

## Reproduce

The independent checker needs only CPython 3.11 or later:

~~~sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py > actual-verification.json
diff -u EXPECTED_VERIFICATION.json actual-verification.json
~~~

The symbolic reconstruction pins SymPy 1.13.3:

~~~sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python derive.py > actual-derivation.json
diff -u EXPECTED_DERIVATION.json actual-derivation.json
sha256sum -c SHA256SUMS
~~~

Expected statuses are `TWO_LEVEL_COLLISION_CLOSURE_VERIFIED` and
`TWO_LEVEL_COLLISION_CLOSURE_DERIVED`.

The canonical output SHA-256 values are respectively
`349bd4dd966f8454e617bfe3fb2cb5aa7e6abddc340a6884128b3dd4e0a1b7e7`
and
`13310db1b13b32a02184e1b34dd3dafd3602f518db93540ede7b3d5355be8f34`.
