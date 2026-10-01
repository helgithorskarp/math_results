# Independent two-facet audit

Reviewer: **six-reviewer-1**, independent mathematical reviewer. The
[review and proofs](REVIEW.md) confirm committed lemma8579 and prove a larger
rational unequal-cube rank repair with separation from both endpoints.

Run from repository root, using CPython standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B -O round-two/six-reviewer-1/two-facet-audit/audit.py --check round-two/six-reviewer-1/two-facet-audit/expected.json
```

No author artifact, solver or graph access is required. The independent
checker covers35 original matrices/28,087 entries, seven complete spectra,
nine improved repairs, all55 four-point facet pairs and complete selector
censuses through order5. The infinite claims rely on the written proofs.

The optional author bridge requires the author's directory at commit
40b5a8044c7f388e72f50a84e1bf3f051a60af2a, materialized separately:

```sh
python3 -B -O round-two/six-reviewer-1/two-facet-audit/compare_author.py --author-dir PATH_TO_PINNED_AUTHOR_DIRECTORY --check round-two/six-reviewer-1/two-facet-audit/bridge.json
```

This bridge imports author code to compare every rational entry; it is
separate from the independent checker. [Provenance](PROVENANCE.json) gives
pins, finite scope and measured resources. [SHA256SUMS](SHA256SUMS) covers
the compact files. Checkpoints, graph receipts and working scratch are not
runtime inputs and are not published.
