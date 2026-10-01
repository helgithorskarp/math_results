# Local-fourteen exclusion in regular Book Ramsey candidates

Actual author **six-books-3**, role **researcher**, 2026-10-01.

All graphs are simple. A red edge is an edge of G; a blue edge is a
nonedge. Validity means red-edge common-red counts <=3 and blue-edge
common-blue counts <=6. Books are ordinary subgraphs, with no restriction
on edges between pages.

**Conditional local theorem.** A valid ten-regular graph G on 22
vertices cannot have a root v whose red neighborhood J has degree
sequence 2^2,3^8. The proof below uses the credited nine-core theorem
and triangle-freeness. It checks every possible outside-degree pattern
directly, without the old cap-six or two-six finite computations.

**Global regular corollary.** Every red edge in a valid ten-regular
G has exactly three common red neighbors. Every red neighborhood is
therefore a triangle-free cubic graph on ten points with fifteen edges;
G has 110 red edges and 110 red triangles. In particular the earlier
red-codegree-two defect graph D is empty.

## Exact dependency split

The credited [packing and nine-core result](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/local14-disjoint/PROOF.md),
graph 8559, source 16d5b8169e841574508035993da91cecfaf5d422,
supplies the normalization, the forced partitions, and the complete
nine triangle-free necessary local cores. It does not claim these
cores extend to a host. The analytic
[ten-regular triangle-free theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/regular_blue_codegrees/PROOF.md),
six-books-1, graph 8541, source 53fa7ea66251df9d255b7d0ff9d0ff309580d42a,
supplies triangle-freeness: a triangle in J would give a red K4.

The local theorem needs neither the earlier positive-codegree result
nor the neighborhood floor, since its degree sequence is explicit.
For the global consequence, the credited
[positive-codegree theorem 8120](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_regular110_positive_codegrees/PROOF.md)
and [floor theorem 8218](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_regular110_neighborhood_floor14/PROOF.md)
give local degrees 2^2,3^8 or 3^10 at every root. The former is now
excluded, so all red-edge codegrees are three. The triangle count is
110*3/3=110. Applying this to every 110-red-edge candidate additionally
uses the credited
[maximum-degree-ten theorem 8012](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md):
sum degrees220 and all degrees<=10 force ten-regularity.

The old [outside cap-six result 8280](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_regular110_local14_outside_cap6/PROOF.md)
and [two-six result 8332](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_regular110_local14_two6_exclusion/PROOF.md)
are prior partial exclusions. Their patterns are independently covered
here under the new nine-core reduction; their expensive computations
are not imported or used as premises. No historical-priority claim is made.

## Miss incidence and complete row coverage

Put A=N_R(v), B=N_B(v), with sizes ten and eleven. For i in A let
h_i=d_J(i), W_i=B minus N_R(i). For b in B let Z_b=A minus N_R(b),
the miss row, with indicator z_b. Ten-regularity gives

    |W_i|=h_i+2,  |Z_b|=d_(G[B])(b),  sum_b |Z_b|=48.

The blue spine vb has10-|Z_b| common blue neighbors, so |Z_b|>=4.
Eleven four-rows already contribute44; the surplus is four. Every row
is <=8 and the complete possibilities are

    8,4^10;  7,5,4^9;  6,6,4^9;  6,5,5,4^8;  5^4,4^7.

Distinct outside vertices may have identical rows. All enumerations
allow these multiplicities.

Let c_ij=|N_J(i) intersect N_J(j)|. Literal page counting gives
S=M^T M, diagonal t_i=h_i+2, and off-diagonal upper bounds

    S_ij <= U_ij=h_i+h_j-5-c_ij  on red pairs,
    S_ij <= U_ij=h_i+h_j-2-c_ij  on blue pairs.              (1)

The prior packing theorem permits labels0,1 for the low points with
N_J(0)={2,3}, N_J(1)={4,5}. For each low x and its neighbors p,q,
W_x, W_p intersect W_q, W_p minus W_q, W_q minus W_p partition B
with sizes4,3,2,2. Thus on each triple (0,2,3) and (1,4,5), every
row has exactly one of the four patterns100,011,010,001. This is a
necessary equality property, not a symmetry assumption about G.

For a row Z of size k and i outside Z, the red A--b spine has
|N_J(i) intersect(A minus Z)| A-pages and at least k-h_i-2 B-pages.
Hence

    k <= h_i+5-|N_J(i) intersect(A minus Z)|.              (2)

For i in Z, its blue A-pages alone give

    |N_J(i) intersect Z| >= k-7.                          (3)

A row must also avoid every pair with U_ij=0. We retain exactly all
words satisfying these necessary filters, discarding other host tests.
For each of the nine cores there are 200 row types: 79 of size 4,
76 of size 5,39 of size 6,6 of size 7, and none of size 8. The size-eight
failure also has a short proof: the partitions force Z to be all
eight cubic points; a low red A--b spine then has at least four B-pages.

The credited F masks are 30083408,51316320,51317328,54986080,54987088,
55740996,126126276,126158020,126158146. Mask bits are the lexicographic
unordered pairs of eight cubic labels0..7, mapped to A labels2..9.
The alignment and isomorphism coverage are precisely those of 8559.

## Integer cuts and the sole zero face

Each record in [cuts.json](cuts.json) supplies integer alpha_i, gamma
and nonnegative pair weights beta_ij. Define the row score

    f(z)=gamma+sum_i alpha_i z_i+sum_(i<j) beta_ij z_i z_j.

Every retained row is checked to have f(z)>=0. In any host,

    0 <= sum_b f(z_b)
      = 11 gamma+sum_i alpha_i t_i+sum beta_ij S_ij
      <= V=11 gamma+sum_i alpha_i t_i+sum beta_ij U_ij.    (4)

The cuts have V values -1,-1,0,-1,-1,-1,-5,-4,-1 in the listed core
order. They therefore exclude eight cores with elementary integer
counting. Several are the four-column inequality
1-|Z intersect T|+binom(|Z intersect T|,2)>=0; the more general
coefficients are checked directly. The largest absolute coefficient
in the nine records is eight.

Only F mask51317328 has V=0. Equality in(4) forces every row to have
score zero, and S_ij=U_ij whenever beta_ij>0. There are exactly 92
zero-score row types: 19 four-rows,36 five,31 six,6 seven. These
restrictions are consequences of a single exact inequality, rather
than assumptions on the unknown incidence matrix.

## Complete integer incidences and outside obstruction

The remaining four-row multisets and high-row multisets are generated
with full repetition, capped by the ten column counts and all 45 pair
bounds. They are joined on complementary column counts and then checked
against every pair bound. The complete counts are:

| High-row sizes | Capped high multisets | Complete 11-row matrices |
|---|---:|---:|
|7,5|32|4|
|6,6|27|3|
|6,5,5|814|42|
|5,5,5,5|1935|81|

There are 5884 admissible seven-four multisets,1740 eight-four multisets
and286 nine-four multisets. The 130 full matrices, ordered by their
sorted row words, are in [incidences.json](incidences.json). Their digest
is7e9c728b3c4e2fb0ad768e43f5a2aaffb543a4036b2e727f3ec14e652cfdb194.
Row permutation merely relabels B; it does not discard possible
outside graphs, including graphs without any automorphism.

For each matrix select the certified row b. Its red degree inside B
must equal k=|Z_b|. Enumerate every k-subset C of B minus{b}. For
every i in A, the hypothetical A--b spine has these exact page counts:

    red, i outside Z_b:
      |N_J(i) intersect(A minus Z_b)| + #{c in C : i outside Z_c};

    blue, i in Z_b:
      |Z_b minus({i} union N_J(i))|
      + #{c in B minus({b} union C) : i in Z_c}.           (5)

The root is red to i and blue to b, so contributes no common page.
Both full neighborhoods relevant to(5) are known; edges between other
B vertices are immaterial. Every tested C violates a red cap3 or blue
cap6. The selected rows give **29,166** possible stars in total.
No B--B spine check is needed. Every incidence matrix therefore fails
to extend, proving the conditional local theorem.

## Two exact algorithms and trust boundary

[generate.py](generate.py) scans all 1024 row words, decides high rows
as a nondecreasing sequence with surplus four, decides four rows as
nondecreasing sequences with prescribed length, joins them by column
counts, and checks every pair bound. Induction on sequence length shows
it includes every multiset once. Its only pruning is a nonnegative
column or pair capacity already exceeded. It enumerates red stars.

[verify.py](verify.py) imports no generator. It constructs rows by
the two four-state triples and all 16 subsets of the remaining four
points; local blue pages and red intersection lower bounds give the
filters directly. It derives U from literal spine-page baselines.
Each integer cut is checked on its entire row set.

Its incidence reconstruction uses the ten column equations, sixteen
saturated pair equations from positive beta, and the row-count equation.
The resulting27-by19 four-row system has rank 17. Exact rational row
operations expose two free multiplicities, at row words643,771; they
are bounded by the residual column counts, at most five. Every choice
in these finite ranges determines the remaining17 counts uniquely.
The checker verifies the row-operation transformation identity exactly,
with common denominator four, rejects negative or noninteger counts,
and checks all remaining pair bounds. It explicitly covers every high
pattern by products and combinations with repetition: 103609 raw choices.
This differs from the generator's multiset join. The complete130
matrices agree entrywise, not just by aggregate count or digest.

Finally the checker visits all 1024 binary blue-star words, retains each
required weight, reconstructs full 22-point neighbor masks, and counts
ordinary pages by bit intersections. All 29,166 stars fail. Six controls
reject altered constants, bounds, weights, repeated weighted pairs,
a missing incidence record and a falsely declared empty star. The
published 21-point matrix also reproduces 93 red edges and page maxima 3/6.

Python integers and Fraction arithmetic are exact. HiGHS was used only
to discover cuts; [discover.py](discover.py) reproduces them, with
integer verification after rational reconstruction. No floating solver
verdict, MILP soundness, incomplete search, timeout or external raw
corpus is a proof premise. The old nine-core census and global floor
remain attributed mathematical dependencies. Both new algorithms share
this author. Written counting, normalization and completeness bridges
are unformalized; independent review of this new exclusion is pending.

## Primary context

Primary sources reopened 2026-10-01 give
[22<=R(B4,B7)<=23, Table1](https://arxiv.org/pdf/2407.07285) and
[Small Ramsey Numbers, TableIXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf).
The [primary 21 matrix](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
is included verbatim as primary 21.txt; zeros are red. Baseline
reproduction validates the decoder, not novelty. The primary upper
flag-algebra certificate was not replayed. The unrestricted endpoint,
all irregular22-point candidates and existence of a regular candidate
remain unresolved.
