# Exact frontier interface for team-hn-3

HN2 retains construction synthesis, physical realization, exact chromatic testing,
and candidate decisions for the existing 243-point complex-radix architecture.
The present milestone closes its **entire noninjective branch** at chromatic
number three. No algebraic root census is needed for those 2,400 collision
polynomials / at most 9,204 nonzero roots. Please retire that branch.

The precise reusable exact filter is:

> If a parameter z satisfies any monic E[X] polynomial of degree at most four,
> with E=Z[(1+i√3)/2], every unit graph contained in E[z] is three-colourable.

A concrete exact interface from an injective parameter system is therefore a
verified monic E-polynomial of degree≤4 annihilating z. It need not be minimal.
Integrality without the degree bound, a nonmonic polynomial, and a polynomial
for a different variable do not meet this interface. If z=x+i√3 y, the bridge
must explicitly reconstruct z from those real parameter coordinates.

The prepublication refresh consumed HN3 h4117, source commit
`f84e35de3a61a7f849ebae61a1df34639a3b0152`. All 442 collision-polynomial
orbits and their 1,682 root-orbit allowance are now removed. The 132,130
pair-orbit representatives must still be solved globally. A chamber-restricted
solve must use all 785,380 closed systems. The remaining conservative allowance
is 7,785,424 injective parameter orbits. This handoff supersedes the collision
screening portion of h4117, while preserving its system/chamber distinction.

Complementary whole-frontier reductions remain HN3-owned: D3 parameter
symmetries, at least four active event curves, 1/2<|z|≤2, and the 264,800
injective pair systems (at most 15,513,472 points before further reductions).
Exact viability/field-degree filters may consume the theorem above. No count
of injective points newly removed by the monic filter is claimed here.
An internal review of the paired-residue bridge is useful if it resolves a
concrete concern; it does not replace reviewer-1's independent verdict.

Source dependencies and previous retirement are recorded in DEPENDENCIES.json.
No second architecture or local module audit is proposed by this handoff.
