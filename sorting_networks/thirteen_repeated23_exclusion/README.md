# Complete repeated-(2,3) B11 exclusion

Author/executing agent: **six-sorting-1, researcher**. The shared signing
identity does not identify the individual author.

Classes40,155,243 in the original480-class quotient admit no B11 sorter
of size at most22. With the prior exclusions of34,149,237, this closes
all six repeated-effective-(2,3) classes and all32,310 effective orders,
at arbitrary allowable depth and with every physical profile loop
interleaving. The new three class exclusions cover16,155 further orders.
Read [PROOF.md](PROOF.md) for complete scope, attribution and written
mathematical bridges. These bridges and imported normal forms remain
unformalized. Separate algorithmic checks are not external-person review.

The imported complete parent reduction has five exact tails. Two47-row
tails have elementary moving marked-cut certificates. The remaining
48/52/52-row tails have complete capped serial CNFs with no activity,
symmetry, suffix-component or depth clauses. Three small input cores
and three compact RUP traces are included,102,403bytes altogether.
Every core clause is checked against the independently audited complete
formula; every RUP addition is replayed without a solver. Full generated
CNFs, metadata, native proofs, logs and environments stay outside Git.

During this pass six-sorting-2 published the complete ten-event branch
exclusion, graph8321/sourcea3888f3045192c326564035fc01e2309ba1cdd63,
including the prior exclusion of class155/image0. Our certificate for
that image supplies an additional independent algorithmic check, not
a new image-exclusion claim. The new moving cut closes its remaining
tail. The imported branch result plus the present complete class
exclusions leave **320=297 eleven-distinct+23 eleven-repeated classes**
and2,186,295 effective orders. GlobalS13 remains44..45; B11 remains22..23.
Other thirteen-input prefixes outside literalP19 remain uncovered.

Run from this directory in a full repository checkout, with
CPython3.11+, assertions enabled and `python-sat==1.8.dev24` installed:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B build.py
python3 -B verify.py
python3 -B controls.py
python3 -B frontier.py
```

`build.py` regenerates exact data and complete CNFs in ignored `out/`.
It does not run a solver unless `--solve` is explicitly selected.
`verify.py` and `frontier.py` use only the standard library and import
neither the generator nor a solver. `controls.py` exercises the actual
SAT encoder with pinned insertion words. Expected statuses are:

```text
LITERAL_DATA_AND_COMPLETE_CNFS_REPRODUCED
COMPLETE_REPEATED23_EXCLUSION_INDEPENDENTLY_VERIFIED
POSITIVE_SORTERS_AND_FOUR_SEMANTIC_REJECTION_CONTROLS_VERIFIED
EXACT_CONDITIONAL_FRONTIER_INCIDENCE_VERIFIED
```

`verify.py` audits686,558 clauses/281 cardinality blocks and replays
1,446 compact proof additions. It checks40,960 original prefix inputs,
790 B11 rows and70,368 actual distinct-marker/free assignments.
The known full45 sorter and the three insertion/full70/69/69 controls
each sort all8,192 original inputs. The source manifest records measured
runtime, memory, exact data hashes and completed native verification.
Neither checksum agreement nor native UNSAT alone is the proof.

Required public inputs are hash pinned in [dependencies.json](dependencies.json):
the sibling `thirteen_repeated23_reduction` fixture/certificate,
the original `thirteen_extreme_multiset_quotient` certificate,
the root `sorting13_B11_ten_event_branch_exclusion` certificate and
the root `sorting13_B11_ten_event_loop_postponement` certificate.
Sparse-checkout overrides are available as `--parent` for the first
three commands and `--quotient`, `--peer-certificate`, `--ten-parent`
for `frontier.py`. `--out` selects local generated output for the first
three commands. The frontier command checks exact incidence and literal
image equality while importing the peer's complete branch proof; it
does not replay that much larger proof suite.

For optional native proof regeneration use `build.py --solve`; it keeps
15-second bounds per case and reports UNKNOWN explicitly. The published
compact proofs can be checked independently with DRAT-trim, commit
`d9260be3bbfedb04306d7f7938cbf1a552097d99`:

```bash
drat-trim class40.core.cnf class40.rup -U -t 25
drat-trim class155.core.cnf class155.rup -U -t 25
drat-trim class243.core.cnf class243.rup -U -t 25
```

All three must report `s VERIFIED`. These native checks supplement the
solver-free replay. Large raw traces are not required to check the
included compact certificates. Solver/BLAS/OpenMP threads are one and
local intensive jobs are serial. Checking stages stop at45seconds.
Timeout, UNKNOWN, a killed process or incomplete coverage proves nothing
about nonexistence. No reviewer verdict or formalization is asserted.
