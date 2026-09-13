# Independent exact review of four-power no-binomial A5 pencils

ACCEPT with high confidence at target commit
`5799dfd83ddcc127f3a53ecd8c35787e7bb291f6`.

A clean-room checker imports no target code and independently enumerates the
54 homogeneous support-`(3,3,3,3,4)` pencils, 110,592 Eisenstein-unit lifts,
2,801 displacement rows, 2,797 event curves, and all 29,403 labelled pairs.
It eliminates the opposite coordinate from both target routes and uses exact
quotient-field fibre gcds to match all components of all 864 anchor pairs.
All 907 complex components are covered and no full five-section pencil is
concurrent.

An independent rational Sturm computation gives 885 components with 2,988
real embeddings.  For every real embedding, exact quotient arithmetic rebuilds
the collision quotient and complete physical unit-distance graph.  The supplied
ternary colouring descends and is proper; a surviving unit triangle proves the
matching lower bound.  Thus every such physical graph has chromatic number
exactly three.  Concurrency and physical transcript hashes agree with the
target, and two target generation routes produce the same pinned 2,184,292-byte
certificate.

This is restricted-family negative progress, not a sub-509 five-chromatic
construction or a global Hadwiger--Nelson result.  Binomial-containing and
nonhomogeneous pencils remain outside the claim.
