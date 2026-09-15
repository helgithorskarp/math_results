The published Snail dual certificate cannot certify an at-most-508-point
construction through the **uniform, full-generator, global Følner-error
test** defined in [PROOF.md](PROOF.md), even after combining cancelling
coefficients. This is a limitation of one proof mechanism. It is not a
four-colouring theorem for arbitrary Snail unions or a lower bound on the
smallest five-chromatic plane graph.

The exact dual gap is `716235/1000000018`. Regrouping identical-subset terms
reduces the non-singleton error coefficient from approximately 5982.37 to
4761.90. The resulting sufficient test requires at least **6,648,512 distinct
isometries**. A strict plane graph on at most 508 points contains at most
8,216 unit edges by the elementary two-common-neighbour bound, and hence at
most **32,864 placements** of any fixed source containing a unit edge.
These conditions are incompatible.

The source mechanism is the geometric fractional bound of
[Dúcz and Varga](https://arxiv.org/abs/2606.28157v1), compiled using the
averaging construction in Theorem 1 of
[Matolcsi, Ruzsa, Varga and Zsámboki](https://arxiv.org/abs/2311.10069v4).
The seed's ordinary chromatic number is three. The geometric dual uses extra
congruence constraints, so its value greater than four is not itself an
ordinary non-four certificate on the seed.

The new calculation checks the actual rational coefficient file, combines
terms at every identical subset, verifies balance in every listed congruence
component, and compares all resulting coefficients against a separate
common-denominator/bit-mask calculation. It does not reproduce the source's
geometric congruences or all dual inequalities. Their validity is an explicit
external theorem dependency, not an independent review claim.

Reproduce with CPython 3.11+ and the standard library. Download the authors'
45.6 MB supplementary archive to scratch storage, outside the repository:

```sh
curl --fail --location https://users.renyi.hu/~akos/ep1070/data/snail.zip --output /tmp/hn-snail-supplement.zip
python3 -B hadwiger_nelson_uniform_folner_certificate_gate/verify.py --supplement /tmp/hn-snail-supplement.zip --check-expected
python3 -O -B hadwiger_nelson_uniform_folner_certificate_gate/verify.py --supplement /tmp/hn-snail-supplement.zip --check-expected
python3 -B hadwiger_nelson_uniform_folner_certificate_gate/controls.py
```

Only two hash-pinned text members are read. The verifier does not unpickle
coordinates, execute the authors' code, extract the archive, or use its large
precomputed matrix. Input provenance and exact trust boundaries are in
[PROVENANCE.md](PROVENANCE.md); compact expected output is in
[EXPECTED.json](EXPECTED.json).

No capped source was admitted and no new geometric enumeration was launched.
This stops the declared proof compiler before repeating the earlier Snail
copy searches. A different proof of a small union might succeed despite this
failed estimate. No record candidate or improvement on Parts's 509-point
construction is claimed.
