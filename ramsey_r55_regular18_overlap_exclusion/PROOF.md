# Complete exclusion of the regular degrees 18 and 24 at order 43

A good graph has neither a clique nor an independent set of order five.
There is no 18-regular good graph on 43 vertices. By complementation there
is no 24-regular one either. No automorphism, vertex partition or selected
neighborhood is assumed in the class under decision.

## 1. Every large-color neighborhood belongs to the same complete finite list

Suppose R is an 18-regular good graph. Fix v, put A=N_R(v), and put
B=V(R)-A-{v}. Thus |A|=18 and |B|=24. Write

    a = e(R[A]),       b = e(complement(R)[B]).

Counting red cross edges from A and from B gives respectively

    e_R(A,B) = 18*18 - 18 - 2a = 306-2a,
    e_R(A,B) = 24*18 - 2*(276-b) = 2b-120.

Consequently a+b=213. R[A] has no K4 and no independent five-set, so the
published exact extremum U(18)=85 implies b>=128.

Let X=complement(R), which is 24-regular and good. **For every vertex v**,
H_v=X[N_X(v)] is a (4,5;24) graph with at least 128 edges. The complete
published catalog contains 352,366 graphs. Exactly 1,027 meet this edge
bound: 843,147,32,3,2 at edge counts 128,129,130,131,132 respectively.
The pinned full catalog is scanned in both implementations, and the exact
retained graph6 lines are compared. Catalog completeness and U(18)=85 are
imported results, not established by this scan.

## 2. Exact overlap of the neighborhoods of any edge

Choose any edge uv of X, and set

    C = N_X(u) intersect N_X(v),       c = |C|,
    T = V(X) - (N_X(u) union N_X(v)),  t = |T| = c-5.

The two neighborhood vertex sets each have size 24 and their union includes
both u and v. C is triangle-free: a triangle in C together with uv would
be a K5. Let e=e(X[C]) and d_w=d_{X[C]}(w) for w in C.

For i in {u,v}, set

    D_i(w) = degree of w inside H_i,
    L_i(wz) = number of common neighbors of w,z inside H_i,
    P_i = sum over w in C of D_i(w),
    Q_i = sum over w in C of d_w D_i(w)
          - sum over edges wz of X[C] of L_i(wz).

These values are obtained solely from the actual rooted neighborhood graph
(H_i, the other endpoint). The common graph C must be the same on both sides.

Let r_w be the number of neighbors of w in T. Counting its full degree in X
and correcting the twice-counted common vertices gives the exact identity

    r_w = 24 - D_u(w) - D_v(w) + d_w.

Since r_w<=t, summing over C proves the first required inequality:

    P_u + P_v >= c(29-c) + 2e.                         (I)

Now let wz be an edge inside C. Its common neighbors in X are counted by
L_u(wz)+L_v(wz), together with their common neighbors in T. This is exact:
the roots u and v occur once each, and C contributes no common neighbor
because C is triangle-free. The two neighbor subsets of T have intersection
size at least r_w+r_z-t. Moreover an edge of a good graph has at most 13
common neighbors, by the classical R(3,5)=14 bound. Hence

    13 >= L_u(wz)+L_v(wz)+r_w+r_z-t.

The right side is a valid lower bound even if r_w+r_z-t is negative.
Summing over the e edges of C, substituting the expression for r_w, and
using sum_w d_w=2e gives the second required inequality:

    Q_u + Q_v >= sum_w d_w^2 + (40-c)e.                (II)

These are simultaneous necessary conditions on any edge of the entire
43-vertex graph. They do not assume that the two neighborhoods are identical
or that the gluing has any symmetry.

## 3. A deliberately enlarged compatibility test has no pair

Root each of the 1,027 retained physical graphs at each of its 24 vertices.
For each of the resulting 24,648 rooted graphs, compute C, its sorted degree
sequence, and the pair (P,Q). Bin the roots only by c and the sorted degree
sequence of C. Isomorphic common graphs necessarily have the same bin.
Graphs with the same degree sequence need not be isomorphic: permitting
all their pairings enlarges the possible overlap family and is safe for
an exclusion. No graph canonicalizer or automorphism verifier is used.

There are 39 bins and 527 distinct (bin,P,Q) profiles. Within each bin,
check all unordered pairs of profiles, including a profile paired with
itself. These 6,669 pairs cover all ordered physical rooted pairings as
well, since (I) and (II) are symmetric in the two sides.

Every pair fails: 6,140 fail (I); the other 529 fail (II). No pairing meets
both. CERTIFICATE.json lists every bin, profile and threshold. The independent
checker reconstructs them from the full pinned catalog and compares each
entry, rather than only these totals.

Thus X cannot have an edge, contradicting its degree 24. This proves the
complete regular18/24 family exclusion.

## 4. Consequences for the campaign's physical search

R(4,5)=25 gives the usual degree window 18 through 24 in any good43. A regular
graph of odd order has even degree, so any regular good43 must now have
degree **20 or 22**. This does not exclude degree-18 vertices in an irregular
graph and does not prove that any good43 must be regular.

The complete regular18 and regular24 strata in every h3887 physical task
are empty. In particular, the teammate's frozen q10 formulas at degrees
18 and 24 are decided semantically by this theorem; no assertion is made
that their old CNFs or unfinished proof streams have been certified. Their
20/22 strata and all irregular completions remain unresolved. No entire
h3887 packing task is declared empty. No good43 or Ramsey lower-bound
improvement is established.

## Inputs, independence and scope

The catalog and its completeness statement are at
https://users.cecs.anu.edu.au/~bdm/data/ramsey.html . The full order24 input
SHA256 is 83ca4028f206b2fa4315ef219b8c2c57c7835209673dd8183d8fb4353bd4fdd0.
The exact U(18)=85 input was independently audited in the campaign's
local-extremal deficiency review; that review imports the historical catalog
completeness. R(3,5)=14 and R(4,5)=25 are stated in McKay and Radziszowski,
R(4,5)=25, JGT 19 (1995), https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf .

The new finite test requires no solver, graph-isomorphism library, floating
point, target CNF, or old neighborhood-gluing implementation. The producer
uses adjacency sets and vertex-weight scores. The separate checker rebuilds
Boolean matrices, computes Q as a sum of literal edge scores, checks all
1,027 retained graphs for the two Ramsey obstructions, and reconstructs
all 6,669 pair decisions. Physical small-graph controls check the overlap
identities directly, including edges inside C and nonempty T.

The result is computer-assisted with explicit imported catalog/extremum
inputs; it is not proof-assistant formalized or externally reviewed here.
Residual trust includes the written covering and overlap argument, the two
implementations, exact Python integer/bit operations, SHA256, OS and hardware.
An indexed prior statement at kenan.works asserts this same regular-degree
exclusion. Its page returned HTTP502 when queried, so its proof and priority
could not be checked. No historical novelty is claimed for the theorem.
The present package supplies a reproducible overlap certificate and a usable
complete branch decision for this campaign.
