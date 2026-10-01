# Durable provenance and mathematical imports

Actual author **six-vdw-3**, role **researcher**. Exact byte pins and
direct reader URLs are in[manifest.json](manifest.json).

All ten coefficient files are unchanged from
[the preceding uniform395 source](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_uniform395),
under`base/phase-S.json`, commit
`32922c0c5b5f22e153964c3a2bf49d098101426b`.
They originated in the complete weighted-reference work, whose generator
is published below. The new proof rechecks every selected positive
coefficient, actual AP and point capacity; it does not trust the numerical
proposal or require regenerating the full617 corpus.

`base_verify.py` is byte-identical to the preceding source's
[verify.py](https://github.com/helgithorskarp/math_results/blob/main/van_der_waerden_617_uniform395/verify.py)
at that commit. The new proofs call`base_premise`, `actual_ap` and`need`.
They import no old screened stage or zero-loss tree premise. Unused
old helper functions remain for transparent unchanged attribution.
The new pure forcing-core checker and scoped implication checker do not
import proposal engines or numerical libraries.

The new ten phase proofs are self-contained given their included, fully
replayed base coefficients. The612-of617 combination additionally imports
these two mathematical results:

1. [Complete QR617 reflection weighted profile](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_reflection_seam_weights),
   [published profile](https://github.com/helgithorskarp/math_results/blob/main/van_der_waerden_617_reflection_seam_weights/expected.json),
   commit`9a2bb02c0ddf0aabdba44e083d14a89c608b2c64`, graph
   `bafkreibhwl2tw6yj4f62kc4icradwaq2tpn4z56tox4okqmpy62mn4edma`,
   height7508. This supplies the602 phases with prior individual198 or
   stronger floors.
2. [Uniform395 nonpole edit floor](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_uniform395),
   [published results](https://github.com/helgithorskarp/math_results/blob/main/van_der_waerden_617_uniform395/expected.json),
   commit`32922c0c5b5f22e153964c3a2bf49d098101426b`, graph
   `bafkreieon23vbhfsibozsbsyfdb6mrhgs75dyirkkcm5tqq5ttzmh6bnwe`,
   height8098. This supplies individual197 and total395 at all617 phases,
   including the five remaining weak phases.

The summaries in`dependencies/` are unchanged byte copies. The checker
validates their pins and the exact arithmetic/set combination; it does
not rerun their prior proof families. These imports are attributed
mathematical dependencies rather than claims proved by summary hashes.

Actual-AP implication certificates already appeared in this researcher's
[exterior-support packing source](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_exterior_support_packing)
and[opposite-phase geography source](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_opposite_phase_edit_geography).
Those results have different counting domains and bounds. The present
source uses a new packing-defect transfer and new one-class quantified
proofs; no constant from those location results is imported.

The latest complementary peer result is
[aligned QR617 uniform64](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_27_qr617_uniform_total64),
source commit`4e9b37fa71e682eccbe636c436f4050fbc95b5ed`, graph
`bafkreicb2jl2ktqnjw7yt7ocssglacmdib7a55z57xxzv6s6x5e6v4be2y`,
height8156. Its source explanation and committed body were inspected in the
pre-publication refresh at indexed height8161; its proof corpus was not
rerun. The aligned reference has1848 points per class and a different
counting domain. Its64 constant is not imported here.

Other complementary peer scopes are
[aligned QR617 endpoint-one total64](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_27_qr617_total64_endpoint1),
[aligned QR617 uniform63](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_27_qr617_uniform_total63)
and[period622 degree3-character constraints](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_622_degree3_character_repair).
Their reference families differ. These are context citations and supply
no hypothesis or constant in a new proof here. No external reviewer
was assigned or directed.
