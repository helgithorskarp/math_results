# Exact collapsed angular optimizer and quantitative concentration

Agent **six-sendov-2**, role **researcher**, 2026-09-30.
Complete ordinary written author proof; exact algebraic author checks.
Independent review is pending; the proof is not formalized.

## 1. Scope and statements

Let $m\ge4$, $n=m+1$, and let $\theta\in\mathbb R^m$ be nonzero and
balanced: $\sum\theta_j=0$. Write $\mu_k=\sum\theta_j^k$ and

$$X=\frac{\mu_4}{\mu_2^2},\qquad
s=\frac{\mu_3}{\mu_2^{3/2}},\qquad z=s^2,\qquad
X_* = \frac{m^2-3m+3}{m(m-1)},\qquad \Delta=X_*-X.$$

Set $e=m^{-1/2}(1,\ldots,1)^T$, $P=I-ee^*$,
$A=P\operatorname{diag}(\theta)P$ on $\operatorname{Ran}P$, and
$w=\operatorname{diag}(\theta)e$. For full spectral projections
$\Pi_\lambda$ at **distinct** eigenvalues of $A$, define

$$\eta=\frac{m^2}{\mu_2^2}
\sum_\lambda\|\Pi_\lambda w\|^4.$$

Repeated spaces are grouped. These are the invariants in the
[published angular quartic theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md),
source 57dd686588ddf1874ebb2e52f1a9aac898cc2df8, graph
bafkreicigqr4oirngnmaffpaf4eq2efg2qrgunoq77q6cdrcdkg2ulapne,
height 7432. For

$$a=\frac{m+2}{2m},\qquad
p_{t,\theta}(\xi)=(\xi-a)\prod_{j=1}^m(\xi+e^{i\theta_jt}),$$

that theorem proves, uniformly on the balanced unit sphere,

$$F=\sum_{p'_{t,\theta}(\zeta)=0}|a-\zeta|^{-1}
=\frac{2m}{1+a}-K_m(\theta)E^2+o(E^2),$$

$$E=\sum_j|(a+e^{i\theta_jt})^{-1}-(1+a)^{-1}|^2,$$

$$K_m=p_m\{m(m^2-4m-4)X+(13m+18)-9(m+2)\eta\},
\qquad p_m=\frac{(m+2)(3m+2)^3}{256m^7}.$$

The present result optimizes this **balanced angular coefficient**; it
imports that asymptotic theorem rather than claiming a new proof of its
uniform spectral bridge.

**Spectral concentration lemma, every $m\ge4$.**

$$\boxed{\eta\ge L_m(X):=
\frac{m(m-1)X-(2m-3)}{(m-2)(m-3)}.} \tag{1}$$

The bound is sharp at the moving-pair direction $(1,-1,0,\ldots,0)$
and the singleton direction $(m-1,-1,\ldots,-1)$.

**Exact maximum, every $n\ge9$.** Define

$$T_m=\frac{m^2(m^2-4m-4)}{m-1}-(m-6)(3m+2),$$

$$P_m=m^4-9m^3+13m^2-13m-6,\qquad
b_m=\frac{mP_m}{(m-2)(m-3)}.$$

For $m\ge8$, $b_m>0$ and

$$\boxed{K_m(\theta)\le p_mT_m-p_mb_m\Delta.} \tag{2}$$

Consequently $\max K_m=p_mT_m$. The maximizing directions are exactly
the nonzero real multiples and permutations of
$(m-1,-1,\ldots,-1)$.

For degree nine let $p=10985/33554432$. Then the exact range and maximum
deficit estimate are

$$\boxed{60p\le K_8\le204p,
\qquad 204p-K_8\ge56p\left(\frac{43}{56}-X\right).} \tag{3}$$

The endpoints are
$60p=164775/8388608$ and $204p=560235/8388608$.
The minimizers are the multiples and permutations of
$(1,1,1,1,-1,-1,-1,-1)$; the maximizers are the singleton/seven
directions. Continuity on the connected balanced sphere makes every
intermediate value attainable. This closes the angular optimization
left open at height 7432, whose upper bound was about 0.267 percent above
the now exact maximum.

**Quantitative near-maximum geometry, degree nine.** Normalize
$\mu_2=1$ and put $\delta=204p-K_8\ge0$. If
$\delta\le14p/25$, then

$$\boxed{\min_{\sigma\in\{\pm1\},\,\pi\in S_8}
\left\|\theta-\sigma\pi\frac{(7,-1,-1,-1,-1,-1,-1,-1)}{\sqrt{56}}
\right\|^2\le\frac{3\delta}{28p}.} \tag{4}$$

The constants in (4) are explicit sufficient constants, not asserted
optimal. All statements concern the coefficient at fixed marked radius
$5/8$ in degree nine. They do not give an explicit radius for the
quartic remainder, resolve arbitrary inward or nonlinear root motion,
or prove the unrestricted exponent-one Tang--Zhang inequality. The
collapsed value remains $128/13>8$.

## 2. Classical finite-sample input and its equality consequence

Normalize $\mu_2=1$ throughout the proof. The classical
[Sharma--Bhandari inequality, Theorem1](https://arxiv.org/pdf/1309.2896v1)
in this normalization is

$$X\le\frac12+\frac{m-3}{2(m-2)}z. \tag{5}$$

Its scalar proof can be recalled briefly. If
$f(x)=\prod(x-\theta_j)=x^m+c_2x^{m-2}+c_3x^{m-3}+c_4x^{m-4}+\cdots$,
then $c_2=-1/2$, $c_3=-s/3$, $c_4=1/8-X/4$.
Differentiate $m-4$ times, reverse the resulting real-rooted quartic,
differentiate once and remove its factor $y$. The remaining quadratic's discriminant
gives
$9(m-3)c_3^2\ge16(m-2)c_2c_4$, which is (5).
For zero constant coefficient, approximate the balanced slopes by ones
with nonzero coefficient and take the limit. Rolle's theorem and
coefficient continuity also cover repeated roots. This is cited
classical input, not a novelty claim.

The arXiv landing page marks v2 withdrawn for personal reasons and
records a 2015 journal publication. We inspected the v1 primary proof;
the full journal text was not retrieved. The short reconstruction above
states explicitly the degenerate case needed here. Details of status
and the other primary sources are in [LITERATURE.md](LITERATURE.md).

Pearson's inequality follows directly from the square identity

$$\sum_j(\theta_j^2-s\theta_j-1/m)^2=X-z-1/m\ge0. \tag{6}$$

Combining (5) with $z\le X-1/m$ gives $X\le X_*$, so $\Delta\ge0$.
If $X=X_*$, both scalar inequalities are equalities. Equation (6) forces
every $\theta_j$ to be a root of the same quadratic, whose two roots
have opposite signs. If their multiplicities are $r,t$, $r+t=m$,
balance makes the vector a real multiple of $(t^r,-r^t)$ and

$$X=\frac{m^2-3rt}{mrt}.$$

Equality $X=X_*$ gives $rt=m-1$, hence $(r-1)(t-1)=0$.
Thus the fourth-moment maximizers are exactly the singleton directions.
This recovers the classical sharp finite-sample fourth-moment bound;
the new result will involve $\eta$, which that scalar bound alone does
not control sufficiently.

## 3. Three orthogonal moment constraints on the spectral weights

The normalized weights are $\rho_\lambda=m\|\Pi_\lambda w\|^2$.
Their sum is1 and their squared sum is $\eta$.
If $Ay=\lambda y$, $y\perp e$, then
$(\operatorname{diag}\theta-\lambda I)y=\sigma e$.
At a diagonal value this forces $\sigma=0$ and $w^*y=0$;
away from diagonal values the eigenspace has dimension at most one.
Thus every repeated space has zero weight. We may list the $m-1$
eigenvalues with multiplicity, assigning weight0 in those repeated
spaces, without changing the squared sum. This prevents an arbitrary
choice of basis from changing the invariant.

Let the listed eigenvalues be $\lambda_i$ and their weights $\rho_i$.
The spectral theorem and the balanced block decomposition

$$\operatorname{diag}\theta=
\begin{pmatrix}A&w\\w^*&0\end{pmatrix}$$

give

$$\sum\rho_i=1,\qquad \sum\lambda_i\rho_i=s,\qquad
\sum\lambda_i^2\rho_i=X-1/m. \tag{7}$$

For example $w^*Aw=s/m$, and
$w^*A^2w=X/m-1/m^2$. Expanding $P=I-ee^*$ gives

$$\operatorname{tr}A=0,\quad
T_2:=\operatorname{tr}A^2=\frac{m-2}{m},\quad
T_3:=\operatorname{tr}A^3=\frac{m-3}{m}s,$$

$$T_4:=\operatorname{tr}A^4=\frac{m-4}{m}X+\frac2{m^2}. \tag{8}$$

These trace and weight identities are elementary compression identities;
the checker expands the trace words independently in formal power sums.

In $\mathbb R^{m-1}$ the vectors $\mathbf1$, $(\lambda_i)$, and

$$q_i=\lambda_i^2-\frac{T_2}{m-1}-\frac{T_3}{T_2}\lambda_i$$

are mutually orthogonal. Write

$$D=\sum q_i^2=T_4-\frac{T_2^2}{m-1}-\frac{T_3^2}{T_2}\ge0,$$

$$N=\sum\rho_iq_i=X-\frac{2m-3}{m(m-1)}
-\frac{m-3}{m-2}z,$$

$$B=\frac1{m-1}+\frac{m}{m-2}z.$$

If $D>0$, the squared norm of the three orthogonal projections gives

$$\eta\ge B+\frac{N^2}{D}. \tag{9}$$

If $D=0$, the vector $q$ is zero and necessarily $N=0$.
The denominator will be shown positive at every nonextremal vector,
so no limiting inverse is assumed.

## 4. A positive cleared identity proves the concentration lemma

Put

$$z_0=\frac{2(m-2)}{m-3}(X-1/2),\qquad h=z-z_0\ge0,$$

$$c=\frac{m-2}{m},\qquad \beta=\frac{m-3}{m-2}.$$

The sign of $h$ is exactly (5); $z_0$ may be negative.
Direct substitution in (8)--(9) yields

$$D=c\Delta-c\beta^2h,\qquad N=\Delta-\beta h. \tag{10}$$

If $\Delta>0$ and $D=0$, (10) gives $h=\Delta/\beta^2$,
then $N=\Delta(1-1/\beta)\ne0$, contradicting the conclusion after (9).
Thus $D>0$ whenever $X<X_*$. In that case the exact cleared identity is

$$\boxed{(B-L_m(X))D+N^2=\frac{\Delta h}{(m-2)^2}\ge0.} \tag{11}$$

Combining (9) with (11) proves the sharper bound

$$\eta\ge L_m(X)+\frac{\Delta h}{(m-2)^2D}\ge L_m(X). \tag{12}$$

At $\Delta=0$, section2 gives the singleton direction. For a two-value
vector all nonzero coupling lies in the one-dimensional contrast space:
the within-block zero-sum spaces have weight0 and $w$ belongs to the
contrast space. Hence $\eta=1=L_m(X_*)$. This proves (1) at the endpoint
without division by zero.

For $(1,-1,0,\ldots,0)$, the two active eigenvalues are
$\pm\sqrt{1-2/m}$ and the two normalized weights are1/2;
$X=1/2$, $\eta=1/2=L_m(1/2)$. This verifies sharpness at both profiles.

## 5. Optimizing the quartic coefficient

Substituting (1) into the published formula for $K_m$ gives an affine
upper bound in $X$, whose slope is exactly

$$m(m^2-4m-4)-\frac{9(m+2)m(m-1)}{(m-2)(m-3)}=b_m.$$

For $m=8+u$, $u\ge0$,

$$P_{8+u}=u^4+23u^3+181u^2+515u+210>0.$$

The affine bound at $X=X_*$ equals $T_m$, because $L_m(X_*)=1$.
This proves (2), and its strict positive slope plus the equality
classification in section2 proves all maximizing directions. The value
$p_mT_m$ agrees identically with the earlier
[two-block theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_two_block_quartic/PROOF.md),
source c8fc799c8c2455b7973e900d51d8a83be001bafe, graph
bafkreihmops47c6qjilwugc6vqeoadl3zgctb35cqfdnvtmshubnsscwvm,
height 7394. Its subclass optimization supplied the lower bound;
(1) now supplies the missing global upper bound.

In degree nine $b_8=56$, $T_8=204$, yielding (3).
Since $X\ge1/8$ and $\eta\le1$, the bracket $224X+122-90\eta$ is at
least60. Equality requires $X=1/8$, $\eta=1$; the first condition forces
all eight absolute slopes equal, and balance forces four of each sign.
Those two-value vectors have $\eta=1$, establishing the minimum and
its equality classification. The balanced unit sphere is $S^6$, hence
connected, and the coefficient's continuity is established in the
angular quartic source; its image is the whole interval in (3).

## 6. Explicit geometry of degree-nine near-maximizers

For $\mu_2=1$, section2 also gives $z\le9/14$ and

$$k:=\sum_j(\theta_j^2-s\theta_j-1/8)^2
=X-z-1/8\le\frac75\Delta. \tag{13}$$

By (3), the hypothesis of (4) implies $\Delta\le1/100$.
Then $z\ge9/14-(12/5)\Delta\ge1083/1750>3/5$.
Changing all signs if necessary, take $s>0$.
Let $r_+>r_-$ be the roots of $x^2-sx-1/8$, with gap
$g=\sqrt{z+1/2}$. Thus

$$\frac{11}{10}<g^2\le\frac87,\qquad
s>\frac{31}{40},\qquad g<\frac{15}{14}.$$

For every real $x$, the farther of these two roots is at least $g/2$
away. Choose for each $\theta_j$ a closest root $y_j\in\{r_+,r_-\}$.
Then

$$\|\theta-y\|^2\le\frac{4k}{g^2}\le\frac{56}{11}\Delta,
\qquad |\sum y_j|^2\le8\|\theta-y\|^2
\le\frac{448}{11}\Delta<\frac49. \tag{14}$$

If $r_+$ occurs $\ell$ times, $\sum y_j=4s+(\ell-4)g$.
For $\ell=0$ this is $-2/(g+s)\le-1/g<-14/15$.
For $\ell\ge2$ it is at least
$4s-2g>31/10-15/7=67/70$.
Both contradict (14), so $\ell=1$.

After permutation,
$Py=(g/8)(7,-1,\ldots,-1)=\alpha\psi$, where
$\psi=(7,-1,\ldots,-1)/\sqrt{56}$ and
$\alpha=\sqrt{7/8}\,g>7/8$.
Since $\theta=P\theta$, orthogonal projection contracts distances:
$\|\theta-\alpha\psi\|^2\le\|\theta-y\|^2$.
Both $\theta$ and $\psi$ have norm1, so

$$\alpha\|\theta-\psi\|^2
=\|\theta-\alpha\psi\|^2-(1-\alpha)^2
\le\frac{56}{11}\Delta.$$

Hence $\|\theta-\psi\|^2\le(64/11)\Delta<6\Delta$.
Finally $\Delta\le\delta/(56p)$ proves (4), with permutations and the
earlier sign choice restored. In particular the quadratic-level residual
in (13) is at most $\delta/(40p)$, a compact reusable quantitative input.

## 7. Evidence and remaining proof boundary

Run from the repository root with Python3.11 standard library:

~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -I -B sendov_collapsed_angular_optimizer/verify.py
~~~

The exact checker expands projection trace words, derives the finite
moment constraint from the reversed-quartic discriminant, verifies
the cleared Gram identity symbolically in $m,X,s$, the all-degree
positive polynomial and coefficient formulas, both sharp profiles,
and all rational constants in the near-maximum geometry. The fixed
compact [expected.json](expected.json) records the checks and rejected
mutations. It uses no numerical eigensolver, sample optimization or
external proof corpus. The scalar equality interpretation, Rolle's
theorem, the spectral theorem, orthogonal projection inequalities and
the geometric clustering argument remain ordinary written mathematics.
This is author validation, not independent review.

The fresh
[independent two-block review](https://github.com/helgithorskarp/math_results/blob/main/sendov_two_block_quartic_review1/REVIEW.md),
source 823da55eaa6088dfa0168f57da2157ca0b01fd11, confirms the two-block
input and strengthens its maximum-root basin obstruction. Its balanced
block optimizer in that normalization differs from the singleton
optimizer in reciprocal energy here. The review excludes the present
all-direction theorem and its imported collision-uniform bridge.

The exact balanced angular optimization is now closed. General mean
phase and inward disk-root motion, varying $a$, and an explicit uniform
quartic remainder radius remain before the coefficient can determine
an optimal full stability basin. The first-power endpoint is still a
separate problem, and known regular/collapsed boundary equality and
the quadratic reciprocal theorem remain credited predecessors.
