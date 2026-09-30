# True degree-nine excess and sharp uniform stability

Actual author **six-sendov-3**, role **researcher**, 2026-09-30.
Complete ordinary author proof; independent review of this extension is
pending. Constants and thresholds are existential; no formal kernel is used.

For the first-power critical-reciprocal sum `F`, small fixed reciprocal
energy `E`, and the actual stationary one-plus-seven original-root branch,
[PROOF.md](PROOF.md) proves a uniform two-sided leading excess law:

    C = 2v^2 sum inward depths + 5v^3(mean error)^2
                            + L(a)t^2 ||seven-root split||^2,
    |F-F_branch-C| <= C_K t C,
    v=1/(1+a), t^2=E/(56v^4)+O(E^2).

The exact credited mean and energy inversion are used. The coefficients
are the known local coefficients; the new result identifies them for the
**true** objective with uniform relative error, even when all perturbation
coordinates shrink with energy or critical points collide.

The argument proves the missing harmonic support defect is `O(t^8)`
on every bounded chart

    split=t^2 x, mean error=t^3 y, inward=t^6 r.

More precisely the defect is bounded by a constant times
`t^8 (||x||^2+y^2)^2+t^12(sum r)^2`. An invariant graph in a fixed rational
complementary basis produces the complete normalized six-point matrix
through degree three. Its two coefficients are explicitly real symmetric.
The proof uses no individually smooth critical-root labels.

The
[preceding fixed-rectangle theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_fixed_rectangle_minimizers/PROOF.md)
then puts **every** full-disk polynomial with `F-F_min<=D E^3`, for
any fixed finite `D`, into such a bounded chart on one fixed rectangle
`0<=a-5/8<=delta0`, `0<E<e_D`. There is no bound on `(a-5/8)^2/E`.
This gives the global two-sided sharp-cost law for that entire class.
It does not solve the unrestricted first-power endpoint.

## Reproduction

From this directory with **CPython3.11.2**, standard library only:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -I -B verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -I -B -O verify.py
```

Both executions regenerate and compare the required `expected.json`
entry by entry: **23 exact universal matrix identities**, all six
independent balanced split coordinates, and **six corruption controls**.
The full eight-dimensional original matrix is compressed algebraically;
no sampling or floating eigenvectors enter. The complete record SHA256 is

    871dd579653616f450c6b539530b99916c96bdf6fb55dee367c705f5923bddd3

Missing/malformed/altered fixtures reject under `-O`. Only the explicit
development flag `--emit-fixture` regenerates the fixture; ordinary
verification requires its existing complete contents. The rational
polynomial kernel is openly adapted from the author's
[fixed-rectangle checker](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_fixed_rectangle_minimizers/verify.py).
The new block calculation is self-contained and imports no campaign module.

The credited prior parabolic **115 identities** were separately replayed
with the unchanged full fixture and record hash
`ae0ac904749e673382b24e820c59c30d3bb1687d6c863db56a06292da0c68ac3`.
That is baseline validation, not new research or independent review.
From the repository root:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -I -B sendov_degree9_parabolic_energy_classification/verify.py
```

New exact computation takes about one second and little memory. Numerical
threads are one; mathematical jobs run sequentially. The graph IFT,
uniform remainders, radial derivative powers, scalar support, Rayleigh
estimates, relative integration and cited global completeness remain
ordinary written mathematics. No solver, external package, floating proof
input, private data or large proof corpus is required. See
[LITERATURE.md](LITERATURE.md) for exact attribution and review boundaries.
