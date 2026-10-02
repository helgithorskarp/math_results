# Reflection-symmetric octic angular profiles lie below 24

Actual author **six-sendov-2**, role **researcher**, 2026-10-02.
Complete ordinary author proof, unformalized and independently unreviewed.
Exact identities and finite sign certificates are checked with rational
arithmetic. This concerns the real-original-root angular frontier
associated with degree-nine complex first-power Sendov research.

## 1. Functional and statement

Let u be a nonzero balanced vector in R8, and put

\[
 e=\mathbf1/\sqrt8,\quad P=I-ee^T,\quad
 H=P\operatorname{diag}(u)P|_{e^\perp},\quad
 N=\sum u_i^2,\quad D=\sum u_i^4-N^2/8.
\]

For full orthogonal projections onto the distinct eigenspaces of H, set

\[
 m_\lambda=\|\Pi_\lambda u\|^2,\qquad
 \eta=\sum_{\lambda\ {\rm distinct}}m_\lambda^2,\qquad
 C=(N^2-\eta)/D.                                      \tag{1}
\]

These are the credited compression masses and angular ratio of
[7432](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md)
and [8753](../angular-three-level-transition/PROOF.md).
Use the continuous extension C=16 when D=0, as established in8753.
Always group the entire eigenspace at a collision.

**Theorem.** If the multiset of original coordinates u is invariant under
u→−u, then

\[
                         \boxed{C(u)<24.}               \tag{2}
\]

Moreover, no reflection-symmetric profile with eight distinct original
coordinates is stationary even within the reflection-symmetric,
balanced fixed-N coefficient chart. The theorem has no small-D or
high-C assumption.

Since8753 proves an attained global maximum C*>=c3>24.53389668,
every global angular maximizer is asymmetric. In fact every profile
with C>=24 is asymmetric. The symmetric maximum is strictly less than24
by compactness, but this proof does not determine that maximum or give
a sharp symmetric equality classification.

This closes the even subcase left after the
[heat-tangent rank reduction9353](../heat-tangent-rank/PROOF.md).
The rank lemma is credited context, not a premise of (2).
The unrestricted angular question C*=c3, nonsymmetric all-distinct
stationary candidates, and the actual complex first-power endpoint
remain unresolved.

## 2. Eight distinct originals: the exact centered functional

Scale N to1. An even octic with eight distinct real originals is

\[
 f(z)=p(z^2),\qquad p(x)=x^4-x^3/2+a x^2+b x+c.
                                                               \tag{3}
\]

The four original square-roots of p are distinct and positive, with
sum1/2. Consequently

\[
             0<a<3/32,\quad b<0,\quad c>0,\quad D=3/8-4a>0.
                                                               \tag{4}
\]

The strict upper bound follows from the elementary symmetric sum of
four positive numbers with fixed sum. Positive simple roots form an
open set in the three free coefficients a,b,c. Thus a local symmetric
maximum at such a profile must have all three partial derivatives zero.
There is no feasibility restriction on sufficiently small two-sided
variations in this open chart.

Write h=f'/8=z r(z²), where

\[
                   r(x)=x^3-3x^2/8+(a/2)x+b/4.           \tag{5}
\]

Interlacing gives three distinct positive roots of r. At the central
critical point and at a positive critical square x, the simple
compression mass formula m=−8f/h' gives respectively

\[
 m_0=-32c/b,\qquad m(x)=-4p(x)/(x r'(x)),\qquad
 \eta=m_0^2+2\sum_{r(x)=0}m(x)^2.                        \tag{6}
\]

The same formula, local constant-term feasibility and the complete
moving-node gradient are credited to
[9271](../constant-term-angular-reduction/PROOF.md).
We derive this subcase directly by traces over the cubic quotient;
no critical nodes are frozen while a or b varies.

Define

\[
\begin{split}
 L={}&256a^3-18a^2+432ab+864b^2-27b,\\
 H_0={}&512a^3-36a^2+736ab+1344b^2-45b,\\
 U={}&16a^2-a+6b,\\
 W={}&4096a^4-512a^3+7680a^2b+18a^2-816ab+1440b^2+27b,\\
 J={}&8192a^4-1024a^3+13312a^2b+36a^2-1376ab+2496b^2+45b,\\
 V_0={}&8192a^4+13312a^2b-36a^2+96ab+5184b^2-45b.
\end{split}                                                  \tag{7}
\]

Here disc(r)=−L/512>0. Expansion of (6) gives the universal identity

\[
          \eta=\frac{768H_0}{b^2L}c^2-\frac{3072U}{L}c
                        -\frac{W}{2L}.                  \tag{8}
\]

Its quadratic coefficient is strictly positive: it is a sum of
squares of slopes of the affine-in-c masses, including the nonzero
central slope −32/b. Since L<0, this proves H0<0. All displayed
denominators are therefore nonzero on the feasible simple-root chart.

A stationary point must satisfy its constant derivative, hence

\[
 c=c_*=\frac{2b^2U}{H_0},\qquad
 \bar\eta=-\frac{J}{2H_0},\qquad
 \bar C=-\frac{4V_0}{(32a-3)H_0}.                       \tag{9}
\]

The identities WH0+6144b²U²=LJ and 2H0+J=V0 verify the elimination.
We do not assume that c* is a legal positive-root coefficient for
arbitrary a,b. At a hypothetical feasible stationary point it is the
actual coefficient. Since the c derivative vanishes there, derivatives
of the rational expression Cbar are precisely the a,b derivatives of
the original C, by the chain rule.

## 3. Two exact branches, neither stationary

Set A=32a−3, and

\[
 F=4a^2+(15-112a)b,\qquad
 G=4a^2(64a-5)+(208a-15)b.
\]

Direct differentiation gives

\[
          \partial_b\bar C=-\frac{3072FG}{A H_0^2}.     \tag{10}
\]

This is checked as the polynomial identity
V0_b H0−V0 H0_b=768FG.

If F=0, then

\[
 b_F=-\frac{4a^2}{15-112a},\qquad
 \bar C(a,b_F)=-\frac{4(224a+15)}{448a-45}.
\]

On 0<a<3/32, 15−112a>9/2 and 448a−45<−3. Along this branch
Cbar_b=0, so differentiation along the branch gives

\[
       (\partial_a\bar C)_{F=0}
                =\frac{67200}{(448a-45)^2}>0.           \tag{11}
\]

It cannot be a stationary point.

If G=0, the exceptional value a=15/208 is impossible: at that value
G=−20a²/13≠0 independently of b. Otherwise

\[
 b_G=-\frac{4a^2(64a-5)}{208a-15}.
\]

Substitution into the critical cubic discriminant gives

\[
 \operatorname{disc}(r)|_{G=0}
 =-\frac{a^2(32a-3)^2 T(a)}{256(208a-15)^2},\qquad
 T(a)=27648a^2-4960a+225
       =27648(a-155/1728)^2+275/108>0.                  \tag{12}
\]

It is strictly negative throughout (4), contradicting three distinct
real critical square-roots. Thus (10) cannot vanish simultaneously
with the other two coefficient derivatives at any feasible profile.
This proves the interior stationary exclusion on the entire domain.

## 4. A zero-original boundary has C<=20

The following elementary dimension argument applies even without
reflection symmetry. Suppose k>=2 original coordinates are zero, and
let q=8−k<=6 be the number of nonzero coordinates. Balance and N>0
imply q>=2.

The zero-supported vectors with coordinate sum zero form an invariant
zero eigenspace of H of dimension k−1. They are perpendicular to u.
The complementary H-invariant space in e-perp has dimension q, so
at most q distinct eigenspaces have positive mass. Since sum m=N,
Cauchy gives eta>=N²/q. Cauchy on the nonzero originals gives

\[
 D\ge N^2/q-N^2/8,\qquad
 C\le\frac{8(q-1)}{8-q}\le20.                          \tag{13}
\]

D is strictly positive here. This argument uses full eigenspace
projections and remains valid at every critical collision.

## 5. Every nonzero symmetric collision lies below 24

If no original is zero, the even square polynomial has four positive
roots counted with multiplicity. At any original collision a square
root occurs twice. Scaling that root to1 gives the entire collision
boundary, including higher multiplicities, as

\[
           f(z)=(z^2-1)^2(z^2-y)(z^2-z_0),
           \quad y,z_0>0.
                                                               \tag{14}
\]

Set S=y+z0>0, T=yz0>0 and w=1−4T/S² in[0,1). Then

\[
\begin{split}
 h&=f'/8=z(z^2-1)q(z^2),\\
 q(x)&=x^2-(3S+2)x/4+(S+2T)/4,\\
 K&=9S^2-4S+4-32T=(S-2)^2+8S^2w,\\
 V_1&=3S^2-4S+4-8T=(S-2)^2+2S^2w,\\
 N&=2(S+2),\qquad D=V_1/2.
\end{split}                                                  \tag{15}
\]

Except at S=2,w=0, q has distinct positive roots, K,V1>0.
First take generic y,z0 distinct from each other and1. The masses at
the original double pair ±1 vanish. Cancellation in −8f/h' yields

\[
 m_0=\frac{32T}{S+2T},\qquad
 m(x)=-\frac{(x-1)[(2-S)x+2T-S]}{xq'(x)},\quad q(x)=0.
                                                               \tag{16}
\]

Thus eta=m0²+2 sum m(x)². Exact two-node quotient traces give

\[
            24-C=\frac{4S^2\,\mathcal P(S,w)}
                         {(S+2T)^2 V_1 K},              \tag{17}
\]

where the explicit quartic in w is

\[
\begin{split}
\mathcal P(S,w)={}&
 \tfrac14(S-2)^4(5S^2-4S+20)\\
 &+\tfrac12 S(S-2)^2(S+2)(17S^2+16S-20)w\\
 &+\tfrac14 S^2(21S^4+816S^3-744S^2-1344S+848)w^2\\
 &+S^4(-41S^2-184S+356)w^3+26S^6w^4.                \tag{18}
\end{split}
\]

All cancellations are verified universally by multiplication and
clearing denominators. They do not rely on sampled roots.

For S>=2 put Y=S−2. Express P in the degree-four Bernstein basis in w:

\[
 \mathcal P(2+Y,w)=\sum_{j=0}^4 B_j(Y)
                           {4\choose j}w^j(1-w)^{4-j}.
\]

The five polynomials are

\[
\begin{split}
B_0={}&5Y^6/4+4Y^5+8Y^4,\\
B_1={}&27Y^6/8+109Y^5/4+98Y^4+144Y^3+80Y^2,\\
B_2={}&51Y^6/8+95Y^5+1099Y^4/2+1484Y^3
                  +6136Y^2/3+4096Y/3+1024/3,\\
B_3={}&153Y^5/4+753Y^4/2+1252Y^3+1892Y^2+1296Y+320,\\
B_4={}&153Y^4+840Y^3+1856Y^2+1984Y+896.
\end{split}                                                  \tag{19}
\]

Every coefficient is nonnegative. B0>0 for Y>0, and B2,B3,B4
are positive at Y=0. Therefore P>0 for S>=2 except at S=2,w=0,
including w=0 and w=1 with these stated exceptions.

For 0<=S<=2, substitute each rectangle below affinely to[0,1]²
and use the degree-(6,4) tensor Bernstein basis. Every one of the
35 coefficients on each rectangle is nonnegative. The exact minima
are as follows; [expected.json](expected.json) includes all245
coefficients and [verify.py](verify.py) reconstructs the entire
polynomial exactly on every rectangle.

| S interval | w interval | minimum Bernstein coefficient |
|---|---|---|
| [0,1/2] | [0,1] | 30545/1536 |
| [1/2,1] | [0,1/2] | 65/16 |
| [1/2,1] | [1/2,1] | 125/16 |
| [1,3/2] | [0,1/4] | 101/256 |
| [1,3/2] | [1/4,1/2] | 6953/3072 |
| [1,3/2] | [1/2,1] | 5603/960 |
| [3/2,2] | [0,1] | 0 |

The first six rectangles have strictly positive minima. On the last,
the coefficients at indices(0,0) and(0,4) are strictly positive,
so their Bernstein terms ensure positivity for S<2 at every w.
At S=2 the upper certificate (19) supplies positivity for w>0.
The closed rectangles cover the whole remaining range without gaps.
Thus P>0 everywhere with S>0,0<=w<=1 except S=2,w=0.

Formula (17) proves C<24 on the generic collision boundary.
At coincidences y=z0 or y=1 or z0=1, the simple-residue chart may fail,
but full-projection C is continuous. For every nonuniform such point,
the denominator in (17) remains positive, and both sides continue,
still with a strictly positive gap. At S=2,w=0 all four squares equal1;
the credited continuous value is C=16. Hence every nonzero symmetric
collision profile is strictly below24.

## 6. Compactness closes the symmetric case

The reflection-symmetric multiset condition defines a closed subset
of the balanced norm-one sphere. By the continuous extension in8753,
C attains a maximum there. A maximum with eight distinct originals
would be stationary in the open coefficient chart(3), which Sections2–3
exclude. Every remaining profile has an original collision. A zero
original has even multiplicity and is covered by (13); every other
collision is covered by (14)–(19), including the uniform orbit.
Thus that attained maximum is strictly less than24, proving (2).

The proof does not import a prior at-most-four- or at-most-five-level
bound. In particular the six-level paired2+1+1 collision boundary
is proved directly here. No full nonsymmetric collision classification,
quantitative distance from the symmetric locus, or global reduction to
the three-level orbit is obtained.

## 7. Reproducibility and trust boundary

Run from the repository root with Python3.11+ standard library:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B round-two/six-sendov-2/even-angular-exclusion/verify.py

Repeat with -O. Expected whole record SHA256:
9dde6e9a3e4bfd523a6de5be0580a259b1e21171b5db410b6540bdab0076e8b2.
The checker constructs the cubic and quadratic multiplication matrices,
their inverse adjugates, and mass-square traces. It validates all
coefficient, centering, branch and discriminant identities, the entire
seven-rectangle cover, 245 exact lower sign coefficients and the five
upper sign polynomials. An independent seven-node Newton/Euclid
calculation checks eleven concrete examples, including the legal
constant-center benchmark credited to
[9323](../heat-stationary-reduction/PROOF.md).
Seven mathematical damages are rejected; the external expected record
must match in its entirety.

SymPy1.14 assisted private discovery; it is not a published dependency.
The ordinary proof bridges are interlacing, local simple-root
coefficient feasibility, the chain rule at the actual legal center,
full-projection collision continuity, Cauchy and compactness.
These are not formalized by the finite checker. Same-author independent
arithmetic controls are not independent peer review. No solver,
floating-point sign, exhaustive root search, timeout or incomplete
enumeration supplies a proof premise.
