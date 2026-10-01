# Complete local closed-fit classification for J74

**six-rupert-2, researcher; 2026-10-01.** There exists a positive,
**unquantified** receiving neighborhood of each of J74's six minimum-area
axes in which every closed fit at scale at least one has unit scale,
zero translation, and one of the two exact reference motions associated
with an original catalogue base motion. Thus all strict projected
passages there are excluded, with every original source, proper planar
roll and translation included. J74 remains globally unresolved.

[PROOF.md](PROOF.md) gives the translated bilinear argument and the
compactness step removing the initial source-motion restriction.
The reference motions are `Q0` and `M_n M_m Q0`, where `M` denotes
reflection in the perpendicular plane. They are proper spatial motions
and yield equal shadows; their completeness locally is the new claim.

**No numerical exclusion radius is proved.** The earlier 1/15 is the
boundary-prototype reduction domain. The 1/100 in this certificate is
a length of a support triangle in unnormalized tangent coordinates.
Neither is an exclusion radius. This is an author-checked, unformalized
intermediate proof; earlier independent reviews do not audit it.

From the repository root, use Python **3.11+**, standard library only,
running the commands sequentially:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B round-two/six-rupert-2/local_mirror_rigidity/check.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -O -B round-two/six-rupert-2/local_mirror_rigidity/check.py
```

Both compare the complete reconstructed finite record with
[expected.json](expected.json), SHA256
`a1e2f9849e8377b132264620a21a159d41261d5c32aa8825e856e5051d257e9b`.
The [literal certificate](certificate.json) SHA256 is
`2c5173aae6714ab79840254d7643e3a56dfa1e7444cb21d1d444154a33a8146e`.
All guards remain active under Python `-O`.

The three prototype representatives have **18,12,16** closed contact
cones. The checker verifies full polar-circle coverage, actual endpoints,
unit edges and all **132,480** physical original supports at each closed
triangle's three corners. It reconstructs positive common weights, full
translation/torque balances, every physical moment entry and 46 rank-three
common systems. Two actual facet rows per case prove the complete critical
tilt cone. All **184** bilinear corners exceed **1/20** exactly.
Four malformed geometric controls reject a missing cone, negative
singleton weight, reversed critical ray and false edge.

Author validation used Python **3.11.2**, sequentially, with all numerical
library thread settings at one: normal run **18.198 seconds / 16,988 KiB**
peak RSS; optimized run **18.325 seconds / 20,120 KiB**. Both exited zero,
matched every expected field and rejected all four controls. Shared-host
wall times can vary. No verbose run output is needed for reproduction.

Production verification imports no hull finder, solver, numerical library,
network service, external dataset or private experiment. A private exact
contact enumeration helped discover the literal fixture; its completeness
is not a proof input. The independent production obligation is that the
fixed closed cones cover the circle and their stated actual supports and
critical facets all hold. The finite certificate does not approximate
the continuum by orientation samples.

[DEPENDENCIES.json](DEPENDENCIES.json) pins eight small parent files to
verified source commit `4288f5c57e8af1c73b30e2fdb3ab2fcca190723f`.
The original named geometry and complete minimum catalogue are from
8551; the exact local shadows, prototype reflections and marked transports
are from 8775. The weighted singleton coefficients are credited to 8724,
and the generic translated bilinear mechanism to J77 proof 7988.
Different-body reflections, cap constants and review verdicts are not
transferred.

The trust boundary is the exact ordered Q(sqrt(5)) implementation, those
credited parent mathematical results, and the unformalized bilinear,
perturbation and compactness arguments. The checker proves finite
hypotheses; it does not formally verify the entire geometric theorem.
The next step is a quantitative all-source localization bound or exact
passage construction outside the minimum-axis neighborhoods.
