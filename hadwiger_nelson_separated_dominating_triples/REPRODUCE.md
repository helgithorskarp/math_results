# Reproduction

Requirements: CPython 3.11 or later, standard library only.  From the
repository root, choose fresh temporary directories:

```bash
python3 -B hadwiger_nelson_separated_dominating_triples/build.py \
  --out /tmp/hn-separated-build
python3 -B hadwiger_nelson_separated_dominating_triples/verify.py \
  --work /tmp/hn-separated-check
python3 -B -O hadwiger_nelson_separated_dominating_triples/verify.py \
  --work /tmp/hn-separated-check-opt
cmp /tmp/hn-separated-check/verification.json \
    /tmp/hn-separated-check-opt/verification.json
(cd hadwiger_nelson_separated_dominating_triples && sha256sum -c SHA256SUMS)
```

`build.py` deterministically regenerates the committed certificate and fails
if its bytes differ.  `verify.py` imports no producer code.  It reconstructs
the sixth-root orbit in exact `Fraction` arithmetic, independently enumerates
all normalized boundary choices, and checks the sharpness graph in the basis
`1,sqrt(3),sqrt(11),sqrt(33)`.  It also rejects five deliberately malformed
certificates.

The finite check validates the explicit parity ingredients and sharpness
witness.  The passage from them to arbitrary real centre positions and all
points of three complete circles is the written proof in `PROOF.md`.

Trust boundary: CPython integer, `Fraction`, JSON and SHA-256 operations; the
linear independence of the displayed squarefree-radical basis; and the
human-checked continuum argument.  There is no floating-point predicate,
SAT/CAS call, external input, omitted trace, or background process.
