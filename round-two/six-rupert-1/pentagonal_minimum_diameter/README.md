# Pentagonal hexecontahedron: exact minimum shadow diameter

**six-rupert-1, researcher; 2026-10-01, fresh round two.**

The standard pentagonal hexecontahedron has a globally minimum orthogonal
projection diameter of

\[
d_*=2\sqrt{C_{19}^2+C_1^2\frac{\phi^2}{\phi+2}}
\in(4.210546827,4.210546828),\qquad \phi=(1+\sqrt5)/2,
\]

in McCooey's normalization based on a unit-edge snub dodecahedron.
The minimizing directions are exactly its **six unoriented fivefold axes**.
Consequently, none of these receiving directions allows a strict Rupert
passage, for **any** proper moving orientation, planar roll, planar
translation, or moving scale at least one. Both handed versions satisfy
the result. No reflected copy is used in the passage definition.

Every passage also satisfies the global scale upper bound

\[
\lambda<\frac{C_{10}\sqrt{\phi+2}}
 {\sqrt{C_{19}^2+C_1^2\phi^2/(\phi+2)}}
\in(1.054495195,1.054495196).
\]

The Nieuwland number, as a supremum of strict passage scales, is at most
this ratio. The final replay used Python 3.11.2: the three normal commands
took about 63, 19 and 15 seconds; an optimized-Python replay of the first
checker matched its output. Peak child memory over all replays was below
47 MiB. All jobs ran sequentially with numerical thread counts one.

These are exact computer-assisted intermediate lemmas. **The full Rupert
problem remains open.** The diameter argument excludes the six receiving
axes, not positive-radius neighborhoods. It gives a continuous source
localization mechanism for future construction searches. Historical
priority and independent peer review are unasserted.

The proof also applies to an explicit four-parameter family of nearby
icosahedral orbit hulls, defined and bounded in [PROOF.md](PROOF.md).

## Reproduction

Python 3.11+ standard library only; no numerical library, solver, external
dataset, CAS, or network call is required. From the repository root, run
**all three commands sequentially**:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -B round-two/six-rupert-1/pentagonal_minimum_diameter/verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -B round-two/six-rupert-1/pentagonal_minimum_diameter/model.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -B round-two/six-rupert-1/pentagonal_minimum_diameter/controls.py
```

Outputs must match [expected.json](expected.json) and
[expected_model.json](expected_model.json). `controls.py` reports
`arithmetic_controls: PASS` and `malformed_evidence_rejections: 14`.
The code uses explicit exceptions rather than Python assertions, and its
verification remains active with `python3 -O`.

The first checker verifies 60 proper symmetries, all 4,186 original
receiving-pair distances (10 symbolic equalities and 4,176 strict bounds),
92 radius comparisons, ten genuine pair-difference rows, an exact
fivefold average, and **238 nonnegative integer weighted halfspace
certificates**. It checks the full 64-pattern icosahedral cover and both
subsequent sign covers explicitly.

The model checker uses exact arithmetic in
`Q(phi)[x]/(phi^2-phi-1, x^3-2*x-phi)` to verify all 20 positive radical
identities, match all 92 literal source vertices to the orbit model,
verify 60 convex supporting pentagons, and check all 150 polar edges
have one common length. Thus the named-solid alignment does not rely on
floating-point similarity. [model.json](model.json) contains only compact
coordinate indices and facet incidences from the attributed exact source.

[duals.json](duals.json), 27,148 bytes, SHA256:
`5be0b452ec1e2f323c7af57bdf8ea24ad6c53538a6a89f4caf64f1e1de2f600e`.

Trust boundary: the written projection, Cauchy--Schwarz, strict-diameter
and convex-polar arguments are ordinary, unformalized mathematics;
Python's arbitrary-precision integer/Fraction semantics and the compact
checker implementations are trusted. No search completeness, numerical
optimizer, CAS output or omitted large proof corpus is a premise.

## Prior work and status

The located current primary Rupert literature retains the pentagonal
hexecontahedron as unresolved:

- [Fredriksson, *Optimizing for the Rupert property*, arXiv:2210.00601](https://arxiv.org/html/2210.00601), last computational paragraph.
- [Gosain--Grimmer, *Some New Insights from Highly Optimized Polyhedral Passages*, arXiv:2509.08190](https://arxiv.org/html/2509.08190), Table 3 and Section 3.3.
- [Zeng, *A stellated tetrahedron that is probably not Rupert*, arXiv:2604.26531](https://arxiv.org/html/2604.26531), Section 1.2.
- [Steininger--Yurkevich, *A convex polyhedron without Rupert's property*, arXiv:2508.18475](https://arxiv.org/html/2508.18475), projection conventions and the general open-solid context.

The exact coordinate source is
[McCooey's laevo model](https://dmccooey.com/polyhedra/LpentagonalHexecontahedron.txt),
with [geometric conventions](https://dmccooey.com/polyhedra/LpentagonalHexecontahedron.html).
The floating-point coordinates and optimizer supplied by
[Gosain--Grimmer](https://github.com/RajGosain13/RupertResults) motivated
diagnostics only; they are not imported by the checkers.

Previously published team work on
[J77](https://github.com/helgithorskarp/math_results/tree/main/convex_geometry/rupert_j77_projection_diameter)
uses the elementary diameter obstruction as well; that general mechanism
is not claimed as new. The
new scoped information here is the sharp value and complete minimizing
axis classification for this Catalan solid, with a compact certificate
stable on a nearby parameter box. Targeted primary-source and committed
graph searches found no overlapping pentagonal-hexecontahedron diameter
claim on 2026-10-01; this is bounded novelty evidence, not a priority claim.
