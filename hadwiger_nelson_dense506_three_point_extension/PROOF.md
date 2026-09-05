# Arbitrary three-point extension for the two dense506 hosts

**Theorem (exact computer-assisted).** Let H be either of the two pinned
506-vertex dense hosts defined below, and let c be its published proper
four-colouring. For every set S of at most three arbitrary points of the
Euclidean plane, c extends to a proper four-colouring of UD(H union S).
Consequently every subgraph of such a union is four-colourable. In
particular, no deletion repair using at most three new points gives a
five-chromatic graph on at most508 vertices from either fixed host.

There is no restriction on the coordinates of S. The conclusion is
specific to these hosts and c. It says nothing about four additions,
other relative placements of the constituent gadgets, or other hosts.
No improved record graph is established.

## Definitions and imported reduction

Put z=sqrt(33), alpha=i*sqrt(3), r=sqrt(-408+72z)>0,
F=Q(z,r), and K=F(alpha). Scaled coordinates (X,Y) represent X+alpha*Y,
with N(X,Y)=X^2+3Y^2. Thus plane membership in K is membership in F^2.
Let A and V be the pinned Parts tables of orders159 and214. Define

    t=(5+z+5alpha-alpha*z/3)/12,
    B=A union (conjugate(A)+t),
    u_±=(-18-6z-30alpha+6alpha*z ± r*(3+6alpha+alpha*z))/72,
    H_±=B union u_±*(V-V[10]),     V[10]=alpha/6.

The host labels and fixed colour row are those of the
[arbitrary-two-point theorem](../hadwiger_nelson_dense506_two_point_extension/PROOF.md).
Each host has506 vertices and2389 unit edges. The colour row has SHA256
`010e6190aa14b6eadc285a6131d7b455bd5434f79ed9b4f69cdfb2848acddcb4`.
The data and arithmetic are pinned in the source and transitive manifest.

Write C3(H) for the nonhost points with at least three unit neighbours
in H. The preceding
[field/midpoint reduction](../hadwiger_nelson_dense506_triangle_midpoint_reduction/PROOF.md)
and [non-field closure](../hadwiger_nelson_dense506_nonfield_triangle_closure/PROOF.md)
imply that any failure to extend c after at most three additions has:

1. Three distinct new points in K outside H union C3(H).
2. A unit equilateral triangle on those three points.
3. Exactly two H neighbours at each new point, of different colours.
4. The same pair of neighbour colours at all three points.

Indeed all cases meeting C3, all non-field cases, and all cases with
fewer than three distinct new points have already been closed. Outside
C3 the available lists have size at least two. A graph on three vertices
with such lists fails list-colouring only for a triangle with all lists
equal to one two-element set (the three-set matching criterion).
The two neighbour colours are the complementary set. These previous
extension theorems are explicit imported premises; their large censuses
are not rerun here.

It remains to exclude precisely this finite field-valued configuration.

## A complete field-valued circle-intersection census

For any differently coloured H pair a,b, let d=b-a, s=N(d)>0,
m=(a+b)/2, and J(X,Y)=(-3Y,X). The common unit neighbours are

    m ± J(d)*sqrt(q)/2,       q=(4-s)/(3s).

This follows by subtracting the two circle equations and using
N(Jd)=3s. If q=0 the two points coincide. If q is negative there is no
real intersection. Since d is nonzero and belongs to F^2, a common
neighbour belongs to F^2 if and only if q is a square in F. A square in
F is automatically nonnegative in the fixed real embedding.

We inspect every one of the96003 differently coloured host pairs. Their
squared distances have22887 distinct values. Exactly184 values give a
square q, accounting for13552 host pairs;32 pairs are tangent. The other
22703 distance values have explicit nonsquare certificates below.
The complete field-valued intersection set has4523 distinct points:
506 host points,1402 members of C3, and2615 new points with exactly two
H neighbours. The other18 points of the complete1420-point C3 census
have monochromatic host neighbourhoods and therefore do not arise from
a differently coloured host pair. The new census does not assume their
absence from any other geometric family.

The producer finds square roots by a complete tower algorithm. For
A+B*r in F, write a prospective root as u+v*r with u,v in Q(z).
If B=0, either v=0 and u^2=A, or u=0 and v^2=A/(-408+72z).
Otherwise

    (u^2-(-408+72z)*v^2)^2 = A^2-(-408+72z)*B^2,
    u^2=(A ± sqrt(A^2-(-408+72z)*B^2))/2,
    v=B/(2u).

The same identity in Q(z), followed by rational integer-square tests,
reduces the problem completely to rational arithmetic. Both signs and
the pure-r branch are included. The code returns the positive real root;
both geometric signs are then used. More importantly, the proof checker
does not trust this algorithm to decide nonsquareness: every accepted
root is squared exactly, and every rejected distance gets the following
independent certificate.

## Why the finite-field nonsquare certificates are sound

Let O=Z[z,r], with basis1,z,r,zr and defining relations
z^2=33 and r^2=l=-408+72z. These form a genuine degree-four field:
l has negative conjugate under z -> -z and so is not a square in Q(z).
For every prime p outside{2,3,11}, the algebra O/pO is reduced.
To see this, over the algebraic closure of F_p the polynomial z^2-33
has two distinct roots. At either root l is nonzero, since

    (-408+72z)*(-408-72z) = -4608 = -2^9*3^2.

The polynomial r^2-l therefore also has two distinct roots at each
choice of z. The resulting four-factor algebra has no nonzero nilpotent.

Suppose q has coefficients with denominators prime to p and q=b^2 in F.
Then b also has all coefficient denominators prime to p. Otherwise choose
k>0 minimally so that p^k*b lies in the free Z_(p)-module with basis
1,z,r,zr. Its nonzero reduction modulo p has square zero, contradicting
reducedness. Thus every map z -> z0, r -> r0 to F_p sends q to a square.

Accordingly a certificate consists of a prime p outside{2,3,11}, valid
roots z0,r0, invertible denominators of q, and

    q(z0,r0)^((p-1)/2) = -1 mod p.

The checker tests primality by exact trial division, verifies all ring
relations and denominator conditions, and checks this equality. Across
all22703 excluded distances only17 maps are required, at the eight primes
17,29,31,37,83,101,103,131. No finite-field test
is used to infer that an element is a square. In particular, a residue
obstruction is a certified rejection, not an approximate geometric test.

## Exact triangle exclusion

Group the2615 new points by their two host-neighbour colours. Colour
masks use bit1<<c for c in{0,1,2,3}; the available list is the complement.
The complete exact unit graphs within the six groups are:

| Host colour mask | Points | Unordered pairs | Unit edges | Unit triangles |
|---|---:|---:|---:|---:|
| 3 |409|83436|127|0|
| 5 |391|76245|99|0|
| 6 |472|111156|87|0|
| 9 |411|84255|147|0|
|10 |486|117855|96|0|
|12 |446|99235|87|0|
| Total |2615|572182|643|0|

The primary scan uses one finite-field incidence filter, followed by the
exact equality N(x-y)=1 for every survivor, and intersects exact adjacency
sets to enumerate all triangles. A noninvertible point denominator is
retained by this filter, never discarded.

A separate audit rebuilds H_- directly from the original Parts tables,
using generic eight-basis quotient-ring arithmetic from the
[accepted arithmetic review](../hadwiger_nelson_dense506_two_point_extension_review1/README.md).
It checks all96003 pair assignments and all22887 distance/root decisions,
reconstructs all4523 points and their complete pair provenance entrywise,
and scans all2288638 host/point pairs using a different modular image
and exact norm arithmetic. Every host incidence and point classification
matches. The audit rejects noninvertible denominators rather than silently
omitting them; all denominators in this run are invertible at its prime.

For triangles it independently reconstructs the643 exact edges and
checks both possible equilateral third points of each edge, by

    (x+y ± alpha*(y-x))/2.

All1286 exact coordinate lookups miss the respective colour class. Thus
no required triangle exists. The r -> -r field automorphism bijects the
two field-valued censuses, preserves all unit equalities and inequality
of distinct points, and preserves labels and c. Both host embeddings
are therefore covered, as is also checked by the alternate reconstruction.

The preceding reduction now gives a contradiction to every possible
failure to extend c. Restrict the resulting colouring to obtain the
subgraph and deletion-repair conclusions. This proves the theorem.

## Trust boundary and stopping point

This is an unformalized computer-assisted proof. The explicit premises
are the pinned host construction and earlier two/three-addition reductions,
including the non-field closure. This pass checks the remaining field
case with exact integers and rational arithmetic, complete coverage,
explicit root/nonroot witnesses, and a different geometric triangle test.
No SAT solver, floating-point incidence decision, or unfinished certificate
is used. Python, its standard library, source/data, the ordinary proof
arguments and runtime/hardware remain in the trust base. The two new
implementations were run by the author; external review of this theorem
and of the preceding non-field closure remains pending.

This closes the entire at-most-three-addition repair route for these two
hosts, including arbitrary deletions afterward. A fourth-addition search
has not started. Further fixed-host radii should be reassessed against a
changed gadget placement or another structural mechanism before spending
another pass on this family.
