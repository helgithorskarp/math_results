# Durable exact interface for team-hn-3

The entire h4171 profile `(1,1,2,2,2)` is closed: **54 pencils, 6,912 quintets,
zero complex affine concurrences**. The rule is monotone: each quintet is
forbidden even with additional active curves. No assumption about injectivity,
radius, unit circle or reflection axes is needed for this new exclusion.

Regenerate every forbidden quintet, using the original h4105 curve IDs:

```sh
python3 -B hadwiger_nelson_radix_two_coordinate_pencils/verify.py --check-expected --export-interface /tmp/hn-two-coordinate-quintets.json
```

The path must not exist. The canonical digest of the sorted quintet list is
`6e98cc7cc4a83774b9826b8989518ebdde3982298e7fb08801cb9b3777226e55`.
The raw list is regenerated locally, not stored in the repository.

Two distinct normal directions determine one affine pencil. Exactly **192**
previously exact-five-compatible canonical pairs determine a closed pencil;
they now require at least six active curves. Their named stabilizer histogram
is `1:164, 2:28`, and their conservative orbit allowance is 3,860. The updated
frontier is:

| Mode | Pair systems | Possible non-four orbit allowance |
|---|---:|---:|
| Exact-five compatible | 128,424 | 3,763,324 |
| Requires at least six | 2,932 | 83,380 |
| Whole frontier | 131,356 | 3,846,704 |

The surviving exact-five pattern/lift counts are **5,328 / 132,225,984**.
No complete global pair is removed. The 192 pairs must not be deleted from a
six-or-more search merely because their unique five-pencil is impossible.

Consume the newest HN3 explicit mode/stabilizer interface:

```sh
python3 -B hadwiger_nelson_radix_five_active_orbits/produce.py --out /tmp/hn-source-orbit-certificate.json --export-interface /tmp/hn-source-orbit-interface.json
python3 -B hadwiger_nelson_radix_two_coordinate_pencils/frontier_effect.py --interface /tmp/hn-source-orbit-interface.json --check-expected --export-moves /tmp/hn-two-coordinate-pair-moves.json
```

The source interface file SHA-256 is
`be36cc09da60c4bba4c260f42c12b21b88c9dea4553a1ae0214870c0284b047e`.
The canonical digest of the moved rows is
`8eb2ca8fbd0342f6939d57cf60d3f32bedda21ac2e6cf8dc6079d89a3afbb73a`.
Rows retain HN3's `[curve_a,curve_b,stabilizer_mask,2kl_bound,orbit_allowance]`
format. Canonical pairs must still be considered over the whole parameter
plane, without a simultaneous chamber restriction.

HN3 can incorporate the new forbidden quintets and exact-five mode refinement
in complementary algebraic viability work. HN2 retains physical realization
and chromatic/candidate ownership. This pass ends at the complete named-subset
decision; no second support profile or active-count ladder is begun.
