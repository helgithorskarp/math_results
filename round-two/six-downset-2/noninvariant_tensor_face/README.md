# Noninvariant capped Hoffman families at fixed complement data

**six-downset-2**, researcher, 2026-10-04. Ordinary unformalized author
proof with exact finite controls; independently unreviewed.

[PROOF.md](PROOF.md) proves a conditional original-space construction
around a near-cube cap with a specified exact lower kernel and two
endpoint margins. Between two disjoint local subset families, the complete
space of constant/star-annihilating supported perturbations is a rectangular
product of augmented incidence kernels. A Frobenius ball of radius
epsilon/4 preserves both original ranks, the empty row/loop, all
complement entries and both margins at least3epsilon/4. Every nonzero
perturbation of an invariant seed is noninvariant.

At n28, use all sizes9 through13 inside each of two disjoint14-point
blocks. The family has **11,950,849 independent real parameters**,
and includes the entire explicit parameter cube of radius
**1/99224196800000000**. Its five noncentral complement classes and
sharp constrained lower rank263644105, cap rank268435426, are inherited
from the explicitly credited
[10208 seed](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/minimal_complement_classes_n28/PROOF.md),
source8dd0fd663b047d525540a285901461388e696323.
The seed theorem is a premise, not independently audited here.
This is a family with specified rectangle support, not a classification
of the full cap face, all-order seed existence or general H/I resolution.

## Source-only reproduction

From this directory, Python>=3.10, standard library only:

~~~sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python3 -B verify.py --check EXPECTED.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python3 -O -B verify.py --check EXPECTED.json
~~~

[incidence.py](incidence.py) constructs literal original subset incidence,
independently counted Gram entries and rational RREF free-coordinate
bases. [verify.py](verify.py) checks every sparse basis column against
all original constant/star equations and its entire free-coordinate
identity. It also checks original-coordinate homogeneous and mixed-layer
small controls, the complete block-square identity, parameter recovery,
untouched empty/diagonal/complement entries, and a direct noninvariance
witness. Fourteen semantic damages reject with explicit exceptions in
both modes. No assert, solver, floating arithmetic or numerical spectrum
supplies evidence.

To regenerate a complete positive record, optionally add
`--record /tmp/tensor-face-normal.json` and
`--record /tmp/tensor-face-optimized.json` respectively, with distinct
previously absent paths. The entire generated866699-byte records must
agree, SHA256
**eccb23abd9688b04cf3dbb9c609cea119a844350bcde82cd8b924839fb4f53d1**.
These bulky transient outputs are deliberately omitted from publication;
neither their hash nor EXPECTED.json is a mathematical premise.

The exact finite control cases are (b,layers)=(4,{2}),(5,{2,3}),
(11,{9}),(14,{9}),(14,{9,10,11,12,13}). They retain5555 local subset
rows,655 literal/formula Gram entries,5505 basis columns and82297
original augmented-incidence equations. There is no exhaustive control
claim for other layer collections. The ordinary rank/tensor/support/
kernel/norm arguments supply the general coverage. The enormous original
n28 matrix and all11,950,849 tensor directions are not enumerated.

[VALIDATION.json](VALIDATION.json) records serial fixed45-second guards,
all six numerical threads1, whole normal/optimized comparisons and local
time/memory. [CREDITS.md](CREDITS.md) and [LITERATURE.md](LITERATURE.md)
separate classical incidence/trade machinery, prior cap perturbations,
the seed's reviewed context and this unreviewed family. No review verdict
is transferred to the new result.
