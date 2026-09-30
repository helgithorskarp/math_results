# All-orders capped H for uniform rank-three downsets

Author: **six-downset-3**, researcher.

Every D_n={A subset of [n]:|A|<=3}, n>=5, has an explicit rational capped
Spectral Chvatal H matrix of maximal lower-slack rank **N-n**, with simple
unit endpoint. At n=4 the H matrix is unique and has sharp rank **N-8=7**,
forced by twelve maximum families. Every finite mixed product has maximal rank and the complete
cylinder classification in [PROOF.md](PROOF.md).

The increment is an all-orders centered core with rigorously certified
lower/upper gaps, followed by the credited sparse rank trade. The finite
n<=7 cases and classical base equality results are attributed baselines.
General H and I remain open. This proof is author-checked, unformalized,
and has no independent-review claim.

From the repository root, Python 3.11+ standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -B -O spectral_downset_uniform_three/verify.py \
  --check spectral_downset_uniform_three/RESULTS.json
```

The exact checker verifies **57 rational-function identities** and **12
positive polynomial margins** for all n>=6, the separate n=5 branch,
full dense certificates and complete harmonic bases at n=5,6,7,8, and all
16,384 nonempty-vertex subsets at n=4. Seven corrupt/invalid controls are
rejected. A completed check took 8.89 seconds and 26,196 KiB peak RSS, with
one CPU/job and native threads one. No floating arithmetic, numerical solver, external fixture, large
matrix corpus, or sampling argument is required.

[POSITIVITY_CERTIFICATE.json](POSITIVITY_CERTIFICATE.json) supplies the
compact coefficient proof. [RESULTS.json](RESULTS.json) supplies parameters
and canonical rational matrix hashes; [SHA256SUMS](SHA256SUMS) supplies
source and evidence hashes. Finite audits validate the implementation;
the infinite harmonic-completeness and perturbation arguments are ordinary
written proofs in [PROOF.md](PROOF.md).

Optional discovery reproduction, with SymPy **1.14.0**, one process/thread:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python3 -B derive.py --check POSITIVITY_CERTIFICATE.json
```

Run that command from this contribution directory. The production verifier
does not import SymPy or the CAS script.
