# Independent review of the universal seven-factor sign

**Verdict: accept at the stated scope.** R8's theorem proves
`b_(j+7,j)>=0` for every j>=0, every bounded probability law on R3, every
1-Lipschitz image and every positive Gaussian variance. Its strictness,
polarized signs and quantitative distance-loss bound are also accepted.
The first generally unsigned entry is now `b_(8,0)`; full majorisation
and new Kneser--Poulsen consequences are not proved by this result.

The [review](REVIEW.md) independently checks the finite-base recentering,
the Gram-polynomial decomposition and all normalizations. Its
[exact checker](independent_check.py) reconstructs the matrices and derives
their annihilating polynomials by a transitive Krylov calculation. It uses
neither the author's programs/expected output nor their supplied spectral
roots or fraction-free elimination certificate.

Reviewed source commit: `f5bbd92be43517c18a6958acf900ddd67bac62f8`.
The [input record](INPUTS.json) pins the reviewed proof. This is an
independent team-agent review of the new argument, with upstream R5
authorship disclosed in the review; it is not external human peer review
or a proof-assistant formalization.

From the repository root, with standard-library CPython3.11 or later:

```sh
python3 -B probability/gaussian_seven_factor_review_r5/independent_check.py
python3 -B -O probability/gaussian_seven_factor_review_r5/independent_check.py
```

Both report `R5_SEVEN_FACTOR_INDEPENDENT_PSD_REVIEW_PASS` and normalized
record SHA256 `ecf53f070ee048e1ec2fad48182b2abe48c409ce47a2685d69ab9bfb71ecb30a`.
The [compact record](EXPECTED.json) contains the derived polynomials,
complete coefficient counts, matrix hashes and rejection controls.
The replay takes about one second in the reviewer environment. No large
certificate, solver, numerical eigenvalue or omitted data is required.
