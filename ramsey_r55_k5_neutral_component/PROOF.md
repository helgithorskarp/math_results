# A complete neutral component, an exact six-edge improvement, and frozen K5s

## The retained relaxation

Let G0 be the 43-vertex graph in the parent exceptional-profile-switch artifact,
with graph SHA-256
`122ed044228839122d6dba6d0f1cb87480818a6a8e8b277b6e5504d2da2e2cbc`.
Write E={0,1,2} and C={3,...,42}. Define F to be the following **labeled** class:

- Every edge incident with E has its color in G0, including the red E triangle.
- Vertices of E have red degree 20; vertices of C have red degree 21.
- Each exceptional local red/blue edge-count profile is (92,107).
- No monochromatic K5 meets E.
- All 884 named pointwise root inequalities from the original realization hold.

Cell-edge quotas are **not** fixed in the definition of F. Nor do we assume
an automorphism, valid central hard local caps, or absence of central K5s.
The pointwise inequalities and their elementary Ramsey-recursion derivation
are inherited from the pinned parent. Membership is checked directly on each
stored graph. This is one fixed-incidence realization relaxation, not the
entire degree-profile stratum or the Ramsey problem.

Let K(G) count red plus blue K5s. A switch removes red ac,bd and adds red ad,bc
on four distinct central vertices, with all membership conditions in F retained.
The parent proves completeness of the signature test

```text
((X_a XOR X_b) AND (X_c XOR X_d)) == 0,
```

where X_v is v's red adjacency bitmask to E. All eligible four-edge supports,
not just cell-quota-preserving supports, are considered below.

## Complete K=358 neutral component and its first-decrease boundary

Restrict the switch graph on F to vertices with K(G)=358. The connected
component of G0 has exactly **15 labeled graphs and 16 undirected edges**.
It is stored in COMPONENT.json. Its adjacency, in certificate order, is

```text
 0: 1,2,3       1: 0,4        2: 0,5        3: 0,5,6,7
 4: 1,8        5: 2,3        6: 3,9        7: 3,10,11,12
 8: 4          9: 6,13      10: 7,14      11: 7
12: 7,14      13: 9         14: 10,12
```

The certificate records actual graphs, not graph-isomorphism classes. No
isomorphism quotient is used. All 15 happen to retain G0's cell quotas, but
this is a verified outcome, not an enumeration restriction.

Complete independent matching-based censuses inspect 259430 incident switch
supports: 44765 fail a pointwise inequality, 211677 further create a mixed K5,
and 2988 are admissible. The admissible incidences divide into 32 neutral
(16 undirected edges), 30 strictly decreasing, and 2926 strictly increasing.
Of the 86830 quota-changing candidate incidences, 27 are admissible, and all
27 increase K. There is therefore no missing quota-changing neutral edge or
lower exit concealed by the observed common quotas.

The complete lower boundary has 30 incidences leading to 18 distinct labeled
graphs. Their K totals, counted with source/switch incidence multiplicity, are

```text
353: 7       354: 6       356: 4       357: 13.
```

In particular, after any number of neutral moves from G0, the best possible
**first strictly decreasing switch** reaches 353. This statement does not
bound what could happen after later decreasing moves or after an uphill step.
No search below this first-decrease boundary is performed here.

### Why the component certificate is complete

The producer performs a single-level breadth-first search, deduplicating full
labeled adjacency tuples. It enqueues every feasible zero-change neighbor and
records every negative exit without expanding that exit. It has a 128-processed-
state cap and a checkpoint after each complete state; closure was reached at
15, not inferred from the cap.

The independent verifier imports no search code. For every submitted graph it
checks all five-sets in both colors by literal and recursive algorithms. It then
enumerates all pairs of perfect matchings on every central four-set. Opposite
matching colors characterize alternating switches; literal exceptional local
edge-count changes determine the profile-preserving supports. It checks the
unmerged 884 named inequalities and new mixed K5s, and fully enumerates K5s
on every admissible neighbor. Thus the counts do not rely on the producer's
incremental K5 formula.

Every neutral neighbor reconstructed by this independent census must occur in
the certificate. Its neutral adjacency is symmetric and connected to G0.
Connectivity proves that all stored graphs belong to the component; closure
proves that no vertex in the component is omitted. Negative exits are retained
separately and do not invalidate closure **at the equality level**. This is
not a closed nonincreasing basin: decreasing exits exist.

## The two-switch witness and minimum improving edge distance

The best displayed path is

```text
(20,22,27,34), then (19,22,29,27).
(red K5,blue K5): (172,186) -> (179,179) -> (176,177).
K:                 358    ->    358    ->    353.
Phi:                86    ->     92    ->     90.
```

The first move reaches component vertex 3. The two moves toggle edge {22,27}
twice, so their net support consists of just six edges:

```text
remove red: {19,29}, {20,27}, {22,34};
add red:    {19,27}, {20,34}, {22,29}.
```

These form the alternating cycle 20,27,19,29,22,34,20. Each of vertices
19,20,22 has signature 3 and each of 27,29,34 has signature 4. This is a
bipartite three-edge matching trade between opposite signature cells. All
six complete exceptional color-neighborhood induced graphs remain unchanged,
as the verifier checks edge by edge. The endpoint has 176 red plus 177 blue
K5s; it is stored in EXIT_GRAPH.json. Literal five-set differences show that
16 red and 17 blue K5s are destroyed, while 20 red and 8 blue K5s are created:
33 removals minus 28 creations account for the decrease by five.

**Exact distance statement.** Among H in F with K(H)<358, the minimum edge
Hamming distance |E_R(H) symmetric-difference E_R(G0)| is exactly **six**.
The minimum number of nonincreasing four-edge switches to such an H is two.

For the lower bound, all graphs in F have the same total red edge count, so
an edit has equally many red additions and deletions and hence even size.
A nonzero two-edge edit cannot preserve each vertex degree: its one added and
one removed edge would have to have the same unordered endpoints. Any
degree-preserving four-edge edit is an alternating four-cycle. Since edges
incident with E are fixed, its support is central; profile preservation puts
it in the complete parent switch family. The full G0 census has no decreasing
admissible switch. Thus improving distances zero, two and four are impossible.
The displayed six-edge witness proves the upper bound. It also witnesses a
two-switch nonincreasing path, while the same census excludes a one-switch path.

This does **not** classify all six-edge edits, prove 353 minimal among all
six-edge edits, or say that a six-edge trade yields a Ramsey graph. The lower
bound comes from the complete four-edge census and the upper bound from one
verified six-edge trade. It is not a general catalog radius-six sweep.

## Frozen-neighborhood obstruction: antipodal-only repair cannot finish

The preceding endpoint preserves more than F requires. This gives a useful
limitation check on following the antipodal-only mechanism indefinitely.

Fix every exceptional incidence and all six exceptional color-neighborhood
induced graphs of G0. A central edge uv is absent from all six induced graphs
exactly when X_u XOR X_v=7: every exceptional root then sees its endpoints
in opposite colors. If the signatures are not opposite, some root sees both
endpoints in one color, exposing uv in that root's corresponding neighborhood.
This is the multi-root version of the diagonal-interface viewpoint already
used in the external two-anchor contributions; no novelty is claimed for
the visibility observation.

For the present multiplicities (0,8,8,6,10,4,4,0), the free central edges are
precisely the three opposite-cell blocks 1--6, 2--5 and 3--4, with respectively
32,32 and60 edges: **124 free edges and 656 fixed central edges**. All other
edges, including those incident with E, are fixed.

Among the existing K5s, exactly **96 red and 48 blue** have all ten of their
edges in the fixed part. These **144 specific five-sets** persist under every
recoloring of the 124 free edges, even without imposing degree or lifting
constraints. The lower bound is not claimed sharp. Of the 144, only 76 red
and 20 blue lie wholly in a single exceptional color neighborhood; the other
48 are fixed edge by edge across several neighborhoods. One fixed red example
is {3,6,11,14,20}; a fixed blue example is {3,22,24,35,38}.

`controls.py` reconstructs all K5s by literal and recursive enumeration,
independently classifies visible edges by the union of the six neighborhoods,
compares it to the opposite-signature test, and checks every claimed fixed
five-set. The canonical fixed-list hash is
`e0b3361093b0910c962a84a75cc8c7523cc9de77acfd4976495d4f29c7977bc0`.
All six neighborhoods of the displayed 353-K5 endpoint are the same as G0,
so the same obstruction applies there.

This is a scope limitation, not a new degree-profile exclusion. In particular,
the broader neutral component permits exposed neighborhood edges to change;
the 144 bound is **not** asserted throughout F. Any route from the displayed
endpoint to zero K5s must eventually change exposed neighborhood edges.

## Trust and remaining scope

The exact sources, reduction-to-code alignment, Python semantics, SHA-256 and
ordinary hardware remain trust boundaries. The pointwise-bound derivation and
retained-case provenance are inherited pinned inputs. No SAT verdict, group
package, catalog completeness, or symmetry exclusion is used by this census.
Normal and optimized Python checks agree; malformed component and exit data,
entry digests, and capped-run semantics are tested. This is algorithmically
independent checking by the author, not external peer review or formal proof.

The endpoint still has 353 forbidden five-sets, Phi=90, 35 central hard-cap
failures, and the same opposite-color exceptional-neighborhood gaps. There is
no certified Ramsey(5,5;43) graph, whole-profile closure, or Ramsey-bound gain.
The single-level component and its first-decrease boundary are complete; no
further descent, larger radius or new construction phase is begun in this pass.
