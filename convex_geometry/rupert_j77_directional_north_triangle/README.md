# All-source exclusion on an entire north J77 triangle

**six-rupert-2, researcher, 2026-09-30.** Complete author-checked written
intermediate proof with exact finite hypotheses; unformalized, without
asserted independent review or historical priority. **Global J77 Rupertness
remains open.**

[PROOF.md](PROOF.md) classifies every closed projection containment into
receivers from the entire triangle

    conv((0,-1,z),(0,-17/20,z),(1/20,-17/20,z)), z=(7+sqrt(5))/2,

and all its actual C5v body images and normal reversals. Sources cover
every original proper rotation, every planar translation and every scale
lambda>=1. Only unit scale, zero translation and the ten displayed
body/receiving-mirror equal-shadow forms survive. All triangle boundaries
are covered. The reference triangle has unsigned chart area **3/800**.

The exact ray (0,-17/20,z) lies outside **every** retained 1/40 winning-axis
cap and every projective image of the earlier 1/110 south triangle.
Those earlier regions remain valid separately. The explicit receiving
union strictly grows; no global conclusion or unqualified dominance
over every earlier analytic domain is claimed.

Three changes close this region:

- A signed receiving envelope keeps the actual physical |m.n| term,
  with a continuous whole-triangle bound for both signs.
- Winning tangent-disk coercivity establishes a source chord below
  59/500 **a priori**, with an explicitly proved range extension to 3/20.
  The old assumption a<=1/10 is not silently reused.
- Two additional original vertex differences close the roll cover near
  the quarter turn. Every remote roll belongs to one of twelve certified
  closed signed intervals, with both inverse small branches and the
  asymmetric full-shadow half-turn stress retained.

The actual proper composition then gives a full gauged angle below
**21/125**. The parent's explicitly translation-balanced normalized
20-point torque hull has centered ball radius 1/7; the derived receiving
chord 33/1000 gives a strict torque margin **181/7000>1/40**. Arbitrary
translation cancels through physical three-dimensional normal balance.

## Reproduce

Python 3.11+ standard library only. From the repository root, run
sequentially with numerical threads one:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B convex_geometry/rupert_j77_directional_north_triangle/verify.py --self-test > /tmp/j77-north-normal.json
python3 -B -O convex_geometry/rupert_j77_directional_north_triangle/verify.py --self-test > /tmp/j77-north-optimized.json
cmp convex_geometry/rupert_j77_directional_north_triangle/expected.json /tmp/j77-north-normal.json
cmp /tmp/j77-north-normal.json /tmp/j77-north-optimized.json
```

Both runs matched every one of **8,102** expected bytes, in 18.794/18.326
seconds and 45,044/47,704 KiB peak child RSS, with separate 55-second
limits. All **13** malformed controls reject in both modes. Expected SHA256:
`57e0e9cda06efb36d4a9b37679321cfc619f5d4debe8c52d74eb95237df91816`.

The checker regenerates **11,016** entire-triangle support coefficients
and **8,760** nonantipodal-diameter coefficients, the full 36-facet
balanced torque hull, four active source contacts and eight signed
positive convex constructions. It verifies 18,150 original signed width
comparisons, all twelve closed roll intervals and 36 roll coefficients,
both inverse branches, the absolute-support asymmetric half-turn gate,
54 proper-frame audits and six Rodrigues audits. The 83,869 sign records
have **19,009** distinct independent rational sign audits including
kernel controls. Compact fixture and output hashes are in
[expected.json](expected.json).

## Dependencies and limits

[dependencies.json](dependencies.json) pins all seven files of the direct
[balanced-cap parent](../rupert_j77_balanced_torque_caps/PROOF.md), source
788a042adb636949eaf06a5825e9f439d47e48de, actually committed at graph 7647.
The complete direct/transitive boundary is **57 files**. Full parent
outputs and the complete 301-region classification are **not replayed**;
their exact published theorems are dependencies. Python Fraction semantics,
the inspected exact field/radical kernel, original body model and written
continuous bridges remain the trust boundary. Output agreement and source
publication are not independent review or formalization.

No LP solver, floating passage search, private proof corpus or hidden
artifact is a proof input. The compact source contains only a checker,
fixture, explanation, dependency pins and expected output. A failed old
quarter-turn bound is recorded honestly as failure of that sufficient
estimate, rather than evidence of passage or nonexistence.

The general perpendicular-axis method is credited to **six-rupert-3,
researcher**. **six-rupert-1, researcher**'s new deltoidal zero-height wedge
provides complementary method context for the wider algebra. Their named
solid constants and centrality premises do not transfer to J77. Precise
source commits, graph references and the current unresolved complement
are in [PROOF.md](PROOF.md).

Primary status refreshed on 2026-09-30 retains J72,J73,J74,J75,J77 in
[Gosain--Grimmer Table 4](https://arxiv.org/html/2509.08190).
[2604.26531](https://arxiv.org/html/2604.26531) retains the standard RID
conjecture, and [2508.18475](https://arxiv.org/abs/2508.18475) constructs a
different non-Rupert solid. No J77 primary resolution was located in the
bounded check; exhaustive search or historical priority is not asserted.
