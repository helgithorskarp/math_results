# J77: exact minimum shadow diameter and a passage-scale bound

Author: **six-rupert-2 — researcher**. Date: 2026-09-29.

For the unit-edge paragyrate diminished rhombicosidodecahedron, Johnson
solid J77, this package proves the computer-assisted optimisation result

\[
\min_d\operatorname{diam}(\pi_d J77)
=2\sqrt{\frac{787+293\sqrt5}{298}}.
\]

It follows that every strict passage scale satisfies

\[
\lambda<\sqrt{\frac{2797-75\sqrt5}{2552}}
<1.015031019665.
\]

The Nieuwland number is at most the radical. A separate analytic lemma
excludes an axial receiver when the inner projection axis is within the
explicit cone in Section 6 of [PROOF.md](PROOF.md), of half-angle about
10.3 degrees. **J77's Rupert property remains unresolved.** These are
intermediate geometric results, not a proof of non-Rupertness.

The exact upper bound is certified by a finite reduction with 9,825
direction candidates. Its attaining direction is parallel to
`(0, -1, (7+sqrt(5))/2)`; all 1,485 projected vertex-pair distances are then
checked. A centrally symmetric 50-vertex core makes the diameter bound
independent of translations. No central-symmetry assumption is made for
J77 itself.

## Reproduction

From the repository root:

```sh
python3 convex_geometry/rupert_j77_projection_diameter/verify.py
```

Python 3.11 or later is sufficient; the validated run used Python 3.11.2.
Only the standard library is needed. Run without `-O` or `-OO`; the
checker explicitly rejects disabled assertions. Verification takes about
ten seconds on the research host, on one thread, and needs no network
access or external input. No solver or floating-point library is used.

The printed JSON must exactly match [expected.json](expected.json). Main
expected fields are:

- 55 vertices, 105 edges; 15 triangular, 25 square, 11 pentagonal and one
  decagonal supporting regular faces.
- 25 antipodal core pairs; 9,825 checked direction candidates and no
  zero candidates.
- 1,485 projected vertex-pair checks at the attaining direction.
- First-blocker SHA256:
  `86666a18873e8162cbd45972710a11c336e69e88e87ce3eb8804ef2b25909a8f`.
- Certified enclosure of the scale radical:
  `(1.015031019664, 1.015031019665)`.

`model.py` includes an exact coordinate fixture and generates J77 again by
deleting opposite cupolas of a rhombicosidodecahedron and restoring one
after a 36-degree gyration. `q5.py` implements ordered exact arithmetic in
Q(sqrt(5)). `verify.py` checks the construction, geometry, finite reduction
obligations, attaining witness, axial lemma ingredients, and compact
expected results. [PROOF.md](PROOF.md) supplies the continuous coverage
argument and interpretation.

The finite reduction is essential: the result is not inferred from a
sampled search. The SHA256 identifies a deterministic replay; it does not
replace mathematical verification. The proof's trust boundary is ordinary
Python exact arithmetic plus the unformalised arguments in PROOF.md.

## Literature and status checked on 2026-09-29

The searched primary literature lists J72 (gyrate rhombicosidodecahedron),
J73 (parabigyrate), J74 (metabigyrate), J75 (trigyrate), and J77 (paragyrate
diminished) as unresolved. This researcher selected J77. The accompanying
unresolved classical lists have three Archimedean solids (snub cube,
rhombicosidodecahedron, snub dodecahedron) and two Catalan solids (deltoidal
hexecontahedron, pentagonal hexecontahedron).

- Albin Fredriksson, [Optimizing for the Rupert property](https://arxiv.org/abs/2210.00601),
  v2, 2023; Monthly 2024. Establishes five further Johnson passages,
  including J76, and identifies the five remaining Johnson solids. Its
  negative numerical searches do not prove nonexistence.
- Raj Gosain and Benjamin Grimmer,
  [Some New Insights from Highly Optimized Polyhedral Passages](https://arxiv.org/abs/2509.08190),
  2025 preprint; Monthly 2026. Reports high-accuracy searches without
  resolving these remaining Johnson or Catalan solids. Table 4 leaves
  J72–J75 and J77 blank.
- Tony Zeng, [A stellated tetrahedron that is probably not Rupert](https://arxiv.org/abs/2604.26531),
  2026. Reports 87 of 92 Johnson solids known Rupert and states the
  rhombicosidodecahedron non-Rupert claim as an open conjecture.
- Jakob Steininger and Sergey Yurkevich,
  [A convex polyhedron without Rupert's property](https://arxiv.org/abs/2508.18475),
  2025. The Noperthedron disproves the universal polyhedron conjecture;
  this does not settle J77. Its translation-free formulation for
  centrally symmetric solids is not applied to all of J77.
- Evan J. Scott,
  [Two Sufficient Conditions for a Polyhedron to be (Locally) Rupert](https://arxiv.org/abs/2208.12912),
  2022. Context for local construction mechanisms.
- David McCooey,
  [exact J77 coordinates](https://dmccooey.com/polyhedra/ParagyrateDiminishedRhombicosidodecahedron.txt).
  The fixture preserves his vertex ordering; the independent cupola
  construction checks the named-solid identification.

Targeted searches did not locate the exact shadow-diameter formula above.
No priority claim is made. No heuristic search output is part of this
package.
