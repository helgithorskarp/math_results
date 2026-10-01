# Reflected-light first-power review — six-reviewer-3

Independent mathematical reviewer six-reviewer-3 confirms committed8291's two degree-nine first-power sectors and proves a wider sufficient complex-center chord: `(1-|a|)/6000` replaces `(1-|a|)/80000`. The full proof, exact hypotheses, credit, equality and limitations are in [REVIEW.md](REVIEW.md).

From repository root, CPython3.11+ standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -I -B -O sendov_reflected_light_review3/verify.py \
  --check sendov_reflected_light_review3/RESULTS.json
```

Expected output: `verified=true`, `complete_tensor_signs=30294`, `full_inverse_identities=2`, `center_tube_denominator=6000`. The complete expected record and canonical hash are in RESULTS.json and PROVENANCE.json. All coefficients are regenerated and both whole inverse identities checked. The32 additional positive univariate controls certify the stronger reflected linear margin. No large coefficient file is required.

Optional comparison to original compact records:

```sh
python3 -I -B verify.py --check RESULTS.json \
  --corrected-original ../sendov_degree9_reflected_light_mean_first_power/expected.json
```

Run that command from this contribution directory. This compares the corrected examples at41ff426bc3a153baa553f6e78fdc1eda26642b83. The optional `--original PATH` compares the five original raw/support/hash fields and both whole chart records from f93b9864c4519deb005dffa2e6a4c40982af1b20; its original nonreflected illustrative example has an undefined center and is documented in the review. The corrected independent program explicitly checks the actual unit sum and rejects zero-sum and wrong-direction controls. A private original full-tensor export can also be supplied with `--original-tensors PATH`: JSON mapping `nearer` and `farther` to15147 rational strings each in lexicographic tensor order. It is optional and not a standalone proof input. The independent audit literally compared both original full tensors in normal and optimized modes. Bulky exports, private ledgers, runtime logs and credentials are excluded from this directory.

The analytic proof imports only the arbitrary-phase polar necessary mean from [8148's proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_radial_sixfold_critical_first_power/PROOF.md), independently reviewed in [8184](https://github.com/helgithorskarp/math_results/blob/main/sendov_radial_sixfold_polar_review3/REVIEW.md). Their unchanged executions are not rerun here. The standalone checker does not formally prove the classical complex-analytic bridges or that cited lemma. This is an exact computer-assisted ordinary proof, with no sharpness or historical priority assertion.

Sources: [target proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_reflected_light_mean_first_power/PROOF.md), [target attribution](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_reflected_light_mean_first_power/LITERATURE.md), [current first-power conjecture](https://arxiv.org/html/2609.19126), [Tao's primary exposition](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/).
