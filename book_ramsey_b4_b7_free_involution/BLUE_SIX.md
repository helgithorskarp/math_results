# Seven blue uniform pairs under every free involution

Actual author: **six-books-2**, role **researcher**, 2026-10-01.
All team members share one signing identity; this identifies the author.

**Theorem.** In every ordinary red-B4/blue-B7-free coloring of K22,
for every fixed-point-free color-preserving involution of the coloring,
at least **seven unordered pairs of its eleven two-vertex orbits are
fully blue**. Every red uniform density, matching signing and
inside-orbit color is covered. No regularity, degree theorem or graph
catalogue is assumed.

**Conditional lemma.** If at least two orbits are entirely matching,
there are at least **eight** blue uniform pairs, without the global
support/minima theorems as premises.

**Corollary.** Together with the prior three-red bound, at least ten
orbit pairs are uniform. At exactly ten, if attainable, the only color
counts are **three red/seven blue**, and at least **ten orbits are
incident with uniform pairs**. This excludes the formerly permitted
four-red/six-blue profile and supplies an analytic ten-total proof.
Neither equality attainment nor an involution in every hypothetical
22-vertex witness is asserted. The unrestricted Ramsey gap remains open.

The main theorem uses [SUPPORT.md](SUPPORT.md)'s analytic uniform-support
minimum nine and blue-pair minimum six. Its optional red/total corollary
uses [TWO_RED.md](TWO_RED.md). The preceding finite [NINE.md](NINE.md)
theorem is refined, not used as a premise; its original computation
trust boundary remains unchanged. The new mechanism is a two-row
sign action that forces an impossible shared-leaf equality shape.
The six remaining blue-degree cases are divided in writing.
**No finite computation is a premise of this analytic proof.**

## 0. Literal page identities and inherited local observations

Write each two-point orbit as {(i,0),(i,1)}, i=0,...,10. Invariance under
simultaneous exchange makes every cross block fully red R, fully blue B,
or one of the two red matchings M. Indeed the four cross edges have two
orbits under exchange; their two color choices give exactly these four
blocks. Let the red and blue uniform graphs be R and D, respectively.
An orbit is entirely matching if all ten cross blocks at it are M;
its inside edge can have either color.

Use W_ij=+1 on R, -1 on B and 0 on M, and S_ij=+1 on parallel matching,
-1 on crossed matching and 0 on R/B. Both diagonals are zero. Put u=W1,
so u_i=deg_R(i)-deg_D(i). At a matching pair ij write sigma=S_ij. Fix
(i,0), and choose its red neighbor and blue neighbor in orbit j as the
two opposite-color spines. The doubled contributions from an outside
orbit k are as follows, where alpha=W_ik,
beta=W_jk, x=S_ik and y=S_jk:

    twice red pages:  (1+alpha)(1+beta)+sigma*x*y,
    twice blue pages: (1-alpha)(1-beta)-sigma*x*y.

These follow by intersecting the two subsets of the outside two-point
orbit. They apply also to uniform outside blocks, for which the relevant
S entry is zero. The two inside-orbit mates give no pages at matching
spines: the needed cross edge has the opposite color. Summing all nine
outside orbits proves the matching identities used in Section 1 below.
Their combined page count is 9+(W^2)_ij, so the caps three/six imply
(W^2)_ij<=0 at every matching pair.

For a red uniform pair ij, summing the red pages at (i,0)(j,0) and
(i,0)(j,1) gives

    sum_{k!=i,j}(1+W_ik)(1+W_jk)+2(epsilon_i+epsilon_j)<=6,

where epsilon_i is one for a red inside edge and zero for blue. Replacing
every nonblue outside link by M can only decrease this sum. The result
is at least 9-|N_D(i) union N_D(j)|, proving the necessary red-candidate
bound |N_D(i) union N_D(j)|>=3. This is an inequality, not a sufficiency
assertion or a sign selection.

Two blue leaves sharing a blue neighbor cannot occur: their mutual pair
is nonblue and has blue-neighborhood union size one, so cannot be red
and is M. At their W-square entry the shared blue center contributes one,
and every other contribution is nonnegative since neither leaf has any
other blue link. This contradicts the matching W-square bound.
Two blue isolates likewise cannot share a red uniform neighbor: their
mutual pair is M by the red-candidate bound and their W-square entry is
positive. A blue isolate's red neighbor must have blue degree at least
three, again by the same union bound. These observations were used in
SUPPORT.md and [FOUR_BLUE.md](FOUR_BLUE.md); they are rederived here so
no unmentioned local lemma is needed.

## 1. Two entirely matching orbits force at least eight blue pairs

Use the established orbit notation: W has +1 on red uniform pairs,
-1 on blue uniform pairs and 0 on matching pairs; S has matching
signs +/-1 and 0 on uniform pairs; both diagonals are zero. Put
u=W1. Let R_ij and B_ij denote the red and blue page counts at the
corresponding matching spines. The exact identities are

    2R_ij = 9+u_i+u_j+(W^2)_ij+S_ij(S^2)_ij,
    2B_ij = 9-u_i-u_j+(W^2)_ij-S_ij(S^2)_ij.

Inside edges contribute no pages at these two opposite-color matching
spines. In particular, R_ij<=3 and B_ij<=6 imply (W^2)_ij<=0.

Suppose H={h0,h1} are entirely matching orbits, and I is the other
nine orbits. The H rows of W and their u values vanish. Every matching
pair involving H therefore saturates both page caps, and

    (S^2)_hi=-(3+u_i)S_hi      (i in I),
    S_h0,h1 (S^2)_h0,h1=-3.

Write

    S = [ T  C ; C^T  L ],

where T is the two-by-two matching-sign block, C is two-by-nine with
all entries +/-1, and L=S[I,I]. Then T^2=I_2 and

    C C^T = 9I_2-3T,
    C K = -T C,   K=L+diag(3+u_i : i in I).

Switch the labels of h1 to make T's off-diagonal sign +1, and switch
the I labels to make C's first row all ones. Its second row c then
has sum -3, hence has exactly three +1 entries on a set P and six
-1 entries on Q. These switches preserve W, u and all colors. The
two row actions are

    1^T K = -c^T,   c^T K = -1^T.

For each i in P, adding these equations gives

    sum_{j in P,j!=i} L_ji = -4-u_i.

For each i in Q, their sum gives sum_{j in P} L_ji=0. Let
a_i=-u_i=deg_D(i)-deg_R(i), and let b_PP,r_PP,m_PP count blue,
red and matching pairs within P; similarly use PQ and QQ suffixes.
Summing the displayed identity over P yields

    sum_{i in P} a_i
      =12+2 sum_{matching pairs in P} S_ij
      >=12-2m_PP=6+2b_PP+2r_PP.

But direct degree counting gives

    sum_{i in P} a_i=2b_PP+b_PQ-2r_PP-r_PQ.

Consequently

    b_PQ >= 6+4r_PP+r_PQ,
    e(D) >= 6+b_PP+b_QQ+4r_PP+r_PQ.             (*).

If e(D)<=6, equality forces e(D)=6, b_PP=b_QQ=r_PP=r_PQ=0,
and b_PQ=6. All three P-P pairs are matching with sign -1, and
each i in P has a_i=2. There is no red link at P, so each has
exactly two blue neighbors in Q. For any i in Q the signed matching
sum towards P is zero. The number of those matching links must be
even, so its blue degree towards P is odd: one or three. There are
six blue links total and six Q vertices, hence each Q vertex has
exactly one blue link. Thus D is three disjoint P3 components.

Two blue leaves with the same blue center cannot occur in any valid
quotient: their pair cannot be red by the red-candidate union bound,
so is matching. Their W^2 entry is at least one, since the shared
center contributes +1 and all other contributions are nonnegative.
This contradicts (W^2)_ij<=0. The three-P3 shape is therefore
impossible, proving e(D)>=7 when two entirely matching orbits exist.

This argument is at arbitrary red density, with every matching sign,
inside color and I-I uniform/matching configuration covered. The exact
controls below audit its small matrix actions against literal
page definitions; they are validation, not a proof premise.

## 1.1 The seven-blue boundary at two entirely matching orbits

Suppose e(D)=7 in the same normalized system. Inequality (*) forces
r_PP=0 and b_PP+b_QQ+r_PQ<=1. At each Q vertex the signed matching
sum towards P is zero, so there are an even number of matching links
and an odd number of uniform links towards P. Summing over six Q
vertices makes b_PQ+r_PQ even. Since b_PQ=7-b_PP-b_QQ, exactly three
possibilities remain:

    (b_PP,b_QQ,r_PQ)=(1,0,0), (0,1,0), (0,0,1).

In the first case, b_PQ=6 and there is no red link touching P.
The identity for sum_P a_i gives eight, so both matching P-P signs
are -1. At each endpoint of the single blue P-P pair, a_i=3;
at the third P vertex a_i=2. Thus every P vertex has two blue
neighbors in Q. Every Q vertex has one blue neighbor in P, since
six positive odd degrees sum to six, and there is no blue Q-Q link.
All six Q vertices are blue leaves, giving two at every P center.
The shared-leaf obstruction excludes this case.

In the second case, b_PQ=6 and all three matching P-P signs are -1.
Every P vertex has two blue neighbors in Q and every Q vertex has
one blue neighbor in P. The single Q-Q blue edge makes precisely
two Q vertices nonleaves. The three P neighborhoods partition Q
into disjoint pairs, so at least one pair consists of two blue
leaves. This case is also excluded.

In the third case, b_PQ=7 and there is exactly one red P-Q link.
Now sum_P a_i=6, so all matching P-P signs are -1 and each a_i=2.
The P endpoint of the red link has three blue neighbors in Q;
the other two have two each. There are eight P-Q uniform links,
with each Q incidence odd: one Q vertex has three uniform links,
the other five have one each. There is no blue link inside Q.
If the red link meets the three-link Q vertex, its P endpoint's
three blue neighbors are all one-link Q vertices, hence blue leaves.
If the red link meets a one-link Q vertex, the three-link vertex is
blue to all P. The red P endpoint has that blue neighbor and two
one-link blue neighbors, again two blue leaves. The last case is
excluded, regardless of any red or matching links within Q.

Thus e(D)=7 is impossible with two entirely matching orbits. Together
with the preceding six-edge contradiction, this proves the conditional
eight-blue lemma. The red/blue page caps and the shared-leaf argument
are its only mathematical premises.

## 2. Six blue pairs with at least ten orbits in support are also impossible

The published SUPPORT.md result gives uniform support at least nine
and blue count at least six. If blue count equals six and support
is nine, there are two entirely matching orbits, excluded by Part 1.
Thus six blue pairs would require support at least ten.

Let v be the number of nonisolated vertices in the six-edge blue graph,
and h the number of its vertices with blue degree at least three.
A blue-isolated orbit can only gain uniform support through a red
neighbor of blue degree at least three, by the red-candidate bound
|N_D(i) union N_D(j)|>=3. Two blue isolates cannot share such a red
neighbor: their pair is matching, and its W^2 entry would be positive.
Thus the red-supported blue isolates inject into these h vertices,
and uniform support is at most v+h. Therefore v+h>=10.

Positive blue degrees sum to twelve; v<=11. Each high vertex contributes
at least two beyond the baseline one, so v+2h<=12. If h>=3 this gives
v+h<=9. If h=0, v is ten or eleven; if h=1, v is nine or ten;
if h=2, v is eight. Distributing the remaining degree sum gives
exactly the following six
sequences (1^k means k entries equal to one):

    h=0: (2,1^10), (2,2,1^8);
    h=1: (3,1^9), (4,1^8), (3,2,1^7);
    h=2: (3,3,1^6).

All except (2,2,1^8) immediately force a vertex with at least two
blue leaves, because there are too few other nonleaf vertices to
supply its blue neighbors. The known shared-blue-leaf obstruction
excludes them. For (2,2,1^8), the two degree-two vertices are either
in separate P3 components (again excluded) or in a single P4; the
remaining graph is three disjoint K2 components. Hence the only
unexcluded blue form is P4+3K2, with one blue isolate.

Label its blue path 01,12,23, with all other nonisolated vertices
in the three K2 components. The blue-neighborhood union at nonadjacent
pair 13 has size two, so this pair is matching. Leaf 3 has no possible
red uniform neighbor: with any nonblue partner the blue-neighborhood
union has size at most two. Therefore (W^2)_13=1, solely from common
blue neighbor 2. This again violates the matching inequality.

Six blue pairs are excluded at every support size. The inherited
at-least-six bound now gives at least seven, as claimed. The prior
three-red theorem gives ten uniform pairs and the unique three-red/seven-blue
color count at exactly ten. The inherited support bound is nine; support
nine would leave two entirely matching orbits, requiring eight blue pairs
by Section 1.1, so support is at least ten in that equality case. QED.

## 3. Exact author controls and trust boundary

Python 3.11+ standard library only. From the repository root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -O book_ramsey_b4_b7_free_involution/blue_six_controls.py
```

[blue_six_controls.py](blue_six_controls.py) imports no campaign program.
Its deterministic output matches [blue_six_expected.json](blue_six_expected.json).
Guards are explicit exceptions and survive -O. All integers are exact.
The final CPython 3.11.2 run took 1.271 seconds and
16508 KiB peak child RSS on Linux, with numeric
threads one and one local job.
There is no solver, floating-point calculation, external input or omitted
large corpus. Computation validates the written proof; it is not a
finite-enumeration premise of the theorem.

The controls check all **86016** raw two-row Gram normalizations,
including both signs of the two-orbit block, and a **joint Gram/action
positive control**. In that example all 76 cross spines touching the two
entirely matching orbits attain their caps three/six. It has the forced
three-P3 blue shape and a forbidden active leaf spine, so it is an actual
solution of the joint necessary row system, not a valid Ramsey witness.
This shows why a feasible Gram target alone cannot exclude the case.

For explicit reproduction of the positive control, take P={2,3,4} and
Q={5,...,10}, with h0=0,h1=1. Set T_01=+1, C's first row all +1 and
its second row +1 on P, -1 on Q. Pair the six Q vertices successively,
and blue-link each pair to its corresponding P center. P-P matching
signs are -1. For each Q pair, the two other P centers have opposite
matching signs at each leaf, reversing the signs at the second leaf.
Within Q use +1 on a six-cycle and -1 on its other pairs. Inside colors
can be set blue. This gives C C^T=[[9,-3],[-3,9]] and C K=-T C;
literal graph construction checks all 76 H spines and the forbidden
matching leaf pair. No existence claim for the full caps follows.

The 256 complete 22-vertex sampled lifts cover H block signs +/-, all
four H inside assignments, eight deterministic seeds and I-I blocks
all matching/all red/all blue/mixed. They check **31456** literal matching
spines, including **19456** touching H, **512** H inside spines,
**6216** uniform sums, and **5632** full switched adjacency rows.
The cross-action residual is checked at **4608** entries against actual
red pages, and the Gram residual at **256** entries. In particular,
without assuming validity, the program checks

    (C K+T C)_hi=2 S_hi (R_hi-3),
    (C C^T)_01+3 S_01=2 S_01 (R_01-3).

Thus the action checks do not depend on sampled valid H configurations
occurring by chance. All other signs, blocks and inside colors are
covered universally by the written proof; the lifts sample them.

There are **76** positive partitions of twelve with at most eleven
parts, including nongraphical sequences. Exactly the six written degree
sequences have v+h>=10. All **3375** three-by-six zero-one matrices with
row degree two are inspected: the **90** whose columns are odd all have
column degree one, hence three shared blue leaf pairs. Finally all
**4096** red subsets of the twelve permitted red positions for P4+3K2
retain (W^2)_13=1. These are controls of the complete written cases,
not a global quotient census or a search over all matching signings.

The seven-blue boundary at two entirely matching orbits is also checked:
270 one-P-P-blue cases, 1350 one-Q-Q-blue cases, and
all 40500 row-degree prescribed one-P-Q-red positions. The
1440 retained odd-column cases in that third domain all have
shared blue leaves, as in the written proof. This enlarges necessary
unsigned data and enumerates no global matching signings.

The proof is ordinary unformalized mathematics. The prior support and
six-blue theorem and three-red corollary remain explicit dependencies;
no unrestricted degree theorem or historical classification is used.
The two-row argument and blue-seven conclusion have author checks and
no independent peer-review verdict. The earlier [review1](../book_ramsey_free_involution_review1/REVIEW.md)
and [review4](../book_ramsey_free_involution_review4/REVIEW.md) are credited
for preceding Gram refinements, individual minima and arbitrary-complement
core audits; neither has reviewed this extension.

## 4. Primary context and scope

Primary literature reopened live 2026-10-01:
[Lidicky--McKinley--Pfender--Van Overberghe, Table 1](https://arxiv.org/html/2407.07285v2),
[Radziszowski, DS1.18, Table IXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf),
and [Wesley, Section 3](https://arxiv.org/html/2410.03625v2). The located
interval remains 22<=R(B4,B7)<=23. The known 21-vertex graph was exactly
reproduced earlier in this campaign; that was baseline validation.
The published general flag-algebra upper certificate was not replayed.
The quotient representation is known block-circulant structure, and no
historical-priority claim is made for it or for an exhaustive literature
search. The mathematical increment here is the two-row action, its
conditional eight-blue bound, and the seven-blue theorem at arbitrary
red density.
All denser patterns and equality attainment remain unresolved by it.
