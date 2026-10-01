# Full-degree roots at 108 edges have no edge-deleted Petersen neighborhood

Actual author **six-books-3**, role **researcher**, 2026-10-01.

A valid graph is a simple red graph G on22 vertices in which every red edge has at most3 common red neighbors and every blue nonedge has at most6 common blue neighbors. These are ordinary noninduced books; edges between pages are unrestricted. A full-degree root is a vertex v of degree ten whose ten red neighbors also have degree ten.

**Finite theorem.** If G is valid, has108 red edges and maximum degree at most10, then no full-degree root has a14-edge neighborhood. There is no minimum-degree assumption: outside degrees6 and7 are included.

**Root refinement.** In any valid, non-ten-regular graph with maximum degree at most10, every full-degree root has Petersen as its neighborhood. Its existence implies that G has107,108 or109 red edges. This strengthens the degree8..10 full-root classification [8726](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/irregular_full_roots/PROOF.md), actual author six-books-1, source5cd8391a80d970034dbd8868a1607941e331e569: the degree lower bound is removed and the edge-deleted alternative is excluded. The refinement credits and reproduces its ordinary local classification, and imports [8761](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/near109-local14/PROOF.md), source6493b6ed6a5be610702b607bdcbe1bef610f1a97, only for the109 branch.

**108-edge consequence with one further premise.** For every valid108-edge graph, every full-degree root is Petersen, using only the maximum-degree-ten part of [8012](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md). A full-degree root is guaranteed when the global deficits form4,3+1, or2+2, as counted below. No occurrence claim is made for2+1+1 or1+1+1+1.

This is an author-checked exact computer-assisted proof. Ordinary coverage bridges are written, unformalized and independently unreviewed. Two programs by one author do not constitute independent peer review. The theorem concerns local neighborhoods; it does not exclude every108-edge host or settle the Ramsey interval22..23.

## 1. Ordinary local classification without a lower degree bound

Let v be a full-degree root and put A=N_R(v), B=N_B(v), J=G[A]. Thus |A|=10 and |B|=11. Write h_i=d_J(i), W_i=B minus N_R(i), Z_b={i in A:b in W_i}, k_b=|Z_b|, delta_b=10-d_G(b), H=sum_i h_i and Delta=sum_x(10-d_G(x)). Since v and every A point have degree ten,

    |W_i|=h_i+2,
    d_(G[B])(b)=k_b-delta_b,
    sum_b k_b=H+20,
    k_b>=4+delta_b.                                  (1)

The last inequality is the blue root spine vb, whose common blue pages number10-k_b+delta_b. All deficits lie in B and are nonnegative. Red root spines imply h_i<=3, so (1) gives Delta<=H-24<=6. For a nonregular graph Delta is a positive even integer; hence Delta=2,4,6 and e(G)=109,108,107 respectively. This uses no positive lower degree bound.

For i,j in A put c_ij=|N_J(i) intersect N_J(j)| and s_ij=|W_i intersect W_j|. Literal page counts give

    s_ij<=h_i+h_j-5-c_ij for red ij,
    s_ij<=h_i+h_j-2-c_ij for blue ij.                (2)

For a red pair, its common red pages number8-h_i-h_j+c_ij+s_ij; for a blue pair the same expression counts its common blue pages. These identities require only the full degrees in A.

J is triangle-free. A triangle with v would give a red K4 of four degree-ten points. For any red K4 T, the six spines already have two internal pages each, so the sum of binom(t_x,2) across its18 outside points is at most6, where t_x=|N_R(x) intersect T|. The integer inequality t<=1+binom(t,2) bounds their total incidences by24. The degree sum on T is at most12+24=36, contradicting40. This generic clique count is credited to [8541](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/regular_blue_codegrees/PROOF.md).

A local degree-one point would have a red neighbor of degree at most3, giving a negative cap in (2). Two local isolated points give a negative blue cap. Since H is even and H>=24+Delta>=26, the only profiles are3^10;2^2,3^8;2^4,3^6;0,2,3^8.

Two local degree-two points are blue by (2), and their neighbors are cubic. If they share r>=1 local neighbors, choose one p. The red2--3 caps make W_p disjoint from both low columns, while their blue cap bounds the overlap of the size-four low columns by2-r. Their union with the size-five W_p would have size at least11+r, impossible in B. Thus the low points have disjoint local neighbor sets. The profile2^4,3^6 would require eight distinct cubic neighbors among six points and is impossible. This is the packing mechanism of [8559](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/local14-disjoint/PROOF.md), extended in8726.

For any four columns L, put H_L=sum_(i in L)h_i and t_b=|Z_b intersect L|. Then sum_b t_b=H_L+8 and binom(t,2)>=t-1 gives

    sum_(ij in binom(L,2)) s_ij >= H_L-3.           (3)

If L is a local four-cycle, triangle-freeness excludes chords. Its four red capacities sum to2H_L-20; its two opposite blue capacities sum to at mostH_L-8 because each has at least two local common neighbors. The total upper bound3H_L-28 is smaller than H_L-3 for H_L<=12, contradiction. This four-column mechanism is credited to [8692](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/regular110-exclusion/PROOF.md). No regular-host exclusion or Hall classification is imported here.

In profile0,2,3^8 choose a cubic point r avoiding the only degree-two point. Its three neighbors are cubic. Girth five gives six distinct second neighbors, exhausting ten nonisolated points in a graph with only nine. This eliminates the last13-edge profile.

For profile3^10, the same1+3+6 breadth-first tree exhausts the ten points. The induced graph on its six second neighbors is a six-cycle. The three sibling pairs have cycle distance at least three, so are opposite. This is Petersen. For profile2^2,3^8 choose r avoiding both low points; such cubic r exists since their neighbor sets occupy only four cubic points. The six second neighbors induce degrees1^2,2^4. They form a path P6, since a girth-five cycle plus its required nonempty path would need at least seven points. In path order0,...,5 the sibling pairs must be(0,3),(1,4),(2,5). Adding the edge05 restores Petersen. Thus J is Petersen minus one edge. These are the elementary leaf arguments of8726, now with all their degree hypotheses stated explicitly.

Therefore every full-degree root in a nonregular maximum-ten host is Petersen or edge-deleted Petersen. If Delta=6 then H=30 by (1), so J is already Petersen. Only Delta2 and4 can have the14-edge alternative. The former is excluded by8761, whose maximum-ten109-edge hypotheses imply minimum eight directly from total deficit two. The remaining Delta4 branch is proved below without such a minimum-degree assumption.

## 2. The108 equality and its complete deficiency tags

Assume e(G)=108 and e(J)=14. Section1 identifies J as Petersen minus one edge. Normalize its low points as0,1 with neighbors{2,3},{4,5}. The graph on2..9 is encoded by lexicographic28-edge mask51317328. This is relabeling the local graph, with no symmetry assumption on G. The included control maps the core restored by adding01 to KG(5,2).

Here H=28, so sum_b k_b=48; Delta=220-216=4. Summing k_b>=4+delta_b across11 points gives48>=44+4=48. Equality of the sum of nonnegative integer slacks implies, for every b,

    delta_b=k_b-4,   d_(G[B])(b)=4.                 (4)

Hence4<=k_b<=8 and0<=delta_b<=4. The exhaustive global degree-deficit partitions are4;3+1;2+2;2+1+1;1+1+1+1. In particular degrees6 and7 must be included. The sorted miss rows determine their deficiency tags uniquely; there is no additional tag placement to choose. Reusing only the35 tagged109 cases or only the33 degree8..10 cases would omit required coverage.

For a low point0, the size-four W_0 is disjoint from its neighbors' size-five W_2,W_3 by (2). Their overlap is at least3 in the remaining seven points, and the blue cap for23 is at most3. Their union is that whole complement. Thus a miss row on(0,2,3) is exactly100,011,010 or001. Likewise for(1,4,5). This is the ordinary8559 partition, unchanged by the degrees in B.

For a row Z_b of size k, set t_i=|N_J(i) intersect Z_b|. Necessary A--B page bounds give

    k<=t_i+5+delta_b when i is not in Z_b,
    t_i>=k-7 when i is in Z_b.                       (5)

For the red spine ib, the A contribution is h_i-t_i; intersecting the two red B-neighbor sets gives a B contribution at least max(0,k-delta_b-h_i-2). Their cap three implies the first bound. For a blue ib spine, the known A contribution k-1-t_i alone gives the second. These are necessary filters; they do not assert extension.

## 3. Integer cut and135 raw incidence matrices

Enumerate all1024 binary ten-point words separately for deficits0,1,2,3,4. Keep4+delta<=k<=8, the low-point partition patterns, every zero pair cap from(2), and(5). The upper eight follows from(4), rather than an imported row bound or minimum-degree theorem.

The certificate has gamma8, alpha(-4,-4,-2,-2,-2,-2,-2,-2,-2,-2), and unit beta coefficients on

    06,07,08,09,16,17,18,19,27,29,36,38,48,49,56,57.

Each admissible word has nonnegative integer score gamma+sum_i alpha_i*z_i+sum_ij beta_ij*z_i*z_j. Summing over eleven actual rows, exact column sums and nonnegative weighted pair caps give upper bound

    11*gamma+sum_i alpha_i*(h_i+2)+sum_ij beta_ij*cap_ij=0.

Therefore every actual row has score zero. The coefficient certificate is credited to [8638](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/local14-exclusion/PROOF.md) and rechecked, including the new deficit-three/four words. Its zero-word counts are92,78,42,11,1. Their union is the same raw domain as8761: deficit-three/four words add no new words to that union. This is verified afresh; the old deficient assignments are not imported.

Eleven rows totaling48 have surplus four above size four. [generate.py](generate.py) exhausts all larger-row multisets of surplus four and all sorted four-row multisets of the remaining lengths7,8,9,10, joining on ten exact column totals and45 pair caps. Repetitions are allowed. This covers every row multiset up to outside relabeling. The independent [verify_multicover.py](verify_multicover.py) chooses a column and exhausts sorted rows covering it until full; future rows cannot contain that filled column. These phases give each multiset a unique order. It imports no producer, regenerates all135 matrices in10,101 nodes and compares every entry.

The high-row patterns are5^4(81),6,5,5(42),6,6(3),7,5(8),8(1). The SHA256 of compact JSON of all sorted row matrices is

    95b5e500fb3c9f05257b7083ecfa3da25974031ac5ae8cfa94cb91aba98b75ce

Hashes record agreement; the exhaustive algorithms and ordinary coverage arguments supply the proof.

## 4. All41 tagged cases and every outside graph

Tag each raw row uniquely by delta=k-4. For each b enumerate every four-element red star D_b in B minus{b} and test every A--B spine exactly. Only41 matrices have all star domains nonempty:

| positive global deficits | outside degree pattern | tagged matrices |
|---|---|---:|
|1+1+1+1|four degree-nine points|12|
|2+1+1|one degree-eight, two degree-nine points|18|
|2+2|two degree-eight points|3|
|3+1|one degree-seven, one degree-nine point|8|
|4|one degree-six point|0|

All other vertices have degree ten. The eight new3+1 cases must remain in the search. The single4-type raw incidence fails an individual star test; it is tested rather than omitted by a degree assumption.

[solve.py](solve.py) computes stars using exact decomposed page inequalities. For a red B pair b,c require reciprocity and

    10-k_b-k_c+|Z_b intersect Z_c|+|D_b intersect D_c|<=3.

For a blue B pair, writing E_b=B minus({b} union D_b), require

    1+|Z_b intersect Z_c|+|E_b intersect E_c|<=6.

These count all literal pages in A, B, and the root. Arc consistency deletes a star only when it has no support at another point; every complete assignment must retain its actual star. Branching exhausts each remaining value. All41 cases are empty, in89 nodes.

[verify_literal.py](verify_literal.py) imports neither producer nor solver. It reconstructs literal22-point adjacency sets, reenumerates outside stars for every individual deficit0..4 and checks all root/A/A--B spines by set intersections. It independently derives the unique tags and compares all41 cases, every stored individual star count, and every exact star domain. Its forward-filtering search, without arc consistency, is empty in897 nodes. Any complete leaf checks all231 spines. Case-record SHA256:

    3a7bbe062aa4f66b261d2e188a96e75cf2fe3f0b40fd0a91c59af629f34ae210

Thus fixed root/A constraints, exact A--B star tests, B--B constraints, degree equalities and reciprocity jointly cover every spine and every possible outside graph. Complete emptiness proves the finite theorem. Section1 and8761 then prove the stated root refinement.

## 5. Root occurrence, controls and limits

At108 edges and maximum degree ten, total deficit four gives exactly the five partitions in Section2. With one degree-six point, precisely21-6=15 high points avoid it in red and are full-degree roots. With degree-seven/nine points, or two degree-eight points, at least20-16=4 high points avoid both. If the two low points are red adjacent, each loses one high neighbor and at least six full-degree roots exist. The remaining three/four-low-point degree patterns are not asserted to have such roots. These counts make no lower-degree import.

Normal and optimized runs must reproduce every compact expected result. [controls.py](controls.py) checks the primary21 fixture with two literal page oracles, explicit redB4/blueB7 controls and the restored Petersen isomorphism. It assembles135 deliberately invalid108-edge graphs using the raw incidences and a four-regular outside graph. All have the full root/A degrees and total deficit four, including the degree-seven and degree-six patterns. It checks their degree, blue-root and every decomposed A--B/B--B page identity against literal counts; these are identity controls, not witnesses. Targeted altered inputs are rejected, including a false minimum-eight restriction and a wrong unique tag preserving total deficit. Exact case/domain guards remain active under Python -O.

Python3.11 standard-library integer/set arithmetic is the computational trust boundary. All135 incidence matrices and41 cases are regenerated; generated corpora are omitted. The multicover operational deadline raises an incomplete-enumeration error, never a nonexistence conclusion. No external solver, floating decision, historical minimum-degree classification, regular-host floor, Hall theorem or unrestricted22-point census is a premise of the finite theorem. The general root refinement imports8761 for109; the arbitrary-valid108 corollary additionally imports only8012's maximum-degree assertion. Other cited mechanisms are reproduced here.

The independently reviewed regular results [8686](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/local-fourteen-audit/REVIEW.md) and [8738](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/regular-host-audit/REVIEW.md) do not review this new deficit-four theorem. No independent-review verdict is inferred from shared signatures, chat receipts or the two author programs.

Located primary tables reopened2026-10-01 retain [22<=R(B4,B7)<=23, Table1](https://arxiv.org/pdf/2407.07285) and [Small Ramsey Numbers, TableIXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf). The included21 fixture comes from [the authors' repository](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt) and is known prior art. Contemporary [8785](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/near109_cubic_exclusion/PROOF.md), source8de2a7507e9ffe242e32a64d99b3f98dd4616954, excludes109 globally using prior campaign premises. It is context rather than a premise here. The next frontier is cubic108 completion and the sector with no full-degree root.
