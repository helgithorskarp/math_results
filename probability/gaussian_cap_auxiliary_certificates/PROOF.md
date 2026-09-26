# Auxiliary certificates for disjoint reflected caps

Complete author proof, 26 September 2026. Independent correctness and priority
review are pending. The full dimension-three Gaussian-majorisation conjecture
remains open. This proves an unrestricted-cap-count positive class and a
four-cap extension, and gives a finite obstruction to one sufficient motion
certificate. The obstruction is not a Gaussian counterexample.

## 1. Positive classes and geometric consequences

Let K be a compact convex subset of R3. Given finitely many unit normals n_i
and offsets b_i, assume the caps C_i={x in K:n_i.x>b_i} are pairwise disjoint.
Let T reflect C_i in its boundary plane and fix the remaining core:

    T(x)=x-2(n_i.x-b_i)n_i on C_i,     T(x)=x on the core.       (1)

**Theorem A.** This map admits a continuous contracting motion in R5 with
analytic individual trajectories in either of the following cases:

1. All the normals lie in one closed hemisphere: there is a nonzero w with
   n_i.w>=0 for every i. The number of caps is arbitrary.
2. There are at most four caps, with no hemisphere restriction.

Consequently, for every probability law mu on K, every s>0, and every h>=0,

    integral(mu*gamma_s-h)_+ <= integral(T#mu*gamma_s-h)_+,      (2)

where gamma_s is the R3 Gaussian of covariance s I. There is no weight,
atom-count, density, or positive contraction-reserve hypothesis. Finite
positive measures follow by scaling their mass.

For every finite labelled selection x_j in K and arbitrary individual
radii r_j>=0, the volume of the union of balls B(Tx_j,r_j) is no larger
than that of the original union, and the intersection volume is no smaller.
The radii need not be ordered or equal. These conclusions use the existing
R5 Gaussian and ball-volume transfer theorems, credited in Section 5.

The [three-cap source](../gaussian_disjoint_cap_reflections/PROOF.md) already
proves the conditional motion from a finite auxiliary-vector certificate.
Our contribution is to discharge that condition for the two classes above
and delimit its universality by an exact twelve-normal obstruction. The
hemisphere class permits arbitrarily many distinct reflection planes with
normals spanning R3. It is not a bound of four on the number of centers.

## 2. The exact finite dependency

The needed auxiliary vectors are unit vectors u_i in R2 satisfying

                     u_i.u_j <= 1+2 n_i.n_j.                  (3)

This is weaker than u_i.u_j<=n_i.n_j. The distinction is essential even
for four regular tetrahedral normals; see Section 6.

For completeness, here is the conditional motion from the cited source.
Write a_i(x)=n_i.x-b_i. For theta from 0 to pi put

    P_theta(x)=(x-(1-cos theta)a_i(x)n_i,
                         sin(theta)a_i(x)u_i) on C_i,         (4)

and P_theta(x)=(x,0) on the core. Boundary formulas agree because a_i=0.
Each trajectory is analytic, and the finite piecewise definition is jointly
continuous. Within-cap distances are constant. A cap/core distance squared
has the form |x-z|^2-2(1-cos theta)a_i(x)(b_i-n_i.z), so decreases.

For x in C_i and y in C_j, i!=j, set

    a=n_i.x-b_i>0, b=n_j.y-b_j>0,
    h_i=b_i-n_i.y, h_j=b_j-n_j.x,
    N=n_i.n_j, U=u_i.u_j, d=x-y, v=a n_i-b n_j.

Disjoint cap intervals on the segment [x,y] imply h_i h_j>=ab. Hence

    E=d.v-|v|^2=a h_i+b h_j+2abN >= 2ab(1+N).                 (5)

Put Delta=2ab(N-U), lambda=(1-cos theta)/2. Direct expansion gives

    |P_theta(x)-P_theta(y)|^2
      =|d|^2-4lambda E+4lambda(1-lambda)Delta.                 (6)

Since N,U are inner products of unit vectors, (3) is equivalent to
|N-U|<=1+N. Thus E>=|Delta| and the derivative in lambda is nonpositive
on [0,1]. This proves the conditional motion for any finite cap count.
Condition (3) is sufficient; it is not asserted necessary for a particular
cap configuration, for motion (4) with larger geometric margins, or for an
arbitrary R5 contracting motion.

## 3. Arbitrarily many hemispherical normals

Normalize w to a unit vector and let p_i=n_i-(n_i.w)w. If p_i!=0 choose

                         u_i=p_i/|p_i| in w-perp.             (7)

Identify the two-dimensional plane w-perp with R2. If p_i=0, then n_i=w,
because n_i.w>=0; it has nonnegative inner product with every other normal.
Choose its u_i arbitrarily on the auxiliary circle.

For a pair with N=n_i.n_j>=0, (3) is automatic because its right side is
at least one. For N<0 put z_i=n_i.w>=0, z_j=n_j.w>=0. Neither p vanishes,
and

    p_i.p_j=N-z_i z_j <= N <0,
    0<|p_i||p_j|<=1,
    u_i.u_j=(N-z_i z_j)/(|p_i||p_j|) <= N <= 1+2N.            (8)

This proves (3), including hemisphere-boundary and polar degeneracies.
There is no cap-count dependence. For rational unnormalized normals, a
rational hemisphere witness and the required signs can be checked using
only rational dot products. The theorem does not require a rational
witness or make such a promise for arbitrary real data.

This simple projection proof is a sufficient geometric dependency, not
a claim of a new general projection theorem. Its application here removes
the finite cap-count restriction from the supplied motion mechanism.

## 4. Every four normals have an auxiliary certificate

The following argument works for four unit vectors in any Euclidean space.
Index them so that m=n_1.n_2 is the smallest of their six pairwise products.
For k=3,4 put a=n_1.n_k, b=n_2.n_k. Then

                              a+b >= -1.                    (9)

Indeed if m>=-1/2, use a,b>=m. If m<=-1/2, Cauchy--Schwarz gives
a+b>=-|n_1+n_2|=-sqrt(2+2m)>=-1. Equality is allowed.

Define the required angular separations

    alpha_ij=arccos(min{1,1+2n_i.n_j}) in [0,pi].              (10)

First alpha_1k+alpha_2k<=pi. If either dot product is nonnegative,
one alpha is zero. Otherwise cosine monotonicity and (9) give
1+2a>=-(1+2b), which is the stated angular inequality.

Second, for every triple i,j,k,

                     alpha_ij+alpha_ik+alpha_jk<=2pi.         (11)

Each alpha is no larger than the original spherical angle. The original
three angles have perimeter at most 2pi: apply the spherical triangle
inequality to a path through the antipode of the third vector.

Set l_k=alpha_1k, h_k=pi-alpha_2k for k=3,4. These are nonempty intervals
I_k=[l_k,h_k]. The interval of possible sums I_3+I_4 intersects
[alpha_34,2pi-alpha_34]: its two cross inequalities are exactly (11) for
triples (1,3,4) and (2,3,4). A deterministic selection is

    S=max{alpha_34,l_3+l_4},
    theta_3=max{l_3,S-h_4},      theta_4=S-theta_3.             (12)

Then theta_k lies in I_k and S in the required sum interval. Put the four
auxiliary angles at 0, pi, theta_3, -theta_4. The pair 1,2 is antipodal;
the four constraints to 1 and 2 follow from the intervals; and the last
constraint follows because cos(S)<=cos(alpha_34). Thus (3) holds.
Repeated normals, antipodes, ties for the minimum, and zero angles are
included. For fewer normals, repeat a normal and then discard duplicates.

The universal interval step (12) is also proved by a compact rational
certificate. In units of pi write

    (a,b,c,d,e)=(alpha_13,alpha_14,alpha_23,alpha_24,alpha_34)/pi.

The fourteen nonnegative affine premises are the ten box constraints on
these five variables and

    1-a-c, 1-b-d, 2-a-b-e, 2-c-d-e.

There are four branches for S=max(e,a+b) and theta_3=max(a,S+d-1).
Each branch adds its two selecting inequalities. For all four branches,
the certificate gives nonnegative rational combinations proving the six
required conclusions: theta_3 in [a,1-c], theta_4 in [b,1-d],
and S in [e,2-e]. All 24 identities are checked coefficient by coefficient.
The branch union is exhaustive by the definition of max; ties may be in
both branches and are not excluded. No numerical angular tolerance enters
this finite proof. The geometric reduction (9)--(11) is written mathematics.

## 5. Gaussian and Kneser--Poulsen transfers

Apply [Aishwarya--Li, Theorem 1.4(i)(a)](https://arxiv.org/html/2609.07041v2)
to the R5 motion. It compares endpoint density values sampled from the
densities themselves. The endpoint densities factor as f phi_2,s and
g phi_2,s. If Y has density phi_2,s, then phi_2,s(Y)/(2pi s)^(-1) is uniform
on (0,1). Consequently, for X with density f and independent Y,

    Pr{f(X)phi_2,s(Y)>(2pi s)^(-1)h}=integral(f-h)_+.

The density-value comparison therefore gives (2). This is the already
established two-auxiliary-coordinate transfer, not cancellation of an
ordinary Gaussian majorisation factor.

For finitely many centers, reverse (4) and apply
[Bezdek--Connelly, Theorem 1](https://arxiv.org/pdf/math/0108098): an endpoint
expansion in R3 with a piecewise smooth expanding motion in R5 has both
individual-radius ball-volume inequalities. Our trajectories are analytic.
Zero radii follow by continuity. The transfer theorem is prior work;
the new geometric input is the auxiliary certificate for Theorem A.

## 6. Exact controls showing the scope of the extension

For an example with four active planes in a hemisphere, take the seven
source points of the earlier three-cap obstruction, in the order

    (0,0,0), (-1,-1,0), (-1,0,1), (0,-1,1),
    (1,-2,5), (-2,-5,-1), (-5,1,2),

and adjoin z=(-4,-10,7). Let K be their convex hull. Use raw cap forms

    t_0=(1,1,1).x,  t_1=(1,-1,-1).x,
    t_2=(-1,1,-1).x, t_3=(1,-1,0).x-11/2.                    (13)

Normalize each raw normal to define the reflection; positive rescaling
does not change its cap or plane. The vector w=(1,1,-1) has products
1,1,1,0 with these raw normals, certifying the common hemisphere.

Disjointness on all of K follows from the affine inequalities

    t_0+2t_1<=0, t_1+2t_2<=0, t_2+2t_0<=0,
    t_0+14t_3<=0, t_1+2t_3<=0, t_2+26t_3<=0.                 (14)

They are checked at all eight vertices, hence throughout the convex hull.
Every coefficient is positive, so simultaneous positive caps are excluded.
The first three moved vertices and their images are unchanged; z maps to
(-9/2,-19/2,7). Each cap is nonempty and has a three-dimensional relative
interior in K. The four distinct reflection linear parts on open pieces
exclude a representation of this same map using only three cap reflections.

Restriction to the original seven sites inherits the source's complete
obstruction to finite chains of strong contractions, with changing frames
allowed. That obstruction is credited, not reproved by a count of one-use
fold orders. Thus the enlarged positive map also lies beyond that mechanism.
The exact audit verifies all 28 full-time pair polynomials and paired rank
six; these checks supplement, rather than replace, the all-domain proof.

For a four-normal control outside every closed hemisphere, take the four
vectors in {+/-1}^3 with coordinate product +1, normalized by sqrt(3).
Their sum is zero and they span R3, precluding a nonzero hemisphere witness.
Square auxiliary vectors have pair products 0 or -1, all at most 1/3,
and hence satisfy (3). In contrast the stronger inequalities U_ij<=-1/3
are impossible in R2: summing gives |sum u_i|^2<=0, forces every product
to equal -1/3, and yields the regular tetrahedral Gram matrix of rank three.
This explains why simply extending the earlier stronger three-angle
comparison would miss even this positive case.

## 7. A finite obstruction to universal planar auxiliary certificates

**Theorem B.** There is a set of twelve unit normals in R3 for which (3)
has no solution. This refutes universal feasibility of that sufficient
normal-only certificate. It does not refute any Gaussian or ball inequality,
nor exclude a different R5 motion for caps with these normals.

Let phi=(1+sqrt(5))/2 and take the twelve vectors

    (0,+/-1,+/-phi), (+/-1,+/-phi,0), (+/-phi,0,+/-1),          (15)

divided by sqrt(phi+2). They form an antipodal set. Declare two vertices
adjacent when their unnormalized dot product is phi. Their normalized
product is c=phi/(phi+2)=1/sqrt(5)>1/4.

Suppose auxiliary circle vectors existed. The constraint for an antipodal
pair forces u_-v=-u_v. For adjacent v,w, apply (3) to v,-w to obtain

                        u_v.u_w >= 2c-1 > -1/2.              (16)

Thus every principal angular increment along an edge is strictly between
-2pi/3 and 2pi/3. On any triangle of adjacent normals, the three increments
sum to an integer multiple of 2pi with absolute value strictly less than
2pi. Their sum must therefore be zero.

The exact certificate supplies a ten-edge cycle, ten oriented adjacent
triangles whose boundary is that cycle, and its antipodal half-shift:
vertex i+5 on the cycle is the antipode of vertex i. Summing the ten triangle
identities cancels internal edges and makes the total cycle increment zero.
But antipodal edges have identical principal increments. The full sum is
twice the sum on the first five edges, whose endpoints are antipodal; that
half-sum is an odd multiple of pi. The full sum cannot be zero, a
contradiction. This is an elementary finite winding argument of the
Borsuk--Ulam type, written without invoking a separate topological theorem.

All coordinates and adjacency identities are checked exactly in
Z[phi], with phi^2=phi+1. The certificate checks the triangle-chain boundary
and antipodal shift, not just the counts 12,30,20. A separate rational
row-space check derives the vanishing half-cycle from all triangle and
antipodal-edge equations, without using the supplied disk chain.
The inequality c>1/4 follows from 3phi>2 and phi>1; no decimal enclosure
or numerical circle infeasibility status is used.

These normals can occur for genuinely disjoint caps of a convex body:
on the unit ball take common offset b=9/10>sqrt((1+c)/2).
The largest inner product of distinct normals is c. If two caps met,
2b<(n_i+n_j).x<=sqrt(2+2n_i.n_j)<=sqrt(2+2c), a contradiction.
The strict bound on b is checked by 5*31^2>50^2, since 2b^2-1=31/50.

In fact this very cap configuration is **positive**: taking all auxiliary
vectors equal makes (4) a contracting motion already in R4. For N>=0,
(5) gives E>=2ab(1+N)>=2ab(1-N)=|Delta|. For N<0, a point in the other
cap has projection onto n_i at most sqrt(1-(9/10)^2)<9/20. Hence
h_i,h_j>9/20, while a,b<=1/10, giving

    E>2ab(9/2+N)>=2ab(1-N)=|Delta|.

The last comparison follows from N>=-1. Thus the actual geometric margin
exceeds the conservative bound (5). This supplies an adversarial positive
control for the normal-only infeasibility claim. The auxiliary obstruction
does not even obstruct motion (4) on these particular shallow caps. No
sharp minimal number of obstructing normals is claimed.

## 8. Checking boundary and remaining question

The public packet contains the four-branch rational duals, the finite
hemisphere control, and the exact winding certificate. Integer/Fraction
arithmetic and the small checkers are trusted. The continuous motion,
projection sign argument, spherical-angle reduction, winding interpretation,
and quoted transfer theorems are written proofs, not formalized theorems.
Two author checking algorithms are not independent peer acceptance.

No Gaussian quadrature, moment enclosure, or signed endpoint assumption is
needed for the positive classes. The functional finite-certificate and
ordered-contact interfaces retain their unrestricted missing signs. General
compatible folding meshes and arbitrary contractions are not settled by
Theorem A or the auxiliary obstruction. See [README.md](README.md) and
[SOURCES.md](SOURCES.md) for replay, attribution, and the precise claim status.
