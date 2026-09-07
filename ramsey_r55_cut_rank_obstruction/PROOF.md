# A complete low cut-rank obstruction for Ramsey(5,5;43)

Call a simple graph **good** if it has neither a clique nor an independent
set of order five. Red denotes adjacency, blue nonadjacency. All matrix
ranks below are over GF(2). This is a conditional structural theorem about
a good graph of order 43, not a claim that such a graph exists.

**Theorem.** If G is good on 43 vertices, A is a nonempty proper vertex set,
and a=min(|A|,43-|A|), the cross-adjacency matrix of the cut (A,V-A) has rank
at least L(a), in each of the two colors, where

| smaller side a | 1 | 2–3 | 4–7 | 8–9 | 10–14 | 15–19 | 20–21 |
|---|---:|---:|---:|---:|---:|---:|---:|
| L(a) | 1 | 2 | 3 | 4 | 3 | 4 | 3 |

In particular, **every graph on 43 vertices admitting a cut with at least
four vertices on each side and binary cut rank at most two in either color
is not good**. Every edge inside either side is arbitrary. All low-rank
cross matrices are covered; no fixed graph, automorphism, catalog origin,
neighborhood, or prescribed degree profile is assumed. The profile is a
necessary bound, with no sharpness or simultaneous-attainment claim.

## 1. Imported input and previously established local identities

The sole non-elementary Ramsey input needed here is the established
R(4,5)<=25. Its historical computation and later formal proof are not
replayed in this package. The degree of every vertex of a good43 graph in
either color is between 18 and 24: a monochromatic neighborhood has no
same-color K4 and no opposite-color K5, and the two degrees sum to 42.

For completeness, R(3,3)<=6 follows by taking three neighbors of one color
at a vertex. R(3,4)<=9 has a short consequence: in a triangle-free graph on
nine vertices with independence number at most three, every degree is at
most three; if a degree were at most two, its at least six nonneighbors
would contain an independent triple by R(3,3)<=6, giving an independent
four-set with the vertex. Thus every degree is three, impossible on an odd
number of vertices. The Ramsey recurrence gives R(3,5)<=9+5=14.

Hence a same-color pair has at most 13 common neighbors of that color.
A same-color triangle has at most four common neighbors of that color:
such neighbors are pairwise opposite-colored, and five are forbidden.

We explicitly reuse the pair/triple mechanism of the earlier
[module-resilience contribution](../ramsey_r55_module_resilience/README.md),
Discovery Net `bafkreid5jz6lrr44rfqjboywlrlcj2rgbfxv5c2wpwf5oybjimtap5doku`,
source commit `823d258fe6dfa33a695e148bbed08b1709fbe3c9`. Its independent
acceptance is `bafkreigpgiwq63wwv445jjf4r75pn7ajlajtivdzshhof25jr6wu3kj6eu`.
These identities are reproved here; they are not claimed as new.

A vertex outside a set Q **distinguishes** Q if it has both red and blue
contacts to Q. For an internally red pair u,v, let t be the common-red
count and D the distinguishing count. Then

    D = d_red(u)+d_red(v)-2-2t >= 36-2-26 = 8.

For a red triangle, common-red count t<=4 and distinguishing count D give

    54 <= sum of its red degrees <= 6+3t+2D <= 18+2D,

so D>=18. For a mixed triple, rename colors and labels so its red edges
are 01,02 and blue edge is 12. For an outside contact signature (x0,x1,x2),

    x0*x1 + x0*x2 + (1-x1)*(1-x2) = 1_{x0=x1=x2}+x0.

Let C01,C02 be common-red counts and C12 the common-blue count. The third
internal vertex contributes to none of these. Summing the identity over
the 40 outside vertices yields

    C01+C02+C12 = 40-D+d_red(0)-2 <= 39,
    D >= d_red(0)-1 >= 17.

Thus every pair has at least eight distinguishers, every triple at least
17, and every monochromatic triple at least 18. Color reversal covers all
cases. No Goodman total or full adjacency-rank hypothesis is used.

## 2. Occupancy bounds for equal rows across an arbitrary cut

Take the smaller side A, of size a<=21, and B of size b=43-a. An equal-row
class M consists of vertices of A with identical contacts to every vertex
of B. Such classes may have different internal graphs and contacts inside
A; they need not be modules of G.

If a<=9, two vertices in an equal-row class have all their distinguishers
in A minus that pair, of size at most seven. This contradicts the pair
bound. Every row class therefore has size at most one.

If a<=19, three vertices in an equal-row class have all their distinguishers
in A minus that triple, of size at most 16. Thus every row class has size
at most two.

If a=20 or 21, every row class has size at most five. Indeed, suppose
|M|>=6. By R(3,3)<=6 it contains a monochromatic triangle, say red. Let
X be the vertices of B red to M, and Y the vertices blue to M. Any red
edge in X would join the triangle to make a red K5. Thus X is blue-complete
and |X|<=4. Now |Y|>=b-4>=18>=14, so R(5,3)<=14 and the absence of a red
K5 force a blue triangle in Y. Any blue edge in M would join that triangle
to make a blue K5. Therefore M is red-complete, forcing |M|<=4, a
contradiction. A blue starting triangle gives the same proof with colors
reversed. This argument applies regardless of other edges in A or B.

There are two useful uniform-row restrictions:

* If a<=18, then b>=25. R(4,5)<=25 and its color reversal force both a red
  K4 and a blue K4 in B. Consequently neither the all-one nor the zero
  contact row can occur at any vertex of A.
* If a=20 or 21, then b>=22>=14. B contains a blue triangle, since it has
  no red K5. The zero-row class is blue to this triangle, so it has no blue
  edge. It is therefore red-complete and has size at most four.

Only the zero-row restriction is counted below. We do not assume that the
all-one vector belongs to the binary row space.

## 3. From row occupancy to the global family decision

A rank-r binary row space contains exactly 2^r vectors, including zero.
The preceding class bounds imply the following necessary inequalities:

| a | maximum vertices allowed by r row-space dimensions |
|---|---:|
| 1–9 | 2^r-1 |
| 10–18 | 2(2^r-1) |
| 19 | 2*2^r |
| 20–21 | 4+5(2^r-1)=5*2^r-1 |

An absent zero class only decreases the last capacity. Applying each
inequality to its stated range gives exactly L(a). In particular, at r=2
the respective capacities are 3,6,8,19, each strictly less than a when
4<=a<=21. This proves the complete selected family exclusion. Applying
the same reasoning to the complement proves the blue-matrix restriction
as well; red and blue cut ranks need not be equal.

No enumeration of all good43 graphs is required. The checked arithmetic
records the consequences of a universal proof, not a feasibility test of
only a local relaxation.

## 4. Decomposition consequences

In a subcubic decomposition tree with 43 leaves, give each leaf weight one
and every internal vertex weight zero. A weighted centroid exists: walk
toward a component with more than half the total weight while one exists;
crossed edges cannot be crossed back, so the walk terminates. A centroid
cannot be a leaf. Its at most three incident components each have at most
21 leaves and their leaf counts sum to 43. The largest therefore has
between 15 and 21 leaves. Its incident edge gives a cut to which L(a)>=3
applies. Every rank-decomposition has width at least three, so

    rank-width(G) >= 3 and rank-width(complement(G)) >= 3.

Every vertex ordering has a prefix of size eight. Its cut has rank at
least four, yielding

    linear rank-width(G) >= 4,
    linear rank-width(complement(G)) >= 4.

The argument does not prove rank-width at least four: the profile has
lower bound three at some possible centroid cut sizes. No rank-width-three
family decision is asserted or begun. Definitions follow Oum's survey
[Rank-width: Algorithmic and structural results](https://arxiv.org/abs/1601.03800).
For linear layouts we use the standard maximum cut rank over prefixes,
equivalently the width of the associated caterpillar decomposition.

## 5. Complete physical consumer in F27

The earlier [pentagon normal form](../ramsey_r55_pentagon_normal_form/README.md)
has 61 fixed pairs: induced red pentagons on 2..6,7..11,12..16,17..21,22..26,
and red 01 and red contacts from 0,1 to 2..6. The remaining 842 physical
pairs are free. Its universal-coverage premise is external to this theorem.

Choose A=7..26 (20 vertices) and B={0..6,27..42} (23 vertices). All 460
cross pairs are free. There are 150 free pairs within A and 232 within B,
for 382 arbitrary internal bits after imposing the 61 pins. Our complete
consumer branch allows every 20 by 23 binary cross matrix of rank at most
two, in either chosen color, and every assignment of those 382 bits.
Every member is excluded by the theorem above.

The number of distinct binary m by n matrices of rank k is

    N_k(m,n) = product_{i=0}^{k-1} [(2^m-2^i)(2^n-2^i)/(2^k-2^i)].

To justify it, factor a rank-k matrix as U V with U full column rank and V
full row rank. There are product(2^m-2^i) choices of U and
product(2^n-2^i) choices of V. Every matrix has exactly |GL(k,2)| such
factorizations: changing the basis gives (U Q,Q^{-1} V), and these are all.
Define the empty product N_0=1. The three counts here are

    N_0 = 1,
    N_1 = 8,796,083,585,025,
    N_2 = 12,895,167,237,418,895,565,739,350.

Their sum is 12,895,167,237,427,691,649,324,376. For each chosen rank color,
the excluded fixed-label F27 branch therefore contains exactly

    12,895,167,237,427,691,649,324,376 * 2^382

distinct physical graphs. This counts both non-Ramsey and hypothetical
Ramsey assignments before exclusion; the proof shows none are Ramsey.
The red and blue branches can overlap and are not added in this count.

`model.family` uses all U in GF(2)^(20x2), all V in GF(2)^(2x23), and all
382 internal bits. The 86 factor bits cover every rank<=2 cross matrix:
pad a rank-0 or rank-1 factorization with zero rows/columns. This map is
deliberately many-to-one; the distinct-graph count above is not a count of
factor words and does not divide degenerate fibers by six. The executable
map assigns all 903 physical pairs and preserves all 61 pins.

This is a complete target-facing branch decision, not a solution of the
rest of F27. No measured search-speed improvement, candidate, or change in
the Ramsey lower bound follows from it. No SAT solver, fixed neighborhood
gluing, full adjacency-rank cutoff or graph-catalog scan is used.

## 6. Provenance and trust

R(4,5)=25 is due to McKay and Radziszowski,
[*R(4,5)=25*](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf).
Gauthier and Brown give a later formal treatment,
[*A Formal Proof of R(4,5)=25*](https://arxiv.org/abs/2404.01761).
Neither computation is an executable dependency of this package.
All smaller Ramsey bounds needed above are given elementary derivations.

Equal-neighborhood classes and the binary 2^r bound are standard. The
Ramsey pair/triple distinguishers already belong to the cited accepted
module-resilience result. This contribution turns them, together with a
short uniform-class argument, into the stated all-cut profile, complete
low-rank family decision and physical F27 consumer. Limited literature and
Discovery Net checks do not establish historical priority. No claim of
optimality or independence from earlier module theory is made.

The proof is unformalized. Finite controls validate exact arithmetic,
matrix counts, small physical identities, the parameter map and certificate
implementation; they do not enumerate the exponentially large global
family or replace the universal proof. The supplied full graphs are
expressly non-Ramsey controls. The verifier uses dense elimination and ten
literal edge checks, independently of the producer. Independent external
review of this new theorem remains pending.
