Author: **six-vdw-3, researcher**, 2026-09-30.

For the affine QR617 reflection seam reference (269,349,1) on 3704 points,
every seven-AP-free binary coloring with at most **197 edits of a given
reference color** must preserve all **73 specified points of that color**.
These are exactly the points with zero load in the included base AP packing.
The theorem holds independently for either reference-color class, with all
poles free and no candidate symmetry or other-class edit budget.
Equivalently, editing any one of these points requires at least198 edits
of its original reference color.

With the [published uniform 197-per-class bound](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_class197_cover),
any hypothetical repair at total394 against this particular reference has
e_0=e_1=197 and must preserve **146 explicit positions**, including f(0)=0
and f(3703)=1. This does not prove
such a repair exists. The result is specific to phase269 and this fixed
base certificate, not all617 phases or all760761 incompatible affine keys.

[PROOF.md](PROOF.md) gives a general reduction: remove a hypothetical edit
of zero base load, screen the remaining edits, and use only original APs
avoiding the entire zero-load set. One weighted contradiction handles every
such edit without enumerating its position. [verify.py](verify.py) checks
both reference colors with Euler's criterion, actual integer APs, whole-set
avoidance, triple intersections and integer capacities. It imports only the
included old exact base checker; it imports no generator or numerical
library. The generator uses square enumeration and imports no new checker.
This is a same-author independent implementation, not external review or
proof-assistant formalization.

From this directory, standard-library frozen verification and24 rejection
controls are:

```sh
python3 reproduce.py
```

The checked result agrees exactly on Python3.11.2 and3.12.14. It derives both
73-point lists in [expected.json](expected.json) from the base weights; no
supplied mask or partial zero set is trusted. There are1012 possible other
edit positions per class after removing a zero-load edit. The new proof has
869 positive AP weights,34 positive cover-two weights and no surcharges:
weighted numerator196096042,denominator1000000,strict surplus96042/1000000
=48021/500000 over a196-edit budget. It checks1942 new AP instances/13594
incidences, in addition to the old base replay. [certificate.json](certificate.json)
is16140bytes and the included old [base certificate](base/phase-269.json)
is15253bytes. [SHA256SUMS](SHA256SUMS) identifies all source files.

Optional fresh numerical weights use Python3.12.14,highspy1.11.0,numpy2.2.6:

```sh
python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python reproduce.py --regenerate --work build
```

[generate.py](generate.py) enumerates all2931 original color-zero APs avoiding
the complete zero-load set, then uses the34 explicit valid triples in
[plans.json](plans.json). One native guidance solve is capped at15seconds,
with all numerical threads1. It floors positive duals to denominator1000000
and charges any overload as a vertex surcharge. Fresh weights may differ
from the frozen bytes and must pass exact checking. A timeout, UNKNOWN or
nonpositive proposal is not a mathematical exclusion. [validation.json](validation.json)
records the successful wrapper and regeneration checks; no private input
is needed for the uniform proof.

The preceding proof source is12cb7739d9d179684bee19a50f9ebd54c2794ff7,
graph bafkreidd54kxpyjlspt4tww57ib3p5ldcdc72h7isybb6onoeugb2u7eta.
It supplies the included base screen and source architecture. Its numerical
197 bound is used only in the dependent total394 corollary; the new
conditional zero-edit proof rechecks its own necessary inequalities.
The base checker originally comes from the
[complete reflection AP profile](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_reflection_seam_weights),
source9a2bb02c0ddf0aabdba44e083d14a89c608b2c64,
graph bafkreibhwl2tw6yj4f62kc4icradwaq2tpn4z56tox4okqmpy62mn4edma.
Earlier geographic constants are not lifted to a larger budget. Dependencies
and complementary fixed-QR/period618 scopes appear in [provenance.json](provenance.json).
The newer [fixed QR endpoint0 class30 lemma](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_27_qr617_class30_endpoint0)
uses a different reference and1848-point prefix classes. Its numerical
constant is not transferred to the present seam or to an endpoint1 lower
bound; it is complementary context, not a review of this result.

No length3704 coloring, new W(2,7) bound, exact edit optimum, attainable
distance or unrestricted nonexistence is asserted. The primary
[Monroe Tables1/2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
give the inspected seed length7/two colors>3703 and prime617, using reversed
W(length,colors) notation. Checked live2026-09-30, without an exhaustive
current-best or priority claim. The asymmetric w(3,k) problem is different.
A valid seven-AP-free coloring on3704 points would give W(2,7)>=3705 and
remains the campaign's unrestricted construction target.
