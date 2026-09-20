# Independent review: circuit and cactus zonotope illumination

This directory independently audits
`discrete_geometry/circuit_zonotope_illumination` at target source commit
`215a67dcd31ca84187b539205414b5c0e71f8c37`.

## Verdict

**Accept, high confidence, with one required minor prose correction.**  The
claimed circuit formula, independent-circuit bound and sharpness model, and
cactus formula are mathematically sound.  Section 1's first normalization
paragraph must distinguish the original generators from their reorientations:
after `h_i=sign(alpha_i)g_i`, the zero-sum vector is
`v_i=|alpha_i|h_i=alpha_i g_i(original)`, not
`alpha_i h_i`.  The target program already implements the correct version.

The full premise, completeness, literature, and scope audit is in
[REVIEW.md](REVIEW.md).

## Reproduction

CPython 3.11 or newer is sufficient; there are no third-party dependencies.

```bash
python3 audit.py
python3 audit.py | diff -u EXPECTED.json -
sha256sum -c SHA256SUMS
```

The independent checker does not import or call the submitted checker.  It:

- computes minimum Boolean-chain covers through rank 9 by maximum matching;
- checks all 3,880 small weak-order directions, including ties;
- performs 57,680 exact quotient illumination tests under mixed signs and
  unequal scales, including the normalization error as a negative control;
- checks exact planar Minkowski summands, basis extensions, and product lower
  certificates; and
- classifies all 27,475 connected labelled graphs through six vertices,
  verifying the direct-sum reduction on all 6,074 cacti and rejecting the
  `K_{2,4}` edge-disjoint weakening.

Expected evidence payload SHA-256:

```text
f57ac274ba42f8429fad9361d7a80725d5498278163740022682126e9bf06b3b
```

Finite computation is corroboration.  The verdict rests on the universal human
audit in `REVIEW.md`.
