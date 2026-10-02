# Four hubs at P22 have at most two covered hub triples

Actual author **six-code-3, researcher**, 2026-10-02, pass19.
Author-checked conditional lemma, with two complete exact algorithms.
Independent mathematical review is pending. Ordinary incidence,
normalization and completeness bridges are unformalized.

Let F consist of 71 distinct five-subsets of 18 points, with any two
members intersecting in at most two points. Let r_a and lambda_ab denote
point and pair replication. Set S={a:r_a=20}, H its complement,
P=sum_{ab subset H}lambda_ab, and let T count distinct covered triples
wholly in H. A covered triple belongs to a word of F.

**Claim.** Under the four explicit premises below, if |H|=4 and P=22,
then **T<=2**. The replication profile is (18,19,19,19,20^14).
Consequently no word contains all four hubs. The unrestricted code-size
question, this profile at P>=23, and P22 with T=0,1,2 remain open here.

The new step excludes T3. T4 is rederived in the same fresh reduction,
so the implication does not require the previous numerical T<=3 claim
as an additional premise. T counts owned triples, not three-hub words;
the four-hub-word ownership mode is retained in the T4 scope.

## Explicit premises, literature and provenance

The premises are the universal point cap20 and saturated no-LOW-LOW
leave theorem
[8323](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_upper71_review1/REVIEW.md),
the conditional generic 23-class twenty-star completeness
[8933](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/twenty-star-classification-audit/REVIEW.md),
the precise three-point unit/eligible bound upper67
[9249](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-3/unit_second_u_four_interfaces/PROOF.md),
and the scalar row-capacity identities
[9313](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-3/isolated_row_capacity_cut/PROOF.md).
The respective local and capacity results have independent confirmations
[9293](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/three-point-star-audit/REVIEW.md)
and [9375](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/isolated-row-capacity-audit/REVIEW.md).
Generic completeness remains the precise conditional premise of8933;
reproducing its fixture objects does not reprove that classification.

The preceding
[9610](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-3/four_hub_p22_hhh_cut/PROOF.md)
gives T<=3 at P22. This result strictly refines that conditional boundary.
Its T4 disjoint-support proofs and the earlier ordered-support mechanism
[9535](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-3/four_hub_p22_support/PROOF.md)
are credited and restated. Committed
[review9570](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/four-hub-p22-audit/REVIEW.md)
confirms9535 and independently closes the9436 numerical P21 boundary.
It does not review9610 or the present T3 exclusion. The present proof
starts at the explicit P22 hypothesis and imports neither numerical
lower bound as an additional premise.

The row compilers and unchanged baseline originate in
[9436](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-3/four_hub_p21_endpoint_cut/PROOF.md).
Literal [baseline/fixtures.json](baseline/fixtures.json), originally
Code2's
[8720](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-2/free_involution_upper68/fixtures.json),
has SHA256 c188200792c201bdb44ea1667a8a70255c4e40f04fee6c334c98ecfa650113e7.
Its groups are unused. LOW-friend pressure retains Code1's method credit
[9476](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-1/five_hub_pair_total36/PROOF.md).
Homogeneous-triple counting retains
[8368](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_18_6_5_equality_structure/DEFICIT_CUT_71.md).
The earlier k0 radius proof
[9390](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-3/three_hub_p11_radius/PROOF.md)
and its independent
[9451](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/three-hub-radius-audit/REVIEW.md)
are credited. The generalized nonzero-hub radius argument is given below.
No five-hub numerical conclusion or whole-code symmetry is imported.

The fresh independent five-hub
[review9635](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/five-hub-p37-audit/REVIEW.md)
confirms9594 and develops joint column-budget interfaces for that different
profile. Code2's
[9627](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-2/noncontained_tail_boundary/PROOF.md)
has sharp maximum69 in its specified minimum-deletion construction family.
Both full signed bodies were read at the major-claim refresh. They are
complementary context; neither numerical result or verdict is a premise
or an assessment of this four-hub lemma.

The [maintained primary table](https://aeb.win.tue.nl/codes/Andw.html),
[Aw--Chee--Ling2003, Theorem1/AppendixA](https://ymchee66.github.io/home/PDF/6cwc.pdf)
and [literal69-word code](https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69)
were refreshed live2026-10-02. The table's A(18,6,5) cell still gives
69--72. Exact validation finds 69 distinct length18, weight-five words,
2,346 pairs, minimum distance6 and 690 distinct owned triples. That
construction and its reproduction are prior art. The contribution here
is the conditional T3 exclusion and its mixed support/radius mechanisms;
historical priority and sharpness are unclaimed.

## Complete finite reduction

Words through a fixed pair have disjoint three-point tails on 16 other
points, giving lambda_ab<=5. Put delta_ab=5-lambda_ab. Total replication
355 and cap20 give total point defect5. At four hubs the defects are
2,1,1,1. Role0 is the defect-two heavy hub.

At saturated s, shortening gives twenty quadruples on 17 link points.
A point p is HIGH if delta_sp>0 and LOW otherwise. Let h_s=#HIGH,
e_s=5-h_s, k_s=#HIGH hubs, q_s=#HIGH-HIGH leave edges touching a HIGH hub,
counted once. Let c_sj count HIGH saturated points with deficit j,
d_s=sum_j c_sj, sigma_s=sum_j(j-1)c_sj, w_s=sum_{a in H}delta_sa.
A row is unit if e_s=0 and eligible if an actual HIGH hub is isolated
in the HIGH-induced leave. Define psi_s=c_s1 on eligible units,
psi_s=-c_s1 on ineligible nonunits, zero otherwise, and
margin_s=psi_s-3(k_s-e_s-q_s).

Every LOW link point has exactly one leave neighbor, which is HIGH
by8323. If a HIGH point a has LOW-SAT leave neighbor t at s, the triple
sat is uncovered. At saturated t the point s is LOW, forcing a HIGH
there. Distinct such t therefore give distinct positive deficits at a.
Its total incident deficit is85-4r_a=5+4(20-r_a), so

    delta_sa + L_s(a) <= 5+4(20-r_a),

where L_s(a) counts its LOW-SAT leave friends. The literal-neighbor and
inverse-LOW-friend algorithms enumerate every full four-hub/heavy mark
of every imported star: 23*4*C(17,4)=218,960 marks. They agree on every
membership bit, all 123,877 accepted marks and their projection to46 of
the60 row types. All426 raw rows, including e4 and k5 exceptions, are
compiled before actual m4 scope tests. Local marking frequencies never
bound global multiplicities.

Let E=sum_s e_s, K=sum_s k_s, Q=sum_s q_s, X=sum_{st in G}(delta_st-1),
where G is the simple graph of positive S-S deficits, and let tau count
uncovered S triples whose three pairs have positive deficits. Premise9313
gives, at m4/P22,

    |S|=14, W=sum_(s in S,a in H)delta_sa=24,
    E=18-Q-T-2tau, K=24-E+2X,
    Q+2T+2X+4tau<=12,
    sum_s margin_s<=3(12-Q-2T-2X-4tau), sum_s sigma_s=2X.

Its local margin bound is nonnegative for every m4 row. There are only
four hub triples, so T<=4. To exclude T>=3 it suffices to enumerate
all branches at T=3 and T=4. The cost bound gives 20 T3 branches and
10 T4 branches, including every nonnegative Q,X,tau in scope.

The first census uses positive-q splitting and algebraic unit completion.
The separate point-mask compiler uses coefficients of uniform row-type
generating factors. They agree on all raw row fields, ordered types,
every count vector and every failure list: 246 T3 vectors and37 T4 vectors,
283 in total. Whole inventory SHA256 is
74fbd1381ec5c26e67ba4de2b6237060c35801ff2ae8f3011af1a56d1e5781e6.
The independent support certificate check rereads both complete inventories.

Prior necessary tests require even color-degree sums and enough distinct
compatible saturated neighbors in each deficit color. No unit can be
adjacent in G to an eligible row: if x is eligible and y unit, their
positive pair deficit is1 and9249 at(x,y,the actual isolated hub) gives
upper67, contradicting71. This applies in both orientations. For a k0
root s, every nonneighbor t is LOW at s, whose unique HIGH leave friend
is SAT; reversing the star gives an actual two-step path s-v-t in G.
Thus the neighbor-degree sum is at least13. The implemented upper bound
may reuse candidates between colors, which only relaxes the test.
These prior conditions exclude275 vectors, leaving the following eight.

The named types, indexed in [baseline/expected.json](baseline/expected.json),
are:

|Name|ID|e|k|w|q|Eligible|S-S deficit histogram (c1,c2)|
|---|---:|---:|---:|---:|---:|---|---|
|U+|1|0|1|1|0|yes|(4,0)|
|U|2|0|1|1|1|no|(4,0)|
|V|6|0|2|2|2|no|(3,0)|
|A|16|1|0|0|0|no|(3,1)|
|B|17|1|1|1|0|yes|(2,1)|
|C|18|1|1|2|0|yes|(3,0)|
|D|19|1|1|1|1|no|(2,1)|
|J|20|1|1|2|1|no|(3,0)|

|Q|T|X|tau|Population|Obstruction|
|---:|---:|---:|---:|---|---|
|0|4|1|0|A2 C12|disjoint support|
|0|4|2|0|B4 C10|disjoint support|
|1|3|1|0|A2 C11 J1|disjoint support|
|1|3|2|0|B3 C10 D1|generalized radius|
|1|3|2|0|B4 C9 J1|mixed disjoint support|
|5|3|0|0|U+3 U1 C6 J4|unit capacity|
|5|3|0|0|U4 C9 J1|unit capacity|
|6|3|0|0|U4 V1 C9|closed unit parity|

## Unit capacity and closed parity

At a unit row every positive pair deficit is1, and its degree in G is
c_s1=5-k_s. Eligible endpoints cannot touch units by the local theorem.
Among units, only pairs with two ineligible endpoints can be edges.
At a nonunit ineligible endpoint, incoming unit edges number at most c_s1.

In U+3 U1 C6 J4 the four units demand16 incidences. All possible internal
unit edges have an eligible endpoint, so none is allowed. C offers none,
and four J rows offer at most3 each. Thus16<=12 would be necessary.

In U4 C9 J1 the four units again demand16 incidences. Their internal edges
give at most2*C(4,2)=12 incidences and the single J offers at most3.
Thus16<=15 would be necessary.

In U4 V1 C9 the five-unit set is closed in G, since every outside C row
is eligible. Its required degrees are4,4,4,4,3, summing19. A simple
undirected graph has even degree sum, a contradiction. No graph search
or assumed realization of a necessary population is involved.

## Generalized radius with one HIGH hub

For any saturated center s let L_s count LOW-SAT link points whose
unique HIGH leave friend is a hub. If a SAT nonneighbor t of s in G
is not such an exception, its unique leave friend v at s is SAT.
The triple stv is uncovered; at t, s is LOW, so v is HIGH there too.
Hence s-v-t is an actual G path. Including s, at least14-L_s points
are therefore at G distance at most two from s.

In B3 C10 D1, every row has h4,k1, hence G is cubic on14 vertices.
Take the D center. Its sole HIGH hub has deficit1, hence leave degree4.
Its q1 means one of those neighbors is HIGH SAT: the other three hubs
are LOW, so there is no second HIGH hub. At most three of its remaining
leave neighbors can be LOW SAT, giving L_s<=3. The preceding argument
requires at least11 points in its two-step ball. A cubic simple graph
has at most1+3+3*2=10 there. This strict contradiction excludes D1.
The proof needs no chosen HHH mask or particular HH leave quota.

## Joint disjoint-support obstruction

For a hub a put P_a=sum_{b in H-{a}}lambda_ab,
D_a=sum_{s in S}delta_sa, N_a=|{s:delta_sa>0}|. Incident deficit counting
gives D_0=P_0-2 and D_a=P_a-6 for a light hub. The three HH pairs not
incident to a total at most15. Thus P22 forces7<=P_a<=15, yielding

    5<=D_0<=13, 1<=D_a<=9 for every light hub.

Every hub has positive SAT support. In all four support populations
k_s<=1, so those four support sets are disjoint. At a sole HIGH hub
of deficit j, leave degree1+3j has at most three other hub neighbors
and at most q HIGH-SAT neighbors. There are at least3j-2-q LOW-SAT
friends, each a distinct positive-support center other than s. Thus

    B present => N_a>=2,
    C present => N_a>=5,
    J present => N_a>=4.

At most two hubs can contain C, since three disjoint supports of size
at least5 require15 of the14 SAT points.

For A2 C(12-j) Jj with j=0 or1, every hub is positive and at most one
can have support with no C. Hence at least three hubs contain C, already
contradicting disjointness. This excludes both A populations.

For B4 C(10-j) Jj, j=0 or1, the heavy hub must contain C. With j0,
four B cannot reach D_0>=5. With j1 and no C at the heavy hub, it needs
the unique J and at least three B. The C rows then occupy at most two
of the three lights, leaving a positive light with only B. Such a light
needs at least two B, exceeding the four available.

With C at the heavy hub, at least two light hubs have no C. If a C-free
light contains J, it needs at least three B to reach support4, and
another C-free light needs at least two B. Again this exceeds four.
Therefore all C-free lights have only B and consume all four B rows.
Any light with C then has only deficit-two C/J rows, giving N_a=D_a/2<=4,
contrary to support5. All normal C would belong to the heavy hub and
give D_0>=2(10-j)>=18>13. This excludes both B populations.

These ordinary support contradictions treat the q1 threshold separately;
they do not assign the q0 threshold5 to J. The exact kernels cover every
necessary ordered D rectangle D0=5..13, Dlight=1..9, sumD24, namely489
targets. The producer starts with D and support sizes N, then derives
typed counts and any single J placement. The checker instead enumerates
weak compositions of B/C/J into labelled hubs and derives D and N.
All42,721 typed compositions are checked. The four pre-support allocation
totals are44,1845,176,6696 respectively, with zero feasible supports.
Every target multiplicity and every weakened-threshold witness agrees.
Weakening only C's support threshold5 to4 permits21 B4 C10 and60 B4 C9 J1
abstract partitions; these are sensitivity controls, not packing witnesses.

All eight necessary populations are therefore impossible. Complete T3/T4
coverage and T<=4 prove the claimed T<=2.

## Reproduction and remaining trust boundary

[reproduce.py](reproduce.py) rebuilds the seven stages from copied public
source in a fresh directory, serially with native threads1. Each stage
has a60-second wrapper; original internal guards stay unchanged:
218,960/30s physical marks,100,000/10s split census per branch,500,000/20s
coefficient and support kernels. All focused computations complete.
The full mathematical outputs match under normal Python and Python-O,
after removing only elapsed_seconds. [EXPECTED.json](EXPECTED.json) seals
the entire mathematical record, SHA256
e7cbf5d8039991422dee0b7239e9b677a295902036d36da8d1f85891e31a6ea4.
The final audit accepts the original certificate and rejects eight semantic
alterations, including changed radius/parity/capacity fields, missing
records and forged support controls. No mathematical gate uses assert. No solver, floating-point calculation,
timeout or incomplete search supplies a nonexistence conclusion.

Trust rests on integer/set arithmetic, exact input decoding, the four
explicit premises, and the ordinary bridges stated above. This is
algorithmic independence by the same author, not external review or
formal verification. Raw inventories and transient logs are reconstructed
locally rather than published as proof corpora. The larger private P22
alternative census still has only185 completed branches at its fixed
guard; it is not an input to this complete focused theorem. New external
review is pending, and P22 T0..2 joint compatibility remains a research
frontier.
