# Independent global-energy Sendov audit and parabolic window

**six-reviewer-4**, independent mathematical reviewer, 2026-09-30.
[REVIEW.md](REVIEW.md) confirms h7839 with its h7857 one-sided basin
clarification. [PROOF.md](PROOF.md) audits the uniform scaled-domain
bridge and proves that the exact degree-nine global fixed-energy
minimizer classification holds on one fixed small window
\(0\le a-5/8\le\gamma\sqrt E\), for sufficiently small positive \(E\).
The only minimizers are the actual stationary singleton/seven branch
and its conjugate, with all original roots allowed in the closed disk.
The positive constants remain existential. The unrestricted first-power
endpoint and arbitrary-energy classification remain outside scope.

The independent checker regenerates the generic true energy chart
in all six zero-sum split coordinates, exact divided compression,
weighted degree list, original/reciprocal mean conversion and precise
positive-cost constants. It imports no author or campaign executable
module. The written analytic proof and reviewed local/sextic premises
remain explicit trust boundaries.

Use CPython >=3.11 and SymPy 1.14.0 from this directory:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
.venv/bin/python -B audit.py --check
.venv/bin/python -B -O audit.py --check
sha256sum -c SHA256SUMS
```

The neighboring target/local-review/sextic-review source directories
must be present in the repository. Pass `--repository /path/to/math_results`
to use a different root. `provenance.json` pins all required source inputs;
they are hash-checked, not imported. Omit `--check` to regenerate the
complete compact independent output for comparison with `EXPECTED.json`.
The fixture is comparison-only. Six algebra corruption controls remain
active under optimized Python. `validation.json` records completed runs,
versions and resource measurements.

Every run uses one CPU, native threads one, and fits the authorized
2 GiB scope. No large corpus, solver, numerical premise or formal kernel
is required. Verified source commit metadata accompanies the graph
review and durable campaign checkpoint; reader-facing URLs use main.
