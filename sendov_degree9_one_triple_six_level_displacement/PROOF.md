# Whole one-triple six-level displacement maximum and sharp phase basin

Actual author **six-sendov-2**, role **researcher**, 2026-10-01.
Complete ordinary written author proof with exact integer/rational evidence;
unformalized, independent review pending. Precise inputs and author credits
are in [LITERATURE.md](LITERATURE.md).

## 1. Angular statement and scope

For a balanced nonzero real eight-vector theta, write

    mu_k=sum theta_j^k, e=1/sqrt8, P=I-ee^T,
    C=P diag(theta)P on e-perp, w=diag(theta)e,
    Psi=sum_distinct_lambda ||Pi_lambda w||^4,
    J=122mu_2+(224mu_4-5760Psi)/mu_2.

Full eigenspace projections count all collisions. Normalize max|theta|=1.
Let F_(6,3) consist of all profiles with at most five actual values, and
all profiles with exactly six values of multiplicities3,1,1,1,1,1.
Equivalently it is the closed union of the prior five-level class and the
labelled3+1^5 cohort, retaining every coincidence. The six-level
2+2+1+1+1+1 cohort is not included.

Use the credited scalar data

    j(u)=(2058+21912u-15876u^2+19224u^3+3402u^4)
         /((3+u)(1+3u)^2),
    u_* = the unique global maximizing root on[0,1] in(2/25,9/100) of
          26634-231084u-907290u^2+376920u^3
          +971190u^4+224532u^5+30618u^6,
    J_*=j(u_*), theta_*=(1^3,-1^3,sqrt(u_*),-sqrt(u_*)).

Let O_* be the unit permutation orbit of theta_*. Reflection preserves
this multiset. The prior scalar result7572 supplies
J_*-j(u)>=450(u-u_*)^2 for0<=u<=1/4.

**Theorem 1.** Throughout F_(6,3),

    J<=J_*,
    J=J_* iff theta is a permutation of theta_*,
    dist(theta/sqrt(mu_2),O_*)^2<=5000(J_*-J).             (1)

The optimizer, scalar constant and earlier five-level theorem8124 are
credited. The new domain is the whole six-level one-triple cohort,
including singleton saturation while the triple lies inside the unit
interval. The prior saturated-triple theorem8236 is used for its boundary
lane. Seven exact simplex kernels and two elementary moment sections close
the new global cover. No whole-six-level, seven/eight-level or unrestricted
first-power Tang--Zhang result is asserted.

## 2. Complete ordered physical sections

For a genuine six-level profile, reflect and permute so its ordered levels
are x_1<...<x_6=1. Reflection sends C,w to-C,-w, preserving Psi and J.
Let r be the rank of the tripled level; m_i=1+2*1_(i=r).
If r=6, the positive unit triple is covered by8236. For r=1,...,5 set

    M_j=sum_(i<=j)m_i, d_j=x_(j+1)-x_j,
    a_j=M_j*d_j/8, j=1,...,5.

Balance is exactly sum_j M_j*d_j=8, since
sum_i m_i*x_i=8-sum_j M_j*d_j. Thus the complete closed section is

    a_j>=0, sum a_j=1, sum a_j/M_j<=1/4,
    x_i=1-sum_(j>=i)8a_j/M_j, x_6=1.                   (2)

The last inequality is exactly x_1>=-1. Conversely (2) reconstructs every
ordered physical profile, including ties. No translation, extremal
normalization beyond reflection, or unproved boundary reduction is used.
All these sections have mu_2>=8/7 by the singleton+1 and Cauchy--Schwarz.
Their cumulative sequences are

    r1:(3,4,5,6,7), r2:(1,4,5,6,7), r3:(1,2,5,6,7),
    r4:(1,2,3,6,7), r5:(1,2,3,4,7).

The complete vertices are e_j with M_j>=4, and for M_j<4<M_k,

    p_jk = gamma e_j+(1-gamma)e_k,
    gamma=M_j*(M_k-4)/(4*(M_k-M_j)).                    (3)

Away from the clipping plane a vertex has one positive coordinate. On
that plane it has at most two: three positive coordinates leave a nonzero
small tangent satisfying the two affine equalities. Such a tangent and
its negative are feasible, contradicting extremality. This proves
completeness of (3); neutral M_j=4 gives an already listed unit vertex.
Exact arithmetic checks all36 vertices, counts7,7,9,8,5, against (2).

For r1 and r2 put e2=e_2,e3=e_3,e4=e_4,e5=e_5 and
p3=p_13,p4=p_14,p5=p_15. Their full sections have the three simplices

    A0=(e2,e3,e4,e5,p5),
    A1=(e2,e3,e4,p4,p5),
    A2=(e2,e3,p3,p4,p5).                               (4)

Here is an explicit algebraic coverage proof. Put
eta_j=M_1*(M_j-4)/(M_j*(4-M_1)), j=3,4,5.
The clipping condition says a_1<=sum_(j=3)^5 eta_j*a_j.
Allocate the mass a_1 greedily to j=5, then4, then3:

    if a_1<=eta_5*a_5: z_5=a_1/eta_5, z_4=z_3=0;
    else if a_1<=eta_5*a_5+eta_4*a_4:
       z_5=a_5, z_4=(a_1-eta_5*a_5)/eta_4, z_3=0;
    else: z_5=a_5, z_4=a_4,
       z_3=(a_1-eta_5*a_5-eta_4*a_4)/eta_3.

Then 0<=z_j<=a_j and a_1=sum eta_j*z_j. Assign weight a_2 to e2,
weight a_j-z_j to e_j and weight(1+eta_j)z_j to p_j. These weights
sum to1 and reconstruct a exactly. In the three cases their support
is respectively A0,A1,A2, proving complete coverage. All full5x5 inverse
coordinate identities are checked against independent Gaussian inversion.
For rank1 only, reorder A2 as(e2,p3,e3,p4,p5) to expose its scalar edge.
Rank5's five vertices in (3) form a single four-simplex. All positive
simplex coordinates in these seven kernels give genuine six ordered
levels; the other faces are retained in the final extension.

## 3. Two middle-rank sections need no polynomial cover

If theta has k distinct values, split R^8 into vectors constant on each
value block and vectors summing to zero within each block. Both spaces
are invariant under diag(theta),P and C. The vector w lies in the first
space and in e-perp, whose dimension is k-1. Thus its spectral weights
are supported at no more than k-1 eigenvalues, even at collisions.
Cauchy--Schwarz gives

    Psi>=||w||^4/(k-1)=mu_2^2/(64(k-1)).

For k<=6 and max|theta|=1, mu_4<=mu_2, so

    J<=104mu_2+224.                                    (5)

The squared norm mu_2 is convex in a. Checking all9 vertices of rank3
and all8 vertices of rank4 in (3) gives mu_2<=16/3 throughout those
closed sections. Therefore both satisfy

    J<=2336/3<785753/1000.                             (6)

This is a universal invariant-block argument and a complete convex
vertex bound, not a finite sampling argument.

## 4. Full filtered compression and exact integer targets

Credit8194 for the filter B_i=C^i(I-C^2),i=0,1,2. Write
s_j=tr(C^j),s_0=7,b_i=w^T C^i w and

    G_ij=s_(i+j)-2s_(i+j+2)+s_(i+j+4),
    r_i=b_i-b_(i+2), D=det G, N=r^T adj(G)r.

The pinching of ww^T onto the full symmetric commutant has squared
Frobenius norm Psi. The B_i belong to that commutant; projecting onto
their span proves Psi>=N/D whenever D>0. Colliding eigenspaces are never
arbitrarily divided into separate weights.

For six distinct slopes, h(y)=prod_i(y-x_i)^(m_i) satisfies
det(yI-C)=h'(y)/8. Rolle gives five distinct roots between the six
levels, all inside(-1,1); the remaining two eigenvalues equal the
tripled level. At those five roots the filter1-y^2 is nonzero. A
nonzero quadratic cannot vanish at five sites, so the Gram is positive
in every simplex interior. No singular boundary quotient is taken.

For each simplex let b_0,...,b_4 be its homogeneous coordinates,
H=sum b_i and L the common denominator of its six literal vertex
levels. The expanded integer root forms T consist of

    T_i=L*sum_v b_v*x_i(vertex_v), with T_r repeated3,
    the other T_i once; sum T=0 and T_6=L H.

The scales are70 for rank5,105/15/10 for rank2 A0/A1/A2, and210/30/30
for rank1 A0/A1/A2. Let m_j=sum T_i^j, M=8C_T. Generate
s_j^M=tr(M^j),j1..8, by all cyclic rank-one words in P=I-ee^T:
a word with q rank-one factors at positive cyclic gaps g_i contributes
(-1)^q 8^(j-q)prod m_(g_i); the empty word contributes8^j m_j.
Set s_0^M=7. The coupling numerators v_i=T^T M^i T are

    m2, 8m3, 64m4-8m2^2, 512m5-128m2m3,
    4096m6-512(2m2m4+m3^2)+64m2^3.

Define

    A_ij=(8LH)^4 s_(i+j)^M-2(8LH)^2 s_(i+j+2)^M+s_(i+j+4)^M,
    R_i=(8LH)^2 v_i-v_(i+2),
    D_int=det A, N_int=R^T adj(A)R,
    F=[785753(LH)^2 m2-122000m2^2-224000m4]D_int+90000N_int.

These have degrees18,22,22 respectively. At H=1,

    D_int=(8L)^18 D, N_int=64L^4(8L)^18 N,
    F=1000L^4(8L)^18[(c mu2-122mu2^2-224mu4)D+5760N],
    c=785753/1000.                                    (7)

Thus F>=0 implies J<=c in the interior. All integer polynomials are
regenerated from the full root forms. In rank5 and rank2 A0/A1/A2 and
rank1 A0/A1, **all14950 degree22 homogeneous coefficients per simplex
are nonnegative**. This gives six complete strict kernels,89700 signs,
without a recursive cover. The last rank1 simplex is handled next.

## 5. The optimizer-containing simplex: exact grouped strict/local cover

Use coordinates(b0,b1,b2,b3,b4) at(e2,p3,e3,p4,p5), respectively.
The edge(b0,b1,0,0,0) is exactly the credited face
(-1^3,1^3,t,-t),t=b0/(b0+b1). Set

    q=b2+b3+b4, t=b0/(1-q), z_i=b_(i+2)/q,

for0<q<1, and group the homogeneous degree22 target by
gamma=(exponent of b2,b3,b4),k=|gamma|:

    F=sum_gamma q^k(1-q)^(22-k)z^gamma P_gamma(t),
    P_gamma(t)=sum_i c_(i,22-k-i,gamma)t^i(1-t)^(22-k-i). (8)

The complete monomial dictionary is reconstructed from these groups.
The exact structural facts are:

* All14535 original coefficients of transverse degree k>=4 are
  nonnegative; exactly five are zero.
* All19 polynomials with k=1,2,3 are nonnegative throughout[0,1],
  certified on[0,1/4],[1/4,1/3],[1/3,1].
* P0 is nonnegative on[0,147/500] and[37/125,1]; the lower interval
  is split at1/4 and the upper at1/3.
* For each of the three unit gamma,119999P0+P_gamma is strictly positive
  on[147/500,37/125], with a split at59/200. The degree21 first-order
  polynomial is elevated to degree22 by a fully checked identity.

All scalar signs use complete exact Bernstein tables and complete
inverse conversions. Nonnegative basis functions sum to one, including
closed interval endpoints. There are1176 low-group entries,92 outer-face
entries and138 strict domination entries, plus14535 high entries:
15941 exact grouped signs,61 scalar tables and6 domination tables.
Together with the six strict kernels the certificate checks105641
target signs. No floating point or incomplete traversal supplies a sign.

Let L=sum_i z_i P_(e_i). All k>=2 contributions are nonnegative, so

    F>=(1-q)^21[(1-q)P0+qL].                            (9)

Outside the central t interval, P0,L>=0. Inside it, L>=0 and
119999P0+L>0. For q>=1/120000 the identity

    (1-q)P0+qL
       =[(1-q)(119999P0+L)+(120000q-1)L]/119999

proves F>=0, hence J<=c by (7) in the interior.

For central t and q<=1/120000 use the credited all-balanced local
theorem7823, which allows both unit triples to move. In this simplex,
the negative triple deficit is2b2/5 in each entry. The positive triple
deficits are(2b3/3+b4/2,b4/2,0). The remaining pair has half-difference
x=b0 and mean one half the positive-minus-negative deficit difference.
Thus the total deficit and pair difference are

    S=(6/5)b2+(2/3)b3+b4<=(6/5)q<=1/100000,
    x=(1-q)t in[(119999/120000)(147/500),37/125].

The squared lower endpoint is at least2/25 and the squared upper
endpoint is at most9/100. Balance and max normalization already hold.
Every point in this closed region therefore satisfies the precise7823
hypotheses, giving

    J_*-J>=200S+450(x^2-u_*)^2,
    dist(theta/sqrt(mu2),O_*)^2<=(J_*-J)/90.             (10)

This is an exact whole-region mapping, not a sampled local label.
The larger fixed-triple tube8194 cannot be used in this region because
the negative triple may move; its full filter is separately credited.

## 6. Closure, equality and global direction stability

The credited scalar maximum and exact rational evaluation give

    J_*-c>=j(87/1000)-c
          =1331662697/1636234509000>1/1250.              (11)

All strict kernels and middle-rank sections have J<=c. Squared distance
between two unit vectors is at most4, so (11) gives
dist^2<5000(J_*-J) there. The local region (10) gives the same weaker
global coefficient5000. Hence every simplex-interior profile satisfies
the two bounds in (1).

For closure, C and w vary continuously. Around each distinct limiting
eigenvalue take a disjoint spectral interval with nonspectral endpoints.
Its full cluster projection is continuous, while its nonnegative split
weights satisfy sum r_i^2<=(sum r_i)^2. Therefore

    limsup Psi(theta_n)<=Psi(theta),
    J(theta)<=liminf J(theta_n).

Here mu2 is bounded away from zero. Unit-orbit distance is continuous,
so both J<=J_* and dist^2<=5000(J_*-J) extend from each simplex interior
to every closed boundary. No singular determinant is divided by.
The middle-rank sections are already closed by (5)-(6), rank6 uses8236,
and every profile with at most five actual values uses8124. Equations
(2)-(4) give complete six-level coverage, proving (1) on all F_(6,3).

If J=J_*, the distance is zero, so theta is a positive scalar multiple
of a permutation of theta_*. Max normalization forces the scalar to1.
Conversely the credited scalar face attains J_*. Thus attainment and
the complete equality classification follow. The constant5000 is
conservative, and the optimizer itself is not new.

## 7. Sharp complex six-phase one-triple displacement basin

Let p(z)=b(z-a)prod8(z-z_j),b!=0, have a simple marked real root
0<a<1 and other roots in the closed unit disk. Count all original and
critical algebraic multiplicities. Coefficients may be complex. Put

    G_a=sum_(p'(zeta)=0)|a-zeta|^-1-16/(1+a),
    rho_p=max_j|z_j+1|, kappa=(1+a)(a-5/8), d0=13/8.

For rho_p<=1/2 there are unique small principal real phases in
z_j=-(1-tau_j)exp(i phi_j),tau_j>=0. Require at most five phase values,
or exactly six phase values with one of multiplicity three. The eight
depths are independent, including within equal-phase blocks. Let R_(6,3)(a)
be the supremum of radii r in[0,1/2] such that every polynomial in this
class with rho_p<=r has G_a>=0. Endpoint admissibility is not assumed.

**Corollary 2.** The complete phase class has the sharp leading basin

    lim_(a downarrow5/8) R_(6,3)(a)^2/kappa
         =B_*=106496/(5J_*).                            (12)

The constant and four/five-phase matching family are credited. The new
conclusion is their validity across the full six-phase one-triple class
with arbitrary independent inward depths.

The joint all-disk bootstrap/expansion7534 and original-root variational
reduction7641 are explicit analytic inputs. Put

    T=sum tau_j, M=sum phi_j,
    s=||phi-(M/8)1||, eta=(phi-(M/8)1)/s,
    q=max eta_j^2, p8=10985/33554432,
    E=sum|(a-z_j)^-1-(1+a)^-1|^2.

Uniformly on negative-gap sequences with a decreasing to5/8 and
rho_p tending to zero, they give s>0, T=O(s^4),M^2=O(s^4),kappa=O(s^2),
and

    G_a=kappa E+(128/169)T+(40/2197)M^2-K(eta)E^2+o(E^2),
    rho_p^2/E=d0^4 q+o(1), K(eta)/q=p8 J(eta/sqrt(q)),
    q>=1/8, d0^4/p8=106496/5.                          (13)

Their uniformity includes moving directions, independent depths, phase
means and critical collisions; it is not inferred from fixed-ray series.
Centering and scaling preserve phase multiplicities. Theorem1 bounds
K/q by p8J_*. If G_a<0, dropping nonnegative penalties in (13) gives
kappa/E<=K+o(1). Combined with q>=1/8 and the metric conversion, this
forces liminf rho_p^2/kappa>=B_* (the sequential argument of7641).
Thus each squared radius(B_*-epsilon)kappa is eventually valid, proving
the liminf in (12). Displacement zero has G_a=0.

The new phase class contains the entire prior five-phase class, so
R_(6,3)<=R5. The credited sharp five-phase limit8124 gives the reverse
limsup. Its matching theta_* direction has only four phases and belongs
to the new class. This proves (12) without inventing a new failure family.

**Corollary 3.** Every negative-gap sequence in this phase class with
a downarrow5/8 and rho_p^2/kappa->B_* satisfies

    T/E^2->0, M^2/E^2->0,
    dist(eta,O_*)->0, G_a/E^2->0.                       (14)

Indeed (13) and the prescribed displacement ratio imply

    G_a/E^2=p8 q(J_*-J(eta/sqrt(q)))
               +(128/169)T/E^2+(40/2197)M^2/E^2+o(1).

All displayed terms are nonnegative. Negativity forces each to zero;
q>=1/8 and (1), noting theta/sqrt(mu2)=eta for theta=eta/sqrt(q),
give the direction conclusion. This extends the near-sharp geometric
selection across the full six-phase one-triple class.

No effective cutoff, finite-radius transition or sign at the asymptotic
endpoint is provided. These are collapsed-baseline stability statements:
at the cutoff that baseline is128/13>8. Negative G is not a counterexample
to the unrestricted first-power inequality.

## 8. Evidence and trust boundary

The standalone standard-library source regenerates every integer target
and every coefficient sign. It checks full section vertices and greedy
inverse matrices, complete grouped reconstruction, scalar inverse basis
conversions and degree elevations. Forty-six rational controls construct
literal full8x8 compressions, moments, eight traces, five coupling moments,
all nine filtered Gram entries and all integer scalings. Their full
symmetric-commutant projection uses28 equations in36 variables with
correct Frobenius weights to recover defining Psi independently of the
moment quotient. Nonsingular controls use a separate Gaussian solve;
singular controls check cleared numerators without division. The local
face, closed mass cutoff, split triples and collisions are included.

These finite author controls support universal written identities; they
do not replace the invariant-block, convexity, coverage, Rolle, projection,
collision or analytic bootstrap arguments. The credited scalar, local,
five-level, saturated-triple and joint analytic statements are external
mathematical inputs. Exact Python and ordinary bridges remain outside a
formal kernel. A compact manifest is mandatory and compared in full.
No private module, large coefficient array, float sign, external solver
or network proof input is used. Independent review is pending.

All seven kernels were freshly regenerated under normal and optimized
execution, with the entire selected case and common section record
compared to the mandatory fixture. The complete union in each mode
reconstructs the same110502-check mathematical record and105641 signs;
all five missing/damaged fixture cases reject in each mode. The collector
audits existing records and does not itself rederive their mathematics or
authenticate an external run. See README.md for the exact bounded commands
and measured evidence. The default entire-regeneration path is retained.

For exact rational evaluation the implementation writes each coordinate
x_j=u_j/B, using a common positive integer denominator B. An integer
monomial c*x^alpha of total degree d becomes c*u^alpha/B^d. Clearing all
terms to B^D, D=max total degree, and summing integer numerators recovers
the identical polynomial value, including mixed degrees, negative
coordinates and zeros. Caching integer powers changes only repeated
arithmetic, not any coefficient, sign, full control or trust boundary.
