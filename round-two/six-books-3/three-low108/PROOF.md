# No full root in the one8+two9 sector at 108 edges

Actual author **six-books-3**, role **researcher**, 2026-10-01.

A valid graph is a simple red graph on 22 vertices, with at most three common
red neighbors on every red edge and at most six common blue neighbors on every
blue nonedge. These are ordinary noninduced books; page-page edges are free.
A full root has red degree ten and all ten red neighbors of degree ten.
A one-nine root has degree ten, exactly one degree-nine red neighbor, and
nine degree-ten red neighbors.

**Finite rooted theorem.** No valid graph with 108 red edges, maximum red
degree at most ten, and degree multiset `8^1,9^2,10^19` has a full root whose
red neighborhood is Petersen. Only one Petersen root is assumed. The exact
certificate covers all 51,240 necessary incidence systems, in 462 local
templates. Of these, 423 have an empty star domain, 38 have static pair-support
obstructions, and one has a seven-step support-deletion certificate.

**Ordinary consequence, with a credited premise.** Every valid 108-edge,
maximum-ten graph with this degree pattern has no full root. The separate
[8828 full-root classification](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/near108-local14/PROOF.md)
would make any such root Petersen. This imports 8828, whose deficit-four
branch is independently confirmed by
[review 9011](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/deficit-four-root-audit/REVIEW.md)
with its inherited census and classification premises explicit. That review
does not audit the present three-low certificate or the two-eight lemma 8979.

**Occurrence consequence, with credit.** Such a graph has at least seven
one-nine roots. This is the previously proved seven-root bound of
[independent review 8987](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/dirty-root-audit/REVIEW.md),
now applicable because the new ordinary consequence supplies rootlessness.
Its short ordinary proof is reproduced in Section 6; seven is not claimed new.

**Combined degree consequence.** With the credited
[8941 below-eight exclusion](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/low-degree108/PROOF.md)
and [8979 two-eight exclusion](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/two-eight108/PROOF.md),
a valid 108-edge graph of maximum degree at most ten either has four
degree-nine points, or has one8+two9 and is rootless with at least seven
one-nine roots. In particular a full root is possible only in the four-nine
pattern. For arbitrary valid 108-edge graphs the upper-degree part of
[8012](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md)
supplies maximum ten. Its historical minimum-eight classification is not
used. No existence or exclusion of the four-nine or rootless sectors follows.

The finite theorem imports none of these host-classification premises.
Ordinary counting and complete finite coverage bridges are written and
unformalized. Separate producer/checker algorithms are by one author, not
independent peer review. New review is pending. This is a necessary
sector restriction, not a full 108-edge exclusion or Ramsey endpoint.

## 1. One full Petersen root fixes every column and deficiency tag

Fix v, A=N_R(v), B=N_B(v), of sizes ten and eleven. Identify P=G[A] with
KG(5,2), using lexicographically ordered ground pairs of {0,1,2,3,4} as
local vertices. For b in B put

    Z_b=A minus N_R(b), C_b=A minus Z_b, k_b=|Z_b|,
    W_i={b in B:i in Z_b}, delta_b=10-d_G(b),
    D_b=N_R(b) intersect B.

Each A point has three red neighbors in P, the root, and six red neighbors
in B. Thus

    |W_i|=5, sum_b k_b=50, |D_b|=k_b-delta_b.            (1)

The blue spine vb has exactly 10-|D_b| common blue pages, giving

    k_b>=4+delta_b.                                     (2)

Every deficient point lies in B since v and A are full. Order B first by
the unique deficit-two row, then the two deficit-one rows, then eight full
rows. Their fixed tags are `(2,1,1,0,0,0,0,0,0,0,0)`.
The low minima are 6,5,5, and the eight full minima are four. The incidence
budget fifty leaves exactly two surplus units above these minima. It bounds
the two-tag word by eight and either one-tag word by seven. The complete
possible low-size patterns, with the equal one-tag sizes sorted for this
display only, are

    (6;5,5), (6;5,6), (6;5,7), (6;6,6),
    (7;5,5), (7;5,6), (8;5,5).                         (3)

For an A red pair, the full red pages number 2+|W_i intersect W_j|: the
root contributes one, P contributes zero, and B contributes one plus the
intersection. For a blue pair, P contributes three common blue points and
B contributes the intersection. Hence

    |W_i intersect W_j|<=1 for red ij,
    |W_i intersect W_j|<=3 for blue ij.                  (4)

These ordinary page mechanisms are credited to
[8541](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/regular_blue_codegrees/PROOF.md)
and [8785](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/near109_cubic_exclusion/PROOF.md).

We reproduce the necessary elementary word filters of 8941/8979. Write
h_i=|N_P(i) intersect C_b|. For a red P-edge ij in Z_b, (4) makes
X_i=W_i minus {b}, X_j=W_j minus {b} disjoint four-sets. On blue bi the
known A pages are k_b-4+h_i, and the B pages are
4-|D_b intersect X_i|. Applying both caps and |D_b|=k_b-delta_b gives

    k_b+delta_b+h_i+h_j<=12    (red ij in Z_b).          (5)

Negative separate lower bounds remain valid when added. On a red bi spine,
i in C_b has h_i known A pages and five other red B neighbors. Counting
its intersection with D_b among ten points gives

    k_b-delta_b<=8-h_i          (i in C_b).              (6)

The known A pages of a blue bi spine give

    |N_P(i) intersect Z_b|>=k_b-7  (i in Z_b).           (7)

Exhausting these necessary conditions retains all 210/120/45 two-tag words
of sizes 6/7/8, and all 252/210/120 one-tag words of sizes 5/6/7. Thus the
complete low domains here have 375 and 582 words. No K2,3-filtered domain,
historical lower-degree theorem or general miss-row cap is imported.

## 2. Full rows without assuming other roots Petersen

We reproduce the weighted four-column argument credited to 8785 and
[8759](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/book-regular-audit/REVIEW.md).
At any degree-ten root u, let J=G[N_R(u)], with local degrees h_i<=3 from
the red spines ui. Suppose four neighbors form an induced four-cycle and
all four have global degree ten. Their miss columns have sizes h_i+2 among
eleven outside points. If H is their local degree sum, H<=12.

For a red local pair ij, with c_ij local common red neighbors, literal page
counts bound the joint miss count by h_i+h_j-5-c_ij; for a blue pair the
bound is h_i+h_j-2-c_ij. Summing the four cycle-edge bounds gives at most
2H-20. The two opposite blue pairs each have at least two local common
neighbors, giving at most H-8. On the other hand summing
binom(t,2)>=t-1 over eleven rows gives at least H+8-11=H-3. Thus
H-3<=3H-28, or 2H>=25, contrary to H<=12. Other neighbors of u may be low.

For a full b in B, if i in C_b has two P-neighbors j,k in C_b, the
degree-ten root i has the induced local four-cycle v,j,b,k, all globally
full. Petersen is triangle-free, so jk is blue; vb is blue by definition.
The contradiction proves

    maximum degree of P[C_b]<=1 for every full b.       (8)

For k_b=4, cubic counting gives e(P[C_b])=3+e(P[Z_b]). The six-point
matching has at most three edges, so Z_b is independent. The five independent
four-sets of KG(5,2) are its ground stars S_t, the four pairs containing t.
A pairwise intersecting family of four ground pairs must have a common
point: otherwise {a,b},{a,c} require a pair avoiding a to be {b,c}, after
which no fourth distinct pair can intersect all three.

Each S_t occurs at most twice among full four-rows. Equal rows have six
common red A-neighbors, forcing their B pair blue. On a blue spine between
two degree-ten points in order 22, common red and blue counts are equal.
Their outside red stars must therefore be disjoint. Three equal rows would
require three disjoint four-subsets of the remaining eight B points.
Write their multiplicities mu_t in {0,1,2}.

At most two surplus incidences occur in full rows. The full large multiset
is empty, one five, one six, or two fives, with repetitions allowed. Direct
subset enumeration of (8) gives thirty five-words and eighty six-words.
There are eight full rows, so sum(mu)+number of full large rows=8.
No all-other-full-roots Petersen or dirty-isolated-row condition is used.

## 3. Two complete incidence algorithms

A key is `(z,w,q, sorted full large words, (mu_0,...,mu_4))`, where z has
deficit two, w and q have deficit one, and **w<=q numerically**. There is
no ordering between z and either one-tag row, and no ordering by row size.
Repetitions are allowed. Numeric sorting of equal tags and full large words
is only relabeling outside vertices, not a host automorphism assumption.

[produce.py](produce.py) first enumerates all unordered one-tag row pairs
within size budget twelve and with no repeated red pair. Their full ten-column
sum vectors form a lookup table. Each coordinate is 0,1,2, packed in two
binary bits; summing two binary columns cannot carry. Counts are 137,193
pairs before red caps, 39,666 after, at 3,351 distinct sum vectors.

It then chooses every red-capped full large multiset and every multiplicity
vector in {0,1,2}^5 with eight full rows. After subtracting their columns
from five, the three low rows have residuals r_i in {0,1,2,3}. A zero
forbids z membership and a three forces it. For every complete two-tag word
respecting these conditions, subtract its binary coordinates. The remaining
vector lies in {0,1,2}^10 with no borrow and is joined to the exact low-pair
table. Check all remaining red and blue pair caps. Every actual incidence
is covered, since its full rows, multiplicities, z word and low pair all
appear and obey these necessary conditions.

Counts are 456 full large multisets, 18,840 multiplicity choices, 9,215
residual vectors, 1,036,750 compatible z assignments before later red caps,
1,670,070 exact column joins, and **51,240 final keys**.

[verify.py](verify.py) imports no producer. It starts from a fixed literal
Petersen adjacency table and enumerates C subsets for its word domains.
Its different low8/large quotient join credits the mechanism of 8785. The
five integral forms on ground-pair coordinates a_ij are

    a_03-a_13-a_02+a_12,
    a_04-a_14-a_02+a_12,
    a_0i+a_0j-a_ij-a_01-a_02+a_12   (ij=23,24,34).

Every form vanishes on each S_t vector and the constant column five. Index
all necessary one-tag pairs by their total size and the sum of these forms.
For a full large multiset of surplus h and a z word, its pair-size demand
is 18-h-|z|. The opposite quotient sum is a necessary join condition.
No rank, converse or surjectivity assumption is made.

After joining, recover the remaining star multiplicities from residual
columns r_ij: 2*mu_0=r_01+r_02-r_12 and mu_j=r_0j-mu_0. Check integrality,
0<=mu<=2, eight full rows, all ten equations mu_i+mu_j=r_ij, and all pair
caps. These formulas uniquely recover every genuine solution. Cached exact
red-pair sets and column vectors only avoid recomputation. A blue local pair
belongs to exactly one ground star, so its full-four-row contribution is
the corresponding mu_t; a red pair belongs to none. The literal ground-star
table is checked. This computes the same capacities as summing all rows.

The checker counts 99,525 budget-compatible z/large pairs, 1,842,530 quotient
joins, 158,400 red-capped joins, 149,100 integral recoveries, and the same
51,240 keys. Their complete eight size patterns are:

| two-tag size | one-tag sizes, sorted for display | full large sizes | keys |
|---:|---|---|---:|
|6|5,5|5,5|24,180|
|6|5,5|6|6,360|
|6|5,6|5|12,720|
|6|5,7|none|1,140|
|6|6,6|none|765|
|7|5,5|5|4,620|
|7|5,6|none|1,140|
|8|5,5|none|315|

Both complete raw transcripts match entrywise. Canonical compact-JSON SHA256:

    49dbd338b5c8911c85e34c4176d23061e3c3cdffe4c69a7f2d0ef8771b3e52e3.

## 4. Every local relabeling and every outside star

Permute the five KG ground labels, move all words and mu, then sort only
the equal one-tag pair and full large rows. These 120 maps preserve P and
all constraints. A completion transports by relabeling A and B; no host
symmetry is required. The producer repeatedly takes the smallest uncovered
raw key and covers its complete local orbit. It checks disjointness, orbit
membership and complete raw union. There are **462 templates**, with orbit
size counts `15:2, 30:1, 60:65, 120:394`, summing to 51,240 keys.

The checker instead expands each supplied representative, verifies every
map against its literal P table, requires the minimum representative and
actual orbit size, checks disjointness, and requires the expanded union to
equal its independently generated key set entrywise. A full classification
of Aut(P) is unnecessary: these explicit maps and exact coverage suffice.

Order B by z,w,q, sorted full large rows, then S_t in increasing t repeated
mu_t times. At b exhaust every D_b subset of B minus {b} with size
k_b-delta_b. The exact red bi pages, i in C_b, are

    |N_P(i) intersect C_b| + |D_b minus W_i|.

The exact blue bi pages, i in Z_b, are

    k_b-1-|N_P(i) intersect Z_b| + |(W_i minus {b}) minus D_b|.

Retain exactly those stars respecting all ten mixed-spine caps. For two
stars x at b and y at c require reciprocal membership c in x iff b in y.
Their red-pair pages are 10-|Z_b union Z_c|+|x intersect y|. For a blue pair,
put E_b=B minus ({b} union x), E_c=B minus ({c} union y); their pages are
1+|Z_b intersect Z_c|+|E_b intersect E_c|.

The producer uses these decomposed formulas. The checker builds full physical
neighborhood sets on root 0, A=1..10 and B=11..21, excludes each endpoint
from its complement, and counts literal common red/blue neighbors. It rebuilds
every initial domain and checks all eleven sizes and the hash in
[certificate.json](certificate.json). Immutable in-memory caches use complete
incidence keys and fixed P/tags; they contain only freshly computed exact
values and import no saved domains or private data.

## 5. Complete obstruction coverage and the one seven-step trace

423 templates, covering 46,740 raw keys, have an actually empty initial
star domain. For 38 templates, covering 4,440 keys, the certificate partitions
one complete initial target domain into disjoint groups. Every group names
a different point whose complete initial domain contains no compatible star
for any value in that group. The checker exhausts all potential supports,
verifies masks/membership and exact partition coverage. A valid completion
would supply a compatible actual support for its actual target star, a
contradiction. These static covers use 47 groups and 87 target stars.

The one remaining representative, of orbit size sixty, is

    (183,79,914,(369,684),(1,1,1,1,2)).

Its initial domain sizes are `16,5,5,4,4,27,27,27,27,32,32`.
The following is the complete shortened trace. Each step removes the listed
stars from the point because none has a compatible star in the **current**
domain at the named support point. Masks use the above B order.

| point | against | removed stars |
|---:|---:|---|
|0|1|60,116,184,240,300,356,424|
|0|2|154,210,394,450|
|0|3|30,86,270|
|1|3|60,1601|
|1|4|1545|
|5|0|30,92,270,581,596,777,780,836,960,1093,1108,1289,1292,1348,1472|
|5|1|525,537,540,664,720,904,1037,1049,1052,1176,1232,1416|

The first five steps restrict two low domains by unsupported stars visible
in the initial domains. The final two cover all 27 initial stars at point5
using those restricted supports. The producer derives this shallow trace
by exhausting pairs of domains to restrict and then targets; it does not
assume the displayed choices. The independent checker only replays the seven
supplied steps using literal pages, including every possible current support.
All removed masks must be present, sorted and unique; a step after emptiness
is forbidden; the final named domain must actually be empty. Forty-four
stars are removed in total.

Every removal preserves every valid completion. Otherwise consider the first
removed actual star; its compatible actual star at the support point would
still be present, contradiction. Thus the final empty domain excludes all
completions of this last orbit. This standard support principle is also
credited in the original 8941 certificate and its
[independent audit 8969](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/petersen-low-degree-audit/REVIEW.md).
Their different 4,985-key domain does not supply coverage of the present
three-low system or a verdict on this result. No branching, solver or incomplete
enumeration establishes any exclusion here.

Root--A spines have three pages, root--B satisfy (2), A--A satisfy (4),
A--B obey the complete star domains, and B--B obey reciprocity and the literal
pair oracle. These exhaust all spines and outside assignments. All 51,240
necessary incidences are therefore excluded, proving the finite theorem.
Canonical certificate SHA256:

    e9bc3b9b1373aa5df9ff0a70f89caddeb2e63db56fd77068451e0f44fcab1039.

## 6. Ordinary host consequences, with exact dependency boundaries

If a valid one8+two9 graph had a full root, 8828 would make it Petersen and
the finite theorem would contradict it. Thus every full-degree point has a
deficient red neighbor. This ordinary rootless conclusion depends on 8828;
the finite certificate above does not.

We reproduce the credited seven-root proof of 8987. Label low points z,a,b
of degrees8,9,9, and the nineteen degree-ten points H. Put
ell_z=e_za+e_zb, where each e indicates a red low edge. Let y count high
points with low type exactly {a,b}, and t those with all three low neighbors.
Exactly 8-ell_z high points are red neighbors of z. Each other high point
has type {a}, {b} or {a,b}, since rootlessness excludes the empty type.
Thus the number R of one-nine roots is 11+ell_z-y.

The common red neighbors of a,b are y+t+e_za*e_zb. If ab is red this is
at most three. If blue, its common blue count is two plus that common red
count, so it is at most four. Hence

    y+t+e_za*e_zb<=4-e_ab,
    R>=7+ell_z+e_ab+e_za*e_zb+t>=7.                     (9)

This is the existing ordinary review refinement, not a new seven-root claim.
Its hypotheses now follow from the present rootless consequence.

At maximum ten and 108 edges the total nonnegative deficit is four.
8941 excludes below-eight patterns 4 and3+1; 8979 excludes2+2. Only
2+1+1 and1+1+1+1 remain. The new result makes the first rootless. The
upper-degree part of8012 is needed only to remove the explicit maximum-ten
hypothesis. A four-nine graph may still have a full root; rootless hosts,
actual one-nine neighborhood completions and the high-graph exceptions are
not excluded. The complementary
[dirty13 isolated-type exclusion](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/dirty13_isolate_exclusion/PROOF.md)
removes one marked type from
[8939's necessary local list](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/rootless108_marked_profiles/PROOF.md), leaving its other
thirteen types. Its finite proof is separate and not imported here. Bounds
for full-root columns cannot be transferred to dirty neighbors whose miss
column has an extra deficiency unit.

## 7. Reproduction, controls and remaining limits

CPython3.11.2 standard-library integers and sets suffice. The producer regenerates
the frozen certificate. The checker independently rebuilds the complete
census and literal domains; neither imports the other. Both compare full
records with [expected.json](expected.json), and all guards are explicit
exceptions active under Python -O. The ordinary bridges, enumeration coverage
and program correspondence are unformalized; new independent peer review
is pending. No private corpus, floating solution, external graph catalogue,
all-other-roots premise or hidden historical degree floor is required.

The primary21 fixture was fetched live and matched byte for byte. With
off-diagonal zeros red it has93 red/117 blue edges and page maxima3/6.
The same literal oracle, using its actual local graph and tags at the unique
degree-ten root, accepts all ten actual outside stars/completion and rejects
196 asymmetric degree-preserving changes. It is prior art and validation,
not a new construction. Raw SHA256 is
3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55.

Geometry controls check P, common neighbors, the five independent four-sets,
ground-star pair membership and all seven low-size possibilities. Thirty-two
deliberately invalid signed frames check137 blue-intersection identities,
including eighteen negative cap slacks; these are identity controls, not
witnesses. [controls.py](controls.py) rejects29 damaged certificates and,
in its separate required summary mode, a frozen summary falsely narrowing
the size-six two-tag domain from210 to200. Damages include wrong equal-tag
order, omitted/duplicated coverage, supported stars removed, incomplete/static
covers, incomplete deletion traces and steps after emptiness. Every normal
and optimized mode is required; [README.md](README.md) supplies commands.

The first independent implementation reached its fixed45-second guard before
completion and established nothing. Exact cached pair/column data, immutable
domain reuse, and separate integrity modes then completed under that same
guard and unchanged1CPU/2GiB scope. No timeout, UNKNOWN, memory kill or partial
enumeration is interpreted as nonexistence. All proof decisions are exact;
timing is operational evidence only. [provenance.json](provenance.json) records
premise roles and [manifest.json](manifest.json) records source bytes/hashes.

Primary tables rechecked2026-10-01 retain
[22<=R(B4,B7)<=23, Table1](https://arxiv.org/pdf/2407.07285) and
[Small Ramsey Numbers, TableIXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf).
The [authors' primary construction](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
is reproduced; the published upper23 certificate was not replayed. Bounded
live literature/graph/source checks calibrate this scoped increment and do
not establish exhaustive historical priority or the Ramsey endpoint.
