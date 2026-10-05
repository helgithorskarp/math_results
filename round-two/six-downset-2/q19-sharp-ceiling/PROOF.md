# Exact q19 sharp ceiling and a cost kink

Actual author: **six-downset-2, researcher**, 2026-10-05.
Ordinary proof with rational computational certificates; unformalized
and independently unreviewed. The self-contained reader includes the
explicitly credited same-author defining modules and complete certificate
data. VALIDATION.json records actual source-only normal/optimized,
semantic adverse-input and isolated cold checks. Source publication and
actual graph commitment remain separate obligations. SOURCE.json records
the paid private predecessor and every source-reader edit; certificate
creation-time private/null metadata is historical, not a claim about
publication or graph commitment.

## Fixed original problem and precise claim

Use the SAME carrier and comparison as actual contribution10332/0,
source58f9c6ab8b6ab58232cd275ddb4691d3430fb02f, and the complete free
coordinates of the same-author source
[fe4bf0695998eda55018095b6f09cee0a4666134](https://github.com/helgithorskarp/math_results/blob/fe4bf0695998eda55018095b6f09cee0a4666134/round-two/six-downset-2/q19-full-optimizer-face/PROOF.md).
Its separate graph submission is accepted-pending, not a committed premise.

Let a,b,c,X,Y be disjoint with |X|=9, |Y|=10. D contains every set of
size at most two and every triple with at least two core points, except
the bcX triples. The empty set and its loop are retained. Here N=303,
the unique largest a-star S has size s=61, h=N-s=242,
B=D\\(S union {empty}) has size241, and Q=D\\{empty,a} has size301.

An original competitor is an INDIVIDUAL-REAL symmetric M on D with
M1=1, M_uv=0 when u intersects v, M_uv>=epsilon on every disjoint
ordered pair INCLUDING the actual empty loop, and L=61I+242M>=0.
Put tau=242epsilon>=0. At tau=0 the nonnegative closed relaxation is
included; positive tau gives positive entries on every allowed position.
No invariance or additional upper PSD condition is assumed.

On proper vertices write C=L_proper,proper-J. On every unordered
disjoint NN edge e in B define delta_e=C_e-C0_e and
P=sum_e max(delta_e,0). The comparison is the fixed exact143-coefficient
table29u/32768 derived from published defining fixture10278, source
65580698bccd45f168ec50272d0ed15e610a3606. Its negative empty budgets
have types YY,bY,cY,bcY and form K of size75. Write G=B\\K and use
KK/KG/GG for edges with two/one/no endpoints in K. Set

    P0=8421443/65536,
    U=42901/98304,
    r=1/32768,
    U+r=5363/12288.

We prove for this FIXED original carrier, comparison and cost:

1. Every original competitor satisfies

       P >= P0+38tau+810 max(tau-U,0).                  (1)

   Thus sharp cost P=P0+38tau is impossible for tau>U. This is a
   cost ceiling, not nonexistence of an H matrix above U.
2. New full-original rational matrix certificates at U and U+r,
   together with the credited fe4 tau0 center and affine interpolation,
   attain (1) for EVERY REAL tau in[0,U+r]. In particular the largest
   sharp-cost floor is epsilon*=U/242=42901/23789568, and on the stated
   interval the exact unrestricted minimum is

       min P = max(P0+38tau,848tau-14745097/65536).

   Equivalently its two slopes in epsilon are9196 and205216. No
   statement about the minimum cost above tau=5363/12288 is made.
3. At tau=U every sharp optimizer has9000 additional independent
   fixed GG coordinates. Its full affine hull has dimension15969,
   and its S9xS10-invariant affine hull has dimension104. At EVERY
   tau in[0,U), these dimensions are24969 and113 respectively. The
   relative interior at U is exactly strict unforced entry/sign
   constraints and positive definite T. No geometry classification
   above U is claimed.

The full spectral certificates give T,Bcap>=I/1024, both original
endpoint ranks302 and all other301 lower/upper eigenvalue gaps at
least1/247808 at the two new endpoints and throughout their affine
segment. This is a sufficient gap, not a maximal one.

## Credited original kernel, mass identity and complete coordinates

The original star Rayleigh argument of10332 forces Lz=0 for
z=N1_S-s1, and L1=N1. Hence C1_S=0. Its fixed star principal block is
sI-J. Exactly35865 disjoint unordered edges of Q are independent
real free coordinates. The remaining proper anchor coefficients and
actual empty row/loop are completed by

    C_a,v=-sum_(D in S\\{a}) C_D,v,
    L=[[1+sum_i r_i,(1-r_i)_i],[(1-r_i)_i,(1+C_ij)_ij]],
    r_i=sum_j C_ij.                                    (2)

Consequently, for every proper nonstar v,

    E_v=ell_v^0-sum_(NN edges incident to v)delta_e,
    E_0=e0^0+2sum_(all NN edges)delta_e.                 (3)

E_v is the actual C-unit empty/v entry hM_empty,v and E_0 is the
actual C-unit empty loop hM_empty,empty. Star trades cancel EXACTLY
in (3); these are individual-coordinate identities without averaging.
The comparison constants satisfy sum_K ell_v^0+e0^0=-2P0.

The credited complete mass identity, whose generic method is also
credited to contributions10296/10306, therefore says, with
Delta=P-P0-38tau,

    2Delta=sum_K(E_v-tau)+(E_0-tau)
      +2sum_KK delta_+ +sum_KG |delta|+2sum_GG delta_-. (4)

Here delta_+=max(delta,0), delta_-=max(-delta,0). Every term on the
right is nonnegative under the original entry floors. In particular
Delta>=0, and equality is EXACTLY

    E_v=tau for all75 v in K, E_0=tau,
    delta_KK<=0, delta_KG=0, delta_GG>=0.               (5)

The full original PSD test is retained. In the residual lift of10332,
T=C_Q,Q and Gmetric=I+rr^T+bb^T, with r the free-star indicator and
b=1-r. Then Gmetric^-1=I-rr^T/61-bb^T/242, and

    L=J+Phi T Phi^T,
    NI-L=Phi Bcap Phi^T+zz^T/(s*h),
    Bcap=N Gmetric^-1-T.                              (6)

The301 columns exhaust {1,z}^perp. Thus lower PSD is equivalent to
T>=0. The original competitors are nonnegative, symmetric and
stochastic, so v^T(I-M)v=sum_(i<j)M_ij(v_i-v_j)^2>=0; upper PSD is
automatic, not an extra competitor premise. Bounds T,Bcap>=dI
give the rank and eigenvalue statements above by (6), with gaps d/h.

## A direct individual-real18-floor dual identity

Let W consist of all90 nonstar XY vertices. Each t={x,y} in W has
exactly nine disjoint Y singletons and eight disjoint X singletons.
Their comparison C-unit proper entries and t's empty budget are

    eY=13599/32768,
    eX=6785/16384,
    ellXY=26455/32768,
    ellXY+9eY+8eX=18U.                               (7)

Let J_t be these17 selected singleton neighbors. For each selected
proper edge E_tu=hM_tu=1+C0_tu+delta_tu. By (3), canceling the
selected deltas gives the original identity

    E_t+sum_(u in J_t) E_tu
       =18U-sum_(remaining NN neighbors u of t)delta_tu. (8)

Set A=sum_(t in W)[(E_t-tau)+sum_(u in J_t)(E_tu-tau)]>=0.
There are1620 scalar floor terms, including1530 distinct selected
proper edges. For any NN edge e, let m_e count its endpoints in W,
except that m_e=0 on selected edges. Then m_KK=0, m_KG is0 or1,
m_GG is0,1 or2. Summing (8) gives

    1620(tau-U)=-sum_e m_e delta_e-A.                 (9)

Combine (4) with (9):

    2Delta-1620(tau-U)
      =sum_K(E_v-tau)+(E_0-tau)+2sum_KK delta_+
       +sum_KG(|delta|+m_e delta)
       +sum_GG(2delta_-+m_e delta)+A >=0.             (10)

The KG term is nonnegative for m_e=0 or1. Each GG term equals
m_e delta_+ +(2-m_e)delta_- and is nonnegative. Thus
Delta>=810(tau-U). Combining with Delta>=0 proves (1) for all
individual-real competitors. No symmetry, rationality or upper PSD
assumption was introduced in this argument.

DUAL.json additionally records a compact exact Farkas certificate for
the complete143-invariant-coordinate ENTRY relaxation, plus tau. It
has220 explicit inequalities,30 equalities and all variables otherwise
unbounded. check_structure.py regenerates the whole canonical instance,
checks the full144-coordinate multiplier identity and nonnegativity,
and obtains U EXACTLY. ENTRY-PRIMAL.json is an exact feasible entry-only
vertex at U. Its lower PSD is NOT asserted. The separate fresh dense
boundary matrix is the spectral attainment certificate. The direct
proof (8)-(10) makes the real and nonsymmetric conclusion independent
of a symmetry-reduction inference from the LP.

## Equality at the ceiling and original affine dimensions

For sharp Delta=0, (5) gives KG=0 and GG>=0. At tau=U, (9) forces
A=0 and every GG edge with m_e>0 to have delta=0. Thus EVERY
selected proper edge is at its entry floor U and every empty/XY
entry is also U. The seven zero-repair GG orbit counts are

| GG orbit | Individual unordered edges |
|---|---:|
| XY/XY | 3240 |
| XY/XX | 2520 |
| XY/b | 90 |
| XY/bX | 720 |
| XY/c | 90 |
| XY/cX | 720 |
| XY/bc | 90 |
| Total zero GG | 7470 |

The810 Y/XY and720 X/XY edges are fixed at their proper floor, with
repairs U-eY=263/12288 and U-eX=2191/98304, both positive. These
1530 coordinates are distinct from the7470 zero GG coordinates.
All9000 are independent original coordinate rows. Conversely these
fixed coordinates plus KG=0 imply the90 empty/XY floor equations
by (8), so those90 equations add no rank.

Let E* be the original affine space given by KG=0, the9000 GG
coordinate values above, all75 bad empty floors and the actual loop
floor. The complete boundary optimizer set is E* intersected with
the original entry halfspaces, remaining sharp sign halfspaces and
T>=0. This is a complete description, not just an invariant template.

The literal census is KK1800, KG10820, GG11245, star12000. After
deleting the10820 KG and9000 fixed GG columns, the75 bad-degree
rows still have the unsigned KK incidence matrix. Its graph is
connected and nonbipartite: YY includes the triangle of disjoint
pairs Y0Y1,Y2Y3,Y4Y5; all YY vertices connect through a disjoint
YY neighbor, and each bY/cY/bcY vertex connects to a YY pair
avoiding its Y. A left-null row alternates signs along each edge;
the odd cycle and a74-edge spanning tree force all75 coefficients
to zero. The loop is independent because a surviving Y/Y GG
column has coefficient2 there and0 on every bad-degree row. Hence

    dim E*=35865-10820-9000-75-1=15969.                (11)

In invariant coordinates the same deletions fix25 KG and nine GG
columns. The five remaining bad-type/loop equations have rank5:
the surviving columns Y/Y,YY/YY,YY/bY,YY/cY,YY/bcY have minor
determinant of absolute value117573120. The checker verifies both
complete rational inverse products. Thus the invariant dimension is

    143-25-9-5=104.                                   (12)

The new boundary center below is strict in every remaining scalar
and sign constraint, and T is positive definite. By finite continuity
and PD openness it has a relative open ball in E*. Therefore (11)
and (12) are the ACTUAL affine hull dimensions. Relative interior
is exactly these strict conditions: a zero nonforced scalar or sign
constraint gives a proper supporting face because the center is
strict. A nonzero v with v^TTv=0 also gives a proper supporting
face because the center's quadratic value is positive. Conversely
strict scalars and PD give a relative open neighborhood. The same
argument applies in the invariant intersection. These ordinary
rank/openness/relative-interior bridges are not formalized.

For every tau<U, interpolate the credited fe4 tau0 center with the
new U center by weights1-tau/U and tau/U. KK stays strictly negative,
every GG repair is strictly positive, and every formerly nonforced
entry remains strictly above its floor, because the tau0 center is
strict and has positive weight. T and Bcap remain>=I/1024. The
credited complete pre-ceiling rank argument therefore gives full
24969 and invariant113 dimensions for EVERY tau in[0,U). A uniform
relative radius as tau tends to U is not asserted.

## Fresh exact boundary and an attaining post-ceiling line

BOUNDARY-CANDIDATE.json gives every143 free coordinate at tau=U.
Its whole-file SHA256 is
70b689016621c1bac532ccf043301865753462d96d968c19566f05a4e6187ff0.
check_boundary.py decodes the complete new matrix from original D
twice in explicitly reused same-author representations, compares
EVERY L and T position, and checks every72817 allowed ordered
position, all rows/support/centered-star identities, full23865 NN
cost/sign coordinates, and every actual loop. P=28524805/196608
equals P0+38U. All3391 tight positions are the151 bad/loop positions,
180 ordered empty/XY positions, and3060 ordered selected proper
positions. All7470 forced GG zeros are counted explicitly.

Every remaining C-unit entry surplus is at least42421/3145728 and
every unforced strict KK/GG repair magnitude is at least14127/1048576;
both exceed1/256. The complete original301-vector basis and all90601
Gram positions, both original row actions (181202 positions), all241
star range columns and58081 original Schur identities/actions are
checked. Fresh exact factor identities pay all six reduced physical
Schur forms and all twelve full physical forms shifted byI/1024.
The original metric/completeness bridge (6), not floating status,
turns these facts into the full spectral certificate.

Starting at this boundary table, set tau=U+t. Change ONLY these eight
invariant NN repair coordinates, by t times the indicated derivative:

| Coordinate | Derivative |
|---|---:|
| Y/XY | 1 |
| X/XY | 1 |
| XY/XY | -1/4 |
| Y/Y | -682/45 |
| YY/YY | -1/84 |
| YY/bY | -1/36 |
| YY/cY | -1/36 |
| YY/bcY | -1/36 |

Leave every other coordinate unchanged. The four bad-type empty
floors have derivative1: for YY its incident KK derivative is
28*(-1/84)+3*8*(-1/36)=-1; for bY/cY/bcY it is36*(-1/36)=-1.
The empty/XY derivative is -9-8-72*(-1/4)=1. Selected proper-floor
derivatives are1. The total NN direction sum is

    630*(-1/84)+3*360*(-1/36)+810+720
      +3240*(-1/4)+45*(-682/45)=1/2,

so the actual empty loop derivative is1. Thus all eight forced
scalar floors follow tau exactly.

At t=r, POSTLINE-CANDIDATE.json gives the complete143 coordinates,
whole SHA2563ed5f72aad412fd7d4c140b69bc7bfe31710e1328a4760c649a37da71940fd83.
check_postline.py retains the full-original basis, action, Schur and
factor checks above, changing only the new endpoint equations and
repair sign expectations. It certifies the same spectral floorI/1024,
all3391 forced original floor positions, every other entry surplus
at least42325/3145728, and every other strict sign margin at least
14127/1048576. Exactly3240 GG repairs are now negative and4230
remain zero; check_structure.py computes both counts from the literal
original edge census and the whole endpoint data.

All original entries, support/row equations, T and Bcap are affine
in this line. Their two certified endpoints imply the entry floors
and spectral bounds for EVERY REAL t in[0,r] by convexity. KK is
negative, KG zero, the XY/XY repairs are nonpositive, six other
special GG orbits stay zero, and all remaining GG repairs are positive
throughout. Consequently P is affine, with derivative

    810+720-682=848.

The negative KK and XY/XY directions contribute no positive-part
cost. Thus P=P0+38(U+t)+810t, attaining (1). The new upper cost is
28529893/196608. The credited tau0-to-U interpolation gives the
other branch of (1), completing the exact minimum on[0,U+r].

## Evidence, provenance and boundaries

The primary problem is EFF Conjecture H, Section4 of
[arXiv2609.28404v1](https://arxiv.org/html/2609.28404v1#S4), live
reverified2026-10-05 (v1 remains the listed version). No general H,
I, arbitrary carrier/count, sharpest spectral gap or global maximal
H entry floor is asserted. The comparison, original completion,
mass-identity method and complete physical lift are credited prior
results. The NEW content is this exact fixed-q19 sharp ceiling,
unrestricted cost kink, attaining post-ceiling segment and equality
dimension change.

Private discovery used floating HiGHS only to find a dual/entry guess
and floating SCS only to find a new dense endpoint. Exact recovery solved
the entry-only LP equations and the five original endpoint floor pivots
after rational rounding. Those search scripts and their logs are not
required inputs and are omitted from this compact reader. The proposed
post-ceiling line is exact algebra. No solver optimum,
timeout, UNKNOWN, memory kill or unsuccessful rationalization is used
as proof. The earlier failed direct LP rounding and preliminary
entry-only witness have no claimed original PSD certificate.

All final mathematical checks use Python3.12.14 Fraction/integer
arithmetic. The new checkers import neither search nor recovery.
They disclose and byte-bind the same-author model.py and physical.py
copied verbatim from fe4, its locally addressed encoding.py and the
complete defining fixture before mathematical use. Closed fe4
endpoint factor/EXPECTED/positive drivers are not rerun as new evidence.
The prior tau0 center is an explicitly credited published premise.
These checks are author verification, not independent review.
All-real identity, coordinate completeness, full physical-sector
completeness, interpolation and affine-hull bridges are ordinary
proofs; no proof-assistant theorem is claimed.
