# Dependencies and scope of novelty

This is Team A's structural route toward exact `r_5(F_5^3)`, the precise
problem assigned by the user.

## Durable dependencies

1. [Global low-plane reduction](../low_planes72/README.md), graph artifact
   `bafkreifb7i4346rrz2c5ch5vhs4odx3n57xijazwl6jrgjhdmmijzthaqy`.
   Its complete 70-spectrum enumeration and 61-equation incidence system
   are reused with attribution. Its three cutoff certificates do not
   give the weighted inequality proved here. The replay recompiles its
   `enumerate_spectra.cpp` and checks its `spectra_expected.txt`.
2. [At most one eight-point plane](../two_eight_planes72/THEOREM.md),
   `bafkreidboslmutvk646hvk6d7kjyvqopa3ks6znrczmmwnyqpdirzoqwwu`, h5942.
   Its bound `a_8<=1` is required for the eight-nine-plane consequence.
   Its finite reduction and 164 checked DRAT exclusions are inherited
   premises, not newly claimed or independently re-reviewed here.
3. [The upper bound 72](../upper_bound72.md),
   `bafkreigdcleaywkrwivj7mewtq4lir55ort2jlkblt6a72m5j5bskscdjq`,
   supplies the current frontier. The new theorem is conditional on a
   candidate of size exactly 72 and does not improve that numerical bound.

Also inspected were the sparse-direction theorem
`bafkreigqsybtdtym4u4lrk5fuypamdiv7oidqrycqkoyius3f5cafmqaj4` and the
[size-71 planar marginal obstruction](../../additive_combinatorics/line_free_planar_lp_obstruction/PROOF.md),
`bafkreifwjecau65opqj3hmj5ba2d4dlig2advvmkjtkx5xztwpovu24o4y`.
Neither is a proof premise for the new inequality or frame lemma.

## Primary literature inspected live on 2026-09-26

* C. Elsholtz et al., *Maximal line-free sets in F_p^n*, Periodica
  Mathematica Hungarica 90 (2025), 7--21,
  [arXiv:2310.03382v2](https://arxiv.org/html/2310.03382v2),
  [DOI](https://doi.org/10.1007/s10998-024-00617-x).
  This supplies the prior 70-point construction and published 70--73
  interval. Its planar and pencil counting framework is antecedent work.
  The known witness is a replay control, not a new construction.
* S. Kurz, I. Landjev and A. Rousseva, *Classification of (3 mod 5) arcs in
  PG(3,5)*, [arXiv:2108.04871v2](https://arxiv.org/abs/2108.04871v2).
  This enters older upper-bound work; its classification is not directly
  used by the new certificate or elementary frame argument.

The relevant committed neighborhood was refreshed through height 5949,
alongside teammate reports and repository commits. No incoming objection
or overlapping weighted/frame theorem was found. A bounded live search
for line-free sets and affine blocking sets found no matching global
nine-plane-frame statement. This is search-relative novelty evidence,
not a historical priority claim.

The new content is the weighted integer inequality, its composition with
the recent eight-plane exclusion, and the resulting single global BBB
normal form with a fourth normal in general position. LP duality,
projective frames, affine normalization, and the prior incidence system
are standard or attributed ingredients. Optimizing the rational bound
beyond its integer threshold is not an objective or novelty claim.
