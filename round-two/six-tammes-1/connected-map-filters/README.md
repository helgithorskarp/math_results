# Filters for connected Tammes-15 contact maps

Actual author **six-tammes-1**, role **researcher**, 2026-10-02, pass21.

[PROOF.md](PROOF.md) gives two geometric filters:

- For1/2<c<=5/7, an edge shared by two actual convex hemispheric Q faces
  cannot have both complete endpoint stars composed solely of those two
  Qs and actual triangles. In a regular map, an endpoint must meet a
  third nontriangle. All six endpoint types are handled. Atc=1/2, the sole such type
  is TTQQ at both ends with spherical squares; the classical HCP/J27
  configuration supplies an exact actual-face control.
- In the explicit connected T11/Q3/P3 cohort of9741 on closed[9/20,19/31],
  triangular faces joined across edges form a forest. With e NN edges
  there are e+3 TT edges and8-e triangle components. A prescribed
  eighteen-contact/eight-triangle pattern on12 distinct vertices can
  occur only in11 of52 necessary component-size profiles.

The other41 profiles exclude that motif route, **not packings**. No
profile is asserted realizable and no compatible profile forces the
motif. The complete physical contact-map hypotheses remain in the proof.
There is no new global bound, optimizer coverage or optimality claim.
New independent review is pending.
The already reviewed one-vertex TQQ cases are credited to REVIEW9770;
its verdict does not cover this new packet. PROOF.md also gives the
literal18-edge plus two-cross-contact interface to the peer's published
twelve-point frame9774. The size filter supplies neither cross contact
nor motif occurrence.

## Exact reproduction

Tested with CPython3.12.14 and its standard library only, using
arbitrary-precision integers and `fractions.Fraction`. Run serially from
the repository root:

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B round-two/six-tammes-1/connected-map-filters/check.py
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B round-two/six-tammes-1/connected-map-filters/audit.py
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B round-two/six-tammes-1/connected-map-filters/controls.py
```

The same entrypoints were run with `-O` after `-B`. Regenerate compact
evidence with `check.py --emit /tmp/tammes-connected-filters.json`;
audit another emitted copy by passing that path to `audit.py`.
Default `check.py` compares complete generated/included canonical bytes.

Expected:6 exact QQ cases,220 supporting triples,144 Gram entries,
24 contacts/42 strict noncontacts,3 endpoint QQ controls,1024 cut masks,
52 forest profiles with11 motif-compatible/41 incompatible flags.
The auditor also verifies every supporting plane, boundary cycle,
triangle component and point support. Matching counts alone is not used.

Certificate SHA256:
`8b48a05d9cde5a5485cde55386b5fa20c90e30ba853db06b5b2d77511344e35c`.
[controls.py](controls.py) rejects31 damaged certificates and accepts5
valid semantic representations. [VALIDATION.json](VALIDATION.json) gives
full normal/optimized outputs, whole-byte equality and measured costs.
Every measured child took at most1.191seconds and22324KiB peak RSS.
The unchanged wall guard was55seconds; checks were strictly serial.
[PINS.json](PINS.json) binds cited source files and their exact scope;
[MANIFEST.json](MANIFEST.json) lists complete compact packet hashes.

The producer uses dense rational functions, affine power-to-Bernstein
conversion, cross-product facets and recursive partitions. The auditor
uses sparse functional identities, Bernstein products/degree elevation
plus a separate derivative proof, Gaussian supporting planes, union-find
trees and all1024 cut masks. Both are written by the same author; this
is not independent researcher review or formal verification. No coordinate
table, parent certificate, private ledger, solver or floating-point data
is a runtime input. The spherical and Jordan bridges are ordinary proofs.

The next unresolved step is physical occurrence in surviving connected
maps, or optimizer coverage enabling these filters. The local QQ rule's
upper endpoint is not claimed maximal.
