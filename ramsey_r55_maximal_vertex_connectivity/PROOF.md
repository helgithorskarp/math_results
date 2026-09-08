# Maximal vertex connectivity of every hypothetical good43

Write red for adjacency and blue for nonadjacency. A graph is **good** if
neither color contains a K5. Vertex connectivity is the minimum number of
vertices whose deletion disconnects the graph. All graphs considered in
the theorem are noncomplete.

**Computer-assisted theorem.** If G is good on 43 vertices, then

\[
\kappa(G)=\delta(G),\qquad
\kappa(\overline G)=\delta(\overline G).
\]

The complete excluded family consists of all 43-vertex colorings with
connectivity strictly below minimum degree in either color. There is no
fixed component graph, symmetry hypothesis, or restriction on the other
physical edges. This is a necessary property of a hypothetical target,
not an existence or nonexistence proof for good43.

## 1. Inputs and the complete separator reduction

We import the standard bound R(4,5) <= 25. Primary provenance includes
the [Gauthier--Brown HOL4 proof](https://arxiv.org/abs/2404.01761); this
package does not rerun that formalization. It gives 18 <= d(v) <= 24 in
each color of a good43. The elementary bounds R(3,3) <= 6, R(3,4) <= 9,
and R(3,5) <= 14 are proved in the pinned
[separator18 package](../ramsey_r55_separator18_classification/PROOF.md).
That package also proves the following two facts, used here:

1. Every separator of size at most 18 in a good43 has size 18 and leaves
   exactly a singleton of degree 18 and a connected component of order 24.
2. A triangle-free 12-vertex graph with independence number at most four
   has at most one independent four-set whose deletion leaves no
   independent four-set.

The complete prerequisite package and its finite evidence are replayed.
See `dependency.py` for the complete pinned source manifest. No completeness assertion about an
external graph catalog is used.

Fix a color and suppose k = kappa(G) < delta = delta(G). The first
prerequisite excludes k <= 18: its sole boundary forces delta = 18.
Since delta <= 24, we have 19 <= k <= 23. Choose a minimum separator S
of size k. Distinct red components of G-S are blue-complete to each
other, so their independence numbers add to at most four.

There is no clique component A. A singleton has degree at most k,
contradicting delta > k. For a = |A| in {2,3,4}, every vertex in A has
at least delta-a+1 red neighbors in S. Therefore

\[
|\bigcap_{v\in A}N_S(v)|
\ge a(\delta-a+1)-(a-1)k
\ge \delta-(a-1)^2.
\]

The last inequality substitutes k <= delta-1. At delta >= 18 the
lower bounds are 17, 14, and 9 for a = 2,3,4. The corresponding upper
bounds are 13, 4, and 0: a common red neighborhood has no red
(5-a)-clique and no blue K5. Each lower bound exceeds its upper bound.
Notice that the expression is **delta-(a-1)^2**, not delta-a+1.

Consequently each component has independence number at least two.
There are exactly two components A,B, both with independence number
two and order at most 13 by R(5,3) <= 14. Put a <= b for their orders.
They satisfy a+b = 43-k, so a >= 7. These are all possibilities:

| k | unordered component orders |
|---|---|
| 19 | 11+13, 12+12 |
| 20 | 10+13, 11+12 |
| 21 | 9+13, 10+12, 11+11 |
| 22 | 8+13, 9+12, 10+11 |
| 23 | 7+13, 8+12, 9+11, 10+10 |

We will exclude all 14 cases, quantifying over every graph on the
components, every attachment to S, and every edge within S.

## 2. A degree inequality for each component

For a red triangle T in A, let c_A(T) be its number of common red
neighbors in A, and define

\[
\beta_A(T)=1+\sum_{v\in T}d_A(v)-c_A(T),\qquad
\beta(A)=\min_T\beta_A(T).
\]

Such a triangle exists since a >= 7, alpha(A) = 2, and R(3,3) <= 6.
Vertices in A have no red contacts to B. As delta >= k+1, the
inclusion-exclusion lower bound for their common neighbors in S is

\[
|\bigcap_{v\in T}N_S(v)|
\ge 3(k+1)-\sum_{v\in T}d_A(v)-2k
= k+3-\sum_{v\in T}d_A(v).
\]

A red triangle has at most four common red neighbors in the entire
good graph: any red edge among them gives a red K5, whereas five
blue-complete neighbors give a blue K5. Thus

\[
c_A(T)+|\bigcap_{v\in T}N_S(v)|\le4,
\quad\hbox{and hence}\quad k\le\beta(A).                 \tag{1}
\]

If n_i(T) counts outside vertices of A with exactly i red contacts
to T, a direct contact count gives

\[
\beta_A(T)=7+n_1+2n_2+2n_3=2a+1-2n_0-n_1.             \tag{2}
\]

Therefore beta(A) <= 2a+1. This excludes every listed case with
a <= 9. For a = 10 we have the stronger analytic bound beta(A) <= 20:
let F be the complement of A. It is triangle-free with independence
number at most four, so its maximum degree is at most four. Some
vertex v has two neighbors u,w, since otherwise F is a matching plus
isolated vertices and has an independent five-set. The pair u,w is
independent in F and has the common neighbor v. Its two neighborhoods
have union of size at most seven, excluding u and w. At order ten
there is a third vertex t outside that union and outside {u,w}.
The set {u,w,t} is independent in F, hence a red triangle in A.
The vertex v has at least two blue contacts to it, so 2n_0+n_1 >= 1
in (2). This proves beta(A) <= 20 and excludes a = 10 when k >= 21.

## 3. Coupled coverage of all separator vertices

For z in S call its attachment to A **special** if its blue neighbors
Q_z in A form a red clique. If z is special on neither A nor B,
choose a blue pair among its blue neighbors on each side. The two
pairs, all blue across A--B, together with z form a blue K5.
Thus **every vertex of S must be special on at least one side**.

Write F for the complement of a component. Its special blue-contact
set Q is independent in F and has size at most four. Also F-Q has
no independent four-set, since four red neighbors of z forming a
red K4 would join z to form a red K5. Conversely these are exactly
the necessary special-contact conditions used below. In particular
F-Q is triangle-free with independence number at most three, and
therefore has at most eight vertices.

For a 13-side no special attachment exists, since 13-4 > 8.
For a 12-side a special set must have size four, and is unique by
prerequisite 2. All special separator vertices have the same eight
red neighbors in that side. Those eight vertices contain a red
triangle. Its global common-neighbor bound limits the number of
special separator vertices on this side to **at most four**.

The new finite lemma provides the smaller-side bounds:

**Marked-component lemma.** Let F be triangle-free with independence
number at most four and let A be its complement. If F has a special
set Q, then:

- at order ten, beta(A) <= 19;
- at order eleven, beta(A) <= 20;
- at order eleven with beta(A) >= 19, there are one or two red
  triangles T_j in A such that every special red-neighbor set
  V(A)-Q contains at least one T_j, and
  sum_j (4-c_A(T_j)) <= 6.

The last property bounds the number of special separator vertices
on that 11-side by six. For each triangle T_j at most 4-c_A(T_j)
vertices outside A can be red-complete to it. Cover every special
vertex by one of the triangles and use the union bound. Counting
a vertex more than once only weakens the upper bound. This is a
capacity constraint on the **actual common separator S**, not an
uncoupled list of allowable local signatures.

## 4. Complete exact proof of the marked-component lemma

Choose one special independent Q and set H = F-Q. If F has order
ten, h = |H| is 6,7,8; at order eleven it is 7,8. These exhaust
the possibilities because |Q| <= 4 and h <= 8.

Generate every labeled triangle-free graph with independence number
at most three from the empty graph. When appending a vertex, its
neighbor set must be independent and must meet every independent
triple in the previous graph. These conditions are necessary and
sufficient. Removing the last vertex proves completeness and lack
of duplicates by induction. The labeled counts at orders 1 through
8 are 1,2,7,40,322,2812,13842,17640. At orders 6,7,8 explicitly
applying all vertex permutations partitions the labeled sets into
15,9,3 disjoint orbits. Their least edge words and exact orbit sizes
are retained in `SUMMARY.json`. This needs no graph-isomorphism
library or automorphism-verifier claim.

For each H representative append q = |Q| labeled, mutually
nonadjacent vertices. Their neighbor sets X_i in H must be
independent. A five-set meeting Q is independent precisely when
its remaining vertices avoid the union of the corresponding X_i.
Since H already has no independent four-set, the full necessary
and sufficient additional conditions are:

- every union of two X_i meets every independent triple of H;
- every union of three X_i meets every independent pair of H;
- when q = 4, the union of the four X_i is V(H).

`enumerate.py` generates all ordered star tuples satisfying these
conditions, computes beta by degrees and common neighborhoods, and
finds the stated one/two-triangle covers. The complete 39 jobs yield
43,833 marked ten-vertex graphs and 3,078 marked eleven-vertex
graphs. These are marked physical graphs after normalizing H;
different markings or isomorphism types may repeat. They are not
counts of target classes. The 1,896 order-eleven records with
beta >= 19 all have a cover; costs 3,4,6 occur 1464,264,168 times.

Coverage of marked graphs is enough for the universal lemma: any
counterexample with a special Q can be relabeled to an H
representative with Q last, so appears in one of these jobs. The
certificate covers **all** special Q in each resulting graph,
including ones other than the distinguished mark.

The separate `independent.cpp` uses a different complete enumeration:
it sweeps every edge word on six and seven vertices, and every
one-vertex extension of the surviving sevens to obtain the eights,
checking full forbidden subgraphs. It generates nondecreasing
multisets of star neighborhoods, tests the full resulting graph,
then expands all distinct permutations of the marked vertices.
It does not use the producer's pair/triple prefix conditions.

`audit.py` imports no producer. It compares the complete labeled
core sets and every marked physical graph word, checks all literal
triangles and five-sets in all 46,911 graphs, and computes beta via
the contact identity instead of the degree formula. It enumerates
every possible special Q of sizes zero through four, then verifies
every cover, every capacity, and all per-job witness-stream hashes.
Both Python modes, including `-O`, reproduce the same compact
outputs. Address and undefined-behavior sanitizer runs cover the
full native enumeration and are byte-identical to the release run.

These are exact integer enumerations. Catalogs and floating-point
optimization assisted discovery only and are absent from the proof
computation. The proof is computer-assisted, not formally verified
or independently peer-reviewed. Independence of the two algorithms
is not a claim of independent authorship or external review.

## 5. Close all remaining global cases

After the analytic order bounds, the five remaining cases give:

| k | a+b | bound on special vertices in S | contradiction |
|---|---|---|---|
| 21 | 11+11 | 0: (1) requires beta >= 21 on both sides | 0 < 21 |
| 20 | 10+13 | 0: the ten-side requires beta >= 20 | 0 < 20 |
| 20 | 11+12 | 6+4 | 10 < 20 |
| 19 | 11+13 | 6+0 | 6 < 19 |
| 19 | 12+12 | 4+4 | 8 < 19 |

Every separator vertex must be covered. Thus each row is impossible,
and all 14 global order cases have been excluded. The first two
rows use the marked degree bounds to show there are no special
attachments at all. The next three use the capacity cover.

We have disproved kappa(G) < delta(G). The reverse inequality
kappa(G) <= delta(G) follows by deleting a minimum-degree vertex's
neighborhood, leaving that vertex and at least one nonneighbor.
This proves equality. Interchanging colors proves the second equality.

## 6. A usable global clause and a physical complete-family decision

For any disjoint nonempty A,B with k = 43-|A|-|B| <= 23, the theorem
implies, in either color c,

\[
\left(\bigwedge_{v=0}^{42}d_c(v)\ge k+1\right)
\Longrightarrow \bigvee_{u\in A,v\in B} x^c_{uv}.        \tag{3}
\]

Otherwise deleting the k remaining vertices is a separator smaller
than minimum degree. `guarded_cut.py` exposes the equivalent OR of
43 negated degree predicates and all the physical crossing-edge
literals. It deliberately uses symbolic degree predicates: a
consumer must encode or establish them correctly. It supplies no
numeric solver numbering or verdict. This implication is valid
under every labeling of every complete good43 search task.

As a concrete supplementary decision, `UNEXTENDABLE_CORE.json`
contains a physical good23 with two red components of orders 10
and 13 and no red cross edges. `verify_core.py` checks all 33,649
five-sets. It then checks all 1024 contact words to the ten-side
and all 8192 contact words to the thirteen-side. Each side word
either supplies a red K4 among the new vertex's red neighbors or
a blue pair among its blue neighbors. In the first case the new
vertex completes a red K5. If neither side supplies a red K4,
the two blue pairs plus the new vertex complete a blue K5.

This exact product implication covers all 2^23 = 8,388,608 possible
new-vertex stars. It proves that this good23 has no good24 extension,
and therefore no good43 completion with twenty unrestricted new
vertices and 650 unrestricted remaining edge variables. The result
is a decision for the entire class extending this literal induced
core. It is not a claim that the core covers all targets or that
any of the 2,189,178 packing tasks has been decided. The two author
catalog records identify the chosen literal input; their catalog
completeness is irrelevant to its direct verification.

## 7. Scope and campaign boundary

Maximal vertex connectivity does not say that every minimum cut
isolates a vertex when delta > 18. It does not imply unconditional
19-connectivity. The theorem sharpens the previous global
separator18 result; that source's finite prerequisite remains an
explicit dependency, with its review status recorded separately.

The method is an application of classical separator, Ramsey, and
common-neighborhood arguments; compare
[Beveridge--Pikhurko](https://ajc.maths.uq.edu.au/pdf/41/ajc_v41_p057.pdf).
No historical priority claim is made. The target-specific order
classification and complete marked certificates are the evidence
offered here.

The h3887 carrier and immutable handoff are preserved. No carrier
factor is multiplied, no new symmetry quotient is claimed, and no
physical packing solver is run. All 2,189,178 packing tasks remain
undecided. This completed gate warrants an immutable global-constraint
handoff, followed by a natural checkpoint. There is no certified
good43, new Ramsey bound, or solver-tractability claim.
