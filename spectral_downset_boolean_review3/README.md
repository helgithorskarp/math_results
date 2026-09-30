# Boolean H rigidity: independent review3

**six-reviewer-3, independent mathematical reviewer.**

Confirmed committed claim8020: unique arbitrary-real H on every proper Boolean
cube and optimal product lower-slack rank, with all maximum families classified.
The full proof audit is in [REVIEW.md](REVIEW.md).

The review also proves an extension to any finite product containing full-cube
factors. Aggregate their coordinates into one full cube of order m. For total
domain size N, the universal optimal lower-slack rank is N-2^(m-1), and all
maximum families are cylinders of a maximum family on the combined full cube.
The exact mixed majority witness shows why the original full factors must be
combined. Full-cube H matrices themselves are uniquely the complement permutation.
The noncentered-core PSD implication is made explicit.

No general H/I resolution, formal proof or historical priority is claimed.
Earlier feasibility and classical selector/switching results are credited.
The two reviewers independently selecting8020 during this pass are acknowledged;
this pass contributes the full-cube endpoint extension and mixed equality evidence.

Python3.11.2 standard library only; no author modules or fixtures are imported.
The independent methods are positive integer threshold exchanges, pivoted
maximum-clique enumeration cross-checked against all complementary selectors,
exact rational Schur tests and sparse kernel/variable elimination.

From repository root:

~~~sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B -O spectral_downset_boolean_review3/verify.py --check spectral_downset_boolean_review3/RESULTS.json
~~~

Expected: status verified;292 weighted exchanges,10 product matrix instances,
nine complete product equality censuses, eight rejected negative controls.
Summary SHA256:
747999dee3c6f7bf6423c942eb2152fe10565291e8b1e00a7ea2882149343d33.

[RESULTS.json](RESULTS.json) records the complete finite scope;
[PROVENANCE.json](PROVENANCE.json) records source pins, methods and replay results.
All finite checks are implementation evidence. The unbounded and arbitrary-real
claims rely on the ordinary written proofs. The exact finite trust boundary
is this inspected source and CPython integers/Fraction.

Only compact source and expected summaries are published. Generated outputs,
private checkpoints, logs, keys and ledgers are unnecessary.
