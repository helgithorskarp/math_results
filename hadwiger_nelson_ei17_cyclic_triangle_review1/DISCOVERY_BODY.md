# Independent review: cyclic EI17 full-input stop is valid but remains a cyclic 2-sum

Verdict: **accept with strict fixed-source, cyclic-frame, and conservative-
contact limitations**.

At target revision `abadf3d5f33005152f588fe0a2e2a52cf0d204eb`, an
independent exact implementation confirms all 124 declared three-copy cyclic
frames.  Each has 48 physical points.  Conservative contact reconstruction
gives 116 upper graphs with 93 inherited edges and eight with three additional
possible edges.  The independent geometry group-and-edge stream agrees
entry-for-entry with target SHA-256
`6bb50a2375d31f15ab407fa24e5cb87ed003999eb0ee486d05c1b1e757abe913`.

The review does not import target or source code.  It recomputes the pinned
EI17 root with exact Fraction intervals, scans all transformed pairs, proves
the source non-three-colourable, and enumerates 170,176 labelled source
colourings after fixing one source edge to colours `(0,1)`.  Each global-colour
orbit occurs twice, independently recovering 85,088 orbits.  All
`8*170176 = 1,361,408` contactful source/frame cases extend through the
conservative upper graphs; the 116 plain frames satisfy a symbolic cyclic
colour-permutation proof.  An independent-set partition count and 43,923
small brute-force solver controls agree.

Structural refinement: every inherited union has no articulation or bridge,
but has exactly three two-vertex cuts, precisely the three anchor pairs.
Hence vertex connectivity is two.  This is a valid cyclic, 2-connected full-
input stop, not a 3-connected forcing source.

Limitations: the eight three-extra-edge objects are conservative upper graphs;
the evidence does not decide which possible contacts are actual.  The family
uses one chosen EI17 edge/frame cycled onto all three sides.  Independent edge
choices, other EI17 roots, phases, polygons, and copy counts are outside scope.
All actual graphs are four-chromatic, so no record candidate results.

Reproducible review evidence:
<https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_ei17_cyclic_triangle_review1>
