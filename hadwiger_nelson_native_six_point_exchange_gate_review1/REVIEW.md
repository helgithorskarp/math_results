# Review of the native B503 six-point exchange gate

## Claim and verdict

At commit `c418ae6bacc76c2f48ee4daa051273651ee898f3`, the target proves:

> Let `H` be its explicit 3,919-point strict plane unit-distance host and `B`
> its displayed 503-point subset.  For every `S` contained in `H minus B` with
> at most six points, `H[B union S]` is four-colourable.

**Verdict: ACCEPT with high confidence for exactly that scope.**  The deletion
corollary is also valid: restricting a four-colouring of `B union S` colours
`(B minus R) union S` for every `R` contained in `B`.

## Geometry and positive witnesses

The review imports only the source of the previously accepted independent
native-host geometry checker, after checking its SHA-256 pin.  That checker
constructs coordinates in `Q(sqrt(3),sqrt(5),sqrt(11))`, examines all
7,677,321 unordered pairs, and obtains 3,919 distinct points and exactly 29,125
unit edges.  Stable point and edge hashes match the earlier independent review.
This establishes an actual plane realization with the complete strict
unit-distance edge set, rather than an abstract chromatic graph.

The 126 inherited words and 40 new words are distinct, have length 3,919, fill
all 503 base positions, and use only `0,1,2,3,.`.  Direct review performs
3,681,762 retained-edge checks and finds no monochromatic edge.  Three malformed
word controls are rejected.  The omission-mask transcript has SHA-256
`b6411520399bcab24e81293e12130166c6b7d77576cd92bbf418496c10f5e61d`.

## Reduction to qualified six-sets

If `B union S` were not four-colourable, repeatedly delete any new vertex of
degree at most three.  A four-colouring after such a deletion could always be
extended with one of four colours, so the remaining counterexample has every
new vertex of degree at least four.  There are 585 free host points already
having at least four neighbours in `B`.  Padding with unused such points gives
exactly six new vertices without destroying non-four-colourability or the
degree condition.  Thus exhaustive coverage of degree-qualified six-sets is
sufficient for every `|S| <= 6`.

The review rebuilt the free graph and confirmed 2,549 qualified free edges,
including 1,238 with a base-degree-three endpoint.  Its canonical tuple growth,
which is neither target ESU nor tree-map code, independently obtains 18,965
qualified connected triples, 175,654 quadruples, and 1,856,054 quintuples.

## Connected selections

Every connected six-vertex graph contains a spanning tree.  Up to isomorphism,
the six trees are the star, path, degree-four broom, double star, and the two
degree-three trees with arm lengths `(3,1,1)` and `(2,2,1)`.  The reviewer
verified this independently by testing every connected labelled graph on six
vertices: all 26,704 contain a relabelled copy of a listed template.

The review C++ search visits every injective template map with no automorphism
ordering at all.  Its qualified counts are:

| shape | qualified maps | uncovered |
|---|---:|---:|
| star | 12,968,400 | 0 |
| path | 27,750,742 | 0 |
| broom | 17,013,870 | 0 |
| double star | 18,664,008 | 0 |
| arms `(3,1,1)` | 22,437,512 | 0 |
| arms `(2,2,1)` | 22,697,448 | 0 |

Each count is exactly the target's symmetry-quotiented count times the relevant
tree automorphism-group order.  All induced free edges—not only tree edges—are
included in the degree test.  This independently corroborates the target ESU
count of 21,289,412 distinct qualified connected six-sets and its zero-survivor
result.

## Disconnected selections

The possible component partitions are exhaustive:

- `5+1`, `4+2`, and `4+1+1` are covered by joining the corresponding connected
  group to a high-base-degree singleton or one of 172,058 qualified two-point
  completions.
- `3+3` is checked directly over the complete triple inventory.
- `3+2+1` and `3+1+1+1` are overapproximated by branching on an atom that hits a
  still-uncovered initial word, followed by a complete two-point or singleton
  query.  The review finds exactly 13 distinct six-point survivors of the first
  126 words.  They are exactly the 13 selected sets in `positive_cases.json`;
  their complete words pass 31,661 checks on actual retained unit edges.
- If all components have size at most two, every component is represented by a
  cost-one high singleton or a cost-two edge with a base-degree-three endpoint.
  A high-high pair may safely be represented by two singletons.  Dropping
  disjointness and cross-edge restrictions only enlarges this atom search.

For the last case, masks contained in another mask of equal or lower cost are
deleted.  This is safe because replacing a dominated atom preserves every hit
and never raises total cost.  The reduction leaves 494 singleton masks and
1,162 pair masks.  Exhaustive zero-, one-, two-, and three-pair cases find no
cost-at-most-six cover of all 166 word indices.  Independent randomized/exact
controls compare both the Python reference and compiled implementation with
brute force.

These cases cover every integer partition of six and complete the contradiction.

## Target replay and controls

The target package passed SHA-256 verification.  A fresh normal replay with
both author connected-six algorithms took 156.10 seconds.  A separate
assertion-disabled replay took 116.87 seconds.  The spanning-tree and ESU files
agree entrywise for every triple, quadruple, and quintuple.  The target control
suite passed under C++ undefined-behaviour sanitization: 20 graph cases include
398 deliberately uncovered sets; 90 cover cases include 74 feasible instances;
four malformed words are rejected.

The reviewer control suite additionally checks 100 weighted instances against
brute force, 2,000 exact bit-column queries, 40 compiled weighted instances
under UB sanitization, the complete labelled six-graph template census, and a
sanitized `K6` traversal with known map counts.

The target's separate rotation pilot also replayed: the exact host
`L union ((7+i sqrt(51))/10)L` has 3,919 points and 29,096 unit edges, and its
published complete four-colouring is valid.  This only rejects that one
alternative host; it is not used in the accepted B503 theorem.

## Limitations

The result does **not**:

- improve the published 509-vertex five-chromatic plane unit-distance record;
- produce any new five-chromatic graph;
- exclude selections with more than six free points;
- exclude a changed base, points outside `H`, other rotations, or other plane
  constructions;
- establish a global lower bound for five-chromatic plane unit-distance graphs;
- formalize the computation in a proof assistant.

The fixed-base insertion lane is now rigorously closed through six and should
not be extended mechanically to seven without a fresh portfolio argument.
