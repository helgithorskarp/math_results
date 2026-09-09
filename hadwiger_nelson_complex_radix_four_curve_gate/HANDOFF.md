# Exact-four branch interface for team-hn-2

The noninjective branch is closed by h4119.  On the remaining injective D3
frontier, an exactly-four-active possible counterexample must lie on one of the
2,554 canonical pair representatives in `exact_four_interface.json`.  Their
total Bezout allowance is 156,176 parameter orbits.

The interface also lists all 91 permissible residue-signature patterns:

- 81 four-hyperplane affine partitions when the circle is absent;
- 10 three-section torus partitions when the circle is present.

These patterns expand to 960,848 eligible curve quartets.  Eligibility is only
a necessary additive-colouring condition; geometric concurrence, injectivity,
and non-four-colourability remain undecided and HN2-owned.

The other 129,576 pair orbits cannot occur inside any exactly-four-active
obstruction.  A non-four-colourable parameter on one of them must activate at
least five curves.  They cannot yet be discarded from the full frontier.

Suggested architecture-owned use: isolate or eliminate the 2,554-system exact-
four branch first.  If it closes, every surviving candidate must satisfy the
stronger five-curve incidence condition.  HN3 has not run physical graph or
chromatic searches.
