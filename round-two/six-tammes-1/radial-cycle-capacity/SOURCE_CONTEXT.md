# Source context and exact scope

Actual author: **six-tammes-1**, role: **researcher**. Refreshed 2026-10-01.
The sole problem family is Tammes packing of fifteen points on `S^2`.

## Primary literature and current status

- [Musin--Tarasov, *The Tammes problem for N=14*, arXiv:1410.2536](https://arxiv.org/abs/1410.2536)
  proves the fourteen-point optimum, with an irreducible contact-graph reduction.
  Its classical face geometry is relevant context, rather than a proof of the
  fifteen-point optimum or of our unrestricted-cycle capacity statement.
- [Musin--Tarasov, *Enumeration of irreducible contact graphs on the sphere*,
  arXiv:1312.5450](https://arxiv.org/abs/1312.5450), Proposition 2.6, records
  that an irreducible contact-graph hexagonal face contains at most one isolated
  vertex, attributed there to Boroczky--Szabo. Both "irreducible" and "isolated"
  are real hypotheses. The degree-one interior points of our eight-point control
  are not covered by that statement.
- [Cohn's maintained spherical-code table](https://cohn.mit.edu/spherical-codes/)
  and [Spherical Codes](https://spherical-codes.org/) are the incumbent construction
  sources. The unstarred `N=15` table entry has cosine
  `0.59260590292507377809642492233276`, with polynomial
  `13c^5-c^4+6c^3+2c^2-3c-1`. Good coordinates are construction data and do not
  prove global optimality. The prior template artifact pins the independently
  normalized [Sloane coordinate file](https://neilsloane.com/packings/dim3/pack.3.15.txt).
  No coordinate table is used at runtime by the present arithmetic companion.
- [Kuznetsov--Sahinidis, *A deterministic global optimization algorithm for the
  Thomson and Tammes problems*, DOI:10.1016/j.dam.2026.05.015](https://doi.org/10.1016/j.dam.2026.05.015)
  is a current primary algorithmic comparison located during this pass. Its
  Tammes experiments recover instances up to thirteen points. Its numerical
  global-optimization scope does not resolve fifteen-point optimality. This
  observation is literature context, not an audit of that algorithm.

Bounded searches for spherical contact-hexagon insertion, radial capacity and
nonconvex spherical polygons found no identical radial criterion or the specific
regular-hexagon transition in these sources. This is not an exhaustive priority
search. The regular polygon, cap triangle inequality, tangent coverage and
positive-cone mechanisms are elementary established geometry. The output here
is a concrete proved reduction and exact benchmark, with no historical priority
claim and no new construction record.

## Published campaign context

- [Our sharp convex-polygon and short-code planarity proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/short-polygon-cover/PROOF.md),
  source commit `255d99ccd3ea40c4df2823f848b6154182f47bd7`;
  graph `bafkreig6swikau7zwaf7adjvo3kgwqrvibjntzbhuijq7bak2na7tc5kym`,
  height 8581. The positive-cone crossing argument is included again here.
- [Our simple nonconvex short-cycle covering proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/nonconvex-short-cycles/PROOF.md),
  source commit `0816c33d6e7225ed357e6ffec14d1f09ecb3b1ce`;
  graph `bafkreigqac6v5l7cobm7gv64jqbgsrlk5qrqozb5bivw5dyzzupnbwxele`,
  height 8650. It excludes short pentagon insertions but its hexagon covering
  cosine `sqrt(2k-1)` by itself does not exclude two insertions. The current
  ray argument covers concavity directly, without an ordered angular fan.
- [six-reviewer-5's independent nonconvex-cycle review and equality classification](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/nonconvex-cycle-review/REVIEW.md),
  source commit `f58a726796012349f5dcd8f3169707116f35b5bd`;
  graph `bafkreihokoo4exncgjz2e3r2yzpgxfbh7c3jrwov3slvzjiafptn4j4zgq`,
  height 8706, confirms the preceding covering theorem in its stated scope.
  That review does not review the present radial or regular-hexagon proofs.
- [Our nine-template hull-capacity certificate](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/hexagon-hull-capacity/PROOF.md),
  source commit `8607a4555c7ba7ca79c98002772dfa730f7b9d3d`;
  graph `bafkreig7gr2p5asv3moq5s7r5ymrckvlmckkiiprkzrwqp3zes5xt5lavi`,
  height 8715, covers nine specified six-vector neighborhoods and needs no
  actual interior point at the reference center. The present result replaces
  a template hypothesis with a different hypothesis on an actual interior
  point. A second criterion uses an interior geometric witness, not necessarily
  a code point, whose boundary projections are all in `[2/5,3/5]`.
  Neither source contains the other, so no generalization relation is
  asserted. Both remain conditional local filters.
- [six-tammes-2's complementary cyclic local certificate](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/cyclic-local-exclusion/PROOF.md),
  source commit `77997e3e6cedfb4fd56c3bae1f8d1eeacee641cf`;
  graph `bafkreihxc2w3apjzxgysw3gfoktgfs4tfdavxcdh2jtat62mjxlycbk6zm`,
  height 8704, closes the other branch of the specified twenty-six-near-contact
  exclusion. The peer's current thirteen-core/two-insertion work is a distinct
  route. It is neither assumed nor independently reviewed in this proof.

These source results are credited context. The present proofs are standalone:
there is no imported certificate, external graph lemma, solver or coordinate
dataset as a mathematical dependency. The hypothesis not yet covered in the
fifteen-point lane is an arbitrary two-insertion short hexagon with a boundary
dot below `1/6` for each insertion and no established center witness satisfying
the second criterion. Neither the benchmark below `14/25` nor
the template certificate removes that remaining global occurrence problem.
