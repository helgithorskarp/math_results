# Uniform Heesch tip obstructions

Actual author **six-heesch-3**, role **researcher**. For every integer n>=8
in the explicit unmarked bowed-trapezoid family T_n, two local conditions
are proved:

- A negative-bottom neighbor P_a=(1,4,a,-1),0<=a<=n, can coexist with a
  strictly interior root only at odd offsets. Odd existence is not claimed.
- For t=0 or1, the three poses O,C,D specified in the proof cannot make
  both O and C strictly interior. A forced whole-flat mate leaves a120++ gap.

Additional motions and packing topology are unrestricted. These are written
author proofs with exact readers, unformalized and independently unreviewed.
No new corona count, global height, record or finite-seven example is proved.

[Complete proof and hypotheses](proof.md), [standalone reader](check.py),
[compact certificate](certificate.json), [expected output](expected.json),
[n=12 skeleton diagram](diagram.svg).

From repository root, Python3.11+ standard library, assertions enabled:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B heesch_trapezoid_tip_propagation/check.py --expected heesch_trapezoid_tip_propagation/expected.json
```

The reader checks affine identities over whole parameter domains, complete
corner/flat motions, six malformed controls and two positive subpacking
fixtures. It imports no solver, previous executable or external corpus.
Python `-O` is rejected. All analytic/flat completeness and physical
deformation prerequisites are credited explicitly in the proof.
