# Provenance

- Campaign: Hadwiger--Nelson, strict sub-509 record objective.
- Lane: researcher 3, exact globally coupled plane geometry.
- Frozen on: 2026-09-16 UTC.
- Selection: three independent centres at the exact symmetric separation
  `sqrt(2)`; all two-circle intersections and all owner-relative sixfold unit
  direction orbits; raw cap 75 fixed before querying colourability.
- Exact proposal arithmetic: Python `Fraction` in
  `Q(sqrt(2),sqrt(6))`.
- Exploratory positive-witness search: python-sat 1.9.dev15 with CaDiCaL
  1.9.5. Solver soundness is not part of the published proof boundary.
- Published checker: Python standard library only; it regenerates coordinates,
  reconstructs all physical edges, and checks literal positive witnesses.
- Related prior scoped stop:
  `hadwiger_nelson_three_sqrt3_lens_orbit_stop`, source commit
  `a164f99e6c49f8c3e336370897d3a363fef07751`.
- Structural context only:
  `hadwiger_nelson_open_dominating_triple_collar`, source commit
  `a30a9a1a88bc268d223a30f69c47ee858b72f2de`. The present result neither
  assumes nor strengthens that continuum theorem.
- Record status: no record improvement; exact scoped stop.

