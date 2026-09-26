# Author validation

The complete ordinary, Python `-O`, and AddressSanitizer/UndefinedBehaviorSanitizer
replays all returned `UNIVERSAL_QUOTIENT_LOCAL_CONSISTENCY_VERIFIED` and
identical mathematical output on 2026-09-26. The interpreter was Python
3.11.2 and the compiler was GCC 12.2.0. There are no third-party Python
dependencies or solver calls in the proof or replay.

Release build flags are `-std=c++20 -Wall -Wextra -Wconversion -Werror -O3`.
The checking build replaces `-O3` by
`-O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer`.
The C++ program uses 25-bit point masks in unsigned 32-bit integers and
64-bit counters. All Python arithmetic used for the conclusions is exact;
conditioned-law comparisons use `fractions.Fraction`.

The audit checks:

* all 1,081,575 planar 17-subsets, with no line-free example;
* six affine types covering every one of the 70 ordinary top profiles;
* seven affine types covering all 101 small-section top profiles;
* a directly checked realization for all 3,069 ordinary and 903
  small-section profiles, including every lower-cardinality boundary;
* every one of the 100 group images of all thirteen templates;
* full fiber-subset laws and the two-fiber product laws involving a
  weight-four fiber;
* explicit 71- and 72-weight quotient controls, with 30 local
  distributions each and identical full-fiber laws across all six
  occurrences of every fiber;
* independent generation of all 775 spatial lines from point pairs,
  with the 750 nonvertical lines covered once and 25 vertical lines
  covered six times by the projection planes;
* malformed profile rejection and rejection of a corrupted template
  containing a full line.

Every individual plane in both controls remains realizable after the
three chosen noncollinear full-fiber holes are fixed to height zero.
Conditioning the particular averaging recipe on those holes gives
inconsistent laws on eight shared fibers in each control. This is an
explicit check of the boundary: no feasibility claim for the *gauged*
marginal relaxation is made.

The template certificate has SHA256

```text
4dae8a9cc94bd216a70b388337bd41a6142d72480fd4b24733bebbd1ee696711
```

Expected output is in `EXPECTED.json`; `SHA256SUMS` covers the source and
compact evidence. The sufficiency and averaging proofs do not rely on
exhaustive discovery searches. The 72-weight control's nonexistence of a
global lift is an imported consequence of the separate upper-bound-71
proof, whose SAT traces are not replayed here. Same-author checking is
not independent peer review or proof-assistant formalization.
