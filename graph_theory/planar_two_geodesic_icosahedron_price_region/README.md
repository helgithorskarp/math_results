# A thirty-dimensional price region for a face-stellated icosahedron

Every nonnegative vertex mass on the graph below has a half-balanced
separator made of at most two original-graph shortest paths, throughout
an explicit **closed, full thirty-dimensional box of core edge prices**.
Each price may vary independently by **7/151**, about 4.64%, about its
specified center. The mass may be supported on **all 32 vertices**.
The sixty face-attachment edge lengths are arbitrary positive numbers
subject to preserving the core metric.

This excludes a construction family considered for
[Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).
It is not a resolution of that problem or a counterexample. The proof
uses three alternative path pairs and two disjoint-heavy-component
implications. No search over vertex masses or parent choices is a proof
premise. Historical priority and independent peer review are not claimed.

## Graph and metric region

The core I is an icosahedron on vertices 0,...,11, with neighbor lists

```
0: 1 2 3 4 5       1: 0 2 5 6 10      2: 0 1 3 6 7
3: 0 2 4 7 8       4: 0 3 5 8 9       5: 0 1 4 9 10
6: 1 2 7 10 11     7: 2 3 6 8 11      8: 3 4 7 9 11
9: 4 5 8 10 11    10: 1 5 6 9 11     11: 6 7 8 9 10
```

List its twenty triangular faces in lexicographic order as sorted triples.
In face number i, starting at zero, add vertex z=12+i joined to its three
corners. The marked faces are

```
12:012   13:015   14:023   15:034   16:045
17:126   18:1,5,10        19:1,6,10
20:237   21:267   22:348   23:378   24:459
25:489   26:5,9,10        27:6,7,11   28:6,10,11
29:7,8,11        30:8,9,11        31:9,10,11
```

Here `012` means the triple (0,1,2), and comma-separated triples avoid
ambiguity for two-digit labels. Inserting one vertex in each face gives
a finite simple planar triangulation G with 32 vertices, 90 edges and
60 faces. Face vertices are called marks for the construction only;
the theorem allows mass at every core vertex as well.

The thirty integer center prices c_e are

| Edge | c_e | Edge | c_e | Edge | c_e |
|---|---:|---|---:|---|---:|
| 0-1 | 187 | 0-2 | 108 | 0-3 | 147 |
| 0-4 | 7 | 0-5 | 70 | 1-2 | 180 |
| 1-5 | 123 | 1-6 | 78 | 1-10 | 174 |
| 2-3 | 169 | 2-6 | 121 | 2-7 | 97 |
| 3-4 | 187 | 3-7 | 107 | 3-8 | 98 |
| 4-5 | 88 | 4-8 | 9 | 4-9 | 160 |
| 5-9 | 66 | 5-10 | 158 | 6-7 | 136 |
| 6-10 | 157 | 6-11 | 25 | 7-8 | 193 |
| 7-11 | 5 | 8-9 | 48 | 8-11 | 162 |
| 9-10 | 78 | 9-11 | 49 | 10-11 | 193 |

For any common scale lambda>0, independently choose each core edge length

    (144/151) lambda c_e <= L_e <= (158/151) lambda c_e.       (1)

Write d_I for the resulting intrinsic core distance. For each mark z in
face abc, its three positive incident lengths must satisfy

    L_zu + L_zv >= d_I(u,v)   for each distinct u,v in {a,b,c}. (2)

Condition (2) is exactly that I is isometric in G. Necessity follows by
considering the two-edge route u-z-v. For sufficiency, replace every such
transit in any core-to-core G-path by an I-geodesic. The resulting core
walk is no longer, so outside routes cannot shorten a core distance.
Equality in (1) or (2), and geodesic ties, are permitted.

One useful subfamily chooses an arbitrary parent corner for each of the
twenty marks, with an arbitrary positive parent-edge length. Let Q be I
plus these twenty edges. Give every other edge uv length at least
d_Q(u,v). Then Q's core distances survive, so (2) holds. Thus the result
covers **all 3^20 parent assignments simultaneously**, without enumerating
them, and all positive parent lengths. Condition (2) also allows stars
not represented by this sufficient parent-edge prescription.

## Six geodesics valid on the whole box

Use the following three candidate pairs:

```
A: (1,6,11,7,3)       and (2,0,4,8)
B: (1,6,11)          and (5,9,10)
C: (0,4,8,9,11,6)    and (1,5)
```

For each displayed path P, form its critical integer price assignment:
give every edge of P price 158 c_e, and every other core edge price
144 c_e. The compact [certificate](certificate.json) supplies a potential
pi_P on the twelve core vertices satisfying

    pi_P(start)=0,
    pi_P(end)=sum_(e in P) 158 c_e,
    |pi_P(u)-pi_P(v)| <= critical_price(uv) for every core edge uv.

Summing the last inequalities along any competing path proves that P is
shortest at its critical assignment. These are 180 exact integer edge
inequalities, verified without a shortest-path algorithm in `verify.py`.

For any competing simple path R, common edges cancel from L(P)-L(R).
This difference is maximized over (1) by putting P-only edges at their
upper bounds and R-only edges at their lower bounds. The critical
assignment does exactly this. Hence all six paths remain shortest
throughout (1), after scaling by lambda/151. Condition (2) makes them
ambient G-geodesics as well.

The radius 7/151 is **tight for this fixed path library and center**:
at the adverse corner the path 5-9-10 and edge 5-10 tie because

    158 (66+78) = 144 (158) = 22752.

Increasing the symmetric relative radius makes that displayed path cease
to be shortest at some corner. This does not assert that half separators
fail outside the box, or that the box is an optimal positive region.

## The mass argument

Deleting pair A leaves one nonsingleton component

    H_A = {5,9,10,13,16,18,19,24,25,26,28,30,31},

and ten singleton components. Deleting pair B leaves

    H_B = {0,2,3,4,7,8,12,13,14,15,16,17,20,21,22,23,24,25,27,29,30},

and five singletons. Deleting pair C leaves two nonsingleton components

    J_A = {2,3,7,12,14,15,17,20,21,22,23,27,29},
    J_B = {10,18,19,26,28,31},

and five singletons. Directly, H_A and J_A are disjoint, as are H_B and
J_B. These component statements concern the **full 90-edge graph**;
metric-long face edges remain present when components are computed.

Let M be the total nonnegative vertex mass. For M=0 any singleton works.
If some vertex has mass at least M/2, delete that singleton geodesic;
the remaining total is at most M/2. Otherwise every singleton is light.
If A or B is half-balanced, use it. If both fail, H_A and H_B each have
mass greater than M/2. Their respective disjoint sets J_A and J_B each
have mass less than M/2. Every component left by C is consequently light.
This proves exact half balance for **all nonnegative real masses on G**.

The three pairs are alternatives. The separator uses only the chosen
pair, or a heavy singleton, never the union of all six displayed paths.

## Boundary relative to the current guard results

The latest [connected-deletion fragment rule](../planar_two_geodesic_cycle_rank_representatives/README.md)
requires every connected deletion representative of a large residual
fragment to have an internal two-geodesic cover. No set S of at most four
vertices makes all components of G-S eligible for that guard, regardless
of edge lengths. Indeed, after deleting k<=4 core vertices the residual
icosahedron stays connected. At least 16 surviving marks still meet this
core: after up to 4-k mark deletions their number is at least

    20 - (4-k) - binomial(k,3) >= 16.

Take a spanning tree of the residual core, and attach every surviving
nonisolated mark through one chosen corner. This is a connected deletion
representative of the large residual component with at least sixteen
leaves. Two internal simple paths can cover at most four tree leaves,
even before imposing ambient shortestness. This representative fails the
guard test. The small-component exception is irrelevant to this component.
The checker verifies core connectivity for all 794 deletions of size at
most four. This distinguishes the present positive family from that
sufficient guard criterion; it does not compare against every known
positive class or contradict the guard theorem.

The earlier [cube price boxes](../planar_two_geodesic_cube_price_boxes/README.md)
provided a different construction-family exclusion. Here the graph,
thirty core prices, twenty attachment sites, and unrestricted vertex-mass
support differ. Neither result is claimed to imply the other. The
short proof here needs no RUP or Farkas certificate: six potential vectors
and the three explicit component partitions suffice.

## Reproduction and trust boundary

From the repository root, with Python 3.11+ and its standard library:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_icosahedron_price_region/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_icosahedron_price_region/audit.py
```

The main checker reconstructs the graph from an explicit adjacency list,
checks its face system, verifies all six shortest-path potentials, the
component partitions, the radius control, and the 794 core deletions.
It rejects a forged potential.

The separate audit imports neither the main checker nor discovery code.
It builds the graph from two oriented pentagonal rings and uses
Floyd--Warshall. It checks thirteen core metrics (the center, all six
critical corners, and six deterministic box samples), five attachment
models each including a three-point metric star, 3,900 star inequalities,
390 ambient path instances, and 10,725 exact integer-mass cases exercising
all three pairs and the heavy-singleton case. It also verifies that a
deliberately forbidden face shortcut does shorten the core. The seed is
2026092919. Expected compact outputs are in [expected.json](expected.json).

The universal real-metric box and real-mass conclusions rest on the
written critical-assignment and disjointness arguments plus the finite
exact certificate, not on the sampled metrics or masses. No external
solver, census, private dataset, omitted large certificate, or proof
assistant is required. The separate audit was written in the same
research pass; it is not an independent peer review.

Literature refreshed 29 September 2026: the cited workshop problem list
fixes the original-graph geodesic convention and half-balance target;
[Diot and Gavoille, Path Separability of Graphs](https://emilie-diot.eu/Article/DG10a)
provides earlier context for strong path separators. Targeted primary-
source searching did not establish priority for this explicit region.
No general open-status assertion is made from the workshop listing.
