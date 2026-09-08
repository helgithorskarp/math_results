# Three 169-point triangular patches: exact pairwise-irrational classification

Let

```text
P48 = {a+b omega : a^2+ab+b^2 <= 48},
omega = (1+i sqrt(3))/2.
```

For unit complex numbers `alpha_0,alpha_1,alpha_2`, suppose every relative
rotation `conjugate(alpha_i)*alpha_j` lies outside `Q(omega)`. Then the three
patches share only the origin, so their union has exactly 505 physical points.
The strict unit-distance graph on that union is always four-colourable. More
precisely, its chromatic number is four exactly when one pair of patches has a
cross edge joining two residue-zero vertices; otherwise it is three.

The only case not settled directly by the two-patch residue colouring is when
all three patch pairs have proper cross contacts. An exact enumeration gives:

- 169 vertices and 456 internal unit edges per patch;
- 720 irrational relative rotations having proper cross contacts;
- 216 complete three-layer contact configurations;
- 114 distinct labelled strict graphs, all with 505 vertices and 1,398 edges;
- an independently checked explicit three-colouring of every graph.

All 216 complete-contact cases have three individually three-chromatic sides,
with 6, 12, and 12 proper cross edges. Their rotations lie in the squarefree
quadratic field with radicand 21. The verifier reconstructs the full contact
inventory in Cartesian coordinates, performs 10,281,960 exact squared-norm
comparisons, enumerates every contact triangle using multiquadratic arithmetic,
and checks all 114 committed colour words against the reconstructed strict
edge sets.

This is a complete negative decision for the stated 505-point family. It does
not improve the 509-vertex five-chromatic record.

See [PROOF.md](PROOF.md) for the proof and exact scope. `EXPECTED.json` and
`VALIDATION.json` record the verified census and validation environment.

## Reproduce

The independent verifier uses only the Python standard library:

```sh
python3 hadwiger_nelson_three_triangular_patches/verify.py \
  --output /tmp/hn-three-patches-verified.json
python3 hadwiger_nelson_three_triangular_patches/controls.py \
  --output /tmp/hn-three-patches-controls.json
```

The recorded runs used CPython 3.11.2 and took about 35--40 seconds each on a
shared machine. `build.py` regenerates the witnesses using Kissat; the solver
is used only to find colour words, not to verify them:

```sh
python3 hadwiger_nelson_three_triangular_patches/build.py \
  --kissat /path/to/kissat \
  --output /tmp/COLOUR_CERTIFICATE.json
```

