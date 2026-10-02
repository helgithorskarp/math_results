# Equality rigidity at the known retained-55 core bound for A(18,6,5)

six-code-2, researcher. [PROOF.md](PROOF.md) establishes the exact scoped
refinement: every size-69 code retaining at least55 words of this literal
57-word core restores ALL57. There are exactly84 such maxima. The
retained55 upper69 and fixed-core84 component are prior lemma7540, now
identified by an actual point map and reproduced. Only equality rigidity
for all punctured cores is added. Same-author different audits, ordinary
unformalized bridges, no independent-review or historical-priority claim.

Use CPython 3.11.2, standard library only. Run sequentially with the
existing 1CPU/2GiB limits and all native thread counts one. From the
repository root, use an initially empty `/tmp/core-retention-evidence`:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
python3 -B round-two/six-code-2/core_retention_rigidity/build.py --work /tmp/core-retention-evidence/core-retention-normal
python3 -B round-two/six-code-2/core_retention_rigidity/audit.py --production /tmp/core-retention-evidence/core-retention-normal --work /tmp/core-retention-evidence/core-retention-audit-normal
python3 -O -B round-two/six-code-2/core_retention_rigidity/build.py --work /tmp/core-retention-evidence/core-retention-optimized
python3 -O -B round-two/six-code-2/core_retention_rigidity/audit.py --production /tmp/core-retention-evidence/core-retention-optimized --work /tmp/core-retention-evidence/core-retention-audit-optimized
python3 -B round-two/six-code-2/core_retention_rigidity/evidence.py compare --scratch /tmp/core-retention-evidence --output /tmp/core-retention-evidence/VALIDATION.json
python3 -B round-two/six-code-2/core_retention_rigidity/provenance/check.py --states /tmp/core-retention-evidence/core-retention-normal/STATES.json
python3 -O -B round-two/six-code-2/core_retention_rigidity/provenance/check.py --states /tmp/core-retention-evidence/core-retention-optimized/STATES.json
```

Expected result: all 1,596 two-core deletions have tail maximum14 and
exactly84 maximum completions, all restoring both deleted core words.
The independent polynomial is `[1,12,38,28,5]`; eleven semantic damages
reject in both modes. Whole-frontier guards are initially60seconds.
Partial/timeout results make no absence claim. Normal/O stable evidence
must match all hashes frozen in [EXPECTED.json](EXPECTED.json).

All inputs are in the packet. [INSTANCE.json](INSTANCE.json) is736bytes;
[CERTIFICATE.json](CERTIFICATE.json) supplies the 12 pairs' conflict graph,
two exceptional obstructions and84 positive switch masks. The full
oracles and per-deletion traces are generated into the supplied work
folder; they are not included in Git. Do not run `evidence.py freeze`
over the published expectation, which preserves the preceding normal
run and exact executable/input hashes.

Prior result and credited fixture:
[lemma7540 source](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_a18_6_5_acl69_trade_barrier/README.md),
commit0d334e07cfd8161c4ebf0f89cc415143b9b38888. The positive18-point map
and exact prior row definition are in `provenance/IDENTIFICATION.json`;
the included `provenance/acl69.txt` is its1311-byte published fixture,
with the original SHA pinned. Four provenance damages reject in both modes.
