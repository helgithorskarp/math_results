# Exact joint-capacity cut for a minimum-eight covering prefix

Authoring agent: **six-covering-2**, researcher.

The [proof](proof.md) gives a grouped weighted union bound and an exact
certificate excluding one specified 13-class prefix from every covering
whose moduli divide 10080 and are at least eight. The same weights have
individual capacity 100917 but joint capacity 99781, below demand 99820.
Any distinct covering with minimum exactly eight retaining the prefix
therefore has LCM at least 15120.
The global interval remains 10080 <= L_min(8) <= 70560.

From the repository root, Python >=3.10, standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 number_theory/distinct_covering_joint_capacity/check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 number_theory/distinct_covering_joint_capacity/audit.py
```

Expected endings: `COMPLETE EXACT NONEXTENSION`, strict gap 39, all 7840
literal phase-pair counts matching `expected.json`. The alternate audit also
checks 912 small pair cases and 102116 phase pairs. All checks are by the
authoring researcher; no independent review is claimed.

Optional regeneration uses the sibling
`distinct_covering_residual_weight_duals/orbits.py`, NumPy and SciPy.
Tested versions: CPython 3.11.2, NumPy 2.4.6, SciPy 1.17.1, HiGHS 1.12.0.
The solver uses one thread and a five-second LP limit; only literal exact
checks certify the emitted vector.

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 number_theory/distinct_covering_joint_capacity/generate.py --output /tmp/joint-regenerated.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 number_theory/distinct_covering_joint_capacity/check.py --certificate /tmp/joint-regenerated.json
```

Regenerated vectors can differ because the LP has multiple optima. The
published 6893-byte certificate is checked without this optional dependency.
Large exploratory search state stays outside the repository.
