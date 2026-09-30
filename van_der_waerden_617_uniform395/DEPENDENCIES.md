# Explicit prior mathematical dependencies

Actual author: six-vdw-3, researcher.

The default command checks unchanged summaries by SHA256 and imports the
named prior results. It does not replay their proofs. Use each source
directory's README for independent full reproduction.

## base_profile

- [Source](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_reflection_seam_weights).
- [Published expected result](https://github.com/helgithorskarp/math_results/blob/main/van_der_waerden_617_reflection_seam_weights/expected.json).
- Source commit: `9a2bb02c0ddf0aabdba44e083d14a89c608b2c64`.
- Discovery Net contribution: `bafkreibhwl2tw6yj4f62kc4icradwaq2tpn4z56tox4okqmpy62mn4edma`.
- Exact copied summary: `dependencies/base_profile.json`.
- SHA256: `f2a45d467cefc5ec605c84417742bbac7a9531211c01baba6770b0d499a61db5`.

## individual197

- [Source](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_class197_cover).
- [Published expected result](https://github.com/helgithorskarp/math_results/blob/main/van_der_waerden_617_class197_cover/expected.json).
- Source commit: `12cb7739d9d179684bee19a50f9ebd54c2794ff7`.
- Discovery Net contribution: `bafkreidd54kxpyjlspt4tww57ib3p5ldcdc72h7isybb6onoeugb2u7eta`.
- Exact copied summary: `dependencies/individual197.json`.
- SHA256: `7eaa9259df5ce7da09ea008f53a76d75f661cfb25ec6019b93b4a7ee152f7b42`.

## joint201

- [Source](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_phase201_joint197).
- [Published expected result](https://github.com/helgithorskarp/math_results/blob/main/van_der_waerden_617_phase201_joint197/expected.json).
- Source commit: `3c9ee6d835f424b8906f4acb3ba3415774ffd082`.
- Discovery Net contribution: `bafkreihc2fz46sihwbcs4mxm4xigqnqyub7o2lw7lkwan43pb3cludz3bu`.
- Exact copied summary: `dependencies/joint201.json`.
- SHA256: `a76947d81e6a2c138568a2ed286ceb7d3b103e384c8880044df1d815e4693182`.

## joint269

- [Source](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_phase269_joint197).
- [Published expected result](https://github.com/helgithorskarp/math_results/blob/main/van_der_waerden_617_phase269_joint197/expected.json).
- Source commit: `6f4a3d42cb193d04a539d65fa01d8b99bbd790e3`.
- Discovery Net contribution: `bafkreib6hwys53rnc2hwfakkcak2ef2lkhaqm2k4knqfukdguofp4h5fhe`.
- Exact copied summary: `dependencies/joint269.json`.
- SHA256: `9a870c5cbf8ef20af9513d36c63186e4ad3d45fcc2561c142a70a90c65572099`.

## Mathematical use

The `base_profile` result supplies the original complete617-phase lower-bound
profile. Its602 phases with individual floor at least198 already exclude a
197/197 box. Its frozen base certificates for the13 new phases are supplied
here and are checked again from definitions.

`individual197` supplies a197 floor at the four old floor196 phases
184,201,205,269, completing the uniform197 floor. The present zero-loss
checks also replay the needed individual floor at184/205 from the complete
old trees; the copied old trees and these two base certificates are unchanged.

`joint201` and `joint269` supply the two earlier excluded197/197 boxes.
Their root proofs are not copied into this directory. Together with the
fully replayed13 new boxes and602 old strong phases this gives exactly617
phases, with no duplicate or omitted phase.

The new code is adapted from the same author's published
[phase201 source](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_phase201_joint197)
and its earlier
[zero-loss argument](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_phase201_zero_screen),
source commit `56592467f119c9ea374c1038e17993589bfd6021`, contribution
`bafkreiefgv6x2yz3mzhilqlmni55pptqyz2oqdizvx6pif4hcscc7q6ula`.
That method is cited; the phase201 zero-loss theorem is not needed as an
additional mathematical assumption for the new184/205 checks.

The old full617 weight corpus is intentionally absent. Its original public
source generates and verifies it; imported summaries are not a substitute
for that verification. No claim is made that a hash proves mathematics.

Nearby complementary work uses different reference models:
[the uniform aligned QR617 total63 floor](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_27_qr617_uniform_total63),
source commit `608d13b42e1090fb6d5ca5b6502f03d74bb69216`, contribution
`bafkreica4jwle5gkif5zzbowoflfreqhas5caz5hpi73fzd43s342m3ykq`, and
[period622 degree3-character repair obstructions](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_622_degree3_character_repair),
source commit `c768156dd53b9d25d45439ecf9e63334dadcaa7e`, contribution
`bafkreic7axpkcg2kybbz5ldy6xp4lumihkvoetygo7kk5s5obrbq56sjye`.
Neither is imported into this proof. Uncommitted teammate improvements are
not used as theorems here.

The fresh committed peer result
[endpoint-one aligned QR617 total64](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_27_qr617_total64_endpoint1),
source commit `d7f48098cb700d6c50236d6fe1381d1be0a1786b`, contribution
`bafkreigdqnclint5ctzsmjpvq56oizpeh67mt35nexvgbrjbi4afaxgyw4` at height8048, was also inspected.
Its endpoint-one lower64 and complementary endpoint-zero upper3632 use a
different reference and edit-counting domain; no constant transfers into
this proof. It is complementary and is not an imported dependency.
