# Validation and scope

The frozen runner first checked SHA-256 identities for the audited formula,
CaDiCaL 3.0.1 binary, and drat-trim binary. It used exactly one command:

```text
cadical -t 1800 -w witness.txt FORMULA trace.drat
```

The fail-closed classifier was checked on six SAT, UNSAT, UNKNOWN, conflicting,
and missing-status controls before the run. The observed output was:

- process exit code 0;
- no solver status line;
- witness bytes exactly `c UNKNOWN\n`;
- empty stderr;
- elapsed wrapper time 1,800.11150585601 seconds;
- peak child RSS 466,412 KiB;
- 3,486,156 conflicts, 14,792,193 decisions, and 811,501,360 propagations.

Those conditions classify only as UNKNOWN. The SAT decoder and DRAT checker
were therefore not invoked. Their hashes and acceptance paths were frozen in
the runner for the counterfactual conclusive outcomes.

The compact checker independently recomputes every published comparison delta
and percentage from the h3893 and expanded raw counts. It verifies that both
outcomes are UNKNOWN and rejects any target, exclusion, or tractability-pass
flag. Normal and `-O` checks agree.

The full reproduction regenerates the input formula from the hash-locked h3899
source and all transitive dependencies, compares its exact hash and metadata,
then independently reads every clause under normal and `-O` Python. It makes
no solver call. The bulk formula, catalog cache, stdout, and partial DRAT are
omitted from the repository.

The formula's equivalence to the original physical task depends on h3899's
K4 expansion proof and h3897's separator classification. The separator theorem
was independently accepted at h3907; the dependent h3899 interface remains
externally unreviewed. The complete ordered family continues to import h3887's
catalog-completeness and predecessor trust boundaries. This boundary does not
test another task, solver seed, backend, cap, or decomposition.
