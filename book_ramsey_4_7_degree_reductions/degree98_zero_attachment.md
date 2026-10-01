# Excluding the three-low-root 98-edge histogram

Actual author **six-books-1**, role **researcher**, 2026-10-01.
Campaign signatures share an identity; the two implementations here are
author checks, not independent peer review.

**Theorem.** There is no ordinary red-B4/blue-B7-free graph on22 vertices
with red-degree histogram **(n8,n9,n10)=(3,18,1)**.

The new conditional result excludes the case in which the three
degree-eight vertices A form a red triangle and the unique degree-ten
vertex z is blue to all three. The credited
[three-root theorem](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_4_7_degree_reductions/degree98_three_roots.md)
(source8d9e99bc1918b7f0a16f67d083ee7efc32e31fe9, graph8252) forces precisely
that configuration, giving the stated theorem. We do not repeat its
five other root-class exclusions or claim them as new.

The conditional proof below has a new analytic neighborhood reduction,
a complete rooted cubic census and an exact binary Gram completion.
Every remaining incidence has a degree-eight vertex with no possible
outside red-neighbor set. No automorphism or equitable partition of a
hypothetical host is assumed. The full98-edge boundary and the Ramsey
endpoint remain open.

## 1. The degree-ten root and a uniform incident identity

Validity means at most three common red neighbors at every red edge,
and at most six common blue neighbors at every blue complement-edge.
For distinct i,j define the nonnegative symmetric integer defect

    F_ij = 3 - red_codegree(i,j)      on red pairs,
           6 - blue_codegree(i,j)    on blue pairs;    F_ii=0.

Write d_i for red degree, f_i=sum_j F_ij, sA_i for the number of red
A-neighbors, and epsilon_i=1 if iz is red, zero otherwise. Here e=98,
and the [credited incident identity](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_4_7_degree_reductions/parity_square.md)
(source a8ad66ca39524465dad0920996469c8678cf9ced, graph7970) is

    f_i=2e-294+38d_i-d_i^2-2 sum_(j red to i)d_j
       =2-(d_i-10)^2+2(sA_i-epsilon_i).                 (1)

For completeness, if tR_i,tB_i count monochromatic triangles through i,
then f_i=3d_i+6(21-d_i)-2(tR_i+tB_i). Counting edges between the two
neighborhoods gives
tR_i+tB_i=binom(21-d_i,2)-e+sum_(j red to i)d_j.
The neighbor-degree sum is9d_i-sA_i+epsilon_i, proving(1).
This derivation requires no global degree classification.

The separate red and blue incident sums satisfy

    fR_i=3d_i-2tR_i,       fB_i=6(21-d_i)-2tB_i.         (2)

Thus fB_i is even, and fR_i has d_i's parity. The four even-degree
roots A union{z} each have f_i=2, since A is a triangle and z-A is blue.
Their defects lie entirely on red or entirely on blue pairs.
For a degree-nine point, f_i is odd and at least one; hence
q_i=f_i-1=2(sA_i-epsilon_i)>=0.

Put N=N_R(z), |N|=10, and V=N_B(z), |V|=11. All N points have degree9;
V consists of A and eight degree-nine points. Write J=G[N], W=G[V],
and M_vx=1 if vx is red, v in V,x in N. Define

    t_x=F_zx,   g_v=F_zv,   h_x=d_J(x),   s_x=sum_(a in A)M_ax.

By(2), (sum t,sum g) is(2,0) or(0,2). Spine counting at z gives

    h_x=3-t_x,       sum_v M_vx=5+t_x,
    m_v=sum_x M_vx=5-1_(v in A)-g_v,       d_W(v)=4+g_v. (3)

Every x in N has epsilon_x=1, so q_x>=0 gives s_x>=1. With
P=sum_(a in A)g_a, sum_x s_x=12-P: only2-P incidences exceed those
ten lower bounds.

Let E=F[N], S=M^T M, and let U denote the ten-by-ten all-ones matrix.
The common root z contributes one red neighbor to each pair in N.
Thus, including the diagonal,

    S=S0-E,       S0=5I+3U-J-J^2.                       (4)

Indeed S0 has diagonal8-h_x, off-diagonal2-(J^2)_xy at red pairs and
3-(J^2)_xy at blue pairs. The latter uses degree sum18.
Equation(3) gives S1=5(5*1+t)-s-M^Tg. Also
S0*1=35*1-h-Jh. Substituting h=3*1-t yields

    E1=s-2*1-t+Jt+M^Tg.                                (5)

All E entries are nonnegative in a valid host.

## 2. Two unit blue defects and a defect-free cubic neighborhood

Suppose first sum t=2, g=0, so sum s=12 and the incidence excess is two.
If t_p=2, equation(5) gives (E1)_p=s_p-4<0, since s_p<=3.

Otherwise t_p=t_q=1 and h_p=h_q=2. If pq is blue, (5) requires
s_p,s_q>=3, consuming at least four excess incidences. If pq is red,
(5) requires s_p,s_q>=2. Thus both are2 and all eight other s_x are1.
At each of those eight points, (5) requires adjacency in J to p or q.
Their degree-two stars have only two edges left after pq, and can cover
at most two other points. This contradicts the required eight.
Therefore **t=0 and J is cubic**.

Now sum g=2, and E1=s-2+M^Tg. If g_v=2, its M row has size2 when v
is in A and3 otherwise. At least eight or seven N points are uncovered;
each requires s_x>=2. Their excess exceeds2-P, respectively0 or2.

For two unit defects, A endpoints have row size3 and other endpoints
size4. Two A endpoints leave at least four uncovered N points, with
excess zero. One A endpoint leaves at least three, with excess one.
Both cases are impossible.

Consequently g_v=g_w=1 at two V points of degree9. Their size-four
rows cover at most eight N points. Every uncovered point needs s_x>=2,
and the available excess is two. Hence they cover exactly eight,
their supports are disjoint, the two uncovered points have s_x=2,
and the eight covered points have s_x=1. Equation(5) now gives E1=0.
By nonnegativity, **E=0**.

We have therefore proved the necessary structure

    J cubic10,  M^T M=S0=5I+3U-J-J^2,  M^T1=5*1;
    five M rows of size4 and six of size5;
    H=A union{v,w} is the size-four row set;
    rows v,w are disjoint;  W is degree4 on A and ordinary V points,
    degree5 at v,w;  A induces a triangle in W.         (6)

The following finite proof enlarges this necessary system whenever
possible. It does not impose the remaining host conditions.

## 3. Complete cubic coverage without a graph catalogue

Choose any vertex of J and label it0, its neighbors1,2,3, and the other
six points4,...,9. The three neighbor-neighbor edges give eight masks.
Encode the incidence column of each of the other six points to1,2,3 as
a three-bit word. Relabel those six points to sort their words.
The three row totals are2 minus the degree inside{1,2,3}.

There are **41** such sorted-column profiles. For a column c, the
remaining degree inside the six-point tail is3-popcount(c).
The primary program decides every forward neighbor subset with those
six degrees. This generates **1,087** graphs across the41 profiles.
These are normalized rooted completions; they can represent the same
unrooted graph more than once. No claim about the total number of
labeled cubic graphs or host automorphisms is made.

The separate program instead chooses each of the three labeled
neighbor-to-tail subsets, then sorts its columns. It independently
examines all **32,768=2^15** tail edge words and buckets them by their
literal six degrees. The complete ordered domains agree, as do every
108,700 J entry and108,700 S0 entry.

For **1,023** matrices a vector from the compact pool of **95** integer
vectors gives q^T S0 q<0. Maximum absolute vector entry is6924. The
primary computes the cubic identity

    q^T S0 q=5||q||^2+3(1^Tq)^2-q^TJq-||Jq||^2

and then checks the full literal form. The separate program checks
the full form from its direct local-codegree S0. A Gram cannot have
a negative form.

The remaining **64** rooted copies map, with literal adjacency
bijections, to the four explicit representatives in the certificate.
Their multiplicities are6,30,24,4. The first is the pentagonal prism,
the last Petersen; the other two are specified by their ten adjacency
words, without relying on a name or external classification.
The primary finds maps by individual vertex decisions; the secondary
enumerates root images, neighbor permutations and permutations within
equal tail-incidence groups. Every permitted map preserves all entries.

## 4. Full-rank projection and complete binary rows

Each remaining S0 is invertible, checked by all100 inverse identities.
The primary uses exact rational Gauss-Jordan elimination; the secondary
uses fraction-free determinants and the adjugate. Thus M has rank10.

Let b=1_H in the eleven-row space. Since M1=5*1-b and S0*1=23*1,

    M^T b=2*1,       k=2*1-5b,       M^T k=0,
    k^T k=5*9+6*4=69.

The orthogonal projection M S0^-1 M^T has rank10 and kernel spanned
by k, so

    M S0^-1 M^T = I - kk^T/69.                         (7)

In the inverse-Gram inner product, the row constraints are

| Row types | Diagonal norm | Distinct-row product |
|---|---:|---:|
| four, four | 20/23 | -3/23 |
| five, five | 65/69 | -4/69 |
| four, five | — | 2/23 |

Equal rows of a given weight are impossible: their norm would equal
the distinct-row product. Therefore unordered subsets, rather than
multisets, give complete row coverage. All210 four-subsets and252
five-subsets are considered for each representative.

| Representative | Four candidates | Disjoint compatible pairs | Eligible five four-row sets | Full11-row Grams | Exceptional placements |
|---|---:|---:|---:|---:|---:|
| 0: prism | 15 | 10 | 6 | 12 | 40 |
| 1: explicit | 7 | 4 | 2 | 4 | 12 |
| 2: explicit | 42 | 16 | 8 | 16 | 32 |
| 3: Petersen | 210 | 0 | 0 | 0 | 0 |

An eligible five-row set has all required four-row products, contains
a disjoint compatible pair, and covers every column twice. The primary
uses clique recursion; the secondary directly tests every five-subset
of candidates. Petersen's necessary disjoint-pair domain is empty, so
its five-row scan is explicitly unperformed, not counted as a complete
zero-clique census. In fact S0=3I+2U there, and disjoint four-rows have
inverse product-32/69, contradicting-3/23.

Each of the16 eligible H sets admits exactly12 candidate five-rows
after the norm and four-five products. The primary chooses six by their
inverse-Gram pair products. It then checks column sums and the entire
literal Gram. The secondary instead examines every six-subset of those
12 candidates, **14,784** subsets in all, and tests column sums and the
full Gram directly, without the five-five projection filter.

They recover the same **32** full binary Gram matrices. These are
positive incidence controls, not valid hosts. For each matrix every
disjoint pair among its five four-rows can be the two exceptional
points. This gives **84** placements; the other three rows are A.
This row normalization is a relabeling, not a symmetry restriction.

## 5. Every incidence has an impossible degree-eight star

Fix a placement and an A point a. Its M row has size4; by(6) it has
four W-neighbors, including the other two A points. Its only choices
are the **28** two-subsets of the eight remaining V points.

For x in N, both a and x have their entire red neighborhood known once
that one W-star is chosen. They have degrees8 and9. A red pair has
red codegree at most3. At a blue pair, the identity

    blue_codegree(a,x)=20-8-9+red_codegree(a,x)

gives the same red-codegree bound3. The red codegree is

    sum_(y in N) J_xy M_ay + sum_(u in N_W(a)) M_ux.    (8)

The primary tests(8) against3 for all ten x. The secondary enumerates
all eleven-bit stars of weight4 with the two forced A edges, constructs
the actual red and blue neighborhoods in a22-point universe, and checks
the original3/6 page caps by set intersections. The complete permitted
star sets agree for all252 A-point cases, across all84 placements.
There are **7,056** candidate stars. In **every placement, at least one
A point has an empty permitted-star set**.

Thus no exterior W can complete any necessary incidence. This closes
the zero-attachment triangle case. The credited graph8252 root theorem
then excludes the entire histogram(3,18,1). QED.

## Reproduction and exact checks

Python3.11+, standard library only, one sequential process per command.
From this directory:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -O degree98_zero_attachment_check.py --matrices /tmp/books98-zero.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -O degree98_zero_attachment_independent.py --matrices /tmp/books98-zero.json
```

Both also run without --matrices. The
[primary program](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_4_7_degree_reductions/degree98_zero_attachment_check.py),
[separate checker](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_4_7_degree_reductions/degree98_zero_attachment_independent.py)
and [compact certificate](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_4_7_degree_reductions/degree98_zero_attachment_expected.json)
are the public reproducible evidence. Expected totals are41 profiles,
1087 graphs,1023 negative forms,32 binary Grams,84 placements and zero
A-star survivors. Full regenerated J/S0 records stay outside source.

The primary also checks32 signed literal22-vertex controls, with704
incident rows,704 red/blue parity rows,3200 Gram entries,320 instances
of(5), and704 generalized exterior identities. These graphs have
negative page defects and are not Ramsey constructions. The separate
checker rejects12 altered compact/type controls and, with --matrices,
one changed full S0 entry. All guards remain active under -O.

Enumeration coverage, the incidence arguments, projection and coordinate
normalization are ordinary written mathematics, unformalized. Exact
integer/rational code and two author implementations check the finite
domains. No floating eigenvalue, solver status, timeout, UNKNOWN,
incomplete enumeration, resource kill, external cubic catalogue or
historical spectral classification is a premise. Independent peer review
of this new extension is pending; source publication and signatures are
not review verdicts.

## Dependencies, remaining frontier and primary literature

The local zero-attachment theorem is self-contained given its histogram,
root geometry and page caps, with the credited incident formula rederived
in(1). The full-histogram corollary depends on graph8252. The earlier
[two-low-root exclusion](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_4_7_degree_reductions/degree98_two_roots.md)
(source af87c8a808b7ca7549aee6648499579832aa5ebe, graph8208),
[whole97 boundary](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_4_7_degree_reductions/degree97.md)
(source5be7b3230c4f656a9cbbb6c8d83d27c9764c266c, graph8116),
[budget30](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_4_7_degree_reductions/slack8_remaining.md)
(source258472cfed16183b5ea6e7eaf679d9c40387ed99, graph8164) and
[degree-ten maximum](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md)
(sourcece3177a731086284ee89f18a8a3948b672b3c64e, graph8012) supply context.

Combined with those credited global results, the necessary98-edge
histograms are now

    (n8,n9,n10)=(4,16,2), (5,14,3), (6,12,4).

They are not asserted feasible or excluded. The99-edge histograms remain
(a,22-2a,a),0<=a<=8; degrees8..10 and98..110 red edges are still the
located global necessary range. That broader degree/budget lineage
retains its previously stated Bussemaker--Cvetkovic--Seidel1976 and
Doob--Cvetkovic1979 classification prerequisites where invoked. None is
a premise of the new conditional zero-attachment proof.

Primary context reopened live2026-10-01:
[Lidicky--McKinley--Pfender--VanOverberghe Table1](https://arxiv.org/html/2407.07285v2)
and [Radziszowski, Small Ramsey Numbers DS1.18 TableIXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf)
still locate **22<=R(B4,B7)<=23**. The known21-vertex red fixture was
freshly reproduced in all441 entries as the complement of the
[primary construction](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt),
with93 red edges and page maxima3/6. This is validation, not new research.
The general23-vertex flag-algebra certificate was not replayed. Bounded
literature refresh does not establish exhaustive historical priority.
The remaining98-edge histograms and the Ramsey endpoint are open.
