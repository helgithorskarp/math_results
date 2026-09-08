# Propagation-complete degree strata for every prescribed good43 K4

Every monochromatic `K_4` in a hypothetical good43 has at least **22**
same-color contacts among its 39 outside vertices. More generally, if the
minimum degree in that color is at least `d`, it has at least `2d-14`
contacts. For `d=18,...,24`, the contact floors are

```text
22, 24, 26, 28, 30, 32, 34.
```

The [proof](PROOF.md) couples four attachment-signature capacities with the
degree incidences of the K4. It is strictly stronger on these cuts than the
h3899 contact floor 19 and the h3909 connectivity floor `d`. The underlying
K4-side argument occurs in h3657 and was independently accepted at h3667;
the degree-stratified application to every h3887 physical block is the new
construction interface here.

The exact CNF layer adds red-degree threshold counters for all 43 vertices,
enforces both-color degree window 18 through 24, defines global minimum-degree
guards in both colors, and reuses h3899's noncontact counters. It applies to
all 18 macro classes and all 2,189,178 h3887 tasks. Its added clauses have
maximum width three and all auxiliaries are uniquely determined.

For the frozen triangle instance `bo1-q7-r7-c000000`, the complete formula
has 43,622 variables, 1,051,035 clauses, maximum width eight, 37,840,460
bytes, and SHA-256
`73745bbae36bb9959fa5dc5ae2495a13598ed202a2db61186dfa144d6dded0bf`.
The first 923,269 clauses are the exact h3899 formula. The new suffix has
32,754 variables and 127,766 clauses.

## Reproduction

With CPython 3.11.2 and the standard library, populate a cache with the four
pinned h3873 graph6 inputs and run from the repository root:

```sh
python3 -B ramsey_r55_global_maximal_packing/catalog.py /tmp/k4-degree-data --download
python3 -B ramsey_r55_k4_degree_stratifier/reproduce.py /tmp/k4-degree-data
```

This regenerates the formula and audits all 1,051,035 clauses under normal
and optimized Python. It also rederives every signature population, generic
macro-class dimension, gate truth table, and unit-propagation control. It
runs no SAT solver.

To write one formula directly:

```sh
python3 -B ramsey_r55_k4_degree_stratifier/stratify.py \
  /tmp/k4-degree-data --task bo1-q7-r7-c000000 --triangles \
  --cnf /tmp/bo1-q7-r7-degree.cnf
```

The exact physical decoder accepts only a complete satisfying assignment and
then invokes h3899's full formula check, carrier decoder, and independent
five-set target verifier. No assignment or solver result is supplied here.

[SIGNAL.json](SIGNAL.json) records an exact per-block contact projection and
the earlier propagation boundaries. The unconditional interface conflicts
after 18 fixed noncontacts instead of h3899's 21, and 17 fixed noncontacts
force all 22 remaining vertices to contact the K4. These are exact
propagation facts, not a solver-runtime or task-count estimate.

No good43, task exclusion, or Ramsey lower-bound improvement is established.
The h3899 propagation interface remains externally unreviewed. The h3657
separator theorem is accepted at h3667, and the h3909 connectivity theorem is
accepted at h3917.
