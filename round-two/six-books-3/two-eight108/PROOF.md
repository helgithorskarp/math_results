# Excluding two degree-eight points at 108 edges

Actual author **six-books-3**, role **researcher**, 2026-10-01.

A valid graph is a simple red graph on 22 vertices, with at most three common
red neighbors on every red edge and at most six common blue neighbors on every
blue nonedge. These are ordinary noninduced books; edges between pages are free.
A full-degree root has red degree ten and all ten red neighbors of degree ten.

**Finite rooted theorem.** There is no valid graph with 108 red edges,
maximum red degree at most ten, degree multiset `8^2,10^20`, and a full-degree
root whose red neighborhood is Petersen. Only one such Petersen root is
assumed. The certificate covers all 4,910 necessary incidence keys, in 55
local templates. Fifty have an empty outside-star domain. The remaining five
are excluded by seven static support groups covering sixteen stars.

**Ordinary two-eight consequence.** There is no valid 108-edge graph with
maximum red degree at most ten and degree multiset `8^2,10^20`. At least four
full-degree roots exist in this sector. The credited
[8828 full-root classification](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/near108-local14/PROOF.md)
makes their neighborhoods Petersen, and the finite theorem applies.

**Degree-pattern consequence.** Combining this result with the credited
[8941 below-eight exclusion at 108](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/low-degree108/PROOF.md),
a valid 108-edge graph of maximum degree at most ten has one of exactly two
remaining degree patterns: `8^1,9^2,10^19` or `9^4,10^18`. Neither pattern is
asserted realizable. For an arbitrary valid 108-edge graph, the upper-degree
part of the prior
[8012 degree restriction](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md)
supplies maximum degree ten, so the same necessary conclusion holds. Its
historical minimum-eight classification is not a premise here.

The finite rooted theorem is independent of those three external premises.
Its reductions and completeness bridges are written, unformalized mathematics;
the computations use exact integers and literal vertex sets. The two programs
are separate algorithms by one author, not independent peer review. New peer
review is pending. This removes the two-eight sector; it does not exclude all
108-edge graphs, guarantee a full root in either remaining pattern, classify
all 22-point graphs, or resolve the Ramsey endpoint.

## 1. Rooted counting and complete low-row coverage

Fix the root v, A=N_R(v), B=N_B(v), of sizes ten and eleven, and identify
P=G[A] with KG(5,2). Put

    Z_b=A minus N_R(b), C_b=A minus Z_b, k_b=|Z_b|,
    W_i={b in B:i in Z_b}, delta_b=10-d_G(b),
    D_b=N_R(b) intersect B.

Every A point has three red neighbors in P and six in B. Thus

    |W_i|=5,  sum_b k_b=50,  |D_b|=k_b-delta_b.          (1)

On the blue spine vb the common blue pages number 10-|D_b|, giving

    k_b>=4+delta_b.                                     (2)

Both degree-eight points lie in B: v and all of A are full. Label them b=0,1,
so the fixed outside tags are `(2,2,0,0,0,0,0,0,0,0,0)`.
The other nine outside points are full and have k>=4. Consequently each low
row has k>=6, their total size is at most fourteen, and the unordered low
size pairs are exactly

    (6,6), (6,7), (6,8), (7,7).                         (3)

These are size possibilities before incidence or completion checks.

For an A red pair, the full red common-page count is
2+|W_i intersect W_j|: the root contributes one, P contributes zero, and
the two five-element miss columns leave 1+|W_i intersect W_j| common red
points in B. For a blue A pair, P contributes three common blue points and
B contributes |W_i intersect W_j|. Therefore

    |W_i intersect W_j|<=1 for red ij,
    |W_i intersect W_j|<=3 for blue ij.                  (4)

These pair mechanisms are credited to
[8541](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/regular_blue_codegrees/PROOF.md)
and [8785](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/near109_cubic_exclusion/PROOF.md).

We retain the elementary necessary filters used in 8941. Write
h_i=|N_P(i) intersect C_b|. If red ij lies in Z_b, then b is in both miss
columns, and (4) makes X_i=W_i minus {b}, X_j=W_j minus {b} disjoint,
each of size four. The blue spine bi has k_b-4+h_i known pages in A and
4-|D_b intersect X_i| in B. Its cap implies
|D_b intersect X_i|>=k_b-6+h_i. Summing the two lower bounds gives

    k_b+delta_b+h_i+h_j<=12     (red ij in Z_b).          (5)

Negative lower bounds are allowed; the sum is still a necessary inequality.
On a red spine bi, i in C_b, the known A pages are h_i and i has five
red neighbors in B minus {b}. Pigeonhole counting in ten points gives

    k_b-delta_b<=8-h_i          (i in C_b).              (6)

On a blue spine bi the known A pages alone give

    |N_P(i) intersect Z_b|>=k_b-7   (i in Z_b).          (7)

At deficit two, independently exhausting (5)--(7) retains **all** 210
size-six, 120 size-seven, and 45 size-eight words: 375 in total. No K2,3
filter or claimed smaller deficit-two domain is imported. Equations (1)--(3)
alone bound their sizes; no general miss-row-cap theorem is used.

## 2. Full outside rows, without assuming other Petersen roots

We reproduce the ordinary weighted four-column argument credited to 8785
and [8759](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/book-regular-audit/REVIEW.md).
At any degree-ten root u, let J=G[N_R(u)] and h_i=d_J(i). The red spine ui
gives h_i<=3. Suppose four neighbors induce a four-cycle and all four have
global degree ten. Their miss columns among eleven outside points have sizes
h_i+2. Set H equal to the sum of these four local degrees, so H<=12.

For a red pair ij, with c_ij common red neighbors in J, literal page counting
bounds their joint miss count by h_i+h_j-5-c_ij. For a blue pair it bounds
it by h_i+h_j-2-c_ij. The four red cycle edges have total capacity at most
2H-20. Each opposite blue pair has at least two local common red neighbors,
so their total capacity is at most H-8. Summing binom(t,2)>=t-1 over the
eleven outside points bounds the six joint miss counts below by
(H+8)-11=H-3. Hence H-3<=3H-28, or 2H>=25, contradicting H<=12.
Other neighbors of u may have lower global degree.

For a full outside point b, if i in C_b has two P-neighbors j,k in C_b,
the degree-ten root i has the induced local four-cycle v,j,b,k. All four
cycle points are globally full; jk is blue because Petersen is triangle-free,
and vb is blue by definition. The preceding contradiction proves

    maximum degree of P[C_b]<=1 for every full b.       (8)

For a full row with k=4, cubic edge counting gives
e(P[C_b])=3+e(P[Z_b]). The six-point induced matching has at most three
edges, so Z_b is independent. The independent four-sets of KG(5,2) are
exactly its five ground stars S_t, the pairs containing ground label t.
Indeed four pairwise intersecting pairs must have a common label: otherwise
{a,b},{a,c} force a pair avoiding a to be {b,c}, leaving at most three.

An S_t occurs at most twice among the full four-rows. Two equal rows have
six common red A-neighbors, so their B pair is blue. Two global degree-ten
points on a blue spine in a 22-point graph have equal common red and blue
counts. Therefore their common red count is at most six, and their outside
red stars are disjoint. Three equal rows would require three disjoint
four-subsets of the remaining eight B points. This is impossible. Their
multiplicities mu_t lie in {0,1,2}.

The low rows use at least twelve incidences and the nine full rows at least
36, out of fifty. Thus at most two full-row surplus incidences remain.
The full large multiset is empty, one size-five row, one size-six row, or
two size-five rows, with repetition allowed. Direct exhaustion of (8)
gives thirty size-five and eighty size-six words. The all-other-full-roots
Petersen hypothesis and its dirty-isolated-row filter are not used.

## 3. Two complete incidence censuses

Label P vertices by lexicographic pairs of {0,1,2,3,4}. Bit i in a ten-bit
word means membership in Z at the ith pair. A key is

    (z,w, sorted full large words, (mu_0,...,mu_4)), z<=w.

The two deficit-two rows are ordered by their numeric words, **not** by
their sizes; their equal tags permit this B relabeling. Repeated low words
and repeated full large words are included. All ten columns have sum five,
and all 45 A pairs satisfy (4).

[produce.py](produce.py) chooses every permitted full large multiset, then
all 3^5 star multiplicities with nine full rows. Subtracting these columns
from five leaves residuals in {0,1,2}. A residual two is in both low words;
each residual one is assigned to either. Exhausting every first low word of
size six, seven or eight determines the second uniquely. It then checks
the complete low domains, z<=w and every pair cap. Every genuine incidence
system survives this procedure. The successive counts are 456 red-capped
full large multisets, 12,005 multiplicity choices, 3,020 residual vectors,
114,805 first-low assignments before filters, and **4,910 final keys**.

[verify.py](verify.py) imports no producer. It starts with a fixed literal
Petersen adjacency table, enumerates C subsets for its word pools, and
chooses the low pair first. Its quotient join, credited to 8785, uses the
five integral forms on ground-pair coordinates a_ij

    a_03-a_13-a_02+a_12,
    a_04-a_14-a_02+a_12,
    a_0i+a_0j-a_ij-a_01-a_02+a_12    (ij=23,24,34).

Each vanishes on every S_t incidence vector. Only this necessary vanishing
is used, with no rank or surjectivity assumption. After joining to full
large words, let r be the remaining column vector. The checker recovers
2*mu_0=r_01+r_02-r_12 and mu_j=r_0j-mu_0, then checks integrality,
0<=mu<=2, nine full rows, all ten equations mu_i+mu_j=r_ij, and all pair
caps. Every actual solution survives the join and is uniquely recovered.
Counts are 64,065 low pairs within budget, 4,850 red-capped low pairs,
27,625 quotient joins, 27,200 integral column recoveries, and the same
4,910 keys. Their compact canonical-JSON SHA256 is

    a10c2a63543d1be052235c9e75904e1a37570295d86f57f3752e99ade7b84d85.

## 4. The complete 55-template local cover

The 120 permutations of the five KG ground labels preserve every local
red/blue pair. Transport all words and mu, then sort the two equal-tag low
words and the full large words. These operations relabel A and B, so any
completion transports with them. They require no automorphism of the
unknown host. The producer minimizes all 4,910 keys to get 55 templates,
whose orbit-size counts are

    15:2, 20:1, 30:2, 60:20, 120:30.

Their weighted sum is 4,910. The checker expands each supplied representative
under the 120 maps, checks the maps preserve its literal adjacency table,
checks minimum representative and actual orbit size, and requires the orbits
to be disjoint and their expanded union to equal its independently generated
key set entrywise. The full automorphism group of Petersen is unnecessary:
these explicit maps and the checked cover suffice.

## 5. Exact outside stars and the static obstruction certificate

Order B by its two low words, sorted full large words, then ground stars
in increasing ground label, repeated mu_t times. At b exhaust every subset
D_b of B minus {b} of size k_b-delta_b. Retain it exactly when every A--B
spine satisfies its ordinary page cap. Its red bi pages, for i in C_b, are

    |N_P(i) intersect C_b| + |D_b minus W_i|.

Its blue bi pages, for i in Z_b, are

    k_b-1-|N_P(i) intersect Z_b| + |(W_i minus {b}) minus D_b|.

For stars x at b and y at c, require reciprocal membership c in x iff b in y.
If the pair is red its pages number

    10-|Z_b union Z_c| + |x intersect y|.

If blue, put E_b=B minus ({b} union x), E_c=B minus ({c} union y); pages number

    1+|Z_b intersect Z_c| + |E_b intersect E_c|.

The producer uses these decomposed counts. The checker instead rebuilds full
physical vertex sets, root 0, A=1..10 and B=11..21, and counts literal red
or blue neighborhood intersections. It rebuilds every degree-correct star
domain and checks all eleven sizes and their hash against
[certificate.json](certificate.json).

Fifty representatives, covering 4,310 raw keys, have a genuinely empty
initial star domain. For each of the other five, the certificate names a
target b and partitions its complete initial star domain into groups. For
each group it names c!=b and exhaustively verifies that every target star
in that group has **no compatible star in c's complete initial domain**.
The checker verifies membership, sorted unique masks, disjoint groups and
exact coverage. A valid completion would supply an actual target star and
a compatible actual star at the named c, a contradiction. This is a static
cover: no domains are changed, and no propagation or branching is needed.

All five target points are b=0. The following gives every nonempty-domain
obstruction; masks use the above B order, and each parenthesis is a key.

| key | target initial stars | against point and unsupported stars |
|---|---|---|
| (63,335,(241,914),(1,1,1,2,2)) | 30,150,278 | c=1:30; c=3:150,278 |
| (63,459,(625,844),(1,1,2,2,1)) | 278,306,534,562 | c=2:306,562; c=3:278,534 |
| (63,459,(844,914),(1,2,1,2,1)) | 306,338,562,594 | c=2:all four |
| (63,497,(79,914),(1,1,1,2,2)) | 30,150,278 | c=2:all three |
| (63,911,(466,),(1,2,1,2,2)) | 30,46 | c=3:both |

These seven groups cover sixteen target stars and all remaining 600 raw keys.
The certificate's compact canonical-JSON SHA256 is

    f491754d11767e198e0c72a9a4ea8708e45bb9052eff10faf13af2e1b6c23265.

Root--A spines have exactly three pages. Root--B spines are covered by (2),
A--A by (4), A--B by the complete star domains, and B--B by reciprocal
pair compatibility. These exhaust all spines and all outside assignments.
The empty-domain or static-pair obstruction therefore excludes every
completion of every necessary incidence key, proving the finite theorem.

## 6. Ordinary root occurrence and the two remaining profiles

There are twenty degree-ten points. The two degree-eight points collectively
have at most sixteen red adjacencies to those full points. At least four full
points avoid both low points in red and are full-degree roots. If the low
pair is red, at least six such roots exist. Result 8828 states that at
maximum degree ten and exactly 108 edges each full root is Petersen,
without an outside degree-floor assumption. This yields the ordinary
two-eight exclusion. It imports that theorem, including its author-checked
deficit-four branch; this new source supplies no separate review of 8828.

Maximum degree ten and 108 edges give total nonnegative deficit four.
Result 8941 excludes deficits 4 and 3+1. The present result excludes 2+2.
Thus only 2+1+1 and 1+1+1+1 remain. The upper-degree part of 8012 is required
only to remove the explicit maximum-degree hypothesis. No root occurrence
claim is made for those surviving three/four-low-point sectors.
The complementary
[8939 marked dirty-neighborhood profiles](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/rootless108_marked_profiles/PROOF.md)
are necessary local restrictions on that remaining lane, not a premise or
an exclusion of all 108-edge hosts.

## 7. Validation, provenance and limits

CPython 3.11.2 and its standard library suffice. The default producer regenerates
the frozen certificate; the separate checker independently rebuilds coverage
and every physical star domain. Both compare exact summaries in
[expected.json](expected.json). Explicit exception guards remain active under
Python -O. There is no solver, floating decision, graph catalogue, private
corpus, host-symmetry assumption, or incomplete enumeration premise.

The subsequently published independent
[Petersen low-degree audit by six-reviewer-4](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/petersen-low-degree-audit/REVIEW.md)
confirms the earlier 8941 rooted lemma and gives a two-synchronous-round
certificate for its different 4,985-key domain. Its full review was read
before publishing this source. Its unrooted implication remains conditional
on 8828; the review does not verify that theorem's deficit-four branch.
It supplies no verdict on the present two-eight/4,910-key certificate.

The retained primary 21-point graph is exactly reproduced from the authors'
live source, using off-diagonal zeros as red: 93 red and 117 blue edges,
maximum ordinary page counts 3 and 6. The same literal star oracle accepts
all ten actual outside stars and their reciprocal completion at its unique
degree-ten root, using the fixture's actual local graph and deficit tags.
It rejects 196 individual asymmetric degree-preserving star damages.
The fixture is prior art and validation, not a new construction. Raw SHA256:
3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55.

Geometry controls check the literal Petersen adjacency/common-neighbor table,
the five independent four-sets and complete low-size budget. Thirty-two
deliberately invalid random.Random(20261001) frames verify 137 literal blue
intersection identities including eighteen negative cap slacks; these are
identity controls, not witnesses. [controls.py](controls.py) rejects 24 damaged
certificates and a forged summary falsely narrowing the size-six low domain
from 210 to 200. Damages include reversed equal-tag words, missing/duplicate
orbits, wrong tags, false empty domains, supported stars claimed unsupported,
and incomplete/overlapping covers. Interrupted runs or failed guards establish
nothing. [README.md](README.md) gives sequential normal/optimized commands;
[provenance.json](provenance.json) states dependency roles, and
[manifest.json](manifest.json) hashes the compact published files.

Primary tables reopened 2026-10-01 retain
[22<=R(B4,B7)<=23, Table 1](https://arxiv.org/pdf/2407.07285) and
[Small Ramsey Numbers, Table IXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf).
The [authors' 21-point construction](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
is reproduced. The upper-23 certificate was not replayed. Bounded primary,
graph and source checks calibrate this increment; no exhaustive historical
priority assertion is made. The new statement is the explicitly quantified
two-eight exclusion and consequent necessary two-profile restriction,
not a claim that R(B4,B7) has been determined.
