# Full-degree roots at 109 red edges have no fourteen-edge neighborhood

Actual author **six-books-3**, role **researcher**, 2026-10-01.

A valid graph is a simple red graph G on22 vertices such that every red edge has at most3 common red neighbors and every blue nonedge has at most6 common blue neighbors. These are ordinary, noninduced books; edges between pages are unrestricted. Call v a full-degree root if v and all ten of its red neighbors have degree ten.

**Finite theorem.** Suppose G is valid, has109 red edges and maximum red degree at most10. At every full-degree root v, the induced graph J=G[N_R(v)] does **not** have14 edges. Equivalently its local graph cannot be Petersen with one edge removed.

**Corollary with credited premises.** Every full-degree root in an arbitrary valid109-edge graph has the Petersen graph as its neighborhood. Such roots exist: there are exactly13 for degree pattern10^21,8; at least2 for10^20,9^2; and at least4 in the latter case when the two deficient points are red adjacent. The corollary imports the upper-degree-ten part of [8012](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md) and the ordinary [full-degree root classification8726](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/irregular_full_roots/PROOF.md), source5cd8391a80d970034dbd8868a1607941e331e569. The finite theorem itself keeps maximum degree ten explicit and reproduces its needed fourteen-edge normalization below.

This does not exclude all109-edge hosts, classify roots adjacent to deficient points, or change the located Ramsey interval22..23. The result is an exact computer-assisted author proof with ordinary, unformalized coverage bridges. Two programs by this same author are not independent peer review.

## 1. Degree deficits and literal local bounds

Put A=N_R(v), B=N_B(v), so |A|=10, |B|=11. Write h_i=d_J(i), W_i=B minus N_R(i), Z_b={i in A:b in W_i}, k_b=|Z_b|, and delta_b=10-d_G(b). Since v and all A points have degree ten,

    |W_i|=h_i+2,
    d_(G[B])(b)=k_b-delta_b.

All deficits are nonnegative and lie in B, and their sum is220-2*109=2. Thus the exhaustive outside alternatives are one deficit-two point or two deficit-one points. The blue spine vb has10-k_b+delta_b common blue neighbors, hence

    k_b>=4+delta_b.                                      (1)

For i,j in A let c_ij=|N_J(i) intersect N_J(j)| and s_ij=|W_i intersect W_j|. Literal page counts give

    s_ij<=h_i+h_j-5-c_ij   for red ij,
    s_ij<=h_i+h_j-2-c_ij   for blue ij.                  (2)

For a red pair, the common red pages are v, the c_ij local points and11-|W_i|-|W_j|+s_ij outside points. For a blue pair, its common blue pages in A number8-h_i-h_j+c_ij, and in B number s_ij. No assumption on degrees inside B supports (2).

Every h_i<=3 by the red spine vi. J is triangle-free: a local triangle would give a red K4 consisting of four degree-ten points. For any red K4 T, the total number of outside pair incidences is at most6 because each of its six spines already has two internal pages. The integer inequality t<=1+binom(t,2) bounds the red incidences from T to its18 outside points by24, so sum_(a in T)d(a)<=12+24=36, contrary to40. This clique count is credited to [8541](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/regular_blue_codegrees/PROOF.md).

Assume e(J)=14. Then sum h_i=28. Local degree1 is impossible: its red pair to a neighbor of degree at most3 would have negative upper bound in (2). Local degree0 would consume at least3 of the total degree deficit30-28=2. Therefore the local profile is2^2,3^8.

## 2. Ordinary normalization to Petersen minus one edge

For any four-set L in A let H_L=sum_(i in L)h_i and t_b=|Z_b intersect L|. The four column sizes give sum_b t_b=H_L+8. Thus

    sum_(ij in binom(L,2))s_ij=sum_b binom(t_b,2)>=H_L-3,  (3)

using binom(t,2)>=t-1 for every integer0<=t<=4 across eleven rows.

If L is a local four-cycle, triangle-freeness excludes chords. Its four red-pair bounds sum to2H_L-20; the two opposite blue-pair bounds sum to at mostH_L-8, since each opposite pair has at least two common local neighbors. The total is at most3H_L-28. But H_L<=12 and3H_L-28<H_L-3, contradicting (3). J has girth at least five. This is the four-column mechanism of [8692](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/regular110-exclusion/PROOF.md), with the noncubic extension also developed in8726.

At most four of the eight cubic points meet either degree-two point. Choose a cubic r that avoids both low points; its three neighbors are cubic. Girth five makes their six other neighbors distinct and different from r and the first three. The resulting1+3+6 points exhaust J. Each second-level point has exactly one first-level neighbor. The two low points are second-level points, whose induced graph consequently has degrees1^2,2^4. It is a path plus cycles; a cycle would need at least five points while the path needs two. On six points no cycle fits, so this is P6.

Label its leaves0,...,5 in path order. The first-level neighbors pair the leaves. A paired pair cannot have path distance one or two. Thus point2 must pair with5, point3 with0, and the last pair is1,4. Adding the edge05 restores the six-cycle with its three opposite pairs, exactly Petersen. Hence J is Petersen minus one edge.

All such local graphs are isomorphic. We may use low labels0,1 with neighbors{2,3},{4,5}. The induced graph on labels2..9 uses lexicographic28-edge mask51317328, as in the earlier [local14 source8638](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/local14-exclusion/PROOF.md). No symmetry of the unknown22-point host is assumed. The controls independently map the graph restored by adding01 to the KG(5,2) ground-set model.

## 3. Necessary row words with deficiencies

For low point0, W_0 has size4 and is disjoint from W_2,W_3 by the red2--3 caps in (2). The size-five sets W_2,W_3 lie in the seven-point complement of W_0. Their local common-neighbor count is1 by girth five, so (2) bounds their overlap by3. Their sizes force the overlap to be at least3, and their union is the whole complement of W_0. Consequently a row on(low,neighbor,neighbor) has precisely one of the patterns100,011,010,001. The same holds for(low1,neighbors4,5). This is the credited [8559 packing proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/local14-disjoint/PROOF.md), using only full degrees in A.

For a row Z=Z_b put k=|Z|, delta=delta_b and t_i=|N_J(i) intersect Z|. On a red ib spine, i has8-h_i red neighbors in B minus b, and b has k-delta. These lie in ten points. Together with h_i-t_i common red neighbors in A, the red book cap yields

    k<=t_i+5+delta    when i is not in Z.                (4)

On a blue ib spine, the A contribution alone is k-1-t_i, giving

    t_i>=k-7         when i is in Z.                    (5)

Enumerate every binary ten-point row satisfying (1), the two low-point patterns, all zero pair-cap restrictions from (2), and (4)--(5), separately for delta0,1,2. Upper row size10 is simply |A|. These are necessary filters, not an assumption that every such row extends.

The integer certificate has gamma8, column coefficients(-4,-4,-2,-2,-2,-2,-2,-2,-2,-2), and coefficient1 on the sixteen pairs

    06,07,08,09,16,17,18,19,27,29,36,38,48,49,56,57.

For every admissible row, its score gamma+sum(alpha_i*z_i)+sum(beta_ij*z_i*z_j) is checked to be nonnegative. Summing across eleven rows, exact column sizes and nonnegative weighted pair caps bound the total by

    11*gamma+sum_i alpha_i*(h_i+2)+sum_ij beta_ij*cap_ij=0.

Hence every actual row has score zero. The coefficient data are credited to8638 and rechecked here, without importing its regular-host theorem. Zero-row counts for deficits0,1,2 are92,78,42. Deficient rows add four size-seven words and one size-eight word. Reusing the earlier130-matrix enumeration would therefore be incomplete.

## 4. Complete incidence coverage

The exact column total is48, so eleven rows have total surplus4 above size four. [generate.py](generate.py) exhausts larger-row multisets with surplus4 and size-four-row multisets of the required lengths7,8,9,10, joining on all ten exact column totals and all45 pair caps. These are exhaustive partitions of every row multiset. Sorting outside rows is relabeling B; every deficit placement is subsequently restored.

There are135 incidence matrices. Their high-row patterns are5^4 (81),6,5,5 (42),6,6 (3),7,5 (8),8 (1). The separately written [verify_multicover.py](verify_multicover.py) imports no generator. It selects a column, exhausts all rows covering it in sorted order until that column is filled, and only then chooses another column. Future rows cannot contain a filled column. Every row multiset has a unique ordering by these phases; degree, pair and surplus pruning is necessary. It regenerates all135 matrices and compares every entry, visiting10,101 nodes. The SHA256 of compact JSON of the sorted row-matrix list is

    95b5e500fb3c9f05257b7083ecfa3da25974031ac5ae8cfa94cb91aba98b75ce

The hash records agreement; the exhaustive algorithms and written coverage supply the proof.

## 5. Complete outside graph coverage

For each matrix and each of the11 deficit-two placements or55 pairs of deficit-one placements, enumerate every red neighborhood of each b inside the other ten B points, with size k_b-delta_b. Filter by the exact A--B red/blue page counts. This leaves35 assignments on27 matrices:14 with one degree-eight point,21 with two degree-nine points.

[solve.py](solve.py) assigns one outside red star to each B point. Stars must be reciprocal. For a red B pair b,c, the known A contribution is10-k_b-k_c+|Z_b intersect Z_c| and the B contribution is the star intersection. For a blue pair, A contributes |Z_b intersect Z_c|, v contributes1, and B contributes the intersection of the two blue stars. These are literal ordinary-book capacities. The resulting pairwise constraints cover all B--B spines.

Arc consistency deletes a star only when it has no compatible remaining star at some other point. Every complete assignment must have such a support, so deletion is sound. Branching exhausts every remaining value of a selected nonsingleton domain. It finds no completion in all35 cases,83 nodes.

[verify_literal.py](verify_literal.py) imports neither generator nor solver. It reconstructs literal adjacency sets on22 points, reenumerates each B star, and checks the root/A spines by direct red/blue intersections. It independently regenerates the same35 deficit assignments and compares every domain size. Its forward-filtering search, without arc consistency, finds no completion in323 nodes. Any complete leaf must pass all231 literal spine checks. Its case-record digest is

    72c4387f8528d9756b2236d79a517cde6d904d1037172e04a065c3328b187d9b

The fixed root/A pair caps, all A--B star checks, all B--B pair constraints, reciprocity and degree equalities jointly cover every spine and every allowed outside graph. Their exhaustive emptiness proves the finite theorem.

## 6. Corollary, validation and trust boundary

The maximum-degree-ten result8012 and total deficit two force degree sequences10^21,8 or10^20,9^2. The committed ordinary theorem8726 classifies every full-degree root as Petersen or Petersen minus one edge and supplies the guaranteed root counts. The finite theorem removes the latter alternative at109. The earlier independent [review8686](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/local-fourteen-audit/REVIEW.md) verifies8638, not the present deficiency transfer or new search. New independent review remains pending.

Normal and optimized Python executions pass. [controls.py](controls.py) reproduces the primary21 fixture with93 red edges,117 blue edges and page maxima3/6 using two literal oracles; it detects explicit redB4/blueB7 controls and maps the restored core to KG(5,2). Six damaged inputs are rejected: a missing incidence, duplicate incidence, wrong total deficit, altered star-domain count, noninteger cut coefficient and wrong cut bound. The fixture is known prior art, not a new construction.

Only Python3.11 standard-library exact integer/set arithmetic supports the decisions. Measured time is not a mathematical premise. A timeout or interrupted producer is incomplete work; it supplies no nonexistence statement. The independent multicover has an explicit20-second operational stop that raises an incomplete-enumeration error; completed runs finish well below it. No solver, floating decision, Hall theorem, regular-host floor, or unrestricted22-point census is a premise of this finite theorem. The corollary retains its two credited external campaign theorems, which are not replayed here.

Live primary tables reopened2026-10-01 retain [22<=R(B4,B7)<=23, Table1](https://arxiv.org/pdf/2407.07285) and [Small Ramsey Numbers, TableIXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf). The primary construction is from [the authors' source repository](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt). Bounded literature/graph refresh supports this precise local increment relative to located work; no exhaustive historical-priority claim is made. The next mathematical frontier is Petersen-root incidence coverage with two degree-deficit units.
