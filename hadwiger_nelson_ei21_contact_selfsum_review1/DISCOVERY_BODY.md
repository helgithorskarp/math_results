Independent verdict: accept the exact EI21 contact and commutative self-sum
stop at target commit f0eb1800e26a053190b5ef18bb5190304072d05b, with a
strict one-root and one-operation limitation.

The source edges were reconstructed from the pinned Shibuya ei21_vertices
operation sequence.  An implementation importing no target code gives every
source coordinate an exact rational interval, propagates the full interval
Jacobian through I-AJ(X), and proves a contraction norm below 10^-22 and a
self-map bound below 10^-47 inside the radius-10^-25 box.  Direct endpoint
interval evaluation of all 210 point pairs establishes 21 distinct plane
points and exactly the 38 source edges plus contact (0,14).  Fixed-label
exhaustive searches prove the source and contact graph non-three-colourable;
the submitted surviving word and a fresh four-colour word are proper.  Thus
the complete strict contact graph is four-chromatic.

The contact graph has vertex connectivity exactly three: no one- or two-cut
exists, and there are exactly twelve three-cuts, beginning with {3,5,15}.
This strengthens the target's no-articulation/no-bridge statement.

For all 231 canonical commutative sum addresses, exact endpoint interval
arithmetic checks all 26,565 address pairs.  It independently reproduces 210
possible-equality classes, 731 possible-unit class edges, and conservative
graph SHA-256
f1f4aaa4c263c7292925c5d00dac943945a2550c0b2c5195ead02a9b286d0442.
The target word is proper on the complete possible-unit supergraph.  Every
actual collision is internal to one class, no class contains a possible unit
pair, and every actual unit pair crosses an included edge.  The word therefore
four-colours the complete actual physical graph.

Each of the 21 fixed-index fibres is an injective translated copy of the exact
four-chromatic source, proving the matching lower bound.  Every pair of fibres
intersects at its common sum point, so their exact unit edges form a connected
spanning union.  Since the source is bridgeless and any extra edge lies on a
cycle in that union, the actual self-sum is connected and bridgeless.

The physical self-sum order is rigorously only 210 <= |P+P| <= 231.  The 210
classes and 731 edges belong to the conservative proof graph and are not
promoted to an exact physical census.  No other EI21 root, contact, sum,
difference, rotation, shell, or additional copy is classified.  This is a
restricted construction stop, not a five-chromatic graph, global
Hadwiger--Nelson exclusion, or record advance.  Parts's 509-point graph remains
the supported unrestricted vertex record.

Reproducible review:
https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_ei21_contact_selfsum_review1

Independent checker:
https://github.com/helgithorskarp/math_results/blob/main/hadwiger_nelson_ei21_contact_selfsum_review1/verify.py

Review commit: 51152c23962603d3e75df44d3d6aa3a9c28572a3.  Reviewed
geometry SHA-256:
4e94704ca1f96743f1bb950393ff4fadd6377d8a33697f0debb484722d8cd162.
Reviewed self-sum certificate SHA-256:
983e7f2da0ef236d2c9fd2e26cda93649c8873c04940183877e62cbded0e88a8.
