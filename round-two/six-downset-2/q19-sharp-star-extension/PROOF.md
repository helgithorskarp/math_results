# Sharp positive q19 repair with an unpenalized star release

Actual author: **six-downset-2, researcher**, 2026-10-04. Ordinary
computer-assisted proof; **unformalized and independently unreviewed**.
The generic all-count block and capacity reductions are proved in
STRUCTURAL.md. The earlier, sealed private count-flow proof is preserved;
this directory contains the complete extended proof and its source.
No general H/I result, other-count feasibility theorem, optimal spectral
margin, globally largest positivity interval or historical priority is
claimed. The exact endpoint of the DECLARED recipe is distinguished from
the feasible set of all competitors throughout.

## Fixed carrier, comparison and theorem

Use the three-core downset of STRUCTURAL.md with X9,Y10, ground22:
all sets of size at most two, all triples with at least two of a,b,c,
except bcX. Actual empty and its loop are retained. There are N303
vertices, unique maximum a-star size s61, and h242. Star sizes are
61,52,52,nine24 and ten25.

The fixed signed comparison C0 has proper diagonal60, intersecting
offdiagonal-1, and complete a-star anchor completion. On every disjoint
nonanchor pair it has coefficient29u_tu/32768. The 143 integers u_tu
are recovered by EXACT division31 of the defining published q17 table,
LEMMA10278, source65580698bccd45f168ec50272d0ed15e610a3606. Its entire
26,316-byte defining input is copied as COEFFICIENTS.json, SHA256
65f2b0a5170e0a7585d4892c33d72aca7e4479d0e3484dc98ee32b0ad27f1105.
The older q16 u/1024 table is prior defining work of six-downset-3,
10242/source52ce9643a4eb700056e37c0df6e3ed3736f71808. Neither parent's
factors, certificates, margins or executables are input here. The
trial scale29/32 is just a definition of this comparison, not an
inherited H certificate. The mass proof below needs C0's supported
star completion, not a prior PSD assertion about C0.

For epsilon>=0 let F_epsilon contain ALL real actual matrices M that
are symmetric, supported on disjoint sets, stochastic, have
242M+61I PSD, and every allowed ORIGINAL entry at least epsilon.
There is no invariance, rationality, sparsity or extra cap restriction
on competitors. Define C=(242M+61I)_proper-J and

    P(M)=sum_{unordered disjoint {A,B} in B} (C_AB-C0_AB)_+,

where B is all241 proper nonstar vertices. Star trades are unpenalized.

For EVERY REAL

    0<=epsilon<=219061/745406464,

the exact minimum is

    min_(M in F_epsilon) P(M)=8421443/65536+9196 epsilon.       (4)

The explicit real affine family below attains (4). It has both original
endpoint ranks302, simple minimum eigenvalue -61/242 and simple unit
eigenvalue1. All other301 eigenvalues have BOTH gaps at least1/247808.
Every allowed entry has minimum exactly epsilon, including the actual
loop. Among strictly positive supported H competitors the infimum is
8421443/65536, approached by the family but unattained.

The family has largest entry-feasible parameter tau=242epsilon equal
to219061/3080192: for every larger tau its empty/X-singleton entries
violate the requested floor. This asserts maximality only of this recipe;
arbitrary unpenalized star trades or other changes are not excluded.

## Exact budgets and the necessity bound

The budget formulas in STRUCTURAL.md and separate full original-set
checks identify four bad nonstar types:

| Type | Number | Deficit |
|---|---:|---:|
| YY pair |45|362147/32768|
| bY pair |10|10683/32768|
| cY pair |10|10683/32768|
| bcY triple |10|13379/16384|

Thus K has75 members, D=16777855/32768. The actual comparison loop
capacity is ell0=2089103/8192. Consequently

    P0=(D-ell0)/2=8421443/65536.

There are1800 KK,10820 KG,11245 GG edges, totaling23865 individual
unordered nonstar coordinates. Their degrees/capacities are literal
original quantities, not transported q17/q18 counts. The three former
bad star types are10abY,10acY,abc. Additionally aY has positive budget
18079/32768; it will supply anchor slack in the declared repair.

For any competitor set z=3031_S-611. Support, stochasticity and the
star size give z^TMz=-303*61^2 and ||z||^2=303*61*242. PSD of
L=242M+61I gives z^TLz=0, hence Lz=0. It follows that C1_S=0 and
the original empty budgets have exactly the individual-edge formulas
in STRUCTURAL.md. Since each bad empty entry and the actual loop
has C-unit floor tau=242epsilon, the credited mass identity implies

    P>=P0+(75+1)tau/2=P0+38tau.

This applies to arbitrary individual REAL competitors. Equality forces
only their bad empty/loop floors and the KK/KG/GG repair signs. The
star floors chosen below are recipe choices, not additional conditions
on every optimizer. The scalar conversion38*242=9196 proves the
necessity part of (4). Exact primal attainment is paid next.

## New explicit affine repair

Fix tau in[0,219061/3080192] and P_tau=P0+38tau. Start from C0 and apply
the following changes to all indicated unordered disjoint proper
pairs and their transposes:

    beta=(13379/16384+tau)/36,
    eta =(10683/32768+tau)/9,
    alpha=(362147/32768+tau-8beta)/28.

Decrease YY/YY by alpha,630 unordered pairs; decrease YY/bcY by
beta,360 pairs; decrease bY/cY by eta,90 pairs. The other720 KK
edges, YY/bY and YY/cY, have zero change. This is the zeta=0 case
of the exact four-type capacity region.

Increase XX/XX by P_tau/1512 on378 unordered disjoint pair/pair
edges; increase X-singleton/X-singleton by P_tau/72 on36 edges;
increase Y-singleton/Y-singleton by P_tau/180 on45 edges. These
three GG components have total positive masses P_tau/4,P_tau/2,
P_tau/4. Every other NN change is zero, in particular every KG.

For each star vertex D of type aY,abY,acY or abc and EACH of the
nine X singletons x, set

    C_D,x += (ell_D-tau)/9,
    C_a,x -= (ell_D-tau)/9.

All31 such D are disjoint from each x. These anchored trades preserve
each nonstar row's whole-star sum. At the comparison their budgets are

    ell_aY=18079/32768,
    ell_abY=ell_acY=-11507/16384,
    ell_abc=-66079/32768,
    ell_a=527991/32768.

These trades initially make all31 actual empty/star entries tau and
give empty/anchor budget91211/16384-31tau. Apply one additional orbit:
for EVERY one of the45 YY pairs v, set

    C_abc,v -= tau,
    C_a,v   += tau,

and transpose. These45 unpenalized star trades preserve every nonstar
whole-star sum and leave all NN degrees, NN signs, objective and the
actual loop unchanged. They make empty/abc equal46tau and empty/a
equal91211/16384-76tau. Each original a/YY entry, formerly the fixed
827/32768 bottleneck, becomes827/32768+tau. The30 aY/abY/acY empty
entries remain tau. Neither these chosen star floors nor this star
release is imposed on arbitrary competitors.

The positive aY trades supply essential anchor slack to this recipe:
omitting them at the new endpoint violates actual anchor entries.
On Q the extra change is -tau(e_abc u_YY^T+u_YY e_abc^T), where u_YY
is the45-member orbit indicator. It acts only on the trivial sector;
all other sectors are nevertheless freshly checked at the new endpoint.

Original empty entries are completed by L_empty,A=1-sum_B C_AB
over the entire proper row, and the actual loop by
L_empty,empty=1+sum_(A,B proper) C_AB. Set M=(L-61I)/242.
All allowed original positions, including anchors and the loop, are
checked directly. The75 bad empty positions equal tau because the
degrees are28alpha+8beta,9eta,9eta and36beta as required. The total
KK decrease is D/2+75tau/2 and positive GG mass P0+38tau, so the
actual loop capacity is ell0-D-75tau+2P0+76tau=tau. Hence all
mass equality conditions hold, and P=P_tau exactly.

## Entire real interval and exact limit of this recipe

The reader constructs every original endpoint and checks all72,817
ordered allowed-entry inequalities at tau0 and tau219061/3080192. Every
entry and every inequality surplus hM_AB-tau is affine in REAL tau,
so interpolation establishes all inequalities on the whole interval.
The changes alpha,beta,eta and all three positive components preserve
their declared signs throughout, again by the two exact endpoints.

For each original allowed position the reader independently computes
the affine surplus intercept and slope and its upper bound whenever
the slope is negative. The minimum of ALL these bounds is219061/3080192.
Exactly18 ordered positions attain it: empty against every one of the
nine X singletons, in both directions. Their comparison budget is
ell_X=120007/8192. The X/X positive component reduces each budget by
P_tau/9, whereas all star trades have zero net effect on that row.
Consequently their exact floor surplus is

    ell_X-P_tau/9-tau = (219061/65536-47tau)/9.

It vanishes precisely at219061/3080192 and is negative beyond it.
Therefore every larger tau violates this recipe's requested floor,
irrespective of any spectral behavior there. At the endpoint the anchor
has positive surplus279971/3080192, so it causes no earlier constraint.
There are211 permanent ordered floors in the recipe: the actual loop,
75 bad empty incidences and30 chosen star incidences with both directions.
Only the former151 positions are forced by
mass equality, rather than this particular witness choice.

## Fresh physical positivity and both ranks

The separate same-author physical reader reconstructs all original sets
from named core pairs; it does not use the generator's membership
predicate. It checks every91809 position of both original lift
identities, every90601 inverse-metric position in BOTH products, every
row/kernel/support equation and all302 proper star-kernel equations.
Its full physical basis on Q has301 vectors:

    22 trivial,64 X-standard,81 Y-standard,
    27 XX-harmonic,35 YY-harmonic,72 XY-mixed.

Every cross-sector Gram entry and each declared metric are checked.
Every original row image of EVERY basis vector at BOTH residual
endpoints is verified,181202 action positions per tau endpoint.
The ordinary all-count decomposition and action derivation in
STRUCTURAL.md establishes independence/completeness and the meaning
of the metrics. The dimension count alone is not used as a bridge.

At EACH endpoint all12 weighted quadratic/scalar forms minus1/1024
times their physical metric have fresh strictly positive exact LDL
pivots. All1264 entries of their full factor identities and all84
pivots are recomputed; no factor, minor or margin from another count
is used. Independent literal and generator hashes bind the entire
original L and T, so the entry and spectral statements concern the
same declared matrix. These comparisons prove T>=I/1024 and
Bcap=303G^-1-T>=I/1024 at both endpoints.

Both matrices depend affinely on real tau. PSD order is preserved by
convex interpolation, proving the same full comparisons throughout.
The original congruences, G>=I and the centered-star projector in
STRUCTURAL.md yield both rank302, simple extremes and the remaining
301 lower/upper gaps1/(242*1024)=1/247808. The entry minimum is exactly
tau/242 because the actual loop and the75 bad empty entries attain it.
For tau>0 this is a strictly positive supported H matrix.

The preceding necessity and this explicit feasibility prove (4).
Taking tau down to zero gives the strictly positive infimum P0.
Every strictly positive competitor has a positive minimum over its
finite set of allowed entries; the universal row/loop bound then
makes its cost strictly greater than P0. Thus that infimum is not
attained in the strictly positive class.

## Structural capacity consequences outside the constructive interval

The four-type KK capacities, in the order YY/YY,YY/bY,YY/bcY,bY/cY,
are84533/32768,17921/16384,19371/16384,25083/32768. Substituting the
actual deficits into STRUCTURAL.md(2) gives EXACTLY

    0<=tau<=25083/32768

as the interval in which SOME individual KK decrement flow pays every
bad degree and its proper capacity. All11 affine inequalities are
checked symbolically via their intercepts/slopes; endpoints and every
individual KK degree/capacity are freshly verified. Beyond that limit
the bY/cY capacity prohibits a nonpositive change. This is ONLY a
KK-flow statement and imposes no PSD/star/GG sufficiency.

A stronger early obstruction comes from the405 YY/X-singleton KG
edges. Each has comparison C-unit entry3755/8192 and MUST have zero
change to saturate the old affine mass bound. Formula(3) gives for
EVERY real tau>=0 and EVERY original H competitor of entry floor
tau/242 the universal necessary bound

    P>=8421443/65536+38tau
                        +(405/2)(tau-3755/8192)_+.

The complete piecewise envelope also includes all other KK and KG
capacities, with their individual unordered multiplicities. Thus the
old affine bound cannot be sharp above tau3755/8192. This does not
prove H infeasibility, locate a globally optimal cost curve, or claim
sharpness in the gap between the constructive interval and that
obstruction. These are concrete next frontiers.

## Trust and publication boundary

Exact integers/rationals, the programs and ordinary completeness,
interpolation, Rayleigh/kernel and congruence proofs are the trust
boundaries. They are not a formal proof assistant or an independent
review. No floating point search, timeout, UNKNOWN or interrupted
enumeration supplies a mathematical conclusion. The all-count block
criterion and capacity iff are ordinary proofs with explicit
conditional premises; finite controls do not assert other-count H.

Final frozen normal/optimized/source-only-cold replays and semantic
fault controls are reported in PRIVATE-REPLAY.json when completed.
The source-first Git/remote/direct-reader/original atomic graph gates
remain a separate future publication obligation; no new commit or
graph acceptance is implied by this private proof.
