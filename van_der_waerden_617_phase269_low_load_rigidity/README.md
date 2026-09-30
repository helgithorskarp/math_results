# Phase269: low-load coordinate rigidity under a class197 cap

**six-vdw-3, researcher.** For the partial reflection QR617 reference
key(269,349,1) on [0,3703], any seven-AP-free binary coloring with at most
197 edits in either original reference-color class must preserve107
specified positions of that class. The other class is unrestricted and
all six poles are free and uncounted. The107 points are exactly those with
load at most65000/1000000=13/200 in the fixed included base packing.
They include73 zero-load and34 positive-load points.

This extends the preceding
[73-point restriction](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_phase269_zero_load_rigidity).
With the separately cited
[class197 lower bound](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_class197_cover),
a hypothetical394-nonpole-edit repair at this reference preserves214
positions, adding68 interior fixed positions to the earlier146-position
corollary. No394-edit repair is asserted to exist. A changed specified
point forces198 edits of its original class; this is a conditional
statement and supplies no unconditional class198 lower bound.

[PROOF.md](PROOF.md) gives a removal argument that retains original APs
through possible removed edits, while charging their precise worst-case
loss. It also handles the lost obligations of three-petal cover-two rows.
One certificate and the complete107-position loss profiles rule out all
low-load edits without separate proof branches. Historical novelty for
the elementary general counting principle is not claimed.

[verify.py](verify.py) derives the masks and1074-point remaining-edit
screens, checks actual APs and triple intersections, and calculates all
losses and capacities in both actual color domains. It uses Euler's
criterion through the unchanged included base checker, no generator,
solver or floating arithmetic. The generator instead enumerates squares
and solves a direct packing LP. This is a same-author independent
implementation, with written unformalized bridges; no external review
or formalization is claimed.

From this directory, standard-library exact replay and28 rejection
controls are:

```sh
python3 reproduce.py
```

The frozen result agrees on Python3.11.2 and3.12.14, also under `python3 -O`.
The controls check omitted/understated losses, incomplete masks, invalid
APs and triples, capacities, surcharges and unsupported hypotheses. A
direct exhaustive three-vertex example independently checks the four
triple-loss cases, with necessary hit minima2,1,1,0.

The frozen [certificate](certificate.json) has891 positive AP weights,
45 triple weights and zero surcharges: W=196038171, worst lost numerator
29027, denominator1000000 and strict gap9144/1000000=1143/125000 over196
remaining edits. Its SHA256 is
8fa71e15ec099961f1074beccb4bb7447c363f5a237784208d4c9dc0c3ac4bce.
The checker replays2052 new AP instances/14364 incidences besides the
base proof. [expected.json](expected.json) contains both107-point lists
and the complete checked summary; supplied masks are not proof inputs.
[SHA256SUMS](SHA256SUMS) identifies the compact source files.

Optional fresh generation uses Python3.12.14, highspy1.11.0 and numpy2.2.6:

```sh
python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python reproduce.py --regenerate --work build
```

The generator enumerates3097 original color-zero crossing APs and uses
45 explicit checked triple plans. It charges every possible removed
point's loss and every capacity overload when rounding numerical weights.
One native solve is capped at15seconds, all numerical threads1. Fresh
weights may differ; the tested regeneration gives a strict gap9143/1000000
and passes the exact checker with the same107-point lists. Frozen+controls
and fresh replay took5.32seconds, with guidance peak56196KiB.
[validation.json](validation.json) records compact successful checks.
Timeout, UNKNOWN, incomplete guidance or a nonpositive gap proves no
exclusion. No private proof input, large search corpus or numerical
solver trust is needed for the frozen replay.

[provenance.json](provenance.json) records the exact source credits,
committed graph dependencies and complementary lanes. The old base
checker and weights are included unchanged. The new conditional proof
rechecks its own base inequalities; the earlier numerical class197
theorem is used only for the214-position/total394 corollary. The newer
fixed-prefix QR617 class30 profile and period618 construction work use
different reference and counting domains. No constants or endpoint
conditions are transferred, and citations are not reviews.

The primary
[Monroe Tables1/2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
retain the inspected length-seven/two-color seed>3703 and prime617,
using W(length,colors). This campaign uses W(colors,length). Checked
live2026-09-30, without an exhaustive current-best or priority claim.
The asymmetric w(3,k) problem is different. A seven-AP-free coloring on
3704 points would prove W(2,7)>=3705 and remains the unrestricted target.
No such coloring, new W bound, exact W value, edit optimum or unrestricted
nonexistence is established here. The new claim concerns one phase and
fixed base, not all617 phases or all760761 incompatible affine keys.
