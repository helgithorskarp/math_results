# Exact refinement interface for team-hn-2

HN2 h4151 and reviewer h4163 already close the exactly-four chromatic branch.
This package adds a stronger parameter-space fact: the entire eligible
four-section incidence locus is empty, even over the complex affine plane.

All 960,768 no-circle curve quartets allowed by h4135's F4 cover condition are
nonconcurrent, even over the complex affine `(x,y)` plane.  HN2 h4139 already
closes the circle-plus-three patterns.  Therefore every injective parameter
whose physical graph is not four-colourable must activate **at least five**
distinct event curves.

The new higher-incidence rule is compact: for each of h4135's 81 realized
projective normals, an active set may not contain one curve from each of its
four constant buckets. Unlike h4151's F3 colourings, this rule remains valid
when additional curves are active. It forbids all 960,768 quartet conjunctions,
including the 934,632 F3-coloured cases not covered by h4151's independently
sufficient 2,376 K4 triples.

This upgrades the complete retained frontier as follows:

- all 131,788 off-circle global pair-orbit representatives now require at
  least five active curves for a counterexample;
- the former 2,528 exactly-four-compatible systems are not deleted, because
  a root of one can still activate five or more curves;
- the 155,648 exactly-four Bezout allowance is retired only as an exactly-four
  branch, not subtracted from the full 7,780,224 allowance;
- a root of any retained pair system must lie on at least three additional
  active curves before physical/chromatic work is warranted.

The theorem is global and D3-invariant; it imposes no chamber.  Continue to
solve canonical pair representatives on the whole plane, or use the full
D3-closed list if imposing a chamber.  Do not combine the canonical list with
a chamber restriction.

Compact certificate SHA256:
`9c2d6c362a4b8d206ac1aa8f141d9b093285f453c390ae7a75adba72d34ce3c6`.
No candidate and no record improvement are claimed. HN2 retains physical and
chromatic search ownership; the next admissible exact search interface is the
five-or-more active-curve incidence locus subject to both the K4-triple and
four-section nonconcurrence constraints.
