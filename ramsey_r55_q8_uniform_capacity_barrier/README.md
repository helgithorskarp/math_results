# Failed q8 fractional capacity mechanism

The proposed mixed common-neighborhood capacity test cannot exclude any of
the 2,185,424 original q8 tasks. For every eleven-vertex Ramsey(4,4) core,
the assignment **x_S=1/64 to each of its 2048 signatures** has total mass 32
and satisfies every constraint in the declared system. This is a feasible
fractional point, not a graph or a physical task verdict.

[PROOF.md](PROOF.md) specifies the system and proves this uniformly over all
valid cores, including the core vertices already occupying each common
neighborhood. It also rules out any exclusion obtained by nonnegative
weighted combinations of these same capacity inequalities. It does not rule
out stronger signature systems with extra constraints.

The first gate was whether this exact mechanism could give a checked capacity
below the 32 outside vertices required by a q8 task. The universal point
disproves that possibility. This pass therefore ends at the declared failure
boundary; no catalog-wide LP, target solver or neighboring refinement was run.

## Reproduce the checks

Use Python 3.10 or later, with only its standard library, from the repository root:

```sh
python3 -B ramsey_r55_q8_uniform_capacity_barrier/verify.py \
  --expected ramsey_r55_q8_uniform_capacity_barrier/EXPECTED.json
```

Expected status: `VERIFIED_UNIFORM_FRACTIONAL_CAPACITY_BARRIER`.

The checker enumerates the 2048 signatures for each of the 15 size classes,
checks the bounds with exact rational and integer arithmetic, and checks
literal core occupants on all labeled graphs of orders four and five with
neither monochromatic K4. The controls cover 62 and 892 valid small cores
and 78,464 mixed clique pairs. These are controls for the general proof;
they are neither a sweep of the eleven-vertex catalog nor physical q8 tasks.

The standard small Ramsey upper bounds are imported as recorded in
[SOURCES.json](SOURCES.json). The general proof is an ordinary mathematical
argument, not a formal proof or reviewer-1's independent verdict. No novelty
claim is made for uniform measures or linear programming duality.

## Task and campaign outcome

There are **zero new original-task exclusions and zero candidates**. All
2,185,424 original q8 tasks remain undecided; the global original registry
remains 518 excluded and 2,188,660 undecided. No certified good43 is supplied.
The active dispatch is unchanged, and the q10 children owned by team-r55-1
were not accessed.

The exact mechanism is parked. Its outcome gives no authorization to add
degree constraints, cell interactions, integrality or a nearby mechanism in
the same pass. Earlier frozen routes and construction endpoints are untouched.
No Discovery Net mathematical contribution is submitted for this failed
task-leverage gate; source and compact evidence are preserved here.

The original task interpretation comes from
[the complete maximal-packing cover](../ramsey_r55_global_maximal_packing).
Earlier exceptional-degree signature systems have additional hypotheses and
are outside this no-go statement, as detailed in the proof and source record.
