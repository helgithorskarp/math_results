# Dense506: every three-point repair using a completion point is four-colourable

**Theorem (exact computer-assisted).** For either pinned 506-point host H,
let C=C3(H) be all nonhost plane points with at least three unit neighbours
in H, and let c be the fixed host four-colouring. For every p in C and
every two Euclidean-plane points x,y, the strict unit-distance graph on
H union {p,x,y} has a proper four-colouring extending c.

These graphs have at most 509 vertices. Every subgraph is also
four-colourable, so in particular no one-deletion/three-point repair of
order 508 can be a counterexample if at least one added point lies in C.
The case of three new points outside H union C remains open. Other host
placements and larger addition patterns are not addressed.

## Fixed geometry and imported census

The exact hosts use the pinned Parts coordinate tables A (159 points) and
V (214 points), with

\[
 \alpha=i\sqrt3,\ z=\sqrt{33},\ \beta=\alpha z/3,
 \ r=\sqrt{-408+72z}>0,
\]
\[
 t=(5+z+5\alpha-\beta)/12,\quad B=A\cup(\overline A+t),
\]
\[
 u_\pm=[-18-6z-30\alpha+6\alpha z
            \pm r(3+6\alpha+\alpha z)]/72,
 \qquad H_\pm=B\cup u_\pm(V-V[10]),
\]

where V[10]=alpha/6. The hosts, exact labels, C of order 1,420, and fixed
colour row are specified in the
[one-outside-point theorem](../hadwiger_nelson_dense506_one_low_repair/PROOF.md),
source `df08b40b24446f5b89c65417b1be179fcae22d60`.
Its [accepted independent review](../hadwiger_nelson_dense506_one_low_repair_review1/README.md)
was published at `09f73be32548fa94f70d7c7510b3b407f81386b3` during this pass.

Write U=H union C. The prior theorem already proves extension of c after
one arbitrary point and at most two points of C are added. It therefore
handles the present cases with at most one of x,y outside U, including
coincident points and points already in H. Assume from now on that x,y
are distinct and both outside U.

For a nonhost point v define its available list

\[
 L(v)=\{0,1,2,3\}\setminus\{c(h):h\in H,\ |h-v|=1\}.
\]

The earlier complete C3 census ensures that points outside U have at most
two host neighbours, so |L(x)|,|L(y)| are at least two. Candidate lists
L(p) are nonempty.

The prior eligible-circle census also supplies the following exact finite
set X of order **1,085**. It consists of all points v outside U that have
two differently coloured host neighbours and at least one unit neighbour
q in C for which L(q) is contained in the complementary two-colour list
M(v)=L(v). For each v it records those two host labels and the complete
list E(v) of such eligible C neighbours.

This definition is complete in the Euclidean plane. Three specified unit
neighbours, two in H and one in C, are noncollinear and determine the
centre uniquely. The earlier 52,550,758 eligible-triple census enumerates
all such centres. That census and its review are imported here; they are
not rerun in this pass. The saved table is bound by canonical SHA-256
identities, including

```
X coordinates  28b46f5eae9a537d8a189d03284e32d9012fbccde35f05bd72e19ee1f1699f43
host pairs     df22d5b218106b24ee0651fd6b7c8e79038765a75a90a923de507efa8299c8f0
eligible lists 3e622b2e34c439bce776300c06890141458f568927e5e476c6dd19d865a13d39
```

All v in X have coordinates in K=Q(z,r,alpha). The canonical coordinate
row (d,X1,Xz,Xr,Xzr,Y1,Yz,Yr,Yzr) represents

\[
 [X_1+X_z z+X_r r+X_{zr}zr+
   \alpha(Y_1+Y_z z+Y_r r+Y_{zr}zr)]/d,
\]

with positive d and coprime integer entries. X labels are lexicographic
row order. Candidate labels are inherited C labels 0 through 1419. For the
minus host use r->-r with unchanged labels, as established by the census.

## Complete list reduction for two outside points

Consider any three-vertex graph with lists A,B of size at least two on
x,y, and a nonempty list D on p. It fails list colouring **if and only if**
it is a triangle and

\[
 A=B=M,\qquad |M|=2,\qquad D\subseteq M.
\]

To see this, a nontriangle is a forest. Root the component containing p
at p and colour away from that root; every other vertex has at least two
choices and at most one coloured parent. Any separate component has the
same property. For a triangle, proper colouring is the choice of three
distinct representatives. All individual lists are nonempty and every
pair union has size at least two. The three-set matching condition can
therefore fail only if the total union has size two, which gives exactly
the displayed condition. Direct brute force of all 14,520 list/edge cases
confirms this criterion, with 18 failures.

Apply it to L(x),L(y),L(p). A failure would force both x and y to have
two differently coloured host neighbours, the same two-colour list M,
and adjacency to p. Thus x,y both belong to X and satisfy

\[
 M(x)=M(y),\qquad p\in E(x)\cap E(y).
\]

They would also have to be unit-distant from each other. It suffices to
check precisely the pairs satisfying these two finite conditions. This
reduction imposes no coordinate or field assumption on the original
arbitrary x,y; field membership follows from their required incidences.

## A 499-byte distance certificate excludes every pair

Of all binomial(1085,2)=588,070 pairs of X points, 98,545 have the same
available colour pair. Exactly **607** also have a common eligible C
neighbour. They account for **629** triples (x,y,p), because a pair can
have more than one eligible common neighbour.

Every one of these 607 pairs is checked by exact field arithmetic. Their
squared distances take **30 distinct values**, listed with multiplicities
in the [499-byte certificate](squared_distances.tsv). A row

```
d a b c e multiplicity
```

represents (a+b*z+c*r+e*z*r)/d. Rows are in canonical form with d positive
and gcd(d,a,b,c,e)=1. The multiplicities sum to 607. **No row represents 1.**

Here 1,z,r,z*r are linearly independent over Q. Indeed r^2=-408+72z is
positive at the chosen real embedding and negative at z->-sqrt33, so it
cannot be a square in Q(sqrt33). Hence Q(z,r) has degree four. It follows
that a canonical row represents 1 exactly when it is (1,1,0,0,0), which
is absent from the certificate. No numerical approximation is involved.

For explicit colouring of each of the 629 realized triples, give p its
least permitted colour a. The shared two-colour list M has another colour
b; give both x and y colour b. Their distance is not one, so this is proper
on all new edges and preserves all host constraints. Combine with c on H.
This completes the proof.

The primary verifier enumerates all point pairs, filters by the exact
palette/eligible-list conditions, computes the squared distance in the
real four-coordinate field representation, and checks the complete
30-row histogram against the certificate. The selected-pair list has
SHA-256
`c1a76ac1ace23836d6415ff9da7bc52f54e5a06e409b45915bbba3d003e7f90d`.
The complete pair-plus-squared-distance stream has SHA-256
`3b5d6f439e8d0c66ebf118d46718ca2a2a2a86ff2d3f8fa0affdf508f4a85e61`.
Both use compact JSON without a trailing newline.

The explicit colouring stream consists of JSON rows [i,j,p,b,b,a], one
newline per row, ordered by i,j,p. Its SHA-256 is
`58492d82f38e6188fd6338ad747cadbbee41ea7500afc478dab34abf1f22d154`.
The rows are regenerated by both implementations rather than published
as an exhaustive dump.

## Independent organization and arithmetic audit

The [audit](audit.py) does not enumerate all 588,070 pairs. It groups the
outside points by each eligible C neighbour and each available colour
pair, then enumerates pairs within groups. There are 1,496 nonempty groups
of orders

```
1:1096  2:314  3:75  4:5  5:6.
```

They produce 629 triples and the identical 607 distinct pairs, matched
entry by entry. Available lists are rebuilt as sets from the pinned host
colour row and candidate host-neighbour lists.

For distance checks, the audit imports the published independent
reviewer's [generic eight-coordinate quotient-ring multiplication](../hadwiger_nelson_dense506_two_point_extension_review1/independent_check.py),
not the primary four-coordinate norm routine. It computes all 607 norms
directly, with no modular or floating-point filter, and compares every
normalized norm to the primary stream. It also checks the minus embedding
by changing the signs of r coefficients in every point. Its 30-class
histogram is the coefficientwise r->-r image of the same certificate;
again no pair is at unit distance. The same labelled pair/colour
certificate therefore works for both hosts.

## Remaining geometry and trust boundary

The new theorem imports the complete 1,085-centre census, its eligible
incidences, the fixed host colouring and the earlier extension cases.
These dependencies were independently reviewed, but their large triple
censuses are not repeated here. Source and compact input identities are
pinned; public commands regenerate the tables when needed. The new audit
is an author-run check using independently derived arithmetic, not an
external review of this new theorem. External review remains pending.

All new distance decisions use exact Python integers and Fractions. No
SAT call, numerical equality or new exhaustive host-triple scan is used.
The residual trust boundary is the imported exact results, coordinate data,
SHA-256 identity, CPython arithmetic semantics, and ordinary unformalized
geometry/code reasoning.

Any possible non-four-colourable one-deletion/three-point repair must now
have all three new vertices outside U. In a vertex-minimal obstruction all
three are present by the earlier arbitrary-two-point theorem. Each has
at most two host neighbours and at most two added neighbours, while the
minimum degree is at least four. Thus each has exactly two retained host
neighbours and the three additions form a unit equilateral triangle.
Failure to extend the fixed host colouring further requires all three
available lists to be the same two-colour set. These are necessary
conditions only. That three-outside-point triangle family has not been
enumerated or excluded here, and need not lie in the present X table.
