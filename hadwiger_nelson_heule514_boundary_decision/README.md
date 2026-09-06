# H514 boundary saturation and a complete local extension decision

**The boundary-only extension shortcut fails.** The fixed sixteen-vertex
boundary of [H514](../hadwiger_nelson_heule514_interface/README.md) realizes
**every one of the 7^4=2,401 tuples of proper subsets of {1,2,3}** as the
four available-colour lists of its added path. Each of the
[37 exact path clauses](../hadwiger_nelson_heule514_path_projection/README.md)
has a proper boundary colouring that violates only that clause. Consequently
no clause can be removed using the induced boundary edges alone.

This complete local result was obtained by exact component convolution and
checked against a separate direct enumeration of **27,433,728** proper
boundary colourings, with the origin fixed to colour 0. Of these,
**3,408,768 extend** over the full path and **24,024,960 do not**.

This does **not** produce a five-chromatic graph, close H514, or settle any
of its 258,914 inherited residual graphs. A boundary colouring need not
extend to the retained old H510 graph. The local twenty-point graph is
four-colourable; a full positive witness is included. There were no native
H514 or SAT queries and no new deletion cuts.

## Fixed exact geometry

H514 is H510 followed by completion centres 170,436,1239,1527 at indices
510,511,512,513. The old index order is increasing labels marked `510` in
[the union certificate](../hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json).
The four new points induce P4 in that order and each is adjacent to origin 0.
Their remaining old neighbours are

| New vertex | Old neighbours other than 0 |
|---:|---|
| 510 | 361,417,495,503,509 |
| 511 | 418,498,506,508 |
| 512 | 359,362,502 |
| 513 | 358,416,507 |

Let B be these fifteen vertices together with 0. The parent projection
certificate proves every non-four-colourable H514 subgraph must retain B,
using sixteen explicit singleton-deletion colourings. That theorem is an
inherited dependency. Here we independently reconstruct the **twenty local
points** B union {510,511,512,513}, and every one of their 190 pairs.
Their complete unit graph has 35 edges; its induced boundary has 13.

The coordinates use the positive radical basis
`1,sqrt3,sqrt5,sqrt15,sqrt11,sqrt33,sqrt55,sqrt165`.
The producer uses the pinned parent integer arithmetic. The independent
checker implements multiplication recursively in the quadratic tower
Q(sqrt3)(sqrt5)(sqrt11), with rational coefficients, and imports no producer
or inherited arithmetic module. Every edge decision is exact.

Origin 0 is isolated within B. Its remaining connected components are

| Vertices | Graph | Proper four-colourings |
|---|---|---:|
| 358,416 | One edge | 12 |
| 359,502,507 | Three-vertex path | 36 |
| 361,362,417,418,498,509 | Four-cycle with a leaf at each of two opposite vertices | 756 |
| 495,503,506,508 | Four-cycle | 84 |

The four-cycle in the third row is `417–498–418–509–417`, with leaves
361 at 417 and 362 at 418. The last cycle is `495–503–508–506–495`.
Thus the normalized boundary count is
`12*36*((3^4+3)*3^2)*(3^4+3) = 27,433,728`.
[`boundary.json`](boundary.json) and [`boundary.txt`](boundary.txt) record
the complete labelled boundary graph and its neighbour-group membership.

## Saturation of all possible proper-subset lists

For a proper boundary colouring f with f(0)=0, let

`L_i = {1,2,3} minus {f(v): v in N_i}`,

where N_i is the corresponding row of the neighbour table. Each N_i
contains an edge, so its vertices cannot all have colour 0. Therefore
L_i is always a proper subset of {1,2,3}. The complete computation proves
the converse simultaneously: **every four-tuple of proper subsets occurs**.

The producer enumerates the proper colourings of each component and groups
them by which positive colours they use in the four N_i. Independent
components combine by bitwise OR of those blocked-colour masks; their exact
multiplicities multiply and then add. The successive component profile
counts are 6,42,2,058,2,401. This is an exact finite convolution, not sampling.
The code keeps a checked colouring representative of every intermediate
profile while computing its multiplicity.

The independent C++ program uses no decomposition or path kernel. It visits
boundary vertices in increasing order, assigns all four colours allowed by
previous boundary edges, and counts each complete colouring by its resulting
four lists. It visits 46,756,181 DFS nodes. The verifier compares **all 4,096
profile counts**, including zeros, order and EOF, with the convolution.
Positive entries occur exactly at the 2,401 indices whose four three-bit
list masks differ from 7. Hence both attainable lists and multiplicities
are completely accounted for.

## Every path clause remains necessary on this boundary

The parent relation has 37 clauses, indexed 0..36 in its certificate.
For each clause j, the public certificate gives a proper colouring of B
whose lists violate j, and another whose lists violate **only j**.
All 37 weighted attainability counts and all 37 weighted unique-violation
counts are positive and checked against the complete census.

Therefore even after restricting to actual proper colourings of this
induced boundary, none of the 37 clauses is redundant relative to the
other 36. This is a clause-necessity statement. It does not assert that no
different algebraic encoding can be shorter, or that the parent literals
remain prime after introducing extra geometric premises.

An illustrative witness, in the boundary order

```
0,358,359,361,362,416,417,418,495,498,502,503,506,507,508,509
```

is the colour string

```
0000032300333200
```

Its path lists are `{1}, {1,2}, {1,2}, {1}`. Both end vertices must have
colour 1, so their inner neighbours must both have colour 2, violating the
middle path edge. It violates precisely clause 25 of the parent relation.
The checker directly tests the path assignments and confirms that **every
one of the fifteen proper selections of the path vertices extends**. The
obstruction for this particular boundary colouring requires all four added
vertices simultaneously.

This is a counterexample to a universal extension assertion, not an
uncolourable graph. A different boundary colouring in the same certificate
extends over all four vertices and directly colours all 35 local unit edges.

## Complete counts

With origin colour 0:

| Quantity | Count |
|---|---:|
| Proper boundary colourings | 27,433,728 |
| Boundary colourings extending over P4 | 3,408,768 |
| Boundary colourings not extending | 24,024,960 |
| Attainable list tuples extending | 942 |
| Attainable list tuples not extending | 1,459 |
| Proper colourings of the twenty-point graph | 4,568,256 |

The last count sums the exact number of path extensions over every
boundary colouring. It is not just the number of extendable boundaries.
The parent dynamic program is not trusted for this count: the checker
exhausts all 81 path colour strings for each of the 4,096 possible list
tuples, including the unattainable ones.
[`result.json`](result.json) also gives the extension-count distribution
and the number of violated clauses for every profile and boundary colouring.

The complete profile stream remains local. It has 4,096 decimal counts,
one per line in increasing packed-list index, and is 15,027 bytes. A list
mask's bit c−1 means colour c is available, c=1,2,3, and the packed index is
`L0 + 8*L1 + 64*L2 + 512*L3`. The SHA-256 is

```
f1a7842afd51bcc1e7fcf5fe608fd45c6bdebd70133e65044775617814a867da
```

## Reproduction and trust

From the repository root, use a new output directory:

```sh
python3 hadwiger_nelson_heule514_boundary_decision/build.py --out /tmp/hn514-boundary
c++ -std=c++17 -O3 -Wall -Wextra -Werror hadwiger_nelson_heule514_boundary_decision/enumerate.cpp -o /tmp/hn514-boundary/enumerate
/tmp/hn514-boundary/enumerate < /tmp/hn514-boundary/boundary.txt > /tmp/hn514-boundary/direct.counts
python3 hadwiger_nelson_heule514_boundary_decision/verify.py --work /tmp/hn514-boundary
```

The checker also compares regenerated compact results with their public
bytes. Python 3.11.2 and GCC 12.2.0 were used. No Python packages or SAT
solver are required. Run the producer with assertions enabled. The checker
uses explicit exceptions. `manifest.json` pins inputs; `SHA256SUMS` pins
public artifacts. All arithmetic is exact; 64-bit counters safely exceed
the unpruned 4^15 boundary assignments.

Verification checks 190 exact geometric pairs, all 4,096 independent profile
entries, all 4,096 path states, the 37 attainability and unique-violation
witness pairs, the illustrative obstruction and all its proper selections,
and the positive full graph colouring: **1,023 witness-edge checks**.
The final Python audit took about 0.596 seconds. Direct enumeration wall
time and peak memory were not measured. `validation.json` records the
compiler, binary digest and one native enumeration. The producer was run
twice to choose an illustrative obstruction requiring the entire path;
the graph, all counts and census were byte-identical. No extra search
phase or target-order graph query occurred.

The trust boundary includes the archived coordinates, quadratic-tower
basis, faithful input parsing, exhaustive algorithms, integer/rational
arithmetic, and the ordinary proof connecting counts and extension.
The forced-boundary and 258,914-residual statements are inherited from the
pinned parent contributions. This new result has author-run algorithmically
independent validation, not a separate-author review or formalization.

## Decision and next unstarted milestone

The proposed universal-boundary shortcut is definitively closed. The
boundary imposes only the four proper-subset restrictions on the available
lists; it cannot remove any of the 37 clauses individually. A proof about
the actual H514 family must use additional old-graph information.

A concrete next family-level test is to apply **degree-at-most-three
peeling** to each of the 258,914 inherited residual induced graphs. If its
4-core omits any of the 484 certified forced vertices v, the core is a
subgraph of the already coloured H514−v. Restrict that colouring to the
core and restore peeled vertices in reverse order, each with at most three
coloured neighbours. This would certify the entire candidate with four
colours. Applying the test to the complete frozen frontier yields either a
closure or an exact surviving family, without new colouring-oracle calls.
The same argument applies if the core omits any of the full 516 known
positive omission sets, so that complete library should be tested as well.
That computation is unstarted. No unchanged omission-master extension,
boundary-radius ladder, retired H517/H574 deletion search, or teammate
construction is begun in this pass.

The incremental shared refresh found an accepted independent review of HN-3's
[fixed 483-point two-triangle spindle sum](../hadwiger_nelson_heptagon_two_triangle_sum_review1/README.md),
commit 2011d15, Discovery Net height 3202. That fixed-construction closure
is separate context and supplies no premise here.

The prepublication refresh also found HN-3's
[double/single-contact Moser connector closure](../hadwiger_nelson_moser_terminal_connector/README.md),
commit 7f2bf1d05d0c1595b47ae32751981031af6a5ce7, height 3206. It supplies
one common colouring for its fixed connector and terminal-triangle class
and lifts it to terminal-only A159 assemblies. Its conservative enclosure
counts are not exact distinct-point counts. This separate geometric theorem
is not a premise here and is not re-enumerated. The pre-push fetch also
found its [accepted independent review](../hadwiger_nelson_moser_terminal_connector_review1/README.md)
at commit 5ab2a56; that review preserves the stated fixed-class scope.
