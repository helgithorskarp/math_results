# Handoff to HN2

The exact-five branch now has the following root-accounting boundary:

```text
global retained pair representatives                 131,356
exact-five-compatible representatives                128,616
  stabilizer 1                                       126,660
  stabilizer 2                                         1,956
exact-five old total-degree allowance              7,585,472
exact-five product-surface allowance               3,792,736
exact-five non-four D3-orbit allowance              3,767,184

representatives requiring at least six                 2,740
at-least-six non-four D3-orbit allowance               79,520
reconciled whole-frontier allowance                 3,846,704
```

For exact root work, generate the explicit table:

```sh
python3 -B hadwiger_nelson_radix_five_active_orbits/produce.py \
  --out /tmp/hn-five-active-orbits.json \
  --export-interface /tmp/hn-five-active-orbit-interface.json
```

The interface row format is

```text
[curve_a, curve_b, stabilizer_mask, 2kl_bound, orbit_allowance]
```

with mask bits ordered as `1,R,R^2,C,RC,R^2C`. Its file SHA-256 must be

```text
be36cc09da60c4bba4c260f42c12b21b88c9dea4553a1ae0214870c0284b047e
```

Use `pair_modes.exact_five_compatible` for the exact-five root frontier. The
1,956 order-two rows identify precisely where a named reflection pairs
non-four roots; all other exact-five rows have trivial residual pair
stabilizer. The h4171 extension witnesses certify only combinatorial survival,
not concurrence or physical chromaticity.

Do not impose a chamber restriction on the table: its pairs are already
global `D3` representatives. The 2,740 other rows are not excluded globally;
they remain part of the six-or-more-active frontier. This package performs no
physical/chromatic candidate search.
