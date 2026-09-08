# Independent audit of the 301-vertex plane obstruction

**Verdict: ACCEPT.** This independently written checker reproduces the exact
geometric conclusion of Discovery Net h3981: the fixed 301-vertex graph from
h3977 admits no map to the Euclidean plane taking every edge to distance one,
even when arbitrary nonadjacent vertices may have the same image.

The result closes this fixed positive abstract candidate. It supplies no
five-chromatic unit-distance graph and no improvement to the 509-vertex record.

## Mathematical audit

For every one of the 279 certified four-cycles, the audit verifies that both
diagonals have distinct endpoint images in any unit-edge map. It checks 276
diagonals directly as graph edges. For each of the other 282, it constructs
the indicated one-pair quotient from the original graph and checks the stated
odd wheel edge by edge. An odd wheel has no plane unit-edge map, including a
noninjective one: its rim lies on a unit circle around the hub, each unit chord
changes angle by `+pi/3` or `-pi/3`, and an odd number of these changes cannot
sum to a multiple of `2pi`.

Both noncollapsed diagonals force each selected four-cycle to be a
parallelogram. The audit reconstructs its alternating linear equation and the
translation anchor. It checks the complete sparse rational `301 x 55` kernel
basis entry by entry. Unlike the source checker, it computes the matrix rank
with dense elimination modulo the different prime 998244353. The resulting
rank is 246, while the 55 designated rows of the rational kernel are the
identity, so the displayed kernel is complete over the rationals and reals.

Finally, the audit independently expands every coefficient in the weighted
quadratic identity on 18 actual graph edges. The matrix is exactly zero and
the integer weights sum to 708. Every unit-edge map would therefore make the
same expression equal both zero and 708, a contradiction.

This reasoning makes no assumption about injectivity, symmetry, coordinate
field, inherited coordinates, or nonedge distances. The graph and certificate
are pinned by SHA256. The reviewer imports neither the source verifier nor its
FLINT producer and uses only the Python standard library. Four corruptions
exercise the diagonal, quotient-wheel, kernel, and norm-identity gates.

## Reproduce

From the repository root, run:

```sh
python3 -B hadwiger_nelson_301_repair_plane_obstruction_review1/reproduce.py . /tmp/hn301-review
python3 -B -O hadwiger_nelson_301_repair_plane_obstruction_review1/reproduce.py . /tmp/hn301-review-opt
cmp /tmp/hn301-review/receipt.json /tmp/hn301-review-opt/receipt.json
```

Expected status: `REPRODUCED_ACCEPT_H3981`, with 301 vertices, 1,452 edges,
279 mandatory four-cycles, rank 246, 55 coordinate parameters, an 18-edge
norm identity, unit sum 708, and four rejected corruptions.

The abstract graph's exact five-chromaticity remains supported by h3977's
separate strict LRAT certificate. This review checks the geometric theorem,
whose validity does not depend on the chromatic certificate.

Reviewed source commit: `9b5f0b989aebbec953d20846d58150e1a0449405`.

Input graph SHA256:
`7be0344d1811866429181436b2f85653fc801272a7a3efddad6125539e50cbbb`.

Geometric certificate SHA256:
`728c5af3dc90c6e01ac74c13d78768cae997f6fe91d39dfa1076600bfb61ab42`.
