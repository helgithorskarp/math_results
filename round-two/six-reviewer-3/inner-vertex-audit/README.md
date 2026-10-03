# Original G20 necessary 260-system audit

Actual six-reviewer-3, independent mathematical reviewer. Read [REVIEW.md](REVIEW.md) for the exact verdict, hypotheses, imports and software limits; [PROOF.md](PROOF.md) contains the ordinary conditional argument and [ADDENDUM.md](ADDENDUM.md) the proved division-free refinement.

With Python 3.12 and its standard library on POSIX, run:

```sh
python3 run.py
```

The runner checks all 25 entire mathematical records in normal and optimized modes, serially, with all six native thread settings equal to one and a fixed 30-second guard per child. It reconstructs all 364 cases, all 260 systems with 122 predicates each, exact binding coefficients and closed sign bounds. To retain the generated records locally, choose a new output directory:

```sh
python3 run.py --records-directory generated
```

No network, external algebra package, private corpus, native author program or author certificate is required. FACTORS.json and SYSTEM.json are credited original literal inputs; their independent checks and provenance are explicit. RESULTS.json holds whole-output hashes and sizes, not accepted mathematical conclusions. PROVENANCE.json records the two primary seals and later code exposure; VALIDATION.json records actual resources and every closed sign cell. source-manifest.json pins every other published file.

The reduction is necessary and conditional on the entire imported normalization/lift. Every residual feasibility question, G20 capacity, the lower chart and global fifteen-point optimum remain separate.
