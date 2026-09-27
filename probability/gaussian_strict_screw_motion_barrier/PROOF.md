# An effective R5 barrier after every tight pair is broken

Author proof, 27 September 2026. Independent acceptance and historical
priority are pending. The unrestricted Gaussian-majorisation problem in
R3 remains open. This is a quantitative motion obstruction, not an adverse
Gaussian sign or a new positive geometric class.

## 1. The reference and the new finite neighborhood

Let P,Q be the labelled 24-site source and target of the existing
[two-body screw](../gaussian_two_body_screw_obstruction/PROOF.md), with
[exact coordinates](../gaussian_two_body_screw_obstruction/WITNESS.json).
Write J(u1,u2)=(-u2,u1), C=I-J, and

    b(u)=(u,-|u|^2),       a(v)=(v,(1+|v|^2)/2),
    T a(v)=a(v),           T b(u)=(Ju,1-|u|^2).

The eight B parameters are

    U={0,e1,-e1,2e1,-2e1,e2,-e2,e1+e2}.

The sixteen A parameters are C U together with

    C u +/- (1/4)e_j,      u in {0,e1}, j in {1,2}.

Every cross squared-distance loss is exactly |v-Cu|^2. Within each group
all endpoint distances agree. The two groups affinely span R3. Their
centered scatter matrices have least eigenvalue greater than k=1/16;
the exact leading minors of scatter-minus-kI are positive, as recorded by
the checker. The maximum squared diameter of either full endpoint is
369/4<128, and max_B |b|^2=20<25. These conservative bounds are the only
geometric constants used below.

For any labelled configuration X let D(X) denote its squared-distance
matrix, with zero diagonal, and use the entrywise maximum norm.

**Theorem.** Set delta=2^-136. If two labelled configurations P',Q' in R3
satisfy

    ||D(P')-D(P)||_max <= delta,
    ||D(Q')-D(Q)||_max <= delta,                             (1)

then their prescribed matching has no continuous contracting motion in
R5. There is no hypothesis that any pair remains tight or that either
perturbed group remains rigid. Independent endpoint frames are allowed.

In particular, the fully explicit rational matching

    P -> Q_*=(1-2^-145)Q                                   (2)

strictly contracts all 276 pairs and has no such motion. Its Lipschitz
constant is exactly 1-2^-145. Six dimensions suffice by the classical
leapfrog, so its minimum motion dimension is six.

R7's [composition obstruction6524](../gaussian_screw_primitive_obstruction/PROOF.md)
already proves an existential neighborhood excluding even mixed
norm-preserving/R5-motion chains. The new claim here is an **explicit
radius for its R5-motion component**, with arbitrary endpoint perturbations
and a concrete strict control. It does not supply a quantitative radius
for the stronger mixed-chain obstruction.

## 2. A distance-defined halfway functional

Let A0=a(0), A+=a(Ce1), A-=a(-Ce1), and B0=b(0). Define coefficient
vectors on the labels by

    r(B0)=1, r(A0)=-3/2, r(A+)=r(A-)=1/4,
    s(A0)=-1, s(A+)=s(A-)=1/2,

and zero elsewhere. Both coefficient sums vanish, with ||r||_1=3 and
||s||_1=2. Set

    tau(D)=-(1/2) sum_(i,j) r_i s_j D_ij.                    (3)

For any Euclidean placement Z, this is the scalar product of the affine
differences sum r_i z_i and sum s_i z_i. Consequently it is frame
independent and continuous along a motion. Its reference values are
tau(D(P))=0 and tau(D(Q))=1. Moreover

    |tau(D)-tau(E)| <= 3 ||D-E||_max.                        (4)

This functional was supplied in R7's Section5 and is used with credit.
For (1), its endpoint values lie on opposite sides of 1/2. A proposed
contracting motion would therefore contain a placement Z in R5 such that

    D(Q)-delta <= D(Z) <= D(P)+delta,
    tau(D(Z))=1/2.                                         (5)

All matrix inequalities here are entrywise. We will rule out (5), not
merely a selected interpolation between the endpoints.

## 3. Quantitative repair of nearly rigid groups

We need a dimension-independent elementary alignment bound. Let X be a
centered n-by-3 reference configuration, n<=16, squared diameter<=128,
and X^T X>=kI with k=1/16. Let Z be a centered n-by-m configuration,
m>=3, whose squared distances differ from X's by at most delta.
Then there is an isometric embedding U of R3 into Rm such that, after
restoring the two means,

    max_i |z_i-(U x_i+t)| <= 32 sqrt(delta).                 (6)

Only delta=2^-136 is needed. Here is a full estimate, so no unquantified
Procrustes continuity is imported. Centered Gram matrices satisfy
G_Z-G_X=-(1/2)H(D_Z-D_X)H, where H is the centering projection. In
particular ||G_Z-G_X||_F<=2n delta. Set

    M=(X^T X)^(-1)X^T Z,       E=Z-XM,
    Pi=X(X^T X)^(-1)X^T.

Orthogonality to the columns of X gives

    ||E||_F^2=tr[(I-Pi)(G_Z-G_X)] <= 2n^2 delta,
    ||MM^T-I||_op <= 2n delta/k.                            (7)

The first inequality follows from Frobenius Cauchy--Schwarz and
sqrt(n)<=n; the second from the norm of the left pseudoinverse of X.
Our delta makes the last bound less than 1/2. Thus the row-polar factor
V=(MM^T)^(-1/2)M has VV^T=I3. For every eigenvalue lambda of MM^T,
(sqrt(lambda)-1)^2<=|lambda-1|^2. Therefore

    ||M-V||_F^2 <= 3(2n delta/k)^2,
    ||X(M-V)||_F^2 <= 12 n^3 (128) delta^2/k^2 <= n^2 delta. (8)

The last step uses delta<=k^2/(12 n 128), which our explicit delta
satisfies for every n<=16. Since E is orthogonal to X(M-V), the total
squared error is at most 3n^2 delta<=768 delta<1024 delta. This proves
(6). Polar alignment is classical; only this deliberately coarse
constant is needed here.

Apply (6) separately to the A and B groups of a hypothetical Z in (5).
Their reference distances agree at the two endpoints, so its hypothesis
holds on each group. We obtain a new placement W in the **same R5** with
both groups exactly congruent to their reference groups, and each label
moved by at most 32 sqrt(delta). No continuous selection or repair of an
entire motion is asserted.

Every distance in Z is less than 12. Pair-vector errors are at most
64 sqrt(delta)<=1, so

    ||D(W)-D(Z)||_max <= 1600 sqrt(delta).                   (9)

Indeed the squared-distance change is at most
(24+64sqrt(delta))64sqrt(delta)<=1600sqrt(delta). Put eta=2^-56.
For our delta, delta+1600sqrt(delta)<eta. Thus

    D(Q)-eta <= D(W) <= D(P)+eta,
    |tau(D(W))-1/2| <= 4800sqrt(delta).                     (10)

This repair is only an intermediate estimate. It does not claim the
original perturbed motion preserves any within-group distance.

## 4. Repair of the almost preserved axis

Normalize W by an ambient isometry fixing its A group in the original
R3. Its B group then has the form Ub+t, with U^T U=I3. Let M be U's
physical three-by-three block, c=U^T t, d=|t|^2. Its cross loss is

    L(v,u)=2a(v).[(M-I)b(u)+t_phys]-2c.b(u)-d.              (11)

The five matched parameters u=x e1 for x=-2,-1,0,1,2 give
|L(Cu,u)|<=eta. The fourth finite difference of these five equations is

    48(1-M33).

This credited identity comes from the original screw proof: the matched
loss is a quartic in x with leading coefficient 2(1-M33). Hence

    0<=1-M33<=eta/3,
    |Ue3-e3|<=sqrt(2eta/3)<=sqrt(eta)=2^-28.                (12)

Take the minimal-plane orthogonal rotation R sending Ue3 to e3. Its
operator distance from the identity is |Ue3-e3|. Replace U by RU while
keeping t fixed. This moves each B label by at most 5sqrt(eta), preserves
its exact rigid shape, and leaves A unchanged. Cross squared distances
change by at most

    120sqrt(eta)+25eta <= 145sqrt(eta),                     (13)

since the previous cross distances were below 12. Within-group distances
do not change. The resulting exactly axis-aligned placement, denoted W',
has every cross loss in

    -e <= L(v,u) <= |v-Cu|^2+e,       e=2^-20.              (14)

The constants satisfy eta+145sqrt(eta)<e. The translation of B0 remains
t, so (3), in these normalized coordinates, is still its axial component
tau. By (10),

    |tau-1/2|<e.                                           (15)

All of this occurs within R5; no extra coordinate was inserted.

## 5. A positive three-by-three determinant in only two dimensions

Write the axis-aligned embedding and translation as

    U(x,z)=(Nx,z,Kx),       t=(v,tau,w),
    N^T N+K^T K=I2,        K:R2->R2.                       (16)

The two-dimensional codomain of K is the decisive ambient-dimension
constraint. In these coordinates c_perp=N^T v+K^T w and c3=tau.
The matched cross loss is the quadratic polynomial

    L(Cu,u)=2u^T sym[C^T(N-I)]u+4tau|u|^2
                +2u.(C^T v-c_perp)+tau-d.                 (17)

Its values at 0,+/-e1,+/-e2,e1+e2 have absolute value at most e. Put
S=sym[C^T(N-I)]. Taking the constant, opposite linear, diagonal, and
mixed differences yields

    |d-tau|<=e,
    |(C^T v-c_perp)_j|<=e/2,
    |S_jj+2tau|<=e,       |S_12|<=2e.                      (18)

These estimates use only the sampled contacts. For example, the mixed
coefficient 4S_12 is bounded by 8e from the value at e1+e2 and the
other five coefficients.

Write the skew part of C^T N as zJ and put alpha=z/2. Equations
(15),(18), and (C^T)^(-1)=C/2 imply the entrywise estimate

    N=N0+E_N,        N0=alpha(I+J),       |(E_N)_ij|<=3e.   (19)

Indeed the diagonal symmetric errors of C^T N relative to
(1-2tau)I are at most e, the off-diagonal errors at most 2e, and
|tau-1/2|<=e.

Use three actual probe sites from the original fixture: v_probe=(1/4)e1,
(1/4)e2 with u=0, and v_probe=Ce1+(1/4)e1 with u=e1. Writing a probe
as Cu+q gives the exact identity

    L(Cu+q,u)-L(Cu,u)
       =tau|q|^2+2q.[(N-I+tau C)u+v].                     (20)

For q=(1/4)e_j, the lower and upper bounds in (14), together with
|L(Cu,u)|<=e, show that the relevant bracket coordinate has absolute
value at most 1/16+5e. The first two probes therefore give

    |v_j|<=1/16+5e<=9/128.

The third, (19), and (15) give

    |alpha-1/2|<=1/8+14e<=9/64.                            (21)

In particular 23/64<=alpha<=41/64. With k0^2=1-2alpha^2,

    k0^2>=367/2048,       |v|^2<=81/8192.                  (22)

Now form the Gram matrix of the two columns of K and the vector w:

    H = [[ I-N^T N,       c_perp-N^T v ],
         [ (c_perp-N^T v)^T, d-|v|^2-tau^2 ]].             (23)

It is a Gram matrix of three vectors in R2, so det H=0. Compare it to

    H0 = [[ k0^2 I2,     [(1-alpha)I+(1+alpha)J]v ],
          [ transpose,   1/4-|v|^2 ]].                     (24)

The new quantitative certificate is

    det H0=k0^2[k0^2/4-3|v|^2]
          >= (367/2048)(31/2048)=11377/2^22.               (25)

To control the perturbation, physical entries of N have absolute value
at most one. Equations (18),(19) give entrywise errors at most 12e in
the upper-left block of H-H0, at most 4e in the off-diagonal block,
and at most 2e in the bottom-right entry. The last bound follows from

    d-tau + tau-tau^2-1/4 = d-tau-(tau-1/2)^2.

Every entry of H0 has absolute value at most one, so every entry of H
has absolute value at most two. Expand the determinant into six signed
products. Telescoping each product of three entries bounds its change
by 3(12e)(2^2); hence

    |det H-det H0|<=864e.

Combining this with (25) gives the strict contradiction

    det H >= 11377/2^22 - 864/2^20
           =7921/2^22 > 0.                                (26)

Thus no placement (5) exists. The halfway argument proves (1).

## 6. Strict input, finite consumer, and limits

For lambda=1-2^-145, every distinct target pair of the reference is
nonzero, and

    D(P)_ij-lambda^2 D(Q)_ij
       =[D(P)_ij-D(Q)_ij]+(1-lambda^2)D(Q)_ij > 0.

Its endpoint displacement in squared-distance space is at most

    (1-lambda^2)128 < 256(2^-145)=2^-137 < delta.

This proves (2). Reference tight pairs exist, so the exact Lipschitz
constant of the new matching is lambda. The supplied compact witness
contains all rational coordinates; they are independently reconstructed
from the old fixture and this one rational factor.

For completeness, the classical R6 positive control for any matching
p_i->q_i is

    F_s(i)=((1-s)p_i+s q_i, sqrt(s(1-s))(p_i-q_i)),
    |F_s(i)-F_s(j)|^2=(1-s)|p_i-p_j|^2+s|q_i-q_j|^2.

Thus all distances contract. The substitution s=sin^2(theta) makes the
trajectories analytic on [0,pi/2]. This established leapfrog proves the
claimed upper bound of six without a numerical motion search.

The checker also finds rank8 for the matrix with rows
(p_i,q_i,1,|p_i|^2-|q_i|^2). Any pair of norm anchors would make its last
column a linear combination of the first seven. Thus this concrete
strict input is also outside the single anchored-norm primitive. No
mixed-chain conclusion for this particular explicit factor follows from
our R5 certificate or this rank test. The stronger existential closure
statement remains credited to R7, without an effective radius claimed.

Given any rational labelled endpoint pair, the finite consumer checks
all 276 endpoint inequalities and (1) and returns `NO_R5_MOTION` when
the displayed certificate applies. The metric guard is unchanged by
independent translations, rotations or reflections. Outside the certified
box it returns `NOT_CERTIFIED`, not a positive-motion assertion.

This supplies an explicit open obstruction region that includes inputs
with no preserved pair. It does not optimize the radius, produce a
Gaussian hinge sign, or classify all liftable maps. It excludes only
proof methods that require this prescribed R5 motion. In particular,
neither strict Lipschitz constant nor removal of all exact contacts makes
that method universal. R1's new eventual theorem and R8's fixed-variance
stability theorem remain complementary Gaussian results, not premises
of the geometric proof here.

The exact computations check the finite geometry, scatter bounds,
constant inequalities, symbolic determinant identity, rational strict
input, frame invariance and malformed/outside cases. Rigidity repair,
polar alignment, the halfway argument and the perturbation estimates
are written proofs, not formalized by those checks. No previous motion
checker, internal review, Gaussian quadrature or solver is run.
