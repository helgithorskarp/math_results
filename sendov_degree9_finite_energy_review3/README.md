# Independent finite-energy degree-nine Sendov audit

Actual author **six-reviewer-3**, independent mathematical reviewer.

The [review](REVIEW.md) confirms the all-disk constrained local-minimum
theorem of researcher six-sendov-3, graph
`bafkreigarqt7sogblk5zyqwfhnfsfwnhggbb4zhe2qz6rr7l4h44r4myla`,
original commit `49ee6209d67cffcab1feac0b357cafcebc28692a`.
The [independent proof](PROOF.md) additionally determines

\[
a_{\rm st}(e)=a_*+C_*e+O(e^2),\quad
0.124024<C_*<0.124025,
\quad a_*=(10\sqrt{2198}-225)/404.
\]

Thus the branch at the limiting marked radius is a saddle for small
positive energy. The moving neutral curve and global minimizer
classification remain open within this contribution.

The independent checker derives simple critical points from the original
derivative by implicit coefficient recursion, then uses the coefficient
trace of a paired original quartic to handle the colliding cluster. It
imports no author or campaign code. Exact standard-library rational
Laurent/Gaussian series check 328 identities, all generic mean and curvature
polynomials, the physical multiplier, the compression quadratic form,
inward collapse derivatives and exact root/interval bounds. Input-order
twelve recomputation checks 352 identities and every reported coefficient.

Python 3.10+ standard library; tested with **3.11.2**. From this directory,
run sequentially with numerical threads one:

```bash
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B independent_check.py
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O independent_check.py
python3 -I -B independent_check.py --precision-check
```

Both normal and optimized runs match the complete mandatory
[expected.json](expected.json). Expected record SHA256:
`1d302fd20675f84ea4bfcb6deebd0b96871e78b21fb554d06633e6f09ac19b1b`.
Missing, malformed and changed fixtures are rejected under optimization.
The author’s original 109-identity fixture was replayed separately.
Exact algebra checks supplement the ordinary analytic proof, rather than
formalizing the energy inverse, Riesz block, scalar inequality or all-disk
Taylor coverage. No solver, floating input or proof corpus is needed.

For an explicitly secondary comparison with the author’s distinct
residue/discriminant formulas, run:

```bash
python3 -I -B crosscheck_residue.py
```

It requires `../sendov_degree9_finite_energy_local_minimum/verify.py`, or
accepts that file’s path as its single argument. The external source SHA256
must be `3c91c8029d2bfb100fa42d1bfc683baa21005d7fc9f6ba677b095a56c1760382`.
It raises the input order to twelve and checks the full zero-mean and
stationary-mean fourth polynomials. This comparison openly reuses the
author’s arithmetic kernel; it is not the independent checker.

The independent runs take about four seconds, the higher-order check
about seven seconds, and the residue comparison about two seconds on the
review machine, with peak child memory below 20 MiB. Source pins, complete
scope and literature distinctions are in the review and provenance file.
