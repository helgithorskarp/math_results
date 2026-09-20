# Certificate provenance

The six committed corner files are self-contained proof inputs: the C++
verifier reconstructs all orders from first principles and checks every
listed pair count.  Their upstream provenance is recorded here so the
transformation can also be reproduced.

## Upstream files

The completion maps and degree-six profiles come from commit
`362de8a541d4a37eecadbb1068778f8b411dd6bd` of
[`njallskarp/math_source_code_open`](https://github.com/njallskarp/math_source_code_open/tree/362de8a541d4a37eecadbb1068778f8b411dd6bd/stable_transitivity_mu8):

```text
ec71ca73e306e5917b9f3a28d99e73c3361716ce195f557584f6f323e1f3fb79  g8_maps.txt
2cddde8ae922758a0475fca44bc50c9200eb1284034c42ced0192cdda37697ff  m6_profiles.txt
```

The degree-two through degree-five residue profiles come from commit
`614f819e56ae9e102c0d8ef7985be1850a4559d8` of the same directory:

```text
2424a035c3715d4b4c1379aee373403baf29c212ae5a36cda12a95d6d529d00b  residue_profiles.txt
```

The degree-one profiles derive from
[`cert_n8_m2.txt`](../stable_tournaments_order8/cert_n8_m2.txt), commit
`cb65c26f6df858a58f1912b1ccfc49adba83ac6f`, SHA-256
`ea0a4dd142f2a720b9f17a20e4de8b4a05dcfb512b645be80d12ca4532c30db6`.

## Deterministic transformation

After checking out the cited external source, run from this directory:

```bash
OUT=/tmp/g8-corners-regenerated
python3 derive_corners.py \
  /path/to/math_source_code_open/stable_transitivity_mu8 \
  ../stable_tournaments_order8/cert_n8_m2.txt "$OUT"

for d in 1 2 3 4 5 6; do
  cmp "corners_d${d}.txt" "$OUT/corners_d${d}.txt"
done
```

The recorded regeneration was byte-identical for all six files.  This step
is optional: `verify_boxes.cpp` treats the resulting order indices as
untrusted data and checks the theorem-relevant margins directly.
