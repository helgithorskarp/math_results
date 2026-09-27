# Straight-path pair positivity fails on the indecomposable test class

For every nontrivial contraction with a connected common tight-edge graph,
a fixed root tetrahedron and positive label weights, the natural straight-path
posterior decomposition has a **negative time-integrated pair contribution**
to some Gaussian hinge, at every variance. This includes every nontrivial
step in the accepted indecomposable test class.

The [proof](PROOF.md) first signs the entire spatial/time-integrated cubic
contribution of a moving tight edge. Layer cake then forces a negative
hinge contribution. Thus averaging in time cannot make every pair favorable;
a proof using this decomposition must retain compensation between pairs.
The endpoint hinge itself is not shown negative.
The previously classified seven-site positive indecomposable example
supplies a concrete adverse edge at every variance; its old classification
and positive motion are used with attribution and are not replayed.

A compact ten-site positive control makes the failure quantitative even
after all 45 pair constraints become strict and after optimal Procrustes
alignment. The map is injective on the sites, has paired affine rank six,
and is a composition of known positive folds and a homothety. Its full
Gaussian comparison holds for every weight vector and variance.

**Author proof, independent review pending.** This is a limitation of the
specified decomposition, not a counterexample to Gaussian majorisation
or a new Kneser--Poulsen class. No negative threshold is numerically located.
The unrestricted question remains open. [SOURCES.md](SOURCES.md) gives
the map-lane handoff and distinguishes the existing conditional-kernel
obstruction.

Run from the repository root with Python 3.11 or later, standard library only:

    python3 -B probability/gaussian_straight_path_pair_obstruction/verify.py
    python3 -B -O probability/gaussian_straight_path_pair_obstruction/verify.py

Expected output:

    STRICT_ALIGNED_PAIR_ACTION_OBSTRUCTION_PASS

The [compact exact record](EXPECTED.json) gives the rational coordinates,
45 strict losses, rank, alignment, triple polynomials, normalization checks
and four controls. The positive rational reserve is 5088829/97435855000.
The checker uses no solver, floating-point sign, quadrature or external data.
Its finite checks support the written analytic proof and do not independently
verify it. Use --emit to regenerate the expected JSON on stdout.

From this directory, sha256sum -c SHA256SUMS checks source integrity.
