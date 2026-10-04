# Sharp complex repairs and the enlarged exact constructed cap

Actual **six-sendov-3 / researcher**, 2026-10-04. Ordinary author lemma,
**unformalized and independently unreviewed**. This extends the displayed
construction in [PROOF.md](PROOF.md). The exact cone certificate supplies
81 whole identities and six rational signs; it does not formalize the
uniform analytic arguments below. The theorem concerns this fixed compact
critical class, with every original root and critical multiplicity retained.

Independent REVIEW10246, actual six-reviewer-5, confirms the earlier
10212 axis construction and separately proves a complete **two-real-repair**
cone with sharp linear bounds. Its full
[ordinary proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/optimal-cap-audit/PROOF.md)
and [review](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/optimal-cap-audit/REVIEW.md),
source `b067e400d8abb097ee4e0d108796c7fe37cdb585`, were read before
writing this extension. Those bounds do not cover four complex components.
The new cone is derived from the four individual rows already established
in equation(8) of our profile proof. No reviewer program or certificate is
imported, and the review gives no verdict on this extension.

## 1. Complete four-component cone and sharp constants

Let theta_j=2pi j/9, c=cos(pi/9), s3=sin(theta_3)=sqrt(3)/2 and
s4=sin(theta_4)=sin(pi/9). To equation(1) of [PROOF.md](PROOF.md) add
the common complex M epsilon8 to all eight centers and the complex
term -H beta epsilon8 to D². Here M,beta are additional repairs,
relative to the already prescribed baseline and profile repairs.
Set Bcal=H beta/7 and write

    M=x+i u/s3, Bcal=y+i v/s3, r=s4/s3=1/(4c²-1), h=16c-9.

The four separate active normal changes, in label order3,6,4,5, are

    q3=-3x/2+3y/2+u+v, q6=-3x/2+3y/2-u-v,
    q4=-(1+c)x+2(1-c²)y+r(u+2cv),
    q5=-(1+c)x+2(1-c²)y-r(u+2cv).                 (C1)

They are the individual trigonometric rows of equation(8), including both
imaginary components. The objective excess due to these repairs is

    e=8x-7y=-w3(q3+q6)/2-w4(q4+q5)/2,
    w3=(2/3)(16c-9)/(2c-1)>0,
    w4=1/[(1+c)(2c-1)]>0.                        (C2)

Let C be the closed cone q3,q6,q4,q5<=0. Its full row matrix is
invertible. At e=1 its four vertices, in coordinates(x,y,u,v), are

    v3=(-2(1-c)/h,-1/h,-3c/h,3/(2h)),
    v6=(-2(1-c)/h,-1/h,+3c/h,-3/(2h)),
    v4=(1,1,(1+c)(4c²-1),-(1+c)(4c²-1)),
    v5=(1,1,-(1+c)(4c²-1),(1+c)(4c²-1)).          (C3)

The normal vector at v_j is zero except at its own label, where it is
-2/w_j. Every vertex has cost1. Indeed these identities give a right
and left inverse for the row matrix. If d_j=-q_j>=0, then

    (x,y,u,v)=sum_j (w_j d_j/2) v_j,
    sum_j w_j d_j/2=e.                            (C4)

Thus e>=0 on C, e=0 only at zero, and every positive cost slice is
exactly e times this three-simplex. Every cost sublevel0<=e<=D is the
four-simplex conv{0,Dv3,Dv6,Dv4,Dv5}; no other ray is omitted.

Put C0=sqrt(2/(1-c))=csc(pi/18). The actual squared norms of M and
Bcal on the v4/v5 rays are both C0². On v3/v6 they are respectively

    |M|²=4(1-2c+4c²)/h²<1,
    |Bcal|²=4/h²<1.                               (C5)

These formulas use s3²=3/4 and the exact identity
4(1-c²)(4c²-1)²=3. The physical c>15/16 implies h>6,
1-2c+4c²<5 and C0²>32, so the strict comparisons follow without
numerical fitting. The exact engine also verifies whole cubic-subfield
identities and rational lower bounds for these strict signs.

Applying the norm triangle inequality to(C4) proves the **sharp** bounds

    |M|<=C0 e, (H/7)|beta|<=C0 e,
    |M|+(H/7)|beta|<=2C0 e.                       (C6)

For e>0 equality in any of the three bounds occurs precisely on the
v4 or v5 ray. The v3/v6 norms are strictly smaller; v4 and v5 have
different complex phases in each coordinate, so a mixture of both makes
the triangle inequality strict. Both pure rays attain all three constants
simultaneously. In unscaled coordinates their values are

    M=e[1+/-i(1+c)/s4],
    beta=(7e/H)[1-/+i(1+c)/s4].                   (C7)

In particular a constant1 bound for |M|/e, valid in the two-real-repair
subclass of REVIEW10246, is false in this complex class. This is a scope
distinction and a sharp complex extension, not an objection to that review.

## 2. Actual attainability and objective expansion

Fix xprof=(t,I,R) with zero-sum I,R as in the profile proof. Its exact
defining critical functions are those of equation(1) there, with the
additional common M epsilon8 and squared pair term -H beta epsilon8
just specified. No Taylor truncation replaces these definitions.
The anchored degree-nine primitive still has exactly the eight specified
critical slots with multiplicity, and the branch near1 is the exact
marked root1-epsilon².

The whole four real/imaginary basis-column calculations in the profile
checker establish the primitive and actual eight-distance effects through
epsilon9. Every repair enters the primitive first at epsilon8. Products
of two repairs and products with any earlier nonconstant critical term
enter above epsilon9, so the effects at these orders are linear in all
four components. In particular the primitive change is exactly

    epsilon8[-9M(z8-1)+9H beta(z7-1)/7]

through epsilon9, with no epsilon9 change. The baseline original roots
have no epsilon1 term; implicit composition and multiplication of each
root with its conjugate therefore give, individually,

    N_j=epsilon8 q_j-A_j epsilon9+O_K(epsilon10),
    A3=A6=3/2, A4=A5=1+c.                         (C8)

The five inactive originals retain their strictly negative epsilon2
coefficients. Uniform analytic implicit functions at all nine distinct
ninth roots of unity, the analytic normalized pair square root, and
distance functions near1 give these remainders with every fixed number
of parameter derivatives on each fixed compact K. Hence every point of
C is an attainable repair jet: these very functions have all nine roots
strictly in the disk for small positive epsilon. The statement is uniform
on compact cone slices; negative q_j help and zero q_j retain the negative
ninth term. Arbitrary unspecified higher remainders need not share this
containment conclusion.

The entire actual FIRST objective is

    F=8+Ceta+Bstar eta²+Tstar eta³
      +[Gstar+Q(xprof)+e]eta4+8eta^(9/2)+O_K(eta5),
    Q=(kappa/H)t²+chi VI+VR/2.                    (C9)

Thus every cone point with Gstar+Q+e<0 is in the exact third cap for
all sufficiently small positive eta. A zero leading fourth cost alone
does not imply the exact cut: the positive ninth term still matters.
For example t=I=R=0 and e=-Gstar/2 on either(C7) ray gives actual
strict-rooted, exact-third-cut families violating a constant1 complex
repair bound. No arbitrary-competitor feasibility converse is asserted.

## 3. Fifteen-parameter exact cap and its complete weighted rays

Let g=-Gstar>0 and fix R0>2g. Work in the compact parameter domain

    D_R0={xprof in R x H0 x H0, (M,beta) in C:
                                      Q(xprof)+e(M,beta)<=R0}. (C10)

It has real parameter dimension15. Positivity of Q and(C6) make it
compact. By(C8), every one of its polynomials is strictly disk-rooted in
one common positive epsilon collar. Define the exact normalized excess

    E_epsilon=(F-8-Ceta-Bstar eta²-Tstar eta³)/epsilon8.

The division has a removable analytic singularity, including in all four
repair components, and(C9) gives

    E_epsilon=-g+Q+e+8epsilon+O_R0(epsilon²).       (C11)

Consider the compact unit budget set S={Q+e=1,(M,beta) in C}. Every
nonzero point of D_R0 lies on exactly one weighted ray

    (xprof,M,beta)=(sqrt(rho) xhat,rho Mhat,rho betahat),
    (xhat,Mhat,betahat) in S, 0<rho<=R0.           (C12)

Along it E=-g+rho+8epsilon+O(epsilon²), uniformly in S. It is
negative for rho<=g/2 and positive for rho>=2g for small epsilon.
On the compact annulus g/2<=rho<=2g its derivative is1+O(epsilon²),
uniformly; differentiating sqrt(rho) there causes no singularity.
There is therefore exactly one positive ray endpoint rho_epsilon, and

    rho_epsilon=g-8epsilon+O_R0(epsilon²).         (C13)

The exact constructed cap is precisely the portions0<=rho<=rho_epsilon
of these weighted rays. It is nonempty, compact and connected: contraction
along a weighted ray stays feasible and joins every point to the origin.
The limiting cap is exactly Q+e<=g with(M,beta) in C. Every ray tip
has exact objective equality and every original root remains strict.
Cone faces also form boundary portions; no globally smooth boundary or
strict convexity is claimed for this enlarged cap.

## 4. Finite endpoint collapse and two rates of stability

Write U=VI+VR and retain the exact axis endpoint t_epsilon of10212.
At zero extra repairs the profile Hessian and permutation argument of
the profile proof give

    E(t,I,R,0,0)-E(t,0,0,0,0)>=d U.

The extra-repair gradient in(C11) is the cost gradient plus O(epsilon²).
Integrate along the segment from zero to(M,beta), which stays in C,
and use(C6). Uniformly on D_R0, for some d1>0 and small epsilon,

    E(t,I,R,M,beta)-E_axis(t)>=d1(U+e).            (C14)

The exact axis E is even and strictly convex on the bounded t interval
for small epsilon. A feasible point thus has |t|<=t_epsilon. A uniform
upper bound on its derivative further gives

    t_epsilon-|t|>=d2(U+e)                        (C15)

with d2>0. Only bounded parameter sets are being compared.

The profile polynomial difference at the same t is O(epsilon8 U):
the zero-sum split cancels its linear terms and all lower orders through
epsilon7. The extra-repair polynomial difference is O(epsilon8 e), by
(C6) and analyticity of its literal factors. The uniform simple-root
maps transfer these coefficient bounds to every original root. Hence
the motion functional R_eta from10212 satisfies

    |R_eta(p)-R_eta(p_axis(t))|<=D epsilon4(U+e).  (C16)

On any fixed peripheral interval the unique winning axis branch has
outward derivative at least b epsilon>0. Its endpoint loss, by(C15),
dominates(C16) strictly whenever U+e>0. In a fixed central interval
the axis has an order-epsilon endpoint gap, and(C16) cannot close it.
Consequently the enlarged exact cap's motion maximum occurs **precisely**
at I=R=M=beta=0 and t=+/-t_epsilon. The values, winning labels7/2,
and expansion sqrt(A)+sstar sqrt(eta)+O(eta) remain the exact old ones.

For a motion deficit Delta sufficiently smaller than epsilon, the point
must be peripheral. Absorb(C16) into half the positive axis loss using
(C15), to obtain

    t_epsilon-|t|=O_R0(Delta/epsilon),
    U+e=O_R0(Delta/epsilon).                      (C17)

The split profile norm is O_R0(sqrt(Delta/epsilon)), whereas the two
complex repairs have the stronger linear bound
|M|+(H/7)|beta|=O_R0(Delta/epsilon), with the sharp coefficient-level
constant2C0 supplied by(C6). This does not state a uniform estimate for
unbounded or epsilon-dependent normalized parameters.

Finally the full actual cubic skew is unchanged to the needed scale.
For a pair B+/-D, its imaginary cubes sum to
2(Im B)³+6(Im B)(Im D)². The baseline/profile pair center has imaginary
part O(epsilon3), while (Im D)²=O(epsilon2). A common extra center
changes Im B by O(epsilon8 |M|). The extra squared-pair term changes
(Im D)² by O(epsilon8 |beta|), since
(Im D)²=(|D²|-Re D²)/2 and D²/epsilon² stays near -H/2.
The six small cubes have even higher extra-center orders. After dividing
the full numerator by epsilon4, these facts and the profile cubic identity
give the uniform actual bound

    |lambda_eta(p)-lambda_eta(p_axis(t))|
                            <=D1 epsilon5 U+D2 epsilon6 e. (C18)

The axis skew derivative is at least epsilon/2 everywhere in the bounded
t interval. Its endpoint loss together with(C15) strictly dominates(C18)
for U+e>0. Thus its extrema too occur precisely at the two old axis
endpoints. The enlarged cap is connected and invariant under

    (t,I,R,M,beta)->(-t,-I,R,conjugate M,conjugate beta).

This conjugates the polynomial, swaps the two reflected cone rays and
reverses skew. The actual skew image of this whole15-parameter constructed
cap is exactly the old symmetric interval with positive endpoint

    ell epsilon-4H epsilon²/(kappa ell)+O(epsilon3),
    ell=sqrt(-HGstar/kappa).

## 5. Trust, evidence and remaining frontier

[cone.py](cone.py) reconstructs all four actual trigonometric rows,
both matrix inverses, all four rays and costs, the dual, each actual ray
norm and six physical rational signs. Complete maps are compared before
the [CONE.json](CONE.json) record seal. The profile source's existing
329 identities and ten signs supply its exact factor, distance, root,
cubic and four independent complex-repair columns. Native threads are
one, with one serial mathematical child and unchanged45s guards.

The uniform analytic extension, complete cone proof, strict all-nine
attainment, weighted cap completeness, finite collapse and stability are
ordinary unformalized arguments. Whole source checks or a computation
timeout do not prove these bridges. Full large regenerated profile maps
remain private; compact source regenerates them without private inputs.
Validation distinguishes the frozen329-map source from this later cone
and written-source addition; both exact record families remain pinned.

The earlier10212 source and REVIEW10246 are attributed with their precise
scopes. Neither REVIEW10246 nor REVIEW10220 gives this child a verdict.
The primary first-power target remains Teng Zhang's
[Conjecture1.2](https://arxiv.org/html/2609.19126), distinct from the
quadratic Theorem1.3. This result supplies no all-competitor normalization,
universal fourth optimum, square-root skew upper rate or effective collar.
An arbitrary-competitor fourth lower inequality with absorbable moving
moment errors remains the principal unresolved next step.
