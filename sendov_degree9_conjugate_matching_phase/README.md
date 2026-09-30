# Complex-phase first power through conjugate matching

Author: **six-sendov-1**, role **researcher**. Date: 2026-09-30.

For a degree-nine disk-root polynomial and an interior marked root
$\alpha\ne0$, rotate its eight critical reciprocals toward the root:
$q_j=(\alpha/|\alpha|)/(\alpha-\zeta_j)$. A singleton has defect
$|q_j-|q_j||$; a paired pair of indices has defect
$|q_i-\overline{q_j}|$. Let $M_*$ be the least sum of these defects over
all 764 partitions into singletons and pairs. Then

$$M_*^2\le\frac{1-|\alpha|}{9000}
\quad\Longrightarrow\quad
\sum_j|\alpha-\zeta_j|^{-1}>8.$$

Matched reciprocals may have large individual angles. No coefficient
symmetry or critical-count hypothesis is imposed. The origin root is
unconditionally strict; a critical-root collision gives infinity.
This is a sufficient criterion, not the unrestricted first-power theorem.

[PROOF.md](PROOF.md) gives the disk-preserving cosine lift, the stronger
radius-dependent quadratic origin estimate, and an exact complex-coefficient
example outside the positive-axis and product sufficient criteria.
[LITERATURE.md](LITERATURE.md) compares the claim to the primary endpoint
conjecture, the published symmetry input and the already-known quadratic
positive-axis estimate. The new feature is approximate conjugate matching,
not the quadratic order of positive-axis perturbations.

The written proof uses the
[published uniform origin lemma](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_real_root_first_power/PROOF.md).
Independent review of that extension and this one is pending. No external
formalization was rebuilt; bounded literature searches do not establish
historical priority.

From a checkout containing this directory and the cited input directory,
run with Python **3.11 or later**, standard library only:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 python3 sendov_degree9_conjugate_matching_phase/verify.py
```

Expected output is [expected.json](expected.json): five complete symbolic
identities, two further example identities, exact constants by two integral
formulas, all 764 matching partitions, dynamic programming compared with
enumeration on three exact tables, the example's rational bounds, four
input-source hashes, and three rejected corruptions. Arithmetic uses
`fractions.Fraction` and unbounded Python integers. Source hashes identify
the dependency; they do not check its positivity certificate. Replay that
certificate separately:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 python3 sendov_degree9_real_root_first_power/verify.py
```

That run checks all 186577 original and strengthened coefficients, complete
identities and rational subdivision coverage. It needs one CPU, about a
minute and about 100 MiB in the observed environment. The present compact
checker takes well under a second. There are no numerical root searches,
solver claims, external coefficient files or large new proof corpora.

[matching.py](matching.py) supplies an exact finite cost-table utility:
enumerate the 764 partitions, or find the minimum using at most 256 subset
states. It accepts certified costs; it does not compute or certify complex
polynomial roots. The proof's Gauss--Lucas, published origin lemma,
geometric inequalities, AM--GM and Taylor argument remain ordinary
mathematics outside this finite code. The remaining frontier is to control
the matching loss for arbitrary complex reciprocal configurations.
