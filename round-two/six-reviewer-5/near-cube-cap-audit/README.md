# Independent near-cube cap audit

Actual agent **six-reviewer-5**, independent mathematical reviewer.
[REVIEW.md](REVIEW.md) confirms the quantified all-order theorem in
LEMMA9424 and proves a uniform top spectral gap for ordinary S2 H matrices,
with an explicit relaxed-cap/support tradeoff. The known n10 cap is an
imported existence premise only for the maximum-order corollary. General
Spectral Chvatal H/I remain open.

Python3.10+ standard library only. Run serially from this directory:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python -B reproduce.py --check expected.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python -B -O reproduce.py --check expected.json
```

Each command reconstructs the complete mathematical record and compares
every frozen byte, including the pre-author-code sealed record and source
hash. `--output /tmp/near-cube-audit.json` additionally saves the generated
record. Explicit exceptions preserve checks under optimized Python.

The independent runner imports only the fresh reviewer modules. It checks
the full supported matrix coefficient identity while retaining the
cardinality-kernel defect, original-coordinate controls with actual empty
rows and every point star, weight signs, binomial moments, scalar endpoint,
induction data, and quantitative consequences. Finite controls do not
replace the written all-order proof. No author code, network, package,
solver, floating input or matrix corpus is needed for this runner.

[FIRST_SEAL.json](FIRST_SEAL.json) records the first independently written
engine and whole record before author executable/fixture access; the
signed defining proof was already read and credited.
[AUTHOR_SOURCE.json](AUTHOR_SOURCE.json) lists the later fetched eight
author files at the exact defining source commit.
[CORROBORATION.json](CORROBORATION.json) separately records the late author
comparison and unchanged normal/optimized author replays. Those are
corroboration and are not independent reviewer code.

To replay the author, use their
[pinned reproduction instructions](https://github.com/helgithorskarp/math_results/blob/b3cbb040e74838da69bc52f0b989895d9fe9b18d/round-two/six-downset-2/near_full_noncentered_uniform/README.md)
and [pinned verifier](https://github.com/helgithorskarp/math_results/blob/b3cbb040e74838da69bc52f0b989895d9fe9b18d/round-two/six-downset-2/near_full_noncentered_uniform/verify.py).
Their original record hash differs from this independent record hash;
both full outputs are checked in their own stated formats.

No optimality, changed-profile verdict, new positive cap, larger-support
classification or general H/I resolution is claimed.
