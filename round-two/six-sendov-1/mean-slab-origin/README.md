# Origin coercivity on a larger real mean interval

Actual author **six-sendov-1**, role **researcher**, 2026-10-01.
Complete ordinary author proof with finite exact checks; independent review
of this extension pending. The analytic arguments are unformalized.

For eight complex q with mean m, sum|q|<=8 and Re m>=a, let

    eta_j = q_j/m - 1 = u_j + i v_j,
    U = sum u_j^2, V = sum v_j^2,
    N_a(q) = |9 integral_0^1 product(1-at q_j) dt|^2 / product|q_j|^2.

If1-10^(-5)<=a<1 and every |u_j|<=1/4, [PROOF.md](PROOF.md) gives

    N_a(q) >= 1 + (1-a) + U/40 + V/16 > 1.

No bound on imaginary deviations is imposed. The modulus mean forces
V<=20(1-a)/a+64(1-a)^2/a^2<1/4000. The proof retains a real radial
reference and bounds the mixed error separately by sqrt(U)*V, U*V and V^2.
It uses the previously published radial Newton-defect theorem. There is
no polar, critical-disk, second-moment, original-root or multiplicity premise
in this abstract interval theorem.

The earlier mean-tube theorem has a broader a interval and stronger radial
coefficient in its smaller complex tube. The new theorem extends the real
relative-deviation range near the boundary; it makes no optimality claim.
Its controls include abstract tuples with mean|q|^2>1, outside the primary
centered argument's second-moment premise.

With the published polar mean and adaptive weighted-phase estimates, this
excludes the joint polar/origin/individual-critical-disk system for

    1 - 5*10^(-6) <= a < 1.

Consequently every degree-nine disk-root polynomial has strict first-power
critical reciprocal sum greater than eight at every marked root in this
annulus. Multiplicities are arbitrary; collisions give infinity. The full
endpoint, an optimal annulus and an unconditional linear reciprocal-sum
margin remain unproved here. [LITERATURE.md](LITERATURE.md) gives exact
dependencies and review scope.

From the repository root, use CPython3.10+ and the standard library:

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B round-two/six-sendov-1/mean-slab-origin/verify.py
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O round-two/six-sendov-1/mean-slab-origin/verify.py

Expected: PASS, six full component identities in fourteen independent real
variables plus six separate Newton component checks; all90 coefficients of
nine primitive polynomials; all42 support counts;26 rational comparisons;
eight Gaussian-rational controls; four damaged symbolic identities and six
damaged fixtures rejected. Canonical record SHA256:

    3dcf544a3d89f5a2ad71450d1fada14610b8f9c308dc86c1de8dbc158c4242cc

Default runs only read [expected.json](expected.json); `--emit` explicitly
regenerates it. No external code/data, floating-point proof input, solver,
omitted computation or large certificate is needed. The checker verifies
finite identities and constants. Chord, support-energy, modulus payment,
complex denominator, flatness and inherited theorem/communication arguments
remain written mathematics. Author checks are not independent review or
proof-assistant formalization.
