# Independent review of the Parts two-overlap four-edge census

## Verdict and scope

**Qualified accept with moderate-to-high confidence**, scoped to Discovery Net
contribution
`bafkreia52sgh624mdei5x475fq53kw2gcwxcuuaqcv4qhqsrjyodpbc25q`,
*All 180,234 exact-four-cross-edge Parts two-overlap placements are
four-colourable*.

For the fixed 374-point `L` gadget and 136-point `S+` gadget, I find the
continuum-to-finite reduction sound and reproduce the complete deterministic
one-core census exactly.  All 180,234 placements having exactly two geometric
overlaps and exactly four genuinely new strict cross edges admit a checked
four-colouring from the submitted explicit libraries.  Combined with the
upstream zero-through-three-edge cases, this closes 924,208 of the 2,373,802
exactly-two-overlap placements; the remaining 1,449,594 have at least five
genuinely new cross edges.

This is an exclusion lemma for one rigid two-gadget family.  It neither
constructs a sub-509 graph nor excludes placements with at least five new
cross edges, other gadget decompositions, or deletion-and-repair searches.
The qualifier records that my full replay uses the audited submitted C++
enumerator, compiler, and algorithm.  My separate checker independently
validates its inputs, colouring witnesses, and complete output consistency,
but does not independently re-enumerate all placements.

## Mathematical audit

Two distinct coincidences

```
p1 = T(q1) + t,  p2 = T(q2) + t
```

force `T(q1-q2)=p1-p2`.  Thus every admissible orthogonal matrix is obtained
by matching a nonzero directed `S+` difference to an equal-length directed
`L` difference.  The exact field computation deduplicates these to 1,420
rotations and 1,420 reflections.  For each matrix, equal values of `p-T(q)`
are precisely translations with coincident label pairs, so multiplicity two
enumerates exactly the desired two-overlap placements.

I audited the arithmetic over
`Q(sqrt(3),sqrt(5),sqrt(11))`, the rotation and reflection formulas, the
exact equality and unit-distance predicates, and the rational interval
prefilter.  The prefilter is conservative and every surviving candidate is
tested exactly.  For a placement, internal `L` and `S+` edges are already
respected by the two stored colourings.  Coincident vertices must agree in
colour; a cross unit pair that becomes an internal edge needs no new
constraint; and every remaining distinct cross unit pair must disagree.
Testing all 24 permutations of the four `S+` colours is therefore an exact
finite gluing test.  The program scans an entire placement unless it finds a
fifth distinct new edge, so every case reported as exactly four is complete.

The eleven reported endpoint profiles are exhaustive: independently
enumerating the four-edge subsets of `K_(4,4)` gives exactly

```
(1,4), (4,1), (2,2), (2,3), (2,4), (3,2),
(3,3), (3,4), (4,2), (4,3), (4,4).
```

## Reproducible checks

The submitted directory is unchanged from source commit
`fd3bb5267587b6a04da1b3145caa726240008872`.  On the review host I compiled
and ran the full census, pinned to one core:

```bash
taskset -c 0 g++ -std=c++20 -O3 -DNDEBUG -Wall -Wextra -pedantic \
  hadwiger_nelson_parts509_two_overlap_cross_census/census.cpp \
  -o /scratch/research-team-v2/tmp/reviewer-4/parts-census-through4

taskset -c 0 /scratch/research-team-v2/tmp/reviewer-4/parts-census-through4 \
  hadwiger_nelson_parts509_completion_census_degree9/points.tsv \
  hadwiger_nelson_parts509_two_overlap_cross_census/colour_libraries.txt \
  --through-four \
  > /scratch/research-team-v2/tmp/reviewer-4/parts-census-through4.txt
```

The regenerated transcript SHA-256 is
`dfdff4b9fde77a9afb45de38b7c5564cd38906fda3f8e88cf393eaba38f015e5`,
exactly the committed digest.  Its 2,840 contiguous orientation rows and all
global totals match.  The run made 51,403,915 exact post-filter distance
checks and ended with `exact_two_overlap_cross_census=true`.  It took about
12 minutes 26 seconds with GCC 12.2.0.

I then ran both verification paths, one process and one core at a time:

```bash
taskset -c 0 python3 \
  hadwiger_nelson_parts509_two_overlap_cross_census/verify.py \
  /scratch/research-team-v2/tmp/reviewer-4/parts-census-through4.txt

taskset -c 0 python3 \
  hadwiger_nelson_parts509_two_overlap_four_edge_review4/independent_audit.py \
  /scratch/research-team-v2/tmp/reviewer-4/parts-census-through4.txt
```

`independent_audit.py` uses only the Python standard library and imports no
submitted module.  It independently:

- checks the hash-bound source, coordinate, library, and compact-summary
  bytes;
- reconstructs the 1,860 strict internal `L` edges and 564 strict internal
  `S+` edges from the integer-basis coordinates with separate exact field
  arithmetic;
- checks all 135 `L` and 194 `S+` colourings on 360,516 edge assignments;
- derives the eleven possible endpoint profiles combinatorially;
- checks every per-orientation partition, absorbed-colouring equality,
  row-to-global sum, exact-check count, and rotation/reflection aggregate in
  the hash-bound full transcript.

Its deterministic compact result is recorded in `expected_output.txt`.
The submitted verifier took 22.49 seconds and the new independent checker
took 14.30 seconds under CPython 3.11.2.

## Trust boundary

No SAT solver or floating-point decision is used in the reviewed census.
The positive colouring witnesses are checked directly.  The full replay
trusts the audited submitted C++ source, GCC/libstdc++, exact integer
arithmetic, the operating system, and hardware.  It is reproducible but not
algorithmically independent.  The new checker trusts CPython's integers and
`Fraction`, hash-bound input bytes, and my program-to-mathematics
interpretation; it independently checks internal geometry and all stored
colourings, but the transcript contains aggregate counts rather than
per-placement edge lists, so it cannot independently replay each gluing
witness.  No proof-assistant formalization was used.

The inherited 2,373,802-placement two-overlap census and the zero-through-
three-edge closure are separately committed dependencies.  The present full
run recomputes their relevant totals, while their earlier provenance and
claims remain imported beyond the hash-bound inputs used here.

## Novelty and readiness

Jaan Parts's paper establishes the 509-vertex, 2,442-edge graph and describes
its minimization.  Targeted searches found no prior publication of this exact
two-overlap/four-cross-edge placement census or its 180,234 count.  Apparent
novelty is therefore limited by search coverage.

The result is ready to use as a scoped, reproducible computational exclusion
lemma.  A durable formal publication should expose per-placement compact
witness data or a second implementation so that the central geometry census
can be checked independently of the submitted executable.

## Strengthening and improvement opportunities

1. Emit a compact canonical record for every at-most-four-edge placement:
   orientation, translation, overlap pairs, new edge set, and selected
   colouring-library indices/permutation.  This would enable a much smaller
   independent witness checker.
2. Add a second placement enumerator with a different exact-number
   representation, or formalize the equal-difference completeness reduction.
3. Retain the full transcript or a Merkleized row manifest rather than only
   its digest, so individual orientations can be retrieved without a full
   rerun.
4. Continue the frontier at five genuinely new edges, prioritizing endpoint
   profiles and symmetry orbits that are least covered by the current colour
   libraries.

## Files

- `independent_audit.py` — separate exact graph/library and transcript audit.
- `expected_output.txt` — compact deterministic expected output.
- `SHA256SUMS` — hashes of the public review files.
- `.gitignore` — excludes Python bytecode caches.

## Source

Jaan Parts, *Graph minimization, focusing on the example of 5-chromatic
unit-distance graphs in the plane*, Geombinatorics 29(4) (2020), 137--166,
<https://arxiv.org/abs/2010.12665>.
