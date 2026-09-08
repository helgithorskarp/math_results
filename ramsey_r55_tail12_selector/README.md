# A canonical 12-vertex residual for nine complete good43 branches

This package consumes the [reviewed greedy-closure interface](../ramsey_r55_global_greedy_closure)
and combines **all nine branches with s=1** into one physical SAT formula.
The entire triangle-free residual ranges over McKay's 12 Ramsey(3,5,12)
representatives. All 372 edges from it to the other vertices remain free.
Canonical relabeling removes 54 former residual edge decisions; it preserves
the complete nine-branch family up to graph isomorphism, conditional on catalog
completeness. It does not cover the other 30 refined branches.

The [proof](PROOF.md) establishes both directions, compatibility with core
block sorting, and the exact selector encoding. `normalize.py` constructs
the relabeling and can repack a canonical residual into the old triple blocks.
No old saved 42-vertex graph or repair basin is used.

The production formula has **1,184 variables and 1,486,424 clauses**. Shared
tail predicates reduce its size from 79,532,312 to 66,250,106 bytes compared
with direct selector disjunctions, removing 3,429,227 literal occurrences.
These are encoding measurements, not a solver speedup or a global count.

```text
production CNF SHA256:
91bf5f741a7e8d08ad1da1e347825cf572060db601bb40f2e185da2c6f734dce
```

One frozen CaDiCaL 3.0.1 call reached its 300-second limit in
300.01969444399583 seconds and returned **UNKNOWN**, with no candidate or
family exclusion. Its 266,149,149-byte partial DRAT stream is not a certificate
and was not checked. No good43 or Ramsey-bound improvement is established.
The earlier support<=8 and r7-s4-t3 timeouts remain UNKNOWN.

The initial reporting wrapper rejected the output because it expected a
status on stdout. CaDiCaL's `-w` option writes `c UNKNOWN` to the witness file
(`src/cadical.cpp` in the pinned solver). The final reader recognizes that
exact output with exit code zero. The preserved run was reclassified; the
solver was not rerun. Six parser controls include conflicting and missing
statuses. [RESULT.json](RESULT.json) records the correction and all run hashes.

Run the compact checks using Python 3.11.2 and the standard library:

```bash
python3 -B ramsey_r55_tail12_selector/reproduce.py
python3 -O -B ramsey_r55_tail12_selector/reproduce.py
```

Regenerate both complete formulas in a new directory outside the repository
and independently audit every literal (about 110 seconds in the recorded run):

```bash
python3 -B ramsey_r55_tail12_selector/reproduce.py --generate /tmp/r55-tail12-replay
```

The compact replay checks every catalog entry, all 4,096 one-hot assignments,
all 5,448 predicate definition cases, 37,752 residual predicate cases, forward
and reverse transport of 36 full physical fixtures, closure preservation, and
strict target-decoder rejection controls. The fixtures deliberately fail the
target. `VALIDATION.json` contains exact expected audit results. Full audits
passed in normal Python and for the production formula with assertions disabled.

For manual formula generation:

```bash
python3 -B ramsey_r55_tail12_selector/compile.py --cnf /tmp/r55-tail12.cnf
python3 -B ramsey_r55_tail12_selector/audit.py --cnf /tmp/r55-tail12.cnf
```

`--direct` selects the unfactored reference encoding for both commands.
`run_decision.py` reproduces the single capped invocation when supplied with
the exact solver executable, a generated production formula, a fresh output
directory, and an independent DRAT checker for a possible UNSAT result:

```bash
python3 -B ramsey_r55_tail12_selector/run_decision.py \
  --solver /path/to/cadical --cnf /tmp/r55-tail12.cnf \
  --output /tmp/r55-tail12-decision --checker /path/to/drat-trim
```

Default reproduction makes **zero solver calls**. Generated formulas, logs,
traces and executable binaries are omitted. Solver/checker commits and hashes
are in [PROVENANCE.json](PROVENANCE.json). A SAT result must pass the complete
model decoder and the literal 43-vertex checker before a compact edge list is
written. An UNSAT result requires an independently checked proof.

The input is h3863, independently accepted at h3865, with source
`18ea1f93c1b13d36cccde343e6e3b875dad0a5e2` and review source
`b78ff17d8922e9a6d984c99a64dc756eac84c912`. Core symmetry builds on h3859.
The 156-byte catalog input is reused from the pinned sibling source and was
freshly downloaded and hash-matched from
[McKay's author catalog](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html).
Catalog completeness is imported, not regenerated. Unlike h3863's purely
physical closure formulas, the covering direction of this selector formula
requires that premise. A satisfying graph is independently checkable without it.
