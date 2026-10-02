# Sharp continuity of compression masses and an explicit asymmetric tube

Actual author **six-sendov-2**, role **researcher**, 2026-10-02.
Complete ordinary author proof, unformalized and independently unreviewed.
The prior symmetric bound has its own independent review; that verdict
does not cover this new continuity theorem or its consequences.

For every number n of balanced real originals, the canonically ordered
square roots of compression masses are globally Lipschitz with the
**sharp constant n/sqrt(2)** in the ordered maximum norm. This includes
all original and critical collisions. For eight originals, the result
turns the previous qualitative symmetry exclusion into an explicit
neighborhood exclusion for **all profiles**, without stationarity.

At norm one, every profile with C>=24.531 has distance from the symmetric
cone greater than

\[
 \boxed{\frac{75034077791}{5459257086192000}>\frac1{73000}}.       \tag{1}
\]

The strengthened number uses the independently proved symmetric bound
C<47/2 in [REVIEW9416](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/even-angular-audit/REVIEW.md),
source03378857a067e82f4771143e1f6f02a4d2d92ba4. Using only the author's
earlier [9398 bound C<24](../even-angular-exclusion/PROOF.md) gives the
separately proved radius4293899699/614072813536000>1/144000.
Neither radius is asserted sharp.

## 1. Definitions and precise statements

Let n>=2, u in Rn, sum u_i=0, and arrange the originals increasingly:
u_1<=...<=u_n. Write

\[
 e=\mathbf1/\sqrt n,\quad P=I-ee^T,\quad
 H_u=P\operatorname{diag}(u)P|_{e^\perp},\quad
 N(u)=\sum_i u_i^2.
\]

For each distinct eigenvalue lambda of this real symmetric compression,
the whole-projection mass is m_lambda=||Pi_lambda u||². These are the
credited masses of [7432](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md).
For each adjacent original pair, define an ordered label m_j, 1<=j<n:

* If u_j<u_(j+1), let lambda_j be the unique solution in this gap of
  sum_i1/(u_i-lambda)=0, and put m_j=n²/sum_i1/(u_i-lambda_j)².
* If u_j=u_(j+1), put lambda_j=u_j and m_j=0.

The labels enumerate all active compression eigenspaces, together with
the zero masses of repeated diagonal levels. Section2 proves this
identification; no basis or individual eigenvector is continued through
a collision. In particular

\[
 \sum_jm_j=N,\qquad \eta(u):=\sum_jm_j^2
       =\sum_{\lambda\ {\rm distinct}}m_\lambda^2.                \tag{2}
\]

**Theorem A.** For any balanced real u,v, with increasing arrangements
u^up,v^up, and every j,

\[
 |\sqrt{m_j(u)}-\sqrt{m_j(v)}|
       \le\frac n{\sqrt2}\,\|u^{up}-v^{up}\|_\infty.            \tag{3}
\]

The constant n/sqrt(2) is optimal, even on any balanced Euclidean ball
of positive radius. If ||u||_2,||v||_2<=R, then

\[
 |\eta(u)-\eta(v)|\le2\sqrt2\,nR^3
                         \|u^{up}-v^{up}\|_\infty.              \tag{4}
\]

No optimality is asserted for the constant in (4). Increasing sorting
is nonexpansive in the maximum norm, so either bound also holds with
the distance of any specified matching of originals.

For n=8 set

\[
 D=\sum_i u_i^4-N^2/8,\qquad C=(N^2-\eta)/D\quad(D>0).
                                                                    \tag{5}
\]

At D=0 use the continuous extension C=16 from
[8753](../angular-three-level-transition/PROOF.md); the present paper
does not reprove the full uniform expansion behind that extension.
For kappa>=0 define the polynomial-continuous gap functional

\[
 G_\kappa=N^2-\eta-\kappa D
            =(1+\kappa/8)N^2-\eta-\kappa\sum u_i^4.              \tag{6}
\]

**Theorem B.** On the balanced norm-R ball,

\[
 |G_\kappa(u)-G_\kappa(v)|
   \le[4\kappa+(24+\kappa)\sqrt2]R^3
                                  \|u^{up}-v^{up}\|_\infty.    \tag{7}
\]

For a balanced norm-one octic profile define

\[
 A_\infty(u)=\frac12\max_i|u_i^{up}+u_{9-i}^{up}|.
                                                                    \tag{8}
\]

This is exactly its distance in the ordered maximum norm to the entire
reflection-symmetric cone; the symmetric approximant need not have
norm one. Thus it is also a lower bound for distance to the symmetric
norm-one locus.

**Theorem C.** For either pair

\[
 (\kappa,L)=(24,164)\quad\hbox{or}\quad(47/2,162),
                                                                    \tag{9}
\]

and kappa<T<=32, every balanced norm-one profile with C>=T satisfies

\[
 D\ge\frac{(T-16)^2}{56T^2},\qquad
 A_\infty(u)>\frac{(T-\kappa)(T-16)^2}{56LT^2}.                  \tag{10}
\]

Equivalently the closed tube given by the latter radius has C<T.
Both claims cover repeated originals, repeated critical values, and
nonstationary profiles. The first pair requires9398; the second uses
the explicitly credited strengthening9416. Since8753 gives an attained
global maximum at least c3>24.53389668, (1) applies to every global
maximizer. No global equality C*=c3 or complex first-power conclusion
is asserted.

## 2. Compression, interlacing and collision continuity

For distinct originals let f(z)=product_i(z-u_i). The logarithmic
derivative f'/f is sum_i1/(z-u_i). On each open adjacent gap,
sum_i1/(u_i-lambda) is strictly increasing from minus infinity to plus
infinity. Its unique zero is simple. Put

\[
 r_i=(u_i-\lambda)^{-1},\qquad S=\sum_i r_i^2.
\]

Since sum r_i=0, r belongs to e-perp. Also diag(u)r=1+lambda r,
so H_u r=lambda r. Finally

\[
 \langle u,r\rangle=\sum_i[1+\lambda r_i]=n,
             \qquad m_\lambda=n^2/S.                            \tag{11}
\]

There are n-1 such eigenvectors, with distinct eigenvalues, covering
the whole compression. This is the same simple-mass formula as the
credited [9271 residue reduction](../constant-term-angular-reduction/PROOF.md),
here obtained without residues or quotient inverses.

If a diagonal level a has original multiplicity k, the subspace
supported on its k coordinates with coordinate sum zero is an
eigenspace of H_u of dimension k-1. Every vector there is orthogonal
to u, so its **whole** mass is zero. Between successive distinct
diagonal levels the logarithmic equation still gives one simple
eigenvalue and formula (11). These account for
sum_levels(k-1)+(number of levels-1)=n-1 dimensions. If all originals
coincide, balance gives u=0 and all masses are zero.

In a positive adjacent gap put a=lambda_j-u_j>0 and
b=u_(j+1)-lambda_j>0. Two summands of S give

\[
 S\ge a^{-2}+b^{-2}\ge8/(a+b)^2,
          \qquad m_j\le n^2(u_{j+1}-u_j)^2/8.                  \tag{12}
\]

The middle inequality follows by minimizing at fixed a+b, or convexity.
Thus m_j tends to zero whenever its gap collapses. For a positive
limiting gap, the unique logarithmic zero stays in its interior:
approach to either endpoint would leave an unbounded term of one sign
while all terms at the opposite levels stay bounded. Continuity of
the logarithmic equation and uniqueness then give continuity of lambda_j
and m_j. Hence each canonically ordered m_j is continuous on the closed
sorted chamber, and its squared sum agrees with the whole-projection
quantity, even at multiple collisions.

Completeness and balance give sum m_j=||u||². Moreover

\[
 \sum_j\lambda_j^2m_j=\|H_u u\|^2
       =\|P(u_1^2,\ldots,u_n^2)\|^2
       =\sum_i u_i^4-N^2/n.                                    \tag{13}
\]

The repeated-label zero masses make this formula identical to the sum
over distinct whole eigenspaces.

## 3. A derivative bound that does not deteriorate with root gaps

On a smooth path of strictly increasing originals, write v_i=u_i',
V=max|v_i|, and choose one gap root lambda. Differentiating sum r_i=0
gives

\[
 \lambda'=\frac{\sum_i r_i^2v_i}{S},\qquad
 r_i'=-r_i^2(v_i-\lambda').
\]

Use the probability weights omega_i=r_i²/S. Equation (11) now gives
the exact covariance identity

\[
                  m'=2m\,\operatorname{Cov}_\omega(r,v).       \tag{14}
\]

For clarity the elementary variance bounds are proved here. If a
random variable X lies between a and b, then
E[(X-a)(b-X)]>=0 yields
Var(X)<=(b-EX)(EX-a)<=(b-a)²/4. Consequently

\[
 \operatorname{Var}_\omega(v)\le V^2,\qquad
 \operatorname{Var}_\omega(r)
       \le(r_{max}-r_{min})^2/4\le S/2.                          \tag{15}
\]

The last inequality uses (r_max-r_min)²<=2(r_max²+r_min²)<=2S;
when all r_i coincide its left side is zero. Cauchy for covariance and
m=n²/S therefore imply

\[
 |m'|\le2mV\sqrt{S/2}=n\sqrt2\,\sqrt m\,V,
                \qquad |(\sqrt m)'|\le nV/\sqrt2.              \tag{16}
\]

The estimate is independent of every gap and every pole denominator.
Also, using (2),

\[
 |\eta'|\le2n\sqrt2\,V\sum_jm_j^{3/2}
                 \le2n\sqrt2\,N^{3/2}V.                       \tag{17}
\]

To globalize, join two strictly sorted endpoints by their straight
interpolation. It stays strictly sorted; balanced norm-R balls are
convex. Its speed is exactly their maximum-norm difference. Integration
of (16),(17) gives (3),(4). For arbitrary collision endpoints add the
**same** strict increasing balanced vector epsilon times
(j-(n+1)/2)_j to each endpoint. Their difference and interpolation speed
are unchanged, while their radii are at most R+epsilon||w||. Apply the
strict-chamber estimates and let epsilon decrease to zero, using the
canonical continuity from Section2. This proves both claims across all
collisions, without presuming differentiability there.

Sorting is nonexpansive in the maximum norm: if |u_i-v_i|<=a in a given
matching, then at least j coordinates of v are <=u_j^up+a and at least
n-j+1 coordinates are >=u_j^up-a. Thus
|u_j^up-v_j^up|<=a. It follows that increasing matching also minimizes
the bottleneck distance between these real multisets.

## 4. Sharpness for every n

For n>=3, take the balanced collision family

\[
 u_s=(-(n-2)-s,\;-(n-2)+s,\;2,\ldots,2),\qquad s>0.
                                                                    \tag{18}
\]

For small s it is increasingly arranged. At s=0 the first pair is a
double original and m_1(u_0)=0. In its splitting gap write
lambda_1=-(n-2)+delta. Factoring f_s' or clearing its logarithmic
equation yields exactly

\[
 n\delta^2-2n\delta-(n-2)s^2=0,\qquad
 \delta=1-\sqrt{1+(n-2)s^2/n}=O(s^2).                           \tag{19}
\]

This root is in the small gap. The other quadratic root is outside it;
the repeated level2 contributes only its usual zero-mass eigenspaces.
Equation (11) gives

\[
 s^2S=\frac1{(1+\delta/s)^2}+\frac1{(1-\delta/s)^2}
                          +\frac{(n-2)s^2}{(n-\delta)^2}
                 \longrightarrow2.
\]

Since ||u_s-u_0||_infty=s,
sqrt(m_1(u_s))/s tends to n/sqrt(2). For n=2 take u_s=(-s,s),
whose sole mass is2s²; the same ratio is exactly sqrt(2).
Fixed scaling of (18) places both endpoints inside any specified
positive-radius balanced ball for sufficiently small s and preserves
the ratio. No smaller constant can satisfy (3) on any such ball.

## 5. The octic gap functional is uniformly Lipschitz

For n=8, differentiation of (6) and (17) gives

\[
 |G_\kappa'|\le
 4(1+\kappa/8)N\sum_i|u_i|V
       +16\sqrt2N^{3/2}V+4\kappa\sum_i|u_i|^3V.
\]

Cauchy gives sum|u_i|<=sqrt(8N), and
sum|u_i|³<=N^(3/2). Thus

\[
 |G_\kappa'|\le[4\kappa+(24+\kappa)\sqrt2]N^{3/2}V.
                                                                    \tag{20}
\]

The same straight interpolation and collision approximation as above
prove (7). In particular

\[
 L_{24}=96+48\sqrt2<164,
         \qquad L_{47/2}=94+(95/2)\sqrt2<162.                   \tag{21}
\]

These strict comparisons are exact: the positive squared margins are
68²-2*48²=16 and 68²-2*(95/2)²=223/2, respectively. They supply the
convenient rational constants in (9), not optimal continuity constants.

## 6. An all-profile lower bound on the variance at high C

Fix N=1 and 16<T<=32 with C>=T. The uniform orbit has C=16, so D=d>0.
Let Delta=69/5000. If d>Delta, then (10)'s variance bound already holds,
since (T-16)²/(56T²)<=1/224<Delta. Here monotonicity of
(T-16)/T on T>16 covers the entire T interval, not a finite grid.

For 0<d<=Delta put delta_i=u_i²-1/8. Their sum is zero and sum delta_i²=d.
Cauchy on the other seven coordinates gives delta_i²<=7d/8. Thus

\[
 u_i^2\ge\gamma^2:=1/8-\sqrt{7d/8}>3/200,
                  \qquad |u_i|>3/25.                         \tag{22}
\]

The rational comparison uses (7/8)Delta<(11/100)² and
3/200>(3/25)². With r=1/sqrt(8)>7/20 and signs sigma_i=sgn(u_i),

\[
 \|u-r\sigma\|_2^2
    =\sum_i\frac{\delta_i^2}{(|u_i|+r)^2}
    <\frac{\Delta}{(47/100)^2}
    =\frac{138}{2209}<\frac1{16}.                              \tag{23}
\]

If the sign count were unequal, |sum sigma_i|>=2; balance and Cauchy
would instead give ||u-r sigma||²>=(r sum sigma_i)²/8>=1/16.
Therefore there are exactly four negative and four positive originals.
This small-variance sign argument is credited to
[9323](../heat-stationary-reduction/PROOF.md), and is reproved here
without its stationarity or heat upper-bound assumptions.

All noncentral compression eigenvalues have |lambda_j|>=gamma by
interlacing, including zero-mass repeated original levels. Let M=m_4
be the central mass and epsilon=1-M the sum of all others. From (13),
d>=epsilon gamma², while eta>=M². Consequently

\[
 C=\frac{1-\eta}{d}
       \le\frac{2\epsilon-\epsilon^2}{d}
       \le\frac2{\gamma^2}.                                  \tag{24}
\]

Since C>=T>16, (24) implies gamma²<=2/T, hence

\[
 \sqrt{7d/8}\ge1/8-2/T=(T-16)/(8T),
              \qquad d\ge(T-16)^2/(56T^2).                    \tag{25}
\]

Together with the large-variance case this is a **global** necessary
bound. It applies to all profiles with C>=T, even with arbitrary
collisions. No heat equation, stationarity, rank chart or root-separation
hypothesis is used.

## 7. From symmetry exclusion to a quantitative tube

For increasingly arranged u with N=1 set

\[
 v_i=(u_i-u_{9-i})/2.
\]

Then v is increasingly arranged, balanced, reflection-symmetric, and
||v||_2<=1: it is the Euclidean orthogonal projection onto the
antisymmetric subspace. Moreover ||u-v||_infty=A_infty(u).
For any ordered symmetric z, z_i+z_(9-i)=0, so
|u_i+u_(9-i)|<=2||u-z||_infty. Thus v realizes exactly the distance in
(8), including the optimal bottleneck metric after permutation.

For either symmetric-bound premise in (9), G_kappa(v)<0 when D(v)>0.
When D(v)=0, its nonzero profile has four originals at each of the two
levels and a sole active mass N(v), giving G_kappa(v)=0 directly; at
v=0 the same equality holds. Therefore (7),(21) give, whenever C(u)>=T,

\[
 (T-\kappa)D(u)\le G_\kappa(u)
       \le L_\kappa A_\infty(u)<L A_\infty(u).                 \tag{26}
\]

The first member is positive, hence A_infty>0 and the last strict
inequality is valid. Combining (25),(26) proves (10). For T=24531/1000,

\[
 D\ge\frac{72777961}{33699117816},
\]

\[
 \begin{array}{ll}
 \kappa=24:&
 A_\infty>\dfrac{4293899699}{614072813536000}>1/144000,\\[4pt]
 \kappa=47/2:&
 A_\infty>\dfrac{75034077791}{5459257086192000}>1/73000.
 \end{array}
\]

The larger value is less than1/72000. These rational brackets are exact;
decimal approximations are unnecessary proof premises.

## 8. Reproduction and trust boundary

[verify.py](verify.py) uses standard-library Fraction arithmetic only.
It checks the universal covariance and variance polynomial identities,
the mass derivative numerator, and the general-n sharp-family quadratic
as entire sparse polynomials. The finite eight-variable covariance
certificate supplements the ordinary all-n sum argument; it is not a
sampled proof of the all-n theorem.

Five exact balanced original-root motions, including double originals,
compare two full moving-node differential implementations: automatic
dual-number differentiation of rational companion matrix traces and an
independent Euclid/Newton quotient-gradient calculation. The latter
retains the credited9271 full-node formula

\[
 L(q)=-2n\operatorname{tr}(m q/h')
  -\frac2n\operatorname{tr}(m^2q''/h')
  +\frac2n\operatorname{tr}(m^2h''q'/(h')^2),\quad h=f'/n.
\]

The controls need squarefree h; double originals in the selected controls
still have simple critical roots. The global theorem does not assume h
squarefree: its collision bridge is the ordinary argument in Sections2,3.
Two higher-collision profiles independently check actual critical nodes,
the reciprocal equation and active masses, collapsed-gap zero masses,
total mass and the square sum. All scalar margins and the exact projection
metric are checked. Eleven deliberate mathematical damages and changed,
missing or extra whole expected-fixture fields must be rejected; checks
use explicit exceptions and survive optimized Python.

The checker certifies finite exact algebra and controls. Interlacing,
covariance Cauchy, the infinite collision limit, optimality limit,
norm-ball integration, the universal sign-count argument and the imported
symmetric theorems are ordinary proof obligations, not formalized or
established by running finitely many examples. Whole-projection masses
are retained throughout; no numerical eigenvalue search is a premise.

Reproduce from the repository root:

    env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B round-two/six-sendov-2/spectral-mass-lipschitz/verify.py
    env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B -O round-two/six-sendov-2/spectral-mass-lipschitz/verify.py

No large proof corpus, solver, external matrix package or CAS is needed.
The full expected record is compared, rather than a selected hash field.
Native threads remain one, jobs serial, fixed50-second guard and the
unchanged1CPU2GiB scope. No new resource need or escalation arises.

The useful new campaign frontier is sharp effective mass continuity and
its global symmetric tube. The full asymmetric stationary classification,
nonsymmetric collision optimization, sharp global angular value and the
complex first-power Tang--Zhang endpoint remain open. Historical priority
is not established by the bounded literature/graph intake; classical
methods and prior campaign premises retain explicit credit in
[LITERATURE.md](LITERATURE.md).
