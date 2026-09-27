# A tangential rigid-motion dependency

This packet supplies an explicit five-dimensional contracting motion with a
genuine screw displacement in three dimensions. It is a construction handoff
from R4's extremal-map lane to the geometric lane, not another cap/flap
extension or a solution of unrestricted Gaussian majorisation.

The motion fixes a full-dimensional convex region and carries a full
tetrahedral region by a quarter turn followed by translation along the axis.
Its displacement has nonzero helicity, so even locally on the moved region
it cannot follow the normals of any convex core. An eight-point restriction
has paired affine rank six and fails the team's scalar-defect criterion.
The construction therefore supplies a tangential positive control for work
beyond those two sufficient criteria. It does **not** exclude other known
motions, fold compositions, independent endpoint changes of frame, or
measure-dependent rematchings.

[PROOF.md](PROOF.md) gives the reusable rank-one completion, the simultaneous
motion, the domain inequalities, and the classical transfers to all bounded
laws at every Gaussian variance and to both arbitrary-radius ball-volume
inequalities. Correctness is an author claim awaiting independent review;
historical priority is not established. General contractions between two
rigid clouds, including general screw matchings, remain unresolved here.

The exact checker uses Python's standard library; no solver or quadrature is
needed. From this directory:

```sh
python3 check.py --verify
python3 -O check.py --verify
sha256sum -c SHA256SUMS
```

Tested with CPython 3.11.2. [EXPECTED.json](EXPECTED.json) records the finite
controls. Polynomial coefficient identities support the written all-time
proof; rational sample trajectories alone would not prove monotonicity for
every time, point, prior, variance, or ball radius. There are no external
data, hidden searches, or large certificates.
