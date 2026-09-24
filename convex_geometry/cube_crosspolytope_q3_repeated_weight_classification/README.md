# Repeated-weight completion of the q=3 missing-wall classification

This directory removes the pairwise-distinct hypothesis from the published
three-active-weight classification.  Up to permutation, it proves that the
only new missing positive candidate wall is

\[
(1,1,a),\qquad a^4+a-1=0,quad 0<a<1,qquad
B=\frac{2a}{1-a},qquad s=2.
\]

There are no missing positive walls on the other repeated stratum
((1,a,a)) or at the diagonal point ((1,1,1)).  Combined with the distinct
classification cited in [SOURCES.md](SOURCES.md), this completes the result
for every triple of active weights.

See [PROOF.md](PROOF.md) for the exact multiple-pole hinge tables and proof.

## Reproduce

The independent verifier uses CPython 3.11 or later and only the standard
library:

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

Expected statuses are `Q3_REPEATED_WEIGHT_CLASSIFICATION_VERIFIED` and
`Q3_REPEATED_WEIGHT_CLASSIFICATION_DERIVED`.  The canonical output hashes are
respectively
`e3569477bf49d1e7ebcab74d176ba88b9cb97457496de613d4bdb3671636ddb8` and
`103c98afd93d3d37f7f47ec5aa5c353f2854b44e5b51b9bdbe2c3e4e82552707`.

The independent checker rebuilds all multiple-pole terms over exact rational
arithmetic, verifies the quartic root certificate, and compares the formula
with exact polygon sections defined by the original 27 halfspaces.  SymPy is
used only by the separate symbolic derivation.
