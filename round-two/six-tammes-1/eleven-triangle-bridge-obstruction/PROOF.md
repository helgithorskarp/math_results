# Full G20 needs at least four bridging triangles in a triangle tree

Actual author **six-tammes-1**, role **researcher**, pass23.
Ordinary geometric coverage plus exact polynomial certificates; separate
programs by the same author. Independent researcher review and
formalization of this new result are pending.

Let X be a finite set of distinct unit vectors in R^3, every distinct pair
having inner product at most c, with

\[
                        c\in I=[14/25,593/1000].          \tag{1}
\]

Its complete contact drawing includes EVERY pair with product c, drawn by
the minor geodesic arc. An actual triangular face is a complementary
component whose closure is the smaller hemispheric triangular disk with
three distinct stated corners. Triangle adjacency always includes every
shared contact edge between the selected actual faces; no adjacency may
be omitted to make a cyclic graph a tree.

Prescribe twelve **distinct** point labels and the eighteen edge contacts
of these eight triangles:

\[
\begin{split}
\mathcal A&=\{(0,5,11),(0,6,11),(0,5,7),(5,9,11)\},\\
\mathcal B&=\{(1,2,4),(2,4,8),(1,2,10),(1,10,12)\}.
\end{split}                                               \tag{2}
\]

Also prescribe **7-12 and 9-10** as contacts. This is exactly the full
twenty-contact interface of the credited
[twelve-point frame9774](../../six-tammes-2/twelve-core-frame/PROOF.md).
Other contacts are allowed. The eight contact triples are actual faces
by the ordinary empty-triangle argument below.

**Theorem.** Suppose an induced connected tree of actual triangular faces
contains all eight faces in(2). After contracting the A and B four-face
subtrees, the unique path between them contains at least **four other
triangles**; equivalently, its contracted edge length is at least5.
Consequently every such selected tree, and every triangle-tree component
containing both clusters, has at least **twelve faces**.

This strengthens [LEMMA9849](../ten-triangle-bridge-obstruction/PROOF.md)'s
at-least-eleven-face component bound on the same closed interval and full
contact interface. The144 two-bridge placements and their root exclusions
are prior work credited to9849; they are reproduced here for an explicit
subtree coverage argument. The new432 three-bridge placements exclude the
remaining eleven-face route.

**Fifteen-point corollary.** Retain ALL the physical hypotheses of
[LEMMA9813 CorollaryC](../connected-map-filters/PROOF.md), restricting c
to I: fifteen distinct unit points; complete contact graph connected and
minimum degree at least3; every actual face closure a simple disk with3..5
distinct boundary points; every nontriangle closure geodesically convex
and in its own open hemisphere; and counts T11/Q3/P3. The full G20's A and
B clusters must belong to **different** triangle components. If e counts
edges shared by two nontriangular faces, then3<=e<=6, and the only remaining
necessary component-size profiles from9813's screen are

|e|necessary full-G20 profiles|
|:---|:---|
|6|4+7;5+6|
|5|1+4+6;1+5+5;2+4+5;3+4+4|
|4|1+1+4+5;1+2+4+4|
|3|1+1+1+4+4|

These nine profiles are necessary, with no realizability or sufficient
occurrence assertion. The weaker eighteen-contact motif retains9813's
original eleven-profile screen. Neither extra cross contact, motif
occurrence nor coverage of every global optimizer is established here.
There is no new global separation bound or Tammes-15 optimality claim.

## 1. Actual faces, basis and reflection

Contact arcs embed. At a transverse crossing choose a nearer endpoint
on each edge. The two distances to the crossing sum to at most acos(c),
and the strict triangle inequality contradicts separation. Collinear
overlap and a vertex inside an edge also violate separation.

For a contact triple x_i, its Gram matrix is H=(1-c)Id+cJ_3, positive
definite since0<c<1. All three corners have positive product1+2c with
their sum, so their smaller spherical triangle is hemispheric. If
q=sum lambda_i x_i with lambda_i>=0 and sum lambda_i=1, then
||q||^2>=(1+2c)/3>c^2. A different packing point z=q/||q|| in this triangle
would satisfy z.x_i<=c and thus ||q||=z.q<=c, a contradiction. Embedding
prevents other edges from entering the empty triangular disk. It is an
actual face. This establishes that the contact triples in(2) are actual
faces without a contact-graph enumeration or irreducibility premise.

For adjacent contact triangles(x,y,z),(x,y,w), the two unit solutions to
w.x=w.y=c are reflected across span{x,y}. Their affine midpoint is
q=c(x+y)/(1+c), with ||q||^2=2c^2/(1+c)<1. Distinct point labels therefore
give the unique other solution

\[
             w=r(x+y)-z,\qquad r=2c/(1+c).                \tag{3}
\]

This classical reflection is proved here for applicability and credited
to the existing frame/contact work; no identity priority is claimed.
Fix either contact triple(p0,p5,p11) or(p1,p2,p4) as coefficient basis.
Its Gram matrix H is invertible; walking an actual triangle tree by(3)
covers every physical branch, because the neighboring third point is
distinct from the previous one. The coefficient vectors are integer
polynomials in r. On I,

\[
 J=[28/39,1186/1593],\quad c=r/(2-r),\quad 0<r<1,\quad2-r>0.\tag{4}
\]

For coefficient vectors v,w define

\[
 N(v,w)=(2-2r)\sum_i v_iw_i+r(\sum_i v_i)(\sum_i w_i).
\]

Then the actual product equals N(v,w)/(2-r). Norm and contact identities
can be checked exactly, with no square-root or orientation sign choice.

## 2. The six-point clusters have exactly their prescribed internal contacts

Build A from its central triple by three reflections, and B from its
first triple by the reflection steps8<-2,4;10<-1,2;12<-1,10. The omitted
third corner at each step is the third corner of the previous triangle.
Direct polynomial contraction gives these noncontact-gap numerators,
where the gap is product minus c and its denominator2-r is positive:

|numerator|A pairs|B pairs|
|:---|:---|:---|
|2(r-1)(r+1)|0-9;5-6;7-11|1-8;2-12;4-10|
|2r(r-1)(r+2)|6-7;6-9;7-9|4-12;8-10|
|2r(r-1)(r+1)(r+2)|none|8-12|

All three expressions are strictly negative for0<r<1. Both programs
independently reconstruct and check every pair's polynomial, all eighteen
internal contact identities, and exact rational Bernstein negativity on J.
The complete12-entry table is also in [CERTIFICATE.json](CERTIFICATE.json).
Thus each cluster has exactly its nine prescribed internal contact edges.
Enumerating triples in each of these six-vertex graphs yields precisely
the four triangles in(2). An additional actual triangle supported only
within A or only within B would duplicate an already selected face.
This is a local contact property; it imposes no incumbent coordinates.

Each four-face patch is a triangulated disk: attach the other faces along
root/tree edges with fresh corners. Its six boundary edges form

\[
                    0-6-11-9-5-7-0,\qquad1-4-8-2-10-12-1.\tag{5}
\]

The separate checker verifies the incidences, fresh-corner attachment and
both literal cycles. The embedding and disjoint interiors of actual faces
realize this abstract disk. A face outside a patch cannot attach along an
internal edge, which already has two incident faces. Disk structure is
not inferred from vertex/edge counts alone.

## 3. Complete short-path reduction, including selected subtrees

A tree of f triangular faces uses at most f+2 distinct point vertices:
start with three at the root and add at most one for each child sharing
its parent edge. The tree closure may have vertex pinches; these reduce
support and do not invalidate the bound.

Take the minimal subtree containing both entire A and B four-face patches.
Contract each patch. Tree contraction introduces no loops or parallel
edges. The contracted minimal tree is a path between A and B; a branch
could be deleted without losing either patch. Their corner supports

\[
A_0=\{0,5,6,7,9,11\},\qquad B_0=\{1,2,4,8,10,12\}
\]

are disjoint, so A and B cannot share an edge. A triangle cannot share
an edge with each patch: that requires two A and two B corners in three
slots. Therefore at least two other triangles occur on the path.

Suppose at most three occur. The selected minimal tree has ten or eleven
faces. It remains an **induced** tree inside the original selected tree:
an extra edge between its vertices would already be a cycle. All its
faces are actual faces of the complete original contact drawing. Outside
triangles and points need not be removed, and maximality as a component
is not assumed. This explicit argument supplies the subtree application
needed beyond9849's published component statement.

For two bridging triangles U,V the support bound is12, already exhausted
by the two patches. They form A-U-V-B. If their A/B attachment edges are
{a,a'} and{b,b'}, their common edge has one corner from each cluster, so

\[
                     U=(a,a',b),\quad V=(a,b,b').          \tag{6}
\]

Six boundary edges and two endpoint choices in each patch give144 cases.
These are exactly the earlier9849 cases, reproduced in the present
certificate under type S. The derivation and polynomial test use only
these selected actual faces, so other triangles in the complete drawing
cannot supply an omitted case.

For three bridging triangles the path is A-U-V-W-B. Its eleven selected
faces use at most13 point vertices, with at most one corner X outside
A_0 union B_0. A triangle outside A cannot use only A corners by Section2,
so U is an A boundary edge plus a B or X corner. Similarly W is a B
boundary edge plus an A or X corner.

Since U and W are not adjacent in the induced tree, they share at most
one corner. V shares an edge with each, so their two edges inside V have
a common corner. Hence U intersection W={z}, and

\[
                       V=(z,u,w),\quad u\in U\setminus\{z\},
                                      \quad w\in W\setminus\{z\}.\tag{7}
\]

V cannot have two A corners. Their required contact is either a strict
noncontact by Section2, or an edge of an A face, making V adjacent to A
and creating a shortcut/cycle in A-U-V-W-B. An internal A edge already
occupied by two A faces cannot acquire V as a third face either. The same
argument excludes two B corners in V. With only A/B corners available,
every three-corner V would have such a pair. Therefore X must exist and
V=(a,b,X), with a an A corner and b a B corner.

There are exactly three possibilities, with a,a' the endpoints of the
chosen A boundary edge and b,b' of the chosen B boundary edge:

|type|U|V|W|faces containing X|
|:---|:---|:---|:---|:---|
|UV|(a,a',X)|(a,b,X)|(a,b,b')|U,V|
|VW|(a,a',b)|(a,b,X)|(b,b',X)|V,W|
|UVW|(a,a',X)|(a,b,X)|(b,b',X)|U,V,W|

To see completeness, if U's third corner is in B then V must share its
A/B edge, forcing that B corner to be b; W must contain X. If W's third
corner is in A the symmetric argument forces it to be a and U to contain
X. If neither occurs, both contain X. U and W cannot simultaneously use
those A/B third corners, since their intersection would have two corners
or V would have no fresh corner. Thus the table covers all possibilities.

Each type has6*6*2*2=144 literal edge/endpoint cases, giving432 new cases.
No symmetry quotient is used. The support is exactly13 for each listed
formal patch. There are **23** distinct patch-contact edges, not24:
eleven triangular incidences give33 sides, and the tree's ten shared edges
give33-10=23 distinct edges. These statements are verified by both
constructions, including every corner and every edge.

The independent combinatorial check uses a different route: take each of
the six A/B boundary edges, all seven possible third corners for U and W,
and all choices in(7). It checks ALL3,024 initial possibilities. Within-core
contact constraints, distinct faces, and the complete induced adjacency
path leave exactly432 unique cases. It compares that entire set with the
typed table, not just the count. The fresh code label13 represents X with
the contacts supplied by this bridge only.

## 4. Exact paired-gap certificates for all576 cases

For every short or long placement, the A-anchored producer constructs the
known A patch, walks(6) or the long table by reflection, then builds the B
patch. The B-anchored checker reverses the path and completes A. In the
short case they verify all12 norms and21 patch contacts; in the long case
all13 norms and23 contacts. Every actual physical configuration in the
covered case satisfies the two additional G20 equations

\[
              F(r)=N(p7,p12)-r=0,\qquad G(r)=N(p9,p10)-r=0.\tag{8}
\]

For each of576 placements the programs produce and explicitly verify
rational-polynomial Bézout witnesses

\[
                            uF+vG=h\ne0.                 \tag{9}
\]

There are38 distinct monic h polynomials. Their complete case bindings and
all Bernstein coefficients on J are in [CERTIFICATE.json](CERTIFICATE.json),
24,039bytes. The witnesses are reconstructed and verified from the gap
polynomials; large per-case witness lists are unnecessary. Every h has
one strict sign among all its Bernstein coefficients. The Bernstein
basis is nonnegative and sums to1 on the entire closed interval, including
both endpoints. Thus h has no root on J; by(9), F and G have no common root.
All576 cases are excluded. The maximal gap degree is10 and witness degree8.

This is a Bézout/common-root argument, not merely a common-divisor test:
the constant1 divides every pair of polynomials but need not satisfy(9).
Both-zero gaps abort rather than becoming a fictitious gcd1. A single
zero gap is handled by the root-free other gap. No approximate root
location, sampled parameter or floating sign is used.

The complete per-case h-degree histogram is

|degree|1|2|3|4|5|6|7|8|
|:---|---:|---:|---:|---:|---:|---:|---:|---:|
|cases|111|117|119|128|37|37|17|10|

The algebraic test includes unphysical formal placements; their inclusion
is safe for a necessary-condition exclusion. The actual-face, branch,
label and minimal-path reduction proves that no physical case is omitted.
Therefore a connecting path needs at least four triangles, proving the
theorem. In9813's full physical cohort, the entire triangle adjacency is
a forest with11 nodes, so a connecting tree with at least12 faces is
impossible. The two clusters are separate; removing11 and1+10 from the
original necessary screen gives exactly the corollary's nine profiles.

## 5. Execution, reproducibility and remaining scope

[check.py](check.py) uses dense rational polynomials, direct typed path
generation and the A anchor. [audit.py](audit.py) uses sparse polynomial
dictionaries, exhaustive long-path generation and the B anchor. Bernstein
arithmetic is affine power conversion in the producer and multiplication/
degree elevation in the checker. The checker imports no producer arithmetic;
its main imports the producer construction solely for full-field comparison.

Both normal and optimized executions cover ALL576 ordinals. The auditor
runs the four disjoint ranges[0,144),[144,288),[288,432),[432,576) serially,
with the complete metadata, input scope, core constraints and enumeration
checked in every range. A partial entrypoint reports only its requested
range; the validation requires the exact contiguous cover before reporting
complete theorem execution. All93,744 Gram polynomials and1,152 cross-gap
polynomials are compared, alongside7,344 norms and12,960 contacts per
construction and576 explicit Bézout identities.

[VALIDATION.json](VALIDATION.json) records all twelve actual entrypoint
executions, full normal/O output equality and whole fresh/included
certificate byte equality. [controls.py](controls.py) rejects damaged
scope, branches, corner/edge labels, enumeration coverage, polynomial and
core certificates, ordinal ranges, common-root traps and altered full
comparison fields. Valid orderings and consistent index permutations pass.
Controls deliberately use small arithmetic ranges; the complete theorem
coverage is supplied by all four auditor ranges, not by control counts.

The ordinary spherical, disk, tree-contraction, support and branch bridges
are unformalized. Two algorithms by the same author are not independent
researcher review. The public computation needs only Python3.12's standard
library and the compact certificate. Private exploratory outputs stay in
scratch and are not runtime or publication inputs.

The independently reviewed [flexible G20 frame](../../six-reviewer-5/twelve-core-frame-audit/REVIEW.md)
has a positive family. This theorem applies when the selected triangle
adjacency is a tree and bounds its connecting path; no exclusion of that
whole frame family is inferred. Peer [9828](../../six-tammes-2/twelve-core-completion/PROOF.md)
fixes twelve incumbent positions to classify arbitrary additions and
prove local stability. Its stronger positions are not assumed here.
The freshly read [9866](../../six-tammes-2/twelve-core-local-gate/PROOF.md)
sharpens fixed-core stability to1400delta for delta<=10^-8 and excludes
strict improvement in the moving-frame tube
24|c-tau|+3|z-z0|<=10^-10 with c<=tau. Its arbitrary-three result and
ordinary proof are independently unreviewed. This is complementary
context, not a premise of the tree theorem or a whole-frame capacity result.
The separated-cluster profiles, cross-contact forcing, motif occurrence,
arbitrary three-addition capacity over ALL frame parameters, the critical
strip and global optimizer-cohort coverage remain open.
