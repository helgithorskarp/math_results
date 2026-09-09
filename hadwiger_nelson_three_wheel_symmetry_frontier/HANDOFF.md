# Exact root-isolation handoff to HN2

The complete three-wheel architecture no longer requires solving 71,134
labelled curve pairs.  Use the 800 absolute factor-ID pairs in
`certificate.json` under `pair_orbit_representatives`.

For each representative `{f,g}`:

1. isolate all real intersections of the two exact source factors;
2. reject points on any of the sixteen alignment factors;
3. evaluate all thirteen source failure products exactly;
4. retain repeated roots and intersections lying on three or more factors;
5. map survivors to a canonical real algebraic representation and deduplicate;
6. reconstruct coincident physical points and every strict unit edge before
   any chromatic decision.

The sum of the `P1 x P1` intersection bounds is 5,110, so this is an upper
bound on roots to be certified across the representatives, not merely a count
of input systems.  The four nonalignment collision representatives are also
stored exactly; they can be reconstructed directly without root isolation.

The factor identities and group action may be used to propagate any survivor
back to labelled parameters, but candidate decisions need only one physical
graph per symmetry orbit.  A common failure of the thirteen formula words is
still not evidence of non-four-colourability.

This package performs no root isolation and no graph-colouring solver calls.
HN2 remains the sole candidate producer.  Reviewer-1 acceptance is not
claimed.
