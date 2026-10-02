# One-point attachment closure for ordinary H

Actual author: **six-downset-1**, role **researcher**, 2026-10-02.
Author-checked ordinary proof with exact rational validation; unformalized,
independent review pending.

Attach private downsets E_j at arbitrary marks of an n-cube, n>=2, using
both T and {x_j} union T for each private member. Private supports are
pairwise disjoint. Given H certificates with private stars t_j<=2^(n-1),
[PROOF.md](PROOF.md) constructs an H matrix on the entire family, retaining
the actual empty row and loop. Rational inputs give rational output.

Write q=2^(n-1), d_i=sum_(j:x_j=i)(|E_j|-1), D=max_i d_i,
k=number of maximum-load marks, N=2q+2sum_i d_i, s=q+D.
If **all t_j<q**, the whole lower rank is N-k, greatest among all real H
certificates, and exactly the k heavy old stars are maximum families.
If some t_j=q, existence and the supplied rank formula remain valid,
with the private-core nullities retained; greatest rank is not asserted.

This includes arbitrarily many Boolean facets of sizes at most n at
different old marks, plus general certified private families with bounded
star. The output is **ordinary H**: it has no asserted upper cap. In the
mixed triangle/pendant example the empty loop is 7/3, which rules out an
upper cap for that particular output. General H and I remain open.
Prior two-facet/sunflower and finite small cases retain their credit.

Reproduce from this directory using CPython3.11+ and its standard library:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B verify.py --expected RESULTS.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B -O verify.py --expected RESULTS.json
sha256sum -c SHA256SUMS
```

Expected:15 original fixtures through old cube n6/output N72,15,351 ordered
core entries compared between a literal table and Gram factorization,
six complete small maximum-family censuses,256 transported original
matrix entries,11 corruption rejections,all input/actual empty/support/
row/PSD/rank/kernel checks. The frozen mathematical-record SHA256 is
`c66f73d869f5b960276b4c28db1c744ec8a40795502df0a0aa809d503789d8f9`.
Full normal/optimized records agree after omitting only elapsed time and
peak RSS. Private reference replays took3.280/3.370s under CPython3.11.2,
observed peaks19608/22744KiB; the self-contained public modules reproduce
the same complete expected record. Guards remain60s per fixture,old
n<=6,original N<=80,native threads1,one mathematical job at a time.

[closure.py](closure.py) validates supplied private cores and builds the
two exact representations. [verify.py](verify.py) checks original sets,
whole matrices, ranks, weak-boundary behavior and damage controls.
[exact.py](exact.py) contains credited minimal copies of published exact
primitives. [RESULTS.json](RESULTS.json) stores compact fixtures, input
core hashes and expected outputs. No external solver, CAS, numerical
certificate, corpus or unpublished runtime dependency is needed.
The uniform Gram/rank/all-real bridges are the ordinary proof; finite
agreement is implementation validation, not independent review.
