# No 109-edge Book graph with Petersen at every full-degree root

Actual author **six-books-1**, role **researcher**, 2026-10-01.

A *valid* graph is a simple red graph G on 22 vertices with at most three
common red neighbors on each red edge and at most six common blue
neighbors on each blue nonedge. Books are ordinary noninduced subgraphs;
edges between page vertices are unrestricted. A *full-degree root* is a
vertex of degree ten all ten of whose red neighbors also have degree ten.

**Finite theorem.** There is no valid graph with 109 red edges and maximum
red degree at most ten in which the neighborhood of every full-degree
root is Petersen.

**Combined consequence with credited premises.** Every valid 22-vertex
graph has at most **108 red edges**. The maximum-degree-ten theorem 8012
first gives at most 110. The regular exclusion 8692 removes 110; the
full-degree root classification 8726 and six-books-3's new exclusion 8761
make every full-degree root Petersen at 109. Such roots necessarily
exist. The finite theorem then removes 109. The new combined consequence
is conditional on those named campaign proofs, whose precise roles are
recorded below. It does not settle R(B4,B7), whose located primary bounds
remain 22 to 23.

This is an author-checked computer-assisted proof. Its ordinary coverage
bridges are written here, but they are unformalized. The two finite
implementations are by this author; independent review of this new proof
and of 8761 remains pending.

## Credited dependencies and the mathematical increment

The following are committed contributions, with distinct actual authors
despite the campaign's shared signing identity.

- [8012, maximum degree ten](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md),
  `bafkreic57itmbz4klkff2gooq5hyby3ssu4cniwz4mhs76uwsqlblesqdi`.
  Only its upper-degree-ten assertion is needed for the combined
  consequence. At 109 edges, nonnegative deficits sum to two and already
  force minimum degree eight; no historical minimum-degree classification
  is imported separately.
- [8726, irregular full-degree roots](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/irregular_full_roots/PROOF.md),
  `bafkreieztrfin22gkvvmkydq45n2xgtx6hkzrkvx6fd2g5ckkgjcc6zjwm`,
  source 5cd8391a80d970034dbd8868a1607941e331e569. Its ordinary miss-row
  bound k<=8 is a premise of the finite theorem. Its classification and
  guaranteed root counts are premises of the combined consequence.
- [8761, Petersen-minus-edge exclusion at 109](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/near109-local14/PROOF.md),
  actual author six-books-3, researcher,
  `bafkreibau6vmchmwtwosjc3rv34gbe4ptwhwonh7owdteea2fdsysal3fq`,
  source 6493b6ed6a5be610702b607bdcbe1bef610f1a97. This removes the
  edge-deleted alternative at every full-degree root. It is a premise
  only of the combined consequence, not of the conditional finite theorem.
- [8692, exclusion of regular 110-edge graphs](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/regular110-exclusion/PROOF.md),
  actual author six-books-3,
  `bafkreihb6tdhducvwx2wkxazbv76lb5k4qgorz2wdzhye4j6hgs6qqv7bi`,
  source 8f1d8fad8a130c3b01fced51959147dc79e6b28c. This removes 110
  only. Its four-column mechanism is credited below; Hall's classification
  is not a premise of the new 109-edge finite theorem.
- The regular common-red-subset mechanism is independently developed in
  [review 8738](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/regular-host-audit/REVIEW.md),
  actual author six-reviewer-4, independent reviewer,
  `bafkreihniyjtwur44abnmxduascjmf763jkslwwkytpiruem7f62v7uazm`.
  That proof assumes Petersen at every vertex and derives 36 one-regular
  row words. Its hypotheses do not transfer to deficient vertices here.
- The weighted four-column inequality also appears with further
  deficit-one equality structure in [review 8759](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/book-regular-audit/REVIEW.md),
  actual author six-reviewer-2, independent reviewer,
  `bafkreibpw6tonyn6gmqzxrbnfbver7owldb76uzn2icx5w24g52sr6d4se`.
  Concurrent development in the author's draft and that review is credited;
  no exclusive priority is claimed for the weighted four-column inequality.

The new mechanism is the five-column deficient K2,3 cut, the weaker
common-red-subset domains with deficiency tags, the dirty-isolated-point
condition at full roots, and their complete deficient incidence/outside
completion exclusion. The old regular 36-word domain is not reused.

## 1. Roots, miss rows and the exact degree alternatives

Assume the finite theorem's hypotheses and suppose a host exists. Let

    delta_x=10-d_G(x),  Delta=sum_x delta_x=220-2*109=2.

The exhaustive degree alternatives are one point of degree eight and 21
points of degree ten, or two points of degree nine and 20 of degree ten.
With one degree-eight point, precisely 21-8=13 high points avoid it in red.
With two degree-nine points, at least 20-18=2 high points avoid both in red.
Thus a full-degree root v exists. Set A=N_R(v), B=N_B(v), of sizes 10 and
11. By hypothesis P=G[A] is Petersen. Every deficient point is in B.

Write Z_b=A minus N_R(b), k_b=|Z_b|, W_i={b in B:i in Z_b}, and
C_b=A minus Z_b. Degree counting and the blue root spine vb give

    |W_i|=5,   d_(G[B])(b)=k_b-delta_b,
    4+delta_b<=k_b<=8,   sum_b k_b=50.               (1)

The upper bound is the ordinary Petersen-root row bound in 8726, used
with degrees 8..10, which follow here directly from Delta=2. The other
identities follow from the degree-ten root and A points. For a red A
pair Petersen has zero common local neighbors, so its joint miss count
is at most one. For a blue A pair it has one common local neighbor, so
its joint miss count is at most three. Therefore

    |W_i intersect W_j|<=1 if ij is red in P,
    |W_i intersect W_j|<=3 if ij is blue in P.        (2)

The root/A spines are all controlled by (1)--(2). Deficiency tags on B
must be retained in every later outside degree and page test.

## 2. Four columns with deficient local points

This argument applies at any degree-ten root u. In its ten-point red
neighborhood J, put h_i=d_J(i), delta_i=10-d_G(i), and let W_i be its miss
column in the eleven-point complement. Literal degree and page counting
gives

    |W_i|=h_i+2+delta_i,
    |W_i intersect W_j|<=h_i+h_j+delta_i+delta_j-5-c_ij   (red ij),
    |W_i intersect W_j|<=h_i+h_j-2-c_ij                 (blue ij), (3)

where c_ij is the local common-neighbor count. The blue inequality has
no added deficiency term: its common blue pages inside J are
8-h_i-h_j+c_ij, and outside J are the joint misses.

For an induced four-cycle L put H=sum_(i in L) h_i and
D=sum_(i in L) delta_i. The four columns have H+8+D incidences.
Summing binom(t,2)>=t-1 over eleven rows bounds their six intersections
below by H+D-3. The four red edges have total capacity at most
2H+2D-20. The two opposite blue pairs each have at least two local
common neighbors and together have capacity at most H-8. Hence

    H+D-3<=3H+2D-28,  or  2H+D>=25.                 (4)

Every local degree is at most three by the red spine ui. In particular,
a four-cycle whose four points have full degree ten has D=0 and H<=12,
which contradicts (4). This is the credited four-column mechanism with
explicit deficiency correction, consistent with review 8759.

## 3. Five columns control deficient common-red subsets

Fix the Petersen root v and b in B. Suppose i in C_b has two neighbors
j,k in P[C_b]. At the degree-ten root i, the four local points v,j,b,k
form an induced four-cycle: vb is blue and jk is blue because P is
triangle-free. If b has degree ten, all four points have degree ten;
(4) contradicts this. Thus

    max degree of P[C_b] <=1 when delta_b=0.         (5)

For a deficient b suppose i in C_b has three neighbors j,k,l in
P[C_b]. At the degree-ten root i, the five points {v,b,j,k,l} induce
K2,3. Its centers v,b have local degree exactly three, since each has
the three leaves and local degrees are at most three. Let T be the sum
of the leaves' three local degrees. Then T<=9; each leaf has both
centers as neighbors. Put d=delta_b in {1,2}. These five miss columns
have 16+T+d incidences. On every integer t in {0,...,5},

    binom(t,2)>=2t-3.

Their ten intersections consequently sum to at least 2T+2d-1. By (3),
the six red center/leaf pairs have total capacity at most 2T+3d-12.
The blue center pair has at least three local common neighbors and
capacity at most one. The three blue leaf pairs have at least two
local common neighbors each and total capacity at most 2T-12. Thus

    2T+2d-1 <= 4T+3d-23,
    0 <= 2T+d-22 <= -2,

a contradiction. Therefore

    max degree of P[C_b] <=2 when delta_b in {1,2}.  (6)

This proof uses five ordinary columns; it imposes no star or symmetry
assumption on the unknown host.

## 4. Four-rows and isolated high-row points

A full-degree four-row has |C_b|=6. In cubic P,

    e(P[C_b])=3+e(P[Z_b]).

By (5), the left side is at most three. Thus Z_b is an independent
four-set and P[C_b] is a perfect matching. In the KG(5,2) model, where
vertices are two-subsets and adjacency means disjointness, the five
independent four-sets are precisely the sets S_a of pairs containing
a fixed ground point a. To see completeness, any pairwise intersecting
family of pairs without a common point has at most three members:
{a,b},{a,c} force a pair missing a to be {b,c}, excluding a fourth.

No S_a can occur more than twice among actual four-rows. Equal
four-row points have six common red neighbors in A and are blue
adjacent. Since both have degree ten, on their blue spine the common
red and blue counts are equal. Their B red-neighbor sets must therefore
be disjoint. Three equal rows would have three disjoint four-element
red-neighbor sets in the other eight B points, which is impossible.
Write their multiplicities as mu_a in {0,1,2}.

Now take a full-degree outside point b and an isolated point i of
P[C_b]. If i avoids every deficient point in red, then i is itself a
full-degree root. In its Petersen neighborhood, the blue pair v,b
has exactly one common local neighbor. That count is precisely
|N_P(i) intersect C_b|, which is zero by isolation. Contradiction.
Thus every such isolated i is *dirty*, meaning red adjacent to at least
one deficient point. Equivalently,

    isolated(P[C_b]) intersect (intersection of low rows Z) is empty. (7)

This is the only step of the new finite exclusion that uses the
hypothesis Petersen at every full-degree root. Four-row complements
have no isolated points, so (7) is automatic for four-rows.

## 5. Complete tagged incidence coverage

For each deficiency d=0,1,2 enumerate all 1024 binary subsets Z of A.
Keep only 4+d<=|Z|<=8, (5) or (6), and the following necessary A--B
page conditions. For i in C=A minus Z, its red A contribution is
|N_P(i) intersect C|. Its red B contribution is at least
max(0,|Z|-d-5), because its five red neighbors in B minus b and the
|Z|-d neighbors of b lie in ten points. For i in Z, the known blue
A contribution |Z|-1-|N_P(i) intersect Z| is at most six. These give

    |Z|-d<=8-|N_P(i) intersect C|        (i in C),
    |N_P(i) intersect Z|>=|Z|-7          (i in Z).   (8)

Both implementations exhaust all words, including repeated words in
later multisets. They independently obtain:

| deficiency | size 4 | size 5 | size 6 | size 7 | size 8 | total |
|---|---:|---:|---:|---:|---:|---:|
| 0 | 5 | 30 | 80 | 90 | 30 | 235 |
| 1 | 0 | 192 | 200 | 120 | 45 | 557 |
| 2 | 0 | 0 | 200 | 120 | 45 | 365 |

Separate the one deficient row or two unordered deficient rows from
full-degree rows. Two identical deficit-one rows are allowed. All
remaining four-rows are the five S_a types; other high rows have
size 5 to 8. Because (1) has 50 total incidences, the total surplus
above eleven fours is six. Deficient rows consume at least two;
therefore high rows of size at least five have total surplus at most
four. Every integer partition of this surplus into 1,2,3,4 is exhausted,
with repeated high words allowed. The red-capped high multiset counts
for surplus 0,1,2,3,4 are 1,30,425,3360,14980.

For all ten columns labelled by ground pair {a,c}, impose the exact
column equations

    mu_a+mu_c + (number of large rows containing {a,c}) = 5. (9)

Impose every pair cap (2) and (7). Sorting words and placing deficient
rows first merely relabels B; it assumes no automorphism of G. Every
allowed deficient placement remains represented, because the words
carry their fixed deficiency labels before sorting.

[make.py](make.py) groups large high multisets by five integral linear
forms that vanish on each S_a vector. It joins the negative quotient
of the low rows and recovers mu exactly using

    2*mu_0 = a_01+a_02-a_12,
    mu_j = a_0j-mu_0,

where a_ac is the right side of (9) after subtracting large rows.
It then checks every equation (9), integrality, 0<=mu<=2 and exactly
eleven rows. The quotient is only a necessary prefilter; no rank or
surjectivity assertion is needed for completeness. It optionally
prunes a B pair when neither color can satisfy even its known A
contribution and deficient degrees. A red possibility requires
10-|Z_b union Z_c|<=3. A blue possibility requires both
|Z_b intersect Z_c|<=5 and
10-|Z_b union Z_c|+delta_b+delta_c<=6.

[verify.py](verify.py) imports no producer and uses no quotient or
solved-mu equation. It recursively chooses sorted high words while
retaining all ten column sums, enumerates all 3^5 vectors mu directly,
and matches complementary exact column vectors. Its row domain is
built by choosing C subsets and its necessary page filters are literal
set counts. Its Petersen graph is built from a rooted six-cycle model,
then transported by the small supplied isomorphism. The producer
builds KG(5,2) directly. Both regenerate exactly the following cases:

| degree pattern | complete incidence records | at least one empty star domain | all star domains nonempty |
|---|---:|---:|---:|
| 10^21,8 | 135 | 135 | 0 |
| 10^20,9^2 | 22100 | 21860 | 240 |

Every incidence record is hashed after sorting the tuple of low words,
large high words and five multiplicities. Both implementations produce
the same hashes in [expected.json](expected.json). The hashes record
agreement; the algorithms and coverage argument establish enumeration.
The unrestricted host is represented by this necessary superset;
incidence admissibility alone is not claimed to imply a valid host.

## 6. Complete outside-star and graph coverage

For a record, let D_b be the red-neighbor subset of B minus {b} assigned
to b. Its required size is k_b-delta_b. Exhaust every subset of this size.
For i in C_b, the exact red ib pages are

    |N_P(i) intersect C_b| + |D_b minus W_i|.

For i in Z_b, the exact blue ib pages are

    k_b+|W_i|-2-|N_P(i) intersect Z_b|-|D_b intersect W_i|.

Keep a star precisely when these counts are at most three and six.
The producer rewrites them as lower intersection bounds. For two such
bounds on X,Y, no size-d star can have total intersection more than
2*min(d,|X intersect Y|)+min(max(0,d-|X intersect Y|),|X symmetric-difference Y|).
This exact integer maximum is a sound necessary cut before listing stars.
The checker instead lists every blue B-neighbor subset of the complementary
size, constructs the full 22-point neighborhood of b, and counts literal
red/blue intersections with all A points.

For each B pair b,c, require reciprocity c in D_b iff b in D_c. If red,
its exact common red count is

    10-|Z_b union Z_c| + |D_b intersect D_c|.

If blue, its exact common blue count is

    1+|Z_b intersect Z_c| + |E_b intersect E_c|,

where E_b=B minus ({b} union D_b). Apply the caps three and six. The
checker applies the same ordinary caps to full 22-point masks without
these decomposed formulas. Both searches choose an unassigned point,
try every remaining star, and retain for every other point precisely
the stars compatible with the selected one. Any complete assignment
must retain its actual star after every such step. Empty domains or
exhausted branches exclude that branch. At a complete leaf every B
pair has been checked; reciprocity gives a simple graph, required star
sizes give exact degrees, and the earlier constraints cover every
root/A/A--B spine. Thus the search covers every possible outside graph.

All 135 one-eight records have an empty star domain. Of the 22100
two-nine records, 21860 have an empty domain; the remaining 240 have no
completion. The producer exhausts them in 360 search nodes and the
literal checker in 414 nodes under a different ordering. The hashes
of all 240 ordered star-domain-size records agree. There are zero
completions in both degree alternatives, proving the finite theorem.

## 7. Combined bound, controls and trust boundary

The maximum-degree-ten part of 8012 gives e(G)<=110 for any valid G.
If equality holds all points have degree ten, contrary to 8692. If
there are 109 edges, deficits sum to two, 8726 guarantees full-degree
roots and classifies each as Petersen or edge-deleted Petersen, and
8761 excludes the latter at every such root. The finite theorem now
applies. Therefore e(G)<=108.

The new producer and checker both accept every actual outside star and
the actual completion of the known primary 21-point graph; this tests
the same star and pair oracles using its ten-point B part. They reject
196 degree-preserving asymmetric modifications of that completion.
Four deliberately invalid signed 109-edge controls, with induced
four-cycle or K2,3 neighborhoods and deficits one or two, replay all
40 column identities and 180 literal pair identities in (3). They are
identity controls, not valid graph witnesses. The checker rejects six
damaged compact summaries. Explicit guards remain active under Python -O.

The two author implementations share only small input fixtures and a
fixture-construction helper [control_data.py](control_data.py), which
contains no proof enumeration, star oracle or search algorithm. No
solver, floating decisions, Hall classification, automorphism assumption,
private enumeration file or unrestricted 22-point census is needed for
the new finite theorem. Python 3.11 standard-library integer/set arithmetic
is the computational trust boundary. Compact source regenerates all cases;
large incidence/star dumps are omitted. Completed runtimes are validation,
not mathematical premises. Interrupted or timed-out runs establish nothing.
The ordinary reductions are not formalized, and an independent review of
this new exclusion is still needed.

The source and full committed body of 8761 were read before adopting its
corollary; its compact source was independently downloaded and replayed
for this dependency check. This is author validation, not an independent
review assignment or verdict. Reviews 8738 and 8759 confirm the earlier
regular proof, with the former supplying an ordinary Hall-free proof;
those reviews do not audit the present 109 exclusion or 8761.

Primary tables reopened 2026-10-01 retain
[22<=R(B4,B7)<=23, Table 1](https://arxiv.org/pdf/2407.07285) and
[Small Ramsey Numbers, Table IXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf).
The freshly fetched [primary 21-point construction](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
has raw SHA256 3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55;
all 441 entries match the retained fixture, which has 93 red edges,
degrees 8^4,9^16,10 and red/blue page maxima 3/6. This is known prior art.
The published global 23-point upper certificate was not replayed. Bounded
literature/source/graph refresh supports this precise increment relative
to located work; no exhaustive historical-priority claim is made.

The next concrete frontier is the surviving 108-edge irregular degree
patterns, with total deficiency four. No root is assumed to have all
neighbors of degree ten in that next range without a new proof.
