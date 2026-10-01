# Source context

Actual author: **six-tammes-1**, role **researcher**, 2026-10-01.
Sole assigned family: Tammes separation for fifteen points on the unit sphere.

[Musin--Tarasov, *The Tammes problem for N=14*](https://arxiv.org/abs/1410.2536)
proves fourteen-point optimality using irreducible contact graphs. The known
fourteen-point cosine is the positive root of `4u^4-2u^3+3u^2-1`, greater than
`14/25`. This and the existing fifteen-point construction give the improvement
domain used in this lane. [Cohn's maintained table](https://cohn.mit.edu/spherical-codes/)
still has an unstarred N15 entry, with cosine
`0.59260590292507377809642492233276` and quintic
`13c^5-c^4+6c^3+2c^2-3c-1`. The primary coordinate source and these tables were
refreshed during this pass. No new construction or numerical optimum is claimed.

[Musin--Tarasov, *Enumeration of irreducible contact graphs on the sphere*](https://arxiv.org/abs/1312.5450),
Proposition2.6, attributes to Boroczky--Szabo the restriction that an irreducible
contact-graph hexagonal face has at most one isolated vertex. Those hypotheses
are preserved when crediting that classical result. The present short-cycle
claim treats arbitrary additional code points, unequal near-contact edges,
concave cycles and cycles that are not faces, on its explicit parameter interval.
It supplies a quantitative sufficient exclusion rather than a new statement
of the classical theorem. Spherical support geometry, great-circle/lune counting
and the two-cap hull mechanism are elementary established geometry; historical
priority is not asserted from bounded searches.

Published campaign context:

- [Our short-polygon/planarity proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/short-polygon-cover/PROOF.md),
  source `255d99ccd3ea40c4df2823f848b6154182f47bd7`, graph8581
  `bafkreig6swikau7zwaf7adjvo3kgwqrvibjntzbhuijq7bak2na7tc5kym`.
- [Our nonconvex short-cycle covering proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/nonconvex-short-cycles/PROOF.md),
  source `0816c33d6e7225ed357e6ffec14d1f09ecb3b1ce`, graph8650
  `bafkreigqac6v5l7cobm7gv64jqbgsrlk5qrqozb5bivw5dyzzupnbwxele`.
  Its positive sum supplies the same hemisphere mechanism, rederived here.
  Its independent reviewer8706 audited that older result, not this claim.
- [Our nine-template hull-capacity proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/hexagon-hull-capacity/PROOF.md),
  source `8607a4555c7ba7ca79c98002772dfa730f7b9d3d`, graph8715
  `bafkreig7gr2p5asv3moq5s7r5ymrckvlmckkiiprkzrwqp3zes5xt5lavi`.
  The template constraint is absent from the new cycle-region exclusion,
  while that certificate controls the entire specified hull neighborhoods.
- [Our radial and geometric-center criteria](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/radial-cycle-capacity/PROOF.md),
  source `778a828b1faecd914a9d816366a7d64432f2c0c8`, graph8771
  `bafkreiaflk2cepjld5clkfd6htf3edwbi3p43nva367fbanezwweaviqti`.
  The new theorem removes those radial/witness hypotheses for six-cycle regions
  in the fifteen-point interval at the narrower1/100 edge tolerance. The earlier
  criteria also handle other cycle sizes, a wider parameter/edge strip and the
  entire convex hull; neither whole source supersedes the other.
  Its [exact regular-hexagon benchmark](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/radial-cycle-capacity/HEXAGON.md)
  has two insertions below the present interval and remains consistent with it.
- [six-tammes-2's fixed thirteen-core/two-insertion completion](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/thirteen-core-completion/PROOF.md),
  source `a487998fad6781a7f3b5f2c1af05aea6707e7ed8`, graph8755
  `bafkreiczt46c72koms4wccxs3ah555j2xlyax5kpb3vswc6jnade6dskta`,
  gives a complementary specified24-contact exclusion. Its source and original
  graph body were read, but are not mathematical premises or independent reviews
  of this geometric exclusion. Optimizer occurrence remains open in both lanes.

The current proof and scalar checkers are self-contained; no graph contribution,
external coordinate file or solver certificate is imported as a proof input.
The prior crossing and hemisphere mechanisms are included, with attribution.
No claimed review of an earlier source is transferred to this source.
