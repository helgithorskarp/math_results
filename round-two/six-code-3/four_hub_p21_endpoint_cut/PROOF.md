# Four unsaturated points at 71 force hub-pair total at least 21

Actual author **six-code-3, researcher**, 2026-10-02, pass15.
Author-checked conditional lemma with complete exact finite checks.
Ordinary bridges are unformalized; independent mathematical review is pending.
The shared signing identity does not establish independent authorship.

Let F contain 71 distinct five-subsets of 18 points, with any two
intersecting in at most two points. Write r_p and lambda_pq for point
and pair replication, S={p:r_p=20}, H=S complement, m=|H|,
n=|S|, and P=sum_{a<b in H}lambda_ab.

**Theorem.** Under the explicit saturated-star, generic classification,
local three-point, and radius premises below, **m=4 implies P>=21**.
The entire four-hub profile (18,19,19,19,20^14) is included.
This excludes the P20 boundary of the independently confirmed prior
P>=20 theorem. It neither excludes the whole profile nor changes the
unrestricted code-size endpoint, and supplies no new construction.

The new reusable mechanism is an ordinary unit endpoint cut, including
its equality rigidity. Seven of the 18 necessary P20 populations violate
that cut. The other eleven force a closed six-vertex side containing a
hub-complete saturated row, although eight saturated points are outside.
The imported radius premise makes each such actual closed partition impossible.

## Explicit premises and credited baseline

Import the point cap20 and no-low-low-leave theorem from
[8323](../../../constant_weight_upper71_review1/REVIEW.md), the complete
23-class twenty-star coverage from
[8933](../../six-reviewer-5/twenty-star-classification-audit/REVIEW.md)
conditional on8323, and the precise
[three-point theorem9249](../unit_second_u_four_interfaces/PROOF.md):
distinct x,y,U with r_x=r_y=20,lambda_xy=4, unit second row y,
and a deficient hub U isolated in the first row's high-induced leave
force |F|<=67. Low leave friends are allowed. There is no fourth mark,
lambda_yU5 hypothesis, or numerical9209/9176/9141 premise here.
Independent [9293](../../six-reviewer-4/three-point-star-audit/REVIEW.md)
supplies a complete combined proof from8933/8323 and confirms exactly
this imported theorem.

The prior [9313](../isolated_row_capacity_cut/PROOF.md) proves P>=20
at m4 and the coefficient/capacity identities used below. Independent
[9375](../../six-reviewer-4/isolated-row-capacity-audit/REVIEW.md)
confirms that scope; its stronger signed coefficient refinement is not
needed. The saturated radius statement is imported from author-checked
[9390](../three_hub_p11_radius/PROOF.md): throughout1<=m<=5,
if k_s=0, every saturated point is within distance two of s in G.
We need only its connectedness consequence, not the three-hub P11
threshold or final K5 argument. No independent verdict on9390 or the
present endpoint cut is claimed.

For clarity, the ordinary radius argument is short: a nonneighbor t
of a k0 root s is low in the s-star. Its unique leave friend v is
high by8323 and saturated because k_s=0. The uncovered triple stv
makes sv a leave edge at t, where s is low. No-low-low forces v high
at t, giving the actual s-v-t path. All three points are distinct.

The literal [fixtures.json](fixtures.json) is credited unchanged to
[8720](../../six-code-2/free_involution_upper68/fixtures.json), SHA256
c188200792c201bdb44ea1667a8a70255c4e40f04fee6c334c98ecfa650113e7.
Its supplied groups are unused. The star compilers and two category
engines adapt the published source of9390, with a fresh m4 inventory;
426-row reproduction and algorithmic reuse are validation, not novelty.
The new mathematical information is the endpoint cut, equality closure,
and complete physical exclusion of all fifteen P20 charge branches.

Complementary [9367](../../six-code-1/five_hub_pair_total35/PROOF.md)
addresses m5/P35 using a closed cubic-block obstruction. Fresh independent
[9422](../../six-reviewer-5/five-hub-girth-audit/REVIEW.md) confirms that
conditional scope and determines its exceptional-row correction region.
Its five-hub threshold and girth argument are not premises here; its
verdict does not cover9390 or the present result. The present cut retains
higher deficit colors and can be applied in that separate lane.

## Local rows and complete projection

A fixed pair has disjoint three-point tails on16 other points, so
lambda_pq<=5. Put delta_pq=5-lambda_pq. Since sum r_p=355 and
r_p<=20, total point defect is5; at m4 the hub defects are2,1,1,1.

At saturated center s, shorten its20 words to quadruples on17 points.
Let D_s be the positive-deficit link points, h_s=|D_s|,
e_s=5-h_s, and k_s=|D_s intersect H|. The row is unit iff e_s=0;
every positive pair deficit at a unit row is1. Let q_s count high-high
leave edges having at least one deficient hub endpoint, once each.
This is not the total leave among all hubs, which may include low hubs.

Write c_sa for the number of saturated link points of deficit a,
for1<=a<=5. Then d_s=h_s-k_s=sum_a c_sa is the saturated support
degree, and sigma_s=sum_a(a-1)c_sa. Eligibility means an actual hub
in D_s is isolated in the leave induced on D_s. Define psi_s=c_s1
for a unit eligible row, psi_s=-c_s1 for a nonunit ineligible row,
and psi_s=0 otherwise. Put margin_s=psi_s-3(k_s-e_s-q_s).

Enumerating every subset J of the actual high points in every literal
star gives426 marked records, including genuine e4/h1 marks and
eight k5 marks with margin -3. The418 marks with k<=4 have margin>=0.
An actual four-hub placement projects to J=H intersect D_s; its other
4-|J| hubs are low and do not change these statistics. There are at
least12 low points. Thus all marks with k<=4 cover every actual
four-hub row, up to the common point relabeling supplied by8933.
No automorphism quotient, full physical placement count, global graph
realization, or matching of the remaining hub labels is inferred.
The compressed statistic catalog has60 types.

After removing the histogram coordinate, both engines reproduce every
published426-row record, canonical SHA256
19205841cee4584466bac048f114d0d5f0db096b6861e45f34c94b9180087b16.
All local exceptions remain in the reconstructed full catalog; they are
excluded from particular global populations only by explicit conditions.

## Every arithmetic branch at m4/P20

The prior theorem reduces the new assertion to excluding P20. Let
E=sum e_s, K=sum k_s, Q=sum q_s, X=sum_{ab in G}(delta_ab-1),
T count covered triples wholly in H, and tau count uncovered S-triples
whose three pairs are positive deficits. Thus sum sigma_s=2X.
At m4/P20, the identities and capacity cut of9313 give

    n=14, W=sum_{s in S,a in H}delta_sa=20,
    E=12-T-2tau-Q, K=20-E+2X,
    Q+2T+2X+4tau<=4,
    sum margin_s<=3(4-Q-2T-2X-4tau).                 (B)

The homogeneous-triple identity retains method credit to
[8368](../../../constant_weight_18_6_5_equality_structure/DEFICIT_CUT_71.md),
with a full derivation in9313. No assumption T0,X0,tau0 or Q0 is
made before enumeration. Q0..4,T0..2,X0..2,tau0..1 exhaust all
cost-admissible values under(B), giving precisely15 branches.

For each branch enumerate all nonnegative type multiplicities with
total14, exact E,K,Q,2X, and margin at most the stated budget. The
prior necessary tests from9390 require enough distinct compatible
neighbors in each deficit color, even color-degree sums, and the relaxed
radius bound13 at every k0 root. A unit vertex cannot neighbor any
eligible vertex: its pair deficit is1, and9249 applies with the
eligible vertex first and the unit vertex second, using an actual
isolated hub distinct from the saturated centers. Both orientations
are enforced, including two eligible unit endpoints.

| Q | T | X | tau | Raw populations | After prior necessary tests |
|---:|---:|---:|---:|---:|---:|
|0|0|0|0|0|0|
|0|0|0|1|1|0|
|0|0|1|0|3|0|
|0|0|2|0|1|0|
|0|1|0|0|0|0|
|0|1|1|0|1|0|
|0|2|0|0|1|0|
|1|0|0|0|2|2|
|1|0|1|0|7|0|
|1|1|0|0|1|0|
|2|0|0|0|6|4|
|2|0|1|0|2|0|
|2|1|0|0|2|0|
|3|0|0|0|13|5|
|4|0|0|0|7|7|

There are47 necessary populations and18 survivors. Only after this
complete computation can T=X=tau=0 be concluded for the survivors.
These vectors are necessary row statistics, not packings or code classes.

## The unit endpoint cut and its equality rigidity

Let U be all unit vertices in S, A the ineligible unit vertices, and
C the ineligible nonunit vertices. Put

    D_U=sum_{s in U}d_s,
    I_U=sum_{s in A}min(d_s,|A|-1),
    C_1=sum_{s in C}c_s1.

**Endpoint lemma.** Under the imported9249 prohibition,

    D_U <= I_U+C_1.                                 (U)

If equality holds, every deficit-one neighbor of every vertex in C
belongs to U. Higher deficit colors remain unrestricted by this
equality claim.

Proof: any edge incident to a unit has deficit1 and cannot have an
eligible endpoint. Unit-unit edges therefore lie inside A. Their
directed endpoint count is at most I_U, since an A vertex has at most
|A|-1 distinct other A neighbors and at most d_s total neighbors.
Every remaining unit endpoint is matched to a deficit-one endpoint
of an ineligible nonunit in C, so their count is at most C_1.
This proves(U), including eligible units with no unit neighbors.
At equality both upper bounds are attained. The latter matching uses
all C_1 endpoints, proving the stated rigidity. There is no repeated
neighbor, fractional matching, or matching existence assumption.

For the eighteen P20 survivors the exact individual certificate
[certificate.json](certificate.json) gives:

| Multiplicity | D_U | I_U | C_1 | Physical obstruction |
|---:|---:|---:|---:|---|
|3|25|20|1|Violates(U)|
|2|24|20|2|Violates(U)|
|1|20|12|6|Violates(U)|
|1|23|19|3|Violates(U)|
|5|29|29|0|Closed six-point side, eight outside|
|5|26|26|0|Closed six-point side, eight outside|
|1|23|20|3|Equality forces closed six-point side, eight outside|

The first seven are impossible directly. For each of the other eleven,
the certificate fixes a labeled partition of the expanded14-row
population and an actual k0 root on the six-point side. Every crossing
pair is disallowed either by unit/eligible incompatibility, absence of
a common positive deficit color, or the just-proved equality rigidity.
Because X0, all saturated positive deficits are1. The potential graph
used to find the partition is an overapproximation of actual G, so
checking that its crossing pairs are impossible proves actual closure.
The nonempty eight-point outside then contradicts the imported radius
premise. Passing the earlier scalar radius bound is insufficient for
this physical connectedness requirement.

The one equality case with C_1>0 illustrates the mechanism. At Q3
there are three units with k0,d5; two units with k1,q1,d4;
eight eligible nonunit rows with e1,k1,q0,d3; and one ineligible
nonunit with e1,k1,q1,d3. The unit demands total23. Their internal
capacity is20; the sole ineligible nonunit supplies exactly3 more.
All three of its neighbors must therefore be units. The five units
and that nonunit form a closed side, separated from the eight eligible
nonunits. Each of the three k0 units must reach those eight points by
the radius premise, a contradiction. No cubic girth argument is needed.

All fifteen P20 branches are now impossible. Combined with the prior
P>=20 theorem, this proves **P>=21** at m4.

## Exact verification and trust boundary

[produce.py](produce.py) reconstructs literal set-based marked stars,
chooses positive-q counts, and iterates zero-q nonunit counts with
algebraic completion of the two unit categories. [verify.py](verify.py)
imports no producer, rebuilds actual quadruple masks and covered-pair
bitsets, and extracts uniform generating-polynomial coefficients.
Both compare every row, all60 types, all15 branches, all47 population
vectors and all prior failure labels with frozen [expected.json](expected.json).
The frozen inventory predates the independent reconstruction.

[cuts.py](cuts.py) computes the endpoint bound and finds a closed side
by BFS in the permitted potential graph. The separate
[verify_cuts.py](verify_cuts.py) imports neither that producer nor the
star producer. It enumerates all simple adjacency subsets inside the
ordinary unit block, checking degrees and remaining external endpoint
demands:334912 subsets in total over all18 populations. It separately
checks every crossing pair in each certified partition, without BFS.
Eligible-unit demands are retained outside the unit block. Five odd
internal-endpoint cases already fail this independent adjacency
relaxation; their original closed-cut certificates remain valid.
These are exact local graph certificates, not actual global packings.

Complete cold normal/optimized runs compare whole producer and
independent output bytes and whole RESULT bytes. Sixteen controls
reject physical input and cut damages, transport all23 stars/852
marked records through two actual point bijections, and enumerate
all256 permitted small role graphs. A separate higher-color control
ensures equality consumes only deficit-one endpoints. Those controls
are graph-algebra objects, not claims of star or code realization.
All checks use explicit exceptions and remain active under Python -O.
Costs, hashes, commands and the final source seal are in
[VALIDATION.json](VALIDATION.json), with provenance in
[DEPENDENCIES.json](DEPENDENCIES.json).

The live [Brouwer table](https://aeb.win.tue.nl/codes/Andw.html),
refreshed2026-10-02, retains69..72. The established69 construction is
[Aw--Chee--Ling2003, Theorem1/AppendixA](https://ymchee66.github.io/home/PDF/6cwc.pdf).
The [literal69](https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69)
is freshly checked for69 distinct weight-five words,2346 valid pairs,
690 unique owned triples, minimum distance6, source SHA256
cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d.
Reproduction is validation, not new research. The separately reviewed
campaign interval69..71 remains unresolved. No historical priority,
threshold sharpness, new construction, or whole profile exclusion is claimed.

Trust boundaries are the explicit imported mathematical results,
generic classification completeness, literal decoding, CPython exact
integer/set semantics, and ordinary shortening, projection, incidence,
endpoint and connectedness arguments. Those bridges are unformalized.
All fresh implementations are by the same researcher; algorithmic
corroboration is not independent mathematical review. Neither the
generic classification carrier nor the local three-point carrier is
rerun here, and verdicts on their imported scope do not transfer.

One serial mathematical job, all numeric threads1, unchanged1CPU/2GiB.
Fixed guards are100000 producer states/10seconds per branch,
500000 polynomial states/20seconds per branch, and at most15 potential
unit edges/10seconds per adjacency audit. No guard is hit or increased.
An incomplete run provides no mathematical absence. Large generated
catalogs and explorations remain in scratch. The next substantive target
is physical feasibility at m4/P21, retaining actual incidence rather
than treating necessary category populations as codes.
