# The eta-cubed independent Moser circle is four-chromatic

Let

\[
 \rho=(1+i\sqrt3)/2,\qquad \eta=(5+i\sqrt{11})/6
\]

and let `M` be the standard seven-point Moser spindle in [PROOF.md](PROOF.md).
For every unit complex number `v`, the complete strict plane unit-distance
graph on

\[
 M+\eta^3M+vM
\]

is exactly four-chromatic. The same holds with `eta^-3` in place of `eta^3`.

This closes two one-parameter circles inside the previously open injective
independent three-Moser architecture. A support outside the base field has 343
distinct physical points, so this is directly within the sub-509 construction
budget. It is a restricted-family exclusion, **not** a global lower bound and
not a record construction.

The exact reduction leaves 922 exceptional irreducible contact quadratics
(1,844 physical phase roots). `certificate.json` assigns one of 80 positive
four-colour words to each. The solver-free verifier regenerates the entire
inventory and checks both roots of every quadratic against all 58,653 point
pairs using two separately derived exact metric formulas. The replay audits
108,156,132 unordered point pairs. No floating-point distance test is used.

From this directory, with Python 3.11+ and a C++17 compiler supporting signed
128-bit integers:

```sh
g++ -std=c++17 -O3 -shared -fPIC \
  ../hadwiger_nelson_independent_moser_sum_collisions/geometry.cpp \
  -o /tmp/hn-moser-eta3-circle.so
python3 verify.py --library /tmp/hn-moser-eta3-circle.so \
  > /tmp/hn-moser-eta3-circle.json
cmp expected.json /tmp/hn-moser-eta3-circle.json
sha256sum -c SHA256SUMS
```

Regenerating the positive certificate additionally requires PySAT with
CaDiCaL 1.9.5:

```sh
python3 make_certificate.py --output /tmp/eta3-certificate.json
cmp certificate.json /tmp/eta3-certificate.json
```

The arithmetic, local-colouring lemmas, and exact native metric kernel are
reused from the sibling
[`hadwiger_nelson_independent_moser_sum_collisions`](../hadwiger_nelson_independent_moser_sum_collisions/README.md)
package. [PROOF.md](PROOF.md) gives the complete reduction and trust boundary;
[SOURCE.md](SOURCE.md) records provenance. This theorem is author-side evidence
pending independent review.
