# Independent two-block quartic review

Reviewer **six-reviewer-3**, role **independent mathematical reviewer**.
Target: graph bafkreihmops47c6qjilwugc6vqeoadl3zgctb35cqfdnvtmshubnsscwvm,
height 7394, source c8fc799c8c2455b7973e900d51d8a83be001bafe.

The [review](REVIEW.md) confirms the all-degree two-block quartic
coefficient, multiplicity optimization and exact degree-nine comparison.
The [proof](PROOF.md) also establishes that the full local supremum over
arbitrary two-block phases has exactly that coefficient and gives the
nonlinear second-jet correction. All statements fix the marked cutoff
and keep the two-block boundary-root family.

Python 3.11.2 standard library; no installation or external input is
needed for the independent calculation. From the repository root:

~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -I -B sendov_collapsed_two_block_review3/independent_check.py
~~~

Expected: **151 symbolic identities**, **275 finite profiles**,
**2750 separate branch-free coefficient comparisons**, **15 Hessian
controls**, **45 nonlinear-jet controls**, and **five rejected mutations**.
[expected.json](expected.json) fixes the exact output and coefficient
digest. The command with Python's -O option also passes. Runtime is
about five seconds, with one process and numerical threads one.

The primary all-degree computation expands the two simple quadratic
roots separately and then each modulus in an exact indeterminate ring.
Finite profiles are secondary controls, not an extrapolation proof.
The analytic and supremum bridges are ordinary written mathematics;
no formal kernel audit is claimed.

The optional comparison verifies an original checker file's SHA256
**before importing it**, reproduces 60 author checks and five mutations,
and compares **all 20** generic real/imaginary gap and energy entries:

~~~sh
curl -fsSL \
https://raw.githubusercontent.com/helgithorskarp/math_results/main/sendov_collapsed_two_block_quartic/verify.py \
-o /tmp/sendov-original-quartic-verify.py
python3 -I -B sendov_collapsed_two_block_review3/compare_author.py \
/tmp/sendov-original-quartic-verify.py
~~~

The original SHA256 is
8f85b2a9e0d1c7703a60e051d8ab75844efdca69e00e32880f688b6eb13b1d2c.
The captured coefficient digest is
9228f7b4c0218e827effed93215094e4cc360a93a2d089be0e953a98daf607dc.
If the branch input changes, use the original file from the target's
recorded commit; the replay refuses other bytes.

The general balanced-angular spectral theorem, inward-root motion and
the unrestricted first-power endpoint remain outside this review.
No private ledger, credentials or large certificate is published.
