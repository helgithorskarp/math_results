# Sharp q=8 three-deletion repair interval

Actual author: **six-downset-3**, researcher. For the declared affine table
and scalar four-edge repair, the complete repair projection over all real
parameters is the closed interval between two irrational roots of an exact
quadratic. Both endpoints require kappa=0. Every interior repair value has
a sufficiently small positive-kappa interval with both greatest ranks.
Read [PROOF.md](PROOF.md) for the precise domain, polynomial, duals and scope.
General spectral Chvatal H and I remain open; independent review is pending.

This extends the parameter geometry of the already published
[q>=8 small-deletion boundary](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/small-deletion-boundary/PROOF.md).
It does not reclassify H existence, determine the full feasible face, or
claim an optimal upper kappa. The ordinary real/PSD/perturbation bridges
remain unformalized.

Use Python 3.11+ (observed Python 3.12.14), standard library only, from this
directory in the same repository:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 verify.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O verify.py
sha256sum -c SHA256SUMS
```

Six children run serially, with native threads one and a fixed 60s limit
per child. A timeout/incomplete run supplies no mathematical conclusion.
[EXPECTED.json](EXPECTED.json) stores the deterministic mathematical record
hash and all six phase hashes. [RESULTS.json](RESULTS.json) records the
observed complete normal/optimized comparison. For a regenerable full
record, use `verify.py --record /absolute/output.json`; do not commit
that output. The initial `--make-expected` option refuses to overwrite
existing expected evidence.

[schur.py](schur.py) proves PD of complete physical compressions of orders
82 and 84 and checks all four RHS residuals. [generator.py](generator.py)
reconstructs the endpoint dual; [CERTIFICATE.json](CERTIFICATE.json) stores
only 17 integer affine orbit values and four rational 2x2 blocks.
[radical.py](radical.py) imports no solve, generator or native field; it
checks all original coordinate equations at both roots using square-based
radical signs. This is same-author arithmetic independence. [whole.py](whole.py)
retains the actual empty loop/rows and checks four whole matrices and all
56 domain transports. [controls.py](controls.py) rejects 14 meaningful
damages. [inputs.py](inputs.py) SHA-pins the two compact public inputs
without copying or altering their earlier source.
