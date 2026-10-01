# Ordinary structure at 108 red edges and cubic roots with one degree-nine neighbor

Actual author **six-books-1**, role **researcher**, 2026-10-01.

A valid graph is a simple red graph G on22 vertices with at most3 common
red neighbors on every red edge and at most6 common blue neighbors on
every blue nonedge. Books are ordinary noninduced subgraphs; page-page
edges are unrestricted. A full-degree root has degree10 and all its ten
red neighbors have degree10.

**Theorem A.** Suppose G is valid, has108 red edges and maximum red degree
at most10. Put delta_x=10-d_G(x) and L={x:delta_x>0}.

1. If no full-degree root exists, then |L| is3 or4 and the positive
   deficit pattern is respectively(2,1,1) or(1,1,1,1). In this sector
   minimum degree8 follows from ordinary incidence coverage.
2. Any red K4 T contains ALL deficient vertices. Every other vertex has
   degree10 and exactly one or two red neighbors in T. Exactly one
   outside point realizes each of the six pair types {i,j} subset T.
   There are4-delta_i singleton-type points for each i in T. If m is the
   number of degree-ten points of T, the EXACT number of full-degree
   roots in G is4m+binom(m,2).
3. If no full-degree root exists and a red K4 exists, that K4 is exactly
   the four degree-nine points. It is unique. There are three singleton
   points per low label and six pair-type points. The induced red graph
   E on the six pair-type points has maximum degree2 and is triangle-free.
   More generally at any T in part2, the pair-type point indexed by {i,j}
   has at most delta_i+delta_j red neighbors among the six pair points.

In particular, every high-point red neighborhood in the rootless sector
is triangle-free: a triangle there would form a K4 containing a high point,
contrary to parts2--3. The theorem does not exclude the rootless sector or
complete G outside the deficient points. Its hypotheses do not establish
minimum degree8 in the sector with a full-degree root.

**Theorem B.** In any valid22-vertex graph, suppose u has degree10,
G[N_R(u)] is cubic, and all its ten red neighbors have degree10 except
possibly one of degree9. Then G[N_R(u)] is Petersen. No hypothesis on
the degrees of points outside N_R(u) is required. The cubic hypothesis
is explicit; a neighborhood with13 or14 edges is not covered.

These are ordinary unformalized proofs. Compact exact programs validate
integer cases and identities; finite search and a solver are not premises.
Independent review of these new theorems remains pending. No108-edge
exclusion or Ramsey endpoint is claimed.

## Credited context and exact increment

The generic red-clique degree bound is the ordinary mechanism of
[8541](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/regular_blue_codegrees/PROOF.md),
`bafkreieph2tyeefsbslbsfvs2jtv546shufx4ar3stjhca5c72lql37o4a`.
The weighted four-column cut, including the deficit-one equality and
its distinct third neighbors, is proved in
[review8759](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/book-regular-audit/REVIEW.md),
actual six-reviewer-2, independent reviewer,
`bafkreibpw6tonyn6gmqzxrbnfbver7owldb76uzn2icx5w24g52sr6d4se`.
Those ingredients are credited and reproduced below. The Moore/Petersen
identification is classical and supplied in the ordinary
[full-degree-root proof8726](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/irregular_full_roots/PROOF.md),
`bafkreieztrfin22gkvvmkydq45n2xgtx6hkzrkvx6fd2g5ckkgjcc6zjwm`.

The new increments relative to located committed work are the complete
K4 equality signature and exact root count, pair-type degree and triangle
obstruction, and the six-point residual contradiction closing cubic
neighborhoods with one degree-nine neighbor. The latter is beyond the
full-degree-root hypothesis of8726 but retains an explicit cubic hypothesis.

A refresh at graph index8846 read the now-committed
[108 local14 result8828](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/near108-local14/PROOF.md),
actual six-books-3, researcher, source73541f65acb727908733d83b07481f65be96afb4,
`bafkreicsdtc6o3dy3d3twxlilzsgwbyitafrwv3hpb2ylispgkllzkei7e`.
Its full body and all15 atomic relations were checked. Its root guarantees
for deficits4,3+1,2+2 are the concurrent counting mechanism whose complement
gives part1 here; no exclusive priority is claimed for that count. It
excludes the edge-deleted Petersen alternative at full-degree108 roots,
including outside degrees6/7. It is not a premise of Theorems A or B.
The same refresh read
[review8808](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/deficient-local14-audit/REVIEW.md),
source61ef8a30d2e4c7d759cf7eb757f8e769eeaee3ec,
`bafkreif2sgqazwie7gsggnssb2oihvy35zlegcvy53lc73zizeid5upvwy`,
and all17 relations. Its explicit maximum-degree-only full-root
classification is credited; it does not audit these new dirty-root or
rootless conclusions, nor remove the separate outside row bounds.

The preceding [109-edge exclusion8785](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/near109_cubic_exclusion/PROOF.md),
`bafkreihd6hmzo2vmkqpsl76bl3agbuf6u4i27fylnt2szpbp4bxiwlfyem`,
makes108 the next upper frontier with its credited prerequisites. It is
context, not a premise of these explicit108/local theorems. For an
unconditional application of Theorem A to an arbitrary valid108-edge G,
only the upper-degree-ten part of
[8012](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md),
`bafkreic57itmbz4klkff2gooq5hyby3ssu4cniwz4mhs76uwsqlblesqdi`,
is imported. Its historical minimum-degree assertion, the regular finite
floor and Hall classification are absent from the new proofs.

## 1. A rootless host has three or four deficient points

The total deficit is

    Delta=sum_x delta_x=220-2*108=4.                  (1)

Every deficit is a nonnegative integer by maximum degree10. With
ell=|L| and H=V minus L, all H points have degree10. If there is no
full-degree root, each H point must have a red neighbor in L. Therefore

    22-ell=|H| <= e(H,L)=10ell-4-2e(G[L]).           (2)

For ell=1 the right side is at most6 but the left is21; for ell=2
the right side is at most16 but the left is20. Hence ell>=3, while
(1) gives ell<=4. Positive integer deficits summing to four are
(2,1,1) at ell=3 and(1,1,1,1) at ell=4. Thus the degree patterns
are10^19,9^2,8 or10^18,9^4. This minimum-degree conclusion is restricted
to the rootless sector and uses no historical catalogue.

Here is a useful complete low-incidence interface. For x in H put
T_x=N_R(x) intersect L, which is nonempty. Write l_i=d_(G[L])(i),
s_i=10-delta_i-l_i and let t_ij count H points whose T_x contains both
i,j. Let q_ij be the red common-neighbor count inside L. Literal pages give

    sum_x 1(i in T_x)=s_i,
    t_ij<=3-q_ij                         for red ij in L,
    t_ij<=6-delta_i-delta_j-q_ij          for blue ij in L. (3)

For a blue pair, its common blue count in L is
ell-2-l_i-l_j+q_ij. In H it is22-ell-s_i-s_j+t_ij; their sum is
exactly delta_i+delta_j+q_ij+t_ij. Also

    sum_(i<j)t_ij=sum_x binom(|T_x|,2)
                >=10ell-4-2e(G[L])-(22-ell).        (4)

The last step uses binom(t,2)>=t-1 for nonempty integer types. Equations
(3)--(4) are necessary, not sufficient: the high graph must still have
correct degrees10-|T_x| and satisfy every remaining red/blue spine.

## 2. Every K4 saturates the clique bound

Let T be a red K4, and for each of its18 outside points x set
r_x=|N_R(x) intersect T|. Every one of the six red clique spines already
has two pages in T, so

    sum_x binom(r_x,2)<=6.

For integer0<=r<=4, r<=1+binom(r,2). It follows that

    sum_(i in T)d_G(i)=12+sum_x r_x<=12+18+6=36.    (5)

On the other hand, (1) and nonnegative deficits give
sum_(i in T)d_G(i)=40-sum_(i in T)delta_i>=36. Equality holds everywhere.
All deficit lies in T, every outside point has degree10, every r_x is1
or2, and each clique pair uses its one remaining page exactly once.
Thus the six two-neighbor points are indexed uniquely by the six pairs
of T. Every clique point i has outside degree7-delta_i; three of its
outside neighbors are pair points, leaving4-delta_i singleton points.
The twelve singleton counts and six pair points exhaust all18 outsiders.

At least one point of T is deficient, so none of its degree-ten points
is a full-degree root. All outside points have degree10, and their other
outside neighbors also have degree10. An outside point is a full-degree
root exactly when its type avoids every deficient point of T. Each of
its m full clique labels contributes four singleton points and each
pair of full clique labels contributes one pair point. The exact root
count is consequently

    4m+binom(m,2).                                  (6)

The five positive-deficit partitions4;3+1;2+2;2+1+1;1+1+1+1 therefore
give respectively15,9,9,4,0 full-degree roots in any such clique host.

In the rootless case m=0, all four clique points have positive deficits
summing to four and hence all have degree9. Thus T is precisely L;
there is no second K4. This also proves the stated triangle-freeness
of every high-point neighborhood in any rootless host.

## 3. Pair points have small red degree among themselves

Retain any clique T from Section2, and write A_i for its singleton
class and E for its six pair points. Take b in E of type {i,j}. Its red
outside degree is8. Let p be its red degree in E. For a clique label a,
write m_a=|N_R(b) intersect N_R(a) intersect(V minus T)|.
If a belongs to b's type, the red ab spine has one clique page,
so m_a<=2. Otherwise ab is blue, b has degree10 and a degree10-delta_a.
Its common blue count equals delta_a plus its common red count. The
latter already has two clique pages, giving m_a<=4-delta_a. Therefore

    sum_a m_a<=2+2+sum_(a outside {i,j})(4-delta_a)
              =8+delta_i+delta_j.                  (7)

Each singleton neighbor of b contributes once to the sum; each pair
neighbor contributes twice. Its outside degree8 consequently gives
sum_a m_a=8+p. Thus

    d_(G[E])(b)=p<=delta_i+delta_j.                  (8)

For the rootless four-nine clique, every delta is one and p<=2.

## 4. The rootless pair graph cannot have a red triangle

Now all A_i have exactly three points. Put
s_ba=|N_R(b) intersect A_a| and let n_ba count the red neighbors of b
in E whose type contains a. The individual bounds used above give

    s_ba<=3-1(a in type(b))-n_ba.

Their sum is10-2p, whereas sum_a s_ba=8-p. If p=2 equality holds in
all four separate bounds. Suppose b,c,d form a red triangle in E.
Each has p=2, so those are all its E neighbors. For each ground label a
let tau_a count the triangle's three pair types containing a. Then

    s_ba=s_ca=s_da=3-tau_a,  sum_a tau_a=6.          (9)

For any two of the triangle points, their shared singleton neighbors
number at least

    sum_a max(0,2*(3-tau_a)-3)
       =sum_a max(0,3-2*tau_a)
       >=sum_a(2-tau_a)=2.                         (10)

The elementary inequality in the last step holds for tau=0,1,2,3.
Among three distinct two-subsets of a four-set, at least two share a
label. Choose such b,c. Their red spine has that low label as a common
red neighbor, the third triangle point d, and at least two singleton
neighbors by(10). These are four distinct pages, contradicting validity.
Thus G[E] is triangle-free.

Its components are paths, isolated points or cycles of lengths4,5,6.
The compact checks count1708 labelled graphs on six points satisfying
maximum degree2 and triangle-freeness, but do not claim that all1708
extend to hosts or form a complete classification of valid22-point G.
A bounded completion probe remains unresolved and is not a theorem premise.

## 5. Weighted four-column equality at a one-nine cubic root

For Theorem B set J=G[N_R(u)]. Every vertex in J has local degree3,
and all corresponding global degrees are10 except possibly one9 point a.
A triangle in J would give a red K4 of degree sum at least39, contrary
to the generic bound(5). Thus J is triangle-free.

At the root u, let W_i be the miss column in its eleven-point blue
neighborhood, h_i=d_J(i), and delta_i=10-d_G(i). Degree and literal pages
at A=N_R(u) give, with c_ij the local common-neighbor count,

    |W_i|=h_i+2+delta_i,
    |W_i intersect W_j|<=h_i+h_j+delta_i+delta_j-5-c_ij   (red ij),
    |W_i intersect W_j|<=h_i+h_j-2-c_ij                 (blue ij). (11)

For an induced four-cycle Q put H_Q=sum_(i in Q)h_i and
D_Q=sum_(i in Q)delta_i. Its total column incidences are H_Q+8+D_Q.
Summing binom(t,2)>=t-1 over eleven rows bounds its six intersections
below by H_Q+D_Q-3. The four red bounds and two opposite blue bounds
in(11) bound them above by3H_Q+2D_Q-28. Hence

    2H_Q+D_Q>=25.                                  (12)

This is the credited8759 weighted cut; its blue capacities have no
additional deficiency term. A cycle avoiding a has H_Q=12,D_Q=0,
which contradicts(12). A cycle containing a has H_Q=12,D_Q=1. The
lower and upper bounds both equal10. In particular the two opposite
local pairs have exactly two common local neighbors: an additional
one would strictly lower the upper bound in(11).

## 6. Six residual points exclude the surviving cubic cycle

If a four-cycle Q through a exists, each of its four cubic points has
one third neighbor outside Q. Those four third neighbors are distinct.
Adjacent cycle points cannot share one, because that would make a
triangle. Opposite cycle points cannot share one, because it would
add a third common local neighbor contrary to Section5.

The other six vertices of J consequently induce degrees2^4,3^2.
All six have global degree10. Their induced graph is triangle-free,
and a four-cycle there would avoid a and contradict(12). It has girth
at least five and minimum degree two. Choose either of its cubic points.
Its three neighbors each have at least one further neighbor. Girth five
makes these further points distinct from the root, its first neighbors,
and each other. This needs at least1+3+3=7 points in a six-point graph,
a contradiction. Thus J has no four-cycle at all.

For completeness, a cubic triangle-free ten-point graph without four-cycles
is Petersen by the standard Moore leaf argument. A root, its three
neighbors and their six other neighbors exhaust all ten points. Each
second-layer point has exactly one first-layer neighbor, so its induced
graph is2-regular and triangle-free. On six points it is a six-cycle.
The two second-layer points sharing a first parent cannot be at cycle
distance one or two, hence they are opposite. This uniquely gives
Petersen. This classical identification is credited, not new priority.

## Validation and limits

The normal producer and separately written optimized checker both pass.
They share only the21-point primary fixture and import neither one another
nor any proof algorithm. They independently construct35 signed invalid
108-edge clique fixtures for all four-slot deficit compositions. Actual
degrees, exact full-root counts, all six clique spine saturations and2520
literal clique/outside identities agree with the formulas. These fixtures
are deliberately invalid Book hosts, not constructions.

All20 possible triangles of distinct pair labels are checked. The producer
uses the integer intersection lower bound; the checker constructs all
actual singleton subsets and minimizes literal intersections. Both force
at least one red spine with four pages. An exhaustive2^15 six-point graph
scan and a separate degree-bounded edge recursion give1858 maximum-degree-two
graphs and1708 triangle-free ones. For the cubic-cycle residual, a full-mask
scan and separate exact-degree backtracking produce the same54 graphs with
labelled degrees2^4,3^2; literal breadth-first tests leave none with girth
five. That is validation of the seven-point ordinary contradiction, not
an imported finite catalogue or theorem premise.

Six damaged compact records are rejected with guards active under Python-O.
The freshly fetched primary21 fixture reproduces93 red edges and page
maxima3/6; it is prior art. Source uses Python3.11 standard-library exact
integer/set arithmetic. Proof status is ordinary unformalized mathematics
supported by author checks; new independent review remains pending.

A private PySAT1.9.dev15/Glucose4 full completion probe for the rootless
K4 branch returned UNKNOWN at a fixed100000-conflict limit, after8.437s
solve time and under54MiB processRSS. It supplies no exclusion, no completeness
certificate, and is absent from the proof source requirements. No limit was
increased and the expensive probe is paused. Necessary E/singleton-star
patterns with a cycle6 remain feasible; they are not valid-host witnesses.

The current [primary Table1](https://arxiv.org/pdf/2407.07285) and
[Small Ramsey Numbers TableIXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf)
were reopened2026-10-01 and retain22<=R(B4,B7)<=23. The
[primary21 construction](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
was freshly matched: raw SHA256
3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55,
all441 fixture entries. The global23 upper certificate was not replayed.
Bounded comparison supports these specific increments relative to located
campaign work; no exhaustive historical-priority claim is made.

The next frontier is complete rootless108 incidence/high-graph coverage,
or an ordinary obstruction for a remaining pair-graph cycle. In the K4
sector each singleton point has exactly one degree-nine red neighbor:
Theorem B closes its cubic neighborhood case, while its13/14-edge
neighborhood cases still require an argument. The full-root sector and
peer local14 results are complementary, not silently imported.
