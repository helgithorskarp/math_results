# Tammes-15: three-T/two-T degree fives

Actual author **six-tammes-1**, role **researcher**, 2026-10-02.

[PROOF.md](PROOF.md) excludes the row
`(r,a,b,f0,f1,f2,O)=(2,3,0,0,1,1,8)` on **1/2<c<3/5** in the complete
connected fifteen-point minor-geodesic contact-map class, degrees3/4/5,
simple strictly convex hemispherical T/Q faces,9Q/8T.
Independent mathematical review/formalization remain pending; a global
Tammes-15 bound or optimizer occurrence is not established.

From this directory, use CPython3.12.14/stdlib. Set native OMP/BLAS thread
counts to1 and run sequentially, with55-second per-command guards:

```sh
timeout 55s python check.py
timeout 55s python -O check.py
timeout 55s python audit.py
timeout 55s python -O audit.py
timeout 55s python controls.py
timeout 55s python -O controls.py
```

Each command compares the entire regenerated output with
[EXPECTED.json](EXPECTED.json) or [CONTROLS_EXPECTED.json](CONTROLS_EXPECTED.json).
All21572 admission decisions, branch selections and twelve terminal
obstruction witnesses match the separate same-author bit/dart audit.
[VALIDATION.json](VALIDATION.json) records all six complete runs.
A timeout or incomplete cover gives no exclusion.

Both fives' Q corners are below phi: the other five remains an allowed
Q opposite in the noncontact case. F's QQ cap is1, D's2. The cover retains
both of D's supplier cases. Twelve closed incidence maps survive the
combinatorial necessities. Each contains an ordinary-ordinary QQ edge,
excluded by the proved adjacent-angle budget for c>1/2.
They are retained and checked explicitly.

No solver, coordinates, network or external certificate is a runtime
proof input. Compact expected outputs regenerate all cases; private
pilots and bulk traces are omitted. [DEPENDENCIES.json](DEPENDENCIES.json)
records credited geometry and the optional catalogue deletion with all
prior hypotheses preserved. [MANIFEST.json](MANIFEST.json) hashes source
and compact evidence files.
