# Author validation

All checks below passed on 2026-09-26. This records author validation,
not independent acceptance or proof-assistant formalization.

## Complete replay

The complete verifier produced exactly [EXPECTED.json](EXPECTED.json)
under each of these configurations:

| Python | Native compilation | Result |
|---|---|---|
| 3.11.2 | GCC 12.2.0, `-O2` | pass |
| 3.11.2, `-O` | GCC 12.2.0, `-O2` | pass |
| 3.12.14 | GCC 12.2.0, `-O2` | pass |
| 3.11.2 | GCC 12.2.0, AddressSanitizer and UndefinedBehaviorSanitizer | pass |

The sanitizer flags were
`-O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer -no-pie`.
Every native census was rerun in full under both sanitizers.
The verifier uses explicit checked conditions, so Python optimization
does not disable proof checks. Reproduction commands are in [README.md](README.md).

The audit covers:

* all 1,081,575 planar 17-subsets, with no line-free survivor;
* actual congruence witnesses for all 15,625 symmetric matrices;
* all 715 deficit compositions, yielding 39 centered zero-cubic profiles;
* all 100,442,349 quartic information words across seven quadratic forms;
* exact agreement of the complete rank-one nonsquare and translated
  square-valued quartic catalogues;
* the complete 1,681-candidate partition into 29 subgroup orbits;
* separately evaluated matrix transports for every surviving word;
* every one of the 37 origin-membership cases and 4,180 integer
  certificate column inequalities.

The certificates contain 1,050 nonzero integer multipliers. Their
largest absolute value is 155; the smallest strict contradiction is 50.
No case remains unexcluded.

## Checks against different formulations

The information minor and inverse are checked in the field. A separate
coefficient reconstruction and direct monomial evaluation checks
\(3^8=6,561\) information words for each quadratic form against the native
census. This is a reference slice, not a second complete enumeration.

Composition enumeration independently recovers the local profile table.
Actual matrix transport is evaluated from the original monomials rather
than from composed projective permutations.

Three arbitrary 71-point sets check every point-star identity, every
line-pencil identity, plane energy, and the general centered-moment
indicator identity against direct counts. These sets are not asserted
to be line-free. The 64-point coordinate grid is a separate positive
control for the definitions of line-freeness and the planar cap.

Eight negative controls reject three malformed native inputs, a missing
completion marker, an incorrect census counter, a missing certificate
case, a negative inequality multiplier, and an altered contradiction.

## Optional certificate discovery

With NumPy 1.24.2 and SciPy 1.14.1, `discover.py` regenerated all 37
certificates. The integer coefficient data agreed with the supplied
certificates after JSON parsing. Each discovered certificate was
rationally reconstructed and checked by the exact integer checker
before being saved.

SciPy and its optimizer are not used by the proof replay. Neither an
optimizer verdict nor a floating-point tolerance is a proof premise.

## Compact evidence hashes

* `certificates.json`: 15,178 bytes; SHA-256
  `98c5f9fb805ce89aeef65798473f1055bbf0a6e9443abb3ba13bb218431178f8`.
* `EXPECTED.json`: SHA-256
  `b4c22818d7a5fc82693f74b3ce0ac63e29fe4f728fea6d5f3b2a2f10c1f8eb9e`.
* Regenerated ordered case cover: SHA-256
  `eb11fd2e24aaa7083b10ea319ed48cfc1a493a9e9f2db1f57f858744fae6d9c8`.

The cover digest uses the canonical JSON serialization implemented in
`verify.digest`. Individual complete catalogue digests are in
`EXPECTED.json`. Hashes identify evidence; the proof comes from the
regenerated cover, exact certificate checks, and written reduction.

The remaining trust boundary is ordinary exact Python/C++ computation,
the compiler, and the unformalized mathematical argument. No raw
catalogue, executable, private checkpoint, or solver trace is needed as
an external input. This result excludes a whole moment family but does
not determine the exact maximum.
