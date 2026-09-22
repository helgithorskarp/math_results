# Gaussian law for the Ray--West correction on separable permutations

This directory proves a central limit theorem for the Ray--West
codimension-two correction `j` on a uniformly random separable permutation.
If `Pi_n` is uniform in `Av_n(2413,3142)`, then

```text
(j(Pi_n)-n/2) / sqrt((sqrt(2)-5/4)n)  ->  Normal(0,1).
```

The proof perturbs the dominant square-root singularity of the previously
derived bivariate algebraic generating function.  It also gives

```text
Var(j(Pi_n)) = (sqrt(2)-5/4)n + O(1).
```

See [THEOREM.md](THEOREM.md) for the proof and [SOURCES.md](SOURCES.md) for
the literature and novelty boundary.

## Reproduction

Python 3.11 or later and only the standard library are required.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify.py | diff -u EXPECTED_OUTPUT.json -
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
sha256sum -c SHA256SUMS
```

The exact audit constructs the discriminant directly from the published
quadratic equation, factors its specialization at `u=1`, evaluates all five
needed partial derivatives in `Q(rho)` with `rho^2-6rho+1=0`, and checks the
implicit-singularity and variance formulas.  It uses rational arithmetic only:
no floating point, external package, solver, or random choice is involved.

## Dependency and trust boundary

This result depends on the proved bivariate equation in
[`ray_west_separable_distribution`](../ray_west_separable_distribution/).
The present checker audits the new discriminant calculation; the earlier
directory independently checks that equation against the original active
two-insertion definition.

The universal limit law rests on the analytic proof in `THEOREM.md`, including
the uniqueness of the perturbed dominant singularity.  The checker verifies
the exact algebra used by that proof but does not numerically simulate a limit
distribution.
