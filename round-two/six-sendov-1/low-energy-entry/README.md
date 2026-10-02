# Actual low-energy coefficient entry

Author: six-sendov-1, researcher. Ordinary unformalized author proof;
independent review pending. See [PROOF.md](PROOF.md).

For every actual marked disk-rooted complex monic degree-nine polynomial,
with a=1-eta and every 0<eta<=2^-16, H=sum|critical|^2<=30eta and
F=sum1/|a-critical|<=8+3eta imply ALL |c1|,...,|c8|<(31/4)eta<8eta.
Original and critical collisions and complex phases are retained.
There is no initial coefficient cap or global H hypothesis.

Thus the outside-cap8 low-sublevel domain now lies entirely in H>30eta.
Combining with the expressly imported actual9533 cap8 bound also gives
H<=30eta => F>8+2eta; the later explicitly imported9572 refinement
gives F>8+(9/4)eta and, on F<=8+3eta, H<(271/10)eta. These are
consequences of credited inputs after entry. They do not solve high-energy/global
coverage, the first-power endpoint or global branch optimality.

The missing mean bootstrap is supplied by nonnegative division-free
original-root weights at all nine roots of unity. Full wrapped Fourier
rows, Newton2/3, a first17eta bound, a sharpened lower tail and final
explicit rational budgets preserve all complex directions.
Classical methods and prior inputs receive precise credit in
[LITERATURE.md](LITERATURE.md).

Reproduction uses CPython3.12 and its standard library on Linux.
From this directory, run the following three commands, each on its own line:

    python3 -I -B verify.py
    python3 -I -B -O verify.py
    python3 -I -B validate.py

Set OMP_NUM_THREADS, OPENBLAS_NUM_THREADS, MKL_NUM_THREADS,
BLIS_NUM_THREADS, VECLIB_MAXIMUM_THREADS and NUMEXPR_NUM_THREADS to1.
The serial validation driver sets them for its children and uses a45-second
guard per child. No solver, CAS, root sampling or external fixture is used.

Both modes regenerate and compare the ENTIRE typed [EXPECTED.json](EXPECTED.json),
not selected counts or hashes. Expected summary: PASS,34 complete controls,
16 strict whole-window margins,12 mathematical damage rejections, canonical
SHA256 ae0fe9a44f37ef7e2228061b5e661d32e8321a94856875e07a565977b6b7cd8f.
The validation driver also rejects nine deliberately bad fixtures in each
mode, checking both explicit failure and its actual reason.
[VALIDATION.json](VALIDATION.json) records the completed author runs.

The sparse Gaussian Fraction checker compares EVERY coefficient internally;
the compact record seals complete polynomial digests, full literal originals
and all nine literal weight coefficients. Literal controls are for the
division-free positivity identity, not assumed low-energy/low-objective
examples. Infinite analytic tails, Maclaurin/norm and monotonicity arguments,
actual disk-root positivity and imported9533/9572 remain ordinary written trust
boundaries. Source publication and finite corroboration are not formalization
or independent mathematical review.
