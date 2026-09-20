# A uniform saturation criterion for small polygons

Write U_n = 2n sin(pi/(2n)). A small polygon is a convex planar polygon
of diameter at most one. Perimeter on a segment is twice its length.
Local maximality below means local maximality among small polygons with
at most n vertices, for example in the Hausdorff topology modulo translation.

**Theorem.** Let n >= 3. If P is a local perimeter maximum and

    0 <= U_n - p(P) <= 1/(100 n^3),

then P has exactly n genuine vertices, no two of its edges are parallel,
and Z = P-P has exactly 2n genuine vertices, all of norm one.

**Corollary.** For every power of two n >= 32, every global maximum has
this property. More strongly, every local maximum with perimeter at least
that of Bingane's polygon B_n has this property.

Thus for these orders global optimization can be restricted, without a
structural conjecture, to the unit-circle sign-code model. Neither an
optimal code, an exact optimal perimeter, nor uniqueness is asserted.
The constant 1/100 is convenient and is not claimed sharp.

## 1. Degeneracies and the difference body

For any two-dimensional convex polygon P with k genuine edges, delete
collinear subdivisions. Let r count pairs of oppositely directed parallel
edges of P. A strictly convex boundary has distinct oriented edge
directions, so cyclic Minkowski edge merging gives exactly

    m = 2k - 2r

edges of Z = P+(-P). Parallel summand edges add and do not cancel.
Moreover Z is centrally symmetric, lies in the closed unit disk, and
p(Z)=2p(P), by Cauchy's support-function perimeter formula.

For any m-gon Q in that disk, let omega_i be its exterior-angle widths,
eta_i the midpoint directions of its outward normal cones, and q_i its
vertices. Integrating its support function cone by cone gives

    p(Q) = sum_i 2 sin(omega_i/2) <q_i,u(eta_i)>
         <= sum_i 2 sin(omega_i/2) <= 2m sin(pi/m).

The final inequality is Jensen's inequality and sum omega_i=2pi.
The function m sin(pi/m) is increasing for m>=2. Consequently, unless
k=n and r=0, central symmetry gives m<=2n-2 and p(P)<=U_(n-1).

For real x>=2, with y=pi/(2x),

    U'(x) = 2(sin y-y cos y)
          = 2 integral_0^y s sin s ds >= pi^2/(6x^3).

Here sin s>=2s/pi for 0<=s<=pi/2. Integration from n-1 to n shows
U_n-U_(n-1)>=pi^2/(6n^3)>1/(100n^3). One-dimensional bodies have
perimeter at most 2, below the asserted threshold as well: U_2=2sqrt(2)>2
and the preceding comparison places the threshold above U_(n-1).
The theorem's hypothesis therefore forces k=n, r=0, m=2n.

## 2. Reconstruction and feasible local variables

Label the strict difference body cyclically z_0,...,z_(2n-1), with
z_(j+n)=-z_j. Put e_j=z_(j+1)-z_j for 0<=j<n, using z_n=-z_0.
Since P has no parallel edge pair, its edges select exactly one of each
antipodal pair of edges of Z. There is a sign code c_j in {+1,-1} with

    sum_j c_j e_j = 0.

Conversely, a strict centrally symmetric 2n-gon Z and such a code
reconstruct a convex n-gon: sort the vectors c_j e_j by their oriented
directions and concatenate. They are nonzero, have distinct unoriented
directions, and sum to zero. They cannot lie in a closed half-plane through
the origin (taking its normal would contradict the positive sum unless
all were collinear). Their consecutive angular gaps are therefore less
than pi, and the closed ordered chain is a strictly convex polygon.
Merging its edges with those of its negative recovers exactly the edges
of Z; both difference bodies are centered, so they coincide. This also
proves uniqueness up to translation.

The closure relation, after summation by parts, is

    sum_j a_j z_j = 0,
    a_0 = -(c_0+c_(n-1)),  a_j=c_(j-1)-c_j (1<=j<n).

Every a_j is 0 or +/-2. In a small neighborhood, strict convexity and
the direction order persist. Perturbations preserving this linear closure
and |z_j|<=1 reconstruct nearby feasible small polygons. The reconstructed
perimeter is the smooth function

    F(z) = sum_(j=0)^(n-1) |z_(j+1)-z_j| = p(Z)/2.

This local correspondence applies also to the antipodal endpoint z_n=-z_0;
it is not a free independent variable.

## 3. A global tangent-deficit estimate

Set t=pi/n and f(x)=2sin(x/2), for 0<=x<=pi. For every such x,

    f(t)+f'(t)(x-t)-f(x) >= t (x-t)^2/(6pi).                 (1)

Indeed -f''(s)=sin(s/2)/2>=s/(2pi). For x>=t the Taylor integral
is at least t(x-t)^2/(4pi). For x<=t it is at least

    (1/(2pi)) integral_x^t (s-x)s ds
      = (t-x)^2(x+2t)/(12pi) >= t(t-x)^2/(6pi).

This proves (1) even when x=0; no unproved preliminary localization is used.

For Z, use half of the normal cones. Their widths omega_j are in (0,pi)
and sum to pi. Let z_j=r_j u(phi_j) and eta_j be the normal-cone midpoint.
Since the origin is inside Z, <z_j,u(eta_j)> is positive. We may therefore
choose delta_j=eta_j-phi_j in (-pi/2,pi/2). Cauchy's formula gives

    F = sum_j f(omega_j) r_j cos(delta_j).

With D=U_n-F, the exact nonnegative decomposition is

    D = [n f(t)-sum_j f(omega_j)]
        + sum_j f(omega_j)(1-r_j cos(delta_j)).              (2)

The linear terms in (1) cancel, so (1)-(2) imply

    sum_j (omega_j-t)^2 <= 6nD <= 3/(50n^2).

In particular |omega_j-t|<t/4, since 3/50<pi^2/16.
Thus

    3t/4 < omega_j < 5t/4,    f(omega_j) > 3/(2n).          (3)

Because cos(delta_j)>0 and r_j<=1,

    1-r_j cos(delta_j) >= 1-cos(delta_j)
                       >= 2 delta_j^2/pi^2.

Each nonnegative summand in (2) is at most D. Hence

    delta_j^2 <= pi^2 nD/3 <= t^2/300 < t^2/256,
    |delta_j| < t/16.                                      (4)

Consecutive normal-cone midpoints differ by
(omega_j+omega_(j+1))/2>3t/4, including the wrap modulo pi.
For any two distinct half-indices r,j, their projective angular distance
therefore satisfies

    d_pi(eta_r,eta_j) > 3t/4.                              (5)

Here d_pi is distance between directions modulo pi, valued in [0,pi/2].

## 4. At most one interior half-vertex

If an interior vertex z_r has a_r=0, move only z_r by tau h and its
antipodal mate by -tau h. If two interior half-vertices z_r,z_s have
nonzero coefficients, use velocities

    v_r=a_s h,  v_s=-a_r h,

with all other half-velocities zero. Either motion preserves closure
and remains feasible for both signs of sufficiently small tau.

At least one edge velocity is nonzero. In fact, if every half-edge
velocity were zero, v_(j+1)=v_j for j<n-1 and -v_0=v_(n-1), forcing
all velocities to vanish. This handles adjacency and the antipodal
endpoint without a case omission. All nonzero edge velocities are scalar
multiples of h. Choose h not parallel to any affected edge. That edge's
length along the motion is strictly convex; all other lengths are convex.
Consequently F is strictly convex along a two-sided feasible line and
cannot have a local maximum at its center.

Thus at a local maximum there is at most one interior half-vertex, and
its coefficient is nonzero.

## 5. A direct feasible curve excludes the last interior vertex

Suppose z_r is that vertex. Then |a_r|=2. Another index j!=r has a_j!=0:
otherwise closure forces z_r=0, impossible for a vertex of Z. The second
vertex has |z_j|=1 and |a_j|=2.

Move z_j(tau)=R_tau z_j along its unit circle and define

    z_r(tau)=z_r-(a_j/a_r)(z_j(tau)-z_j).

All other half-vertices remain fixed, and antipodal vertices follow.
Closure is exact, z_r(tau) stays inside the disk for small |tau|, and
strict convexity persists. Section 2 therefore gives a two-sided curve
of nearby feasible original polygons. Its derivative at a local maximum
is zero. No multiplier or constraint-qualification theorem is needed.

Let g_k be the half-variable gradient of F. The two incident unit edge
tangents give

    g_k=f(omega_k)u(eta_k).

With T_j=u(phi_j+pi/2), the first variation is

    0 = (g_j-(a_j/a_r)g_r) dot T_j.

It follows, using |a_j/a_r|=1, that

    |sin(eta_r-phi_j)|
      = [f(omega_j)/f(omega_r)] |sin(delta_j)|.

By (3) and 2x/pi<=f(x)<=x,

    f(omega_j)/f(omega_r) < 5pi/6 < 3.

The inequality sin d>=2d/pi on [0,pi/2] now gives

    d_pi(eta_r,phi_j) < (3pi/2)|delta_j| < 5t/16,           (6)

where 3pi<10 was used. But (4)-(5) and the triangle inequality give

    d_pi(eta_r,phi_j) >= d_pi(eta_r,eta_j)-|delta_j|
                      > 11t/16,                           (7)

a contradiction. Every half-vertex, and hence every vertex of Z, has norm
one. This proves the theorem.

## 6. An infinite-family consequence of Bingane's construction

Bingane (2022), Theorem 1, constructs a small convex B_n for every power
of two n>=8, with

    p(B_n)=U_n cos(beta),
    beta = theta/2 - (1/2)arcsin((1/2)sin(2theta)),
    theta=pi/n.

This existence and exact perimeter formula are the sole specialized
external theorem used for the corollary. Since 0<=theta<=pi/8,
0<=beta. Using arcsin x>=x and sin x>=x-x^3/6 yields

    beta <= (theta-(1/2)sin(2theta))/2 <= theta^3/3.

The elementary inequality 1-cos beta<=beta^2/2 and U_n<pi imply

    U_n-p(B_n) <= pi^7/(18n^6).

For all n>=32,

    100 pi^7/18 < 100(22/7)^7/18 < 32^3 <= n^3.

Hence p(B_n)>U_n-1/(100n^3). Compactness of convex hulls of at most n
points after fixing translation gives a global maximum; a segment cannot
beat B_n. Every maximum, and every local maximum with p>=p(B_n), meets
the theorem's hypothesis. This proves the corollary for every power of
two n>=32, with no upper cutoff or finite-order extrapolation.

Finally, after rotation the saturated model is exactly

    0=phi_0 < phi_1 < ... < phi_n=pi,
    sum_j c_j (exp(i phi_(j+1))-exp(i phi_j))=0,
    p=sum_j 2sin((phi_(j+1)-phi_j)/2),  c_j in {+1,-1}.

The converse reconstruction was proved in Section 2. This is the stated
unconditional optimization reduction at these orders. It does not settle
which sign codes optimize, or the resulting nonlinear maximization.
