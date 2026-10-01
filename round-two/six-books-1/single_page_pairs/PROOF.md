# Single-page degree-ten pairs force a rigid degree-nine neighborhood

Actual author **six-books-1**, role **researcher**, 2026-10-01.
The campaign uses one signing identity; signatures do not identify authors.

Let a **valid graph** mean a simple red graph G on 22 vertices with at
most three common red neighbors on each red edge and at most six common
blue neighbors on each blue nonedge. Blue is the complement on distinct
vertices. Books are ordinary subgraphs; edges among pages are unrestricted.
All degrees below are red degrees.

**Theorem.** Suppose uv is red, d(u)=d(v)=10, and the unique common
red neighbor of u and v is a. Then d(a)<=9. If d(a)=9, write

```text
X=N_R(u) minus {v,a},   Y=N_R(v) minus {u,a},
T=V(G) minus ({u,v,a} union X union Y),
S_X=N_R(a) intersect X, S_Y=N_R(a) intersect Y, S=S_X union S_Y.
```

These sets have sizes |X|=|Y|=8, |T|=3 and |S_X|=|S_Y|=2.
The point a is red to all of T. The following conclusions hold:

1. Every s in S_X has exactly two red neighbors in X and exactly two
   in T. The corresponding statement holds for S_Y and Y.
2. Both S and T are independent in the red graph. The three T points
   have respectively two, three and three red neighbors in S.
3. Order the four special points with S_X first and S_Y second. Each
   misses exactly one T point. Its four-letter missing-point word
   has multiplicities2,1,1. There are exactly **36 labeled necessary
   incidence patterns**, in two forms with12 and 24 labeled patterns.
4. The red neighborhood of a is triangle-free with **13 edges** and
   degree multiset2,3^8. Its only edges are uv, u--S_X, v--S_Y and
   the eight specified S--T edges. This description has exactly two
   isomorphism types, distinguished below without a graph catalogue.

No hypothesis on the total edge count, global maximum degree, outside
degree floor or rootlessness is required. The proof uses no marked
neighborhood classification or computational exclusion. These are
necessary structures; the theorem does not assert that either structure
occurs in a valid full coloring.

## 1. Partition and saturation at the mark

As uv is red, each root has eight other neighbors besides its partner
and a. The uniqueness of their common red neighbor makes X and Y
disjoint. There are three remaining points T. They are blue to both
roots, X is blue to v, and Y is blue to u.

For the red spine au, the common red pages are exactly v and
N_R(a) intersect X. Thus |N_R(a) intersect X|<=2. Similarly,
|N_R(a) intersect Y|<=2. Consequently

    d(a)=2+d_X(a)+d_Y(a)+d_T(a)<=2+2+2+3=9.

If d(a)=9, all three inequalities are equalities. Hence S_X and S_Y
each have two points, and a is red to all three points of T. Its entire
red neighborhood is {u,v} union S union T.

## 2. Three spines force each special degree

Take s in S_X and put h=d_(G[X])(s), g=|N_R(s) intersect T|.
The red spine us has exactly the page a and h pages in X. Its cap
gives h<=2.

The blue neighbors of v are precisely X union T, eleven points.
The blue spine vs has ten candidate third points after removing s;
among them exactly h+g are red to s. Its blue page cap gives

    10-h-g<=6,  hence h+g>=4.

The red spine as already has the common red page u and the g red
T-neighbors of s, because all of T is red to a. Therefore 1+g<=3,
so g<=2. Combining these inequalities forces

    h=g=2.

The same argument with u and v exchanged gives the result for S_Y.
For every s in S, the spine as now has its three pages: its own
root and its two T-neighbors. Any red adjacency from s to another
member of S would add a fourth common red page. Thus S is independent.
In particular the within-block two neighbors of a special point lie
among the other six, nonspecial block points.

## 3. Summing the three remaining red spines

For each t in T the common red pages on the red spine at are exactly
N_R(t) intersect S and N_R(t) intersect T. Both roots are blue to t,
and a has no other red neighbors. Hence

    c_R(a,t)=d_S(t)+d_(G[T])(t).

There are eight S--T edges, because all four special points have
T-degree two. Sum the three page caps:

    8+2e(G[T]) = sum_(t in T) c_R(a,t) <=9.

The edge count is an integer, so **e(G[T])=0**. Now the three
S-degrees sum to8 and are each at most3. Their multiset must be2,3,3.
This is the complete argument eliminating every nonempty T graph.

## 4. The 36 patterns and two neighborhood types

Each special point omits one T point. Since T row degrees are2,3,3,
the omission multiplicities are2,1,1. Choose the repeated omitted
T point (three choices), choose the two special positions omitting it
(six choices), and assign the other two omissions (two choices).
This gives3*6*2=36 labeled patterns, with no quotient or symmetry
assumption used to remove a case.

In twelve patterns the two repeated-omission positions belong to the
same special pair S_X or S_Y. In the other twenty-four they belong to
different pairs. Permuting T, permuting within S_X and S_Y, and
exchanging the roots maps any pattern of each form to any other of
that form. Thus these are two orbits with the roots and special pairs
retained.

Within N_R(a), the only edges are uv, the two u--S_X edges, the two
v--S_Y edges, and the eight S--T edges:13 edges in all. Each root and
each special has local degree three. The T degrees are2,3,3. There
are no triangles: the S--T graph is bipartite, neither root is red
to T, and neither root is red to the other's special pair.

The unique local degree-two vertex is the T point omitted twice.
Its two neighbors are special points, mutually blue. Delete that T
point and join its two neighbors; this gives a simple cubic graph on
eight vertices. In the same-pair form its neighbors are the two
members of the other special pair, so the newly added edge creates
exactly one triangle, through that pair's root. The two special
points have no other common neighbor after the deletion. In the
cross-pair form its neighbors belong to different special pairs and
have no common neighbor after deletion, so no triangle is created.

This distinguishes the two types even as unmarked nine-point graphs:
an isomorphism must preserve the unique degree-two vertex, hence also
the triangle count after its suppression. It supplies a complete
description of this forced neighborhood without a cubic-graph census.

## 5. Application to the thirteen-edge leaf frontier

The earlier lemma
[9071](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/leaf_neighbor_reduction/PROOF.md),
`bafkreiho6lqqnl7sfo7ttqewug4ffhpqynybcniatdser7vzrt4uialzzq`,
studied the following marked red neighborhood of a degree-ten root u.
Its mark a=0 has global degree nine and all other local points have
global degree ten:

```text
0:1,8,9; 1:0; 2:6,7; 3:4,5; 4:3,7,9;
5:3,6,8; 6:2,5,9; 7:2,4,8; 8:0,5,7; 9:0,4,6.
```

The lexicographic red-edge key is6790396772737. Its full local leaf
v=1 and u have exactly one common red neighbor, a. Our theorem applies
directly and improves the earlier e(T)<=1 conclusion to **e(T)=0**.
This conclusion needs only the two full root degrees and the degree-nine
mark; it does not use the other eight prescribed global degrees,108
edges, maximum degree, rootlessness, or the inherited classification.
The four special columns have T-degree exactly two, with no red edges
between any two of their points.

A further local-edge corollary retains the displayed neighborhood and
all its stated root/neighbor global degrees, but assumes only e(G)<=108
and the ordinary page caps, with no global maximum degree. Put B=N_B(u).
The ten red-neighbor degrees sum to99, and their induced red graph has13
edges. Thus the A--B red edge count is99-10-26=63 and

    e(G)=10+13+63+e(G[B])=86+e(G[B]).

Every blue spine ub gives d_(G[B])(b)>=4. There are eleven B points,
so e(G[B])>=22 and e(G)>=108. Equality follows from the assumed upper
bound, and G[B] is four-regular. This edge-total calculation and its
hypothesis reduction are credited to independent review
[9105](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/leaf-neighbor-audit/REVIEW.md),
`bafkreidoqp2j7xs4otszqbipiilrlxcw6oxptzw7bgpifuolplvexg2nny`,
actual reviewer six-reviewer-2, and are rederived here.

Write Y=B minus T. Since T is independent, its four-regular B degrees
give twelve T--Y edges. The graph G[Y] has22-12=10 edges. In
N_R(v)={u,a} union Y, the only other edges are ua and the two
a--S_Y edges. Therefore

    e(G[N_R(v)])=13.

This excludes the fourteen-edge second-root branch for this specific
leaf configuration. Review9105 independently confirms the full original
9071 theorem and sharpens its low/high incidence counts under its
explicit hypotheses. That verdict does not transfer to this new proof.
We do not reapply the one-nine classification at v, which the earlier
theorem forces to have additional deficient neighbors.

## 6. Exact controls and trust boundary

The proof above is an ordinary argument. The small computations validate
its incidence conclusions, page identities and two types; they are not
premises for the theorem or a census of full colorings.

[derive.py](derive.py) enumerates all 3^4 missing-point words and all
eight red graphs on T,648 candidate cores. The red at caps leave
exactly 36, all with T independent. Independently, [verify.py](verify.py)
starts with all 2^4 subsets in each T row (4096 row triples), retains
the four column-degree-two condition, and builds the corresponding 648
literal22-point Boolean matrices. It counts actual third vertices on
the fixed spines, checks root degrees10,10,9 and the unique uv page,
and computes the nine-point neighborhood and its suppressed graph.
Every accepted actual encoded core is compared entrywise with
[EXPECTED.json](EXPECTED.json). The labeled type counts are12 and 24.

The matrices make the red root--mark, red root--special, red mark--special,
and blue opposite-root--special bounds tight. Other omitted edges are set
blue solely to test the selected spines. The matrices may contain other
forbidden books and are **not valid host constructions**. In an actual
host all edges incident to a, both roots, and each core special--T pair
are fixed by the proof. Arbitrary remaining edge choices cannot change
the red at page counts or the induced neighborhood of a.

Both programs use only exact integers and Boolean colors, CPython 3.12.14
standard library. Serial normal/optimized producer and checker records
are byte-identical; six deliberate damaged records reject in both modes.
All six jobs completed in at most 0.316 seconds and 19,932KiB under an
unchanged 90-second external guard, native thread variables one and the
standing 1CPU/2GiB scope. No timeout or solver status is a premise.
Reproduction commands and exact domain records are in [README.md](README.md)
and [provenance.json](provenance.json).

The author used two different enumerations and literal color checks;
these do not constitute an independent peer review. The combinatorial
proof and implementation correspondence remain unformalized. No new
external review is claimed.

## Literature and remaining frontier

The primary tables of
[Lidicky--McKinley--Pfender--Van Overberghe](https://arxiv.org/pdf/2407.07285)
and [Radziszowski](https://www.cs.rit.edu/~spr/ElJC/sur.pdf) were reopened
live on 2026-10-01. The located interval for R(B4,B7) remains22..23.
The known
[primary21-point construction](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
was freshly reproduced with 93 red edges, red page maximum 3 and blue
page maximum 6; its raw SHA256 is recorded in provenance. This is known
baseline validation, not a new construction. The published upper23 flag
certificate was not replayed. Targeted primary searches did not establish
an earlier identical pair theorem; no exclusive historical priority is claimed.

The new progress is the pair restriction without an edge-total assumption, the forced
36-pattern/two-type degree-nine neighborhood, and the independent-T
refinement at the old leaf frontier. General leaf completions, mixed
outside incidences and the Ramsey endpoint remain open. The next concrete
step is to couple the two forced special pairs with all remaining leaf
completion data and deficient-neighbor tags, using actual page counts.
