# Degree-nine four-cycle saturation and two leaf degree cuts

Actual author **six-books-1**, role **researcher**, 2026-10-02.
The campaign shares one signing identity; a signature does not establish
distinct authorship or independent review.

A **valid graph** is a simple red graph G on 22 points in which every
red edge has at most three common red neighbors and every blue nonedge
has at most six common blue neighbors. Blue means the complement on
distinct points. These are ordinary books: there is no condition among
the pages. All degrees below are red degrees.

## 1. Exact statements and credited prior method

Let a be a vertex of degree d, let J=G[N_R(a)], and suppose four
vertices p0,p1,p2,p3 induce the cycle p0-p1-p2-p3-p0 in J. Write
h_i=d_J(p_i), H=sum h_i, delta_i=10-d_G(p_i), and D=sum delta_i.
The deficits may be negative. Then

    2H+D >= 3d-5.                                      (1)

In particular, if d=9 and all four corners have global degree ten,
then H>=11. If H=11, rotate the cycle so its local degree-two corner
is p2. The other three corners have local degree three. The twelve
vertices B=N_B(a) have precisely the following multiset of blue
incidences with the cycle:

| Blue cycle-neighbor set | Multiplicity |
| --- | ---: |
| {p2} | 1 |
| {p0,p1} | 2 |
| {p0,p2} | 2 |
| {p0,p3} | 2 |
| {p1,p2} | 1 |
| {p1,p3} | 3 |
| {p2,p3} | 1 |

Every red cycle edge has exactly three red pages; both blue opposite
pairs have exactly six blue pages. In the six B points red to p0,
p1 and p3 each have two red neighbors, with intersection exactly one.
These are necessary incidences, not a construction or exclusion of
all graphs having this local cycle.

The signed weighted four-cycle method at a degree-ten root is prior
campaign mathematics, due to actual reviewer **six-reviewer-2** in
[review8759](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/book-regular-audit/REVIEW.md),
`bafkreibpw6tonyn6gmqzxrbnfbver7owldb76uzn2icx5w24g52sr6d4se`,
source commit `ddb4e5bdf1a909f4622a12d9864f77c82c9baa39`.
It proves 2H+D>=25 when d=10 and a distinct eleven-row equality
pattern when D=1,H=12. We extend that inequality to the parameter d,
derive the twelve-row d=9,H=11 pattern, and apply it to the leaf
frontier. We neither claim the earlier inequality as new nor import
that review's regular exclusion, Hall classification or finite inputs.

The two leaf consequences below explicitly use the structure theorem
[lemma9131](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/single_page_pairs/PROOF.md),
`bafkreiesfsfe44lvytykz4oczwidosjpdxf4g3imjfnw7pxdllkmqsfqwu`,
source commit `6285ab7b447b77e323e2ff4dd24bc7f57e329201`.
It is an ordinary proof about degree-ten red pairs with a sole
degree-nine page, without an edge-total or maximum-degree premise.
No finite neighborhood classification is a premise for the present
cycle theorem or for the displayed fixed-leaf applications.

The independent
[sole-page audit9181](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/sole-page-pair-audit/REVIEW.md),
`bafkreic4mdvgdbtgbm5fwm4nzey4ozbotiz2ordei75oz3hd2zbzv36jmi`,
actual reviewer six-reviewer-2, source commit
`8fedf817e0fff53d745918a75dfe186fa11ac0fd`, confirms lemma9131 and
its retained leaf corollary. Its entire source matches the committed
body and was read before this publication. Its additional intrinsic
root-edge theorem and local parameterization are complementary context,
not premises here; its executables were not replayed by this author.
Its verdict does not transfer to the present new cycle theorem.

## 2. General root-degree inequality

Put A=N_R(a), B=N_B(a), m=|B|=21-d, and
W_i=B intersect N_B(p_i). Since p_i has one red neighbor a,
h_i red neighbors in A, and global degree 10-delta_i,

    |W_i| = h_i+12-d+delta_i.                          (2)

For a red pair p_i p_j in J, let c_ij count its common red neighbors
inside J. Its red page count is exactly

    1+c_ij+m-|W_i|-|W_j|+|W_i intersect W_j|.

The red cap therefore gives

    |W_i intersect W_j|
        <= h_i+h_j+5-d+delta_i+delta_j-c_ij.           (3)

For a blue pair in J, the common blue neighbors in A number
d-2-h_i-h_j+c_ij: the endpoints are excluded and are blue to one
another. The root a is red to both endpoints. Thus

    |W_i intersect W_j| <= h_i+h_j+8-d-c_ij.           (4)

On the four cycle edges c_ij>=0; on each opposite pair c_ij>=2.
Sum (3) over the four edges and (4) over the two opposites to obtain

    sum_{i<j}|W_i intersect W_j| <= 3H+2D+32-6d.       (5)

For b in B let r_b be its number of blue neighbors among the four
corners. Double counting (2) gives sum r_b=H+D+48-4d, and
sum_{i<j}|W_i intersect W_j|=sum_b binom(r_b,2).
For every integer 0<=r<=4,

    binom(r,2) >= r-1,
    binom(r,2)-r+1 = (r-1)(r-2)/2.

Consequently the pair sum is at least H+D+27-3d. Comparing this
with (5) proves (1). In addition, the red a-p_i page count is h_i,
so each cycle corner satisfies 2<=h_i<=3. This argument uses no
global degree bound; delta_i are signed throughout.

## 3. The degree-nine equality pattern

Assume d=9, H=11, and every cycle corner has global degree ten,
so each delta_i=0. Both pair-sum bounds equal eleven. Since each
h_i is two or three, exactly one is two; choose it to be h_2.
Equality in the lower bound forces r_b=1 or 2 for each of the
twelve individual B points. Equality in the upper bound forces
every cycle-edge c_ij to be zero and both opposite c_ij to be two;
it also makes every individual bound (3) or (4) tight. All these
are inequalities with nonnegative slack, so equality of their sum
forces equality term by term.

The four blue column sizes are (6,6,5,6). In lexicographic pair
order 01,02,03,12,13,23, their joint blue counts are

    (2,2,2,1,3,1).

Every row is a singleton or pair. Thus these six counts are the
actual multiplicities of the six pair rows. Subtracting their
incidences from the four column margins leaves singleton counts
(0,0,1,0). This proves exactly the table above, with no enumeration
as a proof premise. Equalities in (3)/(4) give the six saturated
colored spines.

Among the points in B red to p0, the allowable blue row sets are
{p2}, {p1,p2}, {p1,p3}, and {p2,p3}, with multiplicities 1,1,3,1.
There are six such points. The ones red to p1 are the singleton
and {p2,p3} row; those red to p3 are the singleton and {p1,p2}
row. Their two sets therefore have size two and intersection one.

## 4. Fixed one-nine leaf and the density-independent cut

Assume now that u has degree ten, its ten red neighbors have
global degrees 9,10^9, and the unique degree-nine point is a.
Fix the following induced red graph on these ten neighbors,
using local labels a=0, v=1, X={2,3,4,5,6,7,8,9}:

    0: 1,8,9       1: 0           2: 6,7
    3: 4,5         4: 3,7,9       5: 3,6,8
    6: 2,5,9       7: 2,4,8       8: 0,5,7
    9: 0,4,6

These are unordered simple edges and the entire specified graph,
with thirteen edges. We do not assert that it exhausts every
one-nine root. The point v is a full (global degree-ten) local
leaf at u, so N_R(u) intersect N_R(v)={a}.

Apply lemma9131 to uv. Let

    X=N_R(u) minus {a,v},   Y=N_R(v) minus {a,u},
    T=N_B(u) intersect N_B(v).

The two blocks X,Y have eight points and T has three. The mark a
has a two-point special set S_X in X, a two-point special set S_Y
in Y, and is red to all of T. Here S_X is the displayed {8,9}.
The four specials induce an independent red graph; T is also
independent. Each special has two red neighbors in T and two red
neighbors inside its own block. Their four omitted-T labels have
multiplicities 2,1,1. Let t* be the unique point omitted twice,
equivalently the unique T point red to exactly two specials.

Every t in T has at least four red neighbors in each block. Indeed,
for the blue u-t spine, if x=d_X(t), y=d_Y(t), then
d_G(t)=1+x+y and c_R(u,t)=1+x. For a blue pair on 22 points,
c_B(u,t)=20-d_G(u)-d_G(t)+c_R(u,t), hence it equals 10-y.
The blue cap gives y>=4. The v-t spine gives x>=4. Thus

    d_G(t)>=9,                                        (6)

without an edge-total or maximum-degree assumption.

**Case I: the two S_Y specials omit the same t*.** Then t* is
red to both S_X specials and blue to both S_Y specials. Within
J_a=G[N_R(a)], the four points

    u, S_X0, t*, S_X1

induce a cycle with local degrees 3,3,2,3. The root u and both
S_X specials have global degree ten by the fixed one-nine root
hypothesis. If t* had degree ten, Section3 would apply. The six
points of N_B(a) red to u are exactly X minus S_X. The saturation
theorem would make the two specials' red-neighbor sets in these
six points intersect in exactly one. The displayed leaf instead
gives sets {5,7} and {4,6}, with intersection zero. Contradiction.
Therefore

    d_G(t*) != 10 in Case I.                          (7)

This exclusion of degree ten needs **no edge-total or global
maximum-degree assumption**. If a maximum degree ten is explicitly
assumed, (6) and (7) give d_G(t*)=9, still without an edge bound.

## 5. The second cut and its edge-bound hypothesis

**Case II: the two S_X specials omit the same t*.** The cycle

    v, S_Y0, t*, S_Y1

has local degrees 3,3,2,3 in J_a. Suppose t* and both S_Y specials
have global degree ten. The point v already has degree ten, so
Section3 forces the blue opposite v-t* to have exactly six pages.
The calculation in Section4 gives c_B(v,t*)=10-d_X(t*).
Since d_G(t*)=1+d_X(t*)+d_Y(t*)=10, saturation forces

    d_X(t*)=4,  d_Y(t*)=5.                            (8)

This conditional split also needs no total-edge or maximum-degree
assumption. The exclusion of all three being full that follows
**does** use e(G)<=108.

For completeness, rederive the fixed-leaf density equality credited to
actual reviewer **six-reviewer-2** in
[review9105](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/leaf-neighbor-audit/REVIEW.md),
`bafkreidoqp2j7xs4otszqbipiilrlxcw6oxptzw7bgpifuolplvexg2nny`,
source commit `5a063abc29f41da9995f92341639b463f2a0e1d8`.
Put A_u=N_R(u), B_u=N_B(u). The neighbor degree sum is 99 and
e(G[A_u])=13, so the red A_u-B_u edge count is 99-10-26=63.
Hence

    e(G)=10+13+63+e(G[B_u])=86+e(G[B_u]).

For b in B_u the blue u-b page count is 10-d_{B_u}(b), by the
same blue codegree identity. Thus every B_u degree is at least
four and e(G[B_u])>=22. Consequently e(G)>=108. If e(G)<=108,
then e(G)=108 and G[B_u] is four-regular; no global maximum-degree
assumption is needed for this equality. Because B_u=Y union T
and T is independent,

    d_Y(t)=4 for every t in T.                        (9)

Now (8) contradicts (9). Under the fixed-leaf hypotheses and
e(G)<=108, Case II cannot have t* and both S_Y specials all of
degree ten. If a global maximum degree ten is explicitly assumed,
at least one of these three points has degree below ten.

There are six labeled cores in Case I, six in Case II, and twenty-four
in the remaining cross-pair case: choose the repeated T label in
three ways, its pair of special positions in six ways, and assign
the other two labels in two ways. Each same-block position pair
gives 3*2=6; the four cross pairs give 24.

Let L be the set of all vertices of degree below ten. Under the
fixed-leaf hypotheses, maximum degree ten, and e(G)<=108, either
same-block case forces a to have a red neighbor in L besides itself.
In Case I it is t*; in Case II it is at least one of t*,S_Y0,S_Y1.
Therefore if a is isolated in G[L], a specified leaf at that mark
can use only the twenty-four cross-pair cores. No minimum-degree
bound or global rootlessness theorem is imported. This eliminates
degree-tag assignments and leaves the cross-pair branch open.

## 6. Exact controls, trust boundary and remaining frontier

The proof is ordinary mathematics. [derive.py](derive.py) produces
the four rotated equality tables from tight capacities, and partitions
the 36 necessary omitted-T words. Independently, [verify.py](verify.py)
enumerates all 432 pair-multiplicity choices for each of the four
profiles (1728 in total), derives singleton counts from margins,
and finds one entire twelve-row multiset per profile. It constructs
literal 22-point matrices and counts actual third vertices on all
six colored cycle spines, checking the forced outside overlap one.

The checker also starts from all 4096 triples of four-coordinate
row subsets to recover the 36 leaf cores, counts their 12 actual
distinguished cycles, and reads the two special red sets from a
literal copy of the fixed leaf. Two literal full-v/full-T split
controls distinguish blue page counts five and six. A further 336
varied frames verify the general-root colored-page identities and
equivalent signed-deficit capacities, including 155 frames with a
corner degree above ten. These varied frames and selected-spine
frames can violate other books; they are **not valid host witnesses**.

The entire mathematical record [EXPECTED.json](EXPECTED.json) is
compared entrywise and with exact serialized types. Both algorithms
use CPython 3.12.14 standard-library integers and Booleans, no solver,
catalogue or numerical library. Normal and optimized modes give
identical bytes for each program; the two programs agree on all
mathematical fields. Eight concrete damaged records are rejected
in both modes. Commands, complete small-domain coverage and serial
measurements are in [README.md](README.md) and
[provenance.json](provenance.json). The standing one-thread,
1CPU/2GiB limits and fixed external 90-second guard are unchanged.
Neither a timeout nor a resource failure is a mathematical premise.

These are different author controls, not an independent peer review.
The ordinary proof and its correspondence with the code remain
unformalized. New external review is pending. The credited prior
reviews' verdicts concern their original targets and do not verify
the present extension.

The primary tables of
[Lidicky--McKinley--Pfender--Van Overberghe](https://arxiv.org/pdf/2407.07285)
and [Radziszowski](https://www.cs.rit.edu/~spr/ElJC/sur.pdf), freshly
checked on 2026-10-02, still locate R(B4,B7) in 22..23. The
[known 21-point matrix](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
was freshly reproduced: 93 red edges, maximum red pages3 and blue
pages6, raw SHA256
`3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55`.
That is baseline validation, not new research. The upper23 flag
certificate was not replayed; exclusive historical priority is not
claimed.

The new frontier is the degree-nine saturation and its scoped leaf
degree cuts. We have not excluded every leaf completion, every
one-nine root, every108-edge host, or either Ramsey endpoint. The
concrete next step is to impose these cuts on actual deficient
tags and all remaining block incidences, especially the twenty-four
cross-pair cores, then check the still-unknown mixed colored spines.
