# One quartic candidate for the negative-edge Tammes core

Actual author **six-tammes-2**, role **researcher**, 2026-10-01.
Author-checked computer-assisted reduction; independent review pending.

Delete `(9,13)` from the 24-contact thirteen-point asymmetric core.
For every `t in [14/25,593/1000]`, its packing realizations must lie on one
explicit quartic curve, unique up to O(3) for each feasible t. The proof
covers eight formal orientations, all rank/denominator/chart exceptions,
and excludes seven models by exact packing inequalities. It does not
prove that the remaining curve admits a packing for every t, exclude its
two-point extensions, or establish global Tammes-15 optimality.

Read [PROOF.md](PROOF.md), especially the scope and next extension test.
The signed local deletion behavior is already in independent review 7288.

From a full repository checkout, install the pinned CAS into a local venv:

```sh
python3 -m venv .scratch/negative-cross-venv
.scratch/negative-cross-venv/bin/pip install -r round-two/six-tammes-2/negative-cross-reduction/requirements.txt
```

Use one native-library thread (`OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`).
Run the algebra and standard-library audit first:

```sh
.scratch/negative-cross-venv/bin/python -B round-two/six-tammes-2/negative-cross-reduction/check.py
python3 -B round-two/six-tammes-2/negative-cross-reduction/audit.py
```

Run the six exact packing exclusions as separate resumable jobs:

```sh
python3 -B round-two/six-tammes-2/negative-cross-reduction/packing.py --branch 0
python3 -B round-two/six-tammes-2/negative-cross-reduction/packing.py --branch 1
python3 -B round-two/six-tammes-2/negative-cross-reduction/packing.py --branch 2
python3 -B round-two/six-tammes-2/negative-cross-reduction/packing.py --branch 3
python3 -B round-two/six-tammes-2/negative-cross-reduction/packing.py --branch 4
python3 -B round-two/six-tammes-2/negative-cross-reduction/packing.py --branch 5
```

To preserve a trace locally, add `--trace .scratch/branch0.trace.json`.
Verify it later with `--replay .scratch/branch0.trace.json` and the same
branch argument. Each trace contains all closed parameter pieces and
root brackets; `packing.py` checks full coverage and the published hash.
Bulky traces stay outside the contribution directory.

Run damaged-certificate and direct arithmetic controls using the small
branch-one trace:

```sh
python3 -B round-two/six-tammes-2/negative-cross-reduction/packing.py --branch 1 --trace .scratch/branch1.trace.json
python3 -B round-two/six-tammes-2/negative-cross-reduction/controls.py --trace .scratch/branch1.trace.json
```

Regenerate the compact algebra certificate with
`check.py --generate .scratch/negative-cross-regenerated.json` using the
CAS venv. Compare its exact bytes with `certificate.json`.
`SELECT_EXPECTED.json` records canonical trace hashes and exact minimum
gap bounds. No floating-point input, solver verdict or timeout is a
mathematical premise. The arithmetic audit is by the same author and
does not replace an independent researcher review.
