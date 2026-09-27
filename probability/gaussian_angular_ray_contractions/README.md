# Angular factors along rays

An author proof gives full Gaussian majorisation and both arbitrary-radius
Kneser--Poulsen inequalities for **every nonexpansive positively homogeneous
map preserving each ray and its orientation**, in particular in R3.
Independent correctness and historical-priority review are pending.

The angular factor is unrestricted subject to nonexpansiveness on the whole
cone. A fractional-linear motion raises the map into one extra coordinate
while preserving each radius, then lowers that coordinate to reach the
target. This differs from the earlier common radius-profile construction.

Read [PROOF.md](PROOF.md) for the exact cone hypothesis, both motion stages,
the classical transfers, and the global example
`T(x)=|x1*x2*x3|x/|x|^3`. The example is 2/3-Lipschitz and fails the direct
scalar-defect and strong-coordinate tests. [SOURCES.md](SOURCES.md) records
prior work, team dependencies and the limits of the novelty assessment.
The unrestricted three-dimensional question remains open.

Reproduce the compact author checks with standard-library CPython 3.11.2:

```sh
python3 probability/gaussian_angular_ray_contractions/check.py --check
python3 -O probability/gaussian_angular_ray_contractions/check.py --check
```

Without `--check`, the script emits [EXPECTED.json](EXPECTED.json). It checks
exact polynomial identities, the differential Lipschitz bound, rational
pair and rank controls, and deliberately invalid cone and identity inputs.
It uses no numerical Gaussian integration, solver, external dataset, or
proof-assistant axioms. The general motion, transfer and class arguments
remain written mathematics; finite checks are supplementary evidence.
