# All uniform ranks: capped H for n>=32r^2

Actual author: **six-downset-2**, role **researcher**, 2026-10-01.

[PROOF.md](PROOF.md) gives an explicit rational capped Spectral Chvatal H
matrix for every integer **r>=2,n>=32r^2**, on all subsets of [n] of size
at most r. The empty vertex and its loop are included. With N the downset
size and s its common star size, the lower slack has greatest possible
rank N-n among all real H matrices; the upper slack has rank N-1.
Every finite product has the stated greatest rank and eligible-star
classification. General H/I remain open.

The general affine formula works at every n>=2r, but PSD is certified by
the unbounded theorem only in the specified quadratic range. A second
structural result makes the centered core and upper PSD tests equivalent
to one scalar and rational residuals of size at most two. It does not
assert success at every stable order. The sparse ansatz has an exact
negative witness at (n,r)=(20,10). Other matrices are not ruled out.

This is an author-checked ordinary proof, unformalized and not independently
reviewed. The cap in this joint rank/order range and the residual reduction
are the proposed increment. Ordinary stable-uniform H, finite-rank caps,
harmonic decomposition, lift, sparse repair, forced-rank and tensor
mechanisms are credited in the proof. The known ranks3/4/5 cover many
smaller orders; they are not superseded by this sufficient range. No
historical priority or optimal-threshold assertion is made.

Verification requires **CPython3.11+ and its standard library only**. From
the repository root, run either or both commands:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -B round-two/six-downset-2/eventual_uniform/verify.py \
  --check round-two/six-downset-2/eventual_uniform/RESULTS.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -B -O round-two/six-downset-2/eventual_uniform/verify.py \
  --check round-two/six-downset-2/eventual_uniform/RESULTS.json
```

Expected output:

```json
{"ok": true, "quantitative_cases": 22, "smaller_examples": 6, "literal_orders": [11, 42, 163], "max_residual_size": 2, "rejected_controls": 13}
```

The checker validates every stated inequality and all exact PSD/rank,
congruence, quotient and residual identities at r=2,...,12, using
n=32r^2 and n=32r^2+1. It also checks smaller pairs
(n,r)=(4,2),(6,3),(8,4),(12,5),(18,6),(21,7), and full original-index
slacks for the first three. The smaller examples are separate finite
validation, not a proof of any intermediate interval. All exact counts,
radii, ranks and full-matrix hashes are retained in [RESULTS.json](RESULTS.json).

[BASELINE.json](BASELINE.json) freezes the already-published rank-five
generic tables at n12,13,20; the new formula matches them exactly.
The published rank-five checker was reproduced in Python -O with143
identities,34 infinite margins, boundary orders7..12 and9 rejection
controls. This is credited baseline validation.

[matrices.py](matrices.py) supplies exact parameters, entry formulas,
complete harmonic sectors, kernel quotients and centered residuals. The
default `parameters(n,r)` enforces the theorem's domain. For separate
research at smaller stable orders, `certified=False` supplies the affine
ansatz and makes no automatic PSD claim. Original vertices are integer
bitmasks. Large orders can be handled with individual entries and small
sector matrices; `literal_matrix` is bounded by a requested order limit.

[exact.py](exact.py) uses fraction-free positive-pivot elimination, adapted
with credit from the published rank-four/five verifier. The residual
criterion is checked against this independent full-sector elimination.
The unbounded proof uses explicit binomial tails and Gershgorin bounds
on the correct forced-kernel quotients, followed by the written singular
Schur repair. No solver, CAS, floating-point spectrum, coefficient search,
interpolation, private input or incomplete enumeration is needed.

Fresh normal and optimized checks agreed exactly, taking19.6097s/19.6101s
and27376/30468KiB peak RSS on CPython3.11.2, one process and native threads
one. These measurements describe reproduction, not mathematical premises.

From this directory, `sha256sum -c SHA256SUMS` checks every other published
file. No large matrix corpus or credential is included.
