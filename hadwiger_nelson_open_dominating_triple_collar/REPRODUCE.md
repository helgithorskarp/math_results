# Reproduction

Requirements: CPython 3.11 or later, standard library only.  From the
repository root, use fresh output directories:

```bash
python3 -B hadwiger_nelson_open_dominating_triple_collar/build.py \
  --out /tmp/hn-open-collar-build
python3 -B hadwiger_nelson_open_dominating_triple_collar/verify.py \
  --work /tmp/hn-open-collar-check
python3 -B -O hadwiger_nelson_open_dominating_triple_collar/verify.py \
  --work /tmp/hn-open-collar-check-opt
cmp /tmp/hn-open-collar-check/verification.json \
    /tmp/hn-open-collar-check-opt/verification.json
python3 -B hadwiger_nelson_open_dominating_triple_collar/controls.py
python3 -B -O hadwiger_nelson_open_dominating_triple_collar/controls.py
cmp hadwiger_nelson_open_dominating_triple_collar/certificate.json \
    /tmp/hn-open-collar-build/certificate.json
(cd hadwiger_nelson_open_dominating_triple_collar && sha256sum -c SHA256SUMS)
```

The build and work directories must not already exist.  Normal and optimized
verification reports are byte-identical.  The producer and checker share no
code.  The checker derives the threshold identities, 60-degree chord table,
three exact fixture distances, strict interior inequalities, cap values, and
palette separation.  Six independent mutations must be rejected.

Trust boundary: CPython integer, `Fraction`, JSON and SHA-256 semantics; the
linear independence of the displayed multiquadratic basis; and inspection of
the elementary continuum proof in `PROOF.md`.  There is no floating-point
predicate, random choice, solver, CAS, native extension, external input,
large omitted artifact, or background process.
