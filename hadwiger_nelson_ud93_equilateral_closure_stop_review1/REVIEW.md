# Review verdict

## Verdict

**Accept, with strict complete-round and single-realization scope.**

The independent checker reproduces the exact closure census through round 9,
the isolated source root, the complete physical unit graphs at rounds 8 and
9, the source's chromatic number four, the round-8 proper four-colour word,
and all four target point/edge stream hashes. Round 8 is 432/1,134 and exactly
four-chromatic; round 9 is 533/1,415. This validates the claimed stop for the
complete equilateral-closure sequence under the 508-point cap.

The target is a sound negative result for one architecture, not a
five-chromatic construction or record candidate.

## Independent findings

- The source has zero canonical three-colourings and 72 canonical
  four-colourings.
- Its five unoriented direction classes generate 30 oriented directions
  under sixth-root rotation.
- The exact all-pairs audits cover 93,096 round-8 pairs and 141,778 round-9
  pairs.
- The weakest certified squared separation remains above 10^-4; the weakest
  nonedge squared-distance gap from one remains above 10^-3.
- Normal and optimized verifier output is byte-identical.
- The pinned producer regenerates the target certificate byte-for-byte.
- The pinned Shibuya parametrization numerically matches the same ordered
  nine-point source and the same complete 15-edge graph.

## Limitations

The contraction certificate proves uniqueness only within its stated
rational box; global uniqueness or rigidity is neither proved nor required.
The review does not exclude:

- choosing only some equilateral completions;
- retaining part of round 9 and searching under the cap;
- deleting vertices or edges after closure;
- using another real root or another UD9-3 realization; or
- embedding the source in a different host or construction family.

Those are outside the target claim. In particular, this restricted-family
closure result is not a global lower bound and must not be represented as
progress beyond the supported 509-vertex unrestricted record.
