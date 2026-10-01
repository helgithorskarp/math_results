# Exact projection and receiving-cap geometry of Johnson solid J74

**six-rupert-2, researcher; 2026-10-01.** This is a rigorous intermediate
computer-assisted result for the unit-edge metabigyrate rhombicosidodecahedron.
Every strict passage of scale at least one is excluded in closed receiving-normal caps of chord radius
**1/270** about the symmetric minimum axis `+/-e_y`. Its full Rupert
property remains open. The continuous arguments are written
in [PROOF.md](PROOF.md) and [RECEIVING_CAPS.md](RECEIVING_CAPS.md);
the finite checks use exact rational arithmetic in
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
  the follow-up source-area argument below supplies an all-source transfer
  on a specified part of the receiving cone.

[The central-section extension](section_transfer/PROOF.md) proves that
all six minimum-axis shadows of `S=(K-K)/2` are actual central sections.
Its 94 exact corner lifts give a quadratic area-loss bound. The global
minimum of `Area(P_nS)` occurs only at `+/-e_y`; its area excess at most
`1/25` localizes the normal within chord less than one third of the excess.
This enlarges the arbitrary-source common-cone transfer band to original
receiving area `a0+1/25`, including a transfer cap of radius **8/875**.
The larger committed RID theorem then gives the **1/270** J74 exclusion
cap and the global strict-receiving condition `Area(P_nS)>a0+1/90`.
The original-body area version of that gap is restricted to the common
cone. [Its independent section-certificate checker](section_transfer/check.py)
replays the pinned parent geometry and verifies all actual lifts; see
[reproduction and explicit dependencies](section_transfer/README.md).

[The first receiving-cap follow-up](RECEIVING_CAPS.md) established:

- A global area budget `0<eta<=1/80` forces the original body normal within
  chord `<eta/3` of one of the six minimum axes.
- Every closed fit of scale at least one into a common-cone receiver with
  area at most `a0+1/400` forces its source into the same cone. Exact
  half-difference areas separate the other five source-axis branches,
  while cancelling arbitrary translation.
- Existence of proper J74 and RID placements is equivalent on that receiving
  band, with the actual scale and translation retained. The band includes
  closed receiving-normal caps of radius **1/1750**, a transfer radius.
- The committed [RID all-source cap theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_brightness_twofold_caps/PROOF.md)
  therefore excludes **every** proper J74 source, full roll, translation
  and scale `lambda>=1` at receiver chord at most **1/30000** from `+/-e_y`.
  Every strict passage whose receiver lies in the common cone also has
  receiving area strictly greater than `a0+1/10000`.

Here `a0=(13+7sqrt(5))/2`. The RID input uses edge two and is explicitly
rescaled to the unit-edge model; normal chord distances are unchanged.
The all-source equivalence and the exclusion radii are distinct statements.

Use Python 3.11 or later, with the standard library only:

```sh
python3 round-two/six-rupert-2/verify.py
python3 -B round-two/six-rupert-2/caps_verify.py
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

The second command compares every field of [caps_expected.json](caps_expected.json)
and prints `exact receiving-cap hypotheses verified`. It regenerates the
minimum spectrum and second level, six tangent disks, six original
half-difference shadows, 5640 separable all-original support evaluations,
64 tangent endpoint sums, 360 cone gates and the RID coordinate scale.
The complete [RID input proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_brightness_twofold_caps/PROOF.md)
and its earlier local criterion are written dependencies. Its exact checker
was replayed locally; no independent-review verdict is asserted.

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

[The weighted-contact extension](tangent_contacts/PROOF.md) constrains
deformations of all 22 minimum fits, with translation retained. Six exact
positive weight certificates imply zero translation velocity, equal or
opposite normal velocities, common planar roll velocity, and
`lambda(epsilon)-1=o(epsilon^2)` along any C1 closed-fit path through a
minimum fit. Its explicit frame radius **1/1000** establishes the
necessary inequalities, not an exclusion cap. The remaining construction
frontier is the higher-order behavior of those two tilt branches; the
full J74 question remains open. See its
[checker and reproduction instructions](tangent_contacts/README.md).

[The exact boundary-prototype reduction](boundary_prototypes/PROOF.md)
replaces all 60 J74 originals by 28 boundary originals throughout six
projective unit-normal caps of chord radius **1/15**. Proper marked-plane
transports reduce the six prototypes to at most three representatives.
Their verified reflection symmetry supplies an exact proper reflected
source companion with the same shadow, retaining roll, scale and
translation, even at mixed axes where the full body has no such symmetry.
Both normal caps are required to reduce a whole source/receiver fit;
the companion itself requires only the source cap. All 22 base motions
extend to exact equal-shadow reference families. The radius is a
reduction domain, not an exclusion cap. See its
[independent finite checker and reproduction instructions](boundary_prototypes/README.md).
