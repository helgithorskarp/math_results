# The four-active branch of the five-digit radix architecture is closed

Let E=Z[omega], omega=(1+i sqrt(3))/2, T={0,1,omega}, and

    A5(z) = {sum(a_j z^j, j=0,...,4): a_j in T}.

The physical graph has the distinct points of A5(z) as vertices and every
distance-one pair as an edge. Its order is at most 243. This result does not
establish a five-chromatic graph or a record improvement.

**Theorem.** Every injective, off-unit-circle member with at most four active
distance-event curves is four-colourable. In the only four-active patterns
that defeat all 256 affine F4 label colourings, every physically realizable
member is exactly three-chromatic.

Combining this with the collision theorem h4119 and unit-circle theorem
h4139, a non-four-colourable member of this entire architecture must be
injective, satisfy |z| != 1, and have **at least five active curves**.
The complete exactly-four-active branch is closed. This statement does not
delete a global pair system that may also contain higher-incidence points.

## Exact physical edge inventory

Labels are the 243 lexicographic words in {0,1,2}^5, decoded using (0,1,omega).
For any two labels their difference is P_d(z)=sum d_j z^j with
d_j in {0} union mu_6. Multiplying the entire displacement by a sixth root
of unity preserves its norm. Canonicalization by the least of these six
rows partitions all 29,403 unordered label pairs into 2,801 classes.

The five monomial classes have norms |z|^j. Off the unit circle, only j=0
is always unit. Its 243 edges are 81 disjoint first-digit triangles.
The other 2,796 classes give distinct nonmonomial distance events
|P_d(z)|^2-1=0. Together with the circle these are exactly the 2,797 curves
of h4105, in the same sorted primitive integer-polynomial order. The checker
independently expands their equations at z=x+i sqrt(3)y by using
z=(x-y)+2y omega and the norm N(a+b omega)=a^2+ab+b^2. It checks the entire
inventory hash, not rounded coordinates or sampled distances.

Consequently, at an injective off-circle parameter with active set Q, the
physical graph is precisely the label graph consisting of the universal
edges and every edge in the classes of Q. When |Q|=4 there are no omitted
additional edges. A K4 in this label graph is impossible for any physical
parameter, whether or not the remaining labels collide.

## Why the eligible list is complete

Reduce E modulo 2, obtaining F4={0,1,t,1+t}, t^2=t+1. For each w in F4^4,
the label map

    C_w(a) = a_0 + w_1 a_1 + ... + w_4 a_4

properly colours all universal triangles. A noncircle curve makes this
word fail exactly when

    n_1 w_1 + ... + n_4 w_4 = c,

where n is the tail of its displacement modulo 2, normalized so its first
nonzero entry is 1, and c is the similarly scaled constant coefficient.
The checker verifies this identity against the actual edges for every
curve and all 256 words. Each failure set is an affine hyperplane of size
64. There are 85 projective normals and 336 realized hyperplane types.

Three or fewer hyperplanes cannot cover 256 words. Four cover them only
if their four size-64 sets are disjoint. Two hyperplanes with nonparallel
normals intersect in 16 points, by rank two linear algebra over F4. Thus
four covering hyperplanes must have one projective normal and all four
constants. Conversely those four hyperplanes partition F4^4.

Exactly 81 normals have all four constants realized. These are HN3 h4135's
81 no-circle patterns, independently recovered here. Each pattern has one
bucket per constant; taking their Cartesian product enumerates every
eligible quartet once. There are 960,768 quartets, with no parameter-chamber
restriction or symmetry quotient. The counts by nonzero tail support are:

| Tail support | Eligible quartets | Explicit F3 colouring | Impossible K4 |
|---|---:|---:|---:|
| 2 | 2,304 | 1,656 | 648 |
| 3 | 73,728 | 67,680 | 6,048 |
| 4 | 884,736 | 865,296 | 19,440 |
| Total | 960,768 | 934,632 | 26,136 |

For clarity, at support s a constant-zero bucket has 2^(s-1) rows, and
each nonzero-constant bucket has 2^s. There are binomial(4,s)*3^(s-1)
normalized normals of support s. These formulas also give the table totals.

## Every eligible quartet receives an exact witness

First try the 81 words with weights (1,w_1,...,w_4) in F3, using omega -> -1.
The producer tests displacement dot products. The independent checker
instead evaluates the 81 words on all 243 labels and directly checks their
values on each edge. A quartet is coloured if one word is proper on all
four groups. Exactly 934,632 quartets receive such a three-colouring.

For each of the remaining 26,136 quartets the code constructs its entire
243-label graph and exhibits four distinct labels with all six edges.
Every edge is checked against the exact universal/event partition.
To exclude this geometry, put one of four proposed points at the origin.
The three difference vectors would have Gram matrix with diagonal 1 and
off-diagonal 1/2. Its determinant is 1/2, so it has rank three. Three planar
vectors have Gram rank at most two, a contradiction. Coincident labels
cannot evade the argument: the six required unit distances force these
four labels to represent distinct points.

Thus no eligible quartet remains unclassified. Every eligible physical
graph is three-colourable and contains T, so its chromatic number is three.
Every other four-active graph retains a proper affine F4 word. This proves
the stated four-active closure without solving any parameter equations.

## Reusable geometric interface

The deterministic K4 witnesses use 3,006 distinct active-curve sets:
2,376 triples and 630 quartets. Their union covers every one of the 26,136
rejected quartets (25,506 assigned to triples and 630 to quartets).
The source can export each curve set together with four label indices.
Every listed conjunction is physically impossible even when more curves
are active: adding edges cannot repair a K4. This exported list is a
sufficient obstruction list, not a complete census of all forbidden
incidences. No new root or global-pair count is inferred from its size.

## Verification boundary

`produce.py` imports the existing h4105 geometry implementation. `verify.py`
imports none of the producer or ancestor implementations. It reconstructs
the 29,403 label pairs, expands norms in a different integral basis, tests
F3 and F4 colourings directly on edges, and reconstructs K4 witnesses using
bitset intersections rather than the producer's set search.
The two programs agree on the transcript of every quartet's word index or
four clique labels, and on every exported forbidden incidence/witness pair.
The public certificate is a 2,275-byte deterministic summary with those
hashes; it is not a substitute for replaying the finite witness checks.

The proof uses exact integers, finite fields and the elementary Gram-rank
argument. It has no floating-point, CAS-factorization, SAT or root-isolation
dependency. The bridge from the finite edge inventory to the physical
family, the elementary hyperplane argument, and imported h4119/h4139
theorems are written mathematics, not a proof-assistant formalization.
This contribution is author checked; no reviewer-1 verdict on it is claimed.
