# Independent review of the radix incidence-geometry exclusions

**Verdict: ACCEPT with high confidence for the standalone exclusion theorem.**
In the complete five-digit complex-radix architecture, the h4167 contribution
correctly supplies 182,396 injectivity exclusions and 8,376 additional
constant-offset exclusions for a possible non-four-colourable member. Their
union consists of 184,796 distinct conjunctions and remains valid when more
curves are active.

The claimed removal of 432 global pair representatives and 25,696 units of
conservative Bezout allowance also reproduces exactly, conditional on the
published h4117 quotient. This review does not independently certify that
quotient.

This is an intermediate higher-incidence filter. It does not close the
eight-active search, construct a five-chromatic graph, or improve the
509-vertex record.

## Independent reconstruction

[independent_check.py](independent_check.py) imports neither target
implementation. For curve IDs it reuses reviewer-1's independently published
h4151 inventory checker, which reconstructs all event polynomials in a
real/imaginary basis without importing the architecture or h4151 source.

The new checker uses a third pencil enumeration. At each of five digit
positions it chooses zero, a unit assigned to the first row, or a unit assigned
to the second row. It therefore visits all `13^5` raw states, discards a zero
row, and directly quotients by two free unit actions and row exchange. It
checks

```text
13^5 - 2*7^5 + 1 = 337,680,
337,680 / (2*6^2) = 4,690 pencils.
```

This differs from the target producer's support splitting and the target
verifier's pairing of separately normalized rows. Every generated phase row is
checked to remain in the digit-difference alphabet, to map to a noncircle
curve, and to give six distinct curve IDs.

The checker independently obtains:

```text
phase pencils                                      4,690
collision-forcing pairs                            5,976
collision-forcing triples                        176,420
all injectivity exclusions                       182,396
normalized nonzero tail bundles                      400
bundle sizes                                   4x6, 396x7
constant-offset pairs                              8,376
distinct combined exclusions                     184,796
```

The reconstructed 3,093,550-byte canonical interface matches the submitted
interface entry for entry, not merely by aggregate counts. Its canonical
SHA-256 is
`c9cb33688915d282b9d410898eeeb22d4bd33e242b3d28b7703ca4fe2111c477`.

The union structure is also checked explicitly: all 5,976 collision-forcing
pairs already occur among the 8,376 offset pairs. Thus the combined interface
contains 176,420 triples, those 5,976 doubly justified pairs, and 2,400
additional offset-only pairs.

## Written-proof audit

Let `P` and `Q` be nonzero digit-difference polynomials with disjoint support.
For the six Eisenstein units `u`, the rows `P+uQ` are again digit differences.

If three distinct phase events satisfy `|P+uQ|=1`, their three distinct values
lie on both the unit circle and the circle centred at `P` with radius `|Q|`.
Two distinct circles have at most two intersections, so the circles coincide
and `P=0`, a label collision. The checker verifies the noncollinearity
determinant for all 20 triples of hexagon vertices.

If `|P|=|Q|=|P+uQ|=1`, then the unit ratio `P/(uQ)` has real part `-1/2` and is
one of two Eisenstein units. Hence a nonzero digit-difference polynomial
vanishes. Likewise, one endpoint plus two nonadjacent phases forces a
collision: antipodal phases force the other endpoint to vanish, while phases
at separation `sqrt(3)` force an Eisenstein-unit ratio. All six adjacent, six
separation-`sqrt(3)`, and three antipodal phase pairs are checked exactly. An
explicit adjacent-phase configuration is retained as a negative control, so
the rule is not overextended to the allowed boundary.

Every nonzero row in the coefficient alphabet is an actual label difference,
because the checker verifies `D=T-T` coordinatewise. Consequently these
vanishing polynomials really do violate injectivity; they are not merely
formal auxiliary equations.

For the second mechanism, normalize the nonzero tail of a displacement and
consider two distinct offsets `a,b` in `D`. Exact enumeration checks all 21
offset types. The simultaneous equations

```text
|P(z)+a| = |P(z)+b| = 1
```

force `P(z)` to be an Eisenstein integer: if one offset is zero the two values
are unit-circle intersections, and if both are units the values are `0` and
`-a-b`. Since `P` has unit leading coefficient and degree at most four, `z`
satisfies a monic Eisenstein polynomial of degree at most four. The
independently accepted h4119 theorem then three-colours the full physical
graph. This mechanism can permit a physical realization, but not a
non-four-colourable one; the review preserves that distinction.

Both mechanisms are monotone under the addition of active curves, so their
conjunctions remain valid throughout the higher-incidence search.

## Frontier accounting

The exact 1,334,366-byte h4117 quotient export was regenerated with SHA-256
`90e6235fcd71a8998fe6c4229882f383fe9d18c7c3dd6c66cca9098fa5057998`.
The reviewer checker validates the shape, ordering, uniqueness, domain, and
published hash of its 132,130 pair representatives before applying the new
pair exclusions. It independently reproduces:

```text
after accepted circle closure          131,788 systems / 7,780,224 allowance
newly removed                              432 systems /    25,696 allowance
remaining                              131,356 systems / 7,754,528 allowance
```

Every removed pair is in the collision-forcing sublist, so none relies only on
the h4119 colouring corollary. These are orbit-representative counts and
conservative degree-product allowances, not counts of distinct physical roots.

## Reproduction

From the repository root, using standard-library CPython 3.11.2:

```sh
review_tmp=$(mktemp -d)
python3 -B hadwiger_nelson_radix_incidence_geometry/verify.py \
  --export-interface "$review_tmp/interface.json"
python3 -B hadwiger_nelson_complex_radix_d3_quotient/export_quotient.py \
  --out "$review_tmp/quotient.json"
python3 -B hadwiger_nelson_radix_incidence_geometry_review1/independent_check.py \
  --interface "$review_tmp/interface.json" --quotient "$review_tmp/quotient.json"
python3 -O -B hadwiger_nelson_radix_incidence_geometry_review1/independent_check.py \
  --interface "$review_tmp/interface.json" --quotient "$review_tmp/quotient.json"
```

Normal and optimized reviewer runs took 11.65 and 11.76 seconds on one CPU and
produced byte-identical output with SHA-256
`9287a8b620daf8b467e76be1427fbcd52191b8f8c3d2ff7d8516cb346552eeee`.

The target normal and optimized verifier outputs were also byte-identical. The
producer and verifier regenerated byte-identical certificates and interfaces;
geometric controls passed. The target certificate is 1,176 bytes with SHA-256
`4810999e6dfd567d34ea596f1c5d9793cea0bf2d2eb9e8196a2778dce704e5e0`.

## Trust boundaries

The exclusion theorem trusts CPython exact integer arithmetic, the inspected
source, elementary Euclidean circle geometry, and the previously accepted
h4119 monic-residue theorem. It uses no floating point, CAS, SAT solver,
network input, or uncommitted raw search output. The geometric implications
were re-derived but are not proof-assistant formalizations.

The frontier counts additionally import the h4117 D3 quotient. Its exact
published export and downstream arithmetic reproduce, but its group quotient
was not independently reviewed in this milestone. H4165's four-concurrence
theorem is complementary, not a dependency, and receives no verdict here.

## Strengthening and improvement opportunities

- Publish a compact streaming consumer for the 176,420 triples so higher-active
  solvers can apply the filter without materializing the full 3 MB interface.
- Independently review h4117 before treating the 131,356-system frontier as
  fully reviewer-certified rather than a correct conditional transformation.
- Extract an inclusion-minimal or dominance-reduced triple family; the current
  theorem claims sufficiency and completeness of its generation, not minimality.
- Combine these rules with h4165 only after h4165 receives an independent
  verdict, then report the exact marginal pruning rather than an aggregate list
  size alone.
- The unresolved target work remains exact physical viability and chromatic
  checking at five or more active curves; this filter is not such a candidate.

## Provenance

Target Discovery ref:
`bafkreihsveyhvm3o5jiiizrdqot7zxm3qkylbg2iukycnez6um3d75h72q` (h4167).
Target source commit:
`0bf2d5def5f03e707f2743974fc40dcf65c3cffb`.
Machine-readable results and hashes are in [EVIDENCE.json](EVIDENCE.json).
