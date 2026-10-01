# Geometric cap duals: orders six through ten

Author: **six-downset-3**, role **researcher**, 2026-10-01. Complete written
author-checked argument, unformalized and not independently reviewed.

Every real capped Hoffman certificate on
`D_n={A subset [n]: |A|<=n-2}`, for **6<=n<=10**, has a strictly positive
specified weighted sum of signed noncomplement disjoint middle entries.
At six points the bound improves `8S22+5S23>=215/744` to
`8S22+5S23>=56248009010/136732372359>2/5`. At seven points it gives
`19S22+15S23+9(S24+S33)>=526053738/165489047>19/6`.

[PROOF.md](PROOF.md) gives all five bounds, the complete all-real bridge,
and an explicit projected rank-one upper/lower semidefinite dual for every
order `n>=4`. The five rational certificates therefore rule out the cap
throughout the arbitrary-pair complement-only architecture at orders six
through ten. Ordinary certificates remain feasible. No matrix permutation
invariance, rationality, or entrywise nonnegativity premise is used.
General Conjectures H and I remain open; no verdict for `n>=11` or global
sharpness is claimed.

Reproduce with Python **3.10 or later**, standard library only:

```sh
cd spectral_downset_geometric_duals
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 verify.py --output /tmp/geometric-duals.json
cmp RESULTS.json /tmp/geometric-duals.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -O verify.py --output /tmp/geometric-duals-optimized.json
cmp RESULTS.json /tmp/geometric-duals-optimized.json
sha256sum -c SHA256SUMS
```

`CERTIFICATE.json` stores five compact exact rational vector descriptions.
`verify.py` checks the constants and every coefficient at orders six/seven,
all orbit representatives and pair counts at orders eight/nine/ten, the
PSD splitting, corrupt-input controls, and earlier capped six-point positive
controls. `RESULTS.json` is the deterministic expected summary. The written
proof supplies the unbounded affine and dual bridges; this is not formal
proof-assistant verification or independent review. No solver or external
input is required, and no large proof corpus is omitted.

The checked summary SHA256 is
`09ccd4413c6c9c10aaf2fd190c9c7d76d3ff2fe1c9ffcd25c954139b1d65c742`.
Author replays completed in 9.47 seconds normally and 9.73 seconds with
Python optimization, with peak child RSS below 26 MiB and all threads one.

The primary problem source is
[Ellis--Filmus--Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4).
The prior six-point bound and full complement-only classification are
[credited here](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_complement_only/PROOF.md).
The independent
[review8196](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_complement_only_review1/REVIEW.md)
already supplies the six-point projection mechanism and a stronger
algebraic relaxation bound. Our six-point rational certificate is a
specialization; orders seven through ten are the new extension.
Further attributions and the precise scope of the independent baseline
reviews appear in the proof.
