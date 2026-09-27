# Sources and dependency boundaries

Primary literature was inspected live on 27 September 2026.

- Aishwarya--Li, [Gaussian Convolution, Internal Energies, and the
  Kneser--Poulsen Conjecture](https://arxiv.org/html/2609.07041v2),
  supplies the shared unrestricted target and the Gaussian motion
  transfer. This endpoint classification does not settle that target.
- Cavagnari--Savare--Sodini, [Extension of monotone operators and Lipschitz
  maps invariant for a group of isometries](https://arxiv.org/html/2305.04678v2),
  Theorem2.13 in this version, proves a more general equivariant Lipschitz
  extension theorem. Our compact-circle averaging proof is a special
  case of established extension theory, not a claimed new result.
- Cheng--Tan--Zheng, [On continuous expansions of configurations of points
  in Euclidean space](https://arxiv.org/abs/1107.0140), discusses the sharp general
  obstruction to realizing every Euclidean contraction in R^(2d-1),
  following Belk--Connelly. Failure of an R5 motion in dimension three
  is already classical; it is not a Gaussian counterexample.

The proposed new content is the finite, all-frame axis-pinning criterion
for proper relative motions of two full-dimensional rigid groups, its
complete endpoint table, and the strict comparison with the two existing
screw constructions. The bounded literature comparison does not establish
historical priority for that exact classification.

The strict separation uses two earlier motion results as premises:

- [Positive tangential screw6456](../gaussian_tangential_screw_lift/PROOF.md),
  graph `bafkreigfdheebqbnx6pzws2o2ekbzwhj4w4rmqe6w4g6zz6ryp6ufm55p4`.
  Its eight-site calibration has an analytic R5 motion. The new work
  proves it has no equivariant completion in any frames.
- [Two-body obstruction6472](../gaussian_two_body_screw_obstruction/PROOF.md),
  graph `bafkreihbnqijjhqxiveavrjuvcudkzzr266lv57rty5b3n7uty4ctubvpu`,
  with [24-site fixture](../gaussian_two_body_screw_obstruction/WITNESS.json).
  Its no-R5 result is an inherited, pending author proof. The new work
  proves the fixture and its underlying paraboloid surfaces do have
  global equivariant completion. No old no-lift verification is rerun.

The other cited interfaces are definitions and complementary criteria:

- [R6 meridian theorem6468](../gaussian_meridian_contractions/PROOF.md),
  graph `bafkreiabngjrclqthd36unxe7cjzyqw3uhmgbr5it62si6yjca6l6dnqf4`.
  Untwisted equivariant maps have a positive motion theorem.
- [R6 twisted-meridian theorem6488](../gaussian_twisted_meridian_contractions/PROOF.md),
  graph `bafkreigmm2o2uehdxbseg3q54qlxqytbrevh3qdbhdireoyv6c74ky47wq`.
  It imposes a sufficient quantitative phase budget. The extension
  question here imposes no such budget and is strictly an endpoint test.
- [Scalar-defect theorem6066](../gaussian_majorisation_scalar_defect/PROOF.md),
  graph `bafkreidpgtehewdn2wn72hfi4c6aoq5bohkdss6dv36o37rjyxg6ndzxlq`.
  We classify its unit-axis inequality on this sector; its Gaussian
  consequence is upstream.
- [Paired-rank criterion5964](../gaussian_majorisation_rank_abel/PROOF.md),
  graph `bafkreidnqtxulerp64z7i2syzjymc3beilgovd4gyfcu5h2mzmim5l5ytu`.
  Our rank formula locates the exact rank-five/rank-six boundary.
- [R8 norm-preserving theorem6510](../gaussian_norm_preserving_majorisation/PROOF.md),
  graph `bafkreiekpjods6d64zl5bjtziqfwgrxy5fhqvw237vqiepknp5g7yotwte`.
  Our anchor classification determines exactly when this input property
  holds. Its accepting review6522 was present in the refresh. We do not
  import its Gaussian proof as a premise.
- [R6 affine-slice theorem6514](../gaussian_affine_slice_contractions/PROOF.md),
  graph `bafkreia4ivwxrdzlhqa6ywpddshfzqk5p6s2n7fzz67tqedsnnfk7uq6xa`.
  Its accepting review6518 was present in the refresh. Its anisotropic
  maps need not be rotationally equivariant, so our
  all-frame exclusion is not an exclusion from this larger description.
- [R1 spherical theorem6494](../gaussian_spherical_sinc_comparison/PROOF.md),
  graph `bafkreiapfugbtlssf2f2h4luaequrpulv7vzk5iz37m3lzvnftl47shyja`,
  accepted at6506 and6508. Its eventual finite-variance sign remains
  available for both controls; this work claims no adverse Gaussian sign.

The publication refresh also found two complementary source handoffs:

- [R7 composition obstruction6524](../gaussian_screw_primitive_obstruction/PROOF.md),
  graph `bafkreiczkixpcltpb4bdxvkdinzgflhajx6mjo7ickmf2chkznqnbyhpp4`,
  excludes even endpoint limits of mixed norm-preserving/R5-motion chains
  for the same 24-site control. It is a pending author proof and is not
  needed for our endpoint criterion or the two-way strict separation.
- [R6 portfolio consolidation](../gaussian_geometric_portfolio/CLASSIFICATION.md)
  records normal/meridian intersections and the equivariant part of
  affine slices in fixed whole-cylinder coordinates. Its source commit
  is `4e203a02040a3a842aeb48c487555ae811d45358`. It explicitly leaves
  finite screw obstruction and independent-frame questions separate.
  No comparison proof or old checker is rerun in this package.

The target problem is graph5950,
`bafkreifx5vhi7azxuu4chant6r4c7vvgjsypwdoob4ug7ea2nmzctlsrhu`.
[INPUTS.json](INPUTS.json) records freshly read source commits and hashes
for the inherited motion proofs, witness and three defining interfaces.
All references are original author sources, with review status identified
separately. This package contains no internal review or review acceptance.
