# Checked physical subtask reduction of the two q10 survivors

Three recovered binary clauses certify **99 of 260 complete physical
subtasks UNSAT**. The remaining **161** tasks stay UNKNOWN; **29** of them
receive an additional forced physical edge. The 260 tasks form a disjoint
cover of the exact frozen d20-22 and d22-20 formulas. Baseline propagation
rejects none; the checked patch rejects exactly 99. [PROOF.md](PROOF.md)
gives the global degree argument, exact scope, and certificate boundary.
Neither whole parent is decided and no good43 graph is established.

From the repository root, using Python 3.11+ and g++ with C++17, and a fresh
scratch directory:

```sh
python3 -B ramsey_r55_q10_recovered_cube_refutations/reproduce.py \
  --branches /path/to/frozen/branches --scratch /path/to/fresh/scratch
```

If the two 94 MB original files are unavailable, the already published
h3969 generator can reproduce them byte for byte. Its complete public
source dependencies must be present beside this directory:

```sh
python3 -B ramsey_r55_q10_recovered_cube_refutations/reproduce.py \
  --rebuild /path/to/fresh/rebuild --scratch /path/to/fresh/scratch
```

That generator writes the historical base and four degree files (about
471 MB) outside the repository. It imports no solver and downloads no data.
The normal replay needs only the two middle-degree files. Expected status:
`REPRODUCED_99_Q10_PHYSICAL_SUBTASK_REFUTATIONS`.

`INPUTS.json` pins both formulas and maps every proof-core clause to its
original source position. The three small core/proof pairs are sufficient
for certificate checking; the large partial traces are not needed.
`EXPECTED.json` records all 260 propagation comparisons and exact receiving
emission hashes. No certificate relies on Python assertions or C++ assert.

`TASKS.json` enumerates all 260 physical cubes. To list the checked residual
interface or emit a remaining CNF, use:

```sh
python3 -B ramsey_r55_q10_recovered_cube_refutations/interface.py
python3 -B ramsey_r55_q10_recovered_cube_refutations/interface.py \
  --task d22-20-w36-p0 --branches /path/to/frozen/branches \
  --output /path/to/new/task.cnf
```

Choose a task ID marked UNKNOWN in TASKS.json. The example above emits a
remaining task with the additional forced edge. A closed task returns its
certificate ID and writes no file. Generated residual CNFs preserve every original clause and
add the proved patch, 13 physical cube units, and the extra edge unit where
applicable. Existing files are never overwritten.

The reductions are recovered from clauses already learned during historical
UNKNOWN runs. They supply portable certificates and physical task statuses,
not measured solver acceleration. The h3969 endpoint closures and h3975 /
h3979 ambient-deletion result remain unchanged. No adjacent ambient,
symmetry, occupancy, repair, or degree-catalog family was opened.
