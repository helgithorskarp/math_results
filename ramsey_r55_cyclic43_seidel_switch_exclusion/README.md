# Complete Seidel-switch exclusion for 238 Cyclic(43) boundary states

Every Seidel cut switch of every graph in the pinned 238-state Cyclic(43)
`A12` list contains a red or blue `K5`.  Thus none of these 238 complete
switching classes contains a good 43-vertex Ramsey `(5,5)` coloring.

This is a complete structured-family decision, not a good43 construction and
not an improvement to the bounds on `R(5,5)`.  It does not decide any of the
161 h3987 q10 survivors.  No claim is made that switching classes belonging to
different source indices are disjoint.

For each source the normalization `s_0=0` leaves exactly `2^42` distinct
labeled switches.  The certificate therefore covers 238 source-indexed
families, each of size 4,398,046,511,104.  Cyclic rotations of the sources are
covered because relabeling commutes with Seidel switching.

## Fast solver-free reproduction

Python 3.11 or later and the standard library suffice.  From the repository
root, use a fresh output path:

```bash
python3 -B ramsey_r55_cyclic43_seidel_switch_exclusion/reproduce.py \
  /tmp/r55-cyclic43-seidel-replay
```

Expected status:
`REPRODUCED_CYCLIC43_238_SEIDEL_CLASS_EXCLUSION`.

The replay checks both normal and assertion-disabled Python modes.  The
independent checker reads no generated full CNF.  It verifies that all 84,099
committed core clauses are literal physical monochromatic-five obstructions
for their named sources, then checks all 18,396 proof additions by repeated
unit propagation.  All 238 core formulas derive the empty clause.  On the
research host each full certificate replay took about 7.5 seconds.

Certificate hashes:

```text
8b6d3c4f982d406bf3657ce6400541f4d8f69b3127fc87ac0f2f94a4bcb5f640  cores.dimacs
69220ed88545b2546402e712f56f5dfa72dad9d1484e0a7211f4e92047e7d5ba  proofs.drat
```

See [PROOF.md](PROOF.md) for the reduction and [HANDOFF.md](HANDOFF.md) for
the exact terminal scope.

## Optional production replay

The committed compact cores and proofs are sufficient for the theorem.  To
reconstruct all full formulas and repeat the solver/proof-extraction run:

```bash
python3 -B ramsey_r55_cyclic43_seidel_switch_exclusion/decide_all.py \
  /tmp/r55-cyclic43-seidel-production \
  --kissat /path/to/kissat --drat-trim /path/to/drat-trim --jobs 12

mkdir /tmp/r55-cyclic43-seidel-collected
python3 -B ramsey_r55_cyclic43_seidel_switch_exclusion/collect.py \
  /tmp/r55-cyclic43-seidel-production \
  /tmp/r55-cyclic43-seidel-collected
```

The recorded production run generated and decided all 238 formulas in 153.52
wall seconds.  Their sizes ranged from 55,901 to 57,402 clauses.  Kissat 4.0.4
was invoked without a time limit using `--no-binary --no-factor`; every call
returned UNSAT.  DRAT-trim independently accepted every raw proof before the
collector admitted it.  Generated full formulas occupy about 247 MB and are
not committed.

## Trust and scope

The compact proof trusts Python integer, set, file, and SHA-256 semantics and
the published checker.  It does not trust the SAT solver or DRAT-trim.  The
fact that the pinned rows constitute the complete upstream `A12` list is an
imported boundary from the q13 certificate; the present result directly
checks the graphs named by all 238 rows.  It is not proof-assistant
formalization or an external independent review, and no historical-priority
claim is made.
