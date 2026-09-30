# A whole five-level degree-nine displacement bound

Actual author **six-sendov-2**, role **researcher**, 2026-09-30.
Complete ordinary author proof with exact rational continuous-domain
certificates; independent review of this extension is pending.

For a balanced real eight-vector with `max|theta|=1`, use the credited
angular functional

    J = 122 mu2 + (224 mu4 - 5760 Psi)/mu2,
    Psi = sum over distinct compression eigenspaces of ||Pi w||^4.

The new bound is **J<=786 throughout the entire 3+2+1+1+1 class**, with
arbitrary asymmetry, all saturation choices and all label collisions.
Combining this with the
[preceding two-cohort exclusions](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_five_level_moment_reduction/PROOF.md)
gives **J<=786 for every profile with at most five actual levels**.
The credited four-level comparison has J*=785.7538723...; the exact
five-level maximum is not established.

The complex disk-root corollary concerns the stronger local comparison
sum_critical |a-zeta|^-1 >= 16/(1+a) near the collapsed other roots.
For the entire class with at most five original phase values and
independent inward depths,

    liminf as a decreases to 5/8 of R5(a)^2/((1+a)(a-5/8)) >= 53248/1965.

The new lower coefficient is 27.0982188.... The credited four-phase
comparison gives a limsup upper coefficient in (27.106707,27.106708).
No exact five-phase basin limit, effective radius cutoff, unrestricted
angular optimum or full first-power Tang--Zhang theorem is claimed.
[PROOF.md](PROOF.md) defines the quantities and proves the statements;
[LITERATURE.md](LITERATURE.md) records attribution and exact dependencies.

From this directory, run the two commands sequentially with Python 3.11
or a compatible newer Python. Only the standard library is required.

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B verify.py
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O verify.py
```

Both author runs with Python 3.11.2 passed **74,275 checks**. The replay
derives its polynomials, checks **59,671 bound-sign entries** and **320
physical/order sign entries**, and covers six full cubes by **49 closed
leaves**: 10 four-moment, 17 three-moment and 22 dimension/moment leaves.
It also checks 147 subdivision basis identities, 15 whole direct affine
leaf reconstructions, 19 distinct full-compression profiles and 60 closed
inverse-chart round trips. These controls supplement the written proof;
sampled profiles alone would not certify a continuous domain.

The canonical complete-record SHA256 is

    fd2b8eb1a0208fab9fb2d3120eccc31a4bca960bb43bd7bd67c0eb8757f245f4

cover.json supplies only complete binary bisection trees and terminal
method names. expected.json is a compact complete regression record;
all its polynomial and coefficient hashes, minima, controls and counts
are regenerated. Six deliberate damaged-input controls were rejected
under Python optimization, including omitted domains/children and altered
sign or compression records. Author replay used under 38 MiB peak child
RSS; the two valid modes took about 50 and 47 seconds on the campaign machine.

The Frobenius projection lemma, spectral interpretation, section
completeness, collision extension, credited cohort exclusions and uniform
analytic basin conversion are ordinary written mathematics outside a
formal proof kernel. The source imports no campaign code, numerical
proof input, private data or external solver. Source publication and
author checks do not constitute independent peer review.
