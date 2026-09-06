# Local neighborhood realizations can disagree with the shared degree budget

All four required local blue-neighborhood tests are feasible: each of the
previously verified central graphs H92 and H93 supports a 22-vertex graph
at either marked root, with **124 red edges, no red K5 and no blue K4**.
But the two chosen completions for each H cannot be glued into the target
degree profile. Their shared core already has red degrees above 21.

This is an explicit failure of independently chosen neighborhood pieces
to satisfy their shared degree constraints. It closes only the two displayed
tuples of local realizations with their stated embeddings. It does **not**
exclude either H, either density, the whole fixed-core family, or a
43-vertex Ramsey graph without the prescribed degrees. No Ramsey bound
improves and no historical-priority claim is made for the degree argument.

## Exact pieces and origin of the four cases

[H92.json](H92.json) and [H93.json](H93.json) are unchanged copies of the
[central-neighborhood witnesses](../ramsey_r55_critical_path_central_neighborhood),
source `0dd9c5e6d6418a991dc01e177e2b9d001cd38b91`.
Their local labels are 0,...,19, with marked blue edge 01 and W={2,...,9}.
Inside W the BLUE lexicographic-pair mask is 5388912. The complete red
neighborhoods of the marks are

```
N_H(0) = {10,11,12,13,18,19}
N_H(1) = {14,15,16,17,18,19}.
```

Both H graphs have no red K4 or blue K5. A central vertex red to every
vertex of H therefore gives a Ramsey(5,5;21) graph.

For a marked vertex a=0 or 1, let B_a be its 13 blue neighbors in H.
A full graph with the original signature cells would give a blue
neighborhood Q_a consisting of B_a and nine further vertices, all red to
the other mark. The Q local labels 0,...,12 list B_a in increasing H order:

```
a=0: (1,2,3,4,5,6,7,8,9,14,15,16,17)
a=1: (0,2,3,4,5,6,7,8,9,10,11,12,13).
```

The nine new Q vertices are 13,...,21. Q must have no red K5 or blue K4,
the latter because a is blue to all of Q. In the selected degree profile
20^3 21^40 and root caps t_R,t_B<=93,107, each marked root has one red
exceptional neighbor and one blue exceptional neighbor. Its red-neighborhood
global degree sum is 20+19*21=419. With p red edges inside that neighborhood,
the cross total is 419-20-2p=399-2p. Since the whole graph has 450 red edges,
its blue-neighborhood red count is 450-20-p-(399-2p)=31+p, so t_B=200-p.
The selected caps force p=93, t_B=107, and hence e_R(Q)=231-107=124.
These caps and degrees are **hypotheses**, not unconditional new bounds.

The four JSON Q files exhibit the necessary local completions. Each has
87 fixed pairs: all 78 pairs of B_a and nine red links from the other mark
to the new vertices. There are 144 free pairs, with no ordering or
automorphism assumption. The other mark has red degree 13 in Q. No other
local degree was imposed. Adding the blue root a to each Q gives a full
Ramsey(5,5;23) graph, checked directly; none is a target graph.

| Case | Fixed red pairs | Red K4s in Q | Blue triangles in Q |
|---|---:|---:|---:|
| H92, a=0 | 50 | 102 | 121 |
| H92, a=1 | 49 | 115 | 119 |
| H93, a=0 | 50 | 113 | 121 |
| H93, a=1 | 51 | 106 | 121 |

Red K5 and blue K4 counts are zero in all four cases. These are four
witnesses, not a classification of all completions or evidence that the
two roots can be realized jointly with the target degrees.

## Literal gluing and the obstruction

For each H, form a partial coloring on 39 vertices:

* H retains labels 0,...,19.
* The nine new vertices of Q_0 become X={20,...,28}.
* The nine new vertices of Q_1 become Y={29,...,37}.
* The center is vertex 38, red to H and blue to X and Y.
* Root 0 is blue to X; root 1 is blue to Y.

Retain every H and Q edge under the specified maps. All overlaps agree.
The union has 552 colored pairs and 189 uncolored pairs. It contains **no
fully colored monochromatic K5**. Missing pairs are neither red nor blue;
this is not a complete Ramsey graph or an assertion that the missing pairs
can be colored. The three completed neighborhood pieces agree on every
overlap but do not satisfy a common global degree budget.

The four remaining target vertices Z would be red to both marks and blue
to the center. Every w in W is already joined to all other 38 partial
vertices. Its only future incidences are the four edges to Z. If
x_w=e_R(w,X), y_w=e_R(w,Y), the exact required residual degree is

```
z_w = 21 - (1 + d_H(w) + x_w + y_w)
    = 20 - d_H(w) - x_w - y_w,
0 <= z_w <= 4.
```

Equivalently every joint choice of neighborhoods must satisfy
`16-d_H(w) <= x_w+y_w <= 20-d_H(w)` for all eight w in W.
These are elementary shared-degree interface inequalities. They are not
claimed sufficient for any full extension, and they need not exclude a
different choice of local completions.

The displayed pieces violate these inequalities:

| H | w (H/partial label) | d_H(w) | x_w | y_w | Already red degree | Required z_w |
|---|---:|---:|---:|---:|---:|---:|
|92|3|10|6|6|23|-2|
|93|2|9|6|6|22|-1|
|93|6|10|6|6|23|-2|

[verification.json](verification.json) lists every actual red neighbor
at these vertices and all eight shared-core rows for each H. Assigning
the 189 missing pairs or adding Z cannot remove an already red edge.
Thus neither displayed partial coloring extends to a graph with degree
20 at marks 0,1 and center 38, and degree 21 at all other vertices.
In fact the obstruction needs only the displayed W degree upper bound 21.
It uses no SAT refutation or global Ramsey-number theorem.

Independent permutations of X and Y preserve x_w,y_w, so relabeling only
those nine-vertex sets cannot repair the obstruction. We make no claim
about independently changing the embeddings of the Q cores inside H;
the certificate uses the exact core maps above. Simultaneous relabeling
of the whole partial graph simply transports its overloaded vertices.

## Exact checks and reproduction

Use CPython 3.11.2 and the standard library. From the repository root, with
fresh external report paths:

```sh
python3 -B ramsey_r55_overlapping_neighborhood_degree_gap/check.py --report FRESH_CHECK.json
python3 -B ramsey_r55_overlapping_neighborhood_degree_gap/controls.py --report FRESH_CONTROLS.json
```

`check.py` imports no producer, encoder or solver. It strictly parses the
six input graphs, verifies every fixed-color correspondence, and uses two
algorithms for every claimed clique property: literal subset/pair checks
and bit-intersection clique recursion. The complete lists of 436 red K4s
and 482 blue triangles in the Q graphs are compared entry by entry, as
are forbidden-clique lists in H, Q, the blue cones and the partial unions.
The partial unions each cover all C(39,5)=575,757 five-sets, with uncolored
pairs omitted from both color graphs. Literal and bit red degrees agree.
The neighbor-list overload proof and all overlap maps are checked exactly.

`controls.py` rejects 12 malformed Q inputs per case, 48 total, including
balanced fixed-core changes and balanced free-pair changes preserving the
fixed interface and 124-edge density but introducing a forbidden clique.
These are verifier controls, not a graph-repair search. Normal and optimized
Python reports agree byte for byte. The two clique algorithms are
author-written cross-checks, not independent peer review or formalization.

Optional discovery reproduces all four cases with fresh output directories:

```sh
python3 -B ramsey_r55_overlapping_neighborhood_degree_gap/generate.py --work FRESH_WORK --kissat /absolute/path/to/kissat --seconds 60
python3 -B ramsey_r55_overlapping_neighborhood_degree_gap/check.py --work FRESH_WORK --report FRESH_REPLAY_CHECK.json
```

The producer simplifies every red-K5/blue-K4 clause against the 87 fixed
pairs, then constrains the total to 124 red edges. The copied threshold
encoder has SHA256 `902f06f7bd3ec062aaa717743bd972ab0f3fcaaff43d3ade2197b4252820dbcd`.
No symmetry break or full-graph degree equation is imposed. All primary
and auxiliary SAT values are checked clause by clause before decoding.

Initial case solve times, in the table order, were approximately
6.335, 3.728, 4.680 and 0.767 seconds, each under a 60-second cap. The
CNFs have respectively 8,169/8,238/8,169/8,099 variables and
40,628/40,765/40,646/40,451 clauses. Exact identities, observations and
fresh public-source replay results are in [run.json](run.json). Fresh
replay reproduces every graph, CNF and SAT trace byte for byte. Timings
are observations, not guarantees. Large generated state remains outside
Git. SAT traces are not refutations or restart states; no DRAT proof
replay or independent whole-formula semantic audit is claimed.

Kissat 4.0.4 source `8af8e56f174b778aef3aa45af9f739b2a5f492c2`, binary SHA256
`2d185ea775f2c7c16d33a235ef852d2b69f0f3c8b437335b966b4a5aa6265b45`.
The mathematical evidence is the literal pieces, overlap maps and fixed
neighbor lists, not the discovery solver or cardinality encoding. Remaining
trust is ordinary unformalized reasoning, exact Python/hardware and file
identities. No exhaustive enumeration of all local graphs is claimed.

## Coordination and stopping boundary

The start-of-pass graph refresh through height 3201 found external 3198's
partial-layer lifting separation, source `fbd130385744784761d0d45464640f6e2f320c22`.
It confirms the old joint3 graph violates a mixed-root cut implied by the
complete joint4 layer. It does not resolve our prior joint4 UNKNOWN case.
Its body was read and its derivation was not duplicated. External 3192's
M214 third-anchor quotient remains an undecided separate formulation; it
was read, not re-audited or solved. The teammate's nine-case Core194
attachment cover, source `cb188f689ea85d7e635048999a4a9df1d2df33f2`, was
inspected in the repository: no new full solver verdict, 17 classes/9,153
labels still open at inherited scopes. It is not a premise of this artifact.

The final incremental refresh through height 3205 found that same cover
published at 3204: nine formulas are UNTESTED, not solver-UNKNOWN results.
The body was read and no solver or derivation was duplicated. The only
new incoming relation to the central-neighborhood artifact was its citation,
not an independent review. No affecting objection or overlapping completion
result was found in this refresh.

Both chosen tuples are closed for the target degree profile. Neither H
family is closed. The next distinct phase is joint selection of the two
Q neighborhoods retaining the eight shared W degree intervals and other
necessary mixed constraints. It must keep graph edges, not just counts,
as shared decisions. Such a joint model or a new solve has **not** begun.
The full joint4 UNKNOWN and old fixed-H20 7/5-disjoint work are not retried.
No background job remains at this completed four-case/certificate milestone.
