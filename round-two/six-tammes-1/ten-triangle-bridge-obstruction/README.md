# Exact obstruction for a ten-triangle G20 component

Actual author **six-tammes-1**, role **researcher**.

[PROOF.md](PROOF.md) proves that a triangle-adjacency tree containing the
two specified four-face clusters and both cross contacts7-12,9-10 has
at least eleven faces, for every c in the closed interval[14/25,593/1000].
In the full fifteen-point T11/Q3/P3 physical cohort of9813 this removes
the1+10 route for FULL G20. It neither forces those contacts/motif nor
gives a new global Tammes bound. The eighteen-contact motif retains its
eleven-profile screen. Independent review of this new theorem is pending.

From this directory, Python3.12 with standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B audit.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B controls.py
```

Repeat with `python3 -B -O` to check optimization does not remove proof
gates. Optional `check.py --emit /tmp/bridge-certificate.json` writes the
full canonical certificate for byte comparison. No generated pilot file,
external coordinate data, solver, CAS or private ledger is needed.

Expected:144 placements,23 root-free polynomials,144 checked Bézout
identities,1,728 norm and3,024 contact identities per construction,
20,736 full Gram polynomial comparisons and288 cross-gap comparisons.
The contact-gap degree is at most9, and the Bézout witness degree at most7.
All32 semantic damages reject;3 valid controls pass.
[VALIDATION.json](VALIDATION.json) gives actual complete normal/O outputs,
timings and certificate equality; [CERTIFICATE.json](CERTIFICATE.json)
is8,029bytes, SHA256
`d6e2ff3a19290c8d7b96f25769bc796bfa3fed030df9c5ae3bb5d988dfc32f2e`.

The dense A-anchored producer and sparse B-anchored checker use different
construction order, polynomial representation, inner-product contraction
and Bernstein algorithms. They are both by one author. Their ordinary
geometric bridge is unformalized; these checks are not independent
researcher review. [DEPENDENCIES.md](DEPENDENCIES.md) separates prerequisites
from context and credits the copied producer kernel.
