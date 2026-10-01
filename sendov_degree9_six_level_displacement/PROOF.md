# The complete six-level displacement maximum and sharp complex phase basin

Actual author **six-sendov-2**, role **researcher**, 2026-10-01.
Complete ordinary written author proof with exact computational coefficients;
unformalized, independent review pending. [LITERATURE.md](LITERATURE.md)
identifies the precise inputs, source commits and original authors.

## 1. The complete angular result

For a balanced nonzero real eight-vector theta, set

    mu_k=sum theta_i^k, e=1/sqrt8, P=I-ee^T,
    C=P diag(theta)P on e-perp, w=diag(theta)e,
    Psi=sum_distinct_lambda ||Pi_lambda w||^4,
    J=122mu2+(224mu4-5760Psi)/mu2.

Every Pi is a full eigenspace projection, including all collisions.
Normalize max|theta_i|=1. Let F6 be the entire class of such vectors
with **at most six distinct actual values**. No block multiplicity or
endpoint saturation condition is imposed beyond this normalization.

Use the credited scalar data7572:

    j(u)=(2058+21912u-15876u^2+19224u^3+3402u^4)
         /((3+u)(1+3u)^2),
    u_* = unique global maximizing root on[0,1], in(2/25,9/100), of
          26634-231084u-907290u^2+376920u^3
          +971190u^4+224532u^5+30618u^6,
    J_*=j(u_*), theta_*=(1^3,-1^3,sqrt(u_*),-sqrt(u_*)).

Let O_* be the permutation orbit of the unit-normalized theta_*.
Reflection already preserves this multiset. The same scalar input gives
J_*-j(u)>=450(u-u_*)^2 for0<=u<=1/4.

**Theorem 1.** Every theta in F6 satisfies

    J(theta)<=J_*,
    J(theta)=J_* iff theta is a permutation of theta_*,
    dist(theta/sqrt(mu2),O_*)^2<=1536(J_*-J(theta)).      (1)

The scalar optimizer and constant retain their prior credit. The new
domain is the **whole** at-most-six-level class. The one-triple input8336
covers at most five values and the full six-level3+1^5 cohort. Input8388
covers eleven closed ordered2+2+1^4 sectors strictly below J_*. The new
twelve kernels below cover all four remaining sectors. The published independent audit by six-reviewer-3 confirms the new
one-triple extension through its stated prior-premise boundary and
strengthens its coefficient to1536. Older exhaustive five-level and
saturated-triple covers remain cited premises. The eleven strict sectors
and the present twelve new kernels await independent review.
Seven/eight-level global optimization remains open here.

## 2. Four whole physical sections and a reversed-row cover

A genuine six-level eight-vector has either multiplicities3+1^5 or
2+2+1^4: distribute the two entries beyond one per level. Reflect and
permute it so its ordered levels satisfy x6=1. Reflection sends C,w
to-C,-w and preserves Psi,J. Write(r,s) for the two doubled ranks.
Input8388 excludes every such section except

    (1,5),(1,6),(2,5),(2,6).                            (2)

For one of these pairs set m_i=1+1_(i in{r,s}), M_j=sum_(i<=j)m_i and
a_j=M_j(x_(j+1)-x_j)/8 for j1,...,5. The complete closed section is

    a>=0, sum a=1, sum a_j/M_j<=1/4,
    x_i=1-sum_(j>=i)8a_j/M_j, x6=1.                   (3)

Indeed balance is sum M_j(x_(j+1)-x_j)=8; the last inequality is
exactly x1>=-1. Conversely(3) reconstructs every physical vector,
including ties. One coordinate is1 and the other seven sum to-1,
so mu2>=8/7. The cumulative sequences are

    pair       M1 M2 M3 M4 M5
    (1,5)       2  3  4  5  7
    (1,6)       2  3  4  5  6
    (2,5)       1  3  4  5  7
    (2,6)       1  3  4  5  6.

The full vertices are e3,e4,e5 and p14,p15,p24,p25, where

    p_ij=gamma e_i+(1-gamma)e_j,
    gamma=M_i(M_j-4)/(4(M_j-M_i)), i in{1,2},j in{4,5}. (4)

Completeness follows as in8388: off the clipping plane a vertex has
one positive coordinate; three positive coordinates on the plane admit
a nonzero tangent preserving both affine equalities. Both signs of a
small tangent remain feasible, contradicting extremality. M3=4 gives
the neutral e3 directly.

For all four sections use the same three ordered four-simplices

    A0=(e3,e4,e5,p15,p25),
    A1=(e3,e4,p14,p15,p25),
    A2=(e3,p24,e4,p14,p25).                            (5)

Here is a complete coverage proof, retaining zero flows and collisions.
Put c_i=4/M_i-1>0 for i1,2 and d_j=1-4/M_j>0 for j4,5. Clipping says
sum c_i a_i<=sum d_j a_j. Give rows2,1 these respective demands,
then add a dummy row with the nonnegative surplus. Order columns5,4.
Greedily allocate the smaller remaining row demand or column supply.
Every allocation is nonnegative and exhausts the demands and supplies.
Ties and zero masses permit either move; append zero allocations to
complete a path. There are precisely three monotone3-by2 paths:

    down,down,right: p25,p15,e5,e4;
    down,right,down: p25,p15,p14,e4;
    right,down,down: p25,p24,p14,e4.

A true flow f at(i,j) gives weight f(1/c_i+1/d_j) at p_ij, contributing
f/c_i to a_i and f/d_j to a_j. A dummy flow gives weight f/d_j at e_j.
Add a3 at e3. These weights reconstruct every coordinate of a, hence
sum to1. Their supports are exactly(5), proving whole-section coverage.
This is the classical staircase transport argument credited in8388,
with the two low rows reversed; no new general triangulation is claimed.

The exact source checks all28 section vertices, all twelve full5-by5
inverse matrices and every row/column/dummy identity on an entire
five-coordinate basis. Positive barycentric coordinates give all five
physical gaps positive. Only A2 has the edge(e3,p24), whose profiles are
(-1^3,-t,t,1^3). The physical face a1=a5=0 and clipping equality has
exactly these two vertices. The scales L below are

    pair       A0 A1 A2
    (1,5)      70 30 30
    (1,6)      15 15 15
    (2,5)      70 10 10
    (2,6)      15 30 30.

## 3. Full filtered projection and the twelve integer kernels

Credit8194 for B_i=C^i(I-C^2),i0,1,2, acting on the full seven-dimensional
space e-perp. With s_j=tr(C^j),s0=7 and b_i=w^T C^i w, set

    G_ij=s_(i+j)-2s_(i+j+2)+s_(i+j+4),
    r_i=b_i-b_(i+2), D=det G, N=r^T adj(G)r.

The pinching of ww^T onto the full symmetric commutant of C has squared
Frobenius norm Psi. The B_i belong to that commutant, so projection onto
their span gives Psi>=N/D for D>0. No colliding eigenspace is divided into
artificial separate weights.

For six distinct levels h(y)=prod(y-x_i)^m_i satisfies
det(yI-C)=h'(y)/8. Rolle gives five distinct eigenvalues strictly between
the six levels, inside(-1,1). The additional eigenvalues are the doubled
levels. A nonzero quadratic times1-y^2 cannot vanish at all five Rolle
sites. Thus G is positive definite in each simplex interior. No singular
boundary quotient is used.

For one simplex let b0,...,b4 be its homogeneous coordinates, H=sum b
and L the least common denominator of its six literal level vertices.
Expand the eight integer root forms T_i=L sum_v b_v x_i(vertex_v), using
the given multiplicities. Then sum T=0 and its largest level is L H.
Put m_j=sum T_i^j and M=8C_T. The public8336 cyclic rank-one word source
regenerates all traces s_j^M=tr(M^j),j1,...,8, with s0^M=7. Its full
coupling numerators v_i=T^T M^i T are

    m2,8m3,64m4-8m2^2,512m5-128m2m3,
    4096m6-512(2m2m4+m3^2)+64m2^3.

Define the complete integer polynomials

    A_ij=(8LH)^4 s_(i+j)^M-2(8LH)^2 s_(i+j+2)^M+s_(i+j+4)^M,
    R_i=(8LH)^2 v_i-v_(i+2),
    D_int=det A, N_int=R^T adj(A)R,
    F=[785753(LH)^2 m2-122000m2^2-224000m4]D_int+90000N_int.

Their degrees are18,22,22. At H=1 the exact normalization is

    D_int=(8L)^18 D, N_int=64L^4(8L)^18 N,
    F=1000L^4(8L)^18[(c mu2-122mu2^2-224mu4)D+5760N],
    c=785753/1000.                                    (6)

Consequently F>=0 gives J<=c in the simplex interior. In all eight
A0/A1 cells, every one of the14950 degree22 coefficients is nonnegative:
119600 complete coefficient signs, with344 zeros. Thus these eight
entire cells are strictly below J_*, using the retained exact scalar gap

    J_*-c>=j(87/1000)-c
          =1331662697/1636234509000>1/1250.             (7)

## 4. Four optimizer cells: grouped strict regions and one uniform local map

In A2 use the ordered coordinates(b0,b1,b2,b3,b4) at(e3,p24,e4,p14,p25).
For0<q=b2+b3+b4<1 put t=b0/(1-q), z_i=b_(i+2)/q. Group every degree22
coefficient by gamma=(exponents of b2,b3,b4),k=|gamma|:

    F=sum_gamma q^k(1-q)^(22-k)z^gamma P_gamma(t),
    P_gamma(t)=sum_i c_(i,22-k-i,gamma)t^i(1-t)^(22-k-i). (8)

The source reconstructs the whole target from this dictionary. For
**each of the four distinct kernels**, its complete exact certificates
establish the following statements:

* All14535 coefficients with k>=4 are nonnegative, with five zeros.
* All19 P_gamma with k1,2,3 are nonnegative on[0,1], using complete
  Bernstein tables on[0,1/4],[1/4,1/3],[1/3,1].
* P0 is nonnegative on[0,147/500] and[37/125,1], split at1/4 and1/3.
* For each unit gamma,119999P0+P_gamma is strictly positive on
  [147/500,37/125], split at59/200. Exact degree elevation matches
  the entire degree21 first-order polynomial to degree22.

Every scalar table has a full exact inverse coefficient conversion;
there are no floating sign inputs or sampled inferences. Per cell there
are61 ordinary scalar tables,6 domination tables and15941 target signs.
Across all four cells these give58140 high signs,5072 ordinary scalar
signs and552 strict domination signs. Together with the eight strict
kernels, the new certificate checks183364 complete target signs.

Put V=sum_i z_i P_(e_i). All k>=2 contributions are nonnegative, so

    F>=(1-q)^21[(1-q)P0+qV].                           (9)

Outside the central t interval, P0,V>=0. Inside it, V>=0 and
119999P0+V>0. For q>=1/120000 the exact identity

    (1-q)P0+qV
     =[(1-q)(119999P0+V)+(120000q-1)V]/119999

gives F>=0, hence J<=c in every strict interior region.

It remains to cover central t with q<=1/120000. Expand the physical
roots in their ordered order: the first three lie in the lower unit
cluster, two are the middle pair, and the last three lie in the upper
unit cluster. Both triples may move. Let

    S=sum_first3(1+theta_i)+sum_last3(1-theta_i),
    x=(theta_5-theta_4)/2.

All deficits are nonnegative by(3). The **entire affine identities** are

    S=(6/5)b2+alpha b3+beta b4, x=b0,
    pair       alpha beta
    (1,5)       2/3   1
    (1,6)       2/3  2/3
    (2,5)        1    1
    (2,6)        1   2/3.                             (10)

For example, these follow at every vertex from(3), and then for every
barycentric point by affinity. More generally
alpha=2(3-M1)/(5-M1), beta=2(M5-5)/(M5-3).
The checker compares both full identities at every one of the five
literal vertices, not at selected interior points. Balance also forces
the middle pair's mean to be half the upper-minus-lower total deficit.
Its two singleton levels and the double-plus-single unit clusters have
exactly the labels needed by the all-balanced local chart7823.

Uniformly for all four maps,

    S<=(6/5)q<=1/100000,
    x=(1-q)t in[(119999/120000)(147/500),37/125],
    2/25<=x^2<=9/100.                                 (11)

The endpoint inequalities are exact rational checks. Relabel the upper
triple first, the lower triple next and the larger middle coordinate
before the smaller. The vector now satisfies every7823 hypothesis:
balance, max norm1, nonnegative deficits, x>=0, the S cutoff and the
scalar interval. That input allows arbitrary splitting of both triples,
and gives throughout the whole closed local region

    J_*-J>=200S+450(x^2-u_*)^2,
    dist(theta/sqrt(mu2),O_*)^2<=(J_*-J)/90.            (12)

The larger fixed-triple local tube8194 is not used in(12). It cannot
replace7823 here because the lower triple also moves.

## 5. Collision closure, equality and whole-six-level stability

Use the sharper orbit argument from **six-reviewer-3's published
one-triple audit**, with its original credit. For balanced unit vectors
v,x, averaging coordinate permutations sigma gives covariance diagonal
1/8 and off-diagonal-1/56, hence E[(x^T sigma v)^2]=1/7. Some permutation
has absolute correlation at least1/sqrt7>3/8. Take v to be the normalized
theta_*; its permutation orbit is centrally symmetric. The positive
correlation is therefore available, so every balanced unit x satisfies

    dist(x,O_*)^2<=2-2/sqrt7<5/4.

Let delta=j(87/1000)-c, the exact rational value in(7). The same credited
argument and exact strict gap give, in every new strict interior region,

    dist^2<=[5/(4delta)](J_*-J),
    5/(4delta)=2045293136250/1331662697<1536,
    1536*1331662697-2045293136250=140766342>0.           (16)

Equation(12) gives coefficient1/90 in the local region. Both bounds
therefore imply the coefficient1536 in(1) in every new cell interior.
The elementary permutation covariance lemma and its1536 application on
the one-triple class retain reviewer credit; its application to the new
whole-six-level class is the present extension. The separate
verify_metric.py checks the full rational covariance and exact margin.

Approach a boundary with positive barycentric points. C and w converge.
Around each distinct limiting eigenvalue choose a disjoint spectral
interval with nonspectral endpoints. Its whole cluster projection is
continuous. Nonnegative split weights satisfy sum r_i^2<=(sum r_i)^2,
so limsup Psi(theta_n)<=Psi(theta). Since mu2>=8/7,

    J(theta)<=liminf J(theta_n).

Unit-orbit distance is continuous; both inequalities therefore extend
to every boundary, including q0,q1, collisions, clipping equality and
singular Gram matrices. No singular determinant is divided by. The
whole transport cover(5), reflection and permutation treat all four
sections(2).

Input8388 supplies J<=c on all eleven other two-double sections, so(16)
strengthens their distance coefficient to1536 as well. The published
one-triple audit supplies the same1536 conclusion on the entire one-triple
and at-most-five-level classes, through its expressly cited older-cover
premise boundary. Those complete input classes and the new cells exhaust F6.
This proves the two bounds in(1). If J=J_*, the unit-orbit distance is
zero, so theta is a positive scalar multiple of a permutation of theta_*.
Max normalization fixes that scalar to1. Conversely the credited scalar
face attains J_*, proving the equality statement. The constant1536 is
conservative; its previous one-triple application retains reviewer credit.
No new equality vector is claimed.

## 6. The complete complex six-phase displacement basin

Let p(z)=b(z-a)prod8(z-z_j),b!=0, with a simple marked real root0<a<1
and all other roots in the closed unit disk. Original and critical
algebraic multiplicities are counted. Coefficients may be complex. Set

    G_a=sum_(p'(zeta)=0)|a-zeta|^-1-16/(1+a),
    rho_p=max_j|z_j+1|, kappa=(1+a)(a-5/8), d0=13/8.

For rho_p<=1/2, write uniquely z_j=-(1-tau_j)exp(i phi_j) using the small
principal real phases and tau_j>=0. Require **at most six distinct phase
values**, with arbitrary independent depths, including inside each
equal-phase block. Let R6(a) be the supremum of radii r in[0,1/2] such
that every polynomial in this phase class with rho_p<=r has G_a>=0.
Admissibility of the supremum itself is not assumed.

**Corollary 2.** The complete complex phase class has

    lim_(a downarrow5/8) R6(a)^2/kappa
      =B_*=106496/(5J_*).                              (13)

The constant and matching four-phase family are credited. The new
conclusion is their validity for the whole six-phase class with
independent depths. It follows by the original-root analytic inputs7534
and7641 and the enlarged angular domain(1); those inputs are not
inferred from raywise Taylor series or finite coefficient controls.

For clarity, put T=sum tau_j,M=sum phi_j,
s=||phi-(M/8)1||,eta=(phi-(M/8)1)/s,q=max eta_i^2,
p8=10985/33554432 and
E=sum|(a-z_j)^-1-(1+a)^-1|^2. Those inputs give, uniformly on negative-G
sequences with a downarrow5/8 and rho_p tending to zero,
s>0,T=O(s^4),M^2=O(s^4),kappa=O(s^2), and

    G_a=kappa E+(128/169)T+(40/2197)M^2-K(eta)E^2+o(E^2),
    rho_p^2/E=d0^4 q+o(1), K(eta)/q=p8 J(eta/sqrt(q)),
    q>=1/8, d0^4/p8=106496/5.                          (14)

Centering and scaling preserve at most six phase values. Theorem1
therefore gives K/q<=p8J_*. Dropping the nonnegative penalties when
G_a<0 yields kappa/E<=K+o(1). Equations(14) and q>=1/8 force
liminf rho_p^2/kappa>=B_*; division is justified since kappa/E>0 and
the upper denominator bound tends to p8qJ_*, uniformly positive. Thus
every squared radius(B_*-epsilon)kappa is eventually admissible,
proving the liminf in(13). The collapsed point itself has G_a=0.

The six-phase class contains the five-phase class. Its radius is at
most the credited five-phase radius8124, whose sharp limit supplies
the reverse limsup. The matching theta_* direction has only four phase
values and belongs to the new class. This proves(13).

**Corollary 3.** Every negative-G sequence in this phase class with
a downarrow5/8 and rho_p^2/kappa->B_* satisfies

    T/E^2->0, M^2/E^2->0,
    dist(eta,O_*)->0, G_a/E^2->0.                       (15)

Indeed the prescribed ratio and(14) imply

    G_a/E^2=p8 q[J_*-J(eta/sqrt(q))]
             +(128/169)T/E^2+(40/2197)M^2/E^2+o(1).

Every displayed term is nonnegative. Negativity forces them all to
zero. The bound q>=1/8 and(1) give the direction conclusion, since
theta/sqrt(mu2)=eta for theta=eta/sqrt(q). This proves(15) with moving
directions, independent depths, means and critical collisions, as
allowed by the cited analytic inputs.

There is no effective cutoff, endpoint admissibility or unrestricted
first-power proof here. These compare with the collapsed baseline:
at a5/8 that baseline is128/13>8. A negative G is not a first-power
counterexample. Seven/eight-phase global directions remain unresolved.

## 7. Exact evidence and trust boundary

The public standard-library source regenerates all twelve integer
targets, all183364 signs, all28 vertices and all full transport inverses.
It checks every grouped reconstruction, scalar inverse conversion,
degree elevation and the whole physical affine maps. The mandatory
complete compact fixture records every case and full rational control.
The new twelve-cell record contains195974 mathematical checks.
A separate exact metric supplement checks the credited covariance and
1536 strict-gap application; it does not regenerate any target kernel.

Eighty-eight full rational controls construct literal8-by8 compressions,
eight traces, five coupling moments, all nine filtered Gram entries,
determinant/adjugate scalings and the defining full commutant projection.
The latter solves the full36-variable symmetric-commutant system with
correct Frobenius weights; it retains repeated eigenspaces. A separate
Gaussian solve checks nonsingular quotients. Singular controls check
cleared numerators without division. Local mass cutoffs, both moving
clusters and the scalar face are included. Complete(1,5) control rows
also agree literally with the credited8336 control algorithm.

The new cover openly adapts the public8388 transport and8336 exact
trace/filter code, with both executable hashes pinned. These are
repository-local dependencies, not private data or independent review.
The previous39 strict and seven one-triple kernels are retained inputs;
they are not claimed as freshly rederived by this new executable.

Exact arithmetic and the ordinary transport, Rolle, projection,
spectral-cluster closure, scalar/local transfer and phase bootstrap
arguments remain outside a formal kernel. Author controls do not prove
these universal bridges by sampling. See README.md for full fresh
normal/optimized reproduction, complete record comparison and measured
cost. A collector audits supplied records and neither regenerates
their mathematics nor authenticates an externally claimed run.
