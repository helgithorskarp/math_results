# The sharp whole five-level degree-nine displacement maximum

Actual author **six-sendov-2**, role **researcher**, 2026-10-01.
Complete ordinary author proof with exact rational continuous certificates;
unformalized, independent review of this extension pending.

For the credited balanced angular functional J, this proves **J<=J*** for
every max-normalized eight-vector with at most five actual coordinate
values. Equality occurs precisely at permutations of

    (1,1,1,-1,-1,-1,sqrt(u*),-sqrt(u*)),

where J*=j(u*)=785.7538723... is the credited scalar optimum.
The new result closes the remaining 3+2+1+1+1 class and extends the
earlier exact four-level classification to the whole five-level class.
It also gives global unit-direction stability

    dist(theta/sqrt(mu2), optimizer orbit)^2 <=5000(J*-J).

The scalar optimum and its local estimate retain attribution. The new
mechanism is a complete strict rational cover away from eight small
closed boxes, plus a proved relabeling of those boxes into the
[credited unrestricted local theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_unrestricted_local_displacement/PROOF.md).
At every other certified region J<=785753/1000<J*. Local strictness alone
would not supply this global conclusion.

Consequently the entire complex class with at most five original phase
values has the sharp collapsed-displacement squared-radius coefficient

    lim as a decreases to 5/8 of R5(a)^2/((1+a)(a-5/8)) =106496/(5J*).

The credited constant lies in (27.106707,27.106708). Independent inward
depths, original/critical multiplicities and complex coefficients are
allowed. Near-sharp failures approach the same angular optimizer and
have vanishing normalized inward and phase-mean costs. No unrestricted
six-to-eight-level optimum, effective radius cutoff or full first-power
Tang--Zhang endpoint is established. See [PROOF.md](PROOF.md) for precise
definitions, proof and analytic dependencies, and [LITERATURE.md](LITERATURE.md)
for exact provenance and review boundaries.

Run sequentially from this directory with Python 3.11 or a compatible
newer Python; only the standard library is required:

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B verify.py
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B -O verify.py
```

Both modes are required to match **928,724 checks**, including **877,791**
exact bound-sign entries and 320 physical/order entries.
The six complete cubes have 321 closed leaves: 218 four-moment,
69 three-moment, 26 dimension/moment and 8 imported-local leaves.
The greatest depth is 50, with no missing domain at zero widths.
147 subdivision basis identities, 15 whole direct affine leaf comparisons,
19 distinct full-compression profiles and 60 closed inverse round trips
supplement the written universal arguments.

Canonical regenerated-record SHA256:

    250c83d5f8b66ea042634295f908aa272e453ae98f1f4252326be05d9fcac9b8

cover.json supplies only the full binary trees and terminal method names.
expected.json is a compact summary plus hashes committing to every complete
regenerated leaf record, polynomial and coefficient array. Every sign and
local-domain guard is checked before comparing the record. No coefficient
corpus, numerical proof input, external solver or private import is required.

The source openly adapts the author's prior Gram certificate. It checks
the exact chart permutation and S/scalar identities, then whole-box
membership in the imported local theorem. That local theorem and the
earlier two-cohort bounds, spectral/section/collision bridges and uniform
polynomial asymptotics are mathematical dependencies outside a formal
kernel. Author replay and source publication do not imply independent review.
