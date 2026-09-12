# Cross-stratum consumption of the full physical q8 carrier

The existing **956 q8 physical jobs**, together with exactly **1,010
original tasks**, cover every hypothetical good43. The same q8 jobs can
now receive checked proofs for **2,188,168 original IDs**, including
2,744 IDs outside q8. No additional target formula or solver sweep was
started. [PROOF.md](PROOF.md) gives the complete transfer and exact scope.

The receiving audit checks all 640 actual local DRAT proofs and their
signed input bridge to the no-augmentation branches of all 1,280 mixed-q7
original IDs. It also supplies a whole-cohort DRAT/RUP receiver and the
previously missing explicit mixed-premise join for q8,r8's +119 input.

**No original task is newly UNSAT.** The complete target join remains
pending, with 956 unresolved active q8 units and a precisely named
1,010-original-parent complement. Existing counts remain 518 original
exclusions and 2,188,660 UNKNOWN IDs. The work proves neither a good43
nor a numerical Ramsey improvement, and establishes no target runtime.

## Replay

Python 3.11 and the standard library are used, with DRAT-trim commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985` built using
`cc -O2 drat-trim.c -o drat-trim`. No target SAT solver is invoked.
Run from the repository root, using fresh output paths outside Git:

```sh
python3 -O -B ramsey_r55_cross_stratum_q8_join/reproduce.py \
  /absolute/catalog /absolute/q8-queue /absolute/local19-proofs \
  /absolute/drat-trim /absolute/fresh-replay \
  --active-queue /absolute/active-cohort-jobs.jsonl
```

Expected terminal status:
`COMPLETE_CROSS_STRATUM_RECEIVING_REPLAY_VERIFIED`.
The replay compares the exact historical active jobs when the optional
last argument is supplied. It never mutates their directory.

External inputs are fully reproducible:

* Obtain the four catalogs with
  `ramsey_r55_global_maximal_packing/catalog.py /absolute/catalog --download`.
* Regenerate the q8 bases, streams and guard tree using the unchanged
  [q8 reproduction command](../ramsey_r55_q8_assumption_queue/README.md).
* Regenerate all 640 local proof inputs/traces using the pinned solver and
  [R1's certificate command](../ramsey_r55_mixed_q7_elimination/README.md).
* The optional active queue is the output of the unchanged
  [edge-119 receiver](../ramsey_r55_q8_root_unit/README.md).

The input catalogs, approximately 770 MB local proof corpus, approximately
300 MB prepared q8 interface, full original-ID ledger, control CNFs and
logs remain outside Git. The public files give deterministic source,
dependency pins, compact expected output and certificate hashes.

## Physical routing and proof admission

`HANDOFF.md` documents source and packet formats and the exact remaining
original ranges. `transport.py` and `verify_transport.py` use all 903
physical edges; the verifier does not import the producer. Routing allows
cores containing a blue K4, which cannot be sent through a listed-core-only
task lookup.

To evaluate actual future target proofs:

```sh
python3 -O -B ramsey_r55_cross_stratum_q8_join/join.py \
  /absolute/q8-queue /absolute/target-proofs \
  --catalog /absolute/catalog --local-proofs /absolute/local19-proofs \
  --checker /absolute/drat-trim
```

Each whole cohort uses either `rR-cohortNNN.json` in the inherited hinted
RUP worker format, or the pair `rR-cohortNNN.cnf` and `.drat`. Every actual
input and proof is checked. Missing or incomplete evidence leaves the
parent unresolved. A physical child with an additional edge cube is not
admitted as a whole cohort. The r8 input must have exactly +119 in addition
to its core guard; the separately checked negative branch retains its
published Ramsey premise.

The current run contains no target proofs. Its controls and receiving
audits are reproducibility evidence for the stated transfer, not a claim
that the hard q8 instances have been solved or become easy.
