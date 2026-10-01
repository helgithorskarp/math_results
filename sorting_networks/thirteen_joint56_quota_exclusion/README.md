# B11 joint56 effective-quota exclusion

**six-sorting-1, researcher.** [PROOF.md](PROOF.md) excludes all18 original
eleven-distinct quotas containing both effective comparators(5,10),(6,10),
210,960 effective orders, at arbitrary allowable depth. It supplies a
complete finite reduction,11 direct tail counts and12 compact C11 RUP
certificates. This excludes a quota cohort, not every first-(6,10) word.
The global44–45 gap and literalB11 gap22–23 remain open. Written bridges
are unformalized; separate algorithms supply finite checks, not an
external reviewer verdict.

From the repository root, run serially with assertions enabled:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 sorting_networks/thirteen_joint56_quota_exclusion/generate_reduction.py
python3 sorting_networks/thirteen_joint56_quota_exclusion/verify_reduction.py
python3 sorting_networks/thirteen_joint56_quota_exclusion/build.py
python3 sorting_networks/thirteen_joint56_quota_exclusion/verify.py
python3 sorting_networks/thirteen_joint56_quota_exclusion/controls.py
python3 sorting_networks/thirteen_joint56_quota_exclusion/frontier.py
```

Use CPython3.11+; the actual execution used3.11.2. Reduction and independent
verification use only the standard library. Build/controls import
python-sat1.8.dev24; the full-CNF producer uses its sequential-cardinality
implementation. Verify.py uses no native solver. Each stage has a
45-second per-class/case limit; a timeout is incomplete checking.
Use one CPU-intensive job and one numerical/solver thread. No allocation
increase is required. All bulky generated state stays in ignored out/.

Expected final statuses:

```
ALL_JOINT56_CLASS_REDUCTIONS_REPRODUCED
ALL_JOINT56_REDUCTIONS_INDEPENDENTLY_VERIFIED
LITERAL_DATA_AND_COMPLETE_CNFS_REPRODUCED
COMPLETE_JOINT56_EXCLUSION_INDEPENDENTLY_VERIFIED
TWELVE_POSITIVE_SORTERS_AND_SIX_SEMANTIC_CONTROLS_VERIFIED
EXACT_JOINT56_CUMULATIVE_INCIDENCE_VERIFIED
```

The18 quotas give240 phase triples,10,524 prefixes and3,952 image/budget
pairs. Partition:3,452 activity,477 fixed boundary,1 movement,6 moving
two-port,4 fixed internal,12 CNF/RUP. Complete native and compact native
checks were actually run with drat-trim commit
`d9260be3bbfedb04306d7f7938cbf1a552097d99`, binary SHA256
`226b68d555a4ee7952a623236090d033437bc6f6bfe4ef97d30895539aa0c16e`.
There are22,088 compact core clauses and9,443 RUP additions, zero RAT
steps/deletions. Optional build.py --solve regenerates full native traces
using one-thread Glucose4, with15 seconds per query; any result must be
checked before use. Exact native raw-trace hashes are provenance, not a
replacement for independent replay of the supplied RUP certificates.

Fixture.json binds the exact158 B11 rows and original13 prefix. The
reduction authenticates complete regenerated boundary witnesses by
canonical hashes, not by publishing a large enumeration. Tail_obstructions
binds every literal tail; certificate.json binds each complete formula,
compact core and proof. Source-manifest.json records executed checks,
resource use and public-file hashes. Independent verification reconstructs
inputs, profiles, preparations, marker counts, clauses, cardinality
extensions, core membership and all RUP steps. Controls verify twelve
full69-comparator sorters and reject six semantic corruptions, including
updated-digest corruptions and omission of a whole quota.

Frontier.py verifies exact cumulative incidence with pinned prior claims:
189 classes become171, with983,070 effective orders. This calculation
does not count subsequent peer closures. It counts the concurrent two
first4 proofs once. Dependencies and trust boundaries are explicit in
[dependencies.json](dependencies.json); no prior suite is silently
reported as rerun. No credentials, private ledger, raw search corpus,
binary or environment is included.
