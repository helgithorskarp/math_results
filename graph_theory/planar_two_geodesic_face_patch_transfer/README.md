# A three-pair certificate survives face-patch substitution

The [icosahedral price-region certificate](../planar_two_geodesic_icosahedron_price_region/README.md)
extends from a 32-vertex graph to planar edge-length metrics of
**unbounded order**.
Replace each marked face vertex by any connected patch whose neighbors
outside the patch are corners of that face. If the patches preserve the
core metric and their boundary-clique torsos have treewidth at most
three, every nonnegative vertex mass has a half-balanced separator made
of at most two shortest paths in the **whole original graph**.

The transfer has two parts. A general three-pair condition gives a
quantitative separator bound even for patches of arbitrary complexity.
The previously proved and reviewed heavy-torso reduction supplies half
balance when one patch holds more than half the mass. This excludes
larger facial attachments as a counterexample strategy under the stated
hypotheses; it does not resolve
[Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).

## General three-pair condition

Let a finite quotient graph Q consist of core vertices U and an
independent set Z of patch atoms. Consider three candidate vertex sets
S_1,S_2,S_3 in U, each the union of at most two paths. Suppose sets
H_1,H_2 of quotient vertices have these properties:

1. For i=1,2, each component of Q-S_i is either a singleton in Z or
   contained in H_i.
2. Each component of Q-S_3 is either a singleton in Z or disjoint from
   at least one of H_1,H_2.

Expand each atom z into a finite patch K_z. Every edge between a patch
and the core must project to an edge of Q, and there are no edges between
different patches. Empty patches and missing boundary incidences are
allowed. Retain all core vertices and edges. Assume the displayed paths
are shortest paths in the expanded graph G. For any nonnegative vertex
mass w, write

    M = w(V(G)),       B = max_z w(K_z),       tau = max(M/2,B),

where B=0 if there are no patches. **At least one of S_1,S_2,S_3 leaves
every component of G-S_i with mass at most tau.** No planarity or
treewidth assumption is needed for this quantitative assertion.

To prove it, assign atom z the total mass of K_z, retaining the mass of
each core vertex. This gives a quotient mass mu with total M. Every
component of G-S_i projects into a component of Q-S_i. Consequently an
expanded component whose projection is a singleton atom has mass at
most B, and a component projecting into H_i has mass at most mu(H_i).

If S_1 and S_2 both fail the bound tau, then mu(H_1)>tau and
mu(H_2)>tau. Any component left by S_3 that projects disjointly from H_i
has mass at most M-mu(H_i)<M-tau<=tau. Components projecting to singleton
atoms have mass at most B<=tau. Thus S_3 succeeds. This also handles
M=0 and equality at all thresholds. Connectivity of individual patches
is unnecessary for this part.

This is a sufficient certificate condition, not a characterization of
all weighted two-path separators. The three candidate pairs are
alternatives: the separator never uses their combined six paths.

The team's [mass-menu duality](../planar_two_geodesic_mass_menu_duality/README.md)
gives a general exact test for all-mass success of any fixed deletion
menu, and the [four-menu gap](../planar_two_geodesic_four_menu_gap/README.md)
identifies the special role of disjoint residual components for at most
three sets. Here the three core pairs have a bound involving B; a heavy
patch can make all three fail half balance. Substitution and the local
repair below are the additional ingredients.

## The icosahedral quotient and metric region

Use the 12-vertex icosahedral core I and the thirty center prices c_e in
the predecessor's [exact certificate](../planar_two_geodesic_icosahedron_price_region/certificate.json).
Its SHA-256 is

```
070ac17d45f77ad18edb0ac1b9fae642982fc36db7dbd82ed5a1c3c325f1d11d
```

For any lambda>0, independently choose the thirty core edge lengths in
the closed box

    (144/151) lambda c_e <= L_e <= (158/151) lambda c_e.        (1)

Number the twenty triangular core faces lexicographically, starting
at zero. In the quotient Q, atom 12+f neighbors all three corners of
face f. The three pairs, using only core vertices, are

```
S_1: (1,6,11,7,3)        and (2,0,4,8)
S_2: (1,6,11)           and (5,9,10)
S_3: (0,4,8,9,11,6)     and (1,5).
```

All six paths are shortest in I throughout (1). The cited certificate
gives one twelve-entry integer potential per path. For a path P, price
its edges at 158 c_e and the other edges at 144 c_e. The potential starts
at zero, ends at that path's length, and changes by at most the edge
price across every core edge. These 180 inequalities certify shortestness
at the adverse corner. Common edges cancel when comparing P with any
competing simple path, so that corner maximizes the length difference
over the whole box. Scaling by lambda/151 proves the claim for (1).

The quotient component sets are

```
H_1 = {5,9,10,13,16,18,19,24,25,26,28,30,31}
H_2 = {0,2,3,4,7,8,12,13,14,15,16,17,20,21,22,23,24,25,27,29,30}
J_1 = {2,3,7,12,14,15,17,20,21,22,23,27,29}
J_2 = {10,18,19,26,28,31}.
```

Deleting S_1 leaves H_1 and ten singleton atoms; deleting S_2 leaves
H_2 and five singleton atoms. Deleting S_3 leaves J_1,J_2 and five
singleton atoms. Since J_1 is disjoint from H_1 and J_2 is disjoint
from H_2, this quotient satisfies the general three-pair condition.
The new checker reconstructs all three partitions and rechecks the
180 potential inequalities; these are exact finite certificate checks,
not mass samples.

## Face-patch theorem

For each triangular face f=abc of I, insert a finite connected graph
K_f with a planar drawing inside the face, with all its outside neighbors
among a,b,c. Every nonempty patch meets at least one boundary corner.
The interiors of different patches are disjoint and have no edges
between them. A face may also be left empty. All edges have positive
lengths. Retain the core edges and their lengths from (1).

Let T_f=G[K_f union {a,b,c}] be the local torso, including the existing
boundary triangle. Require

    d_(T_f)(u,v) >= d_I(u,v)   for u,v in {a,b,c}.             (2)

Condition (2) is equivalent to I being isometric in G. Necessity holds
because every torso path is a G-path. For sufficiency, cut a core-to-core
G-path into excursions through individual patches. Replace each such
excursion by a core geodesic between its boundary endpoints. Condition
(2) ensures the replacement does not increase length. The resulting
core walk proves that G cannot shorten a core distance. Thus the six
displayed paths remain ambient geodesics. Equality and shortest-path
ties are allowed.

For arbitrary nonnegative vertex masses, the general condition now gives
one of the three core pairs with residual component mass at most

    max(M/2, max_f w(K_f)).                                  (3)

This statement allows arbitrary patch treewidth. Its proof uses the
full combinatorial graph: long edges are retained when computing
components. Empty patches and patches meeting only some corners merely
make their projected components smaller than quotient components.

**Half-balance corollary.** If every nonempty T_f has treewidth at most
three, G has a half-balanced separator of at most two ambient geodesics
for every nonnegative vertex mass.

If every patch has mass at most M/2, (3) proves this. Otherwise some
K_f has mass greater than M/2. Apply the existing
[heavy-torso reduction](../planar_two_geodesic_prescribed_attachment/README.md),
whose [independent review](../planar_two_geodesic_prescribed_attachment_review1/REVIEW.md)
checks this precise centroid argument. For completeness, take a width
three tree decomposition of T_f. Its boundary clique {a,b,c} lies in
a bag. Join that bag to one new bag containing all of V(G) outside K_f.
This gives a decomposition of G: every outside edge is in the new bag,
and intersections with the torso consist only of boundary vertices.

Assign the mass of each vertex of K_f to a local bag containing it, and
all other mass to the new bag. A weighted centroid of this decomposition
tree has every branch mass at most M/2. It cannot be the new bag because
the branch containing K_f has mass greater than M/2. Its local bag has
at most four vertices. The tree-decomposition separator property makes
every component left by deleting that bag have mass at most M/2.
Pair its vertices arbitrarily and take shortest paths in **G** between
the pairs; if necessary use a singleton for an unpaired vertex. At most
two such paths cover the bag. Deleting these paths can only split or
shrink the remaining components, so it preserves half balance.

The repairing paths need not stay inside T_f. The exact controls include
many examples in which they leave it. No completion of a prescribed
first path is asserted. The heavy-torso lemma and weighted centroid
principle are prior ingredients; the contribution here is the
three-pair transfer and its application to this metric region.

## An explicit family of unbounded order

Choose an arbitrary nonnegative depth d_f for each of the twenty faces.
Starting from its boundary triangle, insert one vertex in every current
interior triangle at each of d_f rounds, joining it to that triangle's
three corners. The resulting patch has

    r_f = (3^(d_f)-1)/2

interior vertices. Different faces may have different depths, including
zero. Each nonempty patch is connected, and its torso has an explicit
width three decomposition: one bag consisting of each new vertex and
its three insertion corners, joined to the bag that created its parent
triangle. The root bag contains the original boundary triangle.

The full graph is a simple planar triangulation with

    N = 12 + sum_f r_f,      E = 3N-6,      F = 2N-4.

For example, putting depth four in all faces gives N=812. No upper
bound on the depths is used in the proof. To give a simple admissible
metric, let D be the diameter of the priced core and give every new edge
incident with a core vertex a length A>D. All other new edges may have
arbitrary positive lengths. Every excursion through a patch between
distinct core corners pays at least 2A>D, so (2) holds. Assigning A to
every new edge is another admissible choice. The theorem also permits
all positive patch metrics satisfying (2), beyond these prescriptions.

The family has unbounded order, **not unbounded treewidth**. For example,
one bag containing the twelve core vertices joined to all local
decompositions gives width at most eleven. Its icosahedral subgraph has
minimum degree five, so the global treewidth is at least five. This
distinguishes the conclusion from the general treewidth-three theorem;
no hereditary strong path-separability claim is made.

There is also a direct boundary relative to the team's
[connected-deletion guard](../planar_two_geodesic_cycle_rank_representatives/README.md).
Suppose all twenty patches are nonempty and each meets all three face
corners, as in the positive-depth stacked family. For any S with |S|<=4,
let k be the number of removed core vertices. The residual core stays
connected. At most 4-k patches contain a removed interior vertex, and
at most binomial(k,3) faces lose all three corners. Thus at least

    20 - (4-k) - binomial(k,3) >= 16

intact patches meet the residual core. Take a spanning tree of that core.
For each connected piece of a residual patch that meets it, take a
spanning tree of the piece and attach it by just one edge to the core.
This gives a spanning tree of the residual component containing the
core. Each of the sixteen intact patches contributes a leaf outside the
core. Two internal simple paths can cover at most four leaves of a
tree. This connected edge-deletion representative therefore fails the
guard's required internal two-path cover, for every S of size at most
four. This compares against that sufficient criterion only.

## Reproduction and trust boundary

From the repository root, using Python 3.11+ and only its standard library:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_face_patch_transfer/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_face_patch_transfer/audit.py
```

The public dependency is the predecessor's 1,112-byte certificate linked
above; there are no private inputs or external solvers. The main checker
validates the quotient condition and all 180 potential inequalities,
then builds sixteen graphs at the center and one adverse box corner.
It checks oriented spherical triangulations, explicit torso tree
decompositions, core isometry, projected components, and ambient
shortestness. The 928 exact integer-mass controls include every nonempty
patch carrying all the mass and exactly half the mass, all three core
alternatives, zero mass, and deterministic samples. In 328 cases all
three core pairs fail and the heavy-patch repair succeeds; 137 selected
repairs leave the heavy patch's torso. A deliberately shortening patch
violates (2) and is detected.

The separate audit imports neither `model.py` nor `verify.py`. It builds
the core from explicit adjacency and orients its faces by dual traversal;
it builds patches by breadth-first insertion, in contrast to the main
recursive constructor. SHA-256 comparisons cover the complete weighted
edge, oriented-face, patch, bag and parent streams of all sixteen models,
including N=812. On the twelve models with N<=150 it uses Floyd--Warshall
and directly tests local bags as whole-graph separators, rather than
running the production centroid routine. It checks 532 mass profiles,
including 219 heavy-patch repairs; 94 selected repairs leave their
torso. Its guard control checks 794 core deletions for each of two
32-vertex metrics. Compact outputs and complete-stream hashes are in
[expected.json](expected.json). The seeds are 2026092920 (plus fixture
index) and 2026092921.

These finite controls are not exhaustive over graph size, real masses,
or metrics. The universal claims follow from the written transfer,
excursion-replacement and existing heavy-torso arguments, with the exact
finite quotient and potential certificate. The separate audit was
written by the same researcher; independent peer review of this transfer
is pending. Historical priority is not claimed.

Primary literature refreshed 29 September 2026:
[Diot and Gavoille, *Path Separability of Graphs*](https://emilie-diot.eu/Article/DG10a),
Lemma 1 and Proposition 1.1, give the weighted decomposition-centroid
background and the general treewidth-three implication. The earlier
team result and its review provide the localization to a heavy torso.
Targeted primary-source searching did not establish priority for the
three-pair substitution statement. A listed workshop disproof talk was
not identified with an exact applicable theorem or witness; no general
open-status claim is inferred from the problem list.
