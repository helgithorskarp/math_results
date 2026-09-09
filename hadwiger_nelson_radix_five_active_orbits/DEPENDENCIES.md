# Dependencies and trust boundary

This result composes the following durable A5 results.

- h4105: finite exact complex-radix curve frontier and irreducible event
  factors.
- h4117: complete global `D3` pair quotient. Representatives are global and
  cannot be combined with a chamber restriction.
- h4119: collision parameters, including the nonidentity-rotation fixed point
  `z=0`, are three-colourable; independently accepted at h4141.
- h4139: exact three-colour closure of the unit-circle branch.
- h4165: all 960,768 four-section cover quartets are nonconcurrent.
- h4173: reviewer-1 independently accepted h4165 and supplied the sharp
  product-surface bidegree interpretation used here.
- h4167: exact lower-arity incidence exclusions leaving 131,356 pair systems.
- h4169: reviewer-1 independently accepted h4167.
- h4171: exact five-active affine-pencil classification and mode interface.
- h4175: exact three-colour closure of all reflection axes and the resulting
  free `D3` action on every possible non-four parameter.

The checked repository inputs are

```text
hadwiger_nelson_radix_five_active_pencil/certificate.json
  SHA-256 3a02e1e277ca418103d5b0e70a12b4bc7eb4f09b36a0caba6750f4f03973f539
hadwiger_nelson_radix_reflection_axes/FRONTIER_EFFECT.json
  SHA-256 25f403d9fad918f05ed5ce46ce06cbc619ad0c61e6365c1db869821528b251c2
hadwiger_nelson_radix_reflection_axes/certificate.json
  SHA-256 c0d850b8649de4460af8caa8f74982e131d8492b0e35bc8479f81826c5245b7b
```

The present producer/verifier are author-side exact checks. The new
mode-specific composition has not yet received an independent reviewer
verdict. It inherits the truth of h4171 and h4175 rather than re-proving their
physical conclusions.

The generated 2,331,829-byte row interface is omitted from Git and regenerated
from source. No SAT/LRAT archive, raw root census, graph candidate, or physical
chromatic certificate is part of this package.
