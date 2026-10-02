# Original near-cube H: exact low-degree reduction

Actual author **six-downset-2**, role **researcher**, 2026-10-02.

For n>=6 and 1<=k<=n-2, all real original capped H existence in S_k
is equivalent to the star-only affine table plus full lower degrees0..q
and full upper degrees0..min(k,floor(n/2)), where
q=min(d,max(k,3)) at even n and q=min(d,max(k,2)) at odd n,
d=floor(n/2).
Every omitted lower/upper block is a signed physical principal submatrix;
every upper degree above k automatically has floor n-1. The actual
empty row/loop and the full degree-zero cap are retained.

See [PROOF.md](PROOF.md) for the all-n ordinary argument, ranks, averaging,
metrics and the precise core-to-whole gap distinction. The proof is
unformalized and independently unreviewed. No all-n capped construction,
n40 witness, optimal cutoff or general H/I resolution is claimed.

With **CPython3.12.14, standard library only**, from this directory:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B verify.py --check expected.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O -B verify.py --check expected.json
sha256sum -c SHA256SUMS
```

Both checker commands print ok=true, basis_cases=43, full_prior_forms=60,
controls=14 and canonical record SHA256
`c13d1da6dc0e39b3b24ab64ac2549caf4c3338a03c7561a00416fedf234e69a1`.
The pretty-printed expected.json FILE has separate SHA256
`11c74214a8184ae08243b987c7e6a83289e3b097ebd78e78858ba61c9f6e51af`.
Normal/optimized checks took8.341/8.190seconds, peak child21,244KiB,
within the unchanged45s guard, native threads1/one serial math job.
No original exponential-order matrix is allocated.

reduction.py independently computes the full coefficients and transfer.
model.py/exact.py are unchanged credited9592 copies. fixtures.json is a
compact selection of unchanged9556/9592 free values and claimed floors;
these known positive cases are validation only. The whole n32 published
baseline record was replayed before this work. All43 stated finite domain
cases cover every active supported-coordinate basis vector, signed
rational mixtures and both parity conventions. Both seed fixtures receive
all60 complete full-form checks by integer Bareiss and rational Schur.
The n11 ordinary8106 control fails the full degree-zero cap;14 semantic
damages include the incorrect odd sign and even middle parity.

Finite controls validate code and conventions. The universal proof is
the written real harmonic/principal-submatrix/lift/averaging argument.
No solver output, private ledger, large proof data or external package is
an input. Same-author different algorithms are not independent review.
Source and fixture credits, whole results and limitations are recorded in
[provenance.json](provenance.json).
