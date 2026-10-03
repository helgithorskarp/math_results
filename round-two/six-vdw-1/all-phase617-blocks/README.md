# Exact maximum 3703 for independent four-character 617 block/phase rules

Actual author: six-vdw-1, researcher. Author-checked computer-assisted lemma;
ordinary bridges unformalized and independent-person review pending.
The family definition, proof and metric corollary are in [PROOF.md](PROOF.md).
There is no 3704-point coloring or improved numerical W(2,7) bound here.

This source-only packet verifies the complete compact mathematical
certificate, the known 3703 attainment and the physical class metric.
It requires only Python's standard library; tested with Python 3.12.14,
one CPU/thread and the existing 2 GiB scope. No solver, converter, full model,
network, ledger, key or external graph result is needed for verification.

From this directory, run sequentially:

```sh
python3 verify.py
python3 -O verify.py
python3 controls_all_kernel.py
python3 -O controls_all_kernel.py
```

The first two commands must equal the whole EXPECTED.json record. They check
the source manifest before executing the proof, attainment and metric.
The last two reject 11 real certificate damages, including a root alias,
wrong actual AP and local clause, wrong RUP hint and missing final empty
clause, with hashes repaired for the three corrupted-byte cases.

The compact certificate has 3930 leaves:3757 AP signs from 3157 actual APs,
and 173 proved necessary local-row clauses. Positive-RUP replay checks 571
additions and 11128 hints through the final empty clause. Its hashes are:

```
kernel.json  1f9c0440e414000db5c2f136e2e6aea7237523e50d7dd09af2c7bfcbed6933fc
kernel.cnf   cb596ea5250ea8e6d4c47ae4c737a7f4114ec037b7c8561a8f5def5941a498a9
kernel.lrat  9ca40dedeb5ec950a3e31c63b907250f092351b12ed347070d3799621faca1f5
```

The row-plan and kernel input metadata describe immutable construction or
proof proposals. Their false feasibility/exclusion flags are not final
verdicts: the verifier derives the checked result. All proof premises are
reconstructed directly from actual APs and necessary local row constraints.
Raw model/CNF/deletion trace, native binaries, private operational receipts
and full search state are deliberately unnecessary for this compact proof.

Public verification checks only necessary local domains before proving
the target exclusion; it does not claim those domain choices are feasible
words. The 2^596 raw family count and 3108 class equality-star rank are before
AP restrictions. The distance-one extension direction is a new unstarted
model and receives no exclusion from this source.
