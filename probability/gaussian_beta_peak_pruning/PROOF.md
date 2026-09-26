# A peak certificate signs a growing block of every beta row

Author proof, 26 September 2026; independent review pending. This is a
certificate consequence of Aishwarya--Li's existing PC2 theorem, not a new
pressure comparison theorem. It signs actual Gaussian beta averages for
arbitrary contractions when their density peak is bounded. It neither
settles full R3 majorisation nor yields a new Kneser--Poulsen consequence.

## 1. Precise sign statement

Let mu be a bounded probability law on R3, T a contraction on its support,
s>0, f=mu*gamma_s, g=(T#mu)*gamma_s and C=(2 pi s)^(-3/2). Write F=f/C,
G=g/C and use the established normalization

    a_j=C integral[(G^(j+2)-F^(j+2))/((j+1)(j+2))],
    b_(N,j)=(N+1) binom(N,j) sum_(ell=0)^(N-j)
                                  (-1)^ell binom(N-j,ell) a_(j+ell).

Suppose a certified number 0<M<=1 satisfies F,G<=M everywhere.

**Theorem 1.** For every integer N>=0, 0<=j<=N,

    j+2 >= M(N+2)  implies  b_(N,j)>=0.                 (1)

Equivalently the signed block is

    0<=q=N-j<=floor((1-M)(N+2)),

clipped to 0<=q<=N. This is an unbounded-width block when M<1 is fixed.
It is separate from the reviewed universal strip q<=6, which needs no peak
input. The two rules can be united, but the proof and executable here use
only (1). No negative sign is asserted outside the certified block.

**Proof.** Set q=N-j and define U on [0,M] by U(0)=U'(0)=0 and
U''(u)=u^j(1-u)^q. On this interval the function

    W(u)=u^2 U''(u)=u^(j+2)(1-u)^q

is nondecreasing under (1): for q>0 its derivative is

    W'(u)=u^(j+1)(1-u)^(q-1)[j+2-(N+2)u]>=0.           (2)

For q=0, W'= (j+2)u^(j+1)>=0 directly. Extend U past M by specifying

    U''(u)=W(M)/u^2,  u>M,

and integrating with matching value and first derivative at M. Then U is
C2 and convex on [0,infinity), and u^2 U''(u) is globally nondecreasing.
In terms of pressure P(u)=u U'(u)-U(u), the derivative of P(e^t) is
W(e^t), which is nondecreasing. Thus P(e^t) is convex. Its additive second
forward differences are nonnegative, which is exactly the multiplicative
second-difference definition of PC2. This verifies the nonsmooth joining
point directly; we do not assume a nonexistent third derivative at M.

The energy V(rho)=C U(rho/C) is in PC2 as well, since positive scaling and
rescaling its argument preserve that finite-difference condition. Apply
Aishwarya--Li, Theorem1.3, in dimension3 to obtain integral V(g)>=integral
V(f). Only U on [0,M] is evaluated. Expanding its original polynomial
curvature and integrating twice gives

    C integral[U(G)-U(F)]
         =sum_(ell=0)^q (-1)^ell binom(q,ell) a_(j+ell).

Multiplication by the positive factor (N+1)binom(N,j) proves (1).
All integrals are finite: near zero U=O(u^2), and on [0,M] U(u)<=K u
for a finite K. The same observations handle diffuse bounded laws. QED.

The extension is essential. The unmodified polynomial can fail PC2 at
larger density values that neither law attains. Applying the source theorem
to that unmodified polynomial without the extension would be invalid.
Theorem1 claims no quantitative positive margin or strictness theorem.

## 2. Rational peak certificates for finite inputs

For finite centers x_i,y_i in R3, common nonnegative probability weights
w_i, and |y_i-y_l|<=|x_i-x_l|, zero-mass labels are discarded. Put
D_il=|y_i-y_l|^2 and

    B=sum_(i,l) w_i w_l D_il/(4s+D_il),
    M_pair=1-B/2.                                      (3)

**Lemma 2.** Both F and G are at most M_pair.

For either endpoint z_i, Gaussian multiplication and completing a square
show, at every z,

    (sum_i w_i exp(-|z-z_i|^2/(2s)))^2
      <=sum_(i,l) w_i w_l exp(-|z_i-z_l|^2/(4s))
      <=sum_(i,l) w_i w_l /(1+D_il/(4s))=1-B.

The second line uses the contraction at the source endpoint and e^t>=1+t.
Since 0<=B<1 and sqrt(1-B)<=1-B/2, (3) follows. No numerical exponential
or square root is evaluated. The argument is also valid with the corresponding
double integral for a bounded law, although the program consumes finite data.

A second bound can be substantially better for separated target clusters.
Group labels with identical y_i and let rho be the largest total group mass.
If there are at least two groups, let d^2 be their minimum squared separation.
Set

    M_sep=(8s+rho*d^2)/(8s+d^2).                         (4)

If there is only one target group, set M_sep=1.

**Lemma 3.** Both F and G are at most M_sep.

At any z, a ball of open radius d/2 contains positive-mass centers from
at most one target group, at either endpoint. At the source endpoint this
uses |x_i-x_l|>=|y_i-y_l|>=d for labels in different groups. The mass of
centers in that ball is at most rho. Every center outside it contributes
at most exp(-d^2/(8s)) to the normalized Gaussian sum. Therefore

    F(z),G(z)<=rho+(1-rho)exp(-d^2/(8s))
             <=rho+(1-rho)/(1+d^2/(8s))=M_sep.

Points exactly at distance d/2 belong to the outside part, so the open-ball
choice creates no boundary gap. The same proof works if the source points
within one target group are distinct. It does not assume an injective T.
QED.

Use M=min(M_pair,M_sep). With rational coordinates, masses and variance,
this is a rational number computable in O(n^2) pair operations and rational
comparisons, with arbitrary-size integer arithmetic. Bit costs are not
claimed constant. Target collisions are aggregated exactly; source collisions
are accepted only when the contraction test forces matching images.

These bounds are sufficient, not sharp. The theorem also accepts any other
rigorous common peak bound, without relying on how it was obtained.

## 3. A complete row and a large compact-row certificate

This is a sign rule on a whole input class, not a list of positive sample
integrals. For example, suppose distinct target groups are separated by at
least1, each group has mass at most1/10, and 0<s<=1/128. Then (4) gives

    M<=13/85.

Every admissible R3 contraction with these properties satisfies (1) in
every row. In particular all eight entries of N=7, including the otherwise
unresolved b_(7,0), are nonnegative. Arbitrarily many centers and zero weights
are permitted subject to these group-mass and separation bounds. A rescaled
version replaces 1 by d and 1/128 by d^2/128. No full-majorisation statement
is inferred from this finite row or growing block.

[INPUT.json](INPUT.json) instantiates R7's strong ten-point depth-one flap
at shape parameters (1,2,3), equal masses, and variance1/128. Its endpoint
map contracts, retains paired affine rank6, has d^2=1 and rho=1/10.
[CERTIFICATE.json](CERTIFICATE.json) contains M=13/85 and the exact ranges:

| Row N | Signed indices j | Number signed |
| --- | --- | --- |
| 7 | 0 through7 | 8 |
| 2199023255549 | 336321203789 through2199023255549 | 1862702051761 |

The large row equals R3's new N_64=2048*64^5-3. After separate translations
by the first label and rescaling to variance one, both squared radii are
at most2432<128^2, so this ten-label datum belongs to the radius part of
K^c_64; its label budget is also amply below A_64. The unchanged compact
class permits real coordinates. We do NOT claim it is in the strict-loss
rational family R^c_64: the flap has exact zero pair losses and the variance
rescaling need not be rational. The mathematical sign rule applies directly
to every exact rational-family input that passes its peak criterion as well.

No high-degree polynomial, moment stream, quadrature or gigantic power is
formed to certify the large block. The fixture tests delivery and normalization;
the universal class assertion follows from Lemma3 and Theorem1. Paired rank6
alone does not establish that this ten-point map lacks an R5 contracting motion.

## 4. A rigorous boundary: peak pruning cannot close the finite frontier

If the target law has at most A positive-mass centers, then

    ||G||_infinity>=max_i w_i>=1/A,

by evaluating G at a center of maximum mass. Consequently every valid common
peak upper bound M satisfies M>=1/A. Even an exact peak oracle cannot make
criterion (1) certify any integer

    0<=j<ceil((N+2)/A)-2.                                (5)

The number of such entries is max(0,ceil((N+2)/A)-2). This is a limitation
of this sufficient rule, not negative beta values or impossibility of another
proof. Taking A=A_k=O(k^3(1+log k)^(3/2)) and the new N_k+2=2048k^5-1
leaves an unbounded block of order at least k^2/(1+log k)^(3/2) as k grows.
The independently signed q<=6 strip is at the other end of these large rows
and does not remove this leftmost block.

In particular when N+2>2A, even b_(N,0) cannot pass the peak criterion.
Thus tighter peak estimates or more examples cannot by themselves close
the compact frontier. The remaining task is a sign argument for low density,
or an actual negative weighted beta/convex-energy/hinge certificate.

## 5. Reproduction and trust boundary

Run the commands in [README.md](README.md). `certify.py` verifies the finite
contraction and probability law, recomputes both rational peak bounds, and
checks or emits the full index intervals without looping over a large row.
`verify.py` checks169 polynomial identities,3825 exact block/barrier controls,
translations, variance scaling, splitting a target mass, zero masses, paired
rank6, the compact radius, and eight damaged-input/certificate rejections.
These are author controls, not independent review. The analytic pressure
extension, Gaussian peak inequalities and imported PC2 theorem remain written
mathematical premises. There is no solver, interval library, external dataset,
large omitted artifact or floating sign premise in the published certificate.
