# Independent degree-nine critical 4+4 review

Actual author **six-reviewer-5**, role **independent mathematical reviewer**,
2026-09-30. The shared campaign signing key does not distinguish authors.

[REVIEW.md](REVIEW.md) confirms the first-power Tang--Zhang inequality for
every degree-nine complex disk-root polynomial whose derivative has critical
multiplicities **4+4**, allowing the two critical points to coincide. It
checks strictness at interior marked roots and the regular-polynomial
boundary equality case. It does not prove the unrestricted conjecture.

The fresh checker also proves a quantitative origin-norm margin on the
target's weighted domain and an exact necessary curved phase/imbalance
boundary for hypothetical failures. These refinements have ordinary written
proofs in the review. They do not give an optimal gap or an original-root
stability theorem.

Run these commands **sequentially**, with Python **3.10+**, standard library:

~~~bash
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B audit.py
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O audit.py
~~~

Each emits deterministic JSON matching [audit-summary.json](audit-summary.json)
and progress to stderr. Expected **PASS**, **1,485,732** complete exact
Bernstein sign coefficients, 13 cells including the equality corner,
23 polar-mean coefficients, 64 signed Gaussian controls and five rejected
corruptions. All proof guards use explicit exceptions, including under `-O`.
No mutable manifest or output-generation option exists.

- [kernel.py](kernel.py) freshly expands eight linear factors with integer
  Gaussian coefficients in the circle quotient ring, integrates exactly,
  squares the full real and imaginary polynomials and extracts both signed
  norm kernels. It then reimplements the elementary binomial weighted
  substitution and the two rational envelopes. No author code is imported.
- [tensors.py](tensors.py) fuses affine cell substitution and Bernstein
  conversion in univariate matrices and applies the axes in reverse order.
  Every matrix is checked on every monomial by the exact inverse basis
  identity. It uses no de Casteljau routine. Every coefficient, minimum,
  zero support and required strictness slice is checked.
- [audit.py](audit.py) independently specifies the closed cell covers,
  checks the full target and prerequisite certificates, regenerates the
  weak polar mean, and checks an actual nonreal disk-root polynomial.

The small [full_expected.json](full_expected.json) and
[individual_expected.json](individual_expected.json) are untrusted copied
researcher manifests, used only to compare freshly computed exact records.
Neither supplies a polynomial, sign decision or domain to the checker.
Their SHA256 hashes are respectively
`7def1dcf74c07f489584b9311f3c5ca0ad027dbfd5be6c9e2ae32abed848c867` and
`a6ca108d3b0a0e79b70b2e8c4903a13e01a95f26172e791e1c6c70665668bbc1`.
The first comes from source commit
`49de03a4636330c86a240bc97d772720991ae548`, directory
`sendov_degree9_full_critical_four_four_first_power`; the second from
`d8de4379e95fc2d3030ab6df3dd4cb971702c5eb`, directory
`sendov_degree9_individual_phase_sheet_origin`. Researcher code was read
to audit its claim and manifests, but not reused in this executable.

This is exact computer-assisted ordinary mathematics, not a formalization.
The interpreter, integer/rational implementation and the written reduction
to continuous parameter domains remain explicit trust boundaries. No solver,
floating proof input, external census, large certificate corpus or private
state is required. Full tensors are regenerated rather than published.
