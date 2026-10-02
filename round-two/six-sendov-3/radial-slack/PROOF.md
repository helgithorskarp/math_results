# Four independent original-root slacks and local Sendov stability

Actual author **six-sendov-3**, role **researcher**, 2026-10-02.
Ordinary analytic proof with exact whole-box arithmetic; unformalized and
independently unreviewed. This extends the published zero-slack complex
result to **all nearby complex polynomials with the same marked root** on
the explicit branch interval. The neighborhood radius remains existential.

## 1. Branch, original-root metric and theorem

Let `e=1/65536`, `rho=1/1024`, `c=cos(pi/9)` and `d=2c^2-1`.
For `0<eta<=e`, set `a=1-eta`. Use the monic actual branch `p_eta` of
[9113](../validated-boundary-branch/PROOF.md), source
`7bb2d1b6cf6cb3b370ad10023bee018128a1b81f`, independently confirmed by
[9174](../../six-reviewer-3/certified-branch-audit/REVIEW.md), source
`737a94a084ef91129443179fdc892fbb12d65b0f`. Its real tuple
`v(eta)=(x,y,T,xi3,xi4,omega)` lies in the radius-rho cube about the
credited exact initial tuple, and

    r=eta x, s=eta y, A=a-r, D=a-s, W=1+eta omega,
    p_eta'(z)=9(z-r)^6[(z-s)^2+eta T], p_eta(a)=0,
    W^2=D^2+eta T, F_eta=6/A+2/W.                     (1)

All `A,D,W,T` are positive. Its nine original roots are simple, exactly
four are unit, and the marked root and four other roots are strictly
inside. The upper unit roots `Z_k^+`, `k=3,4`, have cosines
`t3=-1/2+eta xi3` and `t4=-c+eta xi4`; `Z_k^-` is their conjugate.
The four actual simple original-root continuations near them are labelled
by these neighborhoods for every nearby polynomial, including polynomials
with complex coefficients. Define their independent radial coordinates
and inward slacks by

    alpha_k^±=(|Z_k^±|^2-1)/2, sigma_k^±=-alpha_k^±.  (2)

These are half squared-modulus coordinates of original roots, not critical
radii, reciprocal slacks or formal constraint residuals. For a disk-rooted
polynomial all four sigma are nonnegative.

For each fixed positive eta, the six criticals near r are a separated
cluster of multiplicity six; the two heavy criticals lie near
`s±i sqrt(eta T)` and are separate simple points. Label the small cluster
in any order and write

    zeta_j=eta u_j+i sqrt(eta)h_j, j=1,...,6,
    z=(h,u), z0=(0^6,x(eta)1^6),
    D_eta(p)=||z-z0||^2=sum h_j^2+sum(u_j-x)^2.       (3)

The norm and D_eta are permutation invariant. They do not require analytic
labelling of colliding criticals and are not a coefficient Euclidean norm.

Import the full twelve-coordinate zero-slack theorem
[9225](../complex-sector/PROOF.md), source
`9f8293764732c302d0225150ea018951b14a96db`. In its unique local family
`f_eta(z)` the four original radials are zero, z0 is stationary, and its
least Hessian eigenvalue is the centered-real value lambda_R. In particular

    kappa_12(eta)=lambda_R/(2eta^2),
    1/2-(33/16)eta<kappa_12<1/2-(129/64)eta.          (4)

The sharper real interval in(4) is credited to independent
[review9203](../../six-reviewer-3/centered-sector-audit/REVIEW.md), source
`d623ba67fd42e57067b4e605cf3c0ac2a3ba8bb0`; the underlying real sector is
[9164](../centered-real-sector/PROOF.md), source
`8a29091f0c1fdf3b310c3788987b3441a13fc1d6`. Neither that review nor9174
reviews9225's new complex extension or the present proof. This theorem
uses9225 as a mathematical premise, with its own stated trust boundary.

**Theorem.** For every fixed `0<eta<=1/65536`, the four coordinates(2)
and the twelve free coordinates(3) form a local analytic parameter family
of labelled critical tuples, covering every sufficiently nearby monic
degree-nine polynomial with `p(a)=0`. At the branch, the individual-root
objective derivatives are

    ∂F/∂alpha_k^+=∂F/∂alpha_k^-=-mu_k,
    1/4<mu_k<3, k=3,4.                              (5)

For every `0<=kappa<kappa_12(eta)`, there is a coefficient neighborhood
N_(eta,kappa) of p_eta such that every disk-rooted monic p in that
neighborhood with the same marked root a satisfies

    F_p(a)-F_eta >= kappa eta^2 D_eta(p)
                    +(1/4) sum_(k=3,4; ±) sigma_k^±. (6)

Consequently p_eta is a strict coefficient-local minimum among **all
complex** disk-rooted monic polynomials with that marked root, throughout
the explicit eta interval. The explicit coefficient `kappa=1/4` is valid
at every eta in it, with a pointwise neighborhood. If the feasible local
stability supremum is defined using exactly(6), including its fixed slack
weight1/4, then

    kappa_feasible,1/4(eta)=kappa_12(eta).            (7)

Review9174 already proves `F_eta>8+(181/64)eta` on the same branch
interval. Thus(6) also gives the local first-power surplus
`F_p(a)>8+(181/64)eta+kappa eta^2 D_eta(p)+(1/4)sum sigma`.
The surplus constant is credited to that review, and the neighborhood
restriction is essential.

No supremum attainment is asserted. The coefficient neighborhood, free
coordinate radius and radial radius depend on eta and kappa and are
existential. This does not identify the unrestricted global minimum on
the entire stated interval, give an effective entry criterion or solve
the degree-nine first-power inequality. The limiting multipliers and the
earlier existential-germ slack mechanism retain their prior credit.

## 2. Actual root normal map at fixed positive eta

Use the same heavy moment coordinates as9225. For arbitrary nearby free
h,u and four heavy variables `(y,T,V,M)`, let

    mh=(eta V-sum h_j)/2, q=sqrt(T-mh^2)>0,
    n=(M-sum h_j u_j-2mh y)/2, du=n/q,
    h_+=mh+q, h_-=mh-q, u_+=y+du, u_-=y-du.          (8)

The heavy criticals are `eta u_±+i sqrt(eta)h_±`. Integrate nine times
the eight critical factors from a to obtain a monic polynomial p. At the
branch mh=n=0. For fixed positive eta this represents every nearby heavy
pair with positive imaginary separation: recover y as its real-coordinate
average, T as half its squared h sum, V from the total h sum divided by
eta, and M from the total h*u sum. Formula(8) then recovers the pair.
The six free criticals may collide.

The original roots at the branch are simple. The real analytic root
implicit-function theorem therefore gives nine labelled original-root
continuations as functions of the critical parameters, on some open
product neighborhood. Define the actual four-normal map

    N(z;y,T,V,M)=(alpha_3^+,alpha_4^+,alpha_3^-,alpha_4^-). (9)

The marked root is exactly a by construction. All root derivatives used
below are derivatives of these actual continuations; prescribed moduli
are not assumed to arise from a polynomial.

For any unit original root Z, a real parameter b gives

    Z_b=-p_b(Z)/p'(Z),
    ( (|Z|^2-1)/2 )_b
       =Re(conj(Z) Z_b)=-Re(p_b(Z)/(Z p'(Z))).      (10)

At the real branch, put `X=Z-r`, `Delta=r-s`. The entire anchored
even polynomial identities are

    p_y/eta=qy=-(9/4)(X^8-A^8)
                           -(18/7)Delta(X^7-A^7),
    p_T/eta=qT=(9/7)(X^7-A^7).                     (11)

Indeed differentiating the heavy factor gives
`p'_y/eta=-18X^6(Z-s)=-18[X^7+Delta X^6]` and
`p'_T/eta=9X^6`; integrate with a fixed lower endpoint a. The anchor
constants in(11) are essential. The odd identities credited to9225 are

    p_V/(i eta^(3/2))=qV
       =-(9/8)(X^8-A^8)-(9/7)(r-2s)(X^7-A^7),
    p_M/(i eta^(3/2))=qM=-(9/7)(X^7-A^7).           (12)

They follow by differentiating(8)'s actual heavy factors at mh=n=0.
For the upper roots define two real matrices

    J_k,j=-Re(q_j/(Z_k^+ p'(Z_k^+))), j=y,T,
    O_k,j=Im(q_j/(Z_k^+ p'(Z_k^+)))/sin(theta_k), j=V,M. (13)

Here theta_k is the upper branch phase and its sine is positive. In the
even y,T directions the lower derivatives equal the upper derivatives.
In the odd V,M directions they have opposite signs: the polynomial
partial is i times a real-coefficient polynomial, whose lower evaluation
is i times its conjugate, rather than the conjugate of the entire partial.
Equation(10) gives precisely

    d alpha_k^±=eta J_k d(y,T)
                 ±eta^(3/2)sin(theta_k) O_k d(V,M). (14)

In half-sum/half-difference row coordinates the actual derivative is the
block diagonal matrix `diag(eta J,eta^(3/2)diag(sin)O)`. The complete
four-by-four determinant in the row order(9), column order(y,T,V,M), is

    det D_heavy N
       =4 eta^5 sin(theta3)sin(theta4) det J det O.  (15)

The factor4 arises from undoing both half-sum/half-difference row pairs.

The whole eta/cube exact certificate establishes

    det J>1/16, det O<-1/100, sin(theta_k)>1/4,
    det D_heavy N/eta^5<-1/6400.                    (16)

The odd matrix is the published9225 matrix; its exact entries are
recomputed here with unchanged arithmetic. Its extension to the full
normal map in(14)-(15) includes the lower roots and their signs. All
removed eta factors are nonzero for the fixed positive eta under study.
Thus the real analytic IFT solves the four heavy variables uniquely as
functions of arbitrary nearby `(z,alpha)`.

At alpha0 this is exactly9225's zero-slack family: both constructions
solve the same actual unit-root constraints near the same simple roots,
and local uniqueness identifies their heavy variables and objective.
The two root phases are outputs of actual root continuation. No extra
phase or distance variable is needed for the present four-normal map.

## 3. Individual-root objective derivative and its pair factor

Let `g_eta(z,alpha)` be the exact objective in this family. At z0 before
normal elimination, the six small distances do not depend on y,T,V,M.
The heavy sum is `2[(a-eta y)^2+eta T]^(-1/2)`, and conjugation makes
its V,M derivatives zero at V=M=0. Hence

    F_y/eta=2D/W^3, F_T/eta=-1/W^3, F_V=F_M=0.      (17)

Conjugation at z0 exchanges each alpha_k^+ with alpha_k^- and preserves
F. The two individual gradients in each pair are equal. Define mu by

    J^t mu=(-D/W^3, 1/(2W^3))^t.                  (18)

Then substituting `g_alpha_k^±=-mu_k` into(14) gives(17), while the
odd gradients cancel. Invertibility of the full normal map makes these
the unique objective derivatives. The factor2 in(18) counts the two
individual conjugate roots. It is needed even though alpha in(2)
already contains one half.

The whole-box interval inverse in(18) gives `1/4<mu_k<3`. Every entry,
determinant, right side and resulting weight is regenerated in the
complete expected fixture. This proves(5). The initial formulas, with
their existing credit, are

    J0=[[-3/8,3/14],[-(1+c)/4,(1-d)/7]],
    det J0=3(c+d)/56,
    O0=[[1/8,-1/7],[1/8,-2c/7]], det O0=(1-2c)/56,
    mu3(0)=26/9-2c/9-4c^2/9, mu4(0)=(2c-1)/3.      (19)

These are half the earlier8921 dual weights. The initial values alone
would prove only an existential small-eta statement. The new covered
enclosure applies at every actual branch point in `0<eta<=e`.

## 4. A feasible product neighborhood and the entire inward segment

Fix eta and `kappa<kappa_12(eta)`. The IFT supplies an open parameter
neighborhood of `(z0,alpha0)`. Choose within it a product of a convex
z ball and a convex alpha box around zero. By continuity, shrink it so
that all four individual derivatives satisfy

    -∂g_eta/∂alpha_k^±>1/4                          (20)

throughout it. This is possible because(5) is strict at the center.
Shrink also so that the heavy opening, all critical distances and all
simple original-root continuations remain in their positive domains.
The four inactive unmarked original roots have strictly positive disk
slacks at the branch by9113/9174. Root continuity keeps all four strictly
inside throughout the entire product neighborhood. The marked a is fixed
and strictly inside. For the four remaining roots, the IFT enforces
their actual radials exactly equal to the input alpha.

Consequently the family is disk-rooted throughout the product's region
`alpha<=0` componentwise. For every point in that region, the entire
segment `(z,t alpha)`, `0<=t<=1`, stays in the same feasible region:
the inactive roots remain interior and each active radial is nonpositive.
Integrating(20) along that actual polynomial segment yields

    g_eta(z,alpha)-g_eta(z,0)
       =integral_0^1 sum_j (∂g_eta/∂alpha_j)(z,t alpha)alpha_j dt
       >=(1/4) sum_j(-alpha_j).                    (21)

No independent inward root has been replaced by a conjugate pair or a
single total slack. The segment moves the actual heavy criticals and
original roots determined by the IFT at fixed free z.

By9225, after shrinking the z ball further,

    g_eta(z,0)-F_eta>=kappa eta^2||z-z0||^2.        (22)

Combining(21)-(22) proves the local parameter inequality(6). This step
requires a pointwise continuity radius; the branch cube radius rho and
the determinant estimate(16) do not themselves supply that radius.
Since(4) implies `kappa_12>1/2-33/1048576>1/4`, the same argument gives
the stated explicit coefficient1/4 at every eta, with a pointwise radius.

## 5. Coverage of all nearby polynomials and the sharp feasible supremum

For a fixed positive eta, choose disjoint critical neighborhoods around r
and the two heavy branch criticals. Coefficients of p' depend continuously
on coefficients of the monic polynomial p. Continuity of polynomial root
multisets therefore guarantees six criticals in the small neighborhood,
with algebraic multiplicity, and exactly one in each heavy neighborhood
for all sufficiently close p. After labelling the six in any order, their
normalized coordinates approach z0. The heavy labels are unique and their
positive imaginary separation persists. The moments recovering(8) approach
the four branch variables. Repeated small criticals present no problem:
continuity of the multiset is sufficient; no analytic root selection is
asserted for that cluster.

Restrict to p(a)=0. The monic polynomial reconstructed by integrating
nine times its eight critical factors is exactly p, because the leading
coefficient, derivative and marked anchor agree. The four original-root
labels remain uniquely continued from the simple branch roots, so their
actual alpha also approach zero. Select a coefficient neighborhood small
enough that all these coordinates lie in the product chosen in Section4
and in the uniqueness neighborhood of the four-normal IFT. Thus p agrees
with `g_eta(z,alpha)`'s polynomial. If p is disk-rooted then alpha<=0,
and(6) follows. The norm is invariant under the six arbitrary labels.
This establishes the asserted coverage of all nearby complex polynomials
and the coefficient-local statement.

For the strict minimum choose kappa1/4. Equality in(6) forces z=z0 and
all alpha0; uniqueness of the heavy tail then forces p=p_eta. Multiplying
p by a nonzero scalar would preserve F, which is why the strict statement
is made in the monic space.

Define kappa_feasible,1/4 using the same polynomial neighborhood and metric
as(6). Every coefficient below kappa_12 is admissible by the proof above.
Conversely any such polynomial-neighborhood bound restricts to the genuine
zero-slack family of9225. Continuous dependence of its coefficients on z
puts all sufficiently small z displacements into that neighborhood.
A centered-real direction has Hessian eigenvalue lambda_R and squared
norm given by(3), and hence its quadratic ratio tends to
`lambda_R/(2eta^2)`. All alpha are zero on that family. No proposed
coefficient above kappa_12 can satisfy(6). This proves(7), and keeps the
previous real-eigenvalue and sharp-supremum credit. It does not establish
attainment at the supremum.

## 6. Exact certificate, baseline and trust boundary

[radial.py](radial.py) evaluates the whole rectangle `eta in[0,e]` and
the radius-rho six-variable cube using the unchanged192-bit outward
dyadic arithmetic. The cubic embedding uses160 exact rational bisections.
The positive original-root derivative norm squares and square-root domains
are checked. There is no interval division by eta or a vanishing Jacobian:
the explicit nonzero factors in(14)-(15) are removed analytically.
There are no subdivisions, sample-based coverage or floating predicates.

[metric_controls.py](metric_controls.py) independently multiplies the
literal eight critical factors over Gaussian first-order series at three
positive rational eta. It checks all ten anchored coefficients of each
of the four y,T,V,M partials and both heavy-distance gradients. A separate
first-root calculation checks the actual half squared-modulus metric,
both conjugate signs and the root equation. Direct exact elimination of
a raw four-by-four matrix checks the factor4 in(15); individual-root
dual equations check the factor2 in(18). These60 finite exact controls
corroborate formulas; their universal justification is(8)-(18), not an
inference from those finite parameter choices.

[verify.py](verify.py) checks every one of29 unchanged attributed sibling
source files against byte lengths and SHA256 before importing their code.
The dependency directories are the13-file9225 complex-sector publication
and the16-file9164 centered-real publication. No duplicate kernel is
bundled. It regenerates the entire [expected.json](expected.json), with
11 mathematical damages and four full-fixture damages rejected.
[arithmetic_check.py](arithmetic_check.py) recomputes **every** interval
record entry using Fraction endpoint operations rounded to the same grid.
The equations and source are shared: this is same-author arithmetic
corroboration, not independent mathematical review.

The exact9225 baseline was reproduced this pass before adopting it, yielding
its full canonical record
`99fd2f1e5f07ede188fd855037bb86abd572df524756973ce1e1b2b73c330ca5`.
Reproduction validates a prior premise and is not new research or an
independent verdict. The new radial fixture, normal/O equality, serial
guards and compact expected output are documented in [README.md](README.md)
and [VALIDATION.json](VALIDATION.json).

The root and parameter IFTs, critical-multiset continuity, feasible product
neighborhood and integration/Taylor arguments are ordinary unformalized
analytic bridges. The complete proof here states their hypotheses and
coverage; finite computations do not replace them. The underlying full
complex9225 premise remains independently unreviewed. [8921](../analytic-boundary/PROOF.md)
already used strict slack removal near eta0 in an existential global
minimizer germ. The novelty here is the explicit branch interval, covered
four-normal/individual derivative bounds and their extension of9225's
zero-slack stability to all nearby feasible complex polynomials.

An explicit nonlinear displacement radius, all-competitor entry and the
unrestricted degree-nine first-power endpoint are separate remaining tasks.
Source publication and graph commitment record reproducibility and scope;
they do not add an independent proof audit.
