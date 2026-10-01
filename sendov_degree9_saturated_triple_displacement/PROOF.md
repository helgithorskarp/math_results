# Exact displacement maximum with a saturated triple

Actual author **six-sendov-2**, role **researcher**, 2026-10-01.
Complete ordinary author proof with exact rational/integer certificates;
unformalized, independent review pending. The angular functional, scalar
optimizer and the local tube are credited inputs in
[LITERATURE.md](LITERATURE.md).

## 1. Claim

Let theta be a balanced nonzero real eight-vector, max-normalized by
max|theta_j|=1. Assume at least three coordinates equal 1, or at least
three equal -1. Put mu_k=sum theta_j^k, e=1/sqrt(8), P=I-ee^T,
C=P diag(theta)P on e-perp, w=diag(theta)e, and

    Psi=sum over distinct lambda of ||Pi_lambda w||^4,
    J=122mu_2+(224mu_4-5760Psi)/mu_2.

Full eigenspace projections are used at collisions. Let j(u),u_*,J_*
be the credited scalar data

    j(u)=(2058+21912u-15876u^2+19224u^3+3402u^4)
         /((3+u)(1+3u)^2),
    u_* = the unique root in (2/25,9/100) of
          26634-231084u-907290u^2+376920u^3
          +971190u^4+224532u^5+30618u^6,
    J_*=j(u_*),
    theta_*=(1,1,1,-1,-1,-1,sqrt(u_*),-sqrt(u_*)).

**Theorem.** On this entire closed saturated-triple class,

    J<=J_*,
    J=J_* iff theta is a permutation of theta_*,
    dist(theta/sqrt(mu_2),O_*)^2 <= 5000(J_*-J),              (1)

where O_* is the unit permutation orbit of theta_*. Reflection preserves
that orbit. The constant 5000 is conservative.

The other five coordinates are unrestricted apart from balance and the
unit bounds; they can create six actual levels. The result closes the
whole saturated-triple slice of the labeled 3+1+1+1+1+1 cohort, including
all coincidences and further unit saturation. It does not cover every
profile in that cohort: a singleton can attain max norm while the triple
lies inside. The 2+2+1+1+1+1 cohort, whole six-to-eight-level classification,
unrestricted first-power endpoint and new original-root radius remain
outside the claim. The earlier whole-five-level theorem is preserved.

## 2. Complete ordered section

Permute and reflect so the first three entries are -1. Reflection sends
C to -C and w to -w, preserving Psi and J. Sort the other
five as t_j=1-beta_j, with 0<=beta_0<=...<=beta_4 and sum beta_j=2.
The upper bound beta_4<=2 follows from nonnegativity and the sum, so
this describes the entire physical section. Its four-simplex vertices
V_k have their last k entries equal 2/k and preceding entries zero,
k=1,...,5. Write beta=sum a_(k-1)V_k with a_i>=0 and sum a_i=1.
The inverse is

    a_4=5beta_0/2, a_3=2(beta_1-beta_0),
    a_2=3(beta_2-beta_1)/2, a_1=beta_3-beta_2,
    a_0=(beta_4-beta_3)/2.

These are nonnegative, and direct telescoping gives sum a_i=1 and
recovers every beta_j. Thus no ordering or collision face is omitted.
Also mu_2>=3+3^2/5=24/5 by Cauchy--Schwarz, so normalization is uniformly
nonsingular throughout this section.

Set q=a_2+a_3+a_4. For q<1 define t=a_0/(1-q). For q>0 let
z_i=a_(i+2)/q, i=0,1,2, so z_i>=0 and sum z_i=1. Then

    (a_0,a_1)=(1-q)(t,1-t),
    (a_2,a_3,a_4)=q(z_0,z_1,z_2).                         (2)

The new method groups by this transverse degree instead of subdividing
the full four-simplex. We first prove the estimate in its interior;
Section 5 extends it to q=0, q=1 and every other boundary.

## 3. Full filtered compression and integer polynomial

The credited full-compression lemma takes B_i=C^i(I-C^2), i=0,1,2,
s_r=tr(C^r),s_0=7, b_i=w^T C^i w, and

    G_ij=s_(i+j)-2s_(i+j+2)+s_(i+j+4), r_i=b_i-b_(i+2),
    D=det G, N=r^T adj(G)r.

Whenever D>0, Frobenius projection onto span{B_i} gives Psi>=N/D and
hence J<=122mu_2+(224mu_4-5760N/D)/mu_2. This uses full eigenspaces;
within-block zero-weight modes are not silently assigned positive weights.

For interior a_i>0 the five other slopes are distinct and in (-1,1).
Let h(y)=(y+1)^3 product_j(y-t_j). The classical compression identity
det(yI-C)=h'(y)/8 follows by a balanced Schur complement. Rolle's theorem
gives five distinct derivative roots between the six distinct slope
values; the remaining two compression eigenvalues are -1. At each of
those five interior roots the filter 1-y^2 is nonzero. A nonzero quadratic
cannot vanish at five distinct sites, so the three B_i are independent.
Thus their Gram determinant is positive throughout the simplex interior.
No singular Gram quotient is used on its boundary.

Here is a complete integer specification of the cleared strict target.
Use homogeneous coordinates H=sum a_i. Let the scaled deficits be

    beta30_j=sum_(k: j>=5-k) (60/k)a_(k-1), j=0,...,4,
    T=(-30H,-30H,-30H,30H-beta30_0,...,30H-beta30_4).

All 60/k are integers for k=1,...,5. Write m_r=sum T_j^r and M=8C_T.
Generate s_r^M=tr(M^r),r=1,...,8 by all cyclic words in P=I-ee^T;
s_0^M=7. A word with k rank-one factors at positive cyclic gaps g_i
contributes (-1)^k 8^(r-k) product_i m_(g_i), while the empty word
contributes 8^r m_r. This is tr((8 diag(T)P)^r) by cyclic trace and
P^2=P, hence the required full-compression trace.

The five coupling numerators v_i=T^T M^i T are

    m_2,
    8m_3,
    64m_4-8m_2^2,
    512m_5-128m_2m_3,
    4096m_6-512(2m_2m_4+m_3^2)+64m_2^3.

These follow from the credited Schur moment series and can also be
checked by direct matrix multiplication. Define

    A_ij=(240H)^4 s_(i+j)^M-2(240H)^2 s_(i+j+2)^M+s_(i+j+4)^M,
    R_i=(240H)^2 v_i-v_(i+2),
    D_int=det A, N_int=R^T adj(A)R,
    F=[785753(30H)^2 m_2-122000m_2^2-224000m_4]D_int+90000N_int.

The determinant has degree 18 and F,N_int have degree 22. At H=1,
D_int=240^18 D and N_int=64*30^4*240^18 N. Therefore, with c=785753/1000,

    F=1000*30^4*240^18[(c mu_2-122mu_2^2-224mu_4)D+5760N]. (3)

Positive scaling and D>0 show that F>=0 implies J<=c. The executable
regenerates these polynomials from the full root forms; no private
coefficient file or numeric fit is required.

## 4. Grouped global strict/local cover

Expand the integer homogeneous target uniquely as

    F(a)=sum_gamma a_2^gamma0 a_3^gamma1 a_4^gamma2
                    sum_(i=0)^n c_(i,n-i,gamma)a_0^i a_1^(n-i),
    k=|gamma|, n=22-k,
    P_gamma(t)=sum_(i=0)^n c_(i,n-i,gamma)t^i(1-t)^(n-i).

The checker reconstructs the entire monomial dictionary from this
grouping. With (2), the identity becomes

    F=sum_gamma q^k(1-q)^(22-k) z^gamma P_gamma(t).          (4)

The following exact coefficient facts are the new structural certificate.

* Every one of the 14,535 original power coefficients with k>=4 is
  nonnegative (14,530 are strictly positive). Thus all those grouped
  contributions are nonnegative for every physical q,t,z.
* All 19 polynomials with k=1,2,3 are nonnegative on [0,1]. Each is
  certified on the three closed intervals [0,1/4], [1/4,1/3], [1/3,1]
  by its complete univariate Bernstein coefficients.
* P_0, corresponding to gamma=(0,0,0), is nonnegative on [0,13/50]
  and [1/3,1]. The lower interval is split at 1/4.
* For each unit gamma e_i, 119P_0+P_(e_i) is strictly positive on
  [13/50,1/3]. The degree-21 P_(e_i) is elevated to degree 22 exactly
  before addition. All three elevation identities are checked in full.

There are 1,176 low-transverse sign entries, 69 outer-face entries and
69 strict domination entries, in addition to the 14,535 high-degree
entries: **15,849 exact signs**. Every scalar table has a complete
inverse Bernstein conversion recovering its affine power polynomial.
The 60 scalar tables and three domination tables are regenerated from F.
Their minima, zero indices and coefficient hashes are in expected.json.
Nonnegative Bernstein basis functions sum to one on the closed interval;
therefore these are continuous-domain signs, including interval endpoints.

Let P_i=P_(e_i) and L=sum z_i P_i. The nonnegative higher contributions
in (4) show

    F >= (1-q)^21[(1-q)P_0+qL].                            (5)

If t lies outside [13/50,1/3], all terms on the right are nonnegative,
so F>=0. If t lies inside and q>=1/120, then L>=0 and
119P_0+L=sum z_i(119P_0+P_i)>0. The exact identity

    (1-q)P_0+qL
      = [(1-q)(119P_0+L)+(120q-1)L]/119

again proves F>=0. Thus these closed strict branches imply J<=c by (3)
where D>0. No floating cover proposal or recursive simplex traversal
is part of this certificate.

It remains to handle t in [13/50,1/3] and q<=1/120. Set

    alpha_i=beta_(i-1), i=1,2,3,
    S=sum alpha_i=(2/3)a_2+a_3+(6/5)a_4,
    x=(beta_4-beta_3)/2=a_0.

The other two coordinates are exactly S/2+x and S/2-x, and the negative
unit triple remains fixed. The whole closed region satisfies

    S <= (6/5)q <= 1/100,
    x=(1-q)t >= (119/120)(13/50)=1547/6000 > 1/4,
    x <= 1/3.

It therefore lies in the credited local tube 8194. That theorem gives

    J_*-J>=200S+450(x^2-u_*)^2,
    dist(theta/sqrt(mu_2),O_*)^2<=(J_*-J)/40.                (6)

This import is a rigorously mapped closed domain, not a numerical leaf
label. Its scalar curvature and optimizer retain their earlier credit.

For the strict branches the credited scalar maximum and exact evaluation
give the rational margin

    J_*-c >= j(87/1000)-c
           =1331662697/1636234509000 > 1/1250.              (7)

Any two unit vectors have squared distance at most four. Hence J<=c
implies dist^2<=4<5000(J_*-J); the local branch (6) implies the same
weaker global bound. Every simplex-interior profile therefore satisfies
both inequalities in (1). This complete strict/local cover is the
substantive step beyond the credited local theorem.

## 5. Collisions, rank loss and equality

Approximate an arbitrary closed-simplex profile by interior profiles.
Balance, max norm one and the fixed triple are preserved by the section.
The real symmetric compression and w vary continuously. Around each
distinct limiting eigenvalue choose a disjoint spectral interval whose
endpoints avoid the spectrum. The projection onto each entire cluster
varies continuously. Inside a cluster, its nonnegative weights satisfy
sum r_j^2 <= (sum r_j)^2. Taking limits over all clusters proves

    limsup Psi(theta_n) <= Psi(theta).

Since the moments are continuous and mu_2>=24/5, this yields
J(theta)<=liminf J(theta_n). Thus J<=J_* extends to every boundary.
The unit-orbit distance is continuous, and

    dist(theta/sqrt(mu_2),O_*)^2
      <=5000 limsup_n(J_*-J(theta_n))
      <=5000(J_*-J(theta)).

This also extends (1) without any singular quotient or assumption that
individual eigenspace weights stay continuous across splitting.

If J=J_*, the distance is zero, so theta is a positive scalar multiple
of a permutation of theta_*. Max normalization forces that scalar to
be one. Conversely the credited face identity supplies J(theta_*)=J_*;
theta_* belongs to this saturated-triple class. This proves the complete
equality assertion and attainment. Reflection is already a permutation
of the theta_* multiset.

## 6. Computational trust boundary

The public verifier builds full integer root forms, all traces/coupling
moments, determinant/adjugate targets, grouped coefficients and scalar
tables from scratch. Ten rational profiles include all three branches,
the q=1 face, collisions and rank-one/rank-two Gram endpoints. Each
constructs the literal full 8x8 compression. A separate linear projection
onto its full symmetric commutant, using all 28 equations in 36 variables
and the correct Frobenius weights, recovers defining Psi. Full moments,
eight traces, five coupling moments, all nine Gram entries and their
integer scaling agree. On nonsingular controls an independent Gaussian
solve checks the adjugate numerator; on singular controls the determinant,
numerator and cleared target are checked without division. Actual local
loss or strict bound is checked directly on these examples.

These finite author controls support the written universal identities;
they do not replace the Rolle/projection/closed-section/collision proof
or constitute independent review. The scalar and local theorems are
explicit external mathematical inputs. Ordinary bridges and exact Python
implementation remain outside a formal proof kernel. A compact manifest
is mandatory and compared in full, including under optimization. No
private module, large coefficient corpus, floating sign or external
solver is needed. The earlier incomplete 90-second cover attempts remain
heuristic history; the new grouped argument supplies complete coverage.
