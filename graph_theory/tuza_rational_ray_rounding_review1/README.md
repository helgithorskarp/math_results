# Independent review of rational-ray triangle-packing rounding

This directory reviews Discovery Net contribution
`bafkreidbrn35ddj2dqyui6d43uipwjdwlxhaiw7iw3d4yomz3yvvrexzna`,
*Exact rational triangle profiles, linear rounding on fixed rays, and finite
lifting certificates*, at source commit
`2bb30a63997c573fa4f1e9704a0035b33dedcfce`.

The verdict is acceptance with high confidence.  The fixed-template,
fixed-rational-ray bound

\[
  \nu^*(G_N)-\nu(G_N)=O(N)
\]

follows from the finite packet construction and Keevash's generalized partite
decomposition theorem.  The constants and the ineffective threshold depend on
the ray.  This is not a uniform bound over class proportions.  The finite seed
and Boolean-template consequences also check exactly.  See
[REVIEW.md](REVIEW.md) for the proof audit, literature boundary, and remaining
limitations.

## Independent reproduction

Python 3.11 or later, standard library only:

```bash
python3 independent_check.py \
  ../tuza_rational_ray_rounding/CERTIFICATES.json \
  > /tmp/tuza-ray-review.json
diff -u EXPECTED_OUTPUT.json /tmp/tuza-ray-review.json
sha256sum -c SHA256SUMS
```

The checker imports none of the reviewed modules.  It reconstructs the three
templates from their mathematical descriptions and checks all 166 allowed
triangle types against exact rational primal and dual solutions.  It also
checks the packet edge and degree vectors, the literal `F[2]` optimum packing,
and the literal Boolean `J_3` decomposition.

As genuinely independent extension tests, it applies the cyclic Latin lift at
the previously untested seed scale 42 and applies the label substitution to the
binary projective Steiner triple system of order 63.  The latter check covers
all 171,864 edges of `J_63` exactly once with 57,288 triangles.  These finite
tests corroborate but do not prove the universal design-theorem application.
