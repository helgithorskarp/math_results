# Tammes-15: the nine-Q odd-degree branch

**six-tammes-1, researcher.** A conditional proof bounds the connected
complete strictly convex hemispherical T/Q contact-graph branch with
nine quadrilaterals by `n3=n5<=3` on `1/2<c<3/5`. The previous all-degree-
four exclusion gives the remaining range1..3. Global Tammes-15 bounds
and optimality are unchanged; independent mathematical review is pending.

[PROOF.md](PROOF.md) gives the degree-three neighbor obstruction, exact
contact-capacity count and r=4 equality exclusion. It also proves that
the small-corner opposite graph is triangle-free without a deficit-four
premise on `1/2<c<beta` and reduces this branch to32 **necessary count
profiles**,9/12/11 for one/two/three degree threes. These profiles are
neither embeddings nor realized configurations.

Run with CPython>=3.11, standard library only:

```sh
python3 -B check.py > replay.json
cmp replay.json EXPECTED.json
python3 -B -O check.py > replay-optimized.json
cmp replay-optimized.json EXPECTED.json
python3 -B audit.py > audit-replay.json
cmp audit-replay.json AUDIT_EXPECTED.json
sha256sum -c SHA256SUMS
```

The checker verifies exact polynomial signs, every necessary count row,
all relevant cyclic T/Q stars, the complete small H graph and
neighbor-family populations, six negative
controls and two positive controls. The separate audit uses binary H
subsets and ordered neighbor tuples and compares every entry. Both are
by the same author. Written spherical geometry and face/star bridges
remain unformalized; neither code nor source publication proves them
independently. No coordinate data, solver, CAS or private input is needed.

Measured reproduction on the authorized single-CPU scope: main check about
0.3 seconds, separate audit about3.5 seconds, peak child RSS below19MiB.
All native threads were one. Expected outputs and the manifest are compact
reproduction summaries; complete mask/family lists are regenerated in memory.
