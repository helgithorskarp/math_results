# Independent P7 small-excess selector audit

Actual contributor: **six-reviewer-5, independent mathematical reviewer**.

This confirms claim9215: a71-word packing with profile(17,19,19,20^15)
and hub-pair sum7 has E>=2, and E2 forces the three-hub triple uncovered.
The new proof uses an independently filtered complete prior9141 carrier:
opposite isolated hubs make the unit/unit interface impossible, while
the unit/mixed interface has sharp maximum61. A counting selector
excludes113 of213 normalized E2,t0 necessary inventories, leaving100.
See [REVIEW.md](REVIEW.md) for every hypothesis and imported premise.
No whole-profile exclusion or unrestricted upper70 is proved.

From the repository root, run offline with standard-library CPython3.12.14
(tested; Python3.11+ should suffice), keeping generated data outside this directory:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -B round-two/six-reviewer-5/p7-selector-audit/reproduce.py --work scratch/p7-normal
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -B -O round-two/six-reviewer-5/p7-selector-audit/reproduce.py --work scratch/p7-optimized
```

Both compare the entire frozen [EXPECTED.json](EXPECTED.json), with compact
sorted-key JSON plus a final newline SHA256:
`e810a32faf8b064be44293c10c6b65f27b45325fe2a425f698dc865f9e87f3ad`.
Expected status: `PASS_COLD_COMPLETE_P7_SELECTOR_REVIEW`.

[rows.py](rows.py) builds117 coarse and138 refined overapproximating row
statistics. [inventory.py](inventory.py) covers30 ordered claimed domains;
[occupancy_oracle.py](occupancy_oracle.py) independently checks complete
budget-valid multisets in all36 ordered claimed/extension domains by
cost-class occupancies and Cartesian products. [comparison.py](comparison.py)
compares all138 actual row tuples, all20 original normalized domain
summaries and all50 actual normalized survivor records against frozen
author comparison data. The author's whole-record hash includes a different
local bridge and is not asserted equal.

[selectors.py](selectors.py) checks the quantified count certificates.
[interface.py](interface.py) freshly decodes all34 prior cores, tests every
extra physical hub marking and constructs the three surviving residual
graphs by two independent intersection/triple-ownership rules. The exact
maxima are59,61,56. [WITNESS61.json](WITNESS61.json) is a literal attaining
packing with explicit five roles, not a new unrestricted incumbent.
[controls.py](controls.py) rejects14 semantic damages and checks all1100
simple graphs on at most five vertices against exhaustive subset maxima.
The reproduction also rejects nine changed pinned external inputs.

The generic23-star census, universal no-low-low leave lemma, shared-hub
incompatibilities and complete prior9141 carrier are explicit mathematical
imports. This audit does **not** rerun the prior191-million-map raw carrier.
No researcher executable is imported or run. Seven pure functions and
the clique kernel explicitly reuse this same reviewer's earlier source;
[PROVENANCE.json](PROVENANCE.json), [FIRST_SEAL.json](FIRST_SEAL.json) and
[INPUTS.json](INPUTS.json) record that boundary. Both enlarged domains were
sealed before reading the target researcher's executable source.

Fixed guards: producer200000 states/20seconds per sector, occupancy
oracle200000 multiset products/20seconds, clique3000000 nodes/30seconds
per root, whole audit60seconds. Every incomplete run raises. All work is
serial, threads1, unchanged1CPU/2GiB. The maximum producer state count is
30331; no guard was hit. Full inventories are regenerated into `--work`.
Only compact source, fixtures, summaries and one attaining witness are published.
