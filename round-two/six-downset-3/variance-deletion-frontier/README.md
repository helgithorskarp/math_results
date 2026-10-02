# Variance deletion frontier

Actual author **six-downset-3**, researcher. See [PROOF.md](PROOF.md)
for the exact quantified theorem and ordinary, unformalized bridges.
For every integer k>=5 the explicit affine/scalar-repair ansatz has
rational capped greatest-rank H certificates for every q>=b(k)-4;
the credited universal obstruction leaves at most q=b(k)-5. The k6
cutoff is exactly24. Every Pell member k=u_j+1,j>=2 has exact cutoff
3u_j+p_j-5=b(k)-5. General H/I and the other remaining orders are
unresolved. New independent review is pending.

Python3.12.14 and the standard library suffice. From this directory,
in a checkout containing the two neighboring SHA-pinned helper files:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1
timeout 60s python verify.py > normal.json
timeout 60s python -O verify.py > optimized.json
cmp normal.json optimized.json
sha256sum --check SHA256SUMS
```

Both modes compare every field with [EXPECTED.json](EXPECTED.json).
The finite part covers all192 specified boundary pairs, the exact
q24/k6 matrix point, all293165 entries of two original whole lifted
matrices, two original row baselines, and13 semantic damage controls.
Coefficient certificates and the written proof supply unbounded
coverage;42 Pell calibrations are explicitly finite validation.
[RESULTS.json](RESULTS.json) records the measured bounded serial runs.
There are no child processes, solver calls or downloaded data in the
math verifier. One mathematical process at a time; native threads1.

An individual rational M entry needs no downset allocation:

```sh
python entries.py 266 49 --a 0 --b 1
python entries.py 24 6 --a 0 --b 0
python entries.py 1000000 100000 --a 1 --b 3
```

Bits0,1,2 are a,b,c; the next q bits are outside points, with the first
k outside points the canonical deleted set. The API rejects deleted
members, invalid types and a failed sufficient variance estimate
unless the separate exact q24/k6 point applies. A failure is no
nonexistence conclusion. Other Z are covered by point permutation.

The complete executable imports are the two pins in [pins.py](pins.py).
The finite original builders keep their historical guards unchanged;
new q19/k5 and q24/k6 builders have separate singleton guards. Only
small source, scalar records and hashes are published; no dense
matrix corpus, credential, key or private ledger is an input.
