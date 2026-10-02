# Global polar-routing independent audit

Actual agent **six-reviewer-3**, independent mathematical reviewer.
Read [REVIEW.md](REVIEW.md) and the complete [PROOF.md](PROOF.md).
Confirms the core global carrier of LEMMA9687 and proves H<82,000,000eta
on F<=8+3eta for actual closed-disk complex degree9,0<eta<=2^-16.
The credited fixed-energy bound now enters globally at
eta<=1/41,984,000,000. The sharp-profile appendix is assessed only as a
conditional transport of its explicitly cited local theorems. No full
first-power endpoint, optimal constant or formal proof is claimed.

Use standard-library CPython3.10+; checked with3.12.14. From repo root:

```bash
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python3 -B round-two/six-reviewer-3/global-polar-routing-audit/audit.py
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python3 -B -O round-two/six-reviewer-3/global-polar-routing-audit/audit.py
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python3 -B round-two/six-reviewer-3/global-polar-routing-audit/validate.py
```

Expected canonical record SHA256:
cb639ba53443b2f4ad80e7f972d9a2dfc7c243a7b5a65915c3ccedf3bb07c265.
Four whole polar certificates, eight exact radial profiles, three controls,
six mathematical-budget counterchecks, ten external fixture corruptions.
The independent core/proof seal precedes producer executable/fixture access.
Default invocations leave source and evidence unchanged. The explicit
audit.py --generate option replaces only the own compact EXPECTED.json.

Optional late data-only comparison, given the unchanged public author
fixture [EXPECTED.json](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-sendov-1/global-polar-routing/EXPECTED.json):

```bash
python3 -B round-two/six-reviewer-3/global-polar-routing-audit/compare_author.py --author-fixture round-two/six-sendov-1/global-polar-routing/EXPECTED.json
```

The optional fixture is not an input to audit.py or PROOF.md. Normal/O
unmodified producer verification and native validation are recorded in
AUTHOR_REPLAY.json; full later arithmetic comparison is in
AUTHOR_COMPARISON.json. Whole source hashes are in SHA256SUMS.
No CAS, solver, external package, root finder, large certificate or
unverified numerical output is required. Analytic universal reductions
remain ordinary written mathematics outside the checker.
