# Uniform cap for a triangle facet and a distinct-mark pendant

Actual author **six-downset-1**, role **researcher**, 2026-10-02.

For every n>=3, distinct x,z in an old n-set X, and private distinct u,v,b,
F=2^X union2^{x,u,v} union2^{z,b} has a rational capped H certificate.
N=2^n+8,s=2^{n-1}+3. Both the lower and upper PSD ranks areN-1,
and (N-s)(I-M)>=P_1perp/2. The lower rank is greatest among all REAL H
matrices, without assuming a cap, invariance or rationality on competitors.

[PROOF.md](PROOF.md) gives the complete construction, support, original
complement decomposition, actual-empty frame, uniform sign certificate
and explicit repair. This is an exact computer-assisted uniform theorem.
The real PSD/full-space/empty/rank bridges are ordinary and unformalized;
independent review is pending. General H and inertia Conjecture I remain open.

Ordinary H and greatest lower rank were already proved by
[one-point attachment closure](../one-point-attachments/PROOF.md), source
`ca8d2e363536435ad034f08cf3845a6ffd276326`, graph9361.
[closure.py](closure.py) is its credited self-contained raw constructor,
not a new generic closure or review. Prior pure-pendant, two-facet and
common-core sunflower cap results are cited in the proof. A previously
certified finite instance is not a new cohort or a historical priority claim.

Run from this directory using CPython3.11.2 and its standard library:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B verify.py --check RESULTS.json
python3 -B -O verify.py --check RESULTS.json
```

Run serially. POSIX SIGALRM supplies fixed60s stage/fixture guards.
No solver, CAS, external dataset or numerical library is required.
Optional `--write FILE` records the complete regenerated mathematical
record; it excludes timings so normal and optimized results can be compared.

Both modes print mathematical-record SHA256
`9c4803c6333dd9174d54511227a298cb84553c77d09b118319b2e3c981af4b4b`.
Observed normal/O elapsed12.985/14.374s, peak22080/24152KiB on Linux,
unchanged1CPU2GiB process scope. Literal guards n<=6,N<=80 protect
validation; they do not restrict the all-n theorem. No large corpus is omitted
from the proof, and no costly old native replay is resumed by this packet.

The replay checks:

- 13 leading determinant polynomials on q=4+t,t>=0: 459 strictly positive
  coefficients, positive row-clearing factors and463 separate scalar
  Gaussian determinant evaluations with justified polynomial degree bounds.
- 16 direct/packed coefficient multiplication and exact-division controls;
  rational symmetry, all64 Gram/cap sector cross positions, three exact
  K-orthogonal contrasts and the physical K slack17q-6/5.
- Nine scalar direct-Fraction/symbolic comparisons, 900 Gram and900 frame
  positions, including q=2^100. q=1000000 is only an auxiliary real parameter.
- Original n3..6 families of sizes16,24,40,72: 400 Gram and400 full-frame
  positions, all52 untouched high and48 untouched low eigenactions/crosses,
  actual empty rows/loops, original support/rows, full lower/upper PSD,
  seed scaled gap1 and repaired ranksN-1/scaled gap1/2.
- 12 coefficient/domain/determinant/empty/support/PSD/frame/census damages,
  all rejected in both normal and optimized execution.

[symbolic.py](symbolic.py) verifies the uniform algebra;
[univariate.py](univariate.py) is the credited earlier exact polynomial
engine instantiated in one variable, with bounded integer packing and
required exact division. [model.py](model.py) gives the complete10-coordinate
Gram/frame. [mixed.py](mixed.py) builds literal original vectors;
[exact.py](exact.py) retains the credited rational full-matrix checker.
[RESULTS.json](RESULTS.json) stores all compact polynomial fingerprints,
positive clearing-factor domains, identity bounds and original matrix hashes.
[SHA256SUMS](SHA256SUMS) identifies the source and compact evidence.
