# Consumer handoff: all-radius relative localization

Author theorem pending independent review. The full conjecture is open.

Normalize variance to one. Supply an **actual** centered source radius
integer R>=1 and a certified Cov(X)>=kappa I, kappa>0. The map must be a
contraction on the entire actual support. No atom-mass or positive loss
floor is required.

1. If ordered loss D=0, use isometry and return zero hinge.
2. For a middle interval [a0,b0], choose L with 2^-L<=a0 and calculate
   B=2R+ceil sqrt(2(L+1)), r=32B^2-1,
   K=56B^3 2^(3L)(1+4R^2/kappa).
3. Lower bounds H(u_i)>=D eta on a mesh of spacing at most
   2^[-r ceil log2(2K/eta)] certify H>=D eta/2 between samples.
4. A common R,kappa,eta makes this uniform over a parameter family,
   including arbitrarily small D. Samples and endpoint signs must themselves
   be certified uniformly over that family.
5. Whole-curve compression uses (6)--(7) of [PROOF.md](PROOF.md). It retains
   precisely the old marginal feature list and original pair labels.
   The explicit schedule (19) has no loss-dependent degree or atom count.
6. To infer exact all-threshold sign from a middle or sparse-law margin,
   retain signed low/high endpoints for the **original** law. The new
   absolute tail estimate cannot replace a signed endpoint.

The high-noise/covariance-free R8 modulus remains preferable when its
radius hypothesis applies. This packet fills a different region: arbitrary
bounded radius with a positive actual covariance floor. It does not settle
the simultaneous covariance/loss degeneration, produce a new positive
middle margin, or certify the strict screw. Its general budgets are large;
symbolic budget output is not a completed enumeration.

The new dependency is a functional error estimate, not another equivalent
test class. R2's exact machinery can consume either its middle mesh bound or
its reconstruction/cubature error. No teammate code is required to run the
compact arithmetic controls.
