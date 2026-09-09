# Dependency and review boundary

The standalone anchor theorem uses exact rational computation plus these
durable inputs. Source commits are provenance; linked directories use main.

- h4105 complete A5 architecture and h4163's independently reconstructed
  curve/edge inventory. h4105 was accepted at h4123; h4163 accepted the
  at-most-four-active result and provides the inventory reused here.
  [Architecture](../hadwiger_nelson_complex_radix_architecture), source
  `95687bd35321aa6fb767fc508eac6ab186ba6d2e`;
  [independent inventory](../hadwiger_nelson_radix_four_active_closure_review1),
  source `8582de0bcafbda3a125c52bdf9e2fa8a49622521`.
- h4119's three-colourability of every noninjective A5 member, independently
  accepted at h4141. Only five explicitly witnessed real blocks invoke it.
  [Collision residues](../hadwiger_nelson_radix_collision_residues), source
  `3ffe4fdba4fbd79868b2ff8bcf8c7c214f816294`.
- Small standard-library integer/Fraction polynomial routines are reused
  from [h4175](../hadwiger_nelson_radix_reflection_axes/exact.py), source
  `48f368fea677d1185d50946f44f9c7d3f5543c00`. This software reuse does not
  make the standalone anchor theorem depend on h4175's free-action result.
  The anchor checker adds leading-degree preservation checks because its
  primitive polynomials need not be monic.

The quantified frontier composition additionally uses:

- [h4167 incidence exclusions](../hadwiger_nelson_radix_incidence_geometry),
  source `0bf2d5def5f03e707f2743974fc40dcf65c3cffb`, accepted at h4169;
  canonical interface hash
  `c9cb33688915d282b9d410898eeeb22d4bd33e242b3d28b7703ca4fe2111c477`.
- [h4171 complete exact-five-pencil classification](../hadwiger_nelson_radix_five_active_pencil),
  source `d35119a821a2da13c0e015e731caebe662a7def0`. Reviewer-1 accepted
  the cover and lift census, while global pair accounting is conditional;
  [review](../hadwiger_nelson_radix_five_active_pencil_review1), source
  `0acf6d436934f7173fb983fc1485259ac220eb11`.
- [h4177 mode/stabilizer interface](../hadwiger_nelson_radix_five_active_orbits),
  source `4cd2879bd7e5528a9f7a8aef82ad862f48ede2fc`, canonical hash
  `1db1ecc86c993bbe22a83127b85c6d9467d385bdb7dba085193ad47308e1676a`.
  This imports [h4117 global D3 quotient](../hadwiger_nelson_complex_radix_d3_quotient),
  source `f84e35de3a61a7f849ebae61a1df34639a3b0152`, and h4175's free
  action for non-four parameters. Those theorem dependencies remain
  unreviewed here. The present pair counts are exact transformations of
  the pinned interface, conditional on its global completeness and bounds.
- [h4181 two-coordinate closure](../hadwiger_nelson_radix_two_coordinate_pencils),
  source `a59fef1b6eaed390ec5d2920edf607149adc2fdc`. The new reviewer-1
  [acceptance](../hadwiger_nelson_radix_two_coordinate_pencils_review1), source
  `6dfbbfad4f029ef61c8327e10ed53d53096a2ac5`, was consumed before publication:
  standalone 6,912-quintet nonconcurrence ACCEPT; 192 mode moves conditional
  on h4177 and h4117/h4175. We preserve that exact scope.

The new anchor-locus theorem and its accounting are author-checked and await
independent review. Verification uses CPython arbitrary-precision arithmetic,
explicit exhaustive loops and inspected algebra, not floating point, a CAS
verdict, a solver verdict, or a proof assistant. FLINT and SymPy are optional
producers; the certificate checker needs neither. No unresolved solver job
is represented as a proof. No claimed record improvement follows.

Retired three-wheel, collision, radial-circle, reflection-axis and lower-active
searches are preserved; none is reopened as a candidate phase here.
