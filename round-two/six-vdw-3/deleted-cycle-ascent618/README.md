# Exact five-term seed condition for three-column618 repairs

Agent six-vdw-3, researcher. [PROOF.md](PROOF.md) states the quantified lemma: an XOR-separable period618 baseline with no bad cyclic seven-AP outside any at most three mod103 columns must have a monochromatic five-term field progression outside those columns. This is a necessary repair seed, not an exclusion of all three-column repairs or a3704-point coloring. Independent peer review and formalization are unclaimed.

Use Python3.11.2, PySAT1.8.dev24, six1.17.0 and a C compiler. Each subprocess is serial, with every solver/BLAS/OpenMP thread set to1. All generated models and proof corpora stay in the chosen work directory, outside the public source. The program downloads the pinned strict checker and drat-trim C source, checks their SHA256 pins, and builds the untrusted converter.

```sh
python3.11 -m venv /tmp/vdw-deleted-ascent-env
/tmp/vdw-deleted-ascent-env/bin/pip install -r round-two/six-vdw-3/deleted-cycle-ascent618/requirements.txt
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  /tmp/vdw-deleted-ascent-env/bin/python round-two/six-vdw-3/deleted-cycle-ascent618/reproduce.py \
  --work /tmp/vdw-deleted-ascent-proof
```

Expected status `VERIFIED_ALL_THREE_HOLE_NO_FIVE_CASES`, eighteen refutations,162983 checked additions and5765067 propagation hints per Python mode. The complete raw176851-hole audit,1808 small orientations including606 positives,128 small pair inputs, damage guards and strict normal/O checks run automatically. `unrestricted_deleted_robustness_proved` and `W_bound_improved` remain false.

Native proposal limits are100000 conflicts and35 seconds, converter25 seconds internal/30 external, and strict replay50 seconds per child. UNKNOWN, timeout, a pin mismatch or a certificate discrepancy aborts without exclusion. Resource limits are not increased automatically. [expected.json](expected.json) was frozen before source validation; its SHA256 is `574581e629e1f74daf800a5b5f4395236f088cef7a9ad632a95779700585ec5a`. Per-case model and proof hashes are checked against it.

To replay existing private LRAT proposals, use `--resume PATH`, where PATH contains `lambda-2/model.lrat`,...,`lambda-47/model.lrat`. Every model is still regenerated and independently audited, every trace is replayed normally/O, and all coverage/positive controls repeat. Cached solver statuses are never accepted as proof. `--only 2` performs a selected pipeline smoke; it explicitly does not establish the full eighteen-case family. Optional `--tools PATH` uses pinned helper sources already present there. No bulky model or proof trace is included in Git.

The local pair-parity/ascent mechanism is credited to the [constant618 result](../separable618-exclusion/PROOF.md); the uncolored triple normalization to the [phase-three cut](../three-exception-orbits/PROOF.md); the separate-modulus motivation to the [three-column620 result](../../six-vdw-1/three-column-robust620/PROOF.md). None of their old refutations is substituted for the eighteen new deleted-model certificates. [verification.json](verification.json) records completed standalone validation and its precise fresh/cached scope.
