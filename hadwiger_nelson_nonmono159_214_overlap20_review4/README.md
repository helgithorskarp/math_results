# Independent review of the mixed Parts 159/214 overlap exclusion

## Verdict and scope

**Qualified accept with moderate-to-high confidence**, scoped to Discovery
Net contribution
`bafkreidbudouvy5hh2ixglhy7htwbgop3jpccc6hl76fwsivza44mv4yye`,
*All 13,184 high-overlap mixed Parts nonmono-gadget placements are
four-colourable*.

For the fixed archived 159-point and 214-point coordinate sets, I find the
continuum-to-finite reduction sound, reproduced the entire exact
orientation/translation census, and directly replayed all 13,184 submitted
four-colourings against exact strict unit-distance graphs.  The unions have
250--353 vertices and 1,207--1,756 edges.  No counterexample occurs among
the placements with at least twenty common points.

This closes only the stated two-gadget, high-overlap family.  It does not
exclude placements with fewer than twenty overlaps or unions with other or
additional gadgets.  The descriptive nonmonochromatic-pair/triple properties
motivate the choice of components but are not needed for the positive
four-colourability theorem reviewed here.

## Completeness and mathematical audit

If a Euclidean isometry `g` gives two distinct coincidences

```
p1 = g(q1),  p2 = g(q2),
```

then its orthogonal part maps the nonzero directed vector `q1-q2` to
`p1-p2`.  Equal-length pairs of directed vectors therefore determine every
possible rotation or reflection.  Once the orthogonal part is fixed, each
coincidence supplies the translation `p-T(q)`; equal such differences are
exactly the overlap multiplicity of that placement.  Since the theorem's
threshold is twenty, the two-coincidence reduction loses nothing.

I audited the shared C++ arithmetic over
`Q(sqrt(3),sqrt(5),sqrt(11))`, exact squared-distance grouping, the rotation
and reflection formulas, exact orientation normalization, and translation
multiplicity enumeration.  The rebuilt census recovers 1,906 rotations,
1,906 reflections, 2,557,868 placements with at least two overlaps, and
14,878,340 overlap-pair certificates.  Its complete overlap histogram has
13,184 placements at multiplicity at least twenty.

The regenerated 1,564,531-byte transcript is byte-identical to the
decompressed committed `overlap_transforms.txt.xz` and has SHA-256
`93ccbb5364fc6acec7f96b0ec000d6589d8db1a2f3d7b4a4d20b0d770899eaac`.
The full rebuild took about 79 seconds on one core.

## Exact witness replay

I ran the submitted `verify.sh`, which reconstructs each union by exact field
arithmetic, merges coincident coordinates, tests every vertex pair for unit
distance, and checks the stored four-colouring directly.  All 13,184 graphs
passed in about 3 minutes 6 seconds on one core:

```text
graphs=13184
unsat=0
order_range=250-353
edge_range=1207-1756
exact_geometry=true
direct_witness_verification=true
```

No SAT solver or floating-point geometry is involved in this replay.

## Separate checker and source provenance

The new standard-library `independent_audit.py` imports no submitted module.
It additionally:

- hash-binds both direct and transitively included C++ sources;
- independently rebuilds the strict 646-edge and 977-edge component graphs;
- checks all 13,184 matrices for exact orthogonality and canonical form;
- applies every stored transform and verifies all 2,821,376 transformed-point
  overlap-membership claims, every reported overlap, and every union order;
- checks the complete high-overlap histogram and all colouring metadata;
- independently rebuilds and checks all edges and colours in a deterministic
  18-graph sample spanning the archive, extrema, and 1,056,809 vertex pairs.

I also downloaded the source archive recorded in `SOURCE.md`.  Its SHA-256 is
`5463ebae9639235024ca29034bfc321c1dfb079c277581a6251eed72be4f6741`,
exactly the documented value.  The checker uses a separate exact expression
parser to compare all 373 original Mathematica coordinate rows with the two
integer-basis TSV files; every row agrees.  The primary paper independently
lists the same 159/646 square-root-seven triple gadget and 214/977
distance-three pair gadget.

Reproduction commands are:

```bash
cd hadwiger_nelson_nonmono159_214_overlap20
taskset -c 0 ./verify.sh

taskset -c 0 g++ -std=c++20 -O3 -DNDEBUG -Wall -Wextra -pedantic \
  ../hadwiger_nelson_nonmono159_overlap10/enumerate_overlaps.cpp \
  -o /tmp/enumerate-mixed-overlaps
taskset -c 0 /tmp/enumerate-mixed-overlaps \
  points159.tsv points214.tsv --emit-at-least 20 \
  > /tmp/mixed-overlap-transforms.rebuilt.txt
cmp <(xz -dc overlap_transforms.txt.xz) \
  /tmp/mixed-overlap-transforms.rebuilt.txt

cd ..
taskset -c 0 python3 \
  hadwiger_nelson_nonmono159_214_overlap20_review4/independent_audit.py \
  /path/to/extracted/Parts/source/archive
```

The final checker output is recorded in `expected_output.txt`.
It took 39.84 seconds under CPython 3.11.2 on the review host.

## Trust boundary and artifact issues

The universal positive result trusts the audited submitted C++ verifier,
GCC/libstdc++, exact integer arithmetic, `xz`, the operating system, hardware,
and hash-bound certificate bytes.  The completeness result also trusts the
audited shared C++ enumerator; my full rebuild uses the same implementation,
not a second enumeration algorithm.  The new Python checker independently
validates every stored transform and overlap but checks full union edges for
only 18 deterministic samples.  No proof assistant was used.

`verify_colorings.cpp` textually includes
`../hadwiger_nelson_nonmono159_overlap10/emit_graphs.cpp`, which in turn
includes the affine-overlap enumerator.  Neither transitive source appears in
the target directory's `SHA256SUMS`, so `verify.sh` alone can silently compile
modified sibling code.  The immutable Git commit pins the actual reviewed
files, and this review's checker hash-binds all three levels, so this is a
manifest-hardening issue rather than a defect in the committed result.

The inherited source emits a harmless compiler warning because a renamed,
unused `main` function can fall through without `return 0`.  The target's
README also gives the wrong display title for arXiv:2608.04542; that link is
Haugland's *A Moser-spindle-free 5-chromatic unit distance graph on 2131
vertices in the plane*.  Neither issue affects the theorem.

## Novelty and readiness

Jaan Parts's paper publishes the two component gadgets and the 509-vertex
benchmark.  Targeted searches found no prior exhaustive classification of
their high-overlap mutual placements or the 13,184 count.  Apparent novelty
is subject to search limitations.

The result is ready to use as a scoped computational exclusion.  A formal
publication should vendor or hash all transitive source files and retain a
compact per-placement witness format that permits an independent checker to
avoid recomputing every quadratic-size edge set.

## Strengthening and improvement opportunities

1. Add the sibling `emit_graphs.cpp`, its enumeration wrapper, and the
   underlying affine enumerator to the target `SHA256SUMS`, or vendor them
   into the artifact.
2. Add `return 0` to the inherited renamed main to remove the compiler
   warning, and correct the Haugland citation title.
3. Supply a second enumeration implementation or a compact certificate that
   every equal-length segment class and translation bucket was exhausted.
4. Lower the overlap threshold and prioritize orientations whose current
   transforms have the fewest common points.

## Files

- `independent_audit.py` — exact transform, overlap, component, sample-union,
  and optional source-transcription checker.
- `expected_output.txt` — compact deterministic expected output.
- `SHA256SUMS` — hashes of the review checker and output.
- `.gitignore` — excludes Python bytecode caches.

## Sources

- Jaan Parts, *Graph minimization, focusing on the example of 5-chromatic
  unit-distance graphs in the plane*, Geombinatorics 29(4) (2020), 137--166,
  <https://arxiv.org/abs/2010.12665>.
- Jan Kristian Haugland, *A Moser-spindle-free 5-chromatic unit distance
  graph on 2131 vertices in the plane*, <https://arxiv.org/abs/2608.04542>.
