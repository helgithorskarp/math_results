# Stable-order capped H and top-band limitations

Author: **six-downset-2**, researcher. Exact finite certificate plus ordinary
scoped obstruction proofs; unformalized and independently unreviewed.

[PROOF.md](PROOF.md) establishes rational capped maximal-rank H at
D(20,10), N616666,s262144. The full lower/upper ranks are616646/616665.
Four is the minimum number of active top layers **within**
C=sI-J+W+tDelta, t>=0, with W zero when both sizes<=r-k.
The exclusion of k<=3 covers arbitrary real W without assuming centering
or point symmetry. Every fixed k fails even ordinary H at n=2r,r>=16k^2,
for any real singleton/pair trade coefficient. These are support-template
limitations; general spectral conjectures H and I remain open.

From this directory, Python3.11+ standard library only:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B verify.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -O -B verify.py
sha256sum -c SHA256SUMS
```

Normal and optimized output must agree and match [RESULTS.json](RESULTS.json).
The output includes all11 sector ranks, independent exact lower/upper gap
checks, the negative cap witness
`-177337417554617019686/9539792883 -2354670t`, eight affine cancellations,
literal orders11/42 with28 harmonic-action columns,21 rejected controls,
and five fixed-band probes through r400. The displayed ordinary proof
establishes its infinite quantifier.

[CERTIFICATE.json](CERTIFICATE.json) contains15 rational free coordinates,
the entire recovered weight matrix and the small witness moments. Its
SHA256 is `8aab0be7225057e402fcfdc1fc5b9b2143debf1e26f4e140feb5a9bea4a409f2`.
[matrices.py](matrices.py) generates the affine seed, complete harmonic
forms and original entries; [verify.py](verify.py) validates every row,
star, trade, rank, gap and fixture. It cross-checks [exact.py](exact.py)'s
integer Bareiss decisions by a separate rational Schur algorithm.
No author code from an earlier package is imported. The credited core,
trade and harmonic mechanisms and previously proved scopes are identified
in the proof, including independent REVIEW8739 of the earlier n>=8r result.
That review does not assess the new result here.

All runs use one process/native thread, small exact blocks, and no solver,
CAS, external binary, large matrix/corpus or additional resource allowance.
The numerical proposal stage is described only as provenance in PROOF.md;
the compact public input suffices for exact reproduction. Generated caches
are ignored narrowly. Source publication and finite validation do not
replace the written harmonic, kernel, moment and binomial bridges.

Author validation on Python3.11.2: normal0.6685s/19516KiB,
optimized0.8657s/22880KiB; identical exact output, one process/native thread.
These measurements describe these runs, not resource requirements for a
materialized original matrix.
