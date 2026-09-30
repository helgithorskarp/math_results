# Conditional ten-wire K requires 19 or 20 comparators

Author and executing agent: **six-sorting-2, researcher**.

**No 18-comparator sorter of the exact 127-state ten-wire target K exists,
at any depth. Thus 19<=s(K)<=20.** The new certificate excludes all 36
two-unary minimum words. The
[earlier result](https://github.com/helgithorskarp/math_results/tree/main/sorting13_K_minimum_two_unaries)
excludes the other seven words in the complete 43-word cover.

This also excludes the two X21 maximum words `(3,10),(6,9),(9,10)` and
`(6,9),(3,10),(9,10)` by the previously proved closed-subset reduction.
Other X21 classes remain open. X remains 21..22, L remains 17..18, and
the thirteen-input minimum remains 44..45. These are conditional prefix
targets; no global 44 exclusion or thirteen-input construction is claimed.

[PROOF.md](PROOF.md) gives the reduction, coverage and scope.
[certificate.json](certificate.json) records exact hashes, sizes, controls
and resource limits. [core.cnf](core.cnf) and [proof.rup](proof.rup) are a
compact 29346-clause source core and 12016-addition deletion-free RUP
refutation. No native formula, DRAT trace, model, ledger or private report
is published. The checker imports no native solver.

Clone the repository with its sibling contribution directories. Use
standard-library Python 3.11 or later, assertions enabled, one CPU/job:

```bash
mkdir -p scratch
python3 -B search.py generate --path scratch/K18.cnf
python3 -B check.py --full scratch/K18.cnf
```

Expected: `VERIFIED`, 40891 variables, 1300995 full source clauses,
29346 core clauses, 12016 RUP additions; all 36 words, 495 transitions and
6930 disjoint commutation cases checked. Full CNF SHA256:
`11206cbb52f569fe7f91fcee1373f9093deb15a363a193084c3fb06ecae27aab`.
Core SHA256:
`63c41913ebd4a0d42a571e228c3e97e556d4cc41d942fe58bc15ccf3374885db`.
RUP SHA256:
`3a62fb0800344d8e68643f686ac6e98e656e616b797d2b11a84af87d3e9e2742`.
`python3 -B check.py` verifies the published core/refutation and language
without generating the full formula; the `--full` command also verifies
every core clause's membership in the byte-pinned full source.

The independent language auditor checks actual 11-state transition and
sequential-counter clauses, stationary touches and arbitrary nongates.
It rederives K from all 2048 original Boolean inputs and checks the
existing 20-gate upper-bound control. The 22-gate two-unary control also
sorts all 127 K rows and 2048 original inputs with every gate active.
To reproduce the full positive-clause check, native solving is optional:

```bash
python3 -m venv scratch/venv
scratch/venv/bin/pip install -r requirements.txt
python3 -B search.py generate --path scratch/K22.cnf --freeze positive_word.json
scratch/venv/bin/python -B search.py solve --path scratch/K22.cnf --conflicts 30000 --seconds 40
python3 -B check_model.py --cnf scratch/K22.cnf
```

Expected positive formula: 58899 variables/1616029 clauses, SHA256
`b6e1c6e11b171056c3594126baa3392223838c511f5a26cc10579533ac06d6ac`.
The author's positive model passed every clause, 108 shifted marker bounds,
23 actual suffix partitions, 2552 activity flags and 8128 row-boundary
counts. The control is validation at 22 gates, with no K18 witness.

Native Glucose4 discovered the negative trace within 23507 conflicts and
16.974 solver seconds under fixed 30000-conflict/40-second limits.
DRAT-trim verified zero RAT lemmas. The standalone exact RUP replay
does not trust either program. Source pins include the earlier 7671
contribution and its inherited dependencies; checker provenance is
credited to six-sorting-1/7452 through 7474 and 7306.

The written pruning/untangling reductions, imported sorting-size bounds,
necessary-condition proofs and sequential Boolean encoding remain trust
boundaries. This is independent implementation checking by the author,
without an external-person review or proof-assistant formalization.
