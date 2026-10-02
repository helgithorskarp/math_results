# Four-promotion KG(7,2) construction barrier

Author: six-books-2, researcher. Ordinary R(B4,B7), round two.

For the fixed C3 action and a root joined to three seed triples, exactly four
original-blue orbit promotions admit at most nine original-red orbit deletions
while avoiding blue B7. The budget is sharp. Every blue-valid q8/q9 graph has
at least18/36 bad red spines. With the explicitly credited prior reductions,
a valid C3 type3^7 1 graph needs at least five promotions, hence at least42/45
original seed color changes at102/99 red edges. R(B4,B7) remains unresolved.
See [PROOF.md](PROOF.md) for definitions, coverage and trust boundaries.

Reproduce from the repository root, using new scratch directories:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 round-two/six-books-2/kg_c3_four_promotion_barrier/reproduce.py \
  --work scratch/kg-c3-four-promotion-replay
python3 round-two/six-books-2/kg_c3_four_promotion_barrier/validate.py \
  --replay scratch/kg-c3-four-promotion-replay \
  --work scratch/kg-c3-four-promotion-validation
```

CPython3.11.2 and g++12.2.0/C++17 standard libraries suffice; no solver or
network is used during replay. Budget about40 minutes on one CPU, plus
representative checking. Use explicit `--resume` only for completed phases
with identical source and fixtures. Failure/timeout is incomplete, not proof.

- `cases.py` explicitly checks all1,832,600 cases and their305,874 case orbits.
- `produce.cpp` searches representative pair cliques and tests every final graph;
  `producer_phase.py` reconstructs every positive from ground two-subsets.
- `native.cpp` independently scans every labeled case by blue-monotone prefix
  insertion, using [the local criterion](LOCAL-CRITERION.md); `native_phase.py`
  saves exact completed-case boundaries.
- `compare.py` transports and compares every full pool and all3,665,200
  complete terminal lists, including red-spine counts and degree predicates.
- `check.py` checks every positive graph, the frozen full inventory and baseline
  controls. `saturation.py` regenerates/verifies all924 compact orbit markers,
  expanding to2,772 single-edge additions over the entire q9 boundary.
- `expected.json` and `saturation-markers.json` predate the cold replay. Their
  hashes identify evidence and do not replace enumeration/completeness proofs.
- `validate.py` checks representative release/sanitizer intervals and malformed
  manifests. All large generated data remain outside this source directory.

All algorithms and checks are by the same author. This is an author-checked
computer-assisted lemma with written unformalized completeness bridges;
independent peer review is separate. See `evidence.json` for completed cold
run provenance when published.
