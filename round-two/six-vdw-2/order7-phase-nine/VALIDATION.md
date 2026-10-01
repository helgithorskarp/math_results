# Completed validation

**six-vdw-2, researcher; 2026-10-01.** Same-author checking by separate
algorithms. No external-review verdict or formalization is claimed.

Initial native proposals and conversions for all eighteen retained
models completed under the unchanged 50000-conflict/30-second native
and 25-second internal/30-second external conversion guards. The largest
retained native conflict count was 32943. Each generated CNF was audited
against literal field arithmetic and each proposed positive-RUP trace
was checked in both Python modes before packaging.

The complete compact public package then regenerated every canonical
CNF and replayed the matching candidate proofs through both strict
checkers. This used `reproduce.py --certificate-cache` with previously
proposed CNF/LRAT bytes, not trusted cached acceptance flags. The source
replay took **72.083 seconds**, with peak parent/child RSS
**23228/71828 KiB**, serial and with all threads fixed to one.

The final result was:

```json
{
  "status": "EXACT_H7_PHASE_ENDPOINTS_8_36_EXCLUDED",
  "endpoint_phase_weights_excluded": [8, 36],
  "nonconstant_phase_band": [9, 35],
  "agreement_point_range": [126, 490],
  "total_checked_additions": 187010,
  "total_hints": 3062858,
  "all_proof_bytes_reproduced": true,
  "global_W_bound": false,
  "whole_H7_exclusion": false
}
```

All eighteen whole-clause definition audits and proof checks agree in
normal and optimized Python. Every canonical CNF, expected proof digest
and expected proof count reproduced. The fixed fixture
[EXPECTED.csv](EXPECTED.csv) has SHA256
`eff634a962397ea473b7287196cec46220c3f16318535b6ebe1051bab8f62b8a`.
These hashes/counts aid reproduction; actual clause semantics and unit
propagation establish the finite refutations.

The exact-six counter controls check 172540 tiny threshold cells and
4092 signed exact-count inputs. Exact-five controls check 159996 cells
and 4092 inputs. The forced-gap auditor separately enumerates 44052
bounded rooted profiles, obtaining exactly the eight cyclic rotations
of (6,0,5,5,5,5,5,5). Both fixed-profile audits check all 44 distinct
scalar rotations per background and retain all color orientations.

`guards.py` rejects **eighteen** damaged inputs in **26.034 seconds**,
with peak parent/child RSS **21516/52680 KiB**. For each Python mode:

- Omitted equality background, following-minority j=8 background, and
  final forced-profile background are rejected as incomplete coverage.
- Flipped exact-six and exact-five final units are rejected by gate
  semantics, even after their stored CNF digest is repaired.
- The reversed directed gap profile is rejected; reflection is not
  an authorized symmetry quotient.
- An altered imported helper is rejected by its source pin before
  the altered code executes.
- An unsupported empty conclusion and a missing live hint are rejected.

Two valid tiny unit-propagation refutations provide positive controls
for these proof-damage tests. Controls supplement the general written
normalization, gap-counting and threshold-induction arguments; they
do not replace them.

An earlier unsplit maximum-six model returned UNKNOWN at 50000
conflicts. It supplies no exclusion and was not retried at higher caps.
The later complete following-minority split is a different finite
reduction. Large generated models, traces, native logs and scratch
experiments are omitted from Git and regenerate from the compact source.
The primary interval target and remaining phase weights are unresolved.
