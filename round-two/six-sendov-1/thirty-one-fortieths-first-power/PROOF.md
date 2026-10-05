# six-sendov-1 / researcher: degree-nine annular gap

For every degree-nine complex polynomial whose nine zeros lie in the
closed unit disk, and every marked zero a with

    3/4 <= |a| <= 31/40,

the eight critical points, counted with multiplicity, satisfy

    sum_j 1/|a-zeta_j| > 8 + 1/10000.

A zero denominator means infinity. Both marked endpoints, all original
and critical collisions, arbitrary complex directions and all eight
factors are included. This is an ordinary author proof, unformalized and independently
unreviewed. The finite checker is a source of exact arithmetic evidence;
its success does not formalize the continuum argument. No global first-power theorem or sharp gap is asserted.

The problem remains Conjecture 1.2, lambda=1, in
[Zhang's current primary manuscript](https://arxiv.org/html/2609.19126).
Its quadratic theorem is not a premise. Communication identities are
credited to its Lemma 3.1 and
[Tao's Lemma 6](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/).
The generic centered, contour, mean, radial-product, homothety and
clipping arguments follow the same author's
[39a184 proof, Sections 1a and 5–11](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/three-quarters-first-power/PROOF.md).
All new-band numerical inequalities are paid afresh; no ancestor
annular exclusion, review verdict or peer's angular result is used.

## Communication and normalization

Rotate the marked root to real a in [3/4,31/40], and make p monic.
If p'(a)=0 the asserted sum is infinite. Otherwise put

    q_j=1/(a-zeta_j), r_j=|q_j|, F=sum r_j,
    mu=sum q_j/8=u+iv, w=v^2,
    E=sum |q_j-1|^2, T=sum(r_j-1)^2, Pi=F-8u,
    S=sum|q_j-mu|^2, b=1-a^2.

Every q_j is finite and nonzero. With the other eight original zeros
z_k, integration of p'(z)=9 product_j(z-zeta_j) gives

    O_a(q)=9 integral_0^1 product_j(1-atq_j)dt
          =product_k z_k product_j q_j,
    J_a(q)=integral_0^1 product_j(a+btq_j)dt
          =product_k (1-az_k)/(a-z_k).

The substitutions are z=a(1-t) and z=a+bt/a, respectively;
p'(a)=9/product q_j=product_k(a-z_k) retains the factor nine.
Gauss–Lucas and |z_k|<=1 imply

    r_j>=1/(1+a), |J_a(q)|>=1, |O_a(q)|<=P:=product r_j.

Indeed |1-az|^2-|a-z|^2=(1-a^2)(1-|z|^2)>=0. No converse from these
necessary conditions to original-root feasibility is assumed.
Direct expansions give

    E=T+2Pi=T+2F-16u,
    S=E-8[(1-u)^2+w]=T+2F-8-8(u^2+w).

For an actual F<=8 let lambda=F/8 in (0,1] and form
p_lambda(z)=lambda^9 p(a+(z-a)/lambda). Its zeros and critical points
become a+lambda(z-a), with every multiplicity preserved. Convexity of
the closed disk keeps all nine original zeros inside it. The marked
root stays a, and the new reciprocal sum is F/lambda=8. Thus excluding
actual mass eight excludes every actual F<=8.

## Uniform formal mass-eight alternative

For any formal complex tuple with F=8 and the stated radius floors,
the completed [energy-entry lemma](ENTRY-PROOF.md) proves

    |J_a(q)|>=2199/2200 implies E<51/10.

Its ordinary Hermite–Rolle radial comparison, complex phase loss,
positive reciprocal-series truncation and exponential bound are fully
written there. The new fixed entry cover has 86 closed radial shells,
304 cuts and 390 leaves, including the final short shell through
53816/5041. The entire 1,827,575-byte normal/O entry records agree.
The earlier statement in that frozen entry document that face work was
unfinished describes its saved construction checkpoint.

At mass eight the entry gives u>109/160, and |mu|<=1 gives
w<=1-u^2<=13719/25600. Every tuple needing a face estimate therefore
lies in the closed four-coordinate root

    [3/4,31/40] x [0,51/10] x [109/160,1] x [0,13719/25600].

[FACE_COVER.json](FACE_COVER.json) has 449 strict rational cuts,
450 leaves and 899 reachable nodes. Each split keeps both closed
children with identical uncut coordinates. All 450 leaves have nonempty
necessary enclosures; no empty-cell inference is needed. On each leaf
one of the following whole-box estimates holds strictly:

    |O_a(q)| > product r_j + 1/3100,  or
    |J_a(q)| < 2199/2200.                         (A)

These are uniform formal-tuple estimates, independent of actual
original-root feasibility. The necessary intersections use the two
identities above, Pi>=0, T>=0, centered Jensen and |mu|<=F/8, as
proved in ENTRY-PROOF. They never discard an admitted tuple.

Here are the analytic mechanisms behind the three leaf roles.

For centered z_j=q_j-mu, sum z_j=0 and sum|z_j|^2=S, the retained
elementary symmetric bounds are |e_k(z)|<=c_k S^(k/2), where

    (c_2,...,c_8)=(1/2,151/512,3/16,5/64,1/54,13/4096,1/4096).

Centering gives max|z_j|^2<=7S/8, hence sum|z_j|^4<=25S^2/32 by
concentrating the remaining squared radii; for a largest squared radius
at most S/2 use sum|z_j|^4<=S^2/2. Newton and Cauchy give the second
and third caps, since (453/512)^2>=25/32 and e_3=p_3/3.
For real centered z, e_4=S^2/8-p_4/4 has norm at most 3S^2/32.
The REAL Hilbert symmetric multilinear norm identity, an explicit
external ordinary premise in
[Carando–Rodriguez, Introduction (2)](https://arxiv.org/pdf/1810.09373),
bounds its associated four-linear form by 3/32. After a unit phase
rotation, write complex z=x+iy with X=||x||^2,Y=||y||^2. Its real
quartic expansion is at most (3/32)(X^2+6XY+Y^2)<=3(X+Y)^2/16.
No real, balance, conjugacy or orthogonality restriction is imposed on q.

For orders five through seven, coefficient extraction from
G(s)=product(1+sz_j), followed by squared-factor AM–GM using sum z=0,
gives |G(s)|<=(1+|s|^2 S/8)^4. Optimizing the radius gives
|e_k|^2/S^k<=8^(8-k)/(k^k(8-k)^(8-k)); the squared values for k=5,6,7
are 512/84375,1/2916,8/823543. The displayed rational caps dominate
these values. This credited Roos/Han–Niles-Weed contour estimate is
rederived here, not claimed new. The eighth cap is direct AM–GM.

The complete origin expansion is
product(1-atq_j)=sum_(k=0)^8 e_k(z)(-at)^k(1-at mu)^(8-k).
The first centered term vanishes; all seven orders two through eight
remain. For a leaf a in[A,H], u in[L,U], w in[W_l,W_h], choose

    A_0=min(A,2L/(L^2+W_h)-H,2U/(U^2+W_h)-H)>0,
    beta(u,t)=1-2A_0ut+A_0^2(u^2+W_h)t^2,
    Q(u,t)=1-A_0ut+A_0^2 W_h t^2/[2(1-A_0U)].

Both anchor endpoint signs are checked. Concavity in u and convexity
in a give |1-at mu|^2<=beta and sqrt(beta)<=Q. Either polynomial
Sbar=E_+-8[(1-u)^2+W_l] or Sbar=T_++2F_+-8-8(u^2+W_l) bounds S;
each is used separately with its own positive gates. Even remainder
orders use beta powers, and odd orders additionally use Q and a checked
upper square root of max Sbar. The diagonal integral is
(1-(1-a mu)^9)/(a mu). Bounding its numerator below and its ACTUAL
mean norm above gives the degree-eight whole-u polynomial lower bound.
The additional positive denominator H[u+W_h/(2L)] gives a degree-nine
cleared lower criterion. If its minimum Bernstein control is negative,
divide it by the denominator at L; otherwise divide by its value at U.
This sign-dependent division is essential. All degree-eight/nine
controls, all seven complete 9x10 coefficient matrices, every integral
and their independent multinomial representations are retained.

The actual product cap follows from, for 0<x<=R and R>=1,
log x<=x-1-(x-1)^2/(2R). Its derivative identity is
Rx f'(x)=(x-1)(R-x), for f=x-1-(x-1)^2/(2R)-log x.
Thus P<=exp(-(8-F)-T/(2R)). Each leaf pays both the seven-other-floor
radius cap and the centered radial Cauchy cap. A positive fourth-degree
lower Taylor sum for exp gives an upper rational cap for P. The origin
lower bound exceeds this cap plus 1/3100 on every origin leaf.

Standard polar leaves use the same radial/phase argument as the entry,
with their necessary T interval and Pi>=max(0,F_--8U). Joint polar
leaves retain d=sqrt(T/56) and Pi>=(E_- -56d^2)/2, including its
nonnegative sign gate. The whole 13x19 coefficient matrix and all
thirteen integrals are checked by two representations; all thirteen
Bernstein controls pay the entire closed d interval. Every polar upper
bound is below 2199/2200. The fixed roles are 276 origin, 164 joint
polar and ten standard polar.

[face_fixed.py](face_fixed.py) and its three consecutive 150-leaf shards
reconstruct the ENTIRE geometry and recompute every selected payment
from compact kernels. They never read discovery records, old numerical
exclusions or the nineteen point diagnostics. Whole normal/O records
agree byte for byte; the private fixed-face validation receipt
records their complete comparison, source hashes and specific rejection
checks. Assertion removal supplies no independent mathematical review.

Actual F=8 contradicts (A), because |J|>=1 and |O|<=P. The physical
homothety already handles F<8. It remains to exclude 8<F<=8+epsilon.

## Positive gap without a circular energy premise

Set epsilon=1/10000 and Delta=F-8 in(0,epsilon]. With m_a=1/(1+a),
define h_j=Delta(r_j-m_a)/(F-8m_a) and q'_j=(1-h_j/r_j)q_j.
Then sum h_j=Delta, r'_j>=m_a and sum r'_j=8. Along the straight
radial path q'+v(q-q'), all radii exceed m=40/71, total mass is at most
S_0=8+epsilon, and the full l1 displacement is Delta. No intermediate
tuple is assumed actual.

Differentiating a J factor leaves seven factors whose radii sum is at
most S_0-m. With sigma=(S_0-m)/7, triangle inequality and AM–GM give

    |partial_(q_k)J| <= (7/16) integral_0^1 t[31/40+(7/16)sigma t]^7dt <2/3.

The full eight integral terms and an independent antiderivative agree
in [coupled.py](coupled.py). Therefore |J(q')|>=1-(2/3)epsilon>2199/2200.
The entry now gives E'<51/10 and u'>109/160 BEFORE any origin
derivative is bounded. This places q' in the complete face.

Put R=S_0-7m, u_-=109/160-epsilon/8 and
E_+=51/10+2(R+1)epsilon. On the whole clipping path,
u>=u_- and E<=E_+. For x=at, expansion with a removed slot gives

    sum_(j!=k)|1-xq_j|^2
       <=8-16xu+x^2(E+16u-8),

because 2x Re(q_k)-x^2|q_k|^2<=1. Since x<1, the combined coefficient
of u is nonpositive: substitute its lower bound only in this combined
expression. The exact compensation E_++16u_--8=8+2R epsilon yields

    (1/7)sum_(j!=k)|1-atq_j|^2 <= B(t),
    B(t)=[8-16(3/4)u_-t+(31/40)^2(8+2R epsilon)t^2]/7.

All three positive degree-two Bernstein controls reconstruct B.
Convexity and its two endpoints give 0<B<=8/7. With c=107/100 and
c^2>8/7, squared-modulus AM–GM gives the seven-factor product at most
c B^3, and hence

    |partial_(q_k)O| <=9(31/40)c integral_0^1 t B(t)^3dt <7/5.

All seven signed cubic coefficients, both expansions and the complete
weighted integral are paid. Thus |O(q')-O(q)|<=(7/5)Delta.

Finally P/P'<=A:=(1+epsilon/(8m))^8 by eight-factor AM–GM and
r'_j>=m; P'<=1 since sum r'_j=8. The ORIGINAL inequality |O(q)|<=P
and the derivative bound give

    |O(q')|<=P'+(A-1)+(7/5)epsilon <P'+1/3100.

All nine eighth-power coefficients and both strict clipping losses are
checked. An origin leaf contradicts this bound by (A); a polar leaf
contradicts |J(q')|>=1-(2/3)epsilon>2199/2200. This excludes every
8<F<=8+epsilon and completes the asserted annular gap.

The continuum inequalities, external REAL Hilbert identity and
correctness of exact Python arithmetic remain ordinary trust boundaries.
Normal/O equality and source fingerprints do not formalize those steps.
No original-feasibility converse, quadratic premise, real angular locus,
resource-limited nonexistence, transferred review or pending graph CID
is used. The comparison source commit 39a184 covers only [29/40,3/4].
Its generic method is credited; its numerical exclusion is not an input.
