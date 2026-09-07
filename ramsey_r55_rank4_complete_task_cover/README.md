# Complete rank-four task cover for good43

Every 43-vertex graph with no clique or independent set of size five that admits a binary rank-four 20+23 cut is represented, up to vertex relabeling, by at least one of **10,959 physical-completion tasks** in `row_cover.tsv`.

The exact row-profile census is **154,847,637 spanning profiles → 10,959 canonical tasks**, an average reduction factor of 154847637/10959 = 51615879/3653, approximately 14,129.723. This counts row multiplicity profiles under change of binary basis. It is **not** a fraction of good graphs eliminated, a graph-isomorphism census, or a measured solver speedup. Some tasks may be impossible; none was solved in this contribution. No good43 or improved Ramsey bound is claimed.

Unlike a one-sided projection, every task has all 23 column labels and all 443 within-side edges as decisions and enforces every physical five-set. No graph automorphism, fixed parent, prescribed column support, or isolated occupancy pattern is assumed. The already reviewed doubled full-support sector is excluded by an exact conditional guard, leaving every other column profile available.

| Row category | Tasks | Variables per task | Clauses per task |
|---|---:|---:|---:|
| One zero row | 5,109 | 1,157 | 1,828,415 |
| No zero, ordinary | 5,841 | 1,157 | 1,936,446 |
| No zero, affine support | 5 | 1,157 | 1,936,454 |
| Full nonzero support, multiplicities one or two | 4 | 1,503 | 1,938,106 |

The last four tasks are not wholly deleted: their columns can omit labels, contain zero, or have multiplicities exceeding two. Only the known impossible joint row-and-column profile is removed.

Read [PROOF.md](PROOF.md) for coverage and exact counting, [HANDOFF.md](HANDOFF.md) for the executable task interface, and [VALIDATION.md](VALIDATION.md) for checks and trust boundaries. `EXPECTED_COVER.json`, `burnside.json`, and `EXPECTED_AUDIT.json` are compact checkable certificates; `row_cover.tsv` is a 223,653-byte canonical representative table.

Reproduce with Python 3.11+ standard library and a C++17 compiler:

```bash
python3 -B ramsey_r55_rank4_complete_task_cover/reproduce.py
python3 -O -B ramsey_r55_rank4_complete_task_cover/reproduce.py
```

The supplied native build uses GCC and `-mpopcnt` on x86-64. A fresh temporary directory holds binaries and approximately 343 MB of generated representative CNFs, then is removed. The orbit generator uses a 128 MiB visited bitset. No SAT solver, network access, external graph catalog, or private run artifact is required. The expected final status is `VERIFIED_ALL_PATTERN_RANK4_TASK_HANDOFF`; it certifies the cover and interface, **not** satisfiability of a target task. The positive 42-vertex fixture is only a verifier control.

The rank-four branch is conditional: a hypothetical good43 could have no rank-four 20+23 cut. Higher ranks remain open. The separate [rank-five distance-sieve interface](../ramsey_r55_rank5_distance_sieve/README.md) remains a different retained family with internal distance restrictions; this contribution does not recount it.
