# Proof audit and an independent terminal replacement

This note audits the r=29 argument of Cao–Mehat, arXiv:2609.04771v1.
All graphs are finite and simple; critical means minimal under proper
subgraphs. Write Z(r) for the usual complete-graph drawing upper bound.
A hypothetical critical counterexample has integer crossing number at most
Z(r)-1. None of the arguments below uses equality in the Hill conjecture.

## 1. The structural input which changes the frontier

The paper's Kempe lemma is valid for every k. In a (k-1)-coloring of G-v,
where d(v)=k-1, each color occurs exactly once among the neighbors x_i of v.
For every pair of colors i,j the two named neighbors must lie in one
bichromatic component: otherwise interchange its colors and color v.
Choose one simple connecting path for each color pair, together with the
spokes vx_i. An edge belongs to only one color-pair path. Paths for disjoint
color pairs have disjoint vertex sets. No branch vertex lies internally on
one of the paths, since only the two endpoint branch vertices have its two
colors. These facts give precisely a branch-clean essential immersion of K_k.
Oporowski–Zhao Corollary 2.2 therefore excludes d(v)=k-1 in a counterexample.
Thus delta(G)>=k, not merely k-1.

The join step also respects this definition. If every terminal critical join
factor had a degree-(k_i-1) vertex, combine its branch-clean immersion with
the actual join edges between branch vertices. A nonincident cross edge
cannot meet a local path at an unrelated branch vertex. This gives an
essential K_r immersion. Consequently some terminal factor J has chromatic
number k>=4 and minimum degree at least k. If |J|=a and n=|G|, Gallai gives
2k-1<=a<=n-r+k, and the other factors have minimum degree at least r-k-1.
The necessary edge bound is

    m >= ceil(ak/2 + (n-a)(r-k-1)/2 + a(n-a)).

Our checker minimizes this expression over *all* permitted integer a,k.
It does not assume the paper's endpoint minimization formula.

## 2. Independently checking the all-order join

For a q-vertex induced sample, every edge survives in C(n-2,q-2) samples and
every crossing in C(n-4,q-4). Applying the published inequality
cr(F)>=5e(F)-(203/9)(|F|-2), summing and dividing gives the lower bound used
in verify.py. Integrality permits its ceiling. Our implementation uses the
binomial expression directly, independently of the target's expanded formula.

For large orders the same crossing inequality gives an independent shortcut.
It also implies cr(F)>=5e(F)-(203/9)|F|, valid for orders 0,1,2 as well.
Retain vertices with probability p=203n/(30m)<=1. Taking expectations in a
crossing-minimal drawing yields

    cr(G) >= 5m/p^2 - 203n/(9p^3)
          = (1500/41209) m^3/n^2.

The hypothesis holds because m>=rn/2 and r>=29. Therefore
cr(G)>=(1500 r^3/(8*41209))n. For r=29 all n>=75 are closed; for r=30 all
n>=78 are closed. These cutoffs are checked exactly, not numerically rounded.

For r=29, orders n<=33 use the small-order subdivision theorem. The code
checks every integer n=34..74, combining minimum degree, the appropriate
Gallai edge inequality, and the join bound for n<=56. The only surviving
numeric rows are (57,827..831) and (58,841..842). At n=57 a disconnected
complement gives m>=840, whose crossing bound already exceeds Z(29).
Thus its complement is connected. No prior r=27/r=28 endpoint, conditional
complete-graph crossing number, old recurrence table, or disputed order-58
enumeration is used.

## 3. Order 57

Stehlík supplies a perfect matching of H-v for every vertex of H=complement(G).
A triangle whose deletion leaves a perfect matching would partition H into
28 cliques, impossible. This is the only matching obstruction needed.
Here Delta(H)<=27 and the total deficit A=sum(27-d_H(v)) is 1,3,5,7,or 9.

The paper's triangle-existence proof covers all these values. For A=1,3,
AES directly contradicts a triangle-free factor-critical graph. For larger A,
choose a vertex with deficit D>=5. If the residual deficit R=A-D<=3, deleting
it gives a bipartite graph with two 28-vertex parts. Triangle-freeness bounds
its neighbors in either part by 2+R, contradicting degree 27-A+R.
The remaining A=9 case has adjacent vertices with deficits 5 and 4; deleting
both gives a bipartite 55-vertex graph of minimum degree at least 25.
It is connected, since each bipartite component has at least 50 vertices.
Factor-criticality forces parts 28,27 and neighbors of both removed vertices
in the larger part. Minimum degree and triangle-freeness confine all their
21 and 22 remaining neighbors to that part. The two sets must be disjoint,
which is impossible. This checks also the implicit connectivity needed to
speak of a fixed bipartition.

A triangle T and Tutte give S containing T with at least |S|-1 odd components
outside. Component orders are bounded below by delta(H)-|S|+1. The checker
regenerates every permitted |S| for all five deficits. Small values |S|=3,4
contradict chi(G)=29 by the component-wise greedy coloring bound. At every
other |S|<=28, the degree-sum identity and the maximum possible outside
edge count force a negative internal edge count. Only |S|=29 remains.

Its outside X is an independent 28-set in H. Define w(u)=27-d_X(u) on S.
The exact degree sums give sum w<=36; for each S-edge yz, w(y)+w(z)<=19.
There is such an edge and a common X-neighbor x. Delete triangle xyz.
In the resulting 27-by-27 bipartite graph, X-side minimum degree is at least
16. A Hall failure of size t>=17 forces r=28-t opposite vertices with
w>=27-r. For r=2..11 this costs at least 50>36. For r=1, the offending
vertex has w>=26, incompatible either with a(v)<=9 when d_S(v)=0 or with
the edge-weight bound when d_S(v)>0. Thus the required matching exists,
contradicting the triangle-deletion obstruction. All five edge rows close.

## 4. Order 58: exhaustive reduction to three barriers

At m=841, G is 29-regular. Rabern's cited inequality has its order term equal
to 18 at n=58, so chi(G)=29 forces a K29, contradicting criticality.
At m=842, H has maximum degree 28, minimum degree 26, and total deficit 2.

The triangle lemma is sound: if H were triangle-free, adding one missing
edge permits at most one 3-clique and no 4-clique in any clique partition.
It therefore cannot yield the 28-clique partition required by edge-criticality.

We also checked the two-triangle lemma. If removing one triangle leaves a
triangle-free graph, AES makes that remainder bipartite with part sizes 27,28.
Degree deficits give total triangle-to-part incidences alpha in [24,26] and
beta in [52,54]. Each nonempty corresponding bipartite triangle-edge family
has at least 18 edges (the checker minimizes its two-sided bound). Distinct
families must be cross-intersecting, hence large stars with one common center.
If only one family exists, the other two triangle vertices have at least 20
common neighbors in the 28-part, giving disjoint triangles directly. With at
least two families, a common center in either part contradicts alpha or beta.
The argument includes all nonempty-family counts 1,2,3.

Delete two disjoint triangles U. Since a perfect matching of H-U would give
28 cliques, choose an inclusion-minimal Tutte witness R and let S=U union R.
There are at least |S|-4 odd components of H-S. Minimality implies each
vertex of R meets at least three components. When |S|=31, all outside
vertices are isolated and the same minimality applied to every nonempty
Y subset R gives |N_X(Y)|>=|Y|+2. This follows from untouched odd components,
so it is simultaneous expansion, not merely a singleton degree claim.

The component-size/parity test gives exactly |S| in {6,26,27,28,29,30,31}.
The degree-sum upper bounds at 26,27,28 are respectively -28,-19,-6.
At 6 the component-wise coloring bound is at most 18. The following three
cases therefore cover every remaining graph, not selected configurations.

## 5. Complete terminal cases

**|S|=29.** The outside has order 29, internal maximum degree at most 4,
and at least one edge ab (otherwise G contains K29). There are at most 11
S-edges. Every chosen edge of each original triangle has at least 11 common
X-neighbors. Choose two distinct anchors outside a,b. Removing the two cross
triangles and ab leaves a 25-by-25 bipartite graph of X-side minimum degree 18.
Any Hall failure would force an S-vertex with original X-degree at most 10,
whereas all have X-degree at least 15. The matching plus those cliques gives
28 cliques covering all 58 vertices.

**|S|=30, ordinary case.** The outside has order 28 and maximum internal
degree 2; e(H[S])<=32. At most one S-vertex has X-degree at most 2, since two
would be incident with at least 47 S-edges. Minimality places it in U.
When this vertex has a cross-neighbor, use it in a cross triangle with a
vertex of R; the relevant two sets in the 24-set R have sizes at least 19
and 18. Without a low vertex, use a good edge of an original triangle.
The other original triangle has a good edge with an anchor different from
the first: otherwise its incident S-edges number at least 45>32.

Delete both cross triangles, including the only possible low vertex.
The remaining 26-by-26 graph has X-side minimum degree 20. A Hall failure
forces r opposite vertices of S-degree at least 25-r, where 1<=r<=6.
For r>=2 they meet at least r(25-r)-C(r,2)>=45 S-edges. For r=1 the vertex
would be low, already removed. This proves Hall for the entire case.

**|S|=30, zero-cross-degree case: independent replacement.** Let ell be the
unique low vertex, with d_X(ell)=0. It lies in an original triangle T0.
Since d_S(ell)>=26 and there are at most 32 S-edges, any other vertex v of S
satisfies

    d_S(v) <= e(H[S])-d_S(ell)+1 <= 7,
    d_X(v) >= 26-7 = 19.

Indeed, the edge sets incident with two different vertices overlap in at
most their mutual edge. Also X contains an edge ab, since otherwise
X union {ell} is an independent 29-set in H. In the other original triangle
choose any edge yz. Its endpoints have at least 19+19-28=10 common
X-neighbors. Choose one x outside {a,b}. Use the three disjoint cliques
T0, {x,y,z}, and {a,b}. The remaining bipartite graph has parts of size 25.
Each remaining X-vertex retains at least 26-2-5=19 neighbors in S; each
remaining S-vertex retains at least 19-3=16 neighbors in X.

A balanced bipartite graph of part size t and part-minimum-degrees a,b with
a+b>=t has a perfect matching: a nonempty Hall-violating left set Q has
|Q|>a, while an opposite vertex outside N(Q) would have degree at most
t-|Q|<t-a<=b. Thus this graph has a matching. Its 25 edges, with the three
chosen cliques, give 28 cliques covering all 58 vertices.

This proof requires neither a unique nontrivial component of X, a selection
among its edges, nor the extra component-incidence expansion. It covers
both of the target checker's zero-degree routes at once.

**|S|=31.** X is independent of order 27, 55<=e(H[S])<=57, and R has order
25 with expansion by two. A triangle with no zero-X-degree vertex is either
splittable into a cross triangle and a disjoint cross edge, or meets at least
48 S-edges. For the latter bound, either its three neighborhoods are disjoint,
or nonsplittability forces all three to be the same singleton (giving 72).
Two nonsplittable original triangles would force 87 S-edges. A nonsplittable
triangle disjoint from a zero-X-degree vertex forces at least 71. Thus,
unless each original triangle contains a zero, retain one triangle inside S
and split the other. Delete its two X-vertices; expansion and Hall match all
25 vertices of R, giving 28 cliques in total.

If each original triangle contains a zero, there are exactly two such
vertices: three would meet at least 75 S-edges. They must be adjacent to
avoid an independent 29-set with X. At most six S-edges avoid the two zero
vertices. All other S-vertices consequently have X-degree at least 18.
Each of the two remaining original triangle edges has at least nine common
X-neighbors; select distinct anchors, use the edge between the zeros, and
match R by expansion after deleting the two anchors. This is again a complete
28-clique partition. It closes the final case.

## 6. Verdict and transfer

The contradiction in every branch is a physical clique partition of H,
therefore a 28-coloring of G, or a crossing bound at least Z(29), or a proper
K29 in a critical graph. The joins are exhaustive. This establishes the
r=29 case under the imported classical theorems stated in DEPENDENCIES.md.
The upstream finite leaf counts are corroborating checks, not load-bearing
certificates for graph realizability.

For r=30, the universal degree/join/sampling arguments remain applicable.
The exact audit, with the published Gallai equality refinement for n<=58,
leaves (59,885..891), (60,900..903), and (61,915). A disconnected complement
at n=59 is also excluded by the join calculation. We do not claim their
complement deficit patterns meet the constants used in Sections 3–5.
Closing those orders is a new mathematical obligation.
