# Author audit and reproducibility boundary

The written construction is universal. The finite verifier does not infer
it from sample quotients: it checks every profile in both filling domains,
then checks the quotient incidence identities and one explicit control.
Independent peer review and proof-assistant formalization are not claimed.

Validated with Python 3.11.2 and GCC 12.2.0, C++20. The ordinary and Python
`-O` runs use `-O3`; the checking build uses `-O1 -g
-fsanitize=address,undefined -fno-omit-frame-pointer -no-pie`. Both builds
enable `-Wall -Wextra -Wconversion`. The complete optimized-Python replay
took 4.88 seconds and the complete sanitizer replay 5.44 seconds on the
author's host; peak child memory including compilation was 88,336 and
100,672 KiB respectively. These timings are descriptive, not promises.

All three runs agree with [EXPECTED.json](EXPECTED.json). The checks cover:

- All 3,069 profiles of total at most sixteen with entries at most four.
  Their 24 height-permutation constructions are decoded into actual point
  sets and checked on all geometric lines and full-subset marginals.
- All 101 top small profiles and their seven affine types. All fourteen
  supplied templates and the required affine images are checked.
- All 903 profiles of total at most ten with entries at most three.
  The verifier expands every random-deletion outcome and checks all
  rational masses, point sets and complete subset marginals.
- An independent point-pair construction of all 30 planar and 775 spatial
  lines. Projection coverage is 750 single incidences and 25 sixfold ones.
- The 71-weight control's 30 local laws, six occurrences of each fiber,
  all nine weight-four holes fixed to zero, and exact transverse-plane
  expectations `(0,71/4,71/4,71/4,71/4)`.
- All 1,081,575 planar 17-subsets, with no line-free survivor, and the
  64-point Cartesian sharpness control on all 775 spatial lines.
- Rejection of five invalid profile/quotient inputs, a corrupted template,
  and a corrupted probability normalization. All checks use explicit
  exceptions and remain active under Python optimization.

The generator uses cyclic hole coverage and explicit group actions. The
geometry audit instead constructs lines from every distinct pair of
points and checks their masks directly. This is a definition-level check
authored by the same researcher, not independent peer validation.

All probability arithmetic uses exact Python fractions. Planar masks use
25 bits; the C++ census loop stays below 2^25, shifts below 25, and counts
in unsigned 64-bit integers. No floating-point number, optimizer verdict,
hidden catalogue or external certificate is used in the published proof.
Private solver experiments were used only to discover the final construction.

No raw catalogues, logs, binaries or generated distributions are published.
The explicit small templates and the short code regenerate every required
law. `SHA256SUMS` records the compact source files; hashes identify bytes
and do not substitute for the mathematical checks.
