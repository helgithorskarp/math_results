# six-sendov-1 / researcher: private exact energy-entry reduction

This is a completed ordinary, unformalized and independently unreviewed
**conditional energy-entry lemma**. The proposed annular theorem on
the CLOSED marked band [3/4,31/40] is still UNPROVED: sixteen parent
face boxes remain unpaid after the first bounded repairs. There is no
new source commit or graph contribution for this private study.

For a real a in [3/4,31/40] and eight nonzero complex numbers q_j, put
r_j=|q_j| and suppose

    r_j >= 1/(1+a),       sum r_j = 8.

Define b=1-a²,

    J_a(q) = integral_0^1 product_j(a+b t q_j) dt,
    E = sum_j |q_j-1|²,       T = sum_j(r_j-1)²,
    Pi = sum_j(r_j-Re(q_j)).

Then the fresh exact entry certificate proves

    |J_a(q)| >= 2199/2200  ==>  E < 51/10.

All eight factors, repetitions, arbitrary complex phases, both marked
endpoints and every closed cell boundary are included. This is a lemma
on formal reciprocal tuples satisfying the stated conditions. It does
not infer original-root feasibility from those conditions.

The communication identities and problem context are credited to
[Zhang, Lemma 3.1 and Conjecture 1.2](https://arxiv.org/html/2609.19126)
and [Tao, Lemma 6 and Conjecture 19](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/).
The current primary article proves the quadratic case; it still states
the first-power endpoint as a conjecture. The radial/phase/closed-cover
method is credited to our own earlier
[39a184 ordinary proof, Sections 3–4](https://github.com/helgithorskarp/math_results/blob/39a184ba1b80329ae027d5c2e05b0f9d232e18fe/round-two/six-sendov-1/three-quarters-first-power/PROOF.md).
Every numerical payment here is new. The present entry has no ancestor
cover or generated corpus as a runtime input.

## Radial and phase inequalities

Direct expansion gives E=T+2Pi, with Pi>=0. Set m=40/71. The stated
per-a floors imply r_j>=m. Writing x_j=r_j-m>=0 and X=sum x_j=8(1-m),
we have sum x_j²<=X², so

    0 <= T <= 56(1-m)² = 53816/5041.

In particular d=sqrt(T/56)<=31/71<1.

Let e_j=r_j-1. Then sum e_j=0, sum e_j²=56d² and e_j<=7d: for a
positive e_j the other seven sum to -e_j, and Cauchy–Schwarz gives
T>=e_j²+e_j²/7. For B>0,y>=0 with B-yd>0 and every B+y e_j>0,

    product_j(B+y e_j) <= (B+7yd)(B-yd)^7.                 (1)

Here is the interpolation proof. For T>0,y>0 let f(x)=log(B+yx),
and take the quadratic Q which agrees with f and f' at -d and with f
at 7d. Its Hermite remainder is

    f(x)-Q(x) = f'''(xi)(x+d)²(x-7d)/6 <= 0

on the positive-factor domain x<=7d, because f''' is positive. The
remainder follows by subtracting a suitable multiple of
(x+d)²(x-7d) and applying Rolle's theorem three times, including the
derivative zero at -d. Since sum e_j=0 and sum e_j²=56d², sum Q(e_j)
equals Q(7d)+7Q(-d)=f(7d)+7f(-d). Exponentiation proves (1). The
cases T=0 or y=0 follow directly.

For B=a+bt,y=bt all radial factors are positive. The exact identity

    |a+bt q_j|²=(a+bt r_j)²-2abt(r_j-Re(q_j))

and log(1-x)<=-x give, if e_j<=D and C_D=B+btD,

    product_j |a+bt q_j|
      <= (B+7btd)(B-btd)^7 exp(-abt Pi/C_D²).             (2)

Indeed the logarithmic loss for the jth modulus is at least
abt(r_j-Re(q_j))/(a+btr_j)², which is at least the same numerator
divided by C_D². A vanishing complex factor gives (2) directly;
t=0 follows by evaluation. No phase is discarded.

## Entire rational box bound

For a closed box a in [A,H] and T in [L,U], define

    b_- = 1-H²,       b_+ = 1-A²,
    a_* = min(A(1-A²), H(1-H²)),       c = A+1-A²-H,
    delta = floor(1024 sqrt(L/56))/1024,
    D = min(ceil(256 sqrt(7U/8))/256, 8-7/(1+H)-1),
    Bhat(t)=H+ct,       Chat(t)=H+b_+(1+D)t.

The maximum e_j<=sqrt(7T/8) follows from the preceding Cauchy bound;
e_j<=8-7/(1+a)-1 follows from all seven other per-a floors. Thus D
bounds every e_j on the entire box. Every rational square floor/ceiling
is checked by both adjacent-square comparisons in the executable.

The chord identity

    H+ct-[a+(1-a²)t]
      = (1-t)(H-a)+t(a-A)(a+A-1) >= 0

pays the marked-coordinate majorant. Concavity of a(1-a²) pays a_*.
All signs D>=0 and c-b_-delta>0 are checked on each complete box.
For phi(x)=(1+7x)(1-x)^7, its logarithmic derivative is
-56x/[(1+7x)(1-x)]<=0 on [0,1). Consequently the radial factor in
(2) is at most

    R_L(t)=[H+(c+7b_-delta)t][H+(c-b_-delta)t]^7.          (3)

To see this without an unproved mixed monotonicity claim, write the
radial factor as B^8 phi(btd/B). We have B<=Bhat and
btd/B>=b_-t delta/Bhat, and both arguments lie in [0,1). Apply the
decrease of phi first and then the increase of the positive eighth
power.

Put M_C=Chat(1) and nu=b_+(1+D)/M_C. Its sign 0<=nu<1 is checked.
The positive reciprocal series about t=1 gives

    G_2(t)=M_C^-2 sum_(n=0)^4 (n+1)nu^n(1-t)^n
          <= Chat(t)^-2.

Under E>=51/10, Pi=(E-T)/2>=P=max(0,(51/10-U)/2). Thus the exponential
argument in (2) is at least K(t)=a_* P t G_2(t)>=0. First decrease
that argument to K; then use exp(-K)<=1-K+K²/2. The latter follows
because the difference has value and first derivative zero at zero,
and second derivative 1-exp(-K)>=0. No monotonicity of the quadratic
in K is needed. Triangle inequality and (2)–(3) yield

    |J_a(q)| <= integral_0^1 R_L(t)(1-K(t)+K(t)²/2)dt.    (4)

The integrand is a rational polynomial of degree at most eighteen.
Each payment checks ALL nineteen coefficients by direct convolution
and by a separate binomial radial expansion with all ordered kernel
pairs. Its integral is checked coefficientwise and independently in
the beta-integral basis. Signed coefficients are all retained.

## Complete new closed entry certificate

[ENTRY_COVER.json](ENTRY_COVER.json) begins with ALL86 consecutive
closed T shells [i/8,min((i+1)/8,53816/5041)], i=0,...,85, each over
the full [3/4,31/40] marked interval. Every strict rational cut retains
both closed children and every uncut coordinate. The fixed tree has
304 cuts,390 leaves,694 reachable nodes, maximum depth nine. Both
endpoints and the short final radial shell are included.

[entry_fixed.py](entry_fixed.py) reconstructs that entire tree from
the compact geometry and pays every leaf afresh using (4). It checks
unique canonical rational nodes, all closed children, full reachable
census and every positive leaf margin below2199/2200. No discovery
record, old numerical exclusion or old EXPECTED file is loaded.

The ENTIRE normal and optimized records agree:1827575 bytes,
SHA2567d27ef45e1581ed76c493eb2805ba20777750179c71ca010a0626f6b0a8c2de3.
The smallest exact margin is retained in both records; its decimal
display is approximately9.36e-6 and is not used in any comparison.
Runs took7.4464 and7.3667 seconds, maximum25784KiB, under the unchanged
45-second guard, native threads1 and one serial intensive job. Hence
(4) is strictly below2199/2200 on every closed cell, proving the lemma.
This is ordinary exact arithmetic and an ordinary analytic proof;
Python is not a proof assistant and no independent review is claimed.

## Why the two smaller entry thresholds were abandoned

At a=31/40 take q=(1543/500,351/500,...,351/500), seven equal small
entries. The exact diagnostics in
[../entry_obstruction.py](../entry_obstruction.py) check

    F=8,       E=T=155407/31250 > 49/10 > 47/10,
    J=167886122981060757966678840694385802293890238737 /
      167772160000000000000000000000000000000000000000 > 1.

All eight radii exceed40/71, and the induced criticals are
27833/61720 and seven copies of -9119/14040, strictly inside the unit
disk. Literal eight-factor products and independent one-large/seven-small
binomial products agree in all nine J and all nine O coefficients.
Thus even adding the critical-disk condition does not make a J-only
formal entry threshold47/10 or49/10 possible on the proposed band.

The same full calculation pays |O|-product r_j>0, with

    O=27239418299176287908172768798428313 /
      25600000000000000000000000000000000,
    |O|-product r_j=20602053741529849348310803998428313 /
      25600000000000000000000000000000000 > 0.

The original-polynomial O condition is therefore violated. This is
an obstruction to those formal entry relaxations, not a counterexample
to the first-power inequality. No original-root feasibility converse
or resource-limited nonexistence conclusion is used. ENTIRE normal/O
five-tuple records agree,8958 bytes,
SHA256672587c13c003d68b088a57f8dc92128046e90b1bce8991d36cbc625a189ed41.

## Remaining face work and licences for exact intersections

For mass8, u=Re(sum q_j/8) obeys E=T+16-16u, so the entry lemma gives
u>109/160. Triangle inequality gives |sum q_j/8|<=1; writing
w=Im(sum q_j/8)² yields w<=1-u²<=13719/25600. Thus every relevant tuple
is contained in the tighter closed face root

    [3/4,31/40] x [0,51/10] x [109/160,1] x [0,13719/25600].

The fresh full clipping kernel pays J derivative<2/3, O derivative<7/5
and the entire eighth-power product-ratio losses for EPS1/10000,
conditionally on this entry and a subsequently completed face proof.
Its normal/O3716-byte records agree, SHA256
167fe0803719fb6e903385bda2aff95515fab06cb9b8d08b2c419e4ae2a643c3.
This conditional payment does not prove the annular theorem.

The368-leaf face diagnostic paid316 leaves. Of the52 unpaid parents,
first closed bisections paid36 parents; sixteen remain. All matrices,
integrals, unsuccessful alternatives and unpaid geometric boxes are
kept in private scratch records. The selected36 bisections use no empty
necessary enclosure. Further refinements and final proof/source checks
remain required.

For possible future exact empty-cell proofs, every intersection in
core.enclose has a direct necessary licence. With a generic surrounding
box E in [e_l,e_h], F in [f_l,f_h], u in [u_l,u_h], w in [w_l,w_h],
where 0<=u<=1, the identities E=T+2F-16u and Pi=F-8u>=0 give

    u<=f_h/8,       u>=f_l/8-e_h/16,
    F>=8u_l,       F<=8u_h+e_h/2,
    E>=2max(0,f_l-8u_h).

Jensen gives E>=8[(1-u_h)²+w_l] and
w<=e_h/8-(1-u_h)². Triangle inequality gives
w<=(f_h/8)²-u_l². These are intersections which contain every tuple
previously admitted by the necessary conditions. Repeating them four
times makes no fixed-point completeness claim. A reversed resulting
interval is an exact contradiction to those necessary conditions.
The additional T lower/upper intervals follow from the same energy
identity, radial Cauchy and the eight radius floors. A disjoint pair
is likewise an analytic contradiction. A failed sufficient estimate,
timeout, solver status or exhausted call cap is never such a proof.

All earlier published/frozen sources and the three original pending
graph packets remain separate. The latest published own-band
claim is39a184 on [29/40,3/4]; its earlier independent review context
does not transfer to this private child.
