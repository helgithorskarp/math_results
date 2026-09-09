# Exact interface for team-hn-3

HN2 closes **every |z|=1 physical A5(z)** at chromatic number exactly three.
This is an entire-parameter-locus theorem: remove that circle from every exact
system, including systems which do not name the circle among their two events.
The collision branch remains closed by h4119. HN2 retains synthesis, physical
realization, exact chromatic testing, and candidate decisions.

For x,y with z=x+i√3 y, the additional exact exclusion is

    x²+3y²−1 ≠ 0.

When using algebraic ideals, saturation by x²+3y²−1 removes their circle-supported
components. A certified real root filter can instead discard the roots satisfying
that equality. Do not drop an entire two-event system merely because some of its
roots are on the circle. A system having the circle itself as one defining event
can be dropped outright.

All h4117 completeness rules still apply. Pair-orbit representatives are solved
on the whole parameter plane; imposing the chamber requires the full D3-closed
system list. The circle is invariant under D3, so deleting circle-containing
system orbits is compatible with either valid interface. The other existing
filters remain: injectivity, at least four active events, 1/2<|z|≤2, and no monic
E-polynomial of degree≤4 annihilating z.

Complementary off-circle parameter/symmetry/viability reductions remain HN3-owned.
Do not spend a candidate-search pass isolating the 820 unit-circle factor blocks:
all their physical unit-circle graphs are already covered. An internal review of
a concrete algebraic bridge is welcome, but it does not substitute for reviewer-1.

The pinned h4117 global list contains 342 pair-orbit representatives explicitly
containing circle ID342. Removing them leaves **131,788 global representatives**
and reduces the conservative parameter-orbit allowance by 5,200 to **7,780,224**.
`frontier_effect.py` checks the pinned source catalog and pair hashes before
reproducing these counts. Other retained systems can still have circle roots;
those roots are excluded by the theorem, but are not counted by this deletion.

Late durable input: HN3 h4135, source commit
`a0d95fd659807f130695ebf94fb799ee00f94d67`, classifies the exactly-four-active
condition. The present circle theorem excludes all 26 torus-compatible systems
from the exactly-four-active branch. Only 22 explicitly contain the circle;
those can be removed as whole systems. The other four remain in the full
search and now require at least five active curves for a counterexample. The next small complete necessary branch is therefore
**2,528 global systems**, with Bezout allowance **155,648**, for parameters
with exactly four active curves. The 81 no-circle signature patterns remain;
the 10 torus patterns are retired with the unit circle. There are 129,260 other
retained global systems, on which a counterexample must activate at least five
curves. Higher-incidence parameters may also lie on the 2,528 compatible systems.
No conclusion of geometric concurrence or non-four-colourability follows from
this eligibility classification. HN2 does not begin that next branch in this pass.
