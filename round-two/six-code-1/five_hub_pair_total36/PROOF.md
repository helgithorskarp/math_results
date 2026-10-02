# Five unsaturated points at 71 force hub-pair total at least 36

Actual author **six-code-1, researcher**, 2026-10-02, pass13.
Author-checked conditional lemma with complete exact finite checks.
The ordinary mathematical bridges are unformalized and independent review
of this extension is pending. A common signing identity does not establish
independent authorship.

Let F be 71 distinct five-subsets of eighteen points, any two intersecting
in at most two points. Write r_p for point replication, lambda_pq for pair
replication, S={p:r_p=20}, H=S complement, and
P=sum lambda_ab over unordered pairs in H.

**Theorem.** Under the explicit imported statements below, if |H|=5,
then **P>=36**. Thus the replication profile (19^5,20^13) cannot occur
at P=35. Feasibility at P>=36 and the unrestricted campaign interval
69..71 remain open. No construction, sharpness or historical priority
is asserted.

The proof adds an ordinary point-deficit propagation bound and a
distinct-edge radius cut to the published unit endpoint mechanism.
All 27 scalar branches, including the five genuine exceptional-row
branches, are checked. The local carrier is a conservative enlargement
of possible ambient rows. Its 136 necessary vectors are statistics,
not code classes or realizations.

## Explicit inputs and prior credit

The mathematical imports are:

- [8323](../../../constant_weight_upper71_review1/REVIEW.md): point
  replication is at most20; in every shortened twenty-word star, a low
  leave point has a unique high leave friend. Its separately proved
  unrestricted upper71 is required for the five-hub append argument
  already incorporated in9367.
- [8933](../../six-reviewer-5/twenty-star-classification-audit/REVIEW.md),
  conditional on8323: all twenty-quadruple stars on17 points have a
  representative among the credited23 literal fixtures. Generic
  classification completeness is imported, not inferred from23 input
  records or rerun by this checker.
- [9249](../../six-code-3/unit_second_u_four_interfaces/PROOF.md): distinct
  saturated centers x,y, lambda_xy=4, a unit SECOND row y, and an actual
  deficient hub isolated in the FIRST row's high-induced leave force
  at most67 words. Low leave friends are allowed. No fourth mark or
  lambda_yU=5 hypothesis is imported. Independent
  [9293](../../six-reviewer-4/three-point-star-audit/REVIEW.md) confirms
  this scope conditional on8323/8933.
- [9367](../five_hub_pair_total35/PROOF.md): the corrected five-hub
  capacity, its incidence identities, T>=1 append statement, and P>=35.
  Independent [9422](../../six-reviewer-5/five-hub-girth-audit/REVIEW.md)
  confirms precisely that prior conditional theorem, including all
  eight exceptional rows. Its verdict does not cover the present P36
  extension.

The radius-two argument is credited to
[9390](../../six-code-3/three_hub_p11_radius/PROOF.md) and independently
confirmed and refined in
[9451](../../six-reviewer-4/three-hub-radius-audit/REVIEW.md). We rederive
the radius statement from8323 below; their numerical P11 theorem and
exact weighted radius identity are not additional premises. The unit
endpoint bound and its equality rigidity are prior
[9436](../../six-code-3/four_hub_p21_endpoint_cut/PROOF.md); the present
proof rederives them and retains both deficit colors when applying them
to the distinct m5 boundary. Code3's durable chat1827 supplied this
connection before its publication. No private numerical conclusion is
imported. The complete committed source scopes were read before use;
review verdicts on those sources do not transfer to this result.

The unchanged [literal fixture](fixtures.json) retains
[8720](../../six-code-2/free_involution_upper68/fixtures.json) provenance,
SHA256 c188200792c201bdb44ea1667a8a70255c4e40f04fee6c334c98ecfa650113e7.
Supplied group data is unused. The homogeneous incidence method retains
[8368](../../../constant_weight_18_6_5_equality_structure/DEFICIT_CUT_71.md)
credit through9367. Reconstructing these prior rows is validation.

## Point-deficit propagation

A fixed pair has disjoint three-point tails on sixteen other points,
so lambda_pq<=5. Put delta_pq=5-lambda_pq and d_p=20-r_p.
Total point replication is355, hence sum d_p=5. Every hub has d=1
when |H|=5, while S has thirteen points.

At saturated center s, shorten the20 incident words to quadruples on17
points. A link point a has shortened replication lambda_sa, deficit
delta_sa, and leave degree 1+3delta_sa. Let D_s be its positive-deficit
points, h_s=|D_s|, e_s=5-h_s, and k_s=|D_s intersect H|. Deficit mass
is5. No-low-low leave gives exactly h_s-1=4-e_s high-high leave edges.

For high a, let L_s(a) count its leave friends t which are LOW at s
and SATURATED globally. The triple sat is uncovered. At t's star,
s is low and sa is a leave pair, so no-low-low forces delta_ta>=1.
These forced points are distinct from s and a. Consequently

    delta_sa + L_s(a) <= sum_{p!=a}delta_ap = 5+4d_a.       (1)

If b_s(a) is a's high-high leave degree, there are only |H|-k_s low
hubs available among its other friends. Therefore

    L_s(a) >= 1+3delta_sa-b_s(a)-(|H|-k_s).

Together with (1), b_s(a)<=4-e_s and e_s>=delta_sa-1, this proves

    4delta_sa-b_s(a)+k_s <= 4+|H|+4d_a,
    4delta_sa+e_s+k_s <= 8+|H|+4d_a,
    5delta_sa+k_s <= 9+|H|+4d_a.                           (2)

These ordinary inequalities use the universal saturated-star premise;
they require neither the generic catalogue nor the local selector.
At71, |H|<=5. Thus a saturated pair has delta<=2, or lambda>=3.
At five hubs a high hub has d_a=1 and k_s>=1, so a saturated-hub
pair has delta<=3, or lambda>=2. No hub-hub bound is inferred.
The minimum-pair consequences hold throughout the relevant profiles,
independently of P=35.

## Physical roles, complete conservative carrier and scalar branches

Call a saturated row unit when e_s=0; all five positive link deficits
then equal1. Eligibility means that an ACTUAL high hub is isolated in
the leave induced on D_s. Let q_s count the high-high leave edges
touching a high hub, once each. Let c_s1 and c_s2 count saturated
positive neighbors of deficits1 and2. By (2),

    d_G(s)=h_s-k_s=c_s1+c_s2, sigma_s=c_s2,

where G is the simple positive-deficit graph on S. Deficit weight is
not support degree. Define psi_s=c_s1 at unit eligible rows,
psi_s=-c_s1 at nonunit ineligible rows, and0 otherwise. Set I_s=1
exactly for unit rows whose five high points are all hubs, and
mu_s=psi_s-3(k_s-e_s-q_s-I_s). The corrected9367 charge gives mu_s>=0.

Both implementations reconstruct every subset of the actual high points
of every literal star:426 records, including the unused-link-point
deficit5 star and all eight genuine I_s=1 marks. Every actual five-hub
placement projects to such a subset; its remaining hubs can lie among
at least12 low points. Low hub choices do not change these coordinates.
Applying only the proved saturated/hub deficit caps2/3 leaves410 marks
and51 distinct coordinate types. This is an enlargement: compatible
low hub placements, cross-row point coincidences, global realizability
and word-count quotas are not presumed. No local representation count
caps a type's multiplicity among the thirteen ambient rows.

By9249, no unit vertex can neighbor an eligible vertex in G. Such an
edge has deficit1; use the eligible center FIRST and the unit center
SECOND, with its actual isolated hub. This covers both orientations
and two eligible unit endpoints. It is the same physical prohibition
used in9367 and9436.

Put E=sum e_s, K=sum k_s, Q=sum q_s, N5=sum I_s. Let X be the sum
of delta_ab-1 on positive S-S pairs, T count covered hub triples,
and tau count UNCOVERED saturated triples with all three pairs positive.
Graph triangles and tau are different statistics. At m5/P35 the
incidence and corrected-capacity identities of9367 give

    W=sum_{s,a}delta_sa=15, T>=1, Q>=4N5,
    E=11-T-2tau-Q, K=15-E+2X, sum sigma_s=2X,
    2T+2X+4tau+Q-N5<=7,
    sum mu_s<=3(E+Q+N5-K).                                (3)

Q>=4N5 and T>=1 imply N5<=1, T<=3, X<=2 and tau<=1.
The rectangular integer carrier N5=0..1,T=1..3,X=0..2,tau=0..1,
Q=0..8, filtered by (3), contains exactly27 possibilities. None of
the five N5=1 branches is discarded or handled by an assumed N5=0
lemma. For each possibility enumerate EVERY nonnegative51-type count
vector with total13, exact E,K,Q,2X,N5, and margin at most the (3)
budget. Every true packing supplies one of these vectors.

## Ordinary physical capacity and radius cuts

Write U for all unit vertices, A for ineligible units, C for ineligible
nonunits, and B for eligible nonunits. Thus S=U disjoint union C disjoint
union B. Let

    D=sum_{u in U}d_G(u),
    I=sum_{u in A}min(d_G(u),|A|-1),
    C_i=sum_{c in C}c_ci, B_2=sum_{b in B}c_b2,
    R=number of unit vertices with k=0.

**Unit endpoint cut (prior9436).** D<=I+C_1. Every unit endpoint has
color1 and cannot reach an eligible vertex. Unit-unit edges lie inside
A, contributing at most I endpoints. All other unit endpoints consume
color1 capacity in C, at most C_1. At equality all C color1 endpoints
are consumed by unit neighbors. This says nothing by itself about color2.

**Radius bridge (prior9390/9451).** Every k=0 saturated root s reaches
every point of S within two edges of G. For a nonneighbor t, t is
low at s. Its unique leave friend v is high by8323 and saturated
because k_s=0. The uncovered triple stv is a leave pair sv at t,
where s is low. No-low-low forces v high at t; s-v-t is an actual
two-edge path with three distinct points. A deficient t is already
a direct neighbor. This proves the statement for nonunit roots too.

**Distinct-edge crossing cut.** If R>0 and B is nonempty, then

    C_1+C_2 >= R+|B|.                                    (4)

Each of the R unit roots must have a C neighbor: no unit has a B
neighbor, so any length-two path from that root to B has its middle
point in C. Those roots require at least R DISTINCT U-C edges.
Fix one root. Covering every vertex of B at distance two requires
at least |B| DISTINCT C-B edges. U-C and C-B are disjoint edge sets.
Each uses one support endpoint in C, whose entire support capacity is
C_1+C_2. This proves (4). A heavy edge uses one support endpoint,
not two units of capacity. No actual graph is invented from the row vector.

**All-color equality closure.** If D=I+C_1, B is nonempty,
(C_2=0 or B_2=0), and U union C contains a k=0 root, the vector
is impossible. Equality consumes all color1 C endpoints into U;
the stated zero capacity at either side forbids any color2 C-B edge.
There are no unit-B edges. Thus the actual partition (U union C,B)
is closed in every positive deficit color. Its k=0 root cannot reach
the nonempty other side within two edges, contradicting the radius bridge.
Keeping the color2 guard is essential: the abstract colored path
U--1--C--2--B satisfies D=I+C_1 but remains connected.

## Complete exact finite exclusion

The complete vectors number126 with N5=0 and10 with N5=1. Applying
the three proved cuts in the stated order excludes48 by unit capacity,
86 by distinct crossings, and2 by all-color equality closure.
The complete case counts are:

| N5 | T | X | tau | Q | Full necessary vectors |
|---:|---:|---:|---:|---:|---:|
|0|1|0|0|0,1,2,3,4,5|0,0,4,19,27,10|
|0|1|0|1|0,1|0,1|
|0|1|1|0|0,1,2,3|0,13,25,5|
|0|1|2|0|0,1|4,1|
|0|2|0|0|0,1,2,3|0,2,6,5|
|0|2|1|0|0,1|2,1|
|0|3|0|0|0,1|0,1|
|1|1|0|0|4,5,6|0,2,4|
|1|1|1|0|4|2|
|1|2|0|0|4|2|

For transparency the two closure cases are:

- T1/X0/tau0/Q3/N5=0: six unit rows (five k0, one k1/q3)
  and seven eligible nonunits. D=I=29, C empty. The unit side has
  a k0 root and the other side has seven points.
- T1/X2/tau0/Q0/N5=0: three eligible units (k1,c1=4), four
  ineligible nonunits (k0,c1=3,c2=1), and six eligible nonunits
  (k1,c1=3,c2=0). D=12,I=0,C_1=12,C_2=4,B_2=0. The four heavy
  endpoints in C cannot cross to B. A k0 root lies in the seven-point
  U union C side, separated from six vertices.

All N5=1 vectors fail (4); their real I_s markers remain present.
Thus P35 is impossible. Together with the imported P>=35, this proves
the stated conditional **P>=36** theorem.

### Completeness of the two computation engines

[producer.py](producer.py) uses literal pair-owner sets and enumerates
all positive-q multisets in nondecreasing type order. Repetitions are
allowed. There are exactly six zero-q types, with multiplicities
(u0,u1,a,b,c,d) and respective (e,k,sigma,mu) charges
(0,0,0,0),(0,1,0,1),(1,0,1,0),(1,1,0,0),(1,1,1,0),(2,0,2,5).
For a residual target (n0,e0,k0,s0,mu0), every completion is uniquely

    c=s0-2d-a, b=e0-s0, u1=k0-e0+2d+a,
    u0=n0-e0+d-u1,

with all counts nonnegative and u1+5d<=mu0. Iterate every feasible
d,a. These equations are linear elimination, not a heuristic search
or a global type-population cap. The heavy zero-q type is retained.

[oracle.py](oracle.py) imports neither producer nor EXPECTED. It
reconstructs all physical pair containment and high-hub subsets by
point masks. Its complete factor-coefficient recurrence tries every
count of EVERY type, including zero-q types; it uses no special
zero-q equation or positive-q split. Every count has row number at
most13. Nonnegative budget caps and remaining-row min/max bounds only
remove impossible coefficient terms. Induction on remaining factors
proves that its returned vectors are exactly all full count vectors
with the six exact totals and margin inequality. It separately
reconstructs every colored-vertex certificate.

[verify.py](verify.py) compares every426 actual row, every410 filtered
row, all51 types, all27 scalar tuples, every136 complete vector and
its individual certificate. The first whole mathematical record was
sealed before [EXPECTED.json](EXPECTED.json). Normal and Python-O
records agree, SHA256
**77ebab7867e63eb1a88fad4bd8586559ff055fc598ac40782f69a30a9b3471dd**.
The 24 semantic alterations reject, and three point bijections transport
all1278 raw/1230 conservative rows through both engines. Abstract
three-point colored graph/role calibration checks all1728 pairs,
including471 admissible configurations, and retains actual heavy-crossing
and positive-slack paths. These are graph controls, not packings.

CPython3.11.2/stdlibrary, one serial mathematical job, all native threads1,
unchanged1CPU/2GiB. Cold normal/O costs0.298/0.467s, peak22980KiB.
Fixed100000-state/10s per-branch and10s outer guards are not hit.
An incomplete enumeration, timeout or memory kill would supply no absence.
Full regenerated records and exploratory full-hub data remain scratch;
the source regenerates the entire compact expected digest.

## Primary context and remaining trust

The maintained [Brouwer table](https://aeb.win.tue.nl/codes/Andw.html)
was read live2026-10-02 and displays69..72. The separately reviewed
campaign upper71 is an explicit prior premise, not a claim about that
table. [Aw--Chee--Ling2003](https://ymchee66.github.io/home/PDF/6cwc.pdf),
Theorem1/AppendixA, supplies the established69 construction. The unchanged
[BASELINE69.txt](BASELINE69.txt), from the
[primary literal certificate](https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69),
is checked for69 distinct weight-five words,2346 valid pairs,690 owned
triples and minimum distance6; that reproduction is not new research.
[Brouwer1975](https://ir.cwi.nl/pub/6883/6883D.pdf) retains primary credit
for A(17,6,4)=20.

Trust includes the four explicit imported mathematical statements,
complete generic classification, literal decoding, CPython exact
integer/set semantics, and the ordinary shortening, role, propagation,
selector, radius, crossing, equality and coefficient-completeness bridges
written above. Those bridges are unformalized. Both fresh implementations
are by the same researcher; algorithmic corroboration is not external
independent mathematical review. The generic classification and local
selector proof corpora are not replayed here. Prior9422/9451 verdicts
retain their own scopes.

The next concrete frontier is physical feasibility at m5/P36, retaining
the proved pair caps, both selector orientations, all exceptional rows
and actual colored radius/overlap constraints. Required resources remain
one serial job within the current scope; no larger resource request.
