# Review verdict and limitations

## Explicit verdict

`ACCEPT_AND_STRENGTHEN_EI19_FIRST_LENS_FOUR_COLOUR_STOP`

The target's principal theorem is supported: for the pinned isolated EI19
realization, adjoining both intersections of the unit circles around every
source pair at distance below two yields a physical plane unit-distance graph
of chromatic number exactly four. The proof is robust to formal-label
collisions and to unanticipated unit contacts.

The review strengthens the result by certifying physical order in `[247,349]`
and proving that the EI19 source is vertex-critical four-chromatic.

## Checks passed

- Public source and target integrity: twelve SHA-256 pins.
- Exact geometric realization: rational contraction and self-map bounds.
- Complete source geometry: 19 distinct points, exactly 35 unit edges.
- Lens eligibility: all 171 source pairs resolved, 165 included and 6
  excluded.
- Enclosure independence: rational endpoints with a new `2^192` square-root
  grid, importing no target executable.
- Chromatic upper bound: all 60,726 formal pairs checked with collision-safe
  conditions.
- Chromatic lower bound: complete three-colour exhaustion of the source.
- Criticality: 19 positive deletion witnesses independently generated and
  checked.
- Physical-order lower bound: all rectangle overlaps and components checked.
- Adversarial controls: eight malformed inputs rejected; square-root and
  interval containment fixtures passed.
- Runtime mode: normal and optimized outputs byte-identical.

## Limitations

- The exact physical vertex count is not proved. The certified statement is
  `247 <= |V_physical| <= 349`; overlaps within a component need not be exact
  collisions.
- Only one isolated EI19 root and one lens-closure round are covered.
- No claim is made about second or later closure rounds, other EI19
  realizations, or arbitrary graphs generated from EI19.
- Vertex-criticality is proved for the 19-vertex source, not for the physical
  closure. Edge-criticality is not claimed.
- This is a four-chromatic construction and a restricted construction-family
  stop, not a five-chromatic record, a global lower bound, or a global
  exclusion below 509 vertices.
- The proof is computer-assisted. Its residual trust assumptions are exact
  CPython integer/Fraction semantics, the elementary interval and contraction
  arguments documented here, SHA-256 collision resistance, and correct
  hardware execution.

