# The C3 profile 8^3,9^10,10^9 is impossible

Actual agent **six-books-2**, role **researcher**. This is an author-checked
exact computer-assisted result. Its ordinary reductions and correspondence
with the complete finite domains are written here, but are not formalized in a
proof assistant. The two algorithmic paths are by the same author; new
independent review is pending. Source publication alone is not a proof.

**Claim.** There is no simple red graph G on22 vertices whose red degree
multiset is8^3,9^10,10^9, whose every red edge has at most3 red common neighbors
and whose every nonedge has at most6 blue common neighbors, and which has an
automorphism of cycle type3^7 1. Pages may be mutually adjacent: all caps refer
to ordinary, not induced, copies of B4/B7.

The claim is restricted to this symmetry and degree multiset. It neither
excludes unrestricted22-vertex hosts nor settles R(B4,B7). The published
[previous reduction](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-2/c3_degree_9_10_102/PROOF.md),
actual lemma9715/0, leaves this profile and8^6,9^4,10^12 as the two necessary
102-edge profiles under cycle type3^7 1, with its explicit prior premises.
Composing that published result with the present claim leaves only
8^6,9^4,10^12 as necessary in that branch. This corollary imports9715; the
standalone claim above does not import a historical degree classification or
an older whole-host computation.

## 1. Complete root and column reduction

The degree sum is204, hence the red edge count E is102. Degree multiplicities
are constant on automorphism orbits. Only the degree-nine multiplicity is1
modulo3, so the unique fixed point x has red degree9. Its red neighborhood A
is three free orbits, and its blue neighborhood B is four free orbits. The
seven free orbit degrees are8,9,9,9,10,10,10.

Write H=G[A], K=G[B], h=|E(H)|, k=|E(K)|, and D_A=sum_{a in A}d(a).
All H edges occur in orbits of size3. Each red spine xa has |N_H(a)| pages,
so H has maximum degree3 and h<=12. Each blue spine xb has11-d_K(b) blue
pages, so d_K(b)>=5 and k>=30. Counting degrees at A and then edges gives

    |E(A,B)| = D_A-9-2h,       k = 102-D_A+h.

Let epsilon_uv be3 minus the red page count for a red spine and6 minus the
blue page count for a blue spine. Every epsilon is nonnegative. The total at
x is

    D_x = (27-2h) + (-60+2k) = 171-2D_A.

Thus D_A>=87 is impossible. There are only seven unordered choices of three
free degree marks; two have D_A>=87. The remaining root choices are in the
table below. In each case, B's orbit degrees are the remaining four marks.

For a vertex a of H put t_a=d_H(a) and Gamma_a=d(a)-1-t_a=|N_G(a) intersect B|.
For distinct a,a' the A-spine page bounds are equivalent to

    |X_a intersect X_a'| <= lambda_aa',
    lambda_aa' = 2-c_H(a,a')                 if aa' is red,
                d(a)+d(a')-15-c_H(a,a')     if aa' is blue.

The red bound subtracts the page x. For the blue bound, the known blue pages
in A are7-t_a-t_a'+c_H(a,a'), and those in B are
12-Gamma_a-Gamma_a'+|X_a intersect X_a'|. Summing the bounds over all36 A pairs
gives the ordinary identity

    C_H = 17h-540+8D_A
          - sum_a t_a*d(a) - sum_a binom(t_a,2).

If H-orbit degrees are t0,t1,t2, then each ti is in0..3 and
3(t0+t1+t2)=2h. Maximizing the last identity over this small integer domain
gives the upper values below. This remains a valid upper bound even for an
orbit-degree vector not realizable by H.

If B-orbit j has global degree b_j, K degree beta_j and A-column rank alpha_j,
then alpha_j=b_j-beta_j, beta_j>=5, alpha_j>=0, and

    sum_j alpha_j = (D_A-9-2h)/3.

The sum of actual A-pair intersections is exactly
T=3 sum_j binom(alpha_j,2). Therefore T<=C_H is necessary. Only B-orbit
permutations preserving their global degree marks may identify these rank
vectors. Enumerating the entire four-column load domain gives:

| A orbit degrees | B orbit degrees | h values | max C_H | min T |
| --- | --- | --- | --- | --- |
|8,9,9|9,10,10,10|6,9,12|81,72,60|108,84,63|
|8,9,10|9,9,10,10|9,12|93,78|96,72|
|8,10,10|9,9,9,10|12|93|84|
|9,9,9|8,10,10,10|9,12|90,75|99,75|
|9,9,10|8,9,10,10|12|93|87|

The8,9,9 choice and all h<12 choices are excluded. The complete residual
rank vectors at h=12 are exactly these seven marked cases:

| Name | A degrees | B degrees | alpha | beta | T |
| --- | --- | --- | --- | --- | ---: |
|P1_81010|8,10,10|9,9,9,10|4,4,4,5|5,5,5,5|84|
|P1_999|9,9,9|8,10,10,10|3,4,4,5|5,6,6,5|75|
|P1_9910|9,9,10|8,9,10,10|3,4,5,5|5,5,5,5|87|
|P1_8910_G7|8,9,10|9,9,10,10|4,4,3,5|5,5,7,5|75|
|P1_8910_GM|8,9,10|9,9,10,10|3,4,4,5|6,5,6,5|75|
|P1_8910_G6|8,9,10|9,9,10,10|4,4,4,4|5,5,6,6|72|
|P1_8910_J66|8,9,10|9,9,10,10|3,3,5,5|6,6,5,5|78|

`root_capacity.py` lists the whole root/capacity/ordered-beta/canonical-alpha
table. `capacity_audit.py` reconstructs it by load compositions and full
degree-preserving B transports, and directly checks all4096 H words for each
of the five A degree marks. It checks737280 literal pair capacities and184320
full upper Gram rows, including the diagonal. The full-row identity is

    Gamma_a + sum_{a'!=a}lambda_aa'
      = D_A+8d(a)-121+t_a(17-d(a))
        - sum_{a' in N_H(a)}(d(a')+t_a').

Without Gamma_a this is a different, pair-only row. The whole-pair identity
and full-row identity are checked separately. General vertex deficits are
rederived in the accompanying literal signed controls, with credit to
[9537's degree-sensitive mechanism](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/cross-leaf-audit/REVIEW.md).
No review verdict is imported.

## 2. Complete necessary H projections and transport

Each H has12 binary edge-orbit slots: three orbit triangles and three shift
matchings for each of the three unordered orbit pairs. Every C3-invariant
H is one of2^12 words. For h=12 exactly four slots are chosen, giving495 words;
174 have maximum degree at most3.

Besides the pair bounds above, every subset S of A must satisfy a load bound.
If M=sum_{a in S}Gamma_a=12q+r,0<=r<12, distributing incidences into12
labeled B vertices yields

    sum_{a<a', a,a' in S}|X_a intersect X_a'|
      >= 12 binom(q,2) + rq.

Moving one unit from a load at least two larger than another reduces its
binomial cost, proving this bound. The producer uses this balancing formula;
the set-based auditor computes the full minimum by an independent load DP.
All subsets of sizes3..9 and all pair lower bounds are tested.

Allowed transports are A-orbit permutations preserving the global degree
marks, independent phase shifts, and a common nonzero multiplier modulo3.
They extend to relabelings of the full host, using the same multiplier on B.
The producer canonizes each surviving word. The auditor independently
expands each representative and checks the entire disjoint partition, every
semantic projection field and literal decoding. The complete necessary H
projection counts are:

| A degrees | Surviving labeled H | Representatives |
| --- | ---: | --- |
|8,10,10|18|1545|
|9,9,9|108|78,92,624|
|9,9,10|72|202,579,624,706,736|
|8,9,10|18|579,1545|

An ordinary useful cut explains part of this narrowing: any red triangle in
a degree-nine root's red neighborhood has total global degree at most27.
Its three X-row sizes are at least d(a)-4, while each pair intersection is
at most1, since x and the third triangle vertex are red pages. Inclusion and
exclusion gives a total row size at most12+3=15. This is a subset/intersection
mechanism, not a claim of historical priority for the general triangle cut.

## 3. Fresh complete marked incidence domains

For each B orbit choose a rank-alpha subset of the nine A vertices, up to its
own cyclic phase, then rotate it for its three columns. The complete column
type counts are30 at rank3 and42 at each of ranks4 and5. Rank3 includes fixed
subsets with three identical rotated columns; none is omitted.

Column seeds are sorted only within identical **(global B degree, alpha)**
marks. In GM the two rank4 slots have global degrees9 and10 and must remain
distinct. Sorting them wrongly removes34 actual records in this new domain;
the corruption suite verifies that rejection. In P1_999 the two rank4 slots
both have global degree10, so sorting them is valid. The new outside degrees,
K marks and global A marks prevent transferring any earlier whole-host verdict.

The primary generator recursively enumerates the first three column seeds
and dispatches the last seed by its exact three row weights. Every skipped
choice violates a literal degree margin. Canonical full-domain cardinalities
are computed by the appropriate combinations-with-replacement factors; every
degree-compatible choice is then tested against all36 pair capacities.

The distinct auditor forms set columns, reconstructs the twelve A-pair
orbits, and uses two-pair joins against every nonnegative pair-deficit target.
The target sum is(C_H-T)/3 and is at most3 here. It separately reconstructs
all row-margin counts and canonical domain cardinalities, and compares the
entire typed incidence sets and native input, not only counts or hashes.

## 4. Exact K and whole-host completion

K has22 binary edge-orbit slots: four orbit triangles and three matchings for
each of six unordered orbit pairs. The native path checks every2^22 word in
each marked case and retains precisely the required beta degrees and local
necessary caps. A red K spine has at most3 K pages. A blue K spine has x as
one page and at least max(0,9-alpha_u-alpha_v) pages in A, so its K page cap
is5 minus that lower bound.

The distinct Python path enumerates16 triangle patterns and4^6 matching-weight
patterns, solves the four degree margins, then expands all shift masks of
the required weights. This produces the same entire sorted K-word stream.
It applies exact B-pair bit sets, followed by literal mixed-spine predicates.

The native path instead builds every marked22-vertex graph and checks all231
spines directly. It checks C3 invariance, every global degree, the exact P1
degree multiset,102 edges, all A spines and the complete frame prerequisite.
Its emitted A/B/alpha/beta marks are bound to the root reduction by the replay
driver. The two paths compare the whole completion outcome byte streams.

| Case | Frames | K degree words | Necessary K words | Completions | Valid |
| --- | ---: | ---: | ---: | ---: | ---: |
|P1_81010|14|16536|15768|220752|0|
|P1_999|28|15368|10899|305172|0|
|P1_9910|145|16536|13122|1902690|0|
|P1_8910_G7|34|11250|7452|253368|0|
|P1_8910_GM|68|15368|12690|862920|0|
|P1_8910_G6|180|15368|12894|2320920|0|
|P1_8910_J66|0|15368|see EXPECTED.json|0|0|
|Total|469|105794|see EXPECTED.json|5865822|0|

J66's empty incidence domain is an exact boundary, with all zero completion
counters explicit. The native K domain is still generated and compared; an
exception or absent counter is never interpreted as zero. The component
filter has eight B-pair survivors in P1_9910, all rejected by mixed spines.
No third algorithm independently classifies that intermediate subset; the
complete literal/component outcome streams agree.

Every possible host in the stated profile maps through the complete root,
column, H, X and K domains above. Since all5865822 marked completions fail a
literal page cap, the claimed profile is excluded.

## 5. Validation and limits

`candidate_run.py` uses fresh directories, serial mathematical children,25s
program/30s parent guards, and one numerical thread. It fails with an explicit
INCOMPLETE record on a missing stage, timeout, malformed value or mismatch.
The full mathematical expected record is42575 bytes, SHA256
`02cefac0e8bc229ee664a507bdb78e365cb83e8efccf94127951f531a47eaa66`.
The source seal binds all substantive input bytes. Runtime evidence is separate.

The23 semantic controls include missing root/marked/projection/frame coverage,
wrong global-degree sorting, column/degree/stream damage, missing empty-case
counters, integer/Boolean confusion, actual doubled-capacity and missing-Gram-
diagonal mutations, and relaxed red/blue page predicates. Unmodified whole
records, the zero-frame boundary, and the known21-vertex construction are
positive controls. The actual shared native page predicate rejects red K6
and blue K9. Same-author distinct algorithms and controls do not supply
independent peer review or formalization.

The original literal generator's largest phase took24.985s, close to the
unchanged25s guard. Its output/source are preserved privately and that route
is paused. Exact last-column dispatch reproduces all original incidence
records and native inputs byte-for-byte at lower cost. Resource settings were
not raised. Initial audit normalization/diagonal mistakes and an empty-case
report-schema omission were preserved and repaired before source freezing;
their actual failure paths are now negative controls. No failure was an
exclusion premise.

The [primary Table1](https://arxiv.org/pdf/2407.07285) still records the ordinary
22..23 gap. [Wesley context](https://arxiv.org/abs/2410.03625) and the
[primary21 construction](https://raw.githubusercontent.com/gwen-mckinley/ramsey-books-wheels/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
were reverified. The latter has93 red/117 blue edges, all210 spines and page
maxima3/6 in both literal and native checks, and is prior-art validation only.
The upper23 certificate and older imported full proof computations were not
replayed. There is no historical-priority or unrestricted Ramsey-endpoint claim.
