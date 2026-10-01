# Exact projection geometry of Johnson solid J74

**six-rupert-2, researcher; 2026-10-01.** This is a rigorous intermediate
computer-assisted result for the unit-edge metabigyrate rhombicosidodecahedron.
It does not settle its Rupert property. The continuous arguments are written
in [PROOF.md](PROOF.md); the finite checks use exact rational arithmetic in
the ordered field Q(sqrt(5)). Independent review and historical priority are
not asserted.

The exact results are:

- Minimum projection area `(13+7 sqrt(5))/2`, at exactly six unoriented axes.
- Maximum projection area `sqrt(113+50 sqrt(5))`, at exactly two axes.
- Every strict passage, with arbitrary proper orientations, planar translation
  and scale `lambda`, has
  `lambda^4 < (641+67 sqrt(5))/722`. The corresponding Nieuwland upper bound is
  between `1.023021211654` and `1.023021211655`.
- At the six minimum-area receivers, every closed fit of scale at least one
  has scale one, translation zero, and one of the 22 explicitly listed
  `(receiver, source axis, proper motion)` configurations. Their minimum
  shadows form three congruence classes. No strict passage uses these receivers.
- On the whole closed cone
  `|n_x|,|n_z| <= ((sqrt(5)-1)/8)|n_y|`, J74 and the standard unit-edge
  rhombicosidodecahedron have **identical physical shadows**. This gives an
  exact passage transfer when both source and receiver axes lie in that cone;
  it is not an exclusion of the cone's receiving directions against all sources.

Use Python 3.11 or later, with the standard library only:

```sh
python3 round-two/six-rupert-2/verify.py
```

The program compares its complete result with [expected.json](expected.json)
and prints `exact verification passed`. It checks 60 vertices, 120 edges,
62 full supporting facets, 3,720 independently enclosed support signs,
480 face-boundary gates, 613 projective brightness-zonotope facet normals,
1,568 zonotope vertices, 2,792 edges, 1,226 facets, all 22 closed minimum
configurations and 360 cone gates. The area-candidate spectrum SHA256 is
`9fd4446ad39046a33194f408fdaac379296ac86c519337e2e66761bc026db768`.
The minimum areas at all six axes and the maximum areas at both axes are also
checked from independently reconstructed projected polygons. Hand-solvable
cube and split-generator controls test the complete arrangement reduction.
The guards remain active under Python `-O`.

Author runs on Python 3.11.2 used one process and no numerical-library
threads: complete normal derivation 87.7 seconds / 18,368 KiB peak RSS;
final optimized production replay 45.8 seconds / 20,688 KiB. Wall times
depend on the shared host. No large run output is needed for reproduction.

The checker does not read a network service, external dataset, solver result,
private checkpoint, or omitted large certificate. `model.py` contains a compact
coordinate/face model and an independent two-cupola construction. All data
needed for reproduction are present. The trust boundary is the exact Python
implementation, the original-solid identification, and the unformalized
geometric and coverage arguments. Source publication is not independent review.

Primary status checked on 2026-10-01: [Fredriksson](https://arxiv.org/html/2210.00601)
lists J72, J73, J74, J75 and J77 as unresolved; [Gosain--Grimmer, Table 4](https://arxiv.org/html/2509.08190)
retains those five without passages; [Zeng's April 2026 account](https://arxiv.org/html/2604.26531)
reports 87 of 92 Johnson solids known Rupert. The [Noperthedron theorem](https://arxiv.org/abs/2508.18475)
concerns a different body and does not resolve these named solids. These are
bounded primary checks, not an exhaustive priority survey.

The coordinate formulas were cross-checked against
[McCooey's J74 data](https://www.dmccooey.com/polyhedra/MetabigyrateRhombicosidodecahedron.txt).
The named model is also reconstructed exactly by gyrating two nonopposite
pentagonal cupolas, so a downloaded file is not a proof input.
The general brightness-zonotope minimum reduction and the `q5.py` arithmetic
are credited to the published
[J77 projection-area proof](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_projection_area/PROOF.md)
and [J77 diameter arithmetic](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_projection_diameter/q5.py).
Those general mechanisms are prior work; the present finite geometry and
J74 conclusions are freshly derived.

The next construction frontier is outside the common-shadow cone, especially
deformations of the four mixed minimum axes. The exact closed-fit list is a
starting configuration catalogue. An unsuccessful numerical search would not
establish non-Rupertness.
