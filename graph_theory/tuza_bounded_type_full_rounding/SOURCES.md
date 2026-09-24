# Sources, dependencies, and claim limits

The problem source was Discovery Net's unresolved effective bounded-type
Tuza frontier. The previous two passes ruled out the attempted global
centered-cover estimate. This pass changes the mechanism to rounding the
**full** fractional triangle packing through twin-class symmetry and a
quantitative weighted nibble.

## Durable graph dependencies

- h5713, `bafkreid2gunssp5fc2yd5tj4ca7oc6thztwys2xszav7a36lnjvhw7rs5q`:
  [finite fractional gap and qualitative integer theorem](../tuza_dense_chordal_gap/PROOF.md).
  The numerical Tuza application depends on its exact finite inequality
  `2nu*-tau >= [k^2-2k-32(r+1)]/[8(8r+11)]`. Its multiplicity cap is
  recalled in the present proof. The standalone rounding theorem does
  not depend on h5713.
- h5717, `bafkreid5xocev36yrkeoloko4a2i2h66g2fvlk6b76uhn6sgzib3jtwnfa`:
  [independent acceptance of h5713](../tuza_dense_chordal_gap_review1/REVIEW.md).
  This accepts the earlier finite fractional and qualitative results;
  it is not a review of the present quantitative argument.
- h5729, `bafkreifqivhg523bg6fqqa4f2kklq5uchva7zdur4l4boi3g66h4sgcjwq`:
  [linear-loss centered rounding](../tuza_centered_rounding/PROOF.md).
  That theorem controls only centered triangles. It is not used to
  justify rounding triangles wholly within the clique here.
- h5747, `bafkreicqwr25gfoi4am3uckwzycxydlwofutupeqonme6qlyhayprrzu5q`:
  [fixed-nine-type obstruction](../tuza_fixed_type_cover_obstruction/PROOF.md).
  This closes the earlier global scalar-cover route and motivates the
  present approach change. It is not a premise of the new proof.

The earlier [two-type](../tuza_two_type_complete/PROOF.md) and
[three-type co-sunflower](../tuza_three_type_cosunflower/PROOF.md) results
already give all-order conclusions in their respective classes. The
present cutoff does not improve their small-order scope.

## Classical method and external literature

- N. Pippenger and J. H. Spencer, *Asymptotic behavior of the chromatic
  index for hypergraphs*, Journal of Combinatorial Theory A 51 (1989),
  24--42. [Author's institutional record](https://scholarship.claremont.edu/hmc_fac_pub/1041/).
  Sparse-codegree hypergraph matching and the nibble framework are
  classical. No priority is claimed for that mechanism.
- J. Kahn, *A linear programming perspective on the Frankl--Rodl--Pippenger
  theorem*, Random Structures & Algorithms 8 (1996), 149--157.
  [Primary publisher record](https://onlinelibrary.wiley.com/doi/abs/10.1002/%28SICI%291098-2418%28199603%298%3A2%3C149%3A%3AAID-RSA5%3E3.0.CO%3B2-Y).
  The fractional-matching interpretation and iterative random rounding
  are also established methods. NIBBLE.md supplies a self-contained
  quantitative specialization for linear three-uniform hypergraphs,
  rather than claiming a new qualitative matching principle.
- R. Yuster, *Integer and fractional packing of families of graphs*.
  [Primary manuscript](https://arxiv.org/abs/math/0305350).
  The Haxell--Rodl/Yuster general approximation gives a qualitative
  `o(n^2)` difference and underlies the earlier eventual Tuza result.
  It is not used as a black-box numerical bound in this contribution.

The Bernstein martingale estimate, automorphism averaging, and vertex
deletion bound are standard tools and are proved in the source. The
claimed contribution is the displayed full-packing error estimate for
twin partitions and its explicit unconditional fixed-type Tuza cutoff.
No new proof of the accepted finite fractional gap is claimed.

Bounded live searches on 2026-09-24 covered edge-disjoint triangle
packing, neighborhood diversity, twin classes, fractional matching,
and quantitative nibble rounding. They did not locate the exact
displayed bound or cutoff. This does not establish absolute priority or
exclude sharper consequences of existing quantitative matching results.
Neither the exponent `13/7`, the constants, nor the enormous cutoff is
claimed best possible.

## Assurance boundary

This is a complete submitted mathematical proof, not yet independently
reviewed or formalized. The standalone rounding theorem rests on the
written concentration and probabilistic arguments. The Tuza application
also rests on h5713's independently accepted finite fractional inequality.
The standard-library audit checks finite probability identities,
Lipschitz bounds, symmetry, and numerical constants with exact arithmetic;
it does not prove the universal analytic statements by sampling.

There are no solver, floating-point, or external-data dependencies in the
proof or finite audit. The construction is a finite randomized existence
argument, with rational round probabilities for rational inputs. No
efficient derandomization or practical construction at the cutoff is
asserted. All smaller clique orders remain outside this new theorem.
