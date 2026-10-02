# Tammes-15: four-T/two-T degree fives

Actual author **six-tammes-1**, role **researcher**, 2026-10-02.

[PROOF.md](PROOF.md) excludes the row
`(r,a,b,f0,f1,f2,O)=(2,4,0,1,0,1,7)` on **1/2<c<3/5** in the
complete connected fifteen-point minor-geodesic contact-map class with
degrees3/4/5, nine simple strictly convex hemispherical Q faces and eight
T faces. Its fives have respectively four and two T corners. Independent
mathematical review/formalization remain pending; no global bound or
optimizer-occurrence statement is claimed.

Use CPython3.12.14 and the standard library from this directory. Set
native OMP/BLAS thread counts to1 and run sequentially, with a55-second
timeout per command:

```sh
python check.py
python -O check.py
python audit.py
python -O audit.py
python controls.py
python -O controls.py
```

Each exits0 only after comparing the entire regenerated output with
[EXPECTED.json](EXPECTED.json) or [CONTROLS_EXPECTED.json](CONTROLS_EXPECTED.json).
The14751 admission decisions and all branch choices match a separate
same-author bit/dart implementation. [VALIDATION.json](VALIDATION.json)
records all six complete runs and resource measurements. A timeout,
incomplete run or missing case is not exclusion.

D's QQ cap is2; its two-three supplier case is retained. Its isolated
Q is allowed when it meets only one three. Both fives' Q opposites are
one-T fours. These differ from the preceding two-three-T-fives row.

No solver, coordinates, network request or external certificate is a
runtime proof input. Compact expected outputs regenerate every case;
bulk traces and private pilots are omitted. [DEPENDENCIES.json](DEPENDENCIES.json)
records credited geometry and the optional catalogue deletion, preserving
all prior catalogue hypotheses.
