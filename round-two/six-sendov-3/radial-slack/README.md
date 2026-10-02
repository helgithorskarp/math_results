# Four original-root slacks on the effective degree-nine branch

Actual author **six-sendov-3**, role **researcher**. The complete statement
and ordinary analytic bridges are in [PROOF.md](PROOF.md). For every fixed
`0<eta<=1/65536`, this extends9225's zero-slack complex stability to all
nearby disk-rooted monic degree-nine polynomials with marked root `a=1-eta`.
The individual original-root derivatives are in `(-3,-1/4)` for radial
coordinates `alpha=(|Z|^2-1)/2`. The local bound is

    F-F_branch >= kappa eta^2 [sum h_j^2+sum(u_j-x)^2]
                         +(1/4)sum(-alpha_k^±),
    any 0<=kappa<lambda_R/(2eta^2).

The local feasible supremum remains lambda_R/(2eta^2), with the sharper
real interval credited to9203 via9225. The coefficient1/4 is admissible
for kappa throughout this eta interval. Review9174's credited branch surplus
`F_branch>8+(181/64)eta` then gives the same local first-power surplus plus
the two stability penalties. Neighborhood radii are existential
at each fixed eta. No numerical radius, global entry or full first-power
solution is claimed. This new extension and its complex9225 premise are
independently unreviewed; older real/branch reviews retain their scope.

From the repository root use standard-library CPython3.11.2 or compatible:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -I -B round-two/six-sendov-3/radial-slack/verify.py
```

The same command with `-O` must give the identical complete output. The
checker hashes29 unchanged public sibling files before importing them;
include all of `radial-slack`, `complex-sector` and `centered-real-sector`
when using a sparse checkout. Versioned byte lengths and SHA256 are in
[dependencies.json](dependencies.json). No dependency source is duplicated.

The complete [expected.json](expected.json) is regenerated entry by entry.
Canonical full-record SHA256:
`6056fc5a2305629f5ed605e03dd755f9976bd03a699a3d8ec815b86bff7e9aab`.
Expected compact output includes `PASS`,60 exact metric/partial controls,
three positive-eta whole records,11 mathematical damages rejected, four
internal fixture damages rejected and every-field Fraction endpoint
agreement. Covered bounds are `det J>1/16`, `det O<-1/100`, full signed
four-radial determinant divided by eta^5 below `-1/6400`, and individual
root multipliers in `(1/4,3)`. Fraction recomputation shares the formulas
and source, so it is same-author arithmetic corroboration, not review.

`--fixture PATH` checks alternate evidence and rejects missing, malformed
or altered files. `--freeze` regenerates a reviewable fixture for maintenance;
it does not validate an existing fixture. No float predicate, solver,
sample-based coverage or large private input is used. Finite factor/norm
checks support formulas whose universal analytic justification is in the
proof. IFT, root-multiset continuity, actual feasible-segment coverage and
Taylor/integration arguments remain ordinary, unformalized mathematics.

The full known9225 baseline was exactly reproduced before using it;
reproduction is validation, not novelty or an independent verdict. Serial
normal/O validation, peak memory and45-second child guards are recorded
in [VALIDATION.json](VALIDATION.json).
