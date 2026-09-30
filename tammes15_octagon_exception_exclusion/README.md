# Tammes-15: saturated exceptional octagon bridge

**six-tammes-2 — researcher — 2026-09-30.** Author-audited exact certificate;
independent mathematical review pending.

For `1/2<t<3/5`, attach both ears of a contact-triangulated pentagon to
pairs of a disjoint contact-triangulated octagon. If one pair has no old
prescribed octagon neighbor, the packing has at most thirteen points.
A unique degree-15 parameter gives a valid thirteen-point core, but all
286 extension triples certify that it admits no additional unit point.
Combined with the earlier 355-case exclusion, this removes the
old-neighbor hypothesis for strictly improved Tammes-15 packings.

Read [PROOF.md](PROOF.md) for the precise original-label hypotheses,
complete ten-case cover, both orientations, extension argument and
mathematical dependencies. No global Tammes-15 bound or new packing
record is claimed.

Run from the repository root with Python3.11 or later:

```sh
python3 -B tammes15_octagon_exception_exclusion/check.py
python3 -B tammes15_octagon_exception_exclusion/check.py --selftest
python3 -B -O tammes15_octagon_exception_exclusion/check.py --selftest
```

The standard-library checker reads only its compact `certificate.json`,
regenerates the geometry and verifies all exact root and vertex signs.
Compare stdout with [EXPECTED.json](EXPECTED.json). Optional separate
arithmetic regeneration requires SymPy1.14.0:

```sh
python3 -B tammes15_octagon_exception_exclusion/generate_certificate.py
```

Its stdout equals the certificate bytes. No external coordinate table,
solver, ledger, scratch file or network is needed. Run with one BLAS,
OpenMP and solver thread; no parallel job is used. `SHA256SUMS` covers the
source and compact evidence. The fixed root bracket undergoes exactly
160 rational bisections; unresolved signs cause failure. Geometric
reduction and ordinary exact software execution remain unformalized.
