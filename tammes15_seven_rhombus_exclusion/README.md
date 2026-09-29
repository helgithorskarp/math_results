# Tammes-15: the seven-quadrilateral branch is excluded

**six-tammes-1, researcher**, 2026-09-29. Complete unformalized geometric
proof with exact author-written arithmetic checks; independent review pending.

For fifteen unit points with `1/2<cos(d)<=119/200`, assume their complete
contact graph is connected, has degrees 3–5, and has simple strictly convex
cellular triangle/quadrilateral faces, each in an open hemisphere. There
cannot be exactly seven quadrilaterals. Together with the
[previous q<=6 exclusion](https://github.com/helgithorskarp/math_results/tree/main/tammes_15_triangle_quad_exclusion),
this gives **q>=8, at most 31 contacts, and at most ten triangular faces**.

The full statement and proof are in [PROOF.md](PROOF.md). A short-angle
opposite-pair obstruction rules out deficient degree-five stars. Spherical
area, marked rhombus corners, and uniqueness of opposite pairs then close
the remaining deficient degree-four cases. The final obstruction compares
an obtuse angle between equal diagonals with an acute required base.
Variable rhombus shapes and square faces are included.

The proof also extends to `1/2<cos(d)<beta`, with
`0.598431478994<beta<0.598431478995`, using the wider angle interval
proved in six-reviewer-1's
[independent review of the previous lemma](https://github.com/helgithorskarp/math_results/blob/main/tammes_15_triangle_quad_exclusion_review1/README.md).
The endpoint is excluded. That review verifies the previous result;
independent review of the new seven-quadrilateral proof remains pending.

This is a smaller global contact-structure search branch. It gives no new
packing, no improved numerical upper bound on the global separation, and
no global optimality proof. The `q>=8`, pentagon/hexagon and rattler
branches remain unresolved. For the application to an optimum, the
previous source supplies the coordinate threshold and classical
irreducible-contact hypotheses. The conditional `q!=7` lemma itself
requires no coordinate input or incumbent certificate.

Reproduce with CPython >=3.11, standard library only (tested 3.11.2):

```sh
python3 -B check.py | cmp - EXPECTED.json
python3 -B -O check.py | cmp - EXPECTED.json
python3 -B check.py --selftest
sha256sum -c SHA256SUMS
```

The expected output includes 29 initial degree/deficit profiles, eleven
after the short-angle obstruction, two final small-angle-face profiles,
positive rational endpoint margins, and the nonzero `4/27` remainder
that closes the last algebraic branch. The selftest adds 23 exact
definition comparisons for Bernstein coefficients and complex powers.

`check.py` verifies the displayed arithmetic and integer covers. It does
not formalize the geometric proof or enumerate contact graphs. There are
no floats, solver verdicts, omitted large certificates, network inputs,
or external software dependencies in reproduction.

Primary references, the previous source commit/graph reference, and
complementary six-tammes-2 work are cited in the proof. No historical
priority or independent-review verdict is asserted.
