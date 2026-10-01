# Release validation — 2026-10-01

Actual author/checker: **six-vdw-2**, researcher. Every check below is
same-author evidence; no independent peer verdict is claimed.

The fresh release-source run finished successfully in 154.723s with:

- Both complete semantic audits, normal and optimized Python.
- All46 checked refutations, each replayed normal and optimized.
- All46 reference CNF hashes and all46 reference LRAT hashes matching.
- 165171 positive-RUP additions and2056956 checked propagation hints
  per complete replay; no unsupported RAT used.
- Parent peak56172KiB and child peak72608KiB (about71MiB).

The completed-run `--resume` branch finished in 98.894s. It re-generated
and compared every model, repeated both semantic audits, validated
completed source/input/trace/conversion hashes, and repeated every strict
proof replay in both Python modes. All46 proof byte hashes still matched.
Resume reused completed native/conversion stages; it did not treat an
earlier progress status as proof. Parent/child peaks54508/64324KiB.

Two deliberate changed-source controls appended text to a scratch copy
of the pinned helper `encode.py`. Both normal and optimized Python
rejected the dependency before creating a model or calling native tools.
Explicit guards remain active under `-O`.

The literal definition auditor covers617*616=380072 ordered field
pairs,375760 retained APs,4312 excluded APs through zero,26488
identical unfolded signed supports, both QR controls,24224 exhaustive
small full-word arc normalizations and924 boundary phase normalizations.
Its alternate deficit enumeration produces126 rooted tuples and22
orbits:20 full44-orbits and two22-orbits,924 phase patterns per endpoint.
All entire clause multisets, dimensions and units are compared.

Initial prototypes independently finished both36-arc refutations in
34.640s and the44 boundary refutations in92.276s. The two hardest arc
proposals used43666/48909 conflicts; the hardest boundary used1898.
Fresh published-source reproduction matched every prototype byte hash.

## Limits and incomplete broader probe

All native mathematical jobs ran serially with one thread. The
standing1CPU/2GiB process scope was unchanged. Native proposals had
a50000-conflict cap and30s external timeout; conversion had25s
internal/30s external limits. No setting was escalated. Each complete
semantic audit had a55s deadline; it completed before any native proposal.
Timeout/UNKNOWN/unchecked native status is not a mathematical exclusion.

A separately audited width43 model for each background covers every
mixed phase through a transition anchor. Both bounded proposals returned
UNKNOWN at50001 API-reported conflicts (one-conflict overshoot of the
requested cap). They finished together in17.600s, peak80688KiB.
They establish no exclusion or witness and are not among the46 certified
instances. The full H7 family remains open. No larger resource request or
identical-instance retry was made.

Earlier width8/12/22 arc prototypes were certified, but their weaker
run bounds are subsumed by the36-arc result. Their corpora and exploratory
code are not published here. The compact release contains exact source,
pins and expected hashes, not bulky proof files or raw logs.
