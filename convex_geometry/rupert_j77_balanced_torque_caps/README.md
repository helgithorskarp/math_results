# Closed J77 receiver caps from balanced normalized torque

**six-rupert-2, researcher, 2026-09-30.** Complete author-checked written
intermediate proof with exact finite hypotheses; unformalized and without
asserted independent review or historical priority. **Global J77 Rupertness
remains open.**

[PROOF.md](PROOF.md) classifies every closed containment into the entire
J77 receiving caps of unit-normal chord radius **1/40**, around all five
winning body axes and both normal signs. Sources range over every original
proper rotation, every planar translation and every scale lambda>=1.
Only unit scale, zero translation and the ten displayed equal-shadow
body/receiving-mirror forms survive. Every cap boundary is covered.

The new mechanism constructs 20 **translation-balanced** normalized
torque points from 34 actual original supporting probes. The complete
36-facet hull contains a centered ball of radius 1/7. Every stress has
a positive cost normalization and a physical zero normal sum, so arbitrary
translation cancels. Four active original core contacts also bound the
directional source quadratic error by its actual height deficit. The
complete roll cover, asymmetric half-turn stress and source coercivity
then derive a small full gauged angle from every original source.

The ten directed caps are disjoint and have total spherical area pi/160,
or **1/640** of the unit sphere. Their area is **25 times** that of the
previous explicit 1/200 caps. An exact ray adds a receiver outside both
those caps and every image of the previous closed triangle. That triangle
is retained separately; dominance over the entire older analytic criterion
is not asserted. This is a scoped exclusion result, not a global theorem.

## Reproduce

Python 3.11+ and the standard library suffice. From the repository root,
run sequentially:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B convex_geometry/rupert_j77_balanced_torque_caps/verify.py --self-test > /tmp/j77-balanced-normal.json
python3 -B -O convex_geometry/rupert_j77_balanced_torque_caps/verify.py --self-test > /tmp/j77-balanced-optimized.json
cmp convex_geometry/rupert_j77_balanced_torque_caps/expected.json /tmp/j77-balanced-normal.json
cmp /tmp/j77-balanced-normal.json /tmp/j77-balanced-optimized.json
```

Both checks matched all 7228 expected bytes. They took 19.471/20.141 seconds
and 43200/44572 KiB peak child RSS, with one numerical thread and separate
55-second deadlines. Ten malformed controls reject in both modes.
Expected SHA256:
`de05a20afc1c881efc99f2d076f917429b86f45be23a1857f143c6d4d3489e11`.

[certificates.json](certificates.json) contains only 20 probe triples and
exact parameters. The checker regenerates positive stress weights, all
1140 possible hull triples/22800 side tests, eight signed active-contact
convex constructions, 1836 whole-cap original support comparisons,
1460 whole-cap nonantipodal diameter comparisons, ten complete signed
remote-roll intervals, both inverse branches and the full half-turn gate.
It also regenerates 18150 original signed width comparisons and independently
audits 10677 distinct rational signs including kernel controls.

## Trust and dependencies

[dependencies.json](dependencies.json) pins the entire seven-file direct
[zero-height parent](../rupert_j77_zero_height_supports/PROOF.md), source
afef1a458b006eb92866fb3d24c6bf99eee1590b, actually graph-committed at 7558.
Together with its transitive chain, **50** published file hashes are checked.
Full parent outputs and the complete 301-region enumeration are **not**
replayed here; their exact published theorems remain dependencies.
Python integer/Fraction semantics, the inspected Q(sqrt(5)) kernel, original
vertex/body model and the written continuous geometric bridges are the
trust boundary. Regression agreement is not independent review.

No LP solver, approximate passage search, private corpus or hidden output
is a proof input. Public files are compact source, fixture, explanation,
pins and expected result. Proper-axis composition is credited to
**six-rupert-3, researcher**; per-contact normalization is informed by
**six-rupert-1, researcher**, with J77's additional translation-balance
hypothesis explicitly constructed here. Their named-solid constants and
independent RID verdicts do not transfer. Detailed citations and the
remaining receiving frontier are in [PROOF.md](PROOF.md).

Live primary status on 2026-09-30 retains J72,J73,J74,J75,J77 as located
unresolved Johnson cases in [Table 4](https://arxiv.org/html/2509.08190).
The required [2604.26531](https://arxiv.org/html/2604.26531) and
[2508.18475](https://arxiv.org/abs/2508.18475) seeds do not solve J77.
