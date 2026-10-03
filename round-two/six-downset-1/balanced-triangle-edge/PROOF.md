# Balanced repeated private triangles on an old edge

Actual author: six-downset-1, researcher, 2026-10-03.
Ordinary author lemma with an exact sign certificate. The original-space,
completeness and Schur bridges are unformalized. Independent review and
formalization remain pending. Scope is n=2 only. No general H/I, h1,
unequal repeat counts, arbitrary old cube or optimality/priority claim.

Primary target: Ellis--Filmus--Friedgut Conjecture H,
https://arxiv.org/html/2609.28404v1#S4 . Live abs/Section4 check on2026-10-03
saw Sep23v1 only and proposed H/I. Classical/projection-packing proofs
are distinct. Baseline9986/source8b611aa69692e07c8dff1beb77b79609f2b5f08b
supplies credited exact utilities and the one-heavy/one-light n2 proof;
its entire original h2 record was reproduced before this new work.
Ordinary H/greatest-rank existence is prior9361. This result concerns
balanced repetitions at BOTH marks, a cap domain excluded from9986/9926.
Products cannot identify private facets or the old two points to produce
this original family. External verdict9870/9968 does not transfer.

## Statement

For EVERY integer h>=2, take an old edge{x,y}, h triangles{x,a_i,b_i}
and h triangles{y,c_i,d_i}, all2h private pairs mutually disjoint and
outside{x,y}. Let D be their downset, retaining empty and its loop.
Here n=2 denotes the old cube; the entire ground has4h+2 points.
Then N=12h+4,s=3h+2. Exactly x,y have largest point-stars; each private
point star has size4. The construction below gives a rational original
symmetric M with intersecting entries0, M1=1, L=(N-s)M+sI PSD and M<=I,

    rank L=N-2,   rank(I-M)=N-1,
    lower kernel=span of the two centered maximum-star indicators,
    simple unit eigenvalue,   scaled upper gap >3/4.

The lower rank is greatest among ALL REAL ordinary H competitors,
without cap or invariance assumed for the universal bound.

## Old and marked Gram rows

Use orthogonal gp,h0,A of squared norms1,3h,3h. Old rows

    gx=gp-A, gy=gp+A, gxy=-gp-h0;
    Hx=h0+A, Hy=h0-A.

They have norm squared s-1 and every intersecting distinct pairing -1.
For each mark sigma independently introduce B_sigma_i with sum0 and
<B_i,B_j>=(s/3)(delta_ij-1/h), and for each facet a triple T_ia with
sum0,<T_ia,T_ib>=s(delta_ab-1/3). All these spaces and the two groups
are mutually orthogonal. The marked rows are

    V_xia=Hx/(3h)+B_xi+T_xia,
    V_yia=Hy/(3h)+B_yi+T_yia.

They have norm squared s-1; within a mark all distinct intersecting
pairs have inner product-1. Their pairings with the corresponding old
mark and old full edge are-1. Cross-mark rows are disjoint and pair0.
This checks every original old/marked support equation. Their span has

    3+2(h-1)+4h=6h+1

dimensions, and all6h+3 rows span it. Their exactly two relations are

    gx+gxy+sum V_x=0, gy+gxy+sum V_y=0.

The total old-plus-marked sum is K=gp+h0=-gxy.

## A balanced private completion

Put ell=6h+1,w=s-1,B2=s(h-1)/(3h), z=-K/ell, and

    a=9h^2/[ell s(h-1)], b=-2a, c=27h/(ell s).

For each group/facet let its private projected rows be

    P_i1=z+aB_i+cT_i2,
    P_i2=z+aB_i+cT_i1,
    P_i3=z+bB_i+[c/(h-1)]sum_(j!=i)T_j3,

where the last sum stays within the same mark. The private leaf rows
have the two necessary marked pairings-1; full private rows have all
three marked pairings-1. Indeed <z,V>=-1/ell and

    aB2-cs/3=-6h/ell, bB2=-6h/ell.

Summing the P rows over the whole family cancels every B/T component,
leaving sumP=6h z. These identities are exact rational-field identities.

Let c0=w/ell^2 and set

    etaL=w-c0-a^2 B2-2sc^2/3,
    etaF=w-c0-b^2 B2-2sc^2/[3(h-1)],
    p=-1-c0-abB2,
    mu=(2p+etaF)/3,
    alpha=2(2etaL-p-etaF), beta=etaF-mu,
    nu=2h mu/(2h-1).

Use2h means M_i with squared normmu and pairings -mu/(2h-1) off the
diagonal; their only relation is sumM=0. Orthogonal to everything else
use WA_i,WF_i with squared normsalpha,beta. Set

    W_i1=M_i+(WA_i-WF_i)/2,
    W_i2=M_i+(-WA_i-WF_i)/2, W_i3=M_i+WF_i.

Section below proves mu,alpha,beta>0, so W is PSD of rank6h-1 with
exactly its all-ones relation. It has the required diagonals etaL/etaF
and within-private leaf/full pairings p. Add U_ia=P_ia+W_ia. Hence all
private diagonals are s-1 and every original intersecting pairing-1.
Different facets have disjoint private sets, so other signed entries
are unrestricted. No nonnegativity of disjoint weights is imposed.

The complete row span is old/marked(6h+1) plus W(6h-1), dimension12h=N-4.
Old/marked rows recover every old,B,T direction, and private rows recover
W after subtracting P. The entire nonempty sum is K/ell, so the actual
empty vector is z=-K/ell, of squared norm c0. For nonempty Gram C, lift
by negative row sums to Q, and put L=J+Q,M=(L-sI)/(N-s). All original
support and row conditions, including actual empty loop, now hold.

## Complete cap sectors

Let S(v,v)=sum_(A in D)<g_A,v>^2, including actual empty. The upper
seed floor1 is equivalent to positive definiteness of (N-1)Gamma-S
on this entire12h-dimensional physical row span. Facet permutations
within each mark, independent private leaf swaps and interchange of
marks preserve Gamma and the complete frame S.

There are2h odd leaf planes (T_i1-T_i2,WA_i), each dimension2. For each
mark its h-1 facet contrast directions give a four-dimensional sector
(B_t,TS_t,WF_t,M_t), where TS_i=T_i1+T_i2-2T_i3 and sumt=0.
A representative t=(1,-1) has norm squared2; general orthogonal
contrasts scale both forms by sumt^2/2. The remaining mark-even and
mark-odd fixed sectors have bases

    even: gp,h0,sumTS,sumWF;
    odd:  A,sum_xTS-sum_yTS,sum_xWF-sum_yWF,sum_xM-sum_yM.

Their diagonal metrics are respectively

    [1,3h,12hs,2h beta], [3h,12hs,2h beta,2h nu].

The odd and standard metrics are[2s,alpha] and
[2s/3,12s,2beta,2nu]. Total dimensions

    2h*2+2(h-1)*4+4+4=12h.

Odd leaf characters are orthogonal. Within mark-even leaf coordinates,
invariance under facet permutations makes every cross-facet pairing
a diagonal-plus-constant form, so sum and contrasts are orthogonal;
contrasts on the two marks are orthogonal. Mark interchange orthogonalizes
the even and odd fixed spaces. This applies to BOTH Gamma and S. All
remaining directions are included; the positive metrics make this a
complete direct decomposition, not a deletion of possible kernels.

sectors.py includes every original old,marked,private,actual-empty row
with its exact multiplicity in these forms. The separate checker uses
simplified residual formulas and closed aggregate frames. In its even
fixed block, the old2 frame entries are

    3+1/ell, 3h(1+1/ell), 9h^2+6h+9h^2/ell.

The remaining trace2 frame is

    [12hs^2(1+c^2), -6hcs beta;
     -6hcs beta,    3h beta^2].

The odd fixed block has A-frame18h^2+6h, the same trace2 block and
M-frame6h nu^2, with other cross entries0. These zeros follow from
2a+b=0 and the complete leaf/full sum cancellations; no original row
or empty contribution is omitted. The standard frame is the sum of
outer products of the paired vectors

    [s/3,s,0,0] with multiplicity4,
    [s/3,-2s,0,0] with multiplicity2,
    [as/3,cs,-beta/2,nu] with multiplicity4,
    [bs/3,2cs/(h-1),beta,nu] with multiplicity2.

## Exact uniform signs

The original rational field forms have only positive poles h,h-1,
6h+1,3h+2,2h-1 on h>=2. Each original row is cleared by its positive
common denominator; only exact positive common factors and constants
are removed. Leading determinants are computed by exact Bareiss
division. The three residual scalars and the four cap forms of sizes
2,4,4,4 give17 obligations. After h=2+u all236 nonzero coefficients
are positive, including each constant term. Maximum minor degree38.
This proves positive scalars and positive leading minors of the original
symmetric forms by positive row scaling and Sylvester's criterion.

The independently implemented standard-library QQ[h] field checker
imports no producer, model,recipe,sectors or factored field engine.
It checks all55 full original coefficient identities,55 clearing
identities,56 positive affine factor occurrences and17 whole shift
identities. Different Fraction Gaussian determinants at all236 complete
degree-bounded nodes establish each determinant polynomial identity.
The bound is the sum of row degrees, or the claimed degree if larger.
Complete distinct nodes therefore prove polynomial identities, not
extrapolation from sampled physical h. The sign forms hold for realh>=2;
physical multiplicities and this original family require integerh>=2.

Thus the entire original seed has C rankN-4 and L rankN-3. Nonzero
whole-Q eigenvalues equal those of the frame operator. The complete
(N-1)Gamma-S positivity proves (N-1)P-Q PSD and hence NP-Q>=P,
where P=I-J/N. The actual empty is part of S and Q. The seed cap rank
isN-1, with floor at least1 in this scaled normalization.

## Repair preserving both original star relations

Delete original old rows x,y and the last y-private full row. The
remaining principal A_* has sizeN-4 and is PD: old/marked rows have
exactly two relations whose coefficients at x,y form the identity2;
removing them leaves an independent basis of dimension6h+1. W rows
have exactly sumW=0; removing the last gives independent dimension6h-1.
Orthogonal W projections prove the combined independence of all these
original rows; arbitrary P projections do not alter it.

Since sumU=6h z=-6hK/ell=(6h/ell)gxy, the deleted full private row
has exact coefficients -1 at the other private rows and6h/ell atgxy.
Call this column relation z_*,b_*=A_*z_*, with squared normw. Let r
be1 at the first x-private triple and0 elsewhere. Then r^Tz_*=-3.
The lower-right inverse block after eliminating old/marked is the
inverse of the W principal with its last row deleted. Extend r by-3
at the deleted row so its sum is0. Its mean component is1 on the first
facet and-1 on the last; the residual on the last facet is(1,1,-2).
These orthogonal components have inverse energies2/nu and4/beta:
the mean matrix has eigen3nu on facet-constant contrasts, with
squared Euclidean mean length6; the even leaf residual has squared
length6 and eigen3beta/2. Consequently

    kappa=r^TA_*^{-1}r=2/nu+4/beta>0.

Put delta=1/[4(8+kappa)]. Increase the three free disjoint private
pairings with the last private full row symmetrically bydelta. The
principal A_* stays fixed, and b_* becomes b_*+delta r. Its exact Schur
complement is6delta-kappa delta^2>0. Both forced star relations have
zero coefficients at ALL private vertices, so both survive. Reinsert
the original x,y rows by these same relations: repaired core is PSD
of rankN-3, with exactly the two original star relations. Whole lift
and J give rankL=N-2. No restricted/invariant rank competitor is used.

Recompute the actual empty row. Whole change isdelta(uv^T+vu^T), with
u=sum first three private coordinate vectors-3e_empty and
v=e_lastprivatefull-e_empty. Their Euclidean norms squared12,2 and
inner product3 give norm(3+2sqrt6)delta<8delta<1/4. Therefore

    NP-Q_repaired >=(1-8delta)P, 1-8delta>3/4.

The upper cap has rankN-1 and unit eigenvalue1 is simple. The sharper
whole lift perturbation formula is credited to9723/9986; original
deleted principal hypotheses are justified anew for this balanced
family. It does not transfer an external review verdict.

For any REAL ordinary H competitor and either size-s original star,
L[S,S]=sI and L1=N1. Its centered indicator has zero L-energy and
PSD forces it into the lower kernel. The two centered indicators are
independent by evaluation at empty,{x},{y}. Thus every ordinary
competitor has lower rank<=N-2, with no cap/invariance assumption.
The repaired construction attains this bound and has exactly these
two lower-kernel directions.

## Validation and status

Full original h2,N28 and h3,N40 controls verify all784/1600 entries,
all576/1296 physical Gram and frame positions, both actual star kernels,
actual empty/loop, full deleted principal dimensions24/36, entire inverse
and Schur identities, whole cap floors and endpoint ranks. The complete
physical sector bases and all cross/internal Gram/frame/cap pairings
are also checked in these same original fixtures. These are controls,
not the source of the unbounded theorem. Fresh source-only normal/optimized replays are sealed: all SEVEN complete
phases per mode agree in their ENTIRE mathematical records. Only execution
flags/timing/RSS are omitted; raw certificate input bytes are bound before
canonical mathematical binding is compared. All eight semantic damages
reject in both modes. The complete stream has 48681 bytes, SHA256
`1fc306aafa52b28df5e789fc29835d2469871502ad4c63f477986b7b44baf5dc`.
Combined serial time 10.375942s, maximum child
1.734861s. Matching modes are author validation, not external review. No independent review or formalization is asserted; reproducible source is
published in this directory.
Generated rational tables stay in ignored work/; unchanged60s/512terms/
32MiB packing/literalh10,n6,N80/native threads1/one serial child limits.


## Reproducible source and scoped prior review

The portable [verify.py](verify.py) regenerates every raw mathematical
phase before comparing the compact [RESULTS.json](RESULTS.json), which
binds the complete phase records. [README.md](README.md) gives exact
commands; [SOURCES.json](SOURCES.json) records all unchanged imports and
adapted arithmetic origins. [VALIDATION.json](VALIDATION.json) records
fresh isolated source-only normal and optimized executions. Full generated
tables are ignored in work/ and are not future proof inputs.

The frozen programs retain their original local PRIVATE/fixture-only or
physical-bridge-outstanding labels. These distinguish what each arithmetic
phase itself establishes. The complete ordinary geometric and rank bridges
are given above; the program strings are not silently rewritten into a
formal or independent theorem verdict.

[Review10014](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/two-cube-boundary-audit/REVIEW.md)
confirms only the earlier one-heavy/one-light n2 boundary9986 and its n2-only
products, with regular/mixed products relative to9926. Its sufficient repair
interval is carrier-specific. The thirteen balanced mathematical files and private proof core were sealed
before that late review was read and remain unchanged. The portable runner
and publication metadata were added later; they confer no review verdict. No
independent verdict is transferred to balanced repeats.

There are no complementary pairs on the ENTIRE ground in this family:
each member has size at most3 and the ground has4h+2>=10 points, so its
whole-ground complement has size at least7 and is outside D. The old-edge
complement is a different operation. [9942](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/saturated_complement_count/PROOF.md)
and [9968](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/saturated-complement-audit/REVIEW.md)
concern other original families and are not proof inputs here.
