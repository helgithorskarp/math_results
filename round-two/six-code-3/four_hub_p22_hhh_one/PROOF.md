# Four hubs at P22 have at most one covered hub triple

Actual author **six-code-3**, role **researcher**, pass20, 2026-10-02.
Author-checked conditional ordinary/computational argument. Independent
mathematical review and formalization are pending. The preceding committed
LEMMA9665, source3e6a0164d456579467a68e8d5aa3f0ddb11e7df2, gives T<=2.

Let F be71 distinct five-subsets of18 points, with two different members
intersecting in at most2. Assume the four explicit premises8323,8933,
9249,9313 from the [published preceding proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-3/four_hub_p22_hhh_two/PROOF.md):
[point cap20 and saturated no-LOW-LOW8323](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_upper71_review1/REVIEW.md);
[conditional generic23-class twenty-star completeness8933](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/twenty-star-classification-audit/REVIEW.md);
[precise unit/eligible upper67 interface9249](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-3/unit_second_u_four_interfaces/PROOF.md);
and [scalar row-capacity identities9313](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-3/isolated_row_capacity_cut/PROOF.md).
Their applicable independent confirmations are
[9293](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/three-point-star-audit/REVIEW.md) and
[9375](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/isolated-row-capacity-audit/REVIEW.md);
neither verdict covers this new result. In a saturated shortened star,
HIGH means positive pair deficit and LOW means zero. The no-LOW-LOW
premise says every leave edge has a HIGH endpoint. The classification
premise quantifies over every packing star, allowing normalization to
one of the23 fixtures without assuming an ambient code automorphism. Let H have four points with replication
18,19,19,19, let S be the14 replicate20 points, and P=sum_(ab in H)lambda_ab=22.
Let T count distinct covered triples in H.

**New claim:** T=2 is impossible. Together with the actual committed
conditional T<=2 result9665, this implies **T<=1** in this same profile.
No unrestricted endpoint or P>=23/profile exclusion is claimed.

## Column identities and necessary support conditions

Write delta_ab=5-lambda_ab, P_a=sum_(b in H-a)lambda_ab,
D_a=sum_(s in S)delta_sa, N_a=|{s:delta_sa>0}| and Z_a=D_a-N_a>=0.
Role0 is the defect-two heavy hub. Alpha=(2,6,6,6) and incidence counting
give D_a=P_a-alpha_a and sum_a D_a=24. If k_s counts HIGH hubs at a
saturated center s, then **sum_a N_a=K=sum_s k_s** exactly.

Let t_ab be the number of covered HHH triples containing ab. Exactly
L_ab=14-3lambda_ab+t_ab saturated centers have ab as a leave edge.
Three-point tails through a fixed pair are disjoint, so lambda_ab<=5;
no-LOW-LOW at each such center forces

    L_ab <= N_a+N_b.

For pair ab and complementary pair cd let M=D_a+D_b and
A_ab=alpha_a+alpha_b. The six HH-edge sum gives
lambda_cd=22+lambda_ab-A_ab-M. Substituting this into the leave bound
at cd and N_c+N_d=24-M-Z_c-Z_d gives

    4M+Z_c+Z_d <=76+3lambda_ab-3A_ab-t_cd.

Thus heavy/light deficit sum is at most16, light/light sum at most13.
Summing three heavy/light bounds gives D_0<=12. The complementary
light/light sum is at least24-16=8. These role bounds hold before
requiring any physical row assignment.

At T=2 there is no four-hub word: one would own all four HHH triples.
Each covered HHH triple belongs to its own three-hub word, so
lambda_ab>=t_ab. Local HHH masks are zero or one covered triple.
Different three-hub words through one SAT center would share two hubs
and that center. Every covered HHH triple appears at exactly two SAT
centers; its exact occurrence quota is relaxed in the support test.
For S14 the pair upper bound is floor((14+t_ab)/3); t_ab=1 permits5.

At a HIGH hub a in the star of s, let L_s(a) count its LOW-SAT leave
friends. Such a friend t satisfies delta_st=0 and the triple ast is
uncovered. At t, s is LOW, so a is HIGH there. Conversely s is the
LOW-SAT friend of a at t. Hence these pairs form a simple undirected
friend graph on the N_a positive-support SAT centers. Its exact local
degrees L_s(a) must have even total, and L_s(a)<=N_a-1. Local types may
repeat freely; marking frequencies never cap global multiplicities.

## Complete fresh T2 census

At T=2 the scalar identities are

    E=16-Q-2tau, K=24-E+2X,
    Q+2X+4tau<=8, sum sigma=2X,
    sum margin<=3(8-Q-2X-4tau).

Here e=5-h, k counts HIGH hubs, q counts HIGH-HIGH leave edges touching
a HIGH hub once, sigma=sum_(HIGH SAT)(delta-1), E=sum e, Q=sum q and
X=sum_(positive SAT pairs)(delta-1). Tau counts uncovered SAT triples
whose three pairs are positive. A unit has e=0; eligibility means an
actual isolated HIGH hub. Put psi=c1 on eligible units, -c1 on ineligible
nonunits, zero otherwise, and margin=psi-3(k-e-q). Premise9313 supplies
nonnegative local margins, and the displayed identities in this profile.

They give35 nonnegative branches:25 at tau0,9 at tau1 and1 at tau2.
Credited literal-set/split-unit and point-mask/uniform-coefficient
engines were frozen from the published9665 source, changing only
the focused T domain and output namespace. All guards remain100000
states/10s per split branch and500000/20s per coefficient branch.
The full426 rows and60 types are compiled before actual H4 tests.
The two complete physical-screen algorithms retain identical123877
memberships over all218960 marks and project to the same46 types.

Both census engines agree on every ordered branch/vector/failure list:
35 branches,1373 vectors. Necessary weighted-partner, color parity and
k0 radius conditions leave266 preliminary populations. For each deficit
color its endpoint sum is even and every row has enough distinct
compatible other endpoints. The unit/eligible interface9249 forbids a
positive pair joining any unit to an eligible row in either orientation:
the actual isolated hub would give an upper67 bound instead of71.
For a k0 SAT root, each nonneighbor has its unique HIGH leave friend
inside S; reversal gives a two-step positive-deficit path. Its neighbor
degree sum must therefore cover all13 other SAT points. The weighted
partner bound may reuse partners between colors, which only relaxes it. The earlier
17-case pilot was a list after additional cuts, and did not itself
provide this full coverage. The present argument checks all266
directly, without using those intervening graph-cut certificates.

## Complete joint-column computation

Full physical signatures are reconstructed here from the small literal
fixtures by two algorithms: literal neighbor sets with precomputed role
transports, and independent heavy-first marks with inverse LOW-friend
counts. They agree on every signature, frequency and minimum witness. Catalogue SHA256 is
e6c013d3b32257181d6b880e1ef1a79154eab8d3a036cf0d1d1ac62de37b0fd8.
All28 type IDs needed by the266 preliminary populations lie in its
complete44-type scope. That catalogue has7681 signatures over119397
actual marks/716382 role bijections. The44-type selection is literal
source data, and the packet proves coverage of every needed T2 type.
No generated private input or preceding wider population list is needed.

The global HHH masks and labelled HH lambda vectors are completely
generated in two different ways: first five lambdas plus the sum-forced
sixth, and bounded deficit compositions. Forward/inverse light-role
point maps agree on the entire3996-labelled/696-canonical carrier
stream. The heavy role is fixed and all six light-role renamings are
checked. Renaming the three light hubs changes no scalar population,
and transports the actual local rows and N columns. Choosing a minimum
carrier orbit representative is therefore valid without any assumed
automorphism of F.

For each carrier and each hub, the first kernel uses states
(deficit sum,positive support count,friend parity), storing the least
maximum friend support requirement. The second fixes N first, omits
physical row choices with L>=N, builds every type multiplicity factor
by weak compositions and checks the exact coefficient. The min-max recurrence preserves the least support requirement for
each exact (w,n,parity) state; a larger requirement with the same state
is dominated under all future max updates. At its end w=D and parity0,
N=n must dominate every required L+1. Since N<=D, pruning requirements
above D is safe. The fixed-N engine includes every weak composition
of each type multiplicity across its permitted (delta,parity) choices
and every sum of the resulting factors. Thus both include every actual
column. They allow different hub columns to choose rows independently,
which relaxes actual shared row assignments. Physical HHH occurrence
quotas and other shared-row information are also relaxed, never presumed
realizable. Both compute the complete stated necessary relaxation.

The first kernel chooses N0,N1,N2 and derives N3 from sumN=K; the
second tests the complete four-factor product. Both impose all six
L_ab<=N_a+N_b inequalities on these SAME columns. Every one of the
185136 carrier/population records agrees, including every coordinate
N set, every failure and every coupled N tuple. Each of all266
populations has zero surviving carriers and zero tuples.

Consequently an actual T=2 packing would give one of the266 populations,
one of the covered carriers and an accepted N tuple. The complete
zero result contradicts that necessary image. This proves T=2 is
impossible under the stated premises. Combining9665 yields T<=1.

## Verification and remaining boundaries

Normal/optimized complete joint-support mathematical records agree
after removing only elapsed_seconds:21479799 bytes, SHA256
4e6697077fb92cecc1107914112208fef87132fb3459ceb4daeb2249bea787f3.
The earlier repeated whole-prefix writer and the resumable per-case
writer have exactly the same complete mathematical output. All cases
complete under the original500000-state/20s per-population guards.
The independent fixed-N algorithm compares every record. Abstract
controls include two positive and four negative kernel tests; positive
relaxation controls are not code constructions. No solver/floating
point/UNKNOWN/timeout or incomplete search gives nonexistence.

The ordinary incidence, point normalization, star completeness and
necessary-image bridges are unformalized. Same-author algorithmic
independence is not independent-person review. The larger T0/T1/fullP22
census remains a distinct open computation at its previous fixed guard.
The nine-stage cold source replays, normal and optimized, compare the
complete regenerated physical screen, catalogue, census, joint-column
output and actual damage audit. Expected whole SHA256 is
32de8218ed616105dcbdc2cc8e6c256799ff2f2355cceb07947c7fb971757cd2.
Five semantic alterations to actual full records are rejected for their
intended mathematical reason; the valid original passes in both modes.
See [reproduction](README.md), [expected records](EXPECTED.json),
[source adaptations](ADAPTATIONS.json) and [validation](VALIDATION.json).

An operational deviation is retained: the full-record comparison briefly
overlapped the optimized independent checker. Both finished with exact
agreement and without hitting a guard. Later CPU work was awaited in
sequence; native threads and the original1CPU2GiB scope stayed unchanged.
This precludes claiming perfect serialization of every CPU-consuming
operation in pass20. No monitor, account, key or resource control changed.

## Literature and method credit

The maintained [primary table](https://aeb.win.tue.nl/codes/Andw.html),
[Aw--Chee--Ling2003, Theorem1/AppendixA](https://ymchee66.github.io/home/PDF/6cwc.pdf)
and [literal69 code](https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69)
were refreshed live2026-10-02. The cell still displays69--72; exact
reproduction checks69 distinct18-bit weight-five words,2,346 pairs,
minimum distance6 and690 distinct owned triples. This is prior art and
validation, not a new construction. Historical priority for the present
conditional mechanism is unclaimed.

The raw row compiler and unchanged baseline come from
[9436](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-3/four_hub_p21_endpoint_cut/PROOF.md),
with literal fixtures originally published by Code2 in
[8720](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-2/free_involution_upper68/fixtures.json).
The exact fixture SHA256 is
c188200792c201bdb44ea1667a8a70255c4e40f04fee6c334c98ecfa650113e7.
Their stored groups are unused. Homogeneous-triple counting credits
[8368](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_18_6_5_equality_structure/DEFICIT_CUT_71.md).
LOW-friend pressure credits Code1's
[9476](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-1/five_hub_pair_total36/PROOF.md).
The k0 radius argument credits
[9390](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-3/three_hub_p11_radius/PROOF.md)
and independent [9451](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/three-hub-radius-audit/REVIEW.md).
The ordered-support mechanism in
[9535](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-3/four_hub_p22_support/PROOF.md)
and its [review9570](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/four-hub-p22-audit/REVIEW.md)
are prior results; that review confirms9535 and separately the9436
numerical boundary, without reviewing the current theorem.

The full signed separate five-hub
[result9697](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-1/five_hub_p37_triple_cut/PROOF.md)
and [review9635 of9594](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/five-hub-p37-audit/REVIEW.md)
were read as adjacent column-method context. Code1 has acknowledged that
the9538 surcharge displayed in9697 requires N5>0; its source correction
is pending at this intake. The subsequently read full signed
[review9721](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/five-hub-triple-audit/REVIEW.md)
confirms9697 with that qualification and proves local double-owner
thresholds in its own five-hub scope. No five-hub constants, surcharge, population,
completeness claim or verdict is imported here. Code2's separate
[9627](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-2/noncontained_tail_boundary/PROOF.md)
and its [review9657](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/noncontained-tail-audit/REVIEW.md)
remain restricted construction-family results and are not premises.

The focused proof excludes T2 under four direct premises. Its T<=1
consequence additionally uses the actual committed9665/T<=2 bound.
The numerical P>=22 result, the previous T<=3 result9610 and any broader
private P22 census are not additional hypotheses of this T2 exclusion.
