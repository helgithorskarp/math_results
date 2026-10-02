# Exact incumbent facial chart

six-tammes-1, researcher. Exact incidence audit of two known Tammes-15 packings.
Both have T11/Q3/P3 and satisfy the nine-triangle/strict-pentagon physical
hypothesis of9562. No new packing, global bound or global occurrence is proved.
Independent researcher review and formalization remain pending.

Run from a checkout with CPython3.11+; standard library only:

```
python3 -B round-two/six-tammes-1/incumbent-facial-chart/check.py
python3 -B round-two/six-tammes-1/incumbent-facial-chart/audit.py
python3 -B round-two/six-tammes-1/incumbent-facial-chart/controls.py
```

`check.py` reconstructs coordinates and regenerates the included compact chart
in memory, without overwriting it. `audit.py` checks the proposed facial polygons
directly by exact inward supports, open hemispheres and outside-point exclusion.
The geometric routes share the attributed peer arithmetic in `inputs/arithmetic.py`.
The other runtime input is the pinned public fourteen-point completion certificate.
The two additional source entries in `inputs/PINS.json` record construction
provenance; they are not downloaded or executed at reproduction time.
See `PROOF.md` for the ordinary geometric bridge and exact source/dependency scope.
