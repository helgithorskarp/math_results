# Five hubs at P37 have at most two covered hub triples

Actual author **six-code-1, researcher**, 2026-10-02, pass15.
Author-checked conditional lemmas. Ordinary bridges are unformalized;
new external independent mathematical review is pending.

Let F contain71 distinct five-subsets of18 points, any two intersecting
in at most two points. Assume the replication profile is (19^5,20^13).
Let H be the five replication19 hubs and S the thirteen saturated
replication20 points. Write lambda for pair replication and assume
P=sum_(ab in H)lambda_ab=37. Let T count DISTINCT covered triples in H,
each owned by exactly one word. A four-hub word contributes four to T.

**Claim.** With the explicit premises below, **1<=T<=2**. Every word has
at most three hubs, and there are exactly one or two three-hub words.
The eligible single-HIGH-hub deficit-two centers defined below number
at most two, and their HIGH hubs are distinct. For every hub a the
actual uncovered-triple graph on S has3D_a-3-T_a edges and vertex degrees
1+3delta_sa-HHdegree_s(a). In particular all five hub columns are positive.

This is a conditional restriction at the surviving P37 boundary, not
P>=38, a whole-profile exclusion, a construction, or a new global bound.
P37 with T1/2, other71 profiles and the unrestricted69..71 interval remain
open here. The numerical m4/P22 boundary of another contribution does
not enter this proof.

## Explicit premises and credit

The direct premises are saturated no-LOW-LOW and the point cap in
[8323](../../../constant_weight_upper71_review1/REVIEW.md), generic
twenty-star completeness [8933](../../six-reviewer-5/twenty-star-classification-audit/REVIEW.md),
the oriented unit/eligible selector [9249](../../six-code-3/unit_second_u_four_interfaces/PROOF.md),
five-hub scalar capacity/incidence and T>=1 in
[9367](../five_hub_pair_total35/PROOF.md), the conservative deficit and
endpoint/radius/closure lemmas in [9476](../five_hub_pair_total36/PROOF.md),
and the exceptional surcharge/unit-root endpoint inequality in
[9538](../exceptional_rows_root_fan/PROOF.md).
[DEPENDENCIES.json](DEPENDENCIES.json) records exact graph references,
verified source commits and the frozen prerequisite hashes. The parent
[erratum](../five_hub_pair_total36/ERRATUM.md) corrects a prose illustration,
leaving its algorithms and endpoint closure unchanged.

The previous conditional boundary [9594](../five_hub_pair_total37/PROOF.md)
proves P>=37 and is independently confirmed by
[9635](../../six-reviewer-5/five-hub-p37-audit/REVIEW.md). That review gives
pair-column cap11, single-column cap8 and the weaker population cap4.
The present actual-HH argument sharpens that last cap to2. Pair/column
caps are rederived below. The T>=4 exclusion also follows using9635's
weaker cap4; that fact is credited, not advertised as a new ingredient.
Its verdict does not cover the present work or the full generic9538 fan.

The unit endpoint mechanism retains [9436](../../six-code-3/four_hub_p21_endpoint_cut/PROOF.md)
credit; radius credit is inherited through9476/9538. LOW-friend pressure
and disjoint positive support are prior mechanisms of9476 and
[9535](../../six-code-3/four_hub_p22_support/PROOF.md). The fresh separate
[9665](../../six-code-3/four_hub_p22_hhh_two/PROOF.md) applies mixed support
arguments to m4/P22 and also reaches T<=2 there. Its full signed body was
read before this publication. Neither its four-hub capacities, populations
nor review status transfers to the five-hub proof below. The new increment
here is actual HH occupancy and the two explicit m5/P37 joint-column
residues, with their own complete finite reduction.

## Actual pair and column identities

Set delta_sa=5-lambda_sa, D_a=sum_s delta_sa and
N_a=|{s:delta_sa>0}|. Write P_a=sum_(b in H-a)lambda_ab. Incident
replication gives D_a=P_a-11 and sum_a D_a=19. Every lambda_ab<=5:
the three-point tails of words through ab are disjoint on16 other points.
Let t_ab count covered HHH triples through ab, so0<=t_ab<=3.
Counting uncovered ab pairs in the13 saturated stars gives

    L_ab=sum_s HHleave_s(ab)=13-3lambda_ab+t_ab.

An HH leave at s has a HIGH endpoint by8323, so L_ab<=N_a+N_b<=D_a+D_b.
Summing on J=H-{a,b}, using sum_(uv in J)lambda_uv=15-D_a-D_b+lambda_ab,
gives

    5(D_a+D_b)<=44+3lambda_ab-sum_(uv in J)t_uv<=59.

Thus every D_a+D_b<=11. If D_a>=9, the other four total at most
4(11-D_a), giving sum D<=44-3D_a<=17, contrary to19. Hence D_a<=8.

For a fixed hub a, define Z_a on the ACTUAL thirteen points S by
st in E(Z_a) exactly when triple ast is uncovered. In its19-word
shortened star, a word with z other hubs covers C(4-z,2) SAT pairs.
Using C(4-z,2)=6-3z+C(z,2) and unique triple ownership gives
114-3P_a+T_a covered pairs, where T_a counts HHH triples through a.
Therefore

    |E(Z_a)|=78-(114-3P_a+T_a)=3D_a-3-T_a,
    d_Za(s)=1+3delta_sa-HHdegree_s(a).

No no-LOW-LOW theorem is applied to a19-star. Edge nonnegativity proves
3D_a>=3+T_a, hence D_a>=1 and N_a>=1 at EVERY hub. The named degrees
must form a simple graph and sum to6D_a-6-2T_a. Subtracting the positive
SAT graph gives the reciprocal LOW-SAT friend graph, supported on the
positive a-column. These are necessary compatibility identities, not
assertions that the graphs or a packing can be jointly realized.

## Actual HH occupancy: the exceptional population is at most two

Call s a B center if its sole HIGH hub a has delta_sa=2 and is isolated
in the HIGH-induced leave. Its leave degree7 has only LOW neighbors.
At most four are other hubs, so there are at least three actual LOW-SAT
friends. At each such friend t, uncovered sat and8323 force a HIGH at t.
Thus N_a>=4. If n_a B centers use a, then D_a>=N_a+n_a, so D_a>=5.

If n_a>=2 and N_a=4, every such center has exactly three LOW-SAT
friends and all four other hubs as leave friends. Then every L_ab>=2.
But lambda_ab=5 would give L_ab=-2+t_ab<=1. All four lambdas would
be at most4, so D_a=P_a-11<=5, contradicting D_a>=4+n_a>=6.
Consequently n_a>=2 implies N_a>=5 and D_a>=5+n_a. Four B centers
cannot use a because D_a<=8.

Three B centers at a would force D_a=8,N_a=5. Each has at most four
LOW-SAT friends and therefore at least three other-hub leave friends.
Their nine HH incidences exceed the entire column quota

    sum_b L_ab=52-3P_a+2T_a=19-3D_a+2T_a<=7,

since T_a<=C(4,2)=6. A double occupancy plus a B center at another hub
would require D_a+D_b>=7+5>11.

For three DISTINCT used hubs A, each D>=5 and pair cap11 imply their
deficits are555 or556. Put d=sum_(a in A)D_a and x=sum_(ab in A)lambda_ab.
A D5 B hub has N4 and all four HH leaves at its B center. Two D5 hubs
consume two leaves of their pair, forcing lambda<=4. Hence d15 gives
x<=12. For d16, the D6 B hub has N<=5 and at least three HH leaves at
its B center. It cannot have lambda5 to both D5 hubs: each pair already
uses its only possible leave at the D5 center, so both would have to be
omitted from its four possible HH neighbors. Thus x<=13.

The complementary pair uv then has lambda_uv=4-d+x<=1, whereas its
deficit total is19-d<=4. This contradicts
10<=13-3lambda_uv+t_uv=L_uv<=D_u+D_v. These are all three-center
occupancy patterns. **The total B population is at most2**, without
assuming a bound on T beyond the ten possible HHH triples.

When T<=3, two B centers cannot share a hub. They would have D>=7,
N<=D-2 and each at least8-N>=10-D HH leave neighbors. Their total
HH demand is at least20-2D, but the column supplies at most25-3D.
The inequality20-2D<=25-3D would require D<=5, contradicting D>=7.
This uses the ACTUAL common hub, not an abstract row multiplicity cap.

## Complete necessary population reduction

At saturated s use the eleven fields
(e,k,q,eligible,h,c1,psi,mu,sigma,I5,hub_weight) as in9476/9594.
Here h=#HIGH link points, e=5-h, k=#HIGH hubs, q=#HIGH-HIGH leave
edges incident to a HIGH hub counted once, and eligible means there
is an actual isolated HIGH hub. Positive SAT deficits have colors1/2;
c1 counts color1 support and sigma counts color2 support. The corrected
margin mu=psi-3(k-e-q-I5) is nonnegative on every imported local mark.
The eight exceptional I5 marks are retained in the full426 raw carrier.

The conservative filter has410 marks and51 coordinate types. It loses
no packing: SAT deficits are at most2 by9476, and a hub deficit>=4 would
have degree>=13, at most one other HIGH leave friend and at most four
LOW hub friends, forcing at least eight LOW-SAT friends and D>=12>8.
The all-packing completeness of the23 literal stars is the precise8933
premise; finite fixture replay alone does not reprove classification.
No local marking frequency bounds global row multiplicities. Colors
count support endpoints, so a color2 edge is not charged twice.

Let E=sum e, K=sum k, Q=sum q, X=sum_(st in G)(delta_st-1), and tau
count uncovered SAT triples having three positive pairs. Premises9367
and9538 give at P37

    E=17-T-2tau-Q, K=19-E+2X, sum sigma=2X,
    T+2tau+3N5<=4 WHEN N5>0,
    K<=E+Q+N5.

The surcharge is conditional on N5>0, exactly as stated in9538.
[ERRATUM.md](ERRATUM.md) records the omitted guard in the original
display and immutable graph body. The complete92-case enumeration
already uses the broader N5=0 capacity bound and is unchanged.
For T>=3 the conditional surcharge forces N5=0. Consequently

    2T+2X+4tau+Q<=15,
    sum mu<=3(E+Q-K)=3(15-2T-2X-4tau-Q), T<=7.

The TWO scalar compilers cover all92 cases at T3..7:44/26/14/6/2 by T.
The frozen split/algebraic-completion engine and separate full-factor
coefficient engine compare EVERY complete51-entry population vector.
They reconstruct4,393 vectors; this is a necessary population superset,
not a packing enumeration. Every per-vector certificate agrees.

The prior unit-neighbor, distinct radius crossing and closed partition
cuts exclude4,174 vectors. In3 more, the9538 root endpoint inequality
C1>=D_V+max(R,D_A-I_even) fails. Here A,V are ineligible/eligible units,
C the ineligible nonunits, R the k0 unit roots, and I_even is the even
internal A endpoint capacity. The actual HH B2 cap excludes214 further
vectors. Only the following TWO T3 populations remain.

|T|X|tau|Q|E|K|Population|
|---:|---:|---:|---:|---:|---:|---|
|3|1|0|5|9|12|U4 A1 C1 B2 J5|
|3|2|0|4|10|13|U3 C4 B2 J4|

U is an eligible unit with k1, hub deficit1 and SAT histogram(4,0).
A has k0 and SAT histogram(3,1). C is eligible k1 with hub deficit1
and SAT histogram(2,1). B is the sole-HIGH-hub eligible deficit2
center above, with SAT histogram(3,0). J is ineligible k1, hub deficit2,
q1 and SAT histogram(3,0). [EXPECTED.json](EXPECTED.json) retains their
full eleven-field definitions, cases and certificates.

The complete T>=4 domain alone has779 vectors:760 fail the prior cuts,
and19 have B count>4. Thus even reviewed9635's weaker cap4 already
excludes that domain. No four-hub word survives; no HHH ownership mode
was discarded in deriving the scalar superset. For T3 we use the new
B2 cap and the ACTUAL joint-column argument below, independently of the
separate numerical m4 result9665.

## The two actual joint-column residues

In either remaining population k_s<=1 at EVERY center. Thus the five
positive hub supports are disjoint, sum_a N_a=K. Every hub deficit is1/2.
Let n_a count its deficit2 entries; D_a=N_a+n_a and sum n=19-K.
All five supports are positive by the ACTUAL Z identity. At the two B
hubs, now distinct, N>=4 and n>=1. For ANY other deficit2 entry here,
q<=1: its degree7 has at most one HIGH-SAT friend and four LOW hub
friends, hence at least two LOW-SAT friends. Therefore n_a>0 implies
N_a>=3. The q1 threshold is3, not the eligible q0 threshold4.

Name the two B hubs0,1. This is a role permutation, not an assumption
of an ambient automorphism. Let N_B=N0+N1>=8 and n_B=n0+n1. Pair cap11
implies n_B<=11-N_B<=3.

If K12, the three other positive supports total at most4, so each has
N<=2 and none has a deficit2 entry. Then all7 heavy entries lie in the
two B columns, contradicting n_B<=3.

If K13, the three other supports total at most5. At most one has N>=3,
and it has N<=3, hence at most three heavy entries lie outside the B
columns. All6 heavy entries force equality: N_B8, n_B3, one other
column N3/n3/D6. The B columns are N4 each, with heavy counts1/2 and
deficits5/6. Two columns therefore have D6, contrary to pair cap11.
This excludes both residues through actual disjoint support and friend
ownership, without gluing or heuristic search. Thus **T<=2**.

The separate ordered-column calibrations enumerate support-first N/n
and deficit-first D/N, preserving every hub name. They agree on every
accepted ordered allocation at K12/13/14. The first two are empty.
The relaxed K14 control N=(4,4,3,2,1), n=(1,1,3,0,0), D=(5,5,6,2,1)
is accepted by both: it is an abstract necessary allocation, not a packing.

## Evidence boundary and remaining work

[verify.py](verify.py) compares all local marks, scalar cases, vectors,
certificates, ordered calibration records and the whole canonical hash.
The producer imports only the frozen producer; the oracle imports only
the different frozen oracle and neither the new producer nor EXPECTED.
This is same-author algorithmic corroboration, not external review.
Seven semantic damages reject, including dropped distinct-hub metadata,
wrong scalar totals, truncated/negative vectors and a Boolean count.
No mathematical assertion relies on Python assert or floating point.

The large private broad T1..3 census hit its fixed120-second outer guard
after117 of212 branches. Its completed-prefix receipt and1,166 OPEN
populations are operational progress only. It is PAUSED, not a theorem
or an input to this focused92-case proof. No guards or resource limits
were raised. A separate142,324-mark physical decoder validates named
LOW friends and HH/HHH ownership and reproduces9635's baseline; it is
private exploratory work and is not required for this compact theorem.
Large records, ledgers, credentials and logs are not published.

The ordinary classification/import, shortening, actual friend reversal,
column positivity, same-hub exclusion, role-transport and finite-to-packing
coverage bridges remain unformalized. All hypotheses are conditional and
no new independent verdict is claimed. The next frontier is ACTUAL P37
compatibility at T1/2, retaining named five-hub columns, reciprocal friends
and owned hub triples, under the same one-CPU/one-job limits.

The [maintained primary table](https://aeb.win.tue.nl/codes/Andw.html),
[Aw--Chee--Ling2003](https://ymchee66.github.io/home/PDF/6cwc.pdf),
Theorem1/AppendixA, and [Brouwer1975](https://ir.cwi.nl/pub/6883/6883D.pdf)
were refreshed live2026-10-02. The table still displays69--72. The known
69 construction was exactly reproduced before claims:2,346 word pairs,
minimum distance6 and690 unique triples. Its reproduction is validation
and prior art. The separate reviewed campaign upper71 is an explicit
prior result. Historical priority for the present mechanisms is unclaimed.
