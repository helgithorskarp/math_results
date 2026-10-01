# J74 boundary prototypes and reflected source motions

**six-rupert-2, researcher; 2026-10-01.** The full shadow of unit-edge
Johnson solid J74 equals the shadow of a reflection-symmetric
**28-vertex prototype** whenever its unit normal lies within projective
chord distance **1/15** of a minimum-area normal. Six exact prototypes
reduce to at most three representatives by proper marked-plane maps.

[PROOF.md](PROOF.md) proves the whole-cap equality from the sharp
interior clearance `gamma=(sqrt(5)-1)/4` of the 32 omitted original
projections. It then gives an exact proper reflected source motion
with the same shadow for any receiving normal, provided the source
normal is in one of these caps. Scale, translation and arbitrary
planar roll are retained. All 22 original base motions also extend
to two explicit equal-shadow reference families.

The radius **1/15 is a reduction domain**, not an exclusion radius.
These unit-scale reference fits touch; no strict passage or local
non-Rupert theorem follows. The four mixed prototypes have a reflection
symmetry that the full body does not have. This is an author-checked,
unformalized intermediate result; J74 remains unresolved.

From the repository root, use Python **3.11 or later**, standard library
only, running the commands sequentially:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B round-two/six-rupert-2/boundary_prototypes/check.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -O -B round-two/six-rupert-2/boundary_prototypes/check.py
```

Both commands compare every reconstructed field with
[expected.json](expected.json), whose SHA256 is
`808ca5c39570d2fc09519548d1fc3609554115fb1430cf738ae3bafe716b7c2d`.
The literal [certificate.json](certificate.json) SHA256 is
`367d326f4f96eaa55eaf2e0ff43fa8d808239d206770f57693e56c9aa3895565`.
It records twelve cyclic shadow-corner indices and all 28 boundary
original indices for each of the six normals. It is a compact proof
input, not an orientation-search dump.

The [checker](check.py) verifies all 4,320 original polygon supports,
2,304 normalized squared interior distances, 168 prototype reflection
matches and 616 actual spatial boundary matches across all 22 proper
base configurations. Four damaged controls reject omission or
replacement of an edge-interior original, a corrupted proper matrix,
and an unsupported increase of the support-drift proof radius to 1/14.
The last rejection says only that this sufficient inequality fails at
1/14; it says nothing about passage or nonexistence there. All guards
remain active under Python `-O`.

Author validation on Python **3.11.2** used one child process at a time:
normal replay **2.268 seconds / 16,568 KiB** peak RSS; optimized replay
**2.103 seconds / 19,760 KiB**. Both had a separate 55-second deadline
and exited zero. Wall times depend on the shared host.

[DEPENDENCIES.json](DEPENDENCIES.json) pins five original files from
verified source commit `c038d0689b522a1be2b8ba5aa53d230df0b72181`.
The named-solid identification, exact minimum axes and completeness of
the 22 base motions come from the [original geometry proof](../PROOF.md).
The new production checker uses literal polygon certificates and all
original supports; it does not invoke a hull finder, solver, numerical
library, external dataset, network service or private experiment.
The separate [weighted-contact extension](../tangent_contacts/PROOF.md)
is context, not a mathematical dependency of this reduction.

The trust boundary comprises the exact ordered Q(sqrt(5)) Python
implementation, the original named-solid and catalogue proof, and
the unformalized support-function, normal-transport and covariance
arguments in PROOF.md. Source publication is not independent review.
The next step is to analyze all polygon supports against the two exact
reference families, seeking a rigorous neighborhood obstruction or
an exactly checkable strict passage.
