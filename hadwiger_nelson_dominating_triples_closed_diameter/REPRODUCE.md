# Reproduction

Requirements: CPython 3.11 or later, standard library only.  From the
repository root, use fresh temporary directories:

```bash
python3 -B hadwiger_nelson_dominating_triples_closed_diameter/build.py \
  --out /tmp/hn-closed-diameter-build
python3 -B hadwiger_nelson_dominating_triples_closed_diameter/verify.py \
  --work /tmp/hn-closed-diameter-check
python3 -B -O hadwiger_nelson_dominating_triples_closed_diameter/verify.py \
  --work /tmp/hn-closed-diameter-check-opt
cmp /tmp/hn-closed-diameter-check/verification.json \
    /tmp/hn-closed-diameter-check-opt/verification.json
(cd hadwiger_nelson_dominating_triples_closed_diameter && sha256sum -c SHA256SUMS)
```

The producer regenerates `certificate.json` deterministically and fails if
its bytes differ.  The checker imports no producer code.  It reconstructs
the equality-boundary graph with exact `Fraction` arithmetic over
`Q(sqrt(3))`, independently exhausts all binary words and normalized boundary
cases, and checks the sharpness spindle in the basis
`1,sqrt(3),sqrt(11),sqrt(33)`.  Five semantic corruptions must be rejected.

The finite checks audit the boundary and parity ingredients.  The extension
to arbitrary real third-centre positions and all points on three complete
circles is the written continuum argument in `PROOF.md`.

Trust boundary: CPython integer, `Fraction`, JSON and SHA-256 operations; the
linear independence of the displayed squarefree-radical basis; and the
human-checked continuum proof.  There is no floating-point predicate, native
solver, CAS, external data, omitted transcript, or background process.
