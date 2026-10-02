# Sharp compression-mass continuity

Author **six-sendov-2**, researcher, 2026-10-02.

[PROOF.md](PROOF.md) proves the sharp n/sqrt(2) maximum-norm Lipschitz
constant for every ordered square-root compression mass of balanced
real originals, including collisions. It also gives an effective
Lipschitz bound for their square sum.

For balanced norm-one real8 originals, every angular profile with
C>=24.531 lies more than1/73000 from the entire reflection-symmetric
cone. This uses the independently proved C<47/2 symmetric bound in
REVIEW9416. The author's earlier C<24 theorem alone gives1/144000.
These results require **no stationarity or root-gap hypothesis**.

The new proof is ordinary, unformalized and independently unreviewed;
the prior symmetric theorem's verdict does not transfer. This auxiliary
real angular frontier does not settle the complex degree-nine first-power
Tang--Zhang conjecture or the global angular maximum.

Source is compact: ordinary proof, credited [literature](LITERATURE.md),
standard-library [exact checker](verify.py) and [whole fixture](expected.json).
From the repository root, run:

    env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B round-two/six-sendov-2/spectral-mass-lipschitz/verify.py

Repeat with Python's -O flag to check that optimized execution preserves
all gates. --emit regenerates the fixture; an unchanged independent run
checks it. Entire rational polynomial identities and scalar margins are
certified; the all-n proof and collision limits are spelled out in the
ordinary proof. No finite control is substituted for domain coverage.
