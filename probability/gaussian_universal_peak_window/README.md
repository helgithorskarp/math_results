# A universal upper-density Gaussian hinge window

Complete analytic author proof, 27 September 2026. Independent mathematical
review and formalization are pending.

Let mu be any bounded probability law on R3, let T be 1-Lipschitz, and
convolve both laws with the Gaussian of covariance s I3, for any s>0. Write

    C_s=(2 pi s)^(-3/2), f=mu*gamma_s, g=T#mu*gamma_s,
    H(u)=integral(g-C_s u)_+ - integral(f-C_s u)_+.

Then, with the absolute constant delta=2^(-32),

    H(u)>=0                       for every u>=exp(-delta).

The inequality is strict when the support map does not preserve all pair
distances and exp(-delta)<=u<max(g)/C_s. The nonstrict assertion also
extends to arbitrary probability laws by truncation.

The cutoff is deliberately conservative, but is independent of support
radius, variance, atom count, atom weights, and distance loss. This signs
an interval of actual hinges uniformly over all contractions. It excludes
a universal upper-density region from the counterexample search, including
laws with arbitrarily rare, arbitrarily distant components.

The full dimension-three Gaussian-majorisation question remains open.
This result does not compare lower thresholds or give a new
Kneser--Poulsen volume case. It is not a priority claim.

The structural input is a monotonicity theorem for the marked-pair coarea
density of **every** six-dimensional Gaussian location mixture at levels
0<=-log Q<=delta. A quadratic change of coordinates, completion of the
square in an unrestricted marked-pair midpoint, and a spherical Helmholtz
comparison prove that sign. A localized Abel inversion then identifies the
actual endpoint hinge. No global regular-level assumption is used.

Read [PROOF.md](PROOF.md) for the complete argument, dependencies, and
scope. To audit the conservative rational constants, using Python 3.11
or later and only its standard library, run from the repository root:

    python3 probability/gaussian_universal_peak_window/audit.py

Expected output:

    PASS: universal cutoff delta=1/4294967296
    PASS: log-derivative partition sums [1, 2, 6, 26, 150]
    PASS: inverse-chart and Jacobian bounds
    PASS: uniform marked-midpoint Helmholtz bound Lambda<=36
    PASS: spherical derivative margin >=42/11
    PASS: Abel calibration and no mode boundary term

The checker audits arithmetic and normalization; it is not an independent
proof, a numerical certificate for the full conjecture, or a replay of the
analytic inequalities. No solver, quadrature, data file, or external corpus
is required.
