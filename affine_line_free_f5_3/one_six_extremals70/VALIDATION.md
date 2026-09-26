# Author validation and its limits

Environment: Python3.12.14, GCC12.2.0, C++20 on Linux. The theorem replay
uses standard libraries only. Optional Boolean controls use
Python-SAT1.9.dev15 and its Minicard backend.

## Complete census

The exploratory implementation completed all21 cases in101.56 seconds
with two workers. The portable public verifier then repeated the complete
census under `python -O`, including fresh planar menus, the full affine
cover, and the explicit affine maps, in108.11 seconds. Both visits cover
all676,318,125 pairs and return the same104 models. All9,276 retained
pairs are completely searched for the remaining two planar sections.

The canonical sorted table of five section masks has SHA-256

```
98c10c5b9c017a1a17718701e7fbfa1e0f2a4f49c7f04f84adab1785f03a8176
```

This is the hash of the verifier's canonical table, not the byte hash of
`models.json`, which also contains the affine certificates.

The final additional six-arc check was run on all104 model certificates
after being added to the verifier. It confirms the small-section line
histogram: nine empty lines, six one-point lines, and fifteen two-point
lines. No pair-generation or completion algorithm changed at that step.

## Sanitizers

The same C++ matching, cover, and completion code was rebuilt with
AddressSanitizer and UndefinedBehaviorSanitizer using

```
-O1 -g -fsanitize=address,undefined -fno-pie -no-pie
```

The full pair intervals for cases0 and18 were replayed:64,411,250 pairs,
4,304 retained pairs, and all104 positive models. The two-worker run took
68.59 seconds; stage counts and ordered model bytes agree with release.
This is a complete replay of those two cases, not a sanitizer replay of
all21 cases. The main `--sanitize` option permits the latter.

Earlier representative graph comparisons also matched byte for byte
under the sanitizer build. No sanitizer finding occurred.

## Independent checks

`validate.py` rebuilds the graph from the interpolation formula in its
endpoints and computes full maximum matchings by breadth-first augmenting
paths. It checks2,000 seeded random cases and all104 positive model triples
against production rows, matching sizes, and explicit matching edges.

The optional `--solver-audit` reconstructs a separate50-variable Boolean
cover problem: one positive two-variable clause per graph edge and native
at-most-nine bounds for each side. On the42,726 maximum-matching-size18
instances in cases0 and18, it agrees with the exact implication search:
3,680 balanced covers and39,046 impossibilities. All returned covers are
checked directly. The624 lower-matching instances pass to exact planar
completion in the theorem and are not part of this Boolean equivalence
comparison. This auxiliary solver agreement is not the proof of the
classification.

`verify.py` independently reconstructs all775 spatial lines from point
pairs and all155 planes from linear equations. Each seed and model is
checked for line-freeness, cardinality, zero sum, maximality, and the
claimed affine image. Deleted-point and completed-line controls are
rejected, and singular affine matrices fail the determinant check.

## Trust and generated state

The mathematical reductions, complete ordinary programs, compiler, and
runtime remain the trust boundary. This is an author-validated exact
computer-assisted theorem, not proof-assistant formalization or independent
acceptance. Independent acceptance of the earlier two-six-plane result
does not transfer automatically to this strengthening.

Raw planar menus, intermediate pair lists, compiler outputs, timing logs,
and operational checkpoints remain outside Git. The repository contains
only source,104 compact positive certificates, the three seeds, the21
orbit representatives, and deterministic count summaries.
