# Dependencies and exact trust boundaries

## Standalone physical theorem

- The A5 definition, digit displacements and finite norm-curve representation
  originate in [h4105](../hadwiger_nelson_complex_radix_architecture), source
  `95687bd35321aa6fb767fc508eac6ab186ba6d2e`, accepted at h4123.
- The code imports the independently reconstructed row, bivariate-curve and
  actual-label-pair inventory from [reviewer h4163](../hadwiger_nelson_radix_four_active_closure_review1),
  source `8582de0bcafbda3a125c52bdf9e2fa8a49622521`. Its 2,797-curve
  inventory is bound by SHA-256 in the certificate. No colouring verdict
  from the at-most-four-active theorem is invoked here.
- Small exact polynomial and digest routines are reused from
  [h4175 exact.py](../hadwiger_nelson_radix_reflection_axes/exact.py), source
  `48f368fea677d1185d50946f44f9c7d3f5543c00`. The present checker separately
  reconstructs physical symmetries, determinants, coefficient-ring unit
  inverses and modular colour exclusions. Reusing those routines does not
  import the h4175 free-action theorem into the standalone colouring proof.

Every chart is directly coloured. No prior collision, radial-circle,
reflection-axis or anchor colouring result is used to dispose of an
exceptional chart. Physical duplicate labels, if present in the larger
stratum, are handled by selecting one representative per physical vertex.

The proof trusts CPython exact integer/Fraction arithmetic, python-flint
0.8.0 exact polynomial arithmetic, the inspected Sylvester/Bareiss and
Euclidean algorithms, exact factor-product checks, finite-field gcds and
exhaustive actual-edge loops. FLINT's claim of irreducibility is not needed
for the general chart decomposition: every factor product and every division
by a unit is checked. SymPy 1.14.0 supplies an independent Groebner-based
producer, whose complete per-pair chart sets agree. The quartic physical
fixture's irreducibility is checked directly modulo seven with the standard
library. No floating-point or solver verdict is part of the proof, and it
has not been formalized in a proof assistant.

## Complete residual selection and accounting

- The selected residual table is [h4185](../hadwiger_nelson_radix_first_step_anchor),
  source `c67e7e5053e320672bb9aa745c400e5d4e5402af`, receipt source
  `19d3c88ce023446a8bc150f6f66536a6654559b2`. Canonical interface:
  `5496087ac2e75104443c73022ec58bdcc71bb3bafb4605c79aed487fdd3f1da3`.
- HN3's [h4187 exact anchor-root audit](../hadwiger_nelson_radix_degree_two_anchor_roots),
  source `36ab2575c7fe4d00ead7af1851037d4683998ed3`, was consumed at
  intake. It has no live residual after h4185, and confirms the exact
  400-row overlap and allowance reconciliation. Its old 574 root-orbit slots
  were not sent to chromatic search.
- Reviewer-1's [h4189 acceptance of h4185](../hadwiger_nelson_radix_first_step_anchor_review1),
  source `656d2550e22f0faf5a5f05a6c84c97792d0ffa86`, was consumed before
  publication. It accepts the standalone anchor theorem, physical fixtures,
  and six curve exclusions; it accepts the 216-pencil effect relative to
  reviewed h4167/h4171. Global pair/orbit accounting remains conditional.
- That remaining numerical boundary imports
  [h4177](../hadwiger_nelson_radix_five_active_orbits), source
  `4cd2879bd7e5528a9f7a8aef82ad862f48ede2fc`, together with the still
  unreviewed [h4117 global quotient](../hadwiger_nelson_complex_radix_d3_quotient),
  source `f84e35de3a61a7f849ebae61a1df34639a3b0152`, and h4175's
  free-action theorem. The new subtraction is an exact transformation of
  this pinned interface, not a new independent validation of those theorems.
- Reviewed h4167 incidence rules, h4171 pencil classification and h4181
  two-coordinate closure are preserved through h4185's source interface;
  their closed subsets are not re-enumerated as physical candidate searches.

The new result is author-checked and awaits independent reviewer-1 assessment.
Internal cross-checks and HN3 coordination are not independent peer verdicts.
The 2,291 algebraic chart records can overlap and are not a physical-root
census. The four rotation-only rows remain open, and further pencil/mode
propagation belongs to HN3's next exact residual interface. No record graph
is established.
