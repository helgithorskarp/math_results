# R(5,5): all rank-four row tasks with column support at most eight

This package records a broad, exact physical-completion experiment with an
honest `UNKNOWN` outcome.  It does not construct a good43 graph or exclude the
tested family.

The independently reviewed rank-four task cover represents every hypothetical
good43 having a red binary-rank-four 20+23 cut by 10,959 canonical row tasks.
This experiment combines all those tasks into one formula and permits every
sorted, spanning 23-side factor list using at most eight distinct labels.
Zero is allowed under the reviewed caps.  All 443 internal edges and all 460
cross edges are physical Boolean variables.

The aggregate CNF has 147,595 variables, 2,462,655 clauses, and SHA-256
`e01a3aec66bf8d3bd0ce8aba611634abc3f5068ad6ad56511be00186d6832989`.
It includes both polarities for all 962,598 physical five-sets, the exact
both-color cut-rank guard, red degrees 18--24, the h3771 tripled-row contact
condition, and h3579 equal-label pair distances.

One predeclared CaDiCaL 3.0.1 call stopped after 900.088 seconds with exit zero
and `c UNKNOWN` in its witness file.  It found no candidate and completed no
refutation.  The 834,897,993-byte partial DRAT stream is not an UNSAT
certificate, was not checked, and is not published.  No solver retry, task
shard, support increase, or alternate backend was run.

`reproduce.py` regenerates the 138,709,891-byte CNF in a temporary directory,
checks its hash, and independently audits all 1,925,196 physical five-set
clauses.  It also reruns the small encoding controls and validates the compact
production record.  From this directory, use Python 3.11 or newer:

```sh
python3 -B reproduce.py
python3 -B -O reproduce.py
```

Expected status:

```text
VERIFIED_ALL_ROW_SUPPORT8_UNKNOWN_BOUNDARY
```

See [FORMULATION.md](FORMULATION.md) for the reduction and
[VALIDATION.md](VALIDATION.md) for the exact trust boundary.  To repeat the
900-second solver call, first regenerate the CNF as documented there, then use
`solve.py` with binaries matching the hashes in `frozen-run.json`.

This boundary shows that one direct selector formula does not decide the broad
support-at-most-eight stratum within the frozen budget.  It says nothing about
whether the formula is satisfiable.  Column supports of size nine or more,
higher cut ranks, and unrestricted good43 existence remain open, as does the
tested support stratum itself.  The known lower bound remains `R(5,5) >= 43`.
