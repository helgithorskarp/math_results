# Reproduction

Requirements: CPython 3.11 or later, standard library only. From the
repository root, run:

```sh
python3 -B hadwiger_nelson_open_dominating_triple_collar_review1/independent_audit.py \
  --check-expected
python3 -O -B hadwiger_nelson_open_dominating_triple_collar_review1/independent_audit.py \
  --check-expected
(cd hadwiger_nelson_open_dominating_triple_collar_review1 && sha256sum -c SHA256SUMS)
```

The checker imports no target module and does not read the target
certificate. It independently works in exact multiquadratic bases, derives
the threshold polynomial and inequalities, reconstructs the six orbit
chords and the interior fixture, and checks two strict-boundary controls.

The separately reproduced target commands are:

```sh
collar_tmp=$(mktemp -d /tmp/hn-open-collar-target.XXXXXX)
python3 -B hadwiger_nelson_open_dominating_triple_collar/build.py \
  --out "$collar_tmp/build"
python3 -B hadwiger_nelson_open_dominating_triple_collar/verify.py \
  --work "$collar_tmp/check"
python3 -O -B hadwiger_nelson_open_dominating_triple_collar/verify.py \
  --work "$collar_tmp/check-opt"
cmp "$collar_tmp/check/verification.json" "$collar_tmp/check-opt/verification.json"
python3 -B hadwiger_nelson_open_dominating_triple_collar/controls.py
cmp hadwiger_nelson_open_dominating_triple_collar/certificate.json \
  "$collar_tmp/build/certificate.json"
(cd hadwiger_nelson_open_dominating_triple_collar && sha256sum -c SHA256SUMS)
```

The finite checks audit exact algebra and the strict boundaries. The
universal statement for arbitrary real centre positions is the elementary
continuum argument reviewed in `README.md`, not a finite sampling claim.
The trust boundary is CPython exact integer/`Fraction` arithmetic, SHA-256,
inspection of the exhaustive loops, and the written Euclidean proof.
