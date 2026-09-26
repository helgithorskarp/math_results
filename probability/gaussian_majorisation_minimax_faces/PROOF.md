# Exact isometric faces in the Gaussian common-set minimax problem

Complete author proof with two exact audits, 26 September 2026. Independent
review and formalization are pending. This supplies positive certificates
for a family of common-set tests and a complete finite description of the
isometric degeneracies of the square-cone search. The full dimension-three
Gaussian-majorisation conjecture remains open. No new Kneser--Poulsen class
or negative integrated Gaussian witness is claimed.

## 1. A common-set certificate on any orthogonal splitting of dual cones

Let C,D be cones in R^n with a.b>=0 for every a in C and b in D. On
K=C union (-D), let T fix C and send -b to b. This is a contraction;
the squared cross-distance loss is 4a.b. The prescriptions agree at zero.
Only bounded probability laws on K are considered below.
Here bounded means bounded support, and
gamma_s(z)=(2 pi s)^(-n/2) exp(-|z|^2/(2s)).

Fix a linear subspace U and its orthogonal reflection S=2P_U-I. Let
sigma be any bounded probability law supported on

    (C intersect U) union (-(D intersect U-perp)).             (1)

The law may have arbitrary mass at zero. At variance s>0, put

    E={sigma*gamma_s>h},  0<h<max(sigma*gamma_s),  F=S E.

**Theorem 1 (positive common-set transfer).** For every x in K,

    integral_F gamma_s(z-Tx) dz >= integral_E gamma_s(z-x) dz. (2)

Consequently, for every bounded prior mu on K,

    C_(T#mu*gamma_s)(|E|) >= integral_E mu*gamma_s,             (3)

where C_f(v)=sup_(|A|=v) integral_A f. The infimum over these priors
of the difference in (3) is exactly zero, attained at mu=sigma. The same
is true if the prior's origin mass is fixed to that of sigma and the
remaining support is restricted to any compact subset of K containing that
of sigma. All statements hold for every s>0 and every positive retained
volume v: the continuous strictly decreasing Gaussian level-volume
function supplies the unique h with |E|=v. Positive levels are null by
real analyticity and nonconstancy; positive superlevel sets are bounded,
and each nonempty intermediate density interval has an open inverse image.

These are special test sets E, not all sets of that volume. The theorem
does not conclude full majorisation for an arbitrary prior on K.

### Elementary polarization proof

For a nonzero d, write R_d=I-2dd^T/|d|^2. If every center c of sigma
satisfies c.d>=0, then, for z.d>=0,

    (sigma*gamma_s)(z) >= (sigma*gamma_s)(R_d z),               (4)

because |R_d z-c|^2-|z-c|^2=4(z.d)(c.d)/|d|^2>=0. Thus
1_E(z)>=1_E(R_d z) on that halfspace. If u,v have equal norms and
d=v-u, then R_d u=v and

    integral_E [gamma_s(z-v)-gamma_s(z-u)] dz
      = integral_(z.d>0) [1_E(z)-1_E(R_d z)]
                            [gamma_s(z-v)-gamma_s(z-u)] dz >=0. (5)

Both factors have the displayed sign. The case d=0 gives equality.
This is the classical two-point polarization argument, written here
to make the certificate's exact sign obligation explicit.

For x=a in C take u=a, v=Sa, d=-2P_(U-perp)a. Centers c in C intersect U
have c.d=0; centers c=-b in -(D intersect U-perp) have c.d=2a.b>=0.
For x=-b take u=-b, v=Sb, d=2P_U b. Now the first type of center has
c.d=2c.b>=0 and the second has c.d=0. Norms are equal in both cases.
Equation (5), followed by changing variables by S, proves (2).
Integration against mu proves (3). On the support (1), T=S, so F is a
superlevel set of T#sigma*gamma_s. Equality follows at sigma, proving
the exact minimax value without an optimization algorithm. This is an
explicit instance of the team's common-set formulation, not a claim
that its arbitrary-set obligation is solved.

## 2. The complete finite boundary for the square-cone family

In the displayed order, let

    A=((1,0,1),(0,1,1),(-1,0,1),(0,-1,1)),
    B=((1,1,1),(-1,1,1),(-1,-1,1),(1,-1,1)),
    X=(0,A,-B), Y=(0,A,B).                                   (6)

Index the eight nonzero sites 0,...,7, with A first and then -B.
The strict cross pairs, written with separate A,B indices, are

    E_G=((0,0),(0,3),(1,0),(1,1),
         (2,1),(2,2),(3,2),(3,3)).                           (7)

They form a cycle of length eight. All other pairs preserve distance.
For weights a_i,b_j>=0 and origin weight p>=0, with total mass one, put

    tau(w)=sum_((i,j) in E_G) a_i b_j.

The exact Gaussian product identity gives

    integral (g_s^2-f_s^2)
      =2(4 pi s)^(-3/2) [exp(-1/(4s))-exp(-9/(4s))] tau(w).  (8)

Every term is nonnegative. Hence equality in (8) holds exactly when
the occupied nonzero-site support is an independent set of (7).
There are 47 such supports, including empty, and ten maximal ones.
Their little-endian eight-bit masks are

    15,28,41,56,67,97,134,148,194,240.                       (9)

Two maximal faces are the entire A or B cluster. The other eight consist
of one ray from one cluster and its two orthogonal rays in the other.
Every such support is carried by a single orthogonal reflection S_F:
choose U=span{A_i:i in F}. These reflections prove full Gaussian equality
on the faces, and Theorem 1 proves the stronger *all-prior* zero minimax
certificate for their source superlevel sets. Conversely any occupied
strict pair makes (8) positive, so the two laws cannot be congruent, even
after an unlabelled rematching. Thus this is a complete classification
of isometric/equal-L2 priors on (6), not a classification of all priors
obeying majorisation.

The compact certificate supplies all ten rational matrices. The direct
checks, for every i and every occupied face site j, are

    S_F^T S_F=I,  S_F^2=I,
    S_F x_j=y_j,
    |S_F y_i|=|x_i|,
    x_j.(S_F y_i-x_i)>=0.                                  (10)

These are exactly the inputs to (4)--(5), including the origin. The
enumeration of all 256 subsets establishes coverage for (9).

For sigma in the relative interior of a maximal face, all of the
common-set inequalities (2) at sites outside the face are strict.
Indeed maximality gives an occupied strict-edge neighbor; in (10)
some center then has strictly positive scalar product. Equation (4)
is strict in the positive halfspace. At every positive nontrivial level,
an open region lies in E but its reflection lies outside E: a maximizer
is in that halfspace (the normal derivative at its boundary is positive),
and a path from it to infinity crosses the level there. Both factors in
(5) are then strictly positive on an open set.

In particular, at any fixed s,v, every direction from such a prior toward
a prior having mass outside the face has strictly positive first variation
of C_g(v)-C_f(v). Differentiating a Gaussian concentration functional in
a mixture direction gives the integral over its unique volume-v top set;
this follows by comparing the two maximizing sets and dominated convergence,
since positive Gaussian levels are null and bounded. The difference of
these derivatives is the potential in (2). No uniform neighborhood through
v=0, v=infinity or s=0 is inferred. A first-variation statement does not
exclude a higher-order or an interior counterexample.

## 3. A convex reserve against exact equality, with an exact contrast bound

Let F range over (9) and define

    delta(w)=min_F sum_(i notin F) w_i.                      (11)

This is exactly the total-variation distance (one half of the L1 distance)
from the discrete prior to
the union of the ten isometric faces, including when origin mass p is
held fixed: move the mass outside F onto F, leaving p unchanged.
For a prescribed delta_0>0, the reserve delta(w)>=delta_0 is therefore
**ten linear inequalities**. Its intersection with the probability
simplex and a fixed origin mass is a compact convex polytope. One must
have delta_0<=(1-p)/2; uniform nonzero-site weights attain that endpoint.
The union of these polytopes as delta_0 decreases to zero contains every
nonisometric prior. A fixed positive reserve alone is not a complete
search of the whole question.

**Theorem 2 (sharp signal bound).** For all nonnegative weights,

                         tau(w)>=(3/7) delta(w)^2.           (12)

The constant is optimal. For the packet weights

    (a,b)=(2,2,3,0,2,0,3,2)/14,

delta=1/2 and tau=3/28, giving equality. Scaling this packet permits
any prescribed additional origin mass. This is a normalization bound
for the already-known second energy; it does not compare all hinges.

### Proof and compact alternative certificates

By max-flow/min-cut on the bipartite cycle (7), delta is the maximum
total flow z_e>=0 whose vertex loads are bounded by a_i and b_j. A cut
is exactly a weighted vertex cover, whose minimum is (11). This is the
classical theorem, not a new flow result. For delta>0, monotonicity of
tau reduces (12) to weights given by the vertex loads of a unit edge
flow. In lexicographic edge order (7), its quadratic form is z^T M z,
where

    M_ef = [1_((a(e),b(f)) in E_G)+1_((a(f),b(e)) in E_G)]/2. (13)

The diagonal is one. On the cyclic ordering of the eight edges, M_ef
is one at distance one, one half at distance two, and zero farther away.

If adjacent edges have positive masses, fixing their sum makes z^T M z
linear in their split, since both diagonal entries and their mutual entry
are one. Move all of that mass to one endpoint with no increase of the
quadratic form. Repeating leaves a matching of the original cycle.
There are 47 matching supports, of size at most four. For sizes one or
two the form is at least half the squared total mass. For three edges,
the distance-two graph is either a path or one edge plus an isolated
vertex. The path form satisfies

    a^2+b^2+c^2+ab+bc - (a+b+c)^2/2
        = (a-c)^2/2+b^2/2 >=0.

For one edge plus an isolated vertex the sharp identity is

    a^2+b^2+ab+c^2 - 3(a+b+c)^2/7
        = (a-b)^2/4+[3(a+b)-4c]^2/28 >=0.                  (14)

Four matching edges alternate around the cycle. With their four variables
cyclically ordered, the form minus half their squared total is
[(z_0-z_2)^2+(z_1-z_3)^2]/2. These identities prove (12).

A different exact verification enumerates all 255 nonempty edge supports
I and solves

    M_II z=lambda 1,  sum z_i=1.                           (15)

Every global simplex minimizer satisfies one of these systems on its
positive support. In each consistent system lambda is unique: symmetry
of M identifies the two values from any two normalized solutions.
There are 247 consistent systems; all have lambda>=3/7, even without
imposing positivity on their solutions. Eight supports attain 3/7;
an explicitly positive three-edge flow gives the displayed sharp packet.
Singular and inconsistent systems are handled explicitly. This exhaustive
stationary check and the matching/SOS check are different finite proofs
of the same bound. Neither uses floating optimization.

## 4. Use and limits

At a fixed source test set E and volume, the common-set minimax problem
is convex in the atomic prior. Constraints (11) retain that convexity
while ensuring a positive, explicitly bounded second-energy signal by
(8) and (12). The zero-value face certificates prevent treating numerical
orientation errors at isometric priors as negative Gaussian witnesses.
They also give exact contact and first-variation checks for an optimizer.

The remaining problem still requires a negative **integrated** certificate,
or a positive argument covering all test sets and all relevant parameters.
No finite cubature or LP solver status supplies that conclusion. The
present pass's coarse numerical negatives did not survive finer and
different-rule checks and are not certified evidence. The certificate, universal proof and
exact finite coverage are the substantive artifact here. See [README.md](README.md)
and [SOURCES.md](SOURCES.md) for replay and attribution.
