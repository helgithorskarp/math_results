# Independent quantitative Sendov profile audit

Reviewer: six-reviewer-1, independent mathematical reviewer.

[REVIEW.md](REVIEW.md) confirms lemma8668's quantitative original-polynomial profile theorem and optimal next critical scale, within explicit prior concentration/bootstrap premises. It proves every fixed numerical penalty0<kappa<1/128, including1/256, with an existential error constant/collar. No global first-power, effective collar or sharp third-order optimum is claimed.

Run from a repository checkout containing the sibling `round-two/six-reviewer-1/quartic-boundary-audit/check.py`. Its exact source SHA256 is checked before import. Python3.11+, standard library only:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B round-two/six-reviewer-1/profile-stability-audit/check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O round-two/six-reviewer-1/profile-stability-audit/check.py
```

Both must pass72 independent exact checks and four damage controls and match [expected.json](expected.json). Optional `--author PATH/expected.json` additionally bridges every published family derivative/primitive/objective coefficient and constants. `--write` is a development option to regenerate the independent record, not validation of a changed fixture.

The new checker uses an independent moment Newton calculation, full six-variable constrained chart and full polynomial-in-profile root/family identities. Only the reviewer's published exact field kernel is reused. Uniform analytic arguments and all-original-root completeness are in the review, outside a formal kernel. One CPU/thread, no solver or extra package.
