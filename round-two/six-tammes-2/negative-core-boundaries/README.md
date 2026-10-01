# Exact lower and critical-vertex boundaries for the negative-edge core

Actual author **six-tammes-2**, **researcher**, 2026-10-01.
Author-checked computer-assisted lemmas; independent review pending.

On the selected `(9,13)`-deleted thirteen-point core curve, an exact
packing selector forces `t>=1/sqrt(3)`. A second exact sign boundary
proves that the critical `(1,4,7)` avoidance vertex, when feasible, has
norm strictly below one for `t<tau`, the credited incumbent quintic root.
The complete statements and geometric reduction are in [PROOF.md](PROOF.md).
The two-arbitrary-point extension and global Tammes-15 problems remain open.

Use a full repository checkout containing the pinned prerequisite
[negative-cross-reduction](../negative-cross-reduction/README.md).
[INPUTS.json](INPUTS.json) records its exact source and hashes. That
classification is a required, separately reproducible theorem.

With Python 3.11, the new arithmetic and sign checker needs only stdlib:

```sh
python3 -B round-two/six-tammes-2/negative-core-boundaries/check.py
python3 -B round-two/six-tammes-2/negative-core-boundaries/controls.py
```

The checker verifies all four resultants, their factorizations, the
closed coefficient-pole and root-locus signs, and four exact dyadic sign
witnesses. Its complete output is compared with [EXPECTED.json](EXPECTED.json).
The four damaged-certificate controls must be rejected.

To reconstruct the geometric coefficients and determinants independently
of their supplied arrays, install the pinned CAS in a local venv:

```sh
python3 -m venv .scratch/tammes-boundary-venv
.scratch/tammes-boundary-venv/bin/pip install -r round-two/six-tammes-2/negative-core-boundaries/requirements.txt
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 .scratch/tammes-boundary-venv/bin/python -B round-two/six-tammes-2/negative-core-boundaries/geometry.py
```

It must report `GEOMETRY_REDERIVED` with four resultants and a verified
norm identity. To regenerate the compact certificate in scratch, append
`--generate .scratch/tammes-boundaries-regenerated.json`; compare its
bytes to `certificate.json`. The normal producer run compares every
entry before reporting success. No floating coordinates, solver verdict
or incomplete cover is a proof premise.

[VALIDATION.json](VALIDATION.json) records measurements, equality checks
and trust boundaries. The new certificate's canonical SHA256 is
`ffb1d90275eea114c6cbd7ca4f3315c11899f80f9f93696f78be64b119dc1be3`.
Exploratory cap-cover output is private and supplies no extension theorem.
