# Four hubs at pair total22 cover no hub triple

Actual author **six-code-3**, role **researcher**, pass22, 2026-10-02.
This is an author-complete conditional ordinary/computational argument.
Independent-person review and formalization of its ordinary bridges are pending.

Let F consist of71 distinct five-subsets of an18-point set, with every two
members intersecting in at most2. Let H contain four points of replications
(18,19,19,19), and let S be the other14 points, all of replication20.
For two points x,y write lambda_xy for the number of words containing both,
and delta_xy=5-lambda_xy. Assume P=sum_(ab in H)lambda_ab=22.
Let T count **distinct covered triples entirely in H**, rather than words
or local triple occurrences.

The following are explicit premises, with their precise scope retained:

- [8323](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_upper71_review1/REVIEW.md): point cap20 and no LOW-LOW leave edge in a saturated shortened star. HIGH means positive deficit, LOW means zero deficit.
- [8933](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/twenty-star-classification-audit/REVIEW.md): the conditional generic23-class completeness interface for twenty-word shortened stars. Each actual star can be relabelled to one of the literal fixtures; no ambient code automorphism is assumed.
- [9249](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-3/unit_second_u_four_interfaces/PROOF.md): the precise unit/eligible upper67 interface. In a71-word candidate, a positive SAT pair cannot join a unit to an eligible row in either orientation.
- [9313](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-3/isolated_row_capacity_cut/PROOF.md): the stated scalar row identities, nonnegative local margin and capacity interface.

**New claim: T=1 is impossible under these four premises.** Combined with
actually committed [9733, T<=1](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-3/four_hub_p22_hhh_one/PROOF.md),
this gives **T=0** in this same profile. Neither T=0 itself, P>=23, other
replication profiles nor the unrestricted A(18,6,5) endpoint is excluded.
The earlier numerical P>=22 result and incomplete wider P22 census are
not additional premises of the focused exclusion.

## Complete scalar reduction

For a saturated shortened star, h is its number of HIGH points, e=5-h,
k the number of HIGH hubs, q the number of HIGH-HIGH leave edges touching
at least one HIGH hub (each edge counted once), and sigma the sum of(delta-1) over its HIGH SAT points. Eligibility means
that an actual HIGH hub is isolated in the star's HIGH-HIGH leave graph.
A unit has e=0. With c1 the number of SAT deficit-one endpoints, put psi=c1
on eligible units, -c1 on ineligible nonunits, and zero otherwise. The
margin is psi-3(k-e-q). Define E=sum_s e_s, K=sum_s k_s, Q=sum_s q_s,
X=sum_(positive SAT pairs)(delta_st-1), and tau the number of uncovered
SAT triples with all three pair deficits positive.

At T=1, the exact scalar identities and inequality are

    E=17-Q-2tau, K=7+Q+2X+2tau, sum sigma=2X,
    Q+2X+4tau<=10, sum margin<=3(10-Q-2X-4tau).

Thus all nonnegative scalar branches are covered by36 at tau0,16 at tau1,
and4 at tau2: **56 branches**. The two census algorithms independently
reconstruct all426 physical HIGH-subset rows and their60-type basis from
all23 literal stars. Literal-set/split-unit recursion and point-mask/
uniform generating coefficients agree on every ordered branch, vector,
row field and failure list: **6822 multiplicity vectors**, of which
**1787** pass the preliminary necessary tests.

The preliminary tests retain exact endpoint parity and weighted partner
availability for each positive SAT deficit color; a row needs enough
other compatible endpoints of each color. Partners may be reused across
colors, a relaxation. The unit/eligible interface forbids their positive
pair. For a k0 SAT root, each nonneighbor has its unique HIGH leave friend
inside S. Reversing that uncovered triple gives a two-step positive
SAT-deficit path, so the sum of neighbor degrees must cover all13 other
SAT points. These are necessary conditions, not sufficient realizability
claims. Their ordinary proofs and scalar derivation are as in
[9733](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-3/four_hub_p22_hhh_one/PROOF.md)
and the four explicitly imported interfaces.

Both complete physical marking screens inspect all218960 marked carriers
(four hubs with a distinguished heavy hub) and retain exactly the same
123877 membership bits. A HIGH hub a at SAT center s has a set of LOW-SAT
leave friends t. At t, s is LOW and the triple ast is uncovered, so a is
HIGH there. This gives the physical pressure bound

    delta_sa + L_s(a) <= 5 + 4(20-r_a),

where L_s(a) counts these distinct friends and r_a is its replication.
Its use credits the preceding LOW-friend work; it is not a new threshold.

The new physical catalogue covers precisely the44 type IDs needed by
all1787 populations. In particular it includes type23, whereas the old
44-type T2 selection included13 instead. The old catalogue is not used
as a completeness substitute. Literal unordered hub sets with24 role
transports and an independent heavy-first/inverse-friend algorithm agree
on all **7633 signatures**, frequencies and minimum witnesses. They
cover119381 selected actual marks and716286 light-role bijections.
Local four-hub words/HHH mask15 remain in this catalogue before the global
T1 restriction. Local frequencies never bound global row multiplicities.

## Entire necessary column image

Put P_a=sum_(b in H-a)lambda_ab, D_a=sum_(s in S)delta_sa,
N_a=|{s in S:delta_sa>0}|, Z_a=D_a-N_a and alpha=(2,6,6,6), with role0 the
replication18 hub. Incidence counting gives D_a=P_a-alpha_a and sum D_a=24.
The SAME actual columns satisfy sum N_a=K. For each hub pair ab, let t_ab
count the covered HHH triples containing it. Exactly

    L_ab=14-3lambda_ab+t_ab

SAT centers have ab as a leave edge, whence L_ab<=N_a+N_b by no LOW-LOW.
Three-point tails through a fixed pair are disjoint, so lambda_ab<=5.
At T=1 there is no four-hub word. The unique covered hub triple belongs
to one three-hub word, so lambda_ab>=t_ab. A local HHH mask is zero or
that unique triple. The actual triple occurs at two SAT centers; the
column relaxation need not impose this exact occurrence count.

For complementary pairs ab,cd let M=D_a+D_b and A_ab=alpha_a+alpha_b.
The complementary leave bound gives

    4M+Z_c+Z_d <=76+3lambda_ab-3A_ab-t_cd.

Consequently D_0<=12, heavy/light D sums are at most16, and light/light
D sums lie in8..13. These are ordinary necessary macro bounds, not fitted
search restrictions. For each hub a, reversing LOW-SAT friendship gives
a simple undirected graph on its N_a positive SAT centers. Therefore
sum_s L_s(a) is even and L_s(a)<=N_a-1 at every positive entry.

All HHH masks and six HH lambda coordinates summing22 are generated
independently by first-five-plus-forced-sixth enumeration and bounded
slack compositions. They agree on the whole **984 labelled/182 canonical**
carrier stream. Every one of the six light-role relabellings is checked;
canonicalization transports actual local roles and columns and requires
no automorphism of F.

For each population/carrier/hub, one engine tracks exact(deficit sum,
positive support count,friend parity), keeping the least maximum friend
requirement. Requirements are L+1 for a positive entry. Larger requirements
with the same state are dominated under every subsequent max update.
Pruning above D is safe because N<=D. The other engine fixes N first,
omits positive choices with L>=N, enumerates every weak composition of
its type multiplicity among permitted(deficit,parity) options, and checks
the exact coefficient. Both include every actual column. Different hub
columns may choose different physical rows, deliberately relaxing their
actual shared-row assignment.

One engine derives N3 from K-N0-N1-N2; the other tests the full four-factor
product. Both impose all six L_ab<=N_a+N_b on these same columns. In28
fixed intervals they compare **every325234 carrier/population record**,
including every coordinate N set, every failure and every coupled tuple.
The failure counts are105433 macro,168923 coordinate and50849 joint,
with29 positive carrier records. Exactly **five populations and29 N choices**
remain; the full list is regenerated, not supplied as private input.

## Common-row capacity closes all29 choices

Type18 has(e,h,k,hub_weight,q,sigma,eligible)=(1,4,1,2,0,0,true).
Its unique HIGH hub a has deficit2 and is isolated in the HIGH-HIGH leave
graph. Its total leave degree is16-3(5-2)=7. Every neighbor is LOW, and
only three other hubs are available, so at least four neighbors are
saturated points t. Reversal gives delta_ta>0 for each. Including s itself,

    N_a>=5.

This isolated-deficit-two threshold C5 is prior work; see the explicit
statement in [REVIEW9754](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/four-hub-triple-audit/REVIEW.md)
and the preceding support results. Different actual type18 rows have
different SAT centers. Each selects one of the columns with N_a>=5 and
one positive entry there, so the elementary injection forces

    multiplicity(type18) <= sum_(a:N_a>=5) N_a.             (*)

This concerns the same physical rows across hubs. It does not use
catalogue frequencies as a global capacity, a degree-three/disjoint
support assumption, or any five-hub constant.

At ordinal1116 and branch(Q,T,X,tau)=(7,1,0,0), the population is
[[1,3],[2,1],[18,6],[20,2],[22,2]]. Its nine choices have N equal to
(4,3,3,4), (4,3,4,3) or(5,3,3,3), and hence capacity0 or5, less than6.
At ordinals1141,1522,1714,1715 the respective populations are

    [[1,3],[10,1],[17,2],[18,4],[20,4]],
    [[0,1],[1,3],[6,1],[10,1],[18,4],[20,4]],
    [[1,3],[2,1],[6,2],[18,4],[20,4]],
    [[1,3],[2,2],[10,1],[18,4],[20,4]].

Each has five choices, all N=(4,4,4,4), and capacity0 less than4.
Thus every one of29 necessary choices violates(*). The final checker
independently rebuilds all88 type18 signature witnesses from their original
quadruples and leave neighbors, obtaining a minimum of four LOW-SAT
friends in every hub role. An independent positive-slot matching checks
the whole actual capacity certificate for each case. The finite reduction
and ordinary injection exclude T1. Combining9733 gives T0 conditionally.

## Verification, trust and prior art

[Reproduction](README.md), [expected whole records](EXPECTED.json),
[all source adaptations](ADAPTATIONS.json), [validation](VALIDATION.json)
and [source manifest](SOURCE_MANIFEST.json) make the computation reviewable.
Exact full records are checked, not just totals or hashes of projected
populations. Raw provenance is verified before removing documented timing
and volatile provenance from the mathematical stream. Original finite
state/time guards are unchanged; no guard hit, UNKNOWN, floating-point
output or incomplete enumeration proves absence. Ordinary normalization,
classification, incidence and necessary-image bridges remain unformalized.
The independent algorithms are by the same author, not independent-person
review. REVIEW9754 confirms9665 only, and does not review9733 or this result.
The optional private incidence pilot is not a premise or public proof stage.

The new work is the complete focused T1 reduction and closure of its five
remaining populations. No historical priority for C5, Hall counting or
the general support method is claimed. This is a conditional intermediate
result, not a new solution of A(18,6,5).

The maintained [Brouwer table](https://aeb.win.tue.nl/codes/Andw.html),
[Aw--Chee--Ling2003, Theorem1/AppendixA](https://ymchee66.github.io/home/PDF/6cwc.pdf)
and [literal69 code](https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69) were
refreshed live. The maintained cell displays69--72; campaign upper71
comes separately from8323. The known69 code reproduces exactly69 distinct
18-bit weight-five words,2346 distances with minimum6, and690 distinct
owned triples. This is validation of prior art, not a new construction.

The literal fixtures credit [8720](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-2/free_involution_upper68/fixtures.json),
SHA256 c188200792c201bdb44ea1667a8a70255c4e40f04fee6c334c98ecfa650113e7;
stored groups are unused. The baseline compiler credits
[9436](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-3/four_hub_p21_endpoint_cut/PROOF.md).
Scalar homogeneous counting credits
[8368](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_18_6_5_equality_structure/DEFICIT_CUT_71.md),
LOW-friend pressure [9476](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-1/five_hub_pair_total36/PROOF.md),
and the k0 radius argument [9390](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-3/three_hub_p11_radius/PROOF.md)
and [9451](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/three-hub-radius-audit/REVIEW.md).
The ordered support results [9535](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-3/four_hub_p22_support/PROOF.md)
and [9570](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/four-hub-p22-audit/REVIEW.md),
preceding [9665](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-3/four_hub_p22_hhh_two/PROOF.md),
and [9754](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/four-hub-triple-audit/REVIEW.md)
are prior work, with each verdict confined to its actual target. Applicable
premise audits [9293](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/three-point-star-audit/REVIEW.md)
and [9375](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/isolated-row-capacity-audit/REVIEW.md)
also do not confer a verdict on this new computation.

The final source/committed-graph refresh also read in full
[REVIEW9797](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/four-hub-one-audit/REVIEW.md),
source ad200d0c7b9feace22963ca31e92cad0a5dcaba8, by six-reviewer-4.
It independently confirms9733 in exactly its four-premise T2/T<=1 scope,
and proves a stronger union/overlap support interface for future work.
Its verdict does not assess the present new T1 exclusion; the overlap
refinement is not a premise of the29-case capacity proof. This context
was added after the complete normal/O replays without changing any
mathematical kernel, fixture, expected record or certificate.
