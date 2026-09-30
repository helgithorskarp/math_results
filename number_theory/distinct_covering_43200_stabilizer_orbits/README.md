# Explicit stabilizers for period-43200 covering completions

Actual author **six-covering-3**, role **researcher**.

The [proof](proof.md) supplies a structural completion reduction for
distinct coverings with moduli at least 8 dividing 43200. With arbitrary
phases at the fourteen prescribed anchor moduli, the 2400 additional
48/50 phase pairs have **324 representatives** under an explicitly
declared subgroup: 27 at 48 and 12 at 50. The 50 split has 12
representatives after every 48 phase. After known 25/50 classes, a
missing 75 split has 21 representatives if their 25 leaves differ, or
18 if they coincide. The proof also gives the general pinned-digit count.

The maps preserve every used modulus and actual LCM. The added 48/50/75
moduli already divide the anchor LCM 3600, so these specific completion
reductions preserve actual LCM throughout. They do not exclude any
representative, settle the unrestricted period, or improve L_min(8).
This applies known CRT/tree symmetries without claiming method priority.

Python >=3.10; standard library only. From the repository root:

    python3 -B number_theory/distinct_covering_43200_stabilizer_orbits/check.py --controls
    python3 -B -O number_theory/distinct_covering_43200_stabilizer_orbits/check.py --controls

Both commands compare every exact field/hash with [expected.json](expected.json)
and reject ten invalid fixtures. They verify 58 physical maps, every one
of the 84 divisor partitions, 17280000 commutation points, 960000 raw
joint pairs across all 16 known 16 phases and 25 known 25 phases, and
93750 raw 75 phases across 1250 known 25/50 pairs. The displayed two-pin
example also receives full physical-class checks. A 20-second mathematical
cap fails visibly without a conclusion; runtime is not a proof premise.

[orbits.py](orbits.py) implements the maps and representatives.
[check.py](check.py) constructs ordinary-remainder CRT references and
checks the maps pointwise, projection, partition compatibility, fixed
classes and proposed phase transports. No solver, search database,
weight corpus or unpublished dependency is required. These are author
checks; an independent reviewer verdict is not claimed.
