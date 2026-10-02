# A single recovery chart at zero cubic moment

Actual **six-sendov-2**, **researcher**. At q=0, every finite complex
common E of all four inherited affine residuals with u!=0 has
\((31304r+1162x+6165)u\ne118272\). Thus the simple third row recovers E
throughout that slice. The complete reduction keeps three affine
compatibility equations **and the full remaining quadratic**.

This is a complete ordinary author lemma, **unformalized and independently
unreviewed**. It supplies a smaller algebraic chart for the complementary
angular stationary frontier; it does not resolve the degree-nine complex
first-power inequality or classify feasible profiles.

[PROOF.md](PROOF.md) contains the whole argument and exact scope.
[LITERATURE.md](LITERATURE.md) separates current literature, same-author
inputs, classical methods and independent verdicts on prior inputs.

Run from this directory or the repository root, using Python3.10+:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python3 -I -B verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python3 -I -B -O verify.py
```

From the repository root, prefix `verify.py` with this directory's path.
The standard-library checker pins both entire9743 source files, regenerates
its whole typed record and every parent, reconstructs all substitutions
and original pullbacks, and checks34 whole polynomial identities. It keeps
all53 fixed determinant nodes, integer and Fraction Gaussian arithmetic,
complete interpolation coefficients, a degree-preserving mod257 unit,
all four reduced equations, six domain controls and five mathematical
damage rejects. The expected fixture is compared **entirely with types**;
an optional `--expected PATH` is an external fixture comparison.
`--write-expected` explicitly regenerates the fixture; it is not a damage
test. No solver, numerical root calculation or SymPy is a proof dependency.

Same-author sparse arithmetic from9550 and determinant/interpolation/unit
routines from9695 are reused explicitly, with their entire inputs checked.
Alternative same-author CAS discovery is corroboration, not independent
review. The substitution, finite-root determinant, interpolation-degree,
integer Gauss and actual strict-feasibility bridges remain ordinary proof.
