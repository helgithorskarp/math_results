# Dependencies and attribution

This is Team A researcher 1's independent review of Team A researcher 2's
[complete decision reduction](../decision71/README.md). It accompanies a
separately written geometric checker and a fresh replay of the author's
complete reduction. It does not claim a new value of the extremal number.

## Mathematical dependencies

* Complete finite cover, graph
  `bafkreifrsrzf2igkvt5o3yfe6uvliewuha5glpyi5kfmi22kvumk2enitu`,
  committed at height 6046. Original source commit:
  `6d2f193aecad54cc41dab4cdf67c16f9add58cc2`.
  Reviewed directory last changed at
  `0bd139b2d32f58fcb080b6f90aa42387931d54b6`.
  Every reviewed file has a hash in `EXPECTED.json`.
* Researcher 3's [two-low-plane theorem](../low_pair71/THEOREM.md), graph
  `bafkreidy3j3g3qeasqbqxpnzayye526ojhqmes2mvj57glffihpdlf2m3i`,
  height 5996; source commit
  `0d331185c9dbfb6db32ebffc8bdaae4e0b4aa144`.
  It supplies the fifteen-type complete cover inside the fixed twenty-type
  domain. Its fourteen certificates are replayed by the production verifier.
* [Independent low-pair acceptance](../low_pair71_review1/README.md), graph
  `bafkreibvd76t2o6klwh7lkxwlshvaty2aoyjdpam6ryonzuvdetzretyea`,
  height 6050. This existing review checks the stronger low-pair premise;
  it is distinct from our new review of the global decision reduction.

The planar cap, integer certificates, complete quotient enumerations,
and full affine partition are reproduced by the existing author verifier.
All source for that replay is retained in its original directories.
`independent_check.py` constructs its own expected geometry, profiles,
coordinate maps and clauses. It imports `decision71/point_model.py` only
to compare the implementation being reviewed with these expectations.
It is not a third complete quotient enumerator or an UNSAT proof checker.

## Positive controls

The raw point lists are read from
[known70.json](../known70.json),
[odd_symmetry/witness70.json](../odd_symmetry/witness70.json), and
[affine_asymmetry71/witness70.json](../affine_asymmetry71/witness70.json).
Their input hashes are recorded. The first file attributes its construction
to Elsholtz et al., *Maximal line-free sets in F_p^n*, Figure 4; the latter
two were supplied by the team's symmetry/construction work. We verify
the supplied points directly, so no claim from the original literature
is required as a premise of the reduction review.

## Context inspected, not assumed

* Our [gauged planar-marginal obstruction](../gauged_quotient_obstruction71/README.md),
  graph `bafkreid4rliqsbmrt22l62s3b5vdmplsdvd46s22c6gw24jkjfeog32ts4`,
  height 6054, source `3143f09575de5866ddf9b96f88ceacdca3d8572b`.
  It closes the preceding separate-plane marginal route and motivates
  checking the complete integral reduction.
* Researcher 4's [two-six-plane classification](../two_six_extremals70/README.md),
  graph `bafkreichd3pgwca4wdmqiheqz2smqojwohoroblkr5brwykam4phhvddjq`,
  height 6056. Its seven-plane corollary is not needed or accepted by this
  review; independent review of that new result is separate work.
* Researcher 3's [nonzero quadratic moment theorem](../nonzero_quadratic_moment71/README.md),
  graph `bafkreidhyh6lrr35v2fuf5noljtusx2cspsoxvhhxhlw3rafxqjrxryxxa`,
  height 6024, is not used.

All four Team A reports and bounded relevant source and graph updates
were refreshed during this pass. Exact-value determination and independent
acceptance of its decisive evidence remain outstanding.
