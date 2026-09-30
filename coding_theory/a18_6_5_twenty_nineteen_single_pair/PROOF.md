# A single pair between points of degrees twenty and nineteen

Agent: **six-code-3**. Role: **researcher**. Date: 2026-09-30.

**Computer-assisted lemma.** Let `F` consist of distinct five-subsets of an
eighteen-point set, with intersections at most two between distinct members.
If distinct points `x,y` have degrees `d_x=20,d_y=19` and pair multiplicity
`lambda_xy=1`, then **`|F|<=57`**. This is an upper bound; an exact maximum
or an attaining 57-word example is not asserted. There is no fixed-incumbent
or code-automorphism hypothesis.

The mathematical reduction below is complete for these hypotheses. The
computation uses exact pair covers and checked proper graph colorings. It
never attempts to infer nonexistence from heuristic coloring failure.

## First-star normalization

Every pair multiplicity is at most five: the complementary triples of
words containing a fixed pair are disjoint on sixteen other points. At `x`,
the pair-deficit row therefore has sum `17*5-4*20=5`. The deficit four at
`y` forces a unique further deficient neighbor `a`, with `lambda_xa=4`;
all other neighbors have multiplicity five.

The proved `(1,4)` split in the previous
[single-pair result](../a18_6_5_saturated_single_pair/PROOF.md), Sections 1--2,
applies to this one star without any assumption that `y` is saturated.
For clarity, its reduction is as follows. Deleting `x` gives twenty
quadruples on seventeen points. Their uncovered-pair graph has degrees
thirteen at `y`, four at `a`, and one at each other point. If `t` records
the edge `ya`, `m` counts edges between the other fifteen points and `s`
counts their edges to `y,a`, then `17=2t+s`, `15=s+2m`; hence `t-m=1`,
forcing `t=1,m=0`. Merging `y,a` gives a `2-(16,4,1)` design, with one of
the five lines at the merged point assigned to `y` and the other four to
`a`. No preimages can collapse to the same quadruple because they would
share three other points.

Every `2-(16,4,1)` design is an affine plane of order four. The previous
result supplies the elementary parallel-class argument and complete Latin
normalization: 24 first-row-normalized Latin squares give two unordered
orthogonal triples, both explicitly mapped to `AG(2,4)`. Its checked
plane group is transitive on the eighty point-line flags. Import only
that normalization here, and write `V={0,...,15}`, `x=17,y=16`, `a=0`,
`L={0,1,2,3}`, `T={1,2,3}`. The first star is exactly

```
{ {17} union B : B in P, B!=L } union { {16,17} union T },
P=AG(2,4).
```

The present generator uses the previous field geometry. The separate
checker imports no generator or geometry module: it uses an explicit
four-element multiplication table and a nine-generator permutation closure,
checks all 5,760 permutations preserve `P`, and obtains the same
72-element flag stabilizer. Only valid relabelings are used; the packing
is never assumed to possess a symmetry.

## The complete nine-edge leave reduction

The other eighteen words at `y` give old quadruples `Q` on `V`, pairwise
intersecting in at most one point. Each meets `T` in at most one point.
It meets every line of `P` except `L` in at most two points by cross-star
compatibility. The condition on `T` also checks `L=T union {0}`, so `Q`
is a four-arc of `P`. Among all 1,820 old quadruples, exactly 714 satisfy
these conditions. The 840 four-arcs have intersection-with-`T` counts
`336,378,126` for intersection sizes `0,1,2` respectively.

The eighteen quadruples cover 108 distinct old pairs. The common word
covers the three pairs of `T`. Their old-pair leave `H` consequently has
nine edges and no edge within `T`. Define `delta_z=5-lambda_yz>=0`. Then

```
deg_H(z)=1+3*delta_z, z in T;
deg_H(z)=3*delta_z,   z outside T;
sum_{z in V} delta_z=5.
```

Indeed, an old point outside `T` has `3*lambda_yz` covered old neighbors;
a point in `T` has `2+3*(lambda_yz-1)=3*lambda_yz-1`. Also
`sum_V lambda_yz=4*d_y-lambda_yx=75`.

At most eight vertices of `H` are active. A deficit at least three would
force degree at least nine and is impossible. Two deficits two leave at
most six active vertices, insufficient for a required degree at least six.
If one deficit is two, there are four deficient points and at most seven
active vertices. Its degree six or seven forces all four deficient points
outside `T`. The doubled point is adjacent to all six other active points;
the other three outside points must form a triangle. This forces `K4` on
the deficient points plus edges from the doubled point to every point of `T`.

Otherwise there are five deficits one. At most one is in `T`, since a
deficient `T`-point needs four outside neighbors and two deficient `T`-points
would leave only three outside active points. Thus the following three
profiles cover every possible leave:

| Profile | Deficient old points | Leaves per support | Labelled leaves |
|---|---|---:|---:|
| 0 | One doubled and three single deficits, all outside `T` | 1 per marked four-set | 2,860 |
| 1 | Five single deficits, all outside `T` | 605 | 778,635 |
| 2 | One single deficit in `T`, four outside | 28 | 60,060 |

These are candidate leaves, not counts of realizable stars. The counts
605 and 28 are complete small-graph enumerations. The generator chooses
internal support edges and attachments of the degree-one `T`-vertices.
The checker instead recursively chooses all neighbors of the first
vertex of positive remaining degree, with the prescribed degree sequence
and forbidden `T`-edges. It checks the resulting actual leaf sets.

The flag group has 72 permutations, transitive on `T`. Complete support
orbits give respectively 50, 30, and 40 representatives; profile 2 first
normalizes its deficient `T`-point to 1 and uses the 24-element stabilizer.
Further quotienting each support's leaf set by its actual stabilizer gives
50, 10,942, and 863 leave representatives, or 11,855 in all. Both programs
explicitly generate disjoint orbit unions covering the full domains. The
header lists are compared entry by entry, with reconstruction of all
841,555 labelled leaves. No divisibility or orbit-count inference
substitutes for explicit coverage.

## Pair covers and residual colors

Fix one of these nine-edge leaves. Remove its pairs and the three `T`
pairs from the 120 old pairs. A second star is exactly a cover of the
remaining 108 pairs by eighteen six-pair columns, one for each of the
714 allowed old quadruples whose pairs all lie in this target. Exact
pair coverage checks all within-star intersections, while the allowed
quadruple definition checks all cross-star intersections. Conversely,
every star with the stated hypotheses supplies one such exact cover.
There is **no assumption that a partial star completes to an affine plane**.

The generator branches on an uncovered pair with fewest available
columns, represents availability and pair conflicts by integer bitsets,
and enumerates all covers. The separate checker uses Algorithm X with
linked sparse columns and exact cover/uncover operations in `cover.cpp`.
The simpler Python set Algorithm X is retained in `verify.py`; its first
100 cases agree entry by entry with the generation and native replay.
The native input is regenerated by the separate set/degree-sequence
checker. Every resulting cover is compared with the generator's exact
cover set, not merely its cardinality.

The complete census gives:

| Profile | Leave representatives | Realized representatives | Star pairs |
|---|---:|---:|---:|
| 0 | 50 | 45 | 248 |
| 1 | 10,942 | 76 | 182 |
| 2 | 863 | 124 | 663 |
| Total | 11,855 | 245 | 1,093 |

These star pairs form a relabeling cover. They are not claimed to be
pairwise inequivalent full codes or star systems. Every star union has
38 words: twenty at `x` plus nineteen at `y`, sharing one common word.
Every remaining word is an old five-subset avoiding both centers. The
first star permits exactly 378 old five-subsets. The generator intersects
precomputed candidate masks to filter these by each second star. The
checker instead scans all 4,368 old five-subsets against the actual first
star, then checks every retained candidate against the full star union.
Every residual list is compared entry by entry.

Join two residual candidates in a graph if their intersection is at most
two. A compatible residual code is precisely a clique in this graph. The
generator produces a proper coloring by a deterministic saturation rule.
The separate checker groups the actual old sets by their supplied color
and verifies that **every two sets in one class intersect in at least
three points**. Thus at most one word of a compatible residual code can
belong to each color class. A proper coloring is an exact upper
certificate even though its choice is heuristic.

Every one of the 1,093 residual graphs has a checked coloring with at
most nineteen colors. The largest residual universe has 69 candidates;
all three profiles have maximum coloring count nineteen. Consequently

```
|F| <= 38 + 19 = 57.
```

Coloring counts are not residual clique optima. Neither an exact optimum
nor attainment of the bound 57 follows from this calculation.

## Consequence for dense packings

The previous single-pair result also proves: degrees `20,20` with pair
multiplicity zero or one force size at most 56, and degrees `20,19` with
an absent pair force size at most 59. Combining these with this lemma,
**in every packing of at least sixty words, a pair joining a degree-20
point to a point of degree at least nineteen occurs at least twice.**
For the possible degree range in this sentence, import Brouwer's
[established A(17,6,4)=20 theorem](https://ir.cwi.nl/pub/6883/6883D.pdf)
by shortening; it implies every point degree is at most twenty.
The restricted bound 57 itself does not require this external theorem.
The same incidence bound gives at least eight and thirteen degree-20
points at sizes seventy and seventy-one. This consequence imposes
additional pair constraints around those points without settling the
global size bound.

## Evidence and trust boundary

The full deterministic replay has SHA-256
`b615a8fefb8ec2b55b3f4be0647ef7121ee50edac99af070b063b136a8afd6d1`.
The repository contains the source and compact expected summary; the
1,319,238-byte replay and native input/output are regenerated locally
and omitted from publication. It is replay evidence, not a standalone
machine-checkable exclusion certificate. The proper-color checks are
small exact certificates for each residual graph, but the complete
finite reduction still relies on replay and the written coverage argument.

Python uses arbitrary-precision integers and sets. In the native helper,
there are at most 120 headers and 714 rows of six entries, so node indices
are below 4,405; input checks additionally enforce a 10,000-node limit.
Masks are between zero and 65,535. Search node counts are capped at
200,000 per leave; totals below `11855*200000` fit the unsigned 64-bit
counter. The native helper does no fixed-width bit shifts or numerical
optimization. Clock comparisons only abort incomplete searches.

The same-researcher checks use different enumerations and representations;
they are not independent peer review. The written split, orbit transport,
degree-profile completeness and clique/color correspondence are not
formalized. No solver, floating-point bound, timeout, UNKNOWN verdict or
memory failure supplies a mathematical exclusion. The current global
interval **69--72 remains unchanged**.
