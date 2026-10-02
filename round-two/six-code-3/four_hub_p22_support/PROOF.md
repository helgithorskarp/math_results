# Four unsaturated points at71 force hub-pair total at least22

Actual author: **six-code-3, researcher**, 2026-10-02, pass17.
Complete author-checked conditional lemma. Ordinary bridges are
unformalized; independent mathematical review is pending. All source
checks are by this same author, despite the shared signing identity.

Let F be71 distinct five-subsets of18 points, any two intersecting in
at most2. Write r_a for point replication and lambda_ab for pair
replication. Put S={a:r_a=20}, H its complement, and
P=sum_{a<b in H}lambda_ab.

**Claim.** Under the explicit imported premises below, if |H|=4, then
**P>=22**. The complete hub replication profile18,19,19,19 is included.
This excludes the P21 boundary left by the earlier conditional P>=21
lemma9436. It does not exclude the whole profile, improve the unrestricted
code-size bound, establish sharpness, or construct a new code.

## Premises, primary literature and authorship

Import the universal point cap20 and saturated-star no-LOW-LOW-leave
theorem from
[8323](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_upper71_review1/REVIEW.md),
the exact23-class twenty-star completeness from
[8933](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/twenty-star-classification-audit/REVIEW.md),
conditional on8323, and the physical three-point theorem
[9249](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-3/unit_second_u_four_interfaces/PROOF.md),
independently confirmed by
[9293](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/three-point-star-audit/REVIEW.md).
Precisely, if distinct x,y,U have r_x=r_y=20, lambda_xy=4,
the second row y is unit, and an actual deficient hub U is isolated in
the first row's HIGH-induced leave, then |F|<=67. Both orientations
are used; LOW leave friends are permitted. There is no fourth mark.

Import the scalar incidence/capacity identities of
[9313](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-3/isolated_row_capacity_cut/PROOF.md),
independently checked in
[9375](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/isolated-row-capacity-audit/REVIEW.md),
and the prior conditional P>=21 at m4 from
[9436](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-3/four_hub_p21_endpoint_cut/PROOF.md).
The latter is still independently unreviewed at the refresh used here.
Its source commit is c9eb285852e843d017d060beb63d8ee625a0df31.
The radius lemma
[9390](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-3/three_hub_p11_radius/PROOF.md)
and exact walk-loss identity are independently confirmed by
[9451](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/three-hub-radius-audit/REVIEW.md).
Their ordinary proofs needed here are also given below. The homogeneous
triple count retains credit to
[8368](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_18_6_5_equality_structure/DEFICIT_CUT_71.md).

The unchanged [baseline/fixtures.json](baseline/fixtures.json) is credited
to Code2/
[8720](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-2/free_involution_upper68/fixtures.json),
SHA256 c188200792c201bdb44ea1667a8a70255c4e40f04fee6c334c98ecfa650113e7.
Supplied automorphism groups are not used. Generic completeness is an
explicit external premise, not established by reproducing23 fixtures.

The LOW-friend pressure and R+|B| crossing mechanisms retain Code1
credit, now in
[9476](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-1/five_hub_pair_total36/PROOF.md).
The needed ordinary inequalities are rederived here. No five-hub
numerical conclusion, private70-row count, review verdict, or literal
five-hub closure example is imported. The extra max(R,D-I) strengthening
uses this author's earlier unit endpoint bound.

Fresh committed
[review9527](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/five-hub-p36-audit/REVIEW.md)
confirms the separate9476 conditional theorem with a specific correction
to an illustrative closure population. It also independently rederives
the max(R,D-I)+|B| crossing mechanism credited to this author's private
handoff. Its five-hub verdict is context only; its CITES9436 edge supplies
no independent verdict on9436 or this P22 result. No literal corrected
five-hub population is used here.

The maintained [primary table](https://aeb.win.tue.nl/codes/Andw.html)
and [Aw--Chee--Ling2003 paper](https://ymchee66.github.io/home/PDF/6cwc.pdf)
were refreshed live. Their known69-word construction is prior art.
Its unchanged literal baseline was exactly revalidated separately.
Neither literature refresh nor baseline reproduction is new research.
The new result is the support obstruction that completely excludes P21
in the stated four-hub profile.

## Definitions and necessary complete local domain

A fixed pair has disjoint three-point tails on16 other points; hence
lambda_ab<=5. Write delta_ab=5-lambda_ab>=0. Since sum r_a=355,
total point defect is5. At m4 the four defects are2,1,1,1. Give the
defect-two hub role0 and the identical light hubs roles1,2,3.

At saturated s, its20 shortened quadruples on17 points form a packing
of pairs. For a link point a its local replication is5-delta_sa.
Call it HIGH when delta_sa>0 and LOW otherwise. Let h_s be the number
of HIGH points, e_s=5-h_s, and k_s the number of HIGH hubs. A unit
row has e_s=0; all its positive deficits are1. Let q_s count HIGH-HIGH
leave edges with at least one HIGH hub endpoint, once each. Let c_sj
count saturated link points of deficit j, and let d_s=sum_j c_sj=h_s-k_s.
Put sigma_s=sum_j(j-1)c_sj. A row is eligible when an actual HIGH hub
is isolated in the HIGH-induced leave. Set psi_s=c_s1 for eligible
units, psi_s=-c_s1 for ineligible nonunits, and psi_s=0 otherwise;
margin_s=psi_s-3(k_s-e_s-q_s).

Each LOW point has a unique leave friend and it is HIGH, by8323.
For a HIGH point a at s, let L_s(a) count its LOW, globally saturated
leave friends t. The triple sat is uncovered. In the t-star, s is
LOW since delta_st=0, so8323 forces a HIGH there: delta_ta>=1.
All these friends are distinct. Pair incidence gives

    sum_(p!=a)delta_ap = 85-4r_a = 5+4(20-r_a).

Thus delta_sa+L_s(a)<=5+4(20-r_a). This necessary pressure is imposed
on every HIGH link point, including globally saturated ones and both
light and heavy hubs. It is never interpreted as sufficient placement.

The literal producer and separately written inverse LOW-friend checker
enumerate all23*C(17,4)*4=218960 H4/heavy marks, retaining genuine e4
and all eight k5 baseline exceptions until explicit tests exclude them.
Exactly123877 physical marks pass and project to46 of the earlier60
statistic types. Every membership bit, first failure witness and all426
baseline marked rows agree between engines. Membership SHA256 is
2cf374d429271e3ebe5045d731ec6245ca517cbba9c8d27629bc31526e867588.
No local frequency caps the number of ambient saturated centers.

## Complete P21 reduction to eleven necessary populations

The prior9436 bound reduces the assertion to excluding P21. Define
E=sum_s e_s, K=sum_s k_s, Q=sum_s q_s, and
X=sum_{st in G}(delta_st-1), where G is the positive-deficit graph on S.
Let T count covered triples wholly in H, and tau count uncovered
triples in S whose three pairs have positive deficits. The scalar
identities/capacity inequality from9313 give

    n=14, W=sum_(s in S,a in H)delta_sa=22,
    E=15-Q-T-2tau, K=22-E+2X,
    Q+2T+2X+4tau<=8,
    sum_s margin_s<=3(8-Q-2T-2X-4tau), sum_s sigma_s=2X.

All70 admissible (Q,T,X,tau) branches in Q0..8,T0..4,X0..4,tau0..2
are covered. A positive-charge/unit-completion engine and a separate
uniform generating-factor engine agree on all1822 full count vectors,
including their complete old failure lists. The prior necessary tests
leave494 vectors. These tests impose color degree parity, distinct
compatible partners and the relaxed k0 radius condition, including the
unit/eligible incompatibility supplied by both orientations of9249.

For a k0 root s, every nonneighbor t is LOW at s. Its unique leave
friend v is HIGH and saturated because no hub is HIGH at s. In the
t-star, s is LOW and sv is a leave pair, so v is HIGH there. Hence
s-v-t is a genuine path. Every S point is within two steps of s.
For any graph with this property the exact walk count is

    13 = sum_(v in N(s)) d_v - 2*t_s - C_s,

where t_s counts graph triangles through s, and C_s sums outward
incidence multiplicity minus one at vertices outside the closed
neighborhood. Forced triangles and forced incidences at vertices
outside the *potential* neighborhood therefore give valid lower losses.

Let U be units, A the ineligible units, C the ineligible nonunits,
B the eligible nonunits, D=sum_U d_s, I=sum_A min(d_s,|A|-1), and
C1=sum_C c_s1. The unit endpoint cut is D<=I+C1; equality uses every
color1 endpoint of C on U. Higher colors remain available. This can
force a closed side containing a k0 root, contradicting its radius.
If R is the number of k0 units, R>0 and B is nonempty, then

    sum_C d_s >= max(R,D-I)+|B|.

Indeed, both R and D-I lower-bound actual U-C edges. A k0 unit cannot
have all its neighbors in units: then every eligible nonunit is
unreachable in two steps. Fixing one such root, radius requires at
least |B| distinct C-B edges. U-C and C-B are disjoint and each uses
one C endpoint. This proves the strengthening without a graph search.

Monotone color propagation removes an edge color when its endpoint's
remaining demand is zero, or forces it when every remaining compatible
pair is needed. Color degree parity is applied separately on every
closed potential component. At tau0, the h_s-1-q_s HIGH-SAT leave
pairs at s must be nonedges between its saturated HIGH neighbors;
otherwise the uncovered triple is a positive-deficit triangle counted
by tau. Thus the graph triangles through s are at most
binom(d_s,2)-(h_s-1-q_s). These give the forced triangle cuts.

Finally enumerate every unit-induced graph on its potential unit
edges, preserving every forced edge. Each unit's remaining degree
must be supplied by distinct compatible C vertices in color1. For
every subset J of units, residual demand cannot exceed
sum_C min(residual_capacity_C, number_of_allowed_J_neighbors).
This is a necessary capacitated Hall inequality; all subsets are
checked. Internal triangles obey the same tau0 bound. All98315
unit masks in this finite domain are enumerated. The <=15 potential
edges and10-second guard are preserved; neither guard is hit.

| New exclusion stage | Excluded | Remaining |
|---|---:|---:|
| Unit endpoint capacity |169|325|
| Closed all-color partitions |232|93|
| Radius crossing capacity |65|28|
| Forced degree inconsistency |1|27|
| Closed color-layer parity |1|26|
| Forced radius losses |8|18|
| Forced uncovered triangles |4|14|
| Complete bounded unit graphs |3|11|

The separate cut checker uses direct crossing-pair checks, one-edge
propagation, literal neighbor subsets and augmenting-path bipartite
flows instead of the producer's closure BFS, batch propagation, neighbor
DP and Hall subsets. Every certificate and every accepted mask agrees.

The eleven necessary populations are below. Type IDs refer to the
unchanged [baseline/expected.json](baseline/expected.json). In notation
`i:n`, type i occurs n times. Every other multiplicity is zero.

| Ordinal | (Q,T,X,tau) | Population |
|---:|---|---|
|0|(0,1,2,0)|16:2,17:2,18:10|
|1|(0,1,3,0)|17:6,18:8|
|2|(1,0,2,0)|16:2,17:1,18:10,19:1|
|3|(1,0,2,0)|16:2,17:2,18:9,20:1|
|4|(1,0,3,0)|17:5,18:8,19:1|
|5|(1,0,3,0)|17:6,18:7,20:1|
|8|(3,0,1,0)|1:2,16:2,18:7,20:3|
|10|(3,0,1,0)|1:3,16:2,18:6,20:2,42:1|
|16|(4,0,1,0)|1:3,16:1,17:1,18:5,20:4|
|18|(4,0,1,0)|1:3,16:1,18:6,19:1,20:3|
|19|(4,0,1,0)|1:3,16:2,18:6,20:2,26:1|

These are necessary populations, not realizable codes. Only now may
tau0 and T<=1 be used. In particular no word contains all four hubs.

## Ordered physical roles and the positive-support obstruction

For the eight occurring types, every relevant accepted physical mark
and all six bijections of the light roles are retained:28736 marks,
172416 role assignments,837 projected physical signatures. Two physical
engines agree on every signature, diagnostic frequency and smallest
literal witness. Coordinates are type, ordered delta_sa, six HH leave
bits, four covered HHH bits, word counts by hub number, and actual
isolated-hub bits. Records SHA256 is
e53e247979c35f92cdd44b152f699d047e7d611c91250b371aef2be57094d039.
Frequencies are diagnostic, never global multiplicity limits.

Let D_a=sum_{s in S}delta_sa and N_a=|{s in S:delta_sa>0}|.
Let P_a=sum_{b in H,b!=a}lambda_ab. Subtracting the three HH deficits
15-P_a from the total hub deficit gives the exact ordered quotas

    D_0=P_0-2, D_a=P_a-6 for a=1,2,3.                (H)

Let ell_s(a) be the HH leave degree of role a at s. For a HIGH hub
a, its complete local leave degree is
16-3(5-delta_sa)=1+3delta_sa. Exactly ell_s(a) of these leave
neighbors are other hubs. Its HIGH-SAT leave neighbors number at
most q_s, by the definition of q_s. The remaining neighbors are LOW
saturated leave friends; therefore

    L_s(a) >= 1+3delta_sa-ell_s(a)-q_s.

Every such t has delta_ta>0 by the already proved no-LOW-LOW argument.
They are distinct members of the positive support of a, all different
from s. Consequently the new necessary support bound is

    N_a >= 2+3delta_sa-ell_s(a)-q_s, delta_sa>0.       (S)

This is an ordinary graph-incidence deduction, not a solver conjecture.
It uses a universal lower bound; no unrecorded SAT-neighbor feature or
LOW-friend count is inferred from one signature witness. In particular,
a projected witness is not assumed representative of other full marks.

For an HH pair ab, let t_ab count covered HHH triples containing it.
Each word through ab contributes three saturated centers minus its
extra hub count. Thus the exact local HH leave quota is

    sum_s HHleave_s(ab) = 14-3lambda_ab+t_ab.          (L)

At T0 every local HHH mask is0 and t_ab=0. At T1 one fixed role triple
is covered globally, at exactly two saturated centers; other local
HHH masks are0. The support census uses only the weaker necessary
restriction that each local mask is0 or that fixed triple. It need
not impose the exact two-center quota, nor positive total HH leave
quotas. If (L) is zero for a pair, however, every corresponding local
leave bit is forbidden. Omitting the other positive quotas enlarges
the relaxation and cannot create a false exclusion.

Exhaustively enumerate all integer lambda6 with each in0..5, total21,
nonnegative leave quotas and nonnegative ordered D4 from(H). There
are56 raw T0 carriers and1704 raw joint T1/triple carriers. All six
light permutations act on the joint tuple (triple,lambda6), fixing
the heavy role. Their verified orbits number14 and311, respectively.
All5022 physical signature transports are checked; light roles have
identical global defect, so this quotient is a genuine bijection of
the entire necessary model. Triple and pair coordinates are relabeled
together. No symmetry of actual codes is assumed.

For each carrier and each physical signature let d4 be its ordered
deficit vector and b4 its requirements from(S), with zero at a LOW
role. The producer retains coordinatewise nondominated b4 for each
fixed d4; every removed pattern is dominated by an actual retained
same-d4 pattern. It multiplies the type factors one center at a time,
storing `(sum d4, sum positive(d4), coordinatewise max b4)`. Terms
whose deficit exceeds the ordered target are discarded. At the end
retain only exact(H) and N4>=max b4.

The independently written checker obtains lambda carriers by bounded
sum recursion and uses forward light relabeling, whereas the producer
uses Cartesian enumeration and backwards pair lookups. Its type
factors enumerate all weak compositions of deficit patterns. It uses
the even weaker coordinatewise minimum b4 for each d4, whether or not
all four minima share a physical witness. This is a necessary
super-relaxation, and its emptiness is sufficient. Both algorithms
complete every14/311 canonical carrier for each of the eleven
populations, with **zero retained states** in every population.

Thus none of the eleven necessary P21 populations can be actual.
Together with the complete preceding reduction and9436's P>=21,
this proves the stated conditional **P>=22** claim.

## Verification, resource scope and trust boundary

[reproduce.py](reproduce.py) reconstructs all fourteen stages from
declared public source and compact pinned inputs. Normal and optimized
CPython3.12 runs compare whole stage outputs, not merely counts; only
timing fields are removed. Full mathematical SHA256:
aaf8bd4b4444c05953998592e86caad8481b21eba00f786fd3e89ed10830aab9.
No `assert` is used as a mathematical check. No solver or floating-point
premise occurs in the proof pipeline. Exploratory random quota witnesses
and their one incomplete search are omitted from the proof and source.
The64 earlier two-root graph carriers are also unnecessary and omitted.

Controls include every218960 membership bit, all426 baseline rows,
all1822 full vectors and old failures, all494 new cut certificates,
all98315 finite unit masks, every837 signature and frequency, all5022
light transports,1674 actual point transports and1227 literal HIGH-hub
friend audits. The support kernel passes one small positive and two
negative polynomial controls; four literal damages of HH leaves,
ordered deficit, distinct role placement and q semantics are rejected.
Earlier stages reject four cut and five physical-signature damages.

Native threads are1 and child stages are serial. Each has a60-second
outer timeout. Inner guards remain100000 states/10 seconds for the
charge producer,500000 states/20 seconds for the polynomial and support
censuses,30 seconds for marking/role coverage, and at most15 potential
unit edges/10 seconds for each unit graph. Every required enumeration
completes; no guard, timeout, memory kill or resource escalation is a
mathematical premise. Bulky enumeration outputs and imported large
classification corpora are not committed; the former regenerate in the
requested fresh work directory.

Trust boundaries are the explicitly imported generic classification
and mathematical lemmas, the ordinary unformalized incidence/coverage
bridges, standard-library exact integer computation and the supplied
literal fixtures. Algorithmic independence by one author is not peer
review. Source publication and shared signatures do not change this
status. The global69–71 question remains unresolved.
