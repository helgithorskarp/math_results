# Arbitrary unequal private triangle counts: original capped H

Actual author **six-downset-1**, role **researcher**, 2026-10-04.
Complete ordinary author proof and exact symbolic certificate. The proof
is unformalized and independently UNREVIEWED.
Finite controls validate the implementation, not the infinite quantifier.

## Quantified statement and credits

Let n>=3 and integers h>l>=2. On an old n-set X choose distinct x,y.
Attach h triples {x,a_i,b_i} and l triples {y,c_j,d_j}, all private pairs
mutually disjoint and outside X. Let D be the union of their downsets
and2^X, INCLUDING the actual empty set. Put

    q=2^(n-1), d=h-l, m=3(h+l), ell=m+1,
    s=q+3h, N=2q+6(h+l)=2s+6l, P=I-J/N.

There is a rational symmetric original N-by-N matrix M with M1=1,
M[A,B]=0 whenever A intersects B, and

    L=sI+(N-s)M>=0, NI-L>=(25/32)P,
    rank L=rank(I-M)=N-1.

The lower kernel is exactly span(chi_x-(s/N)1), the unit eigenvalue is
simple, and both ranks are greatest possible among real competitors.
M is invariant under heavy/light facet permutations, private leaf swaps,
and old-point permutations fixing x,y. More precisely the seed has a
spread repair line, lower PSD iff0<=delta<=6/kappa_bar, where
0<kappa_bar<49/78. Original lower ranks areN-2 at the endpoints andN-1
inside. EVERY real0<delta<=1/8 attains both greatest ranks and scaled cap
floor1-7delta>=1/8; the rational theorem uses delta1/32. No optimal upper
endpoint, n2, overlapping pairs, general downset H, inertia I or priority
claim is asserted.

Ordinary H/greatest lower rank for this class is already implied by
[one-point closure9361](https://github.com/helgithorskarp/math_results/blob/ca8d2e363536435ad034f08cf3845a6ffd276326/round-two/six-downset-1/one-point-attachments/PROOF.md).
The new all-count assertion is the original cap/gap and greatest upper
rank. The old Gram/whole source utilities are credited to
[balanced10111](https://github.com/helgithorskarp/math_results/blob/2252bcaacf4798c6b13d75b4918792fd7c8bbe9c/round-two/six-downset-1/balanced-triangle-all-cubes/PROOF.md) and
[repair-line10160](https://github.com/helgithorskarp/math_results/blob/95ef0d44f2263cb94a191632fc04dd64f0feaba7/round-two/six-downset-1/balanced-triangle-repair-line/PROOF.md).
The retained-mean/harmonic mechanism is credited to
[consecutive10230](https://github.com/helgithorskarp/math_results/blob/21517cfce36b080a73f3c0ec5ed7969e09a50cf9/round-two/six-downset-1/consecutive-triangle-cap/PROOF.md).
Its [independent review10237](https://github.com/helgithorskarp/math_results/blob/4ff8e4ec4693a852d247ed72d56853a170e173ac/round-two/six-reviewer-5/asymmetric-cube-cap-audit/REVIEW.md) covers counts(h,h-1), not this new domain.
The argument below directly recompletes every retained row.
No deleted cap/margin, ancestor review or peer seed is transported.

Primary target: [Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4).
The [version page](https://arxiv.org/abs/2609.28404), rechecked live on
2026-10-04, still lists23 Septemberv1. Classical Chvatal and the proved
projection-packing result are distinct from proposed spectral H/I.

## 1. The whole old and retained marked space

Put D0=3h and w=s-1. On the 2q-1 nonempty old sets use the credited Gram

    A=(q+D0)I+(q-D0)Pold-J,

where Pold exchanges proper complementary pairs and has full-set row zero.
Denote its vectors by g_A. Put G=sum g_A, gF=g_X,
Hx=-sum_(x in A)g_A, Hy=-sum_(y in A)g_A. Direct old-set counts give

    G^2=gF^2=w, G.gF=D0-q+1,
    Hx^2=Hy^2=qD0, Hx.Hy=0,
    G.Hx=G.Hy=gF.Hx=gF.Hy=-D0.

The orthogonal E=G-gF, U=G+gF, R=Hx+Hy+G+gF, Aodd=Hx-Hy have norms
4(q-1),4D0,2D0(q-2),2qD0. There are also q-2 proper-pair-sum contrasts
and q-3 pair-difference directions orthogonal to R,Aodd; their frame
eigenvalues are2q and2D0. These exhaust dimension2q-1.
For completeness, pair sums p_i and differences d_i for q-1 complementary
pairs have p_i.p_j=4q delta_ij-4, d_i.d_j=4D0 delta_ij,
p_i.d_j=d_i.gF=0 and p_i.gF=-2. The R and Aodd difference coefficient
vectors have disjoint supports and squared lengths(q-2)/2,q/2. These
identities prove positive old metrics and the entire decomposition.

For each mark take h-facet B vectors with sum B_i=0,
B_i.B_j=(s/3)(delta_ij-1/h), and orthogonal facet triples satisfying
sum_a T_ia=0 and T_ia.T_ib=s(delta_ab-1/3). The two B spaces, all facet
T spaces and the old space are mutually orthogonal. Retain h heavy and
l light facets, with marked rows

    V_xia=Hx/D0+B_xi+T_xia, V_yja=Hy/D0+B_yj+T_yja.

They have norm w, and distinct rows with the same mark pair to-1.
Required old/marked pairings equal-1 because
g_A.Hsigma=D0(1-2[sigma in A]). Let Bbar=(sum_retained B_yj)/l. Then

    Bbar^2=sd/(3hl), sum_retained V_y=(l/h)Hy+3l Bbar.

Set Btilde_xi=B_xi and Btilde_yj=B_yj-Bbar. Each group of size k=h,l
has sum-zero contrasts and Gram(s/3)(delta_ij-1/k). Bbar is orthogonal
to both contrast and all T spaces, and is retained explicitly.

Facet averages recover every retained B, and within-facet differences
recover every T. The l retained original light B vectors are independent,
since l<h. Thus old/marked rows span

    (2q-1)+(h-1)+(l-1)+1+2(h+l)=2q+m-2

dimensions, with precisely the heavy-star relation. Unused parent ambient
directions are excluded from the row span; their ambient rank is not a
cap or completeness claim.

## 2. Recomplete the actual empty and every private row

The full retained old/marked sum and the new common vector are

    K=G+Hx+(l/h)Hy+3l Bbar, z=-K/ell,
    K^2=q ell+9ld-3h-6l-1, c0=z^2=K^2/ell^2,
    z.V_xia=-(q-1)/ell, z.V_yja=-(q+3d-1)/ell.

These follow from the entire old Gram and new Bbar norm. At q4 its numerator is15l+9(l+1)d+3>0; it increases in q, so c0>0. The vector z is orthogonal to every recentered Btilde and every
retained T direction.

For group g with k=h or l and v_g the displayed marked-common pairing,
define B2=s(k-1)/(3k), a=(1+v_g)/(2B2), b=-2a, c=9(1+v_g)/(2s), and

    P_i1=z+a Btilde_i+c T_i2,
    P_i2=z+a Btilde_i+c T_i1,
    P_i3=z+b Btilde_i+[c/(k-1)]sum_(j!=i)T_j3.

Other-facet sums stay within the same group. Each private leaf must pair
to-1 with the marked row on that leaf and the marked full row; this is
v_g+aB2-cs/3=-1. A private full row pairs to all three marked rows by
v_g+bB2=-1. These are every mandatory private/marked intersection.
The identities2a+b=0 and sum_a T_ia=0 give sum P=mz.

Define separately in both groups

    etaL=w-c0-a^2 B2-2sc^2/3,
    etaF=w-c0-b^2 B2-2sc^2/[3(k-1)], p=-1-c0-abB2,
    mu=(2p+etaF)/3, alpha=2(2etaL-p-etaF), beta=etaF-mu.

Writing r=1+v_g, separate expanded identities are

    mu=(s-3)/3-c0-9r^2/[2s(k-1)],
    alpha=2s-27(2k-3)r^2/[s(k-1)],
    beta=2s/3-3(k+3)r^2/[s(k-1)].

All six scalars are positive for INTEGER h>l>=2, q>=4 by the analytic estimates below. Put

    tau=mu_x mu_y/(h mu_x+l mu_y),
    off_x=(l tau-mu_x)/(h-1), off_y=(h tau-mu_y)/(l-1),
    nu_x=(h mu_x-l tau)/(h-1), nu_y=(l mu_y-h tau)/(l-1).

Take facet means M_i with group diagonals mu_g, within-group
off-diagonals off_g and cross-group entry-tau. This Gram has zero row
sums. It has group-contrast eigenvalues nu_x,nu_y, the positive
group-mean eigenvalue(h+l)tau, and the sole ones kernel.
Positivity also follows directly from tau<mu_x/l and tau<mu_y/h.
Add orthogonal internal vectors WA_i,WF_i of squared norms alpha_g,beta_g,
and set

    W_i1=M_i+(WA_i-WF_i)/2,
    W_i2=M_i+(-WA_i-WF_i)/2, W_i3=M_i+WF_i,
    U_ia=P_ia+W_ia.

The identities mu+alpha/4+beta/4=etaL, mu+beta=etaF and mu-beta/2=p
prove each private norm w and leaf/full-private pairing-1. Different
facets have disjoint private sets; old/private sets are disjoint. Thus
every intersecting nonempty pair, including diagonals, has the required
Gram value. The residual W Gram has rank m-1 and sole relation sum W=0.
The actual empty vector is z, since K+mz=-z.

Every Gram entry is rational at physical integer h,q. A Euclidean
realization is a proof device, not a requirement of rational coordinates.
The entire nonempty core C has rank(2q+m-2)+(m-1)=N-3: each P is in the
retained old/marked span, so private rows recover the full residual W
space. Its two independent kernel vectors are chi_x and

    r_i=m/(m+1) on old/marked rows, r_i=1 on private rows.

The dimension count proves these are all kernels. Complete C with the
negative row-sum lift Q: Q00=1'C1, Q0A=-(C1)_A, Q_AB=C_AB for nonempty
sets. Thus Q1=0, rank Q=N-3, and Q is the complete physical Gram including
z. The seed L0=J+Q, M0=(L0-sI)/(N-s) is symmetric and stochastic with
the required original zero support; rank L0=N-2.

## 3. A cap on every original direction

On the entire physical row span let Gamma be the metric and
S(v,v)=sum_(B in D)(row_B.v)^2, with the actual empty included. It is
enough to prove(N-1)Gamma-S positive definite. Put
TS_i=T_i1+T_i2-2T_i3.

Each facet leaf-odd block has basis(T_i1-T_i2,WA_i) and metric
diag(2s,alpha_g). For every sum-zero facet profile t in a group of size k,
the standard block has basis(Btilde_t,TS_t,WF_t,M_t), metric
diag(2s/3,12s,2beta_g,2nu_g) times sum t_i^2/2. The orthogonal profiles
(1,...,1,-j,0,...,0), j=1,...,k-1, exhaust the standard space.

The aggregate has TEN independent directions

    E,U,R,Aodd,Bbar,sum_x TS,sum_y TS,sum_x WF,sum_y WF,sum_x M,

with diagonal metric

    4(q-1),4D0,2D0(q-2),2qD0,sd/(3hl),
    6hs,6ls,h beta_x,l beta_y,hl tau.

Retain also both untouched old spaces, of dimensions q-2,q-3 and frame
eigenvalues2q,2D0. They pair zero with every new row, whose old projection
is in span(G,Hx,Hy). Leaf swaps separate odd blocks; facet permutations
give diagonal-plus-constant forms, separating sum-zero profiles from
aggregate directions. Direct row sums give the same orthogonality for
both Gamma and S, including all cross-group entries. Their dimensions
exhaust

    2(h+l)+4[(h-1)+(l-1)]+10+(q-2)+(q-3)=N-3.

For a complete, explicit aggregate frame calculation, proper old rows have
first-four coordinates(1/[2(q-1)],0,(1-ix-iy)/(q-2),(iy-ix)/q), with counts
q/2-1,q/2,q/2,q/2-1 for(00),(10),(01),(11). The full old row is
(-1/2,1/2,0,...,0). Common z has coordinates

    (-1/(2ell),l/(2h ell),-(h+l)/(2h ell),-d/(2h ell),-3l/ell,0,...,0).

Marked group-g rows have first-five coordinates
(0,-1/(2D0),1/(2D0),+/-1/(2D0),0 for x or1 for y), and TS_g-sum
coordinate1/(6k) for leaves or-1/(3k) for full rows. Private rows have
the common first-five coordinates, TS_g-sum coordinate c_g/(6k) or
-c_g/(3k), WF_g-sum coordinate-1/(2k) or1/k, and mean coordinate1/h for
x or-1/l for y. There are2k leaves and k full rows of each type. Empty
has the common coordinates.

In the first-five metric above the old frame has nonzero entries
S00=4(q^2-1), S01=S10=-4D0(q-1), S11=4D0^2,
S22=4D0^2(q-2), S33=4D0^2 q. Add

    3h jx jx' +3l jy jy' + zimage zimage'/ell,
    jx=(0,-2,q-2,q,0), jy=(0,-2,q-2,-q,sd/(3hl)),
    zimage=(-2(q-1),6l,-3(q-2)(h+l),-3qd,-sd/h).

Each TS/WF trace has metric diag(6ks,k beta) and frame

    [[6k s^2(1+c^2),-3k s c beta],
     [-3k s c beta,(3/2)k beta^2]].

The last mean is a separate exact frame mode3(h+l)tau. All cross terms
to it and the traces cancel by the complete row counts. Its uniform cap
can also be seen from

    3(h+l)tau <3(h+l)mu_y/h <(h+l)(s-3)/h <2s-6 <N-1.

This mode alone is not a cap certificate. Both untouched margins are6(h+l)-1 and2q+6l-1. The complete leaf-odd and standard weighted row forms are in sectors_harmonic.py. The analytic expansion below pays their whole normalized frames; check_five.py independently binds all five-direction entries.

## 4. Analytic scalars and non-five-dimensional cap blocks

Write r_x=(ell-q+1)/ell and r_y=(6l+2-q)/ell. Each r_g/s decreases
in q. At q4 its positive value is less than1/(3h+4); its limiting
negative value is-1/ell, also of smaller magnitude since ell>=3h+7.
Thus |r_g|/s<1/(3h+4). Also

    c0=(q ell+9ld-3h-6l-1)/ell^2 >0,
    c0<q/[3(h+l)]+1/8,

because(h+l)^2-8l(h-l)=(h-3l)^2>=0. For k=h or l, the generic
expanded alpha,beta,mu formulas therefore give

    s<alpha<=2s, s/2<beta<=2s/3, s/5<mu<s/3.

Details: (2k-3)/(k-1)<2 and(k+3)/(k-1)<=5 imply
alpha>s[2-54/169]>s and beta>s[2/3-15/169]>s/2.
For h>=4,

    mu>s[1/3-1/(3(h+l))-9/(2(3h+4)^2)]
          +h/(h+l)-9/8
       >(1199/4608)s-5/8,
    mu-s/5>487/1440,

using s>=16. For the only remaining integer case h3,l2,
c0=q/16-1/64 and s=q+9. Hence

    mu>s(13/48-9/338)-7/16,
    mu-s/5>1391/10140,

using s>=13. All inequalities are exact rational statements, not
floating-point evidence.

Harmonic tau is positive and both nu are positive. The upper bounds
mu<s/3 and lower bounds mu>s/5 give

    nu_x<s/2, nu_y<=(29/57)s.

Indeed the light contrast is bounded by

    nu_y <=(s/3)[l-3h/(3h+5l)]/(l-1)
          <=(s/3)(8l^2-3)/[(8l+3)(l-1)]
          <=(29/57)s.

The middle ratio equals1+5l/[(8l+3)(l-1)] and decreases for l>=2;
use h>=l+1. The heavy bound follows from h/(h-1)<=3/2.

### Complete normalized frame bounds

The projections have |a|<=3/13, |c|<=9/26,
|(k-3)/(k-1)|<=1 and k/(k-1)<=2. In the metric-normalized SYMMETRIC
standard frame, diagonals are

    s(1+2a^2),
    s[1+c^2/3+2c^2/(3(k-1)^2)],
    3beta/2, 3nu.

The only off-diagonal magnitudes are

    s|ac z|sqrt2/3, |a|sqrt(3s beta),
    |cz|sqrt(6s beta)/6,
    |c|k sqrt(6s nu)/[3(k-1)], z=(k-3)/(k-1).

Use sqrt2<3/2 and sqrt(58/19)<7/4. Its four absolute row sums divided
by s are at most

    1009/676, 1135/676, 19/13, 1907/988,

all strictly below2. Gershgorin therefore caps the ENTIRE standard
block by2s, with every group multiplicity retained. The leaf-odd and
TS/WF trace blocks have largest row sum at most991s/676<2s.
The aggregate mean mode satisfies3(h+l)tau<2s-6; both untouched old
eigenvalues2q,6h are below2s. Since N-1=2s+6l-1>2s, all these blocks
have a strictly positive(N-1)-cap. These are direct matrix bounds,
not truncation of a coefficient certificate.

## 5. The five-block, low-q region

Put D0=3h, Bbar^2=sd/(3hl), Kold=G+Hx+(l/h)Hy and
a0=(3h+6l+1)/ell=1+3l/ell>1. Work in the old four-plane plus Bbar.
The old frame is bounded by2D0 times the old metric when q<=D0.
This follows either from the full old Gram B-J<=B<=2D0 I or directly
from the E/U normalized two-plane and the R/Aodd eigenvalues2D0.
The two marked OLD components are orthogonal and their frame norm is
at most q. The old common frame has norm

    Kold^2/ell=q[1-3ld/(h ell)]-a0<q-a0.

Thus the old diagonal block is bounded by2s-a0. Its cap margin is
at least6l-1+a0>6l. The Bbar frame diagonal equals

    (sd/h)(1+3l/ell)<s,

so its cap margin exceeds s. The cross vector is
3l|Bbar|(Hy/D0+Kold/ell), whose squared norm is strictly less than

    lsdq(2h+3l)/[h^2(h+l)]<6ls,

using q<=3h and
2h(h+l)-(h-l)(2h+3l)=hl+3l^2>0. The two-block Schur bound proves
the whole five-dimensional cap positive definite in this region.
It includes the retained light mean and actual common/empty contribution;
it is not a projection deleting Bbar.

The complete aggregate coordinates in Section3 bind this estimate to the original rows. The remaining high-q region is proved next.


### The entire high-q five-block

For q>=3h set l=2+v,d=1+u,h=l+d,q=3h+w, all u,v,w>=0.
FIVE-HIGHQ-CERTIFICATE.json is39086 bytes and losslessly encodes ALL25
normalized entries of(N-1)Gamma5-S5,5 pivots and30 ORDERED local Schur
updates. Numerators have positive constants and nonnegative coefficients;
all denominator factors do also. Pivot degrees are2,4,5,6,7, with
9,31,51,74,105 coefficients,270 in total. Row normalization divides by
positive metric entries. Positive Gaussian pivots give positive leading
minors of the original SYMMETRIC cap. Sylvester therefore proves PD on
the entire auxiliary high-q region, not sampled powers of two.

check_five.py imports ONLY the standard library, no producer, field engine,
sector or recipe. It separately expands the physical first-five forms,
clearing metric/image denominators with t=3hl; binds all25 entries; checks
every pivot/working-matrix link and every one of30 Schur identities.
The following lemma justifies its exact entire coefficient check.

If a polynomial has coordinate degree boundsD_j and coefficient l1
boundC, choose integerB>2C and substitute
(B,B^(D0+1),B^((D0+1)(D1+1))). Distinct monomials have distinct base-B
slots. If the resulting integer is zero, successive reduction moduloB
forces every coefficient to be zero, since its absolute value is<B/2.
Recursive degrees and l1 norms are bounded by coordinate maxima/norm
sums for addition and degree sums/norm products for multiplication.
These exact bounds dominate every coefficient without cancellation.
This is a COMPLETE coefficient identity, not empirical one-point testing,
modular guessing, probabilistic hashing or interpolation reconstruction.

The25 original cleared identities have coordinate degrees(8,10,2),
encoding1597 bytes. The30 local identities have degrees(27,29,18),
encoding289275 bytes. Full numerator signs and denominator factors are
checked from every coefficient; the zero-identity encoding alone is NOT
a positivity test. All input polynomials are within512 terms, all
encodings within32MiB. The original decomposition and these two q
regions give Q<=(N-1)P and NI-L0>=P, including every mean/empty direction.

## 6. Group-invariant spread repair and every original inverse direction

In the nonempty core let u indicate all3h heavy PRIVATE rows and v all
l light PRIVATE FULL rows. Put a=u/h,b=v/l,p=a-3b,c=(a+3b)/6 and

    C(delta)=C+delta(ab'+ba')
            =C-(delta/6)pp'+6delta cc'.

All changed pairs are FREE, between disjoint private sets, and avoid x;
diagonals are unchanged. Also p.chi_x=c.chi_x=0,p.rho=0,c.rho=1.
The residual physical dual is

    Z=(sum_x M)/(hl tau)-2(sum_y WF)/(l beta_y).

Its scores are1/h on EVERY heavy private row,-3/l on EVERY light private
FULL row, and0 on ALL other rows INCLUDING actual empty. The heavy mean
sum pairs to l tau with each heavy mean and-h tau with each light mean.
The light WF sum pairs to-beta_y/2 with leaves and beta_y with full
rows, canceling the light leaf score. Orthogonal components give

    kappa_bar=Z^2=1/(hl tau)+4/(l beta_y)
             =1/(h mu_x)+1/(l mu_y)+4/(l beta_y)
             <(5/h+13/l)/s <=49/78.

The last bound uses mu>s/5,beta>s/2,h>=3,l>=2,s>=13. The scores pay
EVERY original row. Completeness of the physical row span implies that
this unique dual norm is p'C^dagger p. Equivalently, delete singleton x
and one light private full row; the remaining principal is PD of
sizeN-3. Its inverse solution, zero-extended, satisfies every original
Cz=p equation and p'z=kappa_bar. The literal controls independently
verify all of these inverse and dual equations.

In chi_x-perp, split ranC from rho0=rho-proj_chi_x rho. Then p is in
ranC and c.rho0=1. For delta>0 the kernel block of6delta cc' is positive;
its Schur complement cancels exactly the ranC part of the same outer
product. The remaining range form is C|ranC-(delta/6)pp', PSD iff
delta<=6/kappa_bar by rank-one congruence. For delta<0 its rho0
quadratic form is negative; delta0 is the PSD seed. Thus the WHOLE
lower line is PSD exactly for0<=delta<=6/kappa_bar, with core ranksN-3
at both endpoints andN-2 inside. The full lift and orthogonal J term
give original lower ranksN-2 at endpoints,N-1 inside. No sparse-line
endpoint is assumed for this different spread line.

For the ENTIRE original lift, extend a with empty coordinate-3 and b
with empty coordinate-1. Both sums are zero,a.b=3,
||a||^2=9+3/h,||b||^2=1+1/l. The two nonzero eigenvalues of the
perturbation are delta[3+/-sqrt((9+3/h)(1+1/l))], so for delta>0 its
norm is at mostdelta(3+sqrt15)<7delta. Consequently

    NI-L(delta)>=(1-7delta)P.

The boundkappa_bar<49/78 puts every0<delta<=1/8 inside the lower
interior, with positive cap floor at least1/8. Delta1/32 is rational
and gives25/32>3/4. The actual empty squared norm changes by6delta;
it is never discarded or conditioned away.

The seed is invariant under the stated groups: old pairings depend
only on equality/complement, and marked/private pairings depend only
on group and facet relations. u,v are group invariant, so the spread
repair preserves the symmetry. It equals the uniform average of the
3-pair repairs overh*l choices, but its OWN dual/cap proof above pays
that averaging without transporting a sparse margin or endpoint.

Finally x is uniquely largest: its star, the y star, other old and
private point stars have sizess,q+3l,q,4. For ANY real ordinary H
competitor put f=chi_x-(s/N)1. Intersecting support gives
chi_x'Mchi_x=0; stochasticity gives f'Mf=-s^2/N and
f'f=s(N-s)/N. Hence f'Lf=0 and PSD forces Lf=0. The universal lower
rank ceilingN-1 is attained. The constant cap kernel gives the upper
ceilingN-1; the positive floor makes the unit eigenvalue simple.

## Verification, source and trust status

The original n3/h5/l2 control N50/s19 is outside both prior fixed-gap
profiles; it pays2500 original entries,4418 metric/frame positions,
all cross blocks, actual empty, every dual score and inverse direction.
A separate n5/h3/l2 physical control N62/s25 pays the high-q region,
integer h3 boundary and6962 metric/frame positions. The actual row
span ranks are47 and59; unused parent ambient directions are excluded.
Two full original spread controls at delta1/32,1/8 each pay2500 M
positions and2500 ENTIRE perturbation positions, attain both ranks49,
and also check the exact original lower endpoint rank48. Group-generator
comparisons cover every original matrix entry. Normal/optimized checks
and mathematical defect controls are recorded in EXPECTED.json and README.md.

The source95 balanced parent utility is reused verbatim; its n3/h5
N68 baseline is reconstructed exactly, SHA256
01106b2a14b4e58246a4fba879a4b8c63f0dd499f4936e2a2de9146710d65b51.
Reproducibility is validation, not novelty. Every actual parent stays
at most68. Parent N80 is checked BEFORE construction.

Guards remain child60s,512 input polynomial terms,32MiB packing/whole
identity encoding,native1/serial1/1CPU2GiB,literal n6/h10/N80. Auxiliary
variables and identities are not enumeration of larger carriers. No
floating output, solver status, timeout, memory kill, interruption or
incomplete enumeration is a premise. The real/linear/spectral/encoding
bridges remain unformalized and the whole result independently UNREVIEWED.
The public source-only replay is described in README.md. Hashes bind whole
regenerated outputs after exact checking; they do not replace the ordinary
argument. Source publication is not independent review or formalization.
