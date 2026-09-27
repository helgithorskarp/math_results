# Parity alignment signs the full Gaussian hinge curve

The [author proof](PROOF.md) compares every Gaussian hinge, at every
positive variance, when complete even-sign orbits are aligned to one
parity. Orbit masses, axis lengths, the number of orbits, and bounded
nonatomic mixtures are arbitrary. An explicit two-point doubly stochastic
kernel proves the comparison. No tail or middle-threshold approximation
is used.

Following alignment by a nonnegative radial contraction preserves the
comparison. This signs the existing eight-site indecomposable benchmark
`(v_i,-20v_i) -> (v_i,(58/3)v_i)` for all priors constant on each of its
two tetrahedral orbits. The target's uniform contraction by `1-2^-20`
is covered as well. Arbitrary atom priors and the whole spatial
perturbation box are not covered.

Another direct application is the contraction
`T(x)=sign(x1*x2*x3)x/4` on `1<=|x_j|<=2`. Every law there invariant
under changing two coordinate signs is covered, including diffuse laws.

For finite complete orbits, both ball-union and ball-intersection volumes
have the corresponding signs, with arbitrary radii constant within each
orbit. The proof includes both limiting arguments. Alignment itself need
not be a contraction; applications to the named question require the
complete prescribed endpoint map to be 1-Lipschitz. The eight-site example
meets that condition.

The theorem and stated applications now have an
[independent correctness acceptance](ACCEPTANCE.md). Historical novelty of
the ball-volume consequence is not established. Full unrestricted
majorisation remains open. [SOURCES.md](SOURCES.md) gives the scope and
dependency boundaries.

From the repository root, standard-library Python 3.11 or later:

```sh
python3 -B probability/gaussian_parity_alignment/verify.py --check
python3 -B -O probability/gaussian_parity_alignment/verify.py --check
```

Expected status: `PARITY_ALIGNMENT_EXACT_CONTROLS_PASS`.
[EXPECTED.json](EXPECTED.json) records exact orbit identities, doubly
stochastic witnesses, hinge breakpoints, the sixteen-state interval check,
the eight-site geometry, and rejected malformed controls. These checks
support the written proof; they are not an independent review or numerical
Gaussian integration.
