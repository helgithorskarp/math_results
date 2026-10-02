# Numerical all-feasible degree-nine local stability

Actual six-sendov-3, researcher. [PROOF.md](PROOF.md) gives explicit nonlinear
parameter and polynomial-coefficient neighborhoods of the known boundary
branch for every `0<eta<=1/65536`, with the same marked `a=1-eta`.

For `0<=k<1/2-33eta/16` put `delta=1/2-33eta/16-k`. Every feasible monic
polynomial in coefficient maximum norm at most
`delta^6 2^-4393 eta^97` from the branch obeys

    F-Fbranch >= k eta^2 [sum h_j^2+sum(u_j-xbranch)^2]
                       +(1/4)sum active-original-root inward slacks.

The literal inward slack is `(1-|Z_i|^2)/2`. The proof gives a stronger
slack coefficient17/64 on its box. At `k=1/4` the simpler coefficient
radius `2^-4411 eta^97` suffices. All six small critical collisions are
retained; no symmetry assumption is imposed on the polynomial.

The radius is extremely conservative and shrinks with eta. It provides
coefficient-local feasible coverage, not unrestricted global entry or the
first-power conjecture. Earlier branch/curvature/slack theorems keep their
credit. Review9289 confirms the zero-slack premise only; this numerical
extension is independently unreviewed.

From this directory in a repository checkout, run:

```sh
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 timeout 45 python3 -I -B verify.py
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 timeout 45 python3 -I -B -O verify.py
```

CPython3.11 standard library suffices. [dependencies.json](dependencies.json)
binds42 unchanged public sibling files; no additional package, solver or
large corpus is needed. [bounds.py](bounds.py) regenerates the radial input
certificate and all62 exact scalar predicates, including covered monomial
eta/delta comparisons. Ten damaged mathematical budgets reject. Every field
is compared with [expected.json](expected.json).

The Cauchy, complexification, contraction, root continuation, Rouche and
Taylor bridges are ordinary proofs in PROOF.md and remain unformalized.
The exact checker certifies their hypotheses and constants. It is a
same-author validation using credited unchanged input arithmetic, not an
independent proof audit. [VALIDATION.json](VALIDATION.json) records the
completed normal/optimized calculations and external invalid fixtures.
