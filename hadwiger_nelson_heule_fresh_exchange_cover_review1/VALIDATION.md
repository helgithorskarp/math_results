# Validation record

- Verdict: **ACCEPT with high confidence**, strengthened from order 508 to
  order 509 inside the same two fixed parents.
- Target mathematical commit: `c89c29f27418bd932b2d8e79e7ff728894dbf7ca`.
- Target normal and optimized exact verifiers: PASS and byte-identical.
- Target controls: three malformed cases rejected.
- Target manifest: PASS.
- Independent normal and optimized replays: PASS and byte-identical.
- Independent output SHA-256:
  `9916c957583e31914f6bc2b150d311edaea3164e53f92f4d1058fb639e03870e`.
- Geometry: 129,795 old pairs and 261,121 parent pairs, with two exact metrics
  agreeing entrywise; 510/2,504, 511/2,510 and 512/2,518 vertex/edge censuses.
- Colour witnesses: 1,020 old-singleton-deletion words and 2,554,245 retained
  edge inequalities checked.
- Negative controls: one damaged word per parent rejected; no noncanonical
  packed words accepted.
- Environment: CPython 3.11.2, standard library only.

Limitations: these are two fixed physical supports, not a family of all fresh
centres or a global geometric theorem. The result is an exclusion and produces
no five-chromatic graph or record improvement. Historical discovery
completeness and H510 non-four-colourability are outside the proof premises.
