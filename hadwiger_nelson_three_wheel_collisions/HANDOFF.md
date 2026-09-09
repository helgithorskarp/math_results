# Closed interface: coincident labels in the three-wheel architecture

HN-2 has completed the physical collision branch of the
[h4065 interface](../hadwiger_nelson_three_wheel_architecture/HANDOFF.md).
Every noninjective `W+uW+vW` is now proved four-colourable. Outside alignment
there are exactly four congruence classes and 864 ordered parameter pairs;
their chromatic numbers are 4,3,4,3, with compact checked physical witnesses.

The final refresh consumed HN-3's completed
[h4071 symmetry quotient](../hadwiger_nelson_three_wheel_symmetry_frontier/HANDOFF.md),
source commit `91c3237c5c8200a4a4a0d8d194d5d1e6a023f59c`, with its four exact
collision representatives. `bridge.py` proves they are exactly our physical
representatives in a different coordinate encoding. Thus this supplies the
physical decision requested by that handoff; the four types were reached
independently during overlapping passes.

For the shared next exact viability interface:

- Remove all collision roots as possible non-four-colourable candidates.
  No collision-row root isolation or deduplication remains necessary.
- Keep the injective thirteen-failure product equations, now using h4071's
  **800 representative factor pairs**. The remaining whole-architecture
  bound is **5,110 physical classes**, or the older 902,481 ordered-pair bound.
  The joint Cayley field degree remains at most 16.
- Every surviving physical candidate must have exactly 343 distinct points.
  Any proposed survivor with fewer points is covered by this result.

This is a complete physical decision of one architecture branch. It does not
solve the injective intersection frontier, provide a new source, or invite
parallel candidate SAT searches. The concrete next support need is certified
real-root viability and simultaneous thirteen-failure filtering of the 800
systems, with canonical exact fields for survivors; a reusable obstruction
reducing this full frontier is also useful. HN-3's exact-frontier role and
HN-2's physical reconstruction and chromatic candidate ownership remain
complementary. The preceding h4051/h4055 architecture
obstructions and HN-3's h4061 five-module result remain preserved.

An exact independent check of this reduction is welcome as a bounded
interface check, but an internal check does not replace reviewer-1's verdict.
The next phase begins only after checkpointing this completed physical unit.
