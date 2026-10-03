# RID: a proper touching closed-fit segment

six-rupert-3, researcher; 2026-10-03. [PROOF.md](PROOF.md) gives the
complete ordinary fixed-source lemma. Author checked, unformalized,
independently unreviewed; global Rupert status remains open.

For the explicit 36-degree rotation with Cayley vector
`((4-3*phi)/5,0,(3-phi)/5)`, all closed fits with receiving vector in
`conv((0,0,1),(s,0,1),(s,s*s,1))`, `s=2-phi`, original planar translation,
and scale at least one occur exactly on
`r=(x,0,1), 2*phi-3 <= x <= 2-phi`, at unit scale and zero translation.
The moving shadow is properly contained but touches the boundary.
This is not a strict Rupert passage or a global non-Rupert proof.

Run from the repository root with Python 3.11+ and its standard library:

```sh
python3 round-two/six-rupert-3/rid_midpoint_closed_family/verify.py
python3 -O round-two/six-rupert-3/rid_midpoint_closed_family/verify.py
```

Both commands reconstruct every mathematical check and compare with
[EXPECTED.json](EXPECTED.json), including the SHA256 of the entire
mathematical record:
`fee883551a76bf522410f06c62d6dbb19a27ec6cc6c5e87d8d3c9f05827beec5`.
There are 4800 exact support/containment controls, plus actual-body
rotation, full-hull, tightness and translation checks. Every gate remains
active under `-O`. See [VALIDATION.json](VALIDATION.json) for fresh
relocated author replays and [DEPENDENCIES.json](DEPENDENCIES.json) for
credited model/arithmetic inputs.

`--output PATH` optionally writes the full regenerated record to a fresh
local file. No solver, numerical library, source forest, private cache,
checkpoint or generated coefficient record is a replay input. The copied
elementary [field.py](field.py) is pinned before import. The trust boundary
is ordinary real convexity and Cayley algebra with exact rational
arithmetic over the ordered field Q(phi), not independent review or formal
verification. Hashes provide provenance; the exact signs and ordinary
continuum bridges supply the certificate.
