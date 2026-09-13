# Reproduction

From the repository root:

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

`build.py` is the deterministic producer.  `verify.py` is a separately
written exact checker using rational arithmetic in the fixed multiquadratic
basis `1,sqrt(3),sqrt(5),sqrt(15)`.  It makes no network or solver calls.
`controls.py` checks that eight named semantic corruptions are rejected and
runs identically with Python assertions disabled.

The machine certificate verifies the exact threshold, polynomial and
isolation; the algebraic monotonicity factor; the six orbit chords; the
interior fixture; a nondegenerate cross triple; the sharp boundary triangle;
and the palette audit.  The universal passage from the cross-triple label to
an order-preserving partial matching, the forest argument, and the extension
over all continuum six-cycle orbits are written-proof obligations in
[PROOF.md](PROOF.md), not claims of formal verification.
