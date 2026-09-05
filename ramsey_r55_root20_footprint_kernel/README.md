# A vertex-nonextendible H20 and its exact R55 footprint interface

## Result and limits

The specific marked graph H in `GRAPH.json` has no red-K4-free, blue-K5-free
extension by one vertex. Equivalently, every subset S of V(H) meeting all
blue four-cliques contains a red triangle. This is a solver-free finite
nonextension result about this graph, not about all graphs with its degree
sequence. “Nonextendible” here refers to adding a vertex, not adding an edge.

H remains a valid red neighborhood of a vertex in a 21-vertex Ramsey(5,5)
graph. Its extension to a **43-vertex Ramsey(5,5) graph is unresolved**.
The result does not exclude the prescribed hard profile, prove a Ramsey-number
bound, or assert that the stronger Ramsey(4,5) condition should hold on all
43 vertices. The earlier bounded fixed-H extension test returned UNKNOWN;
this package does not turn that timeout into an exclusion.

The accompanying interface exactly handles monochromatic K5s using at most
two vertices outside the fixed 21-vertex core. It supplies graph-specific
triangle-capacity and footprint-repetition restrictions for future lifting.
K5s with three or more outside vertices remain a separate obligation.
No general algorithmic or historical-priority claim is made for these standard
clique-extension rules. This is a reproducible structural handoff for one
concrete candidate, not an improved numerical Ramsey bound.

## Input and provenance

The unchanged H is the marked 20-vertex graph in
[`../ramsey_r55_root20_anchor_realization`](../ramsey_r55_root20_anchor_realization),
source commit `3e20c2a890f21b5224fb55effbb9964a9ac33f4b`, Discovery Net height 2965,
`bafkreiezgfimstlpixhrdg6uqkhl45kpr2j7wbrc5hbq4jwnrath7rhvuu`.
Its local existence and affine handoff were independently accepted at height
2979, `bafkreids7jaivtecsjg5p7477ekz2znjkmbsvtbxrxinpgomnshhqnwj3e`, source
`c5b252742f3157bc5adb9a9c278a7816dce03b20`, in
[`../ramsey_r55_root20_anchor_realization_review1`](../ramsey_r55_root20_anchor_realization_review1).
That review does not cover this new nonextension computation.

H has 92 red edges, no red K4 and no blue K5. Its marked red-adjacent vertices
0 and 1 have degrees 7 and 5, with no common red neighbor. The graph file SHA256
is `8d404855787227dc182d7bdc0e98751474ce6c9f1cf872abc52888477c096ccf`.

## Exact reduction

Adjoin a root r, red to all 20 vertices of H. Every additional outside vertex
is blue to r. Its **footprint** S is its red neighborhood inside H; its blue
neighborhood inside H is the complement D=V(H) minus S.

1. A K5 involving one outside vertex and four H vertices is impossible in
   red, since H has no red K4. Its blue exclusion says precisely that S meets
   every blue K4 of H.
2. For outside vertices x,y with footprints S,T, a red xy is allowed by all
   three-H/two-outside K5 constraints exactly when H[S intersection T] has no
   red triangle. A blue xy is allowed exactly when H[V(H) minus (S union T)]
   has no blue triangle. Both colors can be forbidden.
3. A five-set meeting r, an outside vertex, and H cannot be monochromatic:
   r is red to H and blue to the outside. The fixed core itself is Ramsey.

These cases prove soundness **and completeness for at most two outside
vertices**, without degrees, automorphisms, quotas, or normalization. The
function `analyze.pair_colors(red_rows,S,T)` returns the permissible colors;
False denotes blue, True red. It assumes the two unary footprints are valid
and the core has the stated Ramsey property.

For a Ramsey(4,5) vertex extension of H, the new vertex must instead have
**no red triangle in S** as well as no blue K4 in D. Exhaustion shows no such
S among all 1,048,576 subsets. An independently implemented recursion visits
all 35,613 red-triangle-free sets and exhibits a missed blue K4 for each.
No solver, catalogue, or external numerical Ramsey value is needed.

The general pairwise-core method also appears in the separate M=214,c=13
handoff at Discovery Net height 2969,
`bafkreigl5xpol5rwgkymeo3xi5ikrqvgjv55txzo6qmvegazysdzipd6du`, source
`3868e4b9f15078a64a05eee233f231bed1bfcbff`. That different-core witness
illustrates why a pairwise interface is insufficient. Its body was inspected,
but its source is not imported or independently revalidated here. The
candidate-specific H20 nonextension and domains are the new finite work;
the generic extension rules are not claimed as a new derivation.

## Marked R55 domains and global obligations

Embed local H vertices as global `[1,2,3..10,19..24,35..38]`, with r=global 0.
The outside vertices lie in the three prescribed classes C2,C4,C6 of sizes
8,10,4, respectively. In a 20-bit mask for S, the two low bits indicate
membership of local 0 and 1. Thus these classes have low-bit values 1,2,3.

| Low-bit type | Outside multiplicity | Unary footprints | Inclusion-minimal footprints |
|---|---:|---:|---:|
| 1 | 8 | 43,348 | 140 |
| 2 | 10 | 67,786 | 252 |
| 3 | 4 | 126,151 | 350 |

Minimality permits deletion of vertices 2 through 19 only: the two marked
incidences stay fixed. Every unary footprint contains a minimal one of its
own type, and every same-type superset of a minimal one is unary valid.
**Minimal footprints cannot replace full footprints in a global search**:
adding vertices changes degrees and red pair compatibility. The minimal
lists are an exact monotone representation of unary validity, not an
exhaustive list of possible actual neighborhoods.

For the declared degree profile, the 22 footprints must satisfy the 20
individual column equations

```
sum_x 1[v in S_x] = 19 - d_H(v)   for v=0,1,
                   20 - d_H(v)   for v=2,...,19.
```

Their right-hand sides sum to 214. Each outside vertex requires red degree
`21-|S_x|` in the outside graph, equivalently blue degree `|S_x|` there.
The outside graph must have no red K5 and no blue K4 (the latter extends
with r), and must have 124 red and 107 blue edges. The inherited other-anchor
profiles and every K5 involving at least three outside vertices still need
to be enforced. None of these simultaneous feasibility conditions is decided
by the domain census.

## Stronger, graph-specific consequences

Every valid footprint contains a red triangle by the nonextension result.
Consequently:

- Two vertices with identical footprints cannot be joined red. If their common
  blue footprint contains a blue triangle, they cannot both occur at all.
- Otherwise repeated copies must be pairwise blue and there can be at most
  three: four copies together with r would be a blue K5. The numbers of
  footprints for which even a pair of copies is allowed are 1,365, 2,363,
  and 10,630 in the three classes, respectively. This does not certify any
  multiplicity as globally realizable.
- In fact the exact capacity of pairwise-blue copies **inside the core-plus-
  copies graph** is `min(3,4-omega_blue(H[D]))`, where D is their common blue
  footprint and `omega_blue(empty)=0`. Unary validity guarantees this clique
  number is at most three. A blue clique of size k in D together with
  `5-k` copies would be a blue K5; four copies together with r are also
  forbidden. Conversely these exhaust the possible blue K5s in this small
  graph, and a red K5 cannot use two copies. Thus the capacity is one when D
  has a blue triangle, two when D has a blue edge but no blue triangle, and
  three when D has no blue edge. `analyze.clone_capacity` implements this
  exact higher-order test. It does not decide whether a permitted number of
  copies can coexist with other outside vertices, degrees or profiles.
- For each of the 104 red triangles Q of H, at most three outside footprints
  can contain Q. All such vertices are pairwise blue by the red pair rule,
  so four again contradict the blue-K4-free outside graph.
- For each of the 153 blue triangles Q of H, at most four outside footprints
  can avoid Q. They must be pairwise red by the blue pair rule, and five
  would be a red K5.

These are necessary higher-order capacity cuts, not a sufficiency theorem.
The proof applies to the explicit graph and is invariant under consistent
relabeling; no assumption about an automorphism of the 43-vertex graph is made.

## Algorithms, verification and reproduction

Use CPython 3.11.2, standard library only, from this directory:

```
python3 -B analyze.py --work /scratch/r55-footprint-replay
python3 -B verify.py --work /scratch/r55-footprint-replay --report /scratch/r55-footprint-check.json
python3 -B controls.py --report /scratch/r55-footprint-controls.json
cmp /scratch/r55-footprint-replay/analysis.json analysis.json
cmp /scratch/r55-footprint-check.json verification.json
cmp /scratch/r55-footprint-controls.json controls.json
sha256sum -c SHA256SUMS
```

Choose a fresh work directory. Repeat all three Python programs with `-O`
and separate output paths; outputs and generated domain streams must agree.
The work directory contains `domains.txt` and `minimal.txt`, with canonical
lines `type five-digit-lowercase-hex-mask`. These are local regenerated
enumerations, not published opaque certificates. The verifier compares every
one of 237,285 domain entries and 742 minimal entries, not merely their counts.

The producer computes subset edge counts and red/blue triangle and blue-K4
presence by a least-vertex recurrence. Edge counts never exceed 190, so its
byte storage is exact. The independent checker imports no producer module:
it enumerates cliques from edge sets, marks all supersets of literal forbidden
cliques, and separately enumerates every red-triangle-free subset by an
increasing-vertex recursion. Each rejected extension has a literal missed
blue four-clique. Both methods reconstruct the full domain streams.

Controls test the pair reduction against **32,256 complete literal seven-vertex
graphs**: every red-K4-free four-vertex core, every pair of footprints, and
both outside edge colors, with the universal root retained. All five-subsets
are tested. Eight malformed graphs, three invalid footprints and three
malformed domain streams are rejected. Another 4,032 literal graphs test every
footprint and one through four pairwise-blue copies on the same 63 small
cores, checking all five-sets against the exact clone capacity. Normal and
optimized Python agree.

This is author validation with different algorithms, **not independent peer
review or proof-assistant formalization**. Trust remains in the short
unformalized reduction, code coverage, Python integer/runtime semantics,
hardware and input identity. All data and code needed for regeneration are
published; no solver result or floating-point decision enters the claims.
The triangle and footprint counts are scoped finite invariants, not counts
of 43-vertex graphs or exclusions of their isomorphism classes.
