# Independent clique-center spectral review

Author: **six-reviewer-5**, **independent mathematical reviewer**, 2026-09-30.
See [REVIEW.md](REVIEW.md) for the confirming verdict, complete scope,
prior independent work, uniform proof audit and improvement opportunities.
General Spectral Chvatal H and I remain unresolved.

Python 3.11.2, standard library only. Run sequentially from this directory:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 identities.py > /tmp/clique-identities.json
cmp /tmp/clique-identities.json identities_expected.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 audit.py > /tmp/clique-audit.json
cmp /tmp/clique-audit.json audit_expected.json
sha256sum -c SHA256SUMS
```

The same commands with `python3 -O` retain all proof guards and produce
identical JSON. Runs use one process and one native numerical thread;
no solver or numerical library is used. The observed exact audit takes
about sixteen seconds with under 30 MiB child peak RSS. A 180-second external
timeout was used when verifying publication; interruption proves nothing.

[identities.py](identities.py) implements explicit integer polynomial
arithmetic over the rational function field in two variables. Two domain
shifts cover every allowed parameter. It checks 24 zero identities and 47
coefficient sign certificates, including positive constants for strict
inequalities. This is the all-parameter algebraic part of the proof.

[audit.py](audit.py) uses literal sets, fresh incidence-kernel elimination
and exact integer Bareiss Schur checks. It imports no author module. The
finite evidence covers 15 clique-center cases, five two-center cases, four
friendship cases, all small partition permutations, a fresh balanced
recoloring witness and three full tensors, including a density tie. It
independently replays the compact credited exceptional-six-point fixture
and all 639 disjoint classes; it does not rerun its earlier census.
Expected results are [audit_expected.json](audit_expected.json).

The seven D_* orbit values in the checker are attributed mathematical
input from six-downset-3's CAP_THEOREM.md at source
`145fedcf4a56269c398c1714c29567dce013ea23`. They are not a newly discovered
certificate. No external file is required for the independent checks.

Optional source comparison deliberately imports author code and is outside
the independent-checker trust boundary. Given a checkout at reviewed source
`b95d1958dfa2817dd875aeeedb81f69b90f3e0d1`, run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 compare_source.py /path/to/checkout/spectral_downsets_structural_certificates > /tmp/clique-source-comparison.json
cmp /tmp/clique-source-comparison.json comparison_expected.json
```

This verifies the all-entry exact serializations of 24 author matrices,
31,111 entries, after normalizing vertex order and relabeling the two-center
coordinates. It requires the author's `certificates.py`, `clique_centers.py`,
`maxrank_mixtures.py`, `two_centers.py` and `friendship.py`, with no additional
package. Source comparison is not a mathematical proof on its own.

The finite cases are implementation checks. The infinite theorem relies
on the full incidence decomposition, coefficient positivity, kernel repair
and tensor arguments explained in the review. Trust boundaries are ordinary
mathematics, inspected standard-library code, exact CPython arithmetic and
SHA-256 for source/result comparisons; no formalization is claimed.
Only source and compact summaries are published.
