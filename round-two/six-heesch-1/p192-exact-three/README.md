# Second 17-cell seed: exact unrestricted Heesch three

**six-heesch-1, researcher.** The primary17-cell seed at zero-based index192
has Hc=Hh=3 under all Euclidean rigid motions and cannot tile the plane.
This matches the author's reported grid value; no new shape or record.
The complete author proof is unformalized, with independent review pending.

[proof.md](proof.md) gives the motion/depth arguments and primary attribution.
[input.json](input.json) contains a checked43-copy three-disc witness.
The fractional first-support census has8 supported types and no reciprocal
survivor, forcing interior translations to be integral. A209-contact corner
obstruction then reduces all fourth-corona possibilities to310 first
surrounds,276 second surrounds and44 failed third covers.

Run from repository root, with standard-library CPython3.11+:

```
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python3 round-two/six-heesch-1/p192-exact-three/check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python3 -O round-two/six-heesch-1/p192-exact-three/check.py
```

Both outputs equal [expected.json](expected.json), including8 rejected
controls. The reader checks406 RUP additions,600 corner exclusions and
independently reconstructs complete admitted inventories with lazy conflicts
and a different branching order. No solver package is required. Five shared
files in [finite-contact-types](../finite-contact-types/README.md) are
byte-pinned. `--progress` emits intermediate verification progress.

Final normal and optimized checks took20.054 and19.492 seconds, with peak
child78,044KiB. Identical output SHA256:
`f8f335ec1a3d77aa4d96dfed62da76caf8a21fdd205be834341040073b0e67bb`.

Unrestricted finite-five remains unresolved. This certificate closes the
second17-cell seed's fractional and alternative-corona branches; it does not
exclude other polyominoes or modified prototypes.
