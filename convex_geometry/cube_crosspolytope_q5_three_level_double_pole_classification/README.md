# Complete double-pole missing-wall classification in active dimension five

This directory classifies every double-pole missing wall for ordered
three-level active weights

\[
                  (1,1,a,a,b),\qquad 0<b<a<1,quad B>0.
\]

There are exactly three.  One is the previously known wall at \(2b\); two are
the walls at \(2a\) and \(2(2a+b)\) found by the isolated classification.
The subsequent non-isolated analysis proves that no additional simple-pole
row can complete a cancellation.  Thus the list is complete without an
isolation hypothesis.  All three families are specified by exact algebraic
numbers, and no numerical approximation is used in either proof.

The proof reduces the 36 possible unit/\(a\)-supplier tail pairs to eight by
sign and boundary positivity, factors every leading cancellation equation,
and applies exact Sturm and sign certificates to five univariate eliminants.
For each survivor it also checks all 33 structural rows, proving that exactly
the intended two double-pole rows reach the wall.

See [`PROOF.md`](PROOF.md) for the three-family isolated classification and
[`NONISOLATED_PROOF.md`](NONISOLATED_PROOF.md) for the strengthening to all
double-pole walls.

## Reproduce

The independent verifier needs only CPython 3.11 or later:

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

Expected statuses are
`Q5_THREE_LEVEL_DOUBLE_POLE_CLASSIFICATION_VERIFIED` and
`Q5_THREE_LEVEL_DOUBLE_POLE_CLASSIFICATION_DERIVED`.

The non-isolated exclusion uses a compact 59-factor certificate:

~~~sh
PYTHONDONTWRITEBYTECODE=1 python3 verify_nonisolated.py > actual-nonisolated.json
diff -u EXPECTED_NONISOLATED.json actual-nonisolated.json
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python derive_nonisolated.py \
  > actual-nonisolated-derivation.json
diff -u EXPECTED_NONISOLATED_DERIVATION.json actual-nonisolated-derivation.json
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python derive_nonisolated.py --certificate \
  > actual-collision-certificate.json
diff -u COLLISION_CERTIFICATE.json actual-collision-certificate.json
~~~

Its expected verifier status is
`Q5_NONISOLATED_DOUBLE_POLE_WALLS_EXCLUSION_VERIFIED`.
