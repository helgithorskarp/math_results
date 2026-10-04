# Reproduce the independent all-count triangle audit

Actual six-reviewer-5 / independent mathematical reviewer,2026-10-04.
Read [REVIEW.md](REVIEW.md), [PROOF.md](PROOF.md), [PROVENANCE.md](PROVENANCE.md)
and [DEPENDENCIES.json](DEPENDENCIES.json) for exact scope/trust/credits.
Source alone is not formalization or a proof of generalH/I.

CPython3.11.2, SymPy1.14.0, mpmath1.3.0. Install the two pinned packages
in a separate local environment; generated output must be outside this
flat source directory:

    python3 -m venv /tmp/triangle-audit-env
    /tmp/triangle-audit-env/bin/python -m pip install -r requirements.txt
    /tmp/triangle-audit-env/bin/python -B verify.py --out /tmp/triangle-audit-validation.json

Expected: complete:true,18 whole generated-record positives,28 semantic
rejections, plus3 no-pole/scalar positives and two no-pole semantic
rejections. The source manifest/census is checked before code imports.
The fresh72883-byte symbolic certificate must match in every producer
mode; the2931-byte entire mathematical record must match in every mode.
No author native/certificate/EXPECTED or external old seed is an input.

To check only the complete high-q coefficient certificate with the
standard library, no CAS installation:

    python3 -B five_check.py --input FRESH-FIVE.json --out /tmp/five-cap.json
    python3 -B bounds.py --input FRESH-FIVE.json --out /tmp/five-bounds.json

The first checks every physical entry and ordered elimination identity;
the second pays all80 intermediate denominators and exact scalar/range
constants. Neither finite q/h/l samples nor hashes establish positivity.
The original geometry and continuum/rank bridges are in the ordinary proof.

All mathematical children have the fixed45-second wall guard, run
serially, native/BLAS/OpenMP threads1, within the existing1CPU/2GiBscope.
No resource-limited work is mathematical nonexistence. The largest
compact public file is72883B; no corpora, matrices, keys or ledgers
are required/published. Public source replays only public files.
