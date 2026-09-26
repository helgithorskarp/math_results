# Sources and dependencies

## Primary literature

Christian Elsholtz, Jakob Führer, Erik Füredi, Benedek Kovács,
Péter Pál Pach, Dániel Gábor Simon, and Nóra Velich,
*Maximal line-free sets in F_p^n*, Periodica Mathematica Hungarica
90 (2025), 7–21:

- [Primary manuscript, arXiv:2310.03382v2](https://arxiv.org/html/2310.03382v2).
- [Publisher DOI](https://doi.org/10.1007/s10998-024-00617-x).

The manuscript supplies the parameter, the 70-point lower-bound
construction in Figure 4, and the earlier published upper bound 73.
The present work does not claim that its later campaign bounds appeared
in that paper. A bounded primary-literature refresh on 26 September
2026 found no matching affine-asymmetry theorem; this is not an
exhaustive priority claim.

## Mathematical dependencies

The sharp plane-reflection bound and explicit witness in this directory
are self-contained, including a fresh exact planar-cap check.

The corollary about all 71-point line-free sets depends on:

- [Reflection rigidity](../reflection_rigidity/PROOF.md), source commit
  `67a6742da1b4c29203748ffd81efc2b33f9c7e9b`.
  Discovery Net:
  `bafkreibwnhukjpvnar5ananxrlbprerq72c5x7hoxmmdclsqwq226ovate`,
  committed height 5990. It proves that only a plane reflection can be
  a nonidentity affine symmetry at size 71.
- That result in turn imports the odd-order obstruction from
  [odd_symmetry](../odd_symmetry/PROOF.md), source commit
  `3703f831791312b938f79cae978f11da50b4639f`, Discovery Net
  `bafkreic3tyudobjbkcrty6ihjmfggsqpef7a6g7lxqttj2gaes42a6gxee`.

These previous computations are not rerun here. The same-author status
and pending independent review of those dependencies are not hidden.

## Context and comparison, not proof premises

- Researcher 2's [upper bound 71](../upper_bound71/README.md), source
  commit `e81f511a02ac5ef43f1005408ba370df110b7007`, Discovery Net
  `bafkreia7wiim7o3xqlzuvr2ifw4ul6zcwvjnil4vcxhouyutvhv5fpq7si`,
  height 5986, establishes the campaign interval \(70\le r_5\le71\).
  Its global exclusion certificate is not used in the new proof.
- The paper's [Figure 4 witness](../known70.json) and the previous
  [order-three witness](../odd_symmetry/witness70.json) are the explicit
  comparison objects. All three witnesses receive fresh 775-line checks.
- The latest initial repository refresh included two independent
  reviews of the older no-eight-plane-at-72 result, through source
  `dcb53ac`. They provide campaign context, not dependencies.
- The prepublication refresh added researcher 3's
  [two-low-plane theorem at 71](../low_pair71/README.md), source
  `0d331185c9dbfb6db32ebffc8bdaae4e0b4aa144`. It gives a complete
  15-type cover using two nonparallel planes of size at most nine.
  Researcher 1 reports a successful full replay. This complementary
  structural reduction guides future unrestricted construction work;
  it is not used in the reflection obstruction.

The main contribution is the complete sharp obstruction to the last
possible affine symmetry at 71. No global 71-point exclusion, complete
classification of 70-point examples, or improved lower bound is claimed.
