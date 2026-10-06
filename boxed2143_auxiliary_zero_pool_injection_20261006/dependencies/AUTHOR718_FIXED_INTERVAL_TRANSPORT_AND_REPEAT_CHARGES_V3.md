# Fixed intervals, birth groups, and a quadratic greedy completion bound

Quinn / literature-researcher-3,2026-10-06. New AUTHOR partial proof, pending a
different researcher's ENTIRE internal check. No claim here inherits acceptance
from648/682 or678/699. Full agreed target410 remains UNSOLVED. The outstanding
quantitative obligation is the actual-source sum
`sum_(n<m) E[A(C(sigma_n))]/(n+1)=o(m log m)`; this text supplies transport and
an obstruction to one proposed way of paying that sum, not its estimate.

Dependencies: accepted444 maximum-insertion blockers;467 Cartesian splitting;
534 leaf-language legality;592 greedy termination/source policy;632 original-gap
conditional law;648/682 exact path cost and pair/blocker COUNT bijection.
678/699 supplies context about energies/records but is not needed in this proof.

## Persistent identities and exact single-insertion rules

Every point receives its increasing global birth value. Insertions never change
existing values or reorder existing points; identify a fixed point by that
value, not its shifting position. Let its current zero-based position be j.
Let ell be its nearest greater left position, or-1, and r its nearest greater
right position, or N=length(current word). The latter sentinel denotes END,
not a genuine greater endpoint. Actual gap weights are w_g=1 immediately before
each ORIGINAL point and at END,0 before each auxiliary point. Define

    K_j = sum_(j<g<=r) w_g.

This quantity is defined for EVERY existing point, eligible or not. Eligibility
additionally requires real endpoints ell,r and value(ell)<value(r). Include
original and auxiliary points throughout; no uniform law on current points or
tree shapes is assumed.

Insert a new global maximum at gap k with new-left-boundary weight z: z0 for an
auxiliary and z1 for an original. The right copy of the cut boundary keeps its
old weight. For an existing point:

* If j<k<=r, the new maximum is its nearest greater right endpoint. Its new
  mass is exactly `sum_(j<g<k) w_g + z`. Its left endpoint persists, and it is
  newly eligible exactly when ell is real.
* Otherwise its mass is unchanged. If ell<k<=j, the new maximum is its nearest
  greater LEFT endpoint, and the point is ineligible: its right endpoint is
  either absent or smaller than that new left endpoint. If k<=ell or k>r,
  both old nearest greater endpoints persist and eligibility is unchanged.

These three position cases partition all gaps, including cuts at j, r and END.
The strict/inclusive endpoints distinguish the new maximum's left boundary
from the old boundary transported to its right. The rules follow directly by
the new maximum exceeding every old value and by the nearest-endpoint definition;
they require neither avoidance nor a repair-count formula.

At its birth the new maximum has no greater endpoints and is ineligible.
Its mass is `sum_(k<=g<=N) w_g`, including old END and excluding its new left
boundary z. This is true for either tag. Births can thus have many original
gaps on their right; assigning them zero mass would be incorrect.

Every actual auxiliary has z0. Every actual original is inserted at a unit
boundary, even after its preceding repairs, so has z1=w_k. The displayed rule
therefore implies that K_j cannot increase at ANY later actual insertion.
A zero mass is permanently zero. A point without a greater right endpoint
always has K_j>=1 because END has mass1; hence a zero-mass point has a real
auxiliary right fence. No later source arrival can create a unit boundary
inside such a zero-mass interval. This statement is about the source policy,
not arbitrary maximum insertion at a zero-weight boundary with z1.

## Exact cap from a selected original gap and conditional drift

At a completed history with n originals, let a selected ORIGINAL gap g lie in
the fixed point's initial interval and let s be its ordinal among that
interval's K_j unit gaps, ordered left to right. Then, after the ENTIRE next
original episode,

    K_j(next) <= s.

The endpoint of the selected original gap, or END, remains the target throughout
repair. Auxiliaries lie strictly before that target. If an auxiliary is inserted
inside the initial interval at or before the target, it installs a closer right
fence with zero new boundary; its new mass is at most s-1. Monotonicity supplies
the rest of the claim in this case. If no such auxiliary occurs, the selected
unit boundary is still in that interval when the original arrives, and the
original's split caps the mass at exactly s. Auxiliaries before the fixed point
or outside its right fence cannot increase its mass. The argument includes a
selected END boundary. If the selected original gap is outside the initial
interval, monotonicity instead gives K_j(next)<=K_j.

Conditional on the actual completed source history, each of n+1 original gaps
is selected with probability1/(n+1), by632. There are exactly K_j choices inside
the interval. Summing the caps s1,...,K_j and K_j for the other choices proves
the all-history inequality

    E[K_j(next)|history]
        <= K_j - K_j(K_j-1)/(2(n+1)).

The fixed point persists in every child. This finite conditional inequality
needs no independence between successive episodes and does not average over
a uniform list of points. It bounds one already existing point and does NOT
sum over the random number of future auxiliary births.

## Every repair has one precise pre-episode charge label

For an illegal target path let w=qRRv use its FIRST offending RR after an
earlier L, and let j be the point reached by qR. The checked648 proof cuts in
j.left and transforms that target path into R L^(#L in q) Rv. Precisely this
first offending pair disappears. Node j stays, every later offending-pair
minimum in v stays with the same identity, and no new offending pair is born.
This label preservation follows from the same split proof: only old R ancestors
before the cut are removed from the suffix path, and the subtree j.right and
its path v are untouched. Removed ancestors precede the first offending pair;
they supply no later counted-pair minimum.

Induction identifies each actual auxiliary with a DISTINCT eligible minimum
of the INITIAL parent whose interval covers the selected original gap. Every
such minimum is charged exactly once in that episode, in path order. No newly
born auxiliary is charged in its own birth episode. Original and previously
born auxiliary minima may both be charged. Thus the exact cost identity can
retain point identities rather than only its total count:

    cost(episode) = sum_(existing points j)
                   1{j initially eligible and selected g in j's interval}.

Its conditional expectation is A/(n+1), as before. A given fixed point may be
charged again in later episodes; the next family makes that failure uniform.

## One auxiliary can be charged arbitrarily often while its mass stays one

For every n>=6 take the source

    s_n=(5,2,n,n-1,...,6,1,4,3).

The descending segment is just6 at n6. Processing the first four ranks has
source restriction2143 and produces (2,4,1,5,3), with the point of birth value4
auxiliary and the other points original. Rank5 is inserted legally at the
first gap, giving(6,2,4,1,5,3). Rank6 is inserted before original1, after that
auxiliary, at a path RLRL, hence legally. The completed source s_6 is
(6,2,4,7,1,5,3), with original tags(5,2,None,6,1,4,3). The earlier illegal
rank4 gap has first offending minimum1 and is repaired at its rightmost earlier
legal gap, so this base uses the actual greedy policy.

Uniform induction gives the exact output for EVERY n>=6:

    (6,2,8,10,...,2n-6,4,2n-5,2n-7,...,7,1,5,3).

The increasing auxiliary list is empty at n6. Its tags are
(5,2,None,...,None,None,n,n-1,...,6,1,4,3), with n-6 auxiliaries in the first
list and the additional old auxiliary4. Total auxiliaries are n-5 and output
length2n-5. All maximum insertions are legal from avoiding parents.

To prove the induction, the current root is the original2n-5. In its left
subtree, the root is6 for n6 and2n-6 for n>6, with auxiliary4 in its right
subtree and no point between4 and the current root. The next source rank is
placed immediately before original n, so the desired leaf is just after4.
Its path is LRR, with the FIRST offending minimum precisely auxiliary4.
The rightmost legal earlier gap is immediately before4. At n6 this is the
rightmost leaf in4's left subtree, the singleton original2; at n>6 that left
subtree is empty. Its path has no offending pair. Every later earlier leaf
is the illegal target; hence this is the actual prescribed repair gap.

Insert auxiliary2n-4 there. The target word becomes RLR and is legal. Insert
original2n-3 just after4, before old original n. The resulting word is exactly
the displayed formula for s_(n+1). Thus each of these later ranks creates ONE
auxiliary and charges the SAME birth point4.

At every completed s_n, this old auxiliary has K_4=1: its only unit boundary
before its nearest greater right endpoint is the gap before the current
original maximum. Its nearest greater left endpoint is6 at n6 and2n-6 at n>6,
strictly below the right endpoint2n-5, so it is eligible. Both its initial and
final masses in the distinguished continuation equal1. It is charged n-6
times by the end of s_n, unbounded as n grows. It was born earlier and is not
charged in that original birth episode.

This refutes every assertion that a current point is charged at most a fixed
constant number of later times. It also shows why decrease of a static
function of THAT point's K alone cannot pay each of its individual charges:
K remains1. It does not reject time-dependent potentials, transfers from
other nodes, eligibility/birth accounts or the full population estimate.
Each particular source has probability1/n!; this family has linear total
length and is not a superexponential growth proof or an adverse average bound.

## All births in an episode: ordered fences and a quadratic completion bound

Let the auxiliary cuts in one episode be k1,k2,... in their then-current gap
coordinates. After a legal auxiliary at k, the two gaps k+1,k+2 are legal by
accepted592. The updated desired gap is larger than k+1; if still illegal it
must be strictly beyond k+2. Hence the next rightmost earlier legal cut is at
least k+2. Auxiliary birth positions are thus strictly increasing from left
to right, in the same order as their strictly increasing birth values. The
final original is to the right of every new auxiliary and larger than all.

At the completed episode every new auxiliary has no greater LEFT endpoint:
all old values are smaller, and all later new maxima lie to its RIGHT. Its
nearest greater RIGHT endpoint is the next new auxiliary, or the final new
original. The last original is the global maximum. Thus ALL new points are
ineligible at this completed birth stage, despite possibly positive mass.

The new auxiliary intervals partition the gaps strictly after the first new
auxiliary through the gap immediately before the final original. With initial
parent weights w, initial target g, and first cut k1, their total mass is

    sum_(new auxiliaries a) K_a = sum_(k1<=h<g) w_h +1.

The1 is the NEW original boundary, not a weight for an auxiliary. The original's
own birth mass is sum_(g<=h<=N) w_h. Consequently the total mass of EVERY newly
born point, original and auxiliary, is sum_(k1<=h<=N) w_h+1 <= n+2 in an
n-original parent. When there is no repair the only birth has mass
sum_(g<=h<=N) w_h <= n+1. These statements include first and END cuts. They
bound newborn mass without incorrectly bounding the number of births by it:
several new auxiliaries may have zero mass.

Keep the source episode as an auxiliary's immutable GROUP label. For any two
auxiliaries a,b in the SAME group with a left of b, value(a)<value(b) forever.
The point b itself is a permanent greater right witness for a. Therefore a's
current nearest greater right endpoint is at or before b, while b's own
interval starts strictly after b. Their intervals are disjoint as sets of
current gaps at EVERY future stage, regardless of later insertions. This is
stronger than summing their individually nonincreasing masses. It does not
assert disjointness between different groups.

At a future selected original gap, at most ONE auxiliary minimum in each
existing birth group can cover the gap. The exact pre-episode charge-label
bijection above then proves

    cost(next episode) <= n + G <= 2n,

where n is the number of existing ORIGINAL points and G the number of prior
source episodes that created auxiliaries. There are at most n such episodes;
no new birth is charged in its own episode. Eligibility can only reduce this
count. Existing original points contribute at most n distinct charge labels,
and all existing auxiliaries contribute at most G. This proves a UNIFORM
quadratic improvement of the accepted exponential termination bound:

    length(greedy completion of ANY m-point source) <= m^2,  m>=1.

Indeed sum_(n=0)^(m-1) 2n=m(m-1), and there are m originals. This is a full
all-size statement ABOUT THIS PARTIAL TOOL, pending an entire different
researcher's check. It does not solve agreed410: m^2 is too large for the
useful sublogarithmic-cost entropy bridge. The required average bound remains
little-o(m log m), and rare recurrent groups still need their actual source
weights. No linear/sublogarithmic average follows from the quadratic bound.

## Falsifiable controls and remaining obligation

The new fixed_interval_controls_v1.py and separately extended fixed_interval_controls_v2.py is a same-author exact control, not an
independent team check. Its domain is ALL154 sources0..5 and every one of their
873 next original choices, plus ONLY the directed s_n parents n6..12 and every
original choice for these seven parents. It checks full literal avoidance at
every executed original/auxiliary child, every old/new point identity and exact
mass/eligibility/birth rule, the selected-unit ordinal cap, exact charge labels,
and each fixed point's complete conditional sum. History generation repeats
some older stages; those are not additional distinct input populations. It
checks the recurrent family's distinguished continuation, actual word/tags,
old auxiliary eligibility/K1 and one charge of identity4. Version2 additionally checks every new birth
mass/left endpoint, increasing auxiliary cuts, exact newborn mass partition,
EVERY group interval separation and distinct group charges, and the bound
cost<=n+G<=2n, on the SAME pinned finite domain. Version1 sources/results
and original pre-run proof are unchanged. The720 next children from S5 represent all source-rank extensions to size6,
but S6 parents are NOT themselves each tested with all seven next gaps. No
complete S6 parent-with-every-next-gap or larger source-input domain, and no
globally minimal obstruction, is claimed. Domain, sources,
time/point caps and first-failure stopping rule are pinned BEFORE execution.

The all-size arguments above and every deterministic control require a fresh
whole internal check. Until then their status is AUTHOR. Even if accepted,
neither the negative drift for one existing node, the recurrent family, nor
the quadratic bound supplies the useful little-o(m log m) estimate over ALL
original/auxiliary births under the actual source law.
The next genuinely quantitative milestone is an all-birth charging inequality
with a controlled expected influx; K1 recurrent charges and nonzero birth
masses must be included, rather than silently excluded or assigned to a
uniform current-node law. No such useful inequality is proved here.
