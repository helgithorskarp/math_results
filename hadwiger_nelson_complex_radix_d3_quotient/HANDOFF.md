# Exact quotient interface for team-hn-2

This package is the complementary exact reduction requested by the complex-
radix architecture handoff.  It does not perform physical graph realization or
chromatic testing.

The smallest complete system interface is 132,130 canonical D3 pair-orbit
representatives solved on the whole `(x,y)` plane.  Its total Bezout allowance
is 7,785,424 parameter-isometry classes.  Collision screening needs only 442
canonical polynomials, of total degree 1,682.  Run `export_quotient.py` to get
the exact lists in source-stable curve IDs.

If a downstream exact solver instead imposes the chamber

    x>=0, 0<=y<=x, 1/4 < x^2+3y^2 <= 4,

it must use all 785,380 systems in the D3 closure, not only the canonical pair
representatives.  Pair canonicalization and point canonicalization cannot in
general be imposed simultaneously.  `PROOF.md` proves both interfaces.

The next architecture-owned step is therefore free to choose between a smaller
global algebraic system list and a larger semialgebraically restricted list.
Either remains only a necessary frontier; HN2 retains all realization and
chromatic candidate decisions.
