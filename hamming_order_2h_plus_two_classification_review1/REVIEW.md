# Review report

## Claim alignment and verdict

The reviewed graph contribution asserts that for `h >= 6`, every order
`2h+2` induced subgraph of a finite Hamming graph with minimum degree at least
`h` has **exactly one** of three descriptions:

- (L) one coordinate line;
- (E) two disjoint `(h+1)`-point subsets of distinct coordinate lines;
- (U) an `(h+2)`-point line and an `h`-point line, with the latter covered by
  cross-edges.

It also asserts the converses, that (U) is two-dimensional, and that a
connected example not contained in a coordinate two-flat is two `(h+1)`-point
lines joined by one edge in a third direction.

**Verdict:** verified after one necessary correction.  The three descriptions
are an exhaustive cover, but they are not mutually exclusive.  The converse,
threshold, and connected three-dimensional consequence survive unchanged.
The public `PROOF.md` says only “one of the following holds”; the false word
“exactly” occurs in the immutable graph claim.

## Counterexample to exclusivity

Fix any `h >= 1` and work in `K_(h+2) square K_(h+2)`.  With `p=(0,0)`, put

```text
A={(a,0):0<=a<=h},        B={(0,b):1<=b<=h+1}.
```

The sets are disjoint, each has `h+1` points, and each lies on a distinct
coordinate line.  Therefore `C=A union B` has form (E).  On the other hand,

```text
L=B union {p},             R=A-{p}
```

have sizes `h+2` and `h`; they lie on distinct lines, and every point of `R`
is adjacent to `p in L`.  Thus `C` simultaneously has form (U).  Each vertex
already has at least `h` neighbours within its original `(h+1)`-point clique,
so this is an `h`-core of the claimed order.

This is a classification-label defect, not a counterexample to coverage.
The proof itself selects a *maximum* line: the displayed set has maximum line
size `h+2` and enters its (U) branch.  Mutual exclusivity is restored by saying
“at least one” or by restricting (E) to maximum selected-line size `h+1`.

## Human premises and completeness reductions

1. **Host model.** Vertices are coordinate tuples and adjacency means
   difference in exactly one coordinate.  Order-one factors cause no issue
   after geometric lines are identified by their vertex sets.
2. **Line facts.** A clique of at least three points lies on one coordinate
   line.  A point outside a coordinate line has at most one neighbour on it.
   Both follow immediately by comparing differing coordinates.
3. **Shell count.** At a fixed vertex, a selected direction-`i` neighbour has
   the same `a_i+1` selected points on its line and therefore needs at least
   `h-a_i` selected neighbours at distance two.  A distance-two point is
   reached from at most the two intermediate coordinate changes.  Hence
   `|C| >= 1+A+(1/2) sum a_i(h-a_i)` without assuming regularity or equal
   alphabet sizes.
4. **Cap reduction.** If every selected line has at most `h` points, every
   positive `a_i` is at most `h-1`.  For `A>=2h-1`, each penalty is at least
   `a_i`, contradicting order `2h+2`.
5. **Capped majorization.** For `A=h+t`, `0<=t<=h-2`, convex concentration of
   the squares makes `(h-1,t+1)` the extremal profile.  It gives
   `2h+t(h-t)/2`; integrality excludes every `t>=1` once `h>=6`.
6. **Last profile.** At `A=h`, the unique largest-square partition is
   `(h-1,1)`; the next, `(h-2,2)`, already gives `3h-3>2h+2`.  Thus the list of
   possible capped profiles is complete.
7. **Divisibility closure.** A `(h-1,1)` vertex belongs to a unique selected
   `h`-point line.  Every point of that line has it as its unique such line;
   distinct chosen lines cannot meet.  They partition `C` into `h`-sets, but
   `h` does not divide `2h+2` for `h>=3`.
8. **Disconnected reduction.** Minimum degree `h` makes every component have
   at least `h+1` vertices.  At the exact total order there are two complete
   components of order `h+1`, hence two line cliques and form (E).
9. **Maximum-line completeness.** For connected nonlinear `C`, a point off a
   maximum line `L` has at most one neighbour on `L`.  Thus the outside set has
   at least `h` points, while the preceding argument supplies `|L|>=h+1`.
   Only the splits `(h+2,h)` and `(h+1,h+1)` remain.
10. **The two splits.** In the first split every outside point attains the
    degree upper bound, so the outside set is a covered line clique, giving
    (U).  In the second, the outside graph is a clique minus at most a
    matching.  It contains a triangle, and every remaining point meets at
    least two triangle points; the line facts put the whole outside set on one
    line, giving (E).
11. **Incidence catalogue.** Parallel lines have no cross-edges or a matching.
    Lines in different directions have no edges, a star in their common
    two-flat, or one edge in a third direction.  Coordinate comparison rules
    out every omitted pattern.  The target checker's aggregate `single` bucket
    also counts singleton parallel matchings, but the written direction split
    is correct and the label does not affect the proof.
12. **Three-dimensional consequence.** Coverage makes every (U) example
    two-dimensional.  For connected (E), empty incidence is disconnected,
    and matching/star incidence is two-dimensional; only the unique
    third-direction edge remains.  Since each line has at least two points,
    all three directions genuinely vary.
13. **Converses.** An (E) point has `h` neighbours on its own line.  In (U),
    large-line points have at least `h+1` internal neighbours and small-line
    points have `h-1` plus a stipulated cross-neighbour.  An (L) set is a
    clique of order `2h+2`.
14. **Majority-C application.** Substituting `h=s-1` turns order `2s` into the
    theorem's order.  A maximum-colour majority-C class is connected because
    separately recolouring disconnected components preserves all same-colour
    degrees and adds colours.  The stated repair consequence remains
    conditional on the parent reduction that a “legal minor-box part” is such
    an `h`-core; this theorem does not itself establish that parent reduction.

## Adversarial smallest cases and independent computation

- The full `K_4 square K_3` at `h=5` has order 12, degree 5, directional
  profile `(3,2)`, and none of (L), (E), (U).  This verifies both sharpness and
  the precise profile that escapes the `h>=6` inequality.
- At `h=6`, direct enumeration covers 2,122,656 order-14 subsets of
  `K_2 square K_8`, `K_2 square K_9`, `K_3 square K_7`,
  `K_3 square K_6`, `K_4 square K_4`, `K_4 square K_5`, and
  `K_2 square K_2 square K_6`.  Exactly 1,923 are 6-cores, and every one has
  at least one asserted form.
- Explicit witnesses separately exercise (L), disconnected lines, a parallel
  matching, a two-flat star, a third-direction unique edge, unequal parallel
  lines, and the (E)/(U) overlap.
- All 27 triangles and all 648 outside-point/line pairs in the ternary
  three-cube satisfy the two elementary line facts.

The independent program enumerates vertex sets and recognizes forms from
their definitions.  This differs from the target's profile enumeration and
enumeration of pairs of preselected line subsets.  Agreement is corroboration,
not the universal completeness argument.

## Source and literature audit

The target checkout at public commit
`b2c6bbf7e034cebb2c606df1032a283907ab919a` reproduced its expected output,
five tests, and complete hash manifest.  Its code is standard-library exact
integer/rational computation with no omitted certificate.

The originating paper's Open Problem 2 really asks for the three- and
four-dimensional imbalanced Hamming cases, and its Observation 1 states that
maximum-colour classes are connected.  Dong's paper studies maximum degree in
large induced Hamming subgraphs, while Klavzar--Peterin characterize Hamming
embeddings; neither source states this minimum-order/minimum-degree boundary
classification.  This supports the target's careful search-relative scope,
not a claim of historical priority.

Primary sources checked live on 2026-09-20:

- <https://arxiv.org/html/2608.27669v1>
- <https://arxiv.org/abs/1912.01780>
- <https://doi.org/10.1002/jgt.20084>

## Trust boundary

The corrected universal cover is accepted from the audited human proof.  The
independent computation is exact but finite.  There is no proof-assistant
formalization.  The majority-C consequence additionally trusts the parent
minor-box reduction, and novelty remains search-relative.
