# Independent ten-point cap audit

Actual agent **six-reviewer-5**, role **independent mathematical reviewer**.
[REVIEW.md](REVIEW.md) confirms six-downset-3's all-real support obstruction and
proves a largest-eigenvalue floor above1019/1000 for ordinary H matrices in that
architecture. It also proves a signed missing-orbit/cap-surplus tradeoff and an
absolute extra-weight bound. No unrestricted cap or general H/I decision.

## Reproduce

CPython3.11.2, standard library only. From this directory choose two different
fresh scratch directories outside the source directory:

~~~sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 \
timeout 120s python3 -B reproduce.py --work /tmp/ten-cap-review5-normal

OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 \
timeout 120s python3 -O -B reproduce.py --work /tmp/ten-cap-review5-optimized

cmp /tmp/ten-cap-review5-normal/result.json /tmp/ten-cap-review5-optimized/result.json
sha256sum -c SHA256SUMS
~~~

The runner requires pinned input data and exact complete expected-output
agreement; generated files go only to fresh external scratch. No author
executable, optimizer, CAS, solver, external library or network is needed.
All arithmetic is integer/Fraction and checks remain active with -O.

DUAL.json and AUTHOR_EXPECTED.json are credited untrusted author data.
INPUT.json pins raw hashes and all seven reviewed source files. Our literal
frozensets, permutation-sum determinants and cofactor adjugates supply the
independence. The full affine fixture is regenerated in memory; it is not PSD.

The complete result verifies254 principal minors,49 Gram entries,11022
constant/star annihilations,7014 layer-invariance coordinates,23436 disjoint
middle pairs,1026169 full affine entries and10130 star equations.
Sixteen corrupted-certificate and hand-checkable arithmetic/scaling controls
pass. validation.json records complete cold run measurements and output hash.
Ordinary real necessity/trace arguments remain unformalized; these finite
checks do not replace the all-real proof.

Complete cold result:3451bytes, SHA256 c76c9f74acddd1b636ccf41dace79570cdc4285c27542d310d2d34621f2e7d0b. Normal4.642s/26396KiB; optimized9.525s/26720KiB. Both complete modes agree exactly.
