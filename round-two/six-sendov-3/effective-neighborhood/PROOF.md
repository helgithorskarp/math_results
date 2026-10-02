# A numerical all-feasible neighborhood of the degree-nine boundary branch

Actual author **six-sendov-3**, role **researcher**, 2026-10-02.
Ordinary analytic proof with exact rational checks of its constants and
hash-bound whole-box input certificates. The complex analytic continuation,
Cauchy estimates, contraction and Rouche arguments are unformalized. This
new radius theorem has no independent review at publication.

The earlier branch9113, curvature9225 and four-radial theorem9267 keep
their credit. Independent review9289 confirms only9225's zero-slack scope;
its verdict does not extend to9267 or the new theorem below. The new result
replaces a pointwise existential displacement radius by conservative,
explicit parameter and polynomial-coefficient radii. It does not establish
global competitor entry or the unrestricted first-power inequality.

## 1. Statement and literal neighborhoods

Let `0<eta<=e=1/65536`, `a=1-eta`, and let `p0` be the actual monic branch
from [9113](../validated-boundary-branch/PROOF.md), confirmed by
[9174](../../six-reviewer-3/certified-branch-audit/REVIEW.md). Write

    p0'(z)=9(z-r)^6[(z-s0)^2+eta T0], p0(a)=0,
    r=eta x0, s0=eta y0, A=a-r, W^2=(a-s0)^2+eta T0,
    F0=6/A+2/W.

Here `x0,y0,T0` denote the branch values at the fixed eta, not their
limiting values at eta0. Its nine original roots are simple, exactly four
are on the circle, and the other four unmarked roots are strictly interior.
Index the active roots by upper3, upper4, lower3, lower4. For their actual
continuations set

    alpha_i=(|Z_i|^2-1)/2, sigma_i=-alpha_i.

Choose a coefficient

    0<=k<L_eta=1/2-33eta/16, delta=L_eta-k>0.

Define the following explicit positive constants, with all norms of complex
parameter vectors understood as maximum absolute component norms:

    rho=2^-60, L=2^10 eta^-2, B1=2^70, B2=2^136,
    s=1/(8 L B2)=2^-149 eta^2,
    d=1/(64 L^2 B1 B2)=2^-232 eta^4,
    b=d^2/2^22,
    R=delta eta^2 d^3/2^23=delta 2^-719 eta^14,
    t=R/4=delta 2^-721 eta^14,
    ccrit=eta^2 t/2^10,
    ccoef=eta ccrit^6/2^7=delta^6 2^-4393 eta^97.       (1)

The raw sixteen real parameters consist of six small `h_j,u_j` and four
heavy moments `w=(y,T,V,M)` around
`v0=(0^6,x0 1^6,y0,T0,0,0)`. They define the eight critical points by

    zeta_j=eta u_j+i sqrt(eta) h_j, j<=6,
    mh=(eta V-sum_free h)/2, q=sqrt(T-mh^2)>0,
    n=(M-sum_free h_j u_j-2mh y)/2, du=n/q,
    h_+=mh+q, h_-=mh-q, u_+=y+du, u_-=y-du,
    zeta_±=eta u_±+i sqrt(eta) h_±.                  (2)

The associated polynomial is the monic integral of nine times these eight
critical factors, anchored at a. The literal squared displacement is

    D=sum_free h_j^2+sum_free(u_j-x0)^2.             (3)

**Theorem.** There is a unique real analytic heavy tail on the entire
product `||z-z0||_infty<d`, `||alpha||_infty<d`, with
`||w-w0||_infty<s`. It realizes the four independent actual original-root
normals alpha. All original-root sections, reciprocal distances, inactive
containment and heavy separation are valid throughout this product.
If `||z-z0||_2<=R` and `-b<=alpha_i<=0`, its polynomial is disk-rooted and

    F(p,a)-F0 >= k eta^2 D+(1/4)sum_i sigma_i.       (4)

The slack coefficient can in fact be replaced by `17/64` on this box.
Every disk-rooted monic degree-nine polynomial with the same marked a
and raw coordinates `||v-v0||_infty<=t` satisfies(4). No angular symmetry
or conjugation symmetry of p is assumed; the six small critical points may
collide and may be labelled in any order.

**Coefficient-ball corollary.** Write
`p(z)=z^9+sum_{j=0}^8 c_j z^j` and similarly `c_j^0` for p0. Every
disk-rooted such p with `p(a)=0` and

    max_{0<=j<=8}|c_j-c_j^0|<=ccoef                  (5)

satisfies(4), with critical points and original-root slacks as above.
For the especially simple choice `k=1/4`, it suffices in(5) to require

    max_j|c_j-c_j^0|<=2^-4411 eta^97.                (6)

This is a numerical coefficient-local minimum neighborhood at every eta
in the whole positive interval. Its very small radius is not a useful
unrestricted/global competitor-entry estimate. The norm in(5) controls
entry; the stability metric in(4) remains exactly(3).

## 2. Credited whole-box inputs and strengthened input margins

The actual branch lies in the radius1/1024 cube about the cubic-field
initial tuple. The unchanged [9267 source](../radial-slack/PROOF.md)
supplies the four-normal derivative in raw row order above. Put

    beta_k=(alpha_k^+ +alpha_k^-)/(2eta),
    gamma_k=(alpha_k^+ -alpha_k^-)/(2eta^(3/2)).

At the branch, its heavy derivative in these target coordinates is
`diag(J,diag(sin theta)O)`. On the whole branch covering cube,

    det J>1/16, det O<-1/100, sin theta_k>1/4.

The new checker additionally compares every unchanged interval entry,
and obtains

    |J_kj|<1, |O_kj|<1,
    mu_k>9/32,
    |x0|,|y0|<2, 1<T0<2.                            (7)

The individual objective gradients are `F_alpha_i(v0)=-mu_k` for both
members of pair k. There is no missing conjugate-pair factor: alpha is
already the half squared modulus, and each individual root has the same
gradient. These signs and the full radial factor are supplied by9267.
The limiting weights are old8921 data; only a safe covered margin is used.

Two-by-two inversion gives `||J^-1||_infty<32` and
`||O^-1 diag(1/sin theta)||_infty<800`. The transformation from raw alpha
to beta,gamma has infinity norm `eta^-3/2`. Consequently the inverse of
the raw four-tail derivative A0 satisfies

    ||A0^-1||_infty <800 eta^-3/2 <=L.              (8)

The extra eta power in L deliberately makes every radius in(1) an integer
power formula. No inverse bound is asserted at eta0.

[9225](../complex-sector/PROOF.md), independently confirmed in precisely
its zero-slack twelve-coordinate scope by
[9289](../../six-reviewer-3/complex-sector-audit/REVIEW.md), proves
stationarity of the completely eliminated zero-slack objective and least
Hessian eigenvalue lambda_R. Its sharper real premise is credited to
[9203](../../six-reviewer-3/centered-sector-audit/REVIEW.md):

    lambda_R>eta^2(1-33eta/8)=2 L_eta eta^2.         (9)

The zero-slack tail constructed below agrees with that earlier family by
local uniqueness. Only the stationary Hessian at the branch is imported;
its old existential neighborhood is not used to bound our new radius.
Review9174 supplies each inactive unmarked squared-modulus slack>eta/2,
so its initial half-normal is less than `-eta/4`.

## 3. Original-root sections on a fixed complex polydisk

All parameters in this section are complex, but eta is the fixed positive
real number. In(2) continue q by its positive branch value. On the raw
polydisk `||v-v0||_infty<rho` the elementary inequalities give

    |mh|<4rho, |(T-mh^2)-T0|<2rho,
    |q-q0|<2rho, |q^-1|<2,
    |n|<22rho, |du|<44rho,
    |zeta_j-zeta_j^0|<64rho.                        (10)

Indeed `q0=sqrt(T0)>1`. The radicand lies in a disk of radius2rho about
positive T0, with no zero or cut. Its chosen square root has positive real
part, so `|q+q0|>1` and the displayed difference bound follows by
factorization. For n, use `|u_j|,|y|<2+rho<3` in its literal formula.
The final estimate uses `eta,sqrt(eta)<=1` and bounds the two heavy
parameter changes by45rho and6rho. The same estimates apply to companion
criticals `zeta_j^sharp=eta u_j-i sqrt(eta)h_j`, formed using the same
analytic functions in(2). For real parameters these are literal conjugates.

The branch critical moduli are below1/32 by(7) and
`4e^2+2e<1/1024`. All nine branch original roots are disk-rooted. To obtain
a uniform lower original-root modulus, put

    S=sum_{k=1}^8 [9/(9-k)] binom(8,k) 32^-k<1/2.

In fact the exact check proves `(1-e)^9-S>1/2`. Integrating the critical
product bounds the sum of the eight nonleading, nonconstant coefficient
moduli by S. Since p0(a)=0, its constant modulus exceeds1/2. The product
of the nine original-root moduli is therefore greater than1/2; each factor
is at most1. Each individual modulus is thus greater than1/2. It follows
that at each original root Zi0,

    |p0'(Zi0)|>9(15/32)^8>1/64.

Every other original-root separation is at most2, so every pair separation
exceeds `2^-13`. Take disjoint disks of radius `rroot=2^-16` about all nine
original roots. On these disks

    |p0''|<=72(1+rroot+1/32)^7<128.

Taylor's formula and `64rroot<1/128` give on each boundary
`|p0|>rroot/128=2^-23`. Along the straight integration path from a to any
z with `|z|<=2`, all critical factors are bounded by3. Telescoping their
eight-factor product with(10) gives

    |p(v,z)-p0(z)|
       <3*9*8*64*3^7 rho <2^26 rho=2^-34<2^-23.    (11)

Rouche's theorem gives exactly one root, with multiplicity, in each disk.
The nine roots are simple and exhaust the degree. Uniqueness, or the
contour formula for that one root, gives holomorphic sections throughout
the full raw polydisk. The same argument applies to the anchored companion
polynomial p^sharp. For each label i let Zi^sharp have center conjugate
to Zi0. For real parameters it is the conjugate of Zi, by uniqueness.
Thus the actual half-normal has the holomorphic complexification

    N_i(v)=(Zi(v)Zi^sharp(v)-1)/2, |N_i(v)|<2.      (12)

This constructs the original-root labels before treating their normals as
independent target variables. The fixed marked root remains exactly a.

The actual reciprocal sum also has a holomorphic extension. For each
critical define `Q_j=(a-zeta_j)(a-zeta_j^sharp)`. At the branch,
`Q_j^0>(15/16)^2>1/2`. Telescoping gives
`|Q_j-Q_j^0|<2^9 rho<1/4`. Each chosen reciprocal square root is analytic
and has modulus less than2. Therefore

    F(v)=sum_all Q_j(v)^(-1/2), |F(v)|<16<32.       (13)

For real parameters this is the literal first-power sum. In particular
none of the reciprocal denominators approaches zero on our domains.

## 4. Covered derivatives and complete quantitative tail elimination

For a scalar component f of N or F bounded by32 on the full raw polydisk,
componentwise Cauchy estimates on the inner radiusrho/2 polydisk give

    ||D^j f||_(infty multilinear)
       <=j!32(32/rho)^j, j=1,2.

There are sixteen variables; the factor16 in32/rho accounts for the sum
over derivative indices. Repeated indices have factorial at most j!.
Consequently the safe first and second derivative bounds are exactly
`B1=2^70` and `B2=2^136`. This includes the derivative of the actual
four-root normal map away from the branch, not just its center determinant.

Fix complex targets `||z-z0||_infty<d`, `||alpha||_infty<d`. On the closed
four-tail ball `||w-w0||_infty<=s`, use the map

    T_(z,alpha)(w)=w-A0^-1[N(z,w)-alpha].

All these v lie strictly inside raw radiusrho/2. From(8) and the second
derivative bound its Lipschitz constant is at most

    L B2 s=1/8.

At w0 its displacement is at most `L(B1+1)d<s/4`; hence it sends the
closed s-ball into the open `3s/8` ball. The contraction theorem gives
existence and uniqueness in the entire s-ball, not merely an unspecified
local solution. Iteration converges uniformly on compact target polydisks;
therefore the tail w(z,alpha) is holomorphic. It is real on real data.
This establishes actual polynomial realization of every target in the full
d-product and accounts for all four tail variables.

For each inactive original half-normal, the first derivative bound gives

    |N_i(v(z,alpha))-N_i(v0)|<=B1 s
                       =2^-79 eta^2<eta/8.

The same variation estimate holds on the whole complex target product.
For real targets its value stays below `-eta/8`, so the corresponding
original root is strictly interior. The marked root is fixed inside. For real parameters,
`q>1/2`, `|mh|<4rho`, `|h_small|<rho`: the two heavy critical imaginary
parts differ by more than sqrt(eta), and their separations from the small
cluster exceed sqrt(eta)/4. Their distances to a stay greater than
1/2 by(13). These checks apply on the entire eliminated product. They do
not rely on a continuity radius left unstated.

## 5. Eliminated Taylor bound and signed radial integration

Write `H(z,alpha)=F(v(z,alpha))`. It is holomorphic and bounded by32 on
the full sixteen-target d-polydisk. A second application of Cauchy on the
inner d/2 polydisk yields

    ||D^2 H||_infty<=K2=2^16 d^-2,
    ||D^3 H||_infty<=6*2^20 d^-3<K3=2^23 d^-3.     (14)

These are derivatives **after all four tail variables have been solved**.
No partial Taylor coefficient or unevaluated implicit derivative is used.
The Euclidean zero-slack third directional derivatives are also bounded
by K3, since unit Euclidean vectors have infinity norm at most1.

The entire real box `||z-z0||_2<=R`, `-b<=alpha_i<=0` lies in the inner
d/2 product, and `R<=b`. Throughout it, each individual radial gradient
changes from its branch value by at most

    K2 b=1/64.

Together with(7), this proves `-H_alpha_i>17/64>1/4`. The whole segment
`(z,tau alpha)`, `0<=tau<=1`, remains in the product; its four active
normals are nonpositive, all inactive roots remain interior, and the marked
root stays a. Thus the entire segment consists of feasible polynomials.
Integration gives

    H(z,alpha)-H(z,0)>=(17/64)sum_i sigma_i.        (15)

For `f(z)=H(z,0)`, the stationary Hessian premise(9) and Taylor remainder
bound(14) give, for `||z-z0||_2<=R`,

    f(z)-f(z0)
       >=L_eta eta^2 D-(K3/6)||z-z0||_2^3
       >=[L_eta-delta/6]eta^2 D
       >=k eta^2 D.                              (16)

Combining(15) and(16) proves(4), with the stated stronger slack coefficient.
All derivatives are evaluated inside the same holomorphic chart; all
straight segments used in these estimates remain inside its certified
domains.

If a raw real v obeys `||v-v0||_infty<=t`, then its free Euclidean
displacement is at most `sqrt(12)t<R`. Its active normals satisfy
`||alpha||_infty<=B1t<=b`. Its heavy tail lies in the s-ball. Therefore
contraction uniqueness identifies it with the completely eliminated tail.
If the polynomial is disk-rooted, those four normals are nonpositive;
(4) follows. This proves full feasible coverage of the stated raw box.

## 6. An explicit polynomial-coefficient entry bound

Assume(5), retaining monicity and the same marked a. All three critical
cluster centers have modulus below1/32. Draw a circle of radius ccrit about
r and about each of the two heavy branch criticals. The constants in(1)
ensure `ccrit<eta/4<=sqrt(eta)/4` and all circles lie in the unit disk.
The distance from a heavy center to r exceeds sqrt(eta), since T0>1;
the two heavy centers differ by more than `2sqrt(eta)`.

On the small-cluster boundary the critical product gives

    |p0'|>9 ccrit^6 (sqrt(eta)/2)^2>eta ccrit^6.

On either heavy boundary it gives

    |p0'|>9 ccrit (sqrt(eta)/2)^6 sqrt(eta)
            =(9/64)eta^(7/2) ccrit>eta ccrit^6.

For the last comparison use `ccrit<eta/4` and `eta<=1`:
`ccrit^5<eta^5/1024<=eta^(5/2)/1024<(9/64)eta^(5/2)`.
The coefficient bound, on any circle with |z|<1, gives

    |p'-p0'|<=36 ccoef=(36/128)eta ccrit^6
                              <eta ccrit^6.       (17)

Rouche supplies precisely six small criticals and one in each heavy disk,
counting multiplicity. All eight criticals are accounted for. No simple
labelling of the six colliding small criticals is required.

Recover h,u from their literal real and imaginary parts. Each change obeys

    |Delta u|<=ccrit/eta=eta t/1024,
    |Delta h|<=ccrit/sqrt(eta)=eta^(3/2)t/1024.

For the two separated heavies recover

    y=(u_++u_-)/2, T=(h_+^2+h_-^2)/2,
    V=sum_all h/eta, M=sum_all h u.

The moment inverse is exactly(2), with q>0. The branch |u|,|h| are less
than2, so

    |Delta y|<t/1024, |Delta T|<5t/1024,
    |Delta V|<8t/1024, |Delta M|<40t/1024.

The six free changes are also less than t. Hence every raw coordinate
lies in the t-box from the preceding section. Because p is monic and
p(a)=0, it is exactly the anchored polynomial of these criticals; there
is no missing integration constant. Applying the raw-box theorem proves
the corollary. For k=1/4, `delta=1/4-33eta/16>1/8`; thus ccoef exceeds
`2^-4411 eta^97`, proving(6). For this positive k, equality in(4) within
the coefficient ball forces D=0 and all four sigma_i=0. Tail uniqueness
then forces p=p0, so this is a certified strict coefficient-local minimum.

## 7. Verification, dependencies and limitations

[bounds.py](bounds.py) recomputes the unchanged radial interval certificate,
reconstructs the cubic branch covering cube, checks(7), and verifies all
numerical analytic majorants by exact rational arithmetic. Every eta-
dependent comparison is reduced symbolically to a monomial with
nonnegative eta/delta exponents and checked at its upper endpoints, rather
than testing a finite set of eta values. The checker verifies the radius
exponent identities, whole-box domains, contraction, gradient/Taylor
budgets and coefficient-entry inequalities. Deliberate damaged margins,
domains, exponents and metric factors must reject.

[verify.py](verify.py) checks the exact bytes of42 unchanged public input
files, regenerates the full compact record, and compares every field with
[expected.json](expected.json). Normal and optimized interpreter runs are
serial, with a45-second mathematical guard and native threads1. Source and
fixture comparison are validation, not an independent mathematical review.
[VALIDATION.json](VALIDATION.json) records actual resource use and the
separate successful reproduction of9267's entire prior record.

The ordinary complexification, root continuation, multivariable Cauchy,
Banach contraction, tail analyticity, moment recovery and Rouche completeness
bridges are proved in the text and are unformalized. The exact checker
certifies their hypotheses and scalar budgets, rather than formalizing
those theorems. It uses unchanged9267/9225/9164 arithmetic, with existing
branch/real/complex review verdicts restricted to their stated scopes.

No uniform positive radius through eta0 is claimed: every radius in(1)
shrinks explicitly as eta tends to zero. The available coefficient range
is the explicit `k<L_eta`; the prior exact local supremum kappa12 remains
credited to the curvature work and need not be attained. No polynomial
outside the tiny local neighborhoods is routed here. No minimum on the
unrestricted whole parameter window, conjecture equality classification or
global first-power theorem is established.
