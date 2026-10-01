# Independent angular obstruction audit

Reviewer: **six-reviewer-1**, independent mathematical reviewer.
Target: COUNTEREXAMPLE 8702, `bafkreifnbx2glypyqprkdsiukmlvidxam6yahqlcbrgcm4fx7tftlx4deu`.

Read [REVIEW.md](REVIEW.md) for the scope, full spectral normalization proof, repeated-eigenspace boundary, independent methodology and proved refinements. The audit confirms both published witnesses, strengthens the necessary universal constant to `111439995781294/4677150970635`, and gives an eight-coordinate rational norm-one counterexample. It does not settle the optimal constant, uniform-angular transition or first-power conjecture.

This directory is standalone: Python 3.11+ standard library, no sibling imports or author code. From the repository root:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B round-two/six-reviewer-1/angular-obstruction-audit/check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O round-two/six-reviewer-1/angular-obstruction-audit/check.py
```

Expected: 63 exact checks, four damaged inputs rejected, record SHA256 `f783b8317886824e8e983ecd3e24b83b382e4aadb76a3d9f04d4b6e95a273141`. The complete fixture is [expected.json](expected.json). `--author-record PATH` optionally compares every author value after independent derivation; `--expected PATH` selects a fixture and fails closed if missing, malformed or unequal. `--emit PATH` writes a regenerated record only after all checks and fixture comparisons pass.

The seven-dimensional contrast-basis compression is generated directly from each root vector. Exact trace-inner-product projection derives the squared spectral coupling sum; no numerical eigensolver or polynomial inverse is used. Matrix closure proves minimal-polynomial degrees; explicit inactive triple-block vectors resolve the compact witnesses' multiplicities. Ordinary spectral and angular interpretation bridges remain outside a formal kernel, as explained in the review.

[provenance.json](provenance.json) contains run receipts and target hashes. [SHA256SUMS](SHA256SUMS) authenticates the packet. Check commands do not alter source or fixture bytes.
