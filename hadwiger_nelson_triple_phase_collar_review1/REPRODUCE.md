# Reproduce the review

Requirements: CPython 3.11 or later; no third-party package, solver, or
network call is used by the independent checker.

From the repository root:

```bash
python3 -B hadwiger_nelson_triple_phase_collar_review1/independent_audit.py \
  > /tmp/hn-triple-phase-independent.json
python3 -B -O hadwiger_nelson_triple_phase_collar_review1/independent_audit.py \
  > /tmp/hn-triple-phase-independent-opt.json
cmp /tmp/hn-triple-phase-independent.json \
    /tmp/hn-triple-phase-independent-opt.json
cmp /tmp/hn-triple-phase-independent.json \
    hadwiger_nelson_triple_phase_collar_review1/EXPECTED.json
(cd hadwiger_nelson_triple_phase_collar_review1 && sha256sum -c SHA256SUMS)
```

For an independent replay of the target package, choose fresh paths and run:

```bash
python3 -B hadwiger_nelson_triple_phase_collar/build.py \
  --out /tmp/hn-triple-phase-build
python3 -B hadwiger_nelson_triple_phase_collar/verify.py \
  --work /tmp/hn-triple-phase-check
python3 -B -O hadwiger_nelson_triple_phase_collar/verify.py \
  --work /tmp/hn-triple-phase-check-opt
cmp /tmp/hn-triple-phase-check/verification.json \
    /tmp/hn-triple-phase-check-opt/verification.json
python3 -B hadwiger_nelson_triple_phase_collar/controls.py
python3 -B -O hadwiger_nelson_triple_phase_collar/controls.py
cmp hadwiger_nelson_triple_phase_collar/certificate.json \
    /tmp/hn-triple-phase-build/certificate.json
(cd hadwiger_nelson_triple_phase_collar && sha256sum -c SHA256SUMS)
```

The expected certificate SHA-256 is
`f37a9fa67101a1aded49098a720aeb972463d46d9849e4e1d924dfc414f7a2ae`.
