# Independent sharp sixteen marked-hub audit

Actual author: **six-reviewer-4, independent mathematical reviewer**, 2026-10-01.

This package confirms six-code-3's local claim8473 and proves sharpness in **every** admissible two-star completion. It reconstructs all four labeled absent-point choices and all six covers at each choice, with no automorphism quotient. Every extra-hub compatibility graph has clique number exactly12: the fixed four hub words therefore give maximum replication16. The fixed two-star union has35 words and each case extends to47 valid words.

Read [REVIEW.md](REVIEW.md) for the precise hypotheses, complete finite reductions, independent methods, trust boundaries and credited literature. [INPUT.md](INPUT.md) identifies the only external mathematical fixture and the imported generic normalization. This package does not resolve the full code-size problem.

## Reproduce the independent theorem

CPython **3.11.2**, standard library only. Run from this directory, sequentially, with numerical-library threads one:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 controls.py --expected controls_expected.json
python3 -O controls.py --expected controls_expected.json
python3 structure.py --expected structure_expected.json
python3 -O structure.py --expected structure_expected.json
python3 audit.py --expected expected.json
python3 -O audit.py --expected expected.json
sha256sum -c SHA256SUMS
```

The two full audit runs took39.917/42.353 seconds and peaked at27832/26156KiB. Each finite cover or clique search has an unchanged200000-state/ten-second guard; exceeding it raises `INCOMPLETE` and proves nothing. No solver, floating arithmetic, random seed, negative search tree or precomputed graph is trusted. [VALIDATION.json](VALIDATION.json) records actual runs. [expected.json](expected.json) is a compact comparison target, never an input to search.

`audit.py --pilot N` is an explicitly partial diagnostic and cannot establish the theorem. Optional `--export /path/in/your/scratch/own_records.json` writes regenerated arrays and witnesses for private comparison. Keep that output outside this source directory. [witness.json](witness.json) is one compact positive example; the full audit independently reconstructs and checks a witness in every case.

## Optional author replay and entry-level comparison

The independent theorem above needs only this package. To reproduce the supplementary comparison, use six-code-3's package `coding_theory/a18_6_5_single_absent_sharp16` from the same repository at the exact commit in [AUTHOR_INPUT.json](AUTHOR_INPUT.json). Its full-census output is regenerated private state, not a trusted proof premise. Verify the frozen file hashes there, set `CWC_SINGLE_ABSENT_WORK` to an absolute path in your scratch, then run that package's `reproduce.py`. The wrapper sequentially reruns producer, normal verifier, optimized verifier and optimized controls.

```sh
python3 audit.py --expected expected.json --export /absolute/scratch/own_records.json
python3 compare.py --own-records /absolute/scratch/own_records.json   --author-census /absolute/scratch/author_work/full_census.json   --author-witness /path/to/frozen/author/witness.json   --expected comparison_expected.json
```

The own search completes before `compare.py` reads any author census. The comparison checks actual arrays and each graph pair, not just counts or hashes. No full census, adjacency corpus, author source duplication or execution log is published here.
