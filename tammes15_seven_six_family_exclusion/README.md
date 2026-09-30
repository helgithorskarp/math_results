# Seven/six reflection family excluded from better Tammes-15 packings

Author: **six-tammes-2**, role: **researcher**. Date: 2026-09-30.

The [proof](PROOF.md) excludes 336 degree-compatible cases of a
thirteen-vertex, twenty-four-contact family from fifteen-point sphere
packings with `1/2<cos(d)<3/5`. This covers every strict improvement over
the known fifteen-point incumbent that contains a specified family motif.
The two remaining points and any extra contacts are arbitrary.

The schema joins a triangulated heptagon and a triangulated hexagon by
four contacts from two marked hexagon ears to pairs with old heptagon
common neighbors. Exact root/orientation checks leave four isolated
thirteen-point packings and one continuous Gram branch. Algebraic and
uniform rational-function polytope certificates prevent adding two
separated unit points. The continuous branch's exceptional parameter
values are covered by a proved scaling/continuity lemma.

Global Tammes-15 bounds and optimality remain unresolved. This family is
not a complete contact-graph cover. No input symmetry, proximity,
spherical embedding or complete convex TQ graph is required.

Run with **Python >=3.11**, standard library only:

```sh
python3 -B tammes15_seven_six_family_exclusion/check.py
python3 -B tammes15_seven_six_family_exclusion/check.py --selftest
python3 -B -O tammes15_seven_six_family_exclusion/check.py --selftest
```

The normal output matches [EXPECTED.json](EXPECTED.json). Checks remain
active under Python optimization. The checker compares independent
noncrossing covers entry by entry, re-derives all 336 residuals, checks
exact Sturm root counts and both orientations, and certifies every
isolated and parametric extension-polytope triple. It reads only the
compact [certificate](certificate.json); no coordinates, network input,
solver, scratch output or floating-point tolerance is needed.

The optional generator requires **SymPy1.14.0** and independently derives
every scalar residual in its `Q(t)` field before factoring/root isolation.
It selects finite infeasibility/norm witnesses and reads no certificate:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python3 -B tammes15_seven_six_family_exclusion/generate_certificate.py \
  | cmp - tammes15_seven_six_family_exclusion/certificate.json
```

The trust boundary is the written geometry and continuity argument,
custom exact integer/Fraction software and ordinary Python execution.
This author-audited computational lemma is unformalized and awaits
independent mathematical review. Primary literature, predecessor and
complementary-lane citations appear in the proof. The directory is
self-contained; arithmetic helpers reuse the author's prior source.
