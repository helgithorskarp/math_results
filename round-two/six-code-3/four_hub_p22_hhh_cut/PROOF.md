# Four hubs at P22 have at most three covered hub triples

Actual author **six-code-3, researcher**, 2026-10-02, pass18.
Author-checked conditional lemma. The ordinary bridges are unformalized;
independent mathematical review of this result is pending.

Let F be71 distinct five-subsets of18 points, any two intersecting in
at most two points. Write r_a for point replication, lambda_ab for pair
replication, S={a:r_a=20}, H its complement, and P=sum_{ab subset H}lambda_ab.
Let T count distinct covered triples wholly in H.

**Claim.** Under the four explicit local/scalar premises below, if
|H|=4 and P=22, then **T<=3**. Consequently no word contains all four
hubs. The hub profile is (18,19,19,19,20^14). Both ways of covering all
four hub triples are excluded: four distinct three-hub words, or one
four-hub word. The numerical P>=22 boundary is unchanged; the whole
profile and the unrestricted code-size question remain open.

## Premises, provenance and literature

The mathematical premises are the universal point cap20 and saturated
no-LOW-LOW leave theorem
[8323](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_upper71_review1/REVIEW.md),
the conditional23-class twenty-star completeness
[8933](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/twenty-star-classification-audit/REVIEW.md),
the precise unit/eligible three-point theorem
[9249](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-3/unit_second_u_four_interfaces/PROOF.md),
and the scalar capacity identities
[9313](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-3/isolated_row_capacity_cut/PROOF.md).
The local theorem has independent confirmation
[9293](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/three-point-star-audit/REVIEW.md);
the capacity identities have
[9375](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/isolated-row-capacity-audit/REVIEW.md).

The preceding conditional P>=22 theorem
[9535](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-3/four_hub_p22_support/PROOF.md)
provides the ordered-support mechanism, rederived below. Fresh committed
[review9570](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/four-hub-p22-audit/REVIEW.md)
confirms that theorem and the separate9436 numerical P21 boundary,
removing the latter as an unreviewed numerical premise in its own proof.
That review does not assess this new T4 exclusion. The present implication
starts at the explicit hypothesis P22 and needs neither numerical lower
bound as an additional premise.

The row compilers and unchanged baseline are credited to
[9436](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-3/four_hub_p21_endpoint_cut/PROOF.md)
and9535. Literal [baseline/fixtures.json](baseline/fixtures.json), originally
[Code2/8720](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-2/free_involution_upper68/fixtures.json),
has SHA256 c188200792c201bdb44ea1667a8a70255c4e40f04fee6c334c98ecfa650113e7.
The supplied groups are unused. Reproducing those fixtures does not prove
generic completeness;8933 remains an explicit external dependency.
LOW-friend pressure retains Code1 method credit
[9476](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-1/five_hub_pair_total36/PROOF.md).
The homogeneous-triple method retains
[8368](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_18_6_5_equality_structure/DEFICIT_CUT_71.md)
credit. The ordinary radius proof used in the finite reduction is restated
below, with
[9390](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-3/three_hub_p11_radius/PROOF.md)
and its independent
[9451](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/three-hub-radius-audit/REVIEW.md)
credited. No five-hub numerical conclusion is imported.

The [maintained primary table](https://aeb.win.tue.nl/codes/Andw.html),
[Aw--Chee--Ling2003, Theorem1/AppendixA](https://ymchee66.github.io/home/PDF/6cwc.pdf),
and the [literal69-word code](https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69)
were refreshed live2026-10-02. Its69 distinct weight-five words,2346 pairs,
minimum distance6 and690 distinct owned triples were exactly revalidated.
That construction and its reproduction are prior art. The new campaign
information is the focused T4 exclusion at P22 and the joint support
argument, with historical priority unclaimed.

## Definitions and complete finite domain

Disjoint three-point tails of a fixed pair give lambda_ab<=5; put
 delta_ab=5-lambda_ab. Total point replication355 and cap20 give total
point defect5. At four hubs the defects are2,1,1,1; role0 is heavy.
At saturated s its20 shortened quadruples form a pair packing on17 points.
A link point is HIGH when delta_sa>0 and LOW otherwise. Put h_s=#HIGH,
e_s=5-h_s, k_s=#HIGH hubs, and q_s=#HIGH-HIGH leave edges touching a
HIGH hub, counted once. Let c_sj count saturated HIGH points of deficit j,
d_s=sum_j c_sj=h_s-k_s, sigma_s=sum_j(j-1)c_sj, and
w_s=sum_{a in H}delta_sa. A row is unit if e_s=0 and eligible if an actual
HIGH hub is isolated in the HIGH-induced leave. Define psi_s=c_s1 on
eligible units, psi_s=-c_s1 on ineligible nonunits, zero otherwise, and
margin_s=psi_s-3(k_s-e_s-q_s).

Each LOW link point has a unique HIGH leave friend by8323. For a HIGH
point a at s, each LOW-SAT leave neighbor t of a gives an uncovered
triple sat. At t, s is LOW, so the same theorem forces delta_ta>=1.
These are distinct positive-support centers. The total pair deficit at
a point is5+4(20-r_a). Hence delta_sa+L_s(a)<=5+4(20-r_a). Both literal
HIGH-to-LOW neighbor sets and the inverse LOW-friend compiler screen
all218960 full H4/heavy marks. They agree on all membership bits:
123877 marks survive and project to46 of the60 types. All426 raw rows,
including genuine e4 and k5 exceptions, are retained until explicit
physical/statistic tests. Diagnostic local frequencies never cap global
row multiplicities.

Let E=sum_s e_s, K=sum_s k_s, Q=sum_s q_s,
X=sum_{st in G}(delta_st-1), with G the positive-deficit graph on S,
and tau=#uncovered S triples whose three pairs have positive deficits.
At m4/P22 the scalar identities and capacity inequality give

    n=14, W=sum_(s in S,a in H)delta_sa=24,
    E=18-Q-T-2tau, K=24-E+2X,
    Q+2T+2X+4tau<=12,
    sum_s margin_s<=3(12-Q-2T-2X-4tau), sum_s sigma_s=2X.

These identities retain a possible four-hub word: T counts covered
triples, not three-hub words. There are only four hub triples, so T<=4.
For the contradiction T4, all ten branches with Q0..4,X0..2,tau0..1
and Q+2X+4tau<=4 are enumerated. A positive-q split plus algebraic unit
completion and an independent uniform generating-factor coefficient
engine agree on every raw row, type, count vector and failure list.
The complete census has37 vectors.

The prior necessary tests require even color-degree sums and enough
compatible distinct neighbors for each color. A unit cannot be adjacent
to an eligible row by both orientations of9249. For a k0 center s, a
nonneighbor t is LOW at s, whose unique HIGH leave friend v is SAT.
The t-star makes v HIGH too, so s-v-t is an actual path. All13 other
saturated points are within two steps. Thus the sum of neighbor degrees
is at least13. The implemented colorwise maximum can reuse a candidate
between colors, giving a conservative upper bound. These tests exclude
35 vectors.

|Q|X|tau|Raw vectors|Remaining|
|---:|---:|---:|---:|---:|
|0|0|0|0|0|
|0|0|1|1|0|
|0|1|0|1|1|
|0|2|0|1|1|
|1|0|0|1|0|
|1|1|0|5|0|
|2|0|0|6|0|
|2|1|0|2|0|
|3|0|0|13|0|
|4|0|0|7|0|

The two necessary populations are **A2 C12** and **B4 C10**, both Q0,tau0.
Type IDs are16,17,18 in [baseline/expected.json](baseline/expected.json):

|Kind|e|k|w|q|Saturated deficit histogram (c1,c2)|
|---|---:|---:|---:|---:|---|
|A (16)|1|0|0|0|(3,1)|
|B (17)|1|1|1|0|(2,1)|
|C (18)|1|1|2|0|(3,0)|

A has no positive hub deficit; B has exactly one, of value1; C has
exactly one, of value2. Passing the census is only a necessary condition.

## Joint disjoint-support obstruction

For a hub a put P_a=sum_{b in H-{a}}lambda_ab,
D_a=sum_{s in S}delta_sa and N_a=|{s:delta_sa>0}|. Direct incidence gives

    D_0=P_0-2, D_a=P_a-6 for a light hub.

The three HH pairs not incident to a have total at most15. Since P22,
**7<=P_a<=15**. Therefore

    5<=D_0<=13, 1<=D_a<=9 for every light hub.

In particular every hub has positive SAT support. A HIGH hub of deficit
j has local leave degree1+3j. At most three such neighbors are other
hubs. Since q_s=0, none is HIGH-SAT; at least3j-2 are LOW-SAT friends.
Each is a distinct positive-support center other than s, as proved
above. Consequently a B center forces N_a>=2 and a C center forces
**N_a>=5**. These are actual distinct-center counts, not weighted mass.

In both populations k_s<=1, so the four positive-support sets are
pairwise disjoint. Thus at most two hubs can have C centers: three
would need at least15 of the14 SAT centers.

For A2 C12, every positive-support center is C. Every hub has D_a>0,
so all four hubs would need support at least5, contradicting disjointness.

For B4 C10, the heavy hub has D_0>=5. Only four B centers exist, so the
heavy hub must have a C center. At most one light hub can also have C
centers. Hence at least two light hubs have only B centers. Each has
positive D and needs support at least2, using all four B centers.
Any light hub with C centers would then have only deficit-two centers;
N_a=D_a/2<=4, contradicting N_a>=5. All ten C centers would therefore
belong to the heavy hub, giving D_0>=20>13, also impossible.

This ordinary obstruction excludes both census survivors, independently
of any assumed HH leave quotas, chosen HHH mask, word ownership mode,
light-role orbit or realization of a necessary row graph. The complete
T4 census therefore gives T<=3. A four-hub word owns all four hub
triples, so such a word is also excluded under the stated hypotheses.

## Exact checks and scope

The support producer enumerates every necessary labelled D rectangle
D0=5..13,Dlight=1..9,sumD24, then its typed support sizes. The separate
checker starts with weak compositions of the B and C counts and derives
D and N. Every target and pre-support multiplicity matches; no support
allocation survives. Positive abstract partitions and a weakened-support
sensitivity control check that the kernel is neither empty by definition
nor insensitive to the support5 threshold. These controls are not code
constructions.

[reproduce.py](reproduce.py) reruns all six stages from copied public
source in a fresh work directory, serially with native threads1. Normal
and Python -O must match every complete output, after removing only
elapsed_seconds. [EXPECTED.json](EXPECTED.json) seals the entire
mathematical record, SHA256
f4a1bfafd5df3c7ae7b164a4b9f25a8ee05597850e447b035a6de5f55d389fa4.
No mathematical gate relies on assert. Integer/set arithmetic, decoded
fixtures and the four named imported premises are the computational and
mathematical trust boundaries; ordinary incidence/coverage/support bridges
are unformalized. No solver, floating-point argument or resource status
is used as a proof.

The larger P22 exploration has a complete one-engine205-branch census
and only185 completed branches of its alternative producer before a
fixed guard. It is private, incomplete as a two-engine whole-domain
classification, and is not an input to this focused proof. The fresh
T4 engines here independently complete their whole ten-branch scope at
the original guards. The T0..3 joint compatibility frontier remains open.
