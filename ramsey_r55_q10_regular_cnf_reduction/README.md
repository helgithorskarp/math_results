# Checked reduction of the frozen q10 regular decision inventory

Two actual frozen formulas, `d18-24.cnf` and `d24-18.cnf`, are certified UNSAT
by checking their physical meaning and applying the complete h3959 theorem.
The four final even-regular q10 jobs reduce to two unresolved files:
`d20-22.cnf` and `d22-20.cnf`. No new solver run occurs.

See [PROOF.md](PROOF.md) for the implication, [REDUCTION.json](REDUCTION.json)
for the machine-readable residual inventory, and [HANDOFF.md](HANDOFF.md) for
receiver instructions. Historical solver outcomes are preserved separately in
[HISTORICAL_RESULT.json](HISTORICAL_RESULT.json).

## Reproduce from public source

Use CPython 3.11 (tested with 3.11.2), standard library only, from a checkout
containing this package and its sibling dependencies. Supply the complete
16,913,568-byte McKay catalog `r45_24.g6`, available at
https://users.cecs.anu.edu.au/~bdm/data/r45_24.g6 . Required SHA256:
`83ca4028f206b2fa4315ef219b8c2c57c7835209673dd8183d8fb4353bd4fdd0`.

```
python3 -B ramsey_r55_q10_regular_cnf_reduction/reproduce.py \
  --catalog /absolute/path/r45_24.g6 \
  --rebuild /absolute/path/empty-rebuild-directory
```

The output directory must be empty. This reconstructs the old base plus four
CNFs (about 471 MB), checks their exact pinned bytes, audits normal and `-O`
executions, runs corruption controls, replays the complete h3959 certificate,
and checks the residual manifest. Generated CNFs and the full catalog are not
stored in Git. The included 12-byte `r44_3.g6` is the original pinned three-vertex
core catalog; no other core catalogs are needed for reconstruction.

If all four historical CNFs are already available, replace `--rebuild` with
`--branches /absolute/path/to/branches`. The full logical audit and h3959 replay
still run; reconstruction alone is skipped.

Expected status:
`CERTIFIED_TWO_OF_FOUR_FROZEN_Q10_REGULAR_CNFS_UNSAT`, with remaining unknown
branches `d20-22`, `d22-20` and `new_solver_calls: 0`.

The stand-alone `audit.py --branches DIR` verifies the literal implication
only. An implication audit by itself is not the h3959 theorem replay or the
complete UNSAT certificate chain.

## Evidence and scope

The independent auditor reconstructs required clauses from their five-vertex
supports and checks all 962,598 five-sets. It verifies 32,250 exact counter gates
and 504 guard gates by exhaustive truth tables. It neither imports the encoder
nor relies on historical symmetry/cut correctness for its UNSAT implication.
`frozen_encoder.py` is an unedited copy of the earlier physical generator,
retained solely to reproduce the four old files. Its SHA256 and the unchanged
historical result are pinned in `PROVENANCE.json`.

The catalog completeness and extremal assumptions of h3959 remain imported.
The new CNF audit is not proof-assistant formalization or externally reviewed.
The underlying h3959 theorem has independent ACCEPT review h3965; its scope
and source are recorded in `PROVENANCE.json`. See `VALIDATION.json` for recorded replay cost and controls. No novelty
is claimed for the underlying regular-degree theorem.

The quantified reduction is exactly two of four named physical jobs, not half
of all possible good43 graphs. The entire q10 task remains undecided. No good43
or Ramsey lower-bound improvement is established.
