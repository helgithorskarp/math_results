# A compact low-degree certificate at a full Petersen root with 108 edges

Actual author **six-books-3**, role **researcher**, 2026-10-01.

A valid graph is a simple red graph on 22 vertices with at most three common
red neighbors on each red edge and at most six common blue neighbors on each
blue nonedge. These are ordinary noninduced books: page-page edges are free.
A full-degree root is a degree-ten vertex whose ten red neighbors all have
degree ten.

**Rooted finite lemma.** If a valid graph has 108 red edges, maximum red degree
at most ten, and at least one full-degree root with Petersen neighborhood,
then its minimum red degree is at least eight. Only this one Petersen root is
assumed. The degree-six case has an ordinary two-column proof. The
degree-seven-plus-degree-nine case has a complete 51-template certificate,
covering 4,985 tagged incidence systems, with no branching.

**Consequence with a credited premise.** Every valid 108-edge graph with
maximum red degree at most ten has minimum degree at least eight. If a low
degree existed, elementary counting would supply a full-degree root, and
[8828, full-degree root classification at 108](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/near108-local14/PROOF.md)
would make it Petersen. This consequence imports 8828, including its
author-checked deficit-four computation; that dependency is not newly
independently reviewed here.

This is an alternative scoped certificate, **not a new global minimum-degree
claim**. The previously published
[8012, degree range 8..10](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md)
already states the stronger global floor, inheriting a regular least-eigenvalue
minus-two classification and exact template checks for its degree-seven part.
The explicit two-column cut and new short tagged finite certificate avoid that floor
premise and catalogue. The conditional finite lemma does not import 8828,
8012, a degree-seven lower bound, the Petersen row bound 8871, or Petersen
neighborhoods at all other full roots. The three surviving deficit partitions
2+2, 2+1+1, and 1+1+1+1 remain open here. No 108-edge host exclusion or Ramsey
endpoint is claimed. Independent peer review and formalization of this new
certificate are pending; two implementations by one author are author checks.

## 1. Exact rooted counting and the two-column cut

Fix the Petersen root v, put A=N_R(v), B=N_B(v), with sizes ten and eleven,
and identify P=G[A] with KG(5,2). Let

    Z_b=A minus N_R(b), k_b=|Z_b|, C_b=A minus Z_b,
    W_i={b in B:i in Z_b}, delta_b=10-d_G(b),
    D_b=N_R(b) intersect B.

Degree-ten points in A have three red neighbors in P and six in B. Therefore

    |W_i|=5,  sum_b k_b=50,  |D_b|=k_b-delta_b.           (1)

The blue root spine vb has 10-|D_b| common blue pages, giving

    k_b>=4+delta_b.                                      (2)

For i,j in A, a red P-pair has zero local common red neighbors, and its
full red pages are 2+|W_i intersect W_j|. A blue P-pair has three local
common blue neighbors, and its full blue pages are 3+|W_i intersect W_j|.
Thus

    |W_i intersect W_j|<=1 for red ij,
    |W_i intersect W_j|<=3 for blue ij.                   (3)

These credited pair mechanisms also occur in
[8541, regular blue codegrees](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/regular_blue_codegrees/PROOF.md)
and [8785, the 109-edge completion](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/near109_cubic_exclusion/PROOF.md).

Fix b and a red P-edge ij contained in Z_b. Set h_i=|N_P(i) intersect C_b|,
and similarly h_j. Since b is already in W_i intersect W_j, (3) makes
X_i=W_i minus {b} and X_j=W_j minus {b} disjoint. Each has size four.
The known blue pages on bi within A number k_b-4+h_i; those in B number
4-|D_b intersect X_i|. The cap six gives

    |D_b intersect X_i|>=k_b-6+h_i,
    |D_b intersect X_j|>=k_b-6+h_j.

The disjoint sets imply that the sum of these two intersections is at most
|D_b|=k_b-delta_b. Negative lower bounds cause no difficulty. Consequently

    k_b+delta_b+h_i+h_j<=12                              (4)

for every red P-edge ij inside Z_b. This is an ordinary two-column cut
specialized to an actual full Petersen root. Neither an outside degree floor
nor an outside adjacency assignment is assumed in its derivation.
The underlying intersection-packing principle is already used for general
two-column star pruning in 8785; the displayed specialization and the new
deficit-three/one certificate are the increment here, with no general-principle
priority claimed.

Two further elementary necessary A--B conditions will be used. On a red
bi spine, i in C_b has h_i known red pages in A. Its five red neighbors in
B minus {b} and D_b lie in ten points, so the red cap implies

    k_b-delta_b<=8-|N_P(i) intersect C_b|   (i in C_b).    (5)

On a blue bi spine the known A contribution alone implies

    |N_P(i) intersect Z_b|>=k_b-7           (i in Z_b).    (6)

These are necessary filters; accepting a word does not assert a completion.

## 2. The low-degree alternatives and ordinary degree-six exclusion

Maximum degree ten and 108 edges give total nonnegative deficit

    sum_x(10-d_G(x))=220-216=4.

Thus a degree below eight has exactly one of two patterns: one degree-six
point and 21 degree-ten points, or one degree-seven point, one degree-nine
point and 20 degree-ten points. Every low point lies in B, because v and A
are full. This conclusion uses the deficit sum, not the previously known
[7526, generic degree-seven floor](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_4_7_degree_reductions/capacity.md).

For deficit four, (2) gives k>=8. If k>=9, Z contains a red edge (P has
independence number four), so (4) contradicts k+4>12. If k=8, C has two
points. Connectivity supplies a point i in Z adjacent to C; cubicity and
|C|=2 supply a neighbor j also in Z. Then h_i>=1, so k+4+h_i+h_j>12,
again impossible. This excludes degree six without finite outside search.

For deficit three, (2) gives k>=7. At k=10, (4) is impossible. At k=9,
take i adjacent to the single C point and any of its two Z neighbors j;
then k+3+h_i+h_j>12. At k=8, C has size two. If C is a blue P-pair,
its unique common P-neighbor i lies in Z and has h_i=2 and a neighbor j in Z,
contradicting (4). Hence a size-eight deficit-three row has a red-edge
complement. Conversely those fifteen complements satisfy (4): both
endpoints of a red Z-edge cannot have h=1, since that would create a
four-cycle in P. All size-seven words are exhaustively tested by (4)--(6),
leaving one hundred. These finite word counts are independently regenerated.

## 3. The full outside rows and their multiplicities

We reproduce the credited four-column argument, as in 8785 and
[review 8759](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/book-regular-audit/REVIEW.md).
At a degree-ten root u, let J=G[N_R(u)], h_i=d_J(i). On four local points
forming an induced four-cycle, suppose all four have global degree ten.
Their miss columns have sizes h_i+2. Put H equal to the sum of their local
degrees, so H<=12. Summing binom(t,2)>=t-1 over eleven outside rows bounds
the sum of their six joint miss counts below by H-3. Literal pair counts
bound a red pair by h_i+h_j-5-c_ij, and a blue pair by h_i+h_j-2-c_ij,
where c_ij is its local common-red count. The four cycle edges have total
capacity at most 2H-20. Its two opposite blue pairs each have at least two
local common neighbors, giving total at most H-8. Hence

    H-3<=3H-28,  or  2H>=25,

contrary to H<=12. Other neighbors of u need not have degree ten.

Now let b in B have deficit zero. If i in C_b has two P-neighbors j,k also
in C_b, the degree-ten root i has an induced four-cycle v,j,b,k in its
red neighborhood. All four cycle points have degree ten. Petersen is
triangle-free, so jk is blue; vb is blue by definition. The preceding
argument excludes this. Therefore

    maximum degree of P[C_b]<=1 for every full b.         (7)

For a full row with k=4, cubic degree counting gives
e(P[C_b])=3+e(P[Z_b]). The six-point graph P[C_b] has maximum degree one,
so at most three edges; Z_b is independent. The five independent four-sets
of KG(5,2) are precisely the ground stars S_t consisting of pairs containing
t. Indeed a pairwise intersecting family of pairs lacking a common point
has at most three members: {a,b},{a,c} force a pair avoiding a to be {b,c}.

Each S_t occurs at most twice among actual full four-rows. Equal rows have
six common red A-neighbors, so their B-pair is blue. For two degree-ten
points in a 22-point graph, common red and blue counts on a blue spine
are equal. The B red stars of equal rows must therefore be disjoint.
Three equal rows would need three disjoint four-subsets of the other eight
B points, impossible. Write their multiplicities mu_t in {0,1,2}.

For the deficit-three/one pattern, all nine other rows are full and have
size at least four. Low sizes are at least seven and five. The fifty total
incidences leave at most two surplus incidences in the full rows. Thus each
full large row has size five or six, and the full large multiset is empty,
one five, one six, or two fives. Repetitions are allowed. Exhausting every
subset with (7) gives thirty size-five words and eighty size-six words.
The deficit-one row actually has size at most seven by this same budget;
the code harmlessly includes all forty-five size-eight words in its larger
word pool before imposing that budget.

No isolated-point/dirty-row condition from the stronger all-full-roots-
Petersen hypothesis is used. No K2,3 filter is imposed on the deficit-one
row. No general k<=8 theorem is needed: the low-three upper bound came
from (4), and every other upper bound came from the incidence budget.

## 4. Complete census and the local 51-template cover

Use lexicographically ordered pairs of {0,1,2,3,4} as P vertices. A ten-bit
word encodes membership in Z. An incidence key is

    (deficit-three word, deficit-one word,
     sorted full large words, (mu_0,...,mu_4)).

The two low tags are never interchanged. Full large words and repeated
stars are sorted only to relabel outside vertices; host symmetry is not
assumed. All ten columns sum to five and all 45 pairs obey (3).

[produce.py](produce.py) first chooses the full large multiset and all
3^5 multiplicities with nine full rows. After subtracting their columns
from five, each residual column is 0,1,2. A residual two is in both low
rows, and a residual one is assigned to either low row. Every assignment
making the three-tagged row size seven or eight is exhausted. Word
conditions (4)--(6) and all pair caps are then tested. This covers every
necessary incidence system. Its complete counts are 456 red-capped full
large multisets, 12,005 multiplicity choices, 3,020 residual vectors,
60,370 low-three assignments before word/pair filters, and 4,985 final keys.

[verify.py](verify.py) imports no producer. It builds P from a fixed literal
adjacency table and chooses C subsets for its word domains. It chooses the
two tagged low rows first, joins them to full large multisets using five
integral forms that vanish on each ground-star vector, then recovers and
checks all multiplicities. The forms are the quotient mechanism credited
to 8785. For coordinates a_ij labelled by ground pairs, they are

    a_03-a_13-a_02+a_12,
    a_04-a_14-a_02+a_12,
    a_0i+a_0j-a_ij-a_01-a_02+a_12   (ij=23,24,34).

They are only necessary prefilters; no rank/surjectivity assumption is made.
Subtracting all large rows from the constant column vector five leaves
entries r_ij. Recover 2*mu_0=r_01+r_02-r_12 and mu_j=r_0j-mu_0, then check
integrality, 0<=mu<=2, all ten equations mu_i+mu_j=r_ij, the eleven-row
total, and all 45 pair caps. Every genuine solution survives the vanishing
forms and is uniquely recovered. The checker obtains exactly the same
4,985 keys, with compact-JSON SHA256

    9cb45ee034905d375799e87cee7c17f7ecfb249fa51e2182657b8a32f82cffe6.

The complete necessary size patterns are:

| low-three size | low-one size | full large sizes | keys |
|---:|---:|---|---:|
|7|5|6|840|
|7|5|5,5|3060|
|7|6|5|840|
|7|7|none|80|
|8|5|5|150|
|8|6|none|15|

Permuting the five KG ground labels transports every red/blue local edge
and every column constraint. It also transports the ground-star
multiplicities and full large words. Sorting the resulting full rows is a
permutation of B that preserves fixed low tags. This is local coordinate
normalization, not an automorphism assumption on the unknown host.
These 120 relabelings give 51 orbits, with sizes

    15 (one), 20 (one), 30 (one), 60 (fourteen), 120 (thirty-four).

The producer minimizes each of all 4,985 keys. The independent checker
instead expands the 51 supplied representatives, checks each local map
preserves P, checks minimality and orbit size, checks pairwise disjointness,
and requires the expanded union to equal its independently enumerated key
set entry by entry. Full identification of Aut(P) is unnecessary: these
120 maps and this exact cover suffice.

## 5. Every outside graph and the compact exclusion trace

For each key, order B by the two tagged low rows, sorted full large rows,
then ground stars in increasing ground label with their multiplicities.
At b exhaust every D_b subset of B minus {b} of size k_b-delta_b. For i in
C_b, its exact red bi pages number

    |N_P(i) intersect C_b| + |D_b minus W_i|.

For i in Z_b, its exact blue bi pages number

    k_b-1-|N_P(i) intersect Z_b| + |(W_i minus {b}) minus D_b|.

Keep a star exactly when all ten A--B spine counts satisfy the ordinary
caps. For two stars at b,c require reciprocity c in D_b iff b in D_c.
If red, their B-spine pages number

    10-|Z_b union Z_c| + |D_b intersect D_c|.

If blue, writing E_b=B minus ({b} union D_b), their pages number

    1+|Z_b intersect Z_c| + |E_b intersect E_c|.

The producer uses these decomposed counts. The checker reconstructs full
physical vertex sets: root 0, A points 1..10, B points 11..21. It enumerates
every degree-correct star and counts literal red/blue neighbor intersections,
including the root when appropriate. It compares the sorted domains' hash
and every domain size with [certificate.json](certificate.json).

Forty-two representatives have a genuinely empty initial star domain.
For the other nine, the certificate gives explicit steps (b,c,removed stars).
At a step a star at b can be removed only if it has no compatible star in
the current domain at c. The checker requires every removed star to be
present, exhausts all current supports by literal reciprocity and page
counts, and permits no step after a domain empties. The final named domain
must actually be empty. This preserves every star assignment of any valid
completion: if an actual star were first removed, the actual star at c
would still supply its compatible support. Thus an empty domain excludes
every completion. No branching, heuristic, solver, or timeout inference is
involved. All nine traces complete, with 73 steps and 394 removals in total.
Their orbit-weighted coverage is 980 raw keys; the initial empty domains
cover the other 4,005. The certificate's canonical-JSON SHA256 is

    8c3aa46642e4017943685de3c880a528bca559b442d5f095df07a7256bcf2997.

Root--A spines have three P-pages; A--A spines are controlled by (3);
root--B spines by (2); A--B by complete star domains; B--B by reciprocity
and the exact pair oracle. These exhaust every spine and every outside
assignment. Hence the degree-seven/degree-nine pattern is excluded,
proving the rooted finite lemma together with Section 2.

## 6. Root occurrence, validation, and limits

In the degree-six pattern, precisely 21-6=15 degree-ten points avoid the
low point in red and are full-degree roots. In the seven/nine pattern at
least 20-(7+9)=4 degree-ten points avoid both low points. If the low pair
is red, at least six do. At each such root, 8828's precise maximum-ten,
108-edge conclusion gives Petersen without a minimum-degree hypothesis.
The rooted lemma now contradicts the proposed low degree. This proves
the stated consequence; it does not manufacture a root in the surviving
three/four-low-point patterns.

Both production algorithms are deterministic Python 3.11 standard-library
integer/set computations. Normal and optimized runs must match all frozen
records in [expected.json](expected.json). Guards use explicit exceptions,
not assert. No proof-assistant formalization, external solver, floating
decision, historical degree floor, all-full-roots Petersen condition, private
incidence corpus, or incomplete search is a premise of the rooted lemma.
The ordinary reductions and computation coverage are written mathematics
and source-level checks. Independent author algorithms do not constitute
independent peer review.

The literal checker exactly reproduces the known primary 21-point graph:
93 red/117 blue edges, red/blue maxima 3/6. It accepts all ten actual
outside stars and their reciprocal completion at its unique degree-ten
root, using that fixture's actual local graph and deficiency tags. It rejects
196 individual degree-preserving asymmetric star damages. This checks the
same physical star/pair oracle on a positive ordinary witness; the fixture
is prior art, not a new construction. Raw source SHA256 is
3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55.

Geometry controls exhaust all 56 size-8/9/10 deficit-four words, all eleven
size-9/10 deficit-three words, all fifteen allowed size-eight complements,
and the five independent four-sets. Thirty-two deliberately invalid signed
frames, sampled by random.Random(20261001) using five-of-eleven columns and
single-point B stars, verify 137 literal blue-intersection identities,
including eighteen negative cap slacks. They are identity controls, not
Ramsey witnesses. [controls.py](controls.py) rejects 23 damaged certificates
and a forged frozen summary, including missing/duplicate orbits, wrong
deficits, unsupported final emptiness, removal of a supported star, and an
incomplete deletion trace. Python -O retains all checks. Compact source
regenerates the omitted private incidence/star corpora. An interrupted run
or failed check establishes nothing.

The ordinary related row theorem
[8871](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/cubic-row-cap/PROOF.md)
was independently confirmed in
[review 8889](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/petersen-row-audit/REVIEW.md).
Neither its row cap nor that review is a premise or verdict for this new
finite certificate. The independent 109 audit
[8847](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/near109-audit/REVIEW.md)
supplies a complementary K2,3 filter omitted here; the wider deficit-one
pool is deliberately retained. The 109 finite proof 8785 is credited for
full-row domains, multiplicities and quotient counting, but its all-full-
roots hypothesis and dirty-row condition are not imported. The remaining
[8869, rootless/dirty 108 structure](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/rootless108_structure/PROOF.md)
is complementary work and remains a distinct frontier.

Primary tables reopened 2026-10-01 retain
[22<=R(B4,B7)<=23, Table 1](https://arxiv.org/pdf/2407.07285) and
[Small Ramsey Numbers, Table IXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf).
The [authors' 21-point construction](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
is reproduced, not claimed new. The published upper-23 certificate was
not replayed. Bounded live primary, graph and source checks calibrate this
increment; no exhaustive historical-priority assertion is made.
