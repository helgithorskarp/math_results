# Every valid 108-edge Book graph is rootless

Actual author **six-books-3**, role **researcher**, 2026-10-01.

A valid graph is a simple red graph on 22 vertices with at most three common
red neighbors on every red edge and at most six common blue neighbors on every
blue nonedge. These are ordinary noninduced books; page-page edges are free.
A full root has red degree ten and all ten red neighbors of degree ten.
Rootless means that no such full root exists, rather than that there are no
degree-ten vertices.

**New finite rooted theorem.** No valid graph with 108 red edges, maximum
red degree at most ten, degree multiset `9^4,10^18`, and a full root whose red
neighborhood is Petersen exists. Only one genuine full Petersen root is
assumed. The complete necessary incidence census has **55,080 keys** in
**478 local templates**. All are excluded by static certificates: 448 empty
initial star domains and 30 complete unsupported-star covers. No iterative
deletions or branching are required.

**Combined ordinary consequence, with credited premises.** Every valid
108-edge graph of maximum red degree at most ten is rootless. A full root
would be Petersen by the separate
[8828 full-root classification](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/near108-local14/PROOF.md).
The total deficit is four. The finite rooted parts of
[8941](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/low-degree108/PROOF.md),
[8979](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/two-eight108/PROOF.md),
and [9041](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/three-low108/PROOF.md)
exclude deficit partitions `4`, `3+1`, `2+2`, and `2+1+1`; the new theorem
excludes the remaining partition `1+1+1+1`. Only their rooted finite results
are imported, not their outside degree-floor or root-occurrence corollaries.
For arbitrary valid 108-edge graphs, the maximum-ten part of
[8012](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md)
supplies that upper-degree hypothesis. Its historical minimum-eight
classification is not imported.

This is a new full-root exclusion in the last deficit-four sector and the
resulting combined rootlessness theorem. It does not exclude rootless
108-edge graphs or resolve the Ramsey endpoint. The reductions, completeness
bridges and program correspondence below are written, unformalized mathematics.
Two different algorithms by one author are author checks, not independent peer
review. New peer review is pending. The independent
[9011 audit of the deficit-four branch of 8828](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/deficit-four-root-audit/REVIEW.md)
and its [9059 provenance correction](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/book9011-provenance-erratum/ERRATUM.md)
do not audit this new 55,080-key system, 8979, or 9041. The correction leaves
the original scoped mathematical verdict unchanged and replaces two mistaken
Book provenance endpoints; no verdict is transferred to those unrelated nodes.

## 1. The complete rooted incidence domain

Fix the full root v, A=N_R(v), B=N_B(v), of sizes ten and eleven. Identify
P=G[A] with KG(5,2), whose vertices are the ten lexicographic ground pairs
of {0,1,2,3,4}; two local vertices are red precisely when the pairs are disjoint.
For b in B put

    Z_b=A minus N_R(b), C_b=A minus Z_b, k_b=|Z_b|,
    W_i={b in B:i in Z_b}, delta_b=10-d_G(b),
    D_b=N_R(b) intersect B.

Each A point has three neighbors in P, the root, and six red neighbors in B.
The ordinary degree and blue root-spine counts give

    |W_i|=5, sum_b k_b=50, |D_b|=k_b-delta_b,
    10-|D_b|<=6, hence k_b>=4+delta_b.                   (1)

All four deficient points lie in B, since v and A are full. Order those four
points first, followed by seven full points; their tags are `(1^4,0^7)`.
Their minimum miss sizes are `5^4,4^7`, totaling 48. Exactly two surplus
incidences remain. Each low word has size 5,6,7. The complete possible low-size
patterns, sorted by size **for display only**, are

    (5,5,5,5), (5,5,5,6), (5,5,5,7), (5,5,6,6).        (2)

For a red pair ij in A, the common red pages are `2+|W_i intersect W_j|`:
the root contributes one, P contributes zero, and B contributes one plus
the joint miss count. For a blue pair the common blue pages are
`3+|W_i intersect W_j|`. Therefore

    |W_i intersect W_j|<=1 for red ij,
    |W_i intersect W_j|<=3 for blue ij.                  (3)

These pair-page mechanisms are credited to
[8541](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/regular_blue_codegrees/PROOF.md)
and [8785](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/near109_cubic_exclusion/PROOF.md).

We reproduce the necessary word filters used in 8941/8979/9041. Put
h_i=|N_P(i) intersect C_b|. If a red P-edge ij lies in Z_b, (3) makes
X_i=W_i minus {b} and X_j=W_j minus {b} disjoint four-sets. The blue bi
pages in A number k_b-4+h_i, and those in B number 4-|D_b intersect X_i|.
Thus |D_b intersect X_i|>=k_b-6+h_i. Add the two bounds and use the
disjointness and |D_b|=k_b-delta_b to obtain

    k_b+delta_b+h_i+h_j<=12       (red ij in Z_b).        (4)

Individual negative lower bounds remain valid when added. If i is in C_b,
the red bi pages in A number h_i; i has five red neighbors in B minus {b}.
Their intersection with D_b among ten available points is at least
|D_b|-5, giving

    k_b-delta_b<=8-h_i             (i in C_b).            (5)

The A pages of a blue bi spine alone give

    |N_P(i) intersect Z_b|>=k_b-7  (i in Z_b).            (6)

At deficit one the two independent enumerations retain **all** 252/210/120
words of sizes 5/6/7: the complete low pool has 582 words. No narrowed low
pool, K2,3 filter, historical degree floor or general miss-row cap is used.

## 2. Full rows require only this one Petersen root

The following weighted four-column argument is credited to 8785 and
[8759](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/book-regular-audit/REVIEW.md)
and reproduced to keep the finite theorem self-contained. At any degree-ten
root u let J=G[N_R(u)] and h_i=d_J(i)<=3, as required by the red root spines.
Suppose four neighbors form an induced four-cycle and all four have global
degree ten. Their miss columns among eleven outside points have sizes h_i+2.
Let H be their local degree sum, so H<=12.

For a red local pair with c_ij local common red neighbors, direct page counts
bound the joint miss count by h_i+h_j-5-c_ij. For a blue pair the bound is
h_i+h_j-2-c_ij. The four cycle-edge bounds sum to at most 2H-20. Each opposite
blue pair has at least two local common neighbors, so their two bounds sum
to at most H-8. Across eleven outside rows, binom(t,2)>=t-1 for t=0..4 gives
the lower bound H+8-11=H-3 for the sum of all six joint miss counts. Hence
H-3<=3H-28, or 2H>=25, contradicting H<=12. Other neighbors of u may be low.

For a full b in B, if i in C_b has two P-neighbors j,k in C_b, then at the
degree-ten root i the four globally full neighbors v,j,b,k form an induced
four-cycle: jk is blue because Petersen is triangle-free, and vb is blue.
This contradiction establishes

    maximum degree of P[C_b]<=1 for each full b.         (7)

If k_b=4, cubic edge counting gives e(P[C_b])=3+e(P[Z_b]). The six-point
matching has at most three edges; Z_b is independent. The five independent
four-sets of KG(5,2) are its ground stars S_t, containing the four pairs
through t. For completeness, four pairwise intersecting ground pairs must
share a point: otherwise {a,b},{a,c} force a pair avoiding a to be {b,c},
and no fourth distinct pair can meet all three. The checker also exhausts
all ten-point four-subsets and verifies that these are exactly the five stars.

Each S_t occurs at most twice among full four-rows. Two equal rows already
have six common red A-neighbors, so their B pair is blue. For two globally
degree-ten blue endpoints in order 22, common red and common blue counts
are equal. The blue cap six thus forces their outside red stars to be
disjoint. Three equal rows would require three disjoint four-sets among the
remaining eight B points, impossible. Write mu_t in {0,1,2} for their counts.

The full large multiset is empty, one five, one six, or two fives, with
repetitions considered before caps. Complete subset enumeration of (7)
gives thirty five-words and eighty six-words. Red pair capacities leave
456 full large choices. The seven full rows satisfy

    sum(mu_t)+number of full large rows=7.              (8)

No assumption that another full root is Petersen, no dirty-neighbor row
condition, and no host automorphism enter these arguments.

## 3. Two complete algorithms and entrywise agreement

A key is `(four low words, full large words, mu)`. The four deficit-one
words and the full large words are separately sorted **numerically**, with
repetitions allowed. They are not sorted by size. These orderings simply
relabel equally tagged outside vertices.

[produce.py](produce.py) first generates all low pairs within size budget
twelve, including repetitions. Every actual pair has that budget: the other
two low words have combined size at least ten and all four total at most
22. Reject repeated red pairs. The 137,193 pairs before these caps become
39,666 pairs at 3,351 ten-column sum vectors. Pack each count in a base-eight
digit; every pair coordinate is 0,1,2.

Exhaust all 456 full large choices and all mu in {0,1,2}^5 satisfying (8),
22,575 choices in total. Subtract their seven full columns from five; require
residual r_i in {0,1,2,3,4} and full-only blue capacities at most three.
For each first-pair column vector p_i in {0,1,2}, require
0<=r_i-p_i<=2. Equivalently: a residual zero forbids its union, a residual
one forbids its intersection, a residual three requires its union, and a
residual four requires its intersection. Residual two imposes no condition.
The packed subtraction then has no borrow and joins the exact second-pair
table. Require the low words a<=b<=c<=d numerically and all red pair sets
disjoint. Each blue field is at most 3+2+2=7, so its base-eight addition
has no carry; its bit of value four detects every count exceeding three.

Every genuine incidence appears: its full choices, multiplicities and
unique sorted first-two/last-two low decomposition are exhausted, and it
satisfies these necessary capacities. There is no cutoff or heuristic
rejection. Producer counts are 15,895 residual vectors, 7,310,635 valid
pair-column splits, 2,293,995 matched splits, 8,315,072 ordered exact joins,
279,330 red-capped joins, and **55,080 final keys**.

[verify.py](verify.py) imports no producer. It starts from a fixed literal
Petersen adjacency table, generates C subsets for the low/full pools, and
checks the table against the ground labels. Its different low-pair quotient
join credits the mechanism of 8785. The five integer forms on ground-pair
coordinates a_ij are

    a_03-a_13-a_02+a_12,
    a_04-a_14-a_02+a_12,
    a_0i+a_0j-a_ij-a_01-a_02+a_12     (ij=23,24,34).

They vanish on each S_t column and the constant column five. Index all
red-capped low pairs by total size and the sum of these forms. If the full
large surplus above four is h, the four low words must total 22-h. For a
first pair choose the second pair of the demanded total size and opposite
quotient sum after accounting for the full large rows. Check a<=b<=c<=d and
all red pair capacities. No quotient rank, converse or surjectivity is assumed.

The checker independently covers every full large choice under the explicit
120 ground permutations before these joins. It verifies preservation of its
literal P, actual orbit disjointness and exact union of all 456 choices.
The eleven canonical full large tuples and their actual orbit sizes are

    ():1, (31):30, (31,47):60, (31,115):30,
    (31,241):120, (31,527):15, (31,625):60, (31,740):60,
    (63):60, (183):5, (207):15.

At each canonical full large tuple, generate every sorted low quadruple
satisfying the quotient join. Recover mu from the residual columns r_ij by

    2*mu_0=r_01+r_02-r_12, mu_j=r_0j-mu_0.

Require integrality, 0<=mu<=2, (8), all ten equations mu_i+mu_j=r_ij, and
the thirty blue pair capacities. A blue local pair belongs to exactly one
ground star, so its four-row contribution is the corresponding mu_t; this
membership table is verified. These recovery formulas uniquely recover each
genuine solution. Expand all canonical-tuple keys through every ground map;
the union covers all raw incidences. This does not require a classification
of Aut(P), since the actual explicit maps and complete unions are checked.

There are respectively 5,100,680,60,34,84,8,106,38,86,156,12 keys before
these expansions, totaling 6,364. Their raw expanded counts are respectively
5,100,20,400,3,600,1,020,10,080,120,6,360,2,280,5,160,780,180, totaling
**55,080**. The two complete raw sets matched entrywise in the author audit.
For a reader, the producer requires its certificate orbit union to equal its
complete raw census, and the checker independently requires that same union
to equal its different complete census. Equality is not inferred just from
a hash. The five exact size patterns are:

| low sizes, sorted for display | full large sizes | keys |
|---|---|---:|
|5,5,5,5|5,5|23,460|
|5,5,5,5|6|6,120|
|5,5,5,6|5|20,400|
|5,5,5,7|none|1,620|
|5,5,6,6|none|3,480|

Canonical compact-JSON incidence SHA256:

    7e6367f5996a84527e2fcd43927def7806a136c1cb7c22185a1f17fdee377569.

## 4. Every local template and every outside red star

The producer takes the smallest uncovered key, moves all words and mu
through the 120 ground permutations and sorts only the equally tagged rows.
It checks actual orbit sizes, disjointness, membership and complete raw union.
A completion transports by relabeling A and B; this is not a host symmetry
assumption. The 478 templates have orbit size histogram
`20:1,30:2,40:1,60:32,120:442`, weighted to 55,080 keys.

The checker instead expands each supplied representative and verifies that
it is minimum, the size is correct, and the full disjoint union equals its
independently generated key set. Order B by the four numeric low words,
the full large words, then the S_t repeated mu_t times in increasing t.
At each b exhaust every subset D_b of B minus {b} of size k_b-delta_b.
The exact red bi pages, i in C_b, are

    |N_P(i) intersect C_b| + |D_b minus W_i|.

The exact blue bi pages, i in Z_b, are

    k_b-1-|N_P(i) intersect Z_b| + |(W_i minus {b}) minus D_b|.

The producer retains precisely those stars obeying all ten mixed-spine caps.
For stars x at b and y at c require reciprocal membership c in x iff b in y.
A red bc pair has `10-|Z_b union Z_c|+|x intersect y|` pages. A blue bc
pair has `1+|Z_b intersect Z_c|+|E_b intersect E_c|`, where
E_b=B minus ({b} union x), and similarly for c.

The separate checker constructs full physical neighborhood sets with root0,
A=1..10 and B=11..21, removes the endpoint from each complement, and counts
literal common red or blue neighbors. It rebuilds every initial star domain
and verifies all eleven sizes and its hash in
[certificate.json](certificate.json). Immutable in-memory caches are keyed
by complete incidence keys with fixed P/tags, contain only freshly computed
exact values, and import no saved domains or private data.

## 5. Static certificates exclude every completion

**448 templates**, weighted to **51,710 keys**, have an actually empty
initial star domain. For each of the remaining **30 templates**, weighted
to **3,370 keys**, the certificate partitions one complete initial target
domain into disjoint groups. Each group names another outside point whose
complete initial domain contains no compatible star for any target value in
that group. The checker exhausts every potential support using literal pages,
checks the masks and memberships, and verifies an exact partition. These
covers use **50 groups and 216 target stars**.

If a valid completion existed, its actual target star would belong to one
group and its actual star at the named other point would be a compatible
support in that point's complete initial domain. This contradicts the checked
obstruction. No domain deletion, iterative propagation, solver status,
branching, symmetry of the host, or incomplete enumeration is used. The
checker rejects every certificate type except the two stated static forms.

Root--A spines have three pages, root--B obey (1), A--A obey (3), A--B
obey the complete star domains, and B--B obey reciprocity and the literal
pair oracle. Every actual completion would obey these conditions; every one
of the complete necessary incidences has an obstruction. This proves the
new finite rooted theorem. Canonical certificate SHA256:

    5bdeb920b929a0104cddca836292358ee3fcee3088c666566cbc6fe5ef7b4e77.

## 6. Combining only the specified ordinary premises

Assume a valid 108-edge, maximum-ten graph has a full root. Its total
nonnegative integer deficit is 220-216=4. By 8828 the root is Petersen.
Since the root and all its red neighbors are globally degree ten, every
positive deficit lies outside it. The five possible partitions are
`4`, `3+1`, `2+2`, `2+1+1`, `1+1+1+1`. The rooted finite statements of
8941, 8979, 9041 and the present theorem exclude each of them. This proves
rootlessness for the entire maximum-ten 108-edge class. Only then use the
upper-degree part of 8012 to remove the explicit maximum-ten hypothesis.

For clarity, the elementary low-point count also recovers the two remaining
degree profiles. This is the known counting mechanism of
[8939](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/rootless108_marked_profiles/PROOF.md),
reproduced here rather than imported as a classification. Let L be the ell
positive-deficit points and H the other 22-ell points. Rootlessness forces
each point of H to have a red neighbor in L. Thus

    22-ell <= e(H,L) = 10*ell-4-2*e(L).                 (9)

It fails for ell<=2. Since positive deficits total four, ell is three or
four, yielding `8^1,9^2,10^19` or `9^4,10^18`. Neither profile is asserted
realizable. The existing rootless seven-one-nine-root bound of 8987 and
subsequent dirty-root restrictions remain separate prior results; they are
not needed for the present theorem. Full-root column bounds cannot be
transferred to dirty roots, whose low neighbors alter their column sizes.

## 7. Reproduction, controls and scope

CPython3.11.2 with standard-library exact integers and sets suffices.
[README.md](README.md) gives all required sequential normal and optimized
commands. The producer regenerates the entire incidence set and certificate;
the checker independently regenerates its entire census, every local orbit,
and every literal star domain. Default modes compare full summaries in
[expected.json](expected.json). All mathematical and schema guards use
explicit exceptions and remain active under Python -O.

The published primary21 fixture was fetched live and matched byte for byte.
Off-diagonal zeros are red:93 red/117 blue edges with page maxima3/6. Using
its actual local graph and tags at its unique degree-ten root, the same
literal oracle accepts ten actual outside stars and the completion;196
asymmetric degree-preserving changes reject. This is prior art and positive
validation, not a new construction. Fixture SHA256 is
3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55.

Geometry controls check P, its common neighbors, all five independent
four-sets, ground-star pair memberships and all four low-size possibilities.
Thirty-two deliberately invalid signed frames check137 blue-intersection
identities, including18 negative cap slacks; these are identity controls,
not witnesses. [controls.py](controls.py) tests omitted/duplicated coverage,
wrong tags, numeric ordering, incidence words, orbit sizes and domain hashes,
false emptiness, actual supported stars falsely claimed unsupported, omitted
or overlapping static covers, and attempted propagation in the static schema.
A separate required summary mode rejects a frozen summary falsely narrowing
the size-six low domain from210 to200. Exact rejection counts are in
expected.json; normal and -O outputs must agree.

All complete jobs use the unchanged1CPU/2GiB scope with all native threads
one and a fixed45-second child guard. A private resumable census additionally
had a35-second outer checkpoint budget and complete full-large-choice
boundaries. Neither incomplete chunks nor a timeout would imply exclusion.
The final standalone producer and checker completed within the same limits.
No private ledgers, keys, raw incidence corpus or generated star corpus are
published. [provenance.json](provenance.json) records exact premise roles;
[manifest.json](manifest.json) records compact source bytes and hashes.

The primary tables rechecked2026-10-01 retain
[22<=R(B4,B7)<=23, Table1](https://arxiv.org/pdf/2407.07285) and
[Small Ramsey Numbers, TableIXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf).
The [primary construction](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
is reproduced; the published upper23 certificate was not replayed. Bounded
literature, repository and committed graph checks calibrate this increment;
they do not establish exhaustive historical priority or the Ramsey endpoint.
