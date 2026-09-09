# Dependencies and trust boundary

This result composes the following durable `A5(z)` results.

- h4105: finite exact complex-radix curve frontier and irreducible event
  factors.
- h4117: complete global `D3` pair quotient. Its representatives cannot be
  combined with another chamber restriction.
- h4119: collision parameters, including the nonidentity-rotation fixed point
  `z=0`, are three-colourable; independently accepted at h4141.
- h4139: exact three-colour closure of the radial unit-circle branch.
- h4165/h4173: exact four-section nonconcurrence and independent acceptance.
- h4167/h4169: exact lower-arity incidence exclusions and independent
  acceptance, leaving 131,356 global pair systems.
- h4171/h4179: five-active affine-pencil classification and independent
  acceptance of its cover/lift census (with its stated conditional boundary
  for derived pair counts).
- h4175: exact reflection-axis closure and the free `D3` action away from the
  accepted closed loci.
- h4177: global exact-five pair/stabilizer interface and product-surface orbit
  allowance.
- h4181: complete two-coordinate-pencil exclusion, moving 192 h4177 pairs to
  the at-least-six branch and leaving 128,424 exact-five pairs.
- h4185: complete three-colour closure of the six first-step anchor circles,
  published during the final verification of this root census. Its 400
  exact-five removals are independently matched row for row here; its
  colouring theorem is imported rather than rechecked.

The checked repository inputs bound into `certificate.json` are:

```text
hadwiger_nelson_radix_five_active_orbits/certificate.json
  SHA-256 9ce28be5f8a71a19fc84ec447ae43e2d55361cc0e4c0a419771c9f700f9b0fbd
hadwiger_nelson_radix_two_coordinate_pencils/FRONTIER_EFFECT.json
  SHA-256 36335d3bf6bbfae797b7d386e759119baf65a2291065410a777573f78ee1c0a0
reconstructed curve inventory, canonical JSON
  SHA-256 85c286422c01bcb6ebb244186032bc607984471bc2b705ef7247084dd7c33db9
```

The verifier regenerates h4177 through its independent standard-library
checker and reconstructs all 2,400 collision rows through reviewer-1's
independent inventory implementation. It imports the predecessor results'
finite enumerations and physical closure theorems rather than re-proving
them.

The new root census has two exact implementations but is author-side evidence
pending independent reviewer assessment. The generated 232,908-byte interface
is omitted from Git and regenerated from source. No SAT/LRAT archive, graph
candidate, physical chromatic certificate, or record claim is part of this
package.
