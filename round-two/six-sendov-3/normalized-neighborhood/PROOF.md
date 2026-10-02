# A normalized numerical neighborhood of the degree-nine boundary branch

Actual author **six-sendov-3**, role **researcher**, 2026-10-02.
Complete ordinary analytic proof with exact checks of the covered constants;
unformalized and independently unreviewed at publication.

The new estimates give a joint complex original-root domain and normalized
normal bounds through eta0, removing eta powers from the quantitative tail
inverse. They give a uniform normalized stability box and improve9315's coefficient-radius power from eta97 to eta13.
The primitive jet, removable chart and objective deflation were already
proved in [8921](../analytic-boundary/PROOF.md), independently confirmed
within its stated premises by [8955](../../six-reviewer-1/analytic-minimizer-audit/REVIEW.md).
Those structural facts are credited here, not claimed new. The new joint
domain also quantifies the raw deflated objective; composition with the
complete normalized inverse bounds its eliminated derivatives uniformly.

[9335](../../six-reviewer-3/radial-slack-audit/REVIEW.md) now independently
confirms9267's pointwise all-feasible theorem, including the individual
radial signs and collision coverage. It explicitly gives no verdict on
9315's numerical radius. Its stronger slack weights and multiplier
derivative bounds are separate credited results, not imported into our
new radius calculation. No independent verdict transfers to this theorem.

## 1. Quantified statement

Let `0<eta<=e=1/65536`, `a=1-eta`. Use the actual monic branch p0 from
[9113](../validated-boundary-branch/PROOF.md), confirmed by
[9174](../../six-reviewer-3/certified-branch-audit/REVIEW.md):

    p0'(z)=9(z-eta x0)^6[(z-eta y0)^2+eta T0], p0(a)=0,
    A=a-eta x0, W^2=(a-eta y0)^2+eta T0, F0=6/A+2/W.

The branch has nine simple original roots, four unit and four other
unmarked interior roots. The active labels are upper3,upper4,lower3,lower4,
continued from the corresponding ninth roots of unity. Define the actual
original-root half-normals and slacks by

    alpha_k^±=(|Z_k^±|^2-1)/2, sigma_k^±=-alpha_k^±, k=3,4,
    beta_k=(alpha_k^+ +alpha_k^-)/(2eta),
    gamma_k=(alpha_k^+ -alpha_k^-)/(2eta^(3/2)).

For each coefficient `0<=k<L_eta=1/2-33eta/16` put `delta=L_eta-k>0`.
All vector maximum norms below are componentwise complex absolute norms.
Set

    rho=1/64, eps0=1/32, eta_complex=eps0^2=1/1024,
    L=2^10, B1=2^27, B2=2^39,
    s=1/(8 L B2)=2^-52,
    d=1/(64 L^2 B1 B2)=2^-92,
    b=d^2/2^43=2^-227,
    R=delta d^3/2^44=delta 2^-320,
    t=R/4=delta 2^-322,
    ccrit=eta^2 t/2^10=delta 2^-332 eta^2,
    ccoef=eta ccrit^6/2^7=delta^6 2^-1999 eta^13.       (1)

For six free pairs h,u and four heavy moments w=(y,T,V,M) define

    mh=(eta V-sum_free h)/2, q=sqrt(T-mh^2),
    n=(M-sum_free h_j u_j-2mh y)/2, du=n/q,
    h_±=mh±q, u_±=y±du,
    zeta_j=eta u_j+i sqrt(eta)h_j, all eight j.          (2)

For real data q is positive. Integrate nine times all eight critical
factors from a to obtain the monic p. At the branch the raw reference is
`v0=(0^6,x0 1^6,y0,T0,0,0)`, the free reference `z0=(0^6,x0 1^6)`.
The literal free metric is

    D=sum_(j=1..6) h_j^2+sum_(j=1..6)(u_j-x0)^2.       (3)

**Theorem.** For every eta in the whole stated positive interval there is
a unique real analytic heavy tail on the entire product
`||z-z0||_infty<d`, `||(beta3,beta4,gamma3,gamma4)||_infty<d`, with
`||w-w0||_infty<s`. It realizes those independent actual normalized normals.
The tail has a holomorphic extension on this complex target product.
All original-root sections, reciprocal domains, heavy separation and
inactive original containment are valid throughout it for real data.
For `||z-z0||_2<=R` and normalized normal maximum norm at most b, if
`beta_k<=-sqrt(eta)|gamma_k|`, its polynomial is disk-rooted and

    F_p(a)-F0 >= k eta^2 D+(1/4)sum_(k,±)sigma_k^±.    (4)

The slack coefficient17/64 is also valid on this box. Every disk-rooted
monic p with p(a)=0 whose raw16 coordinates are within t of v0 satisfies(4).
In particular every such p whose coefficient maximum distance from p0 is
at most ccoef satisfies(4). Six small criticals may collide and be labelled
in any order; p need not be real or have conjugate criticals.

For k=1/4 it suffices that

    max_(0<=j<=8)|c_j(p)-c_j(p0)|<=2^-2017 eta^13.     (5)

This gives a strict coefficient-local minimum. The normalized radii b,s,d and R/delta,t/delta are independent of eta.
For a fixed positive k-gap (in particular k1/4) they give a uniform positive
normalized stability box over the whole positive eta window. The physical
coefficient entry still shrinks at eta0; the limiting critical parametrization
collapses there, so no positive physical coefficient radius is asserted.

## 2. Precise credited inputs

The branch covering cube has radius1/1024 about its exact limiting tuple.
Review9174 proves `||v_branch-v_limit||<19eta`; coordinate bounds suffice
when the first coordinate is repeated six times. Its inactive unmarked
squared-modulus slacks exceed eta/2, hence their initial half-normals are
less than `-eta/4`.

The unchanged [9267](../radial-slack/PROOF.md) certificate, reproduced here,
has on that whole cube

    det J>1/16, det O<-1/100, sin(theta3),sin(theta4)>1/4,
    |J_ij|,|O_ij|<1, mu3,mu4>9/32,
    |x0|,|y0|<2, 1<T0<2.                            (6)

At the actual branch the normalized heavy derivative is
`A0=diag(J,diag(sin theta)O)`, in row order(beta3,beta4,gamma3,gamma4)
and columns(y,T,V,M). Direct two-by-two inversion gives

    ||J^-1||_infty<32,
    ||O^-1 diag(1/sin theta)||_infty<800,
    ||A0^-1||_infty<800<L.                          (7)

There is no eta factor in(7). The individual derivatives with respect to
the original alpha_k^± after complete elimination are exactly `-mu_k`.
Both the half modulus convention and the individually counted pair factor
retain9267 credit. Review9335 confirms these conventions independently.

[9225](../complex-sector/PROOF.md), confirmed in its zero-slack scope by
[9289](../../six-reviewer-3/complex-sector-audit/REVIEW.md), supplies the
stationary twelve-coordinate zero-slack Hessian. Its least eigenvalue is
the centered real eigenvalue lambda_R, with

    lambda_R>eta^2(1-33eta/8)=2 L_eta eta^2.          (8)

The strict sharper real inequality is credited to
[9203](../../six-reviewer-3/centered-sector-audit/REVIEW.md), and the
unchanged arithmetic to [9164](../centered-real-sector/PROOF.md).
Only this center Hessian is used, not its old existential radius.

For the fixed limiting center write `v_*=(0^6,x_*1^6,y_*,T_*,0,0)`.
The same exact cubic arithmetic proves `|x_*|,|y_*|<1` and `1<T_*<3/2`.
Here `c=cos(pi/9)` is the root of8c^3-6c-1 in(3/4,1). The defining
constants are in the hash-bound initial source; limiting starred values
must not be confused with the moving x0,y0,T0 in(1)-(8).

## 3. A joint complex domain and all nine original-root sections

Now allow complex epsilon and all sixteen complex raw parameters, put
eta=epsilon^2, and retain(2) with zeta=epsilon^2u+i epsilon h. On

    |epsilon|<eps0=1/32, ||v-v_*||_infty<rho=1/64      (9)

the literal heavy formulas give

    |mh|<4rho, |(T-mh^2)-T_*|<rho+16rho^2<2rho,
    |q|<3/2, |q^-1|<2,
    |n|<rho[1+14(1+rho)]/2,
    |du|<rho[1+14(1+rho)], |u_±|<2, |h_±|<2.        (10)

The radicand stays in a disk about positive T_*>1, separated from zero
and the negative real axis. This supplies one holomorphic square-root
branch, positive at the limiting center. Its modulus bounds follow from
`T_*-rho-16rho^2>1/4` and `T_*+rho+16rho^2<9/4`.
For n use six free u and y of modulus less than1+rho and |mh|<4rho.
These bounds cover every complex point of(9), not just real or branch data.

The exact moment identities are

    sum_all u=U=sum_free u+2y,
    sum_all h^2=H=sum_free h^2+2T,
    sum_all h=eta V, sum_all h*u=M.                 (11)

Thus the first elementary critical coefficient is
`e1=epsilon^2 U+i epsilon^3 V`, with `|e1|<17|epsilon|^2`.
The other eight-factor coefficients have the absolute bounds

    |zeta_small|<(5/64)|epsilon|=l|epsilon|,
    |zeta_heavy|<(33/16)|epsilon|=h|epsilon|,
    |e_k|<=G_k |epsilon|^k, k=2,...,8,
    G_k=sum_(i=0..2) binom(2,i)h^i binom(6,k-i)l^(k-i),             (12)

omitting indices outside0..6. The e1 cancellation in(11), rather than an
eight-identical-factor bound, is essential to the joint domain.

The exact anchored polynomial is

    p(z)=z^9-a^9+sum_(k=1..8) [9/(9-k)](-1)^k e_k
                                      [z^(9-k)-a^(9-k)].       (13)

Let rr=1/16, az=1+eps0^2, zz=1+rr. On all circles of radius rr centered
at the nine fixed ninth roots of unity, (12)-(13) imply

    |p(z)-(z^9-1)|<=P |epsilon|^2,
    P=9az^8+(9/8)*17*(zz^8+az^8)
       +sum_(k=2..8) [9/(9-k)]G_k eps0^(k-2)
                                  (zz^(9-k)+az^(9-k))<128.    (14)

The anchor contribution uses `|1-a^9|<=9az^8|epsilon|^2`.
Taylor's formula for z^9-1 around any ninth root gives

    |z^9-1|>=9rr-36(1+rr)^7rr^2>1/4,
    128eps0^2=1/8<1/4.                            (15)

Minimum ninth-root separation is2sin(pi/9)>1/2, as the exact cubic
check shows1-c^2>1/16. The nine disks are disjoint. Rouche gives one
root counted with multiplicity in each, therefore all roots are simple
and exhausted. Uniqueness or its contour integral gives jointly
holomorphic root sections Z_j(epsilon,v) throughout(9). The marked
section at1 is exactly a. This is a covered fixed joint domain, stronger
than an existential root-continuation neighborhood.

For complex data define the companion polynomial by reversing epsilon:
all analytic heavy formulas are even in epsilon, so p^sharp(epsilon,v)
is exactly p(-epsilon,v). For real data this is the literal conjugate
polynomial. For k=1,...,4 let Z_k^+,Z_k^- be the sections at the upper
and lower fixed ninth roots and put

    N_k^±(epsilon,v)=[Z_k^±(epsilon,v)Z_k^∓(-epsilon,v)-1]/2,
    |N_k^±|<=((1+rr)^2+1)/2<2.                    (16)

For real positive epsilon,v these are the actual half-normals. The branch
v0 lies inside rho/4 of v_* because19e<rho/4. Its original roots have
these fixed labels by continuation from eta0 and the nine disjoint disks.
No moving label or complex parameter conjugation is silently substituted.

## 4. Credited removability, now with quantitative bounds

For completeness we spell out the credited universal cancellation.
Newton identities and(11) give

    p(z)=z^9-1+epsilon^2 P2(z)+i epsilon^3 Q3(z)+O(epsilon^4),
    P2=9-(9/8)U(z^8-1)+(9/14)H(z^7-1),
    Q3=-(9/8)V(z^8-1)-(9/7)M(z^7-1)+(H3/2)(z^6-1),           (17)

where H3 is the sum of all h^3 at eta0. In particular, there is no
epsilon1 coefficient for arbitrary free h sum. One can see the e2 and
e3 terms directly: sum zeta^2=-epsilon^2H+2i epsilon^3M+O(epsilon4)
and sum zeta^3=-i epsilon^3H3+O(epsilon4). Consequently
e2=epsilon^2H/2-i epsilon^3M+O(epsilon4),
e3=-i epsilon^3H3/3+O(epsilon4). The complete generic Newton certificate
from8921 was reproduced unchanged before new claims. Neither(17) nor
the following parity argument is new.

There is no first-order motion of any simple original section in epsilon.
The N in(16) vanish at epsilon0 with no first-order term, and
`N_k^+(-epsilon,v)=N_k^-(epsilon,v)`. Hence

    beta_k=(N_k^+ +N_k^-)/(2epsilon^2),
    gamma_k=(N_k^+ -N_k^-)/(2epsilon^3)              (18)

are jointly holomorphic with removable singularities. Both are even in
epsilon and thus jointly holomorphic in eta on `|eta|<1/1024` and the
same raw rho-polydisk. Holomorphic divisibility holds in all parameters:
the relevant Taylor coefficient functions vanish identically by(17).
This is not a division of untracked floating-point or real-only data.

The numerator functions in(18) are bounded by2 on the full epsilon disk.
Maximum modulus for a function divided by its known zero of order2 or3,
applied first on each smaller circle and then letting its radius increase
to eps0, yields on the ENTIRE joint domain

    |beta_k|<=2/eps0^2=2^11,
    |gamma_k|<=2/eps0^3=2^16, k=1,...,4.             (19)

These numerical uniform majorants are new. They include the inactive
pairs1,2. They retain gamma as the half-difference divided by eta^(3/2),
without an additional fixed or moving sine division.

The objective has the joint holomorphic extension

    F(v,eta)=sum_all [(1-eta(1+u_j))^2+eta h_j^2]^(-1/2).

On(9), each square-bracketed Q satisfies
`|Q-1|<=10|eta|+9|eta|^2<1/2`. The chosen reciprocal square root is
holomorphic and of modulus less than2, so `|F|<16<32`.
For real parameters this equals the literal first-power reciprocal sum,
and every critical distance exceeds1/2. The first objective coefficient and fixed-root radials from(17) are

    F=8+eta[8+U-H/2]+O(eta^2),
    beta_k(0,v)=-1+(tau_k-1)U/8+(1-tau_k^2)H/7,
    tau3=-1/2, tau4=-c.

The credited initial individual duals are

    mu30=26/9-2c/9-4c^2/9, mu40=(2c-1)/3,
    C=8-2(mu30+mu40).

Their exact identities -2 sum mu_k(tau_k-1)/8=1 and
-2 sum mu_k(1-tau_k^2)/7=-1/2 prove, for EVERY complex raw v,

    8+U-H/2=C-2 mu0 dot beta(0,v).                  (20a)

The limiting sum is positive and <4, and 0<C<8. These coefficient/dual
identities are old8921 data, not a new expansion or limiting constant.
Define on the raw joint domain

    Graw(eta,v)=[F(eta,v)-8-eta(C-2mu0 dot beta(eta,v))]/eta^2.   (20b)

The numerator and its first eta derivative vanish identically at eta0
by(20a). Hence this quotient is jointly holomorphic with a removable
singularity on the ENTIRE |eta|<1/1024 raw-rho domain. Its undivided
numerator is bounded by

    32+8+(1/1024)[8+2*4*2^11]<64.

Maximum modulus after the known order-two eta zero now gives the NEW
uniform numerical bound

    |Graw|<=64/(1/1024)^2=2^26.                    (20c)

This deflates before any tail elimination. Consequently we do not need
a complex-eta extension of the moving branch or its inverse to retain
this majorant after fixed-eta tail elimination below. The prior qualitative
deflation keeps its credit; the covered(20c) and its quantitative use are
new.

## 5. The uniform quantitative normalized inverse

For fixed real eta in(0,e], let Ntilde=(beta3,beta4,gamma3,gamma4).
From(19), Cauchy on the inner raw rho/2-polydisk, in sixteen parameters,
gives multilinear infinity-operator bounds

    ||D Ntilde||<=2^16(32/rho)=B1=2^27,
    ||D^2 Ntilde||<=2*2^16(32/rho)^2=B2=2^39.       (20)

The same component bounds hold for every inactive beta/gamma. Sixteen
variables, all repeated-derivative factorials, and sums over every
derivative index are included. Eta is fixed for these derivative estimates;
they do not purport to bound derivatives in a seventeenth eta coordinate.

Fix arbitrary complex free/normal targets of maximum displacement <d.
On the closed four-tail s-ball about w0, all raw parameters lie inside
the inner rho/2-polydisk: the branch offset is <rho/4 and s<rho/4.
Use

    T_(z,beta,gamma)(w)=w-A0^-1[Ntilde(z,w)-(beta,gamma)].       (21)

Along the complete raw segment from v0, (7),(20) give its tail
Lipschitz constant at most `L B2 s=1/8`. Its displacement at w0 is
at most `L(B1+1)d<s/4`. It sends the closed s-ball into the open3s/8
ball, giving existence and uniqueness throughout that s-ball. Uniform
iteration on compact target polydisks gives a holomorphic tail, real on
real data. This quantifies the fully off-branch four-tail Jacobian rather
than using a branch determinant alone.

For real data each inactive half-normal is
`alpha_k^±=eta beta_k±eta^(3/2)gamma_k`. Its total change throughout the
entire eliminated product is bounded by

    |Delta alpha_k^±|<2eta B1s=2^-24 eta<eta/8.       (22)

Since its branch value is <-eta/4 it remains <-eta/8. The marked root
stays a. From(10) on real data, q>1/2 and `|mh|<4rho`, `|h_free|<rho`;
the heavy critical gap exceeds sqrt(eta), and each heavy-small gap exceeds
sqrt(eta)/4 since1/2-5rho>1/4. The reciprocal bounds apply throughout
the product. At normalized target0 our tail is the9225 zero-slack tail
near the branch by uniqueness, hence it has exactly the same stationary
Hessian at the branch. No old nonlinear collar is imported.

## 6. Complete elimination, Taylor estimates and feasible radial integration

Let G(z,beta,gamma)=Graw(eta,v(z,beta,gamma)) at each fixed positive eta.
It is holomorphic and bounded by2^26 on the full sixteen-target d-polydisk,
by(20c) and the complete inverse. Put H=F after the same elimination:

    H=8+eta(C-2mu0 dot beta)+eta^2 G.

Cauchy on the inner d/2-polydisk gives

    ||D^2 G||<=K2=2^37 d^-2,
    ||D^3 G||<K3=2^44 d^-3.                        (23)

These derivatives are AFTER every heavy variable has been solved; no
unevaluated implicit derivative or partial Taylor polynomial is used.
Euclidean unit free directions have maximum norm at most1, so K3 also
bounds all zero-slack third directional derivatives of the deflated G.
Those of the physical objective are bounded by eta^2 K3.

On `||z-z0||_2<=R`, `||(beta,gamma)||_infty<=b`, we have R<=b<d/2.
Each partial G_beta or G_gamma changes by at most K2 b from its branch
value. The actual individual alpha derivatives obey

    H_alpha_k^±=-mu0_k+(eta/2)G_beta_k±(sqrt(eta)/2)G_gamma_k.   (24)

Their variation is at most [(eta+sqrt(eta))/2]K2 b<=K2 b=1/64.
The individual center derivatives from9267 are -mu_k, so by(6)

    -H_alpha_k^±>9/32-1/64=17/64>1/4.               (25)

If alpha<=0, the full path(z,tau beta,tau gamma),0<=tau<=1 stays in
the box, retains alpha_k^±<=0, and has all inactive originals interior by
(22). It is an actual feasible polynomial path with the same fixed a.
Integrating the individual gradients(25) yields

    H(z,beta,gamma)-H(z,0,0)>=(17/64)sum sigma_k^±.   (26)

For f(z)=H(z,0,0), stationarity and(8),(23) give

    f(z)-F0>=eta^2[L_eta D-(K3/6)||z-z0||_2^3]
            >=(L_eta-delta/6)eta^2D>=k eta^2D.       (27)

Here `K3 R=delta` exactly. Combining(26)-(27) proves(4).
All gradient, Taylor and feasible segments lie in the same certified
domains. This argument does not assert the optimal local endpoint is
attained on our box.

For any raw real v within t of v0, the free Euclidean displacement is
at most sqrt(12)t<R. Its active normalized normals have maximum norm
at most B1t<b. Its tail lies in the complete uniqueness s-ball. The
quantitative inverse therefore identifies this p with the completely
eliminated tail. Disk-rootedness supplies alpha<=0, proving raw-box coverage.

## 7. Collision-safe polynomial-coefficient entry

This geometric entry mechanism is credited to [9315](../effective-neighborhood/PROOF.md);
we include it to make the improved constants fully checkable. On the
branch all eight critical moduli are <1/32, as(6) gives
`4e^2+2e<1/1024`. The heavy centers differ by >2sqrt(eta) and each is
more than sqrt(eta) from the small center r=eta x0, since T0>1.

Draw three disjoint circles of radius ccrit in(1). The covered bounds give
`ccrit<eta/4`, and each circle lies in |z|<1. On the small boundary

    |p0'|>9 ccrit^6 (sqrt(eta)/2)^2>eta ccrit^6.

On either heavy boundary

    |p0'|>9 ccrit (sqrt(eta)/2)^6 sqrt(eta)
           =(9/64)eta^(7/2)ccrit>eta ccrit^6.

The last inequality follows from ccrit<eta/4 and eta<=1. If the monic
coefficient maximum distance is <=ccoef, then on these circles

    |p'-p0'|<=36 ccoef=(36/128)eta ccrit^6<eta ccrit^6.          (28)

Rouche gives six small criticals with multiplicity and one critical in
each heavy disk, exhausting all eight. Analytic labels at the six-fold
collision are unnecessary. Literal real/imaginary parts recover

    |Delta u|<=ccrit/eta=eta t/1024,
    |Delta h|<=ccrit/sqrt(eta)=eta^(3/2)t/1024.

For the heavy pair recover y=(u_++u_-)/2, T=(h_+^2+h_-^2)/2,
V=sum_all h/eta and M=sum_all h*u. Using branch |u|,|h|<2 gives

    |Delta y|<t/1024, |Delta T|<5t/1024,
    |Delta V|<8t/1024, |Delta M|<40t/1024.            (29)

The free changes are <t as well. The positive heavy ordering recovers(2)
exactly, and monicity plus p(a)=0 recovers the anchored p exactly. Thus
every polynomial in the coefficient ball lies in the raw t-box. This
proves the corollary with `ccoef=delta^6 2^-1999 eta^13`.
For k=1/4, delta>1/8, giving(5). Equality in(4) at this positive k forces
D=0 and all sigma0; tail uniqueness then gives p=p0.

## 8. A precise interface with root-displacement entry

The following elementary conversions describe sufficient common entry
quantities; their telescoping method is not claimed historically new.
For two monic disk-rooted degree-nine polynomials with the same a, match
their eight unmarked originals and put

    E_orig,branch=min_permutation sum_(j=1..8)|Z_j-Z_j^0|^2.

Telescoping each elementary symmetric product bounds its coefficient
difference by `binom(8,k-1)sum|Delta Z_j|`, for k=1,...,9.
Since the largest binomial is70 and sum|Delta Z|<=sqrt(8E_orig,branch),

    ||c(p)-c(p0)||_infty<=200 sqrt(E_orig,branch).    (30)

Thus `E_orig,branch<=(ccoef/200)^2` suffices for our stability theorem.
Original collisions do not invalidate the finite multiset match.

Similarly match all eight criticals to the branch with multiplicity and set
`E_crit,branch=min_permutation sum|zeta_j-zeta_j^0|^2`. Both multisets lie
in the unit disk by Gauss-Lucas. Their kth elementary coefficient difference
is <=binom(7,k-1)sum|Delta zeta|. Integrating and anchoring at the same
|a|<=1 bounds the constant as well as the other coefficients by

    [sum_(k=1..8)9/(9-k)binom(7,k-1)]sum|Delta zeta|
       =(2295/8)sum|Delta zeta|<1024 sqrt(E_crit,branch).        (31)

Consequently `E_crit,branch<=(ccoef/1024)^2` also suffices. These are
energies relative to this particular branch, not a critical reciprocal
energy relative to a collapsed constant profile.

[9307](../../six-sendov-1/energy-phase-routing/PROOF.md) instead enters an
antipodal original configuration. With d_a=1+a, gamma_a=a-5/8 it uses

    E_antipodal=sum|1/(a-Z_j)-1/d_a|^2
                          <=gamma_a/(164000 d_a^2),
    or B_antipodal=sum|Z_j+1|^2<=d_a^2 gamma_a/165000.            (32)

Equations(30)-(31) supply a coefficient interface only when the energy
is measured relative to our branch. They do not convert(32) into branch
entry. At a=1-eta our coefficient neighborhood and9307's entry region
leave, in particular, the competitor set

    ||c(p)-c(p0)||_infty>ccoef,
    E_antipodal>gamma_a/(164000 d_a^2)               (33)

unrouted by those two sufficient conditions. Polynomials in(33) may be
handled by other theorems; no failure of first-power is inferred.

The newly committed independent
[9339](../../six-reviewer-1/critical-phase-audit/REVIEW.md) confirms9307's
new phase/entry theorem and enlarges the denominators in(32) to163200
and164000. Its final surplus remains conditional on9189, whose higher
certificate it does not audit. We cite that scope as coverage context,
without importing its kernel or transferring a verdict to this theorem.

A concrete example is p(z)=z^9-a^9. Its criticals are all0 and F=8/a>8.
Its eight unmarked originals are a times the nontrivial ninth roots.
One has theta=2pi/9, giving imaginary reciprocal magnitude
cot(pi/9)/(2a)>1/2, so E_antipodal>1/4. Also |a exp(2pi i/9)+1|^2>1,
so B_antipodal>1. Both conditions in(32), and both enlarged9339 conditions,
fail. Its branch z8
coefficient differs by >9eta/8, because `6x0+2y0<-1` on the credited
covering cube; ccoef<eta/2. Thus our coefficient entry also fails. The
benchmark illustrates a real coverage gap while itself satisfies the
desired first-power inequality. No global intermediate-region exclusion
or small-eta all-competitor entry is claimed here.

## 9. Verification and limits

[bounds.py](bounds.py) recomputes the unchanged radial/cubic certificate,
verifies the joint anchored polynomial majorant and checks every stated
domain, derivative, contraction, gradient, Taylor, metric and entry budget.
Its monomial comparisons use exact rational half-integer eta exponents:
all remaining exponents are nonnegative and eta<=e,delta<=1/2. Every
positive eta and gap is covered, without a finite eta grid.
[verify.py](verify.py) hash-checks61 unchanged public input files, regenerates
the entire compact [expected.json](expected.json), and compares every field.
[VALIDATION.json](VALIDATION.json) records normal/O agreement, damaged
mathematical and external fixture rejections, baseline reproductions,
serial45-second guards and native threads1. Validation is not independent
review and does not prove an unformalized analytic bridge by itself.

The ordinary multivariable root continuation, holomorphic divisibility,
even descent in epsilon, Cauchy estimates, contraction dependence, root-
multiset Rouche completeness, moment inverse and actual feasible segment
are proved above outside a formal proof kernel. The generic jet/parity
structure, all branch/curvature/radial premises and old collision-safe
entry receive explicit prior credit. The new contribution is the joint
quantitative majorants and a uniform positive normalized stability collar for every fixed positive
k-gap and the resulting eta13 numerical coefficient radius.
No positive physical coefficient radius through eta0, effective
all-competitor concentration entry, whole-window global minimum, endpoint
attainment or unrestricted first-power solution is established.
