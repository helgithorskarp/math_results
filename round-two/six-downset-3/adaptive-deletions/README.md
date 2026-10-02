# Adaptive triangle-link deletions

**six-downset-3, researcher.** Author-checked ordinary proof; unformalized
and independently unreviewed. General Spectral Chvátal H/I remain open.

For q>=4 outside points and any k deleted triples bcx, 1<=k<=q, this
packet constructs capped greatest-rank H whenever

```
B0=[q²+(7-6k)q+2k²-12k+8]/2>0.
```

The exact cutoffs in q for k=1..6 are4,7,12,18,24,29. The proof covers
every labelled choice of deletions through a canonical permutation
argument. It gives a closed rational repair interval, whole spectral
gap, unique a-star, and eligible-factor product equality classification.
The scalar sufficient criterion is feasible for some positive parameter
exactly in this region; this is not an H obstruction outside the region.

[PROOF.md](PROOF.md) contains the full quantified ordinary proof and
credits. [EXPECTED.json](EXPECTED.json) contains all14 leading determinant
coefficients,18 upper margins, five small exact bridge forms, and15
original-domain phases. [RESULTS.json](RESULTS.json) is the compact summary.

Use Python3.11+ and the standard library only, with the repository
directory layout intact. Six small published inputs in sibling
triangle-majority and two-deletion-kappa are SHA-verified before import.
Their exact commits are recorded in [bootstrap.py](bootstrap.py).

From this directory:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 verify.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -O verify.py
```

The complete deterministic outputs must match EXPECTED.json. The record
SHA256 is `33f4947bd0c5a319edd28635563bc69744903e2d1d59e0a4d6c959847d903e73`.
One exact child runs at a time, with a fixed60-second limit per task.
The largest original fixture has N=155. Typical total replay is about
two minutes; each task prints a short progress message to stderr.
An interrupted or timed-out check is incomplete operational validation,
never mathematical nonexistence. Do not increase the published bound
or interpret only a partial replay as the whole certificate.

A single resumable phase can be run independently:

```sh
python3 verify.py --task endpoint
python3 verify.py --task original 12 3 whole-gap
```

`original.py` explicitly bounds full allocations to q<=12, retained
N<=155 (undeleted N0<=158). Its matrix builder uses original subsets,
not the symbolic sector decoder. `entries.py` has a separate API for
arbitrary admissible q,k, without allocating the downset or k deleted
columns:

```python
from fractions import Fraction
from entries import certificate

parameters, entry = certificate(12, 3)   # t defaults to exact tau
print(parameters['kappa'])              # 6355/724352
print(entry(0, 0))                       # 52654149/83300480
print(entry(1, 2))                       # a,b entry
parameters, entry = certificate(1000000, 100000, Fraction(1, 10**12))
```

Member masks use bits0,1,2 for a,b,c and bits3..q+2 for the outside
points. The canonical deleted group consists of the first k outside
points. The API rejects deleted members, inexact inputs, and t outside
the proved closed interval. It reads a constant-size type table and
examines at most two outside points in a member. The theorem also
allows real t; the implementation intentionally uses exact rational t.

`checks.py` includes31 rejection controls for mathematical/arithmetic
damage: changed dependencies, unmet hypotheses, coefficient signs,
missing balancing edges, lost empty vertex, bad support/rows/symmetry,
and an indefinite smaller-singleton substitute. Guards survive -O.
The Schur and small characteristic checks are two methods by the same
author, not independent peer review or proof-assistant formalization.
