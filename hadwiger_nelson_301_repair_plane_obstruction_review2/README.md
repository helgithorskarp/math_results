# Independent review of the h3981 plane obstruction

This directory records an independent **ACCEPT** review of Discovery Net
contribution h3981.  The reviewed claim is exact and narrow: the fixed
301-vertex, 1,452-edge abstract graph named by SHA-256
`7be0344d1811866429181436b2f85653fc801272a7a3efddad6125539e50cbbb`
has no map to the Euclidean plane that sends every edge to unit length, even
when arbitrary nonadjacent vertices may coincide.

This is a negative result about one proposed repair.  It constructs no
five-chromatic unit-distance graph and does not improve the 509-vertex
Hadwiger--Nelson record.  The upstream graph's chromatic claims are not a
premise of this obstruction and are not accepted by this review.

The independent checker imports no reviewed implementation.  It enumerates
all graph four-cycles canonically, constructs every claimed quotient graph
literally, checks two fresh modular ranks, and expands the complete rational
quadratic identity.  [REVIEW.md](REVIEW.md) gives the derivation, scope, and
trust boundary.

From the repository root, using Python 3.11 or later:

```sh
python3 -B hadwiger_nelson_301_repair_plane_obstruction_review2/reproduce.py \
  . /scratch/research-team-v2/tmp/reviewer-1/review-h3981
```

The work path must not already exist.  Expected status:
`REPRODUCED_ACCEPT_REVIEW_H3981`.  The script archives the exact reviewed
source commit, checks its manifest, replays both source and reviewer checkers
with and without assertions, and compares exact JSON receipts.

Reviewed source commit:
`9b5f0b989aebbec953d20846d58150e1a0449405`.
