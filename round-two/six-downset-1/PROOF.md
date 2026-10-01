# Capped unions with equal largest stars

Actual author: **six-downset-1**, role **researcher**, round two,
2026-10-01. Complete author-checked ordinary proofs, unformalized and
not independently reviewed. Exact finite replay validates the formulas;
it does not establish the unbounded quantifiers.

## 1. Statement, conventions, and credited ingredients

For a nontrivial finite downset D, retain the empty vertex, put N=|D|,
and let s be its largest-star size. A capped H certificate is a real
symmetric matrix M with

    M1=1, M[A,B]=0 if A intersects B,
    L=(N-s)M+sI >= 0, I-M >= 0.

The empty diagonal is unrestricted. Deleting a maximum-star coordinate
injects its star into the outside family, so 1<=s<=N/2. The target H and
its distinction from inertia conjecture I are from
[Ellis--Filmus--Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4).
The live arXiv record checked on October 1 still lists v1, with H and I
unresolved. This work concerns H with an additional spectral cap.

**Union lemma.** Let r>=2, and let D_1,...,D_r be nontrivial downsets on
pairwise disjoint coordinate supports. Suppose each has a capped H
certificate, and all their largest-star sizes are the same integer s.
Write N_j=|D_j|, m_j=N_j-1, m=sum_j m_j, and N=m+1. Their set-theoretic
union, with just one empty vertex, has an explicit capped H certificate.
If nu_j is the lower-slack nullity of the chosen factor certificate, the
new lower-slack nullity is exactly sum_j nu_j. Its upper slack has rank
N-1: its unit eigenvalue is simple even if the factors' unit eigenvalues
are repeated. Rational inputs give rational outputs.

There is a certificate-independent quantitative upper gap. Put

    delta=m-max_j m_j > 0, h=max_j N_j,
    d0=(1/m) sum_j s/(N_j-s),
    gamma=delta*d0/(delta+h) > 0.

Every eigenvalue of the constructed M other than its unit eigenvalue is
at most 1-gamma/(N-s).

The empty-vertex core criterion, ordinary disjoint-support union, and
conditional tensor closure are credited to
[the prior structural source, Sections 2,3,5](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
graph7578. That source expressly does not establish cap preservation for
unions. The increment here is cap preservation under equal largest-star
sizes, automatic strictness of the upper endpoint, a uniform quantitative
gap, and the exact spectra and maximal-rank consequences below. No
historical priority claim for general graph/theta operations is made.

## 2. Core normalization and the explicit union

This section restates the credited core criterion to make the proof
self-contained. For a family with m=N-1 nonempty vertices, let E be the
N-by-m matrix with first row -1^T and remaining rows I_m. A certificate
at parameter s is equivalent to a symmetric core C satisfying

    C >= 0, C[A,A]=s-1,
    C[A,B]=-1 for distinct intersecting A,B.

The lift is

    Q=ECE^T, L=J_N+Q, M=(L-sI)/(N-s).                 (1)

Indeed Q1=0, L1=N1, and the entries have exactly the required support.
Conversely an H slack L has constant eigenvalue N, so Q=L-J_N is PSD,
has zero row sums, and is determined by its nonempty principal core C.
The additional cap is equivalent to

    U=N I_m-J_m-C >= 0,
    (N-s)(I-M)=EUE^T.                                (2)

For each component extract C_j from its given certificate, and set

    C=direct_sum_j C_j.                               (3)

All intersections occur within a component, and all core diagonals have
the common value s-1. Thus (1) proves ordinary H without further work.

There is also a direct entry formula, useful for separate implementation
validation. Preserve each component's vertex order. For a nonempty A in
D_j and any B in the same component, including B=empty, set

    M[A,B]=(N_j-s)/(N-s) * M_j[A,B].

Use symmetry for the empty row. For nonempty vertices in different
components set M[A,B]=1/(N-s), and set

    M[empty,empty]=
      [sum_j (N_j-s)M_j[empty,empty]+(r-1)(s-1)]/(N-s).

These are exactly (1)-(3), not an additional hypothesis. Factor matrices
may have signed entries.

## 3. Cap, strictness, and nullities

Let U_j=N_j I_(m_j)-J_(m_j)-C_j >=0. The new upper core in (2) is

    U=direct_sum_j U_j + K,                           (4)

where K has diagonal blocks (m-m_j)I_(m_j), and off-diagonal blocks
-J_(m_j,m_k). This is the Laplacian of the complete multipartite graph
whose parts have sizes m_j. Its quadratic form is

    z^T K z=sum_(j<k) sum_(a in j,b in k) (z_a-z_b)^2.

Because r>=2 and every m_j>=1, it is PSD with kernel exactly span{1_m}.
This proves the cap.

For each j let x_j be any maximum-star indicator on its nonempty
vertices. The prescribed core entries give

    x_j^T C_j x_j=s(s-1)-s(s-1)=0,

so C_j x_j=0. In particular U_j1 cannot vanish: otherwise C_j1=1,
but then x_j^T C_j1=s contradicts C_j x_j=0. The kernel of a sum of PSD
matrices is the intersection of their kernels, so (4) is positive
definite. Since E has rank m and image 1_N-perpendicular, the full upper
slack has rank m=N-1. This is independent of any seed upper strictness.

The ranges of Q and J_N in (1) are orthogonal. Hence rank L=1+rank C.
The same identity holds in each factor, and C is a direct sum. Therefore

    nullity L=sum_j nullity L_j,
    rank L=1+sum_j (rank L_j-1).                       (5)

This is the nullity of the particular output certificate. It is not an
assertion that arbitrary chosen factors have universally maximal rank.

## 4. A uniform upper spectral gap

Write D0=direct_sum_j U_j and u=1_m/sqrt(m). The multipartite decomposition
into within-part zero-sum vectors and vectors constant on parts gives

    K >= delta*(I-uu^T), delta=m-max_j m_j.

Also 0<=D0<=h I because C_j and J_(m_j) are PSD. Let d=u^T D0 u.
Using the maximum-star vector above,

    x_j^T U_j1=s,
    x_j^T U_j x_j=s(N_j-s).

Cauchy--Schwarz for the PSD form U_j gives

    1^T U_j1 >= s/(N_j-s), so d>=d0>0.               (6)

PSD Cauchy--Schwarz also gives D0>=ww^T, with
w=D0u/sqrt(d), u^T w=sqrt(d), and ||w||^2<=h. On the span of u and the
component of w perpendicular to u, the matrix

    delta*(I-uu^T)+ww^T

has a two-by-two block of determinant delta*d and trace
delta+||w||^2<=delta+h. Its smaller eigenvalue is at least its
determinant divided by its trace. On the remaining directions the
eigenvalue is delta. If w is parallel to u, the two eigenvalues are
instead d and delta and the same lower bound still holds. Thus

    U=K+D0 >= gamma I_m, gamma=delta*d0/(delta+h).

Finally E^T E=I_m+J_m, so every nonzero singular value of E is at least
one. Its image is 1_N-perpendicular. Equation (2) therefore gives

    (N-s)(I-M) >= gamma I on 1_N-perpendicular.

No nonsingularity assumption on a factor core, numerical optimization,
or square-root coefficient in the output certificate is required.

## 5. Cubes: closed spectra and universally maximal lower rank

Let D(n,r) be the union of r Boolean cubes on pairwise disjoint n-point
supports, n>=2 and r>=2. Put s=2^(n-1). Then

    N=r(2s-1)+1, b=N-s=(2r-1)s-r+1.

The factor certificate is the usual complement permutation. Its core
has one class for the full set and one class for each proper nonempty
complementary pair. If P records membership in the same class, including
the diagonal, then C_j=sP-J_(2s-1).

The output matrix has the following complete spectrum:

| Eigenvalue | Multiplicity |
| --- | ---: |
| 1 | 1 |
| -s/b | rs |
| s/b | r(s-2) |
| 1/b | r-1 |
| [r(s-1)+1]/b | 1 |

The multiplicity r(s-2) is zero when n=2. In particular the upper gap is
exactly (r-1)s/b and the lower-slack rank is r(s-1)+1=N-rs.
All displayed entries of this cube-union matrix are nonnegative.

To derive the spectrum, represent each component core by the s vertices
u_l of a regular simplex: ||u_l||^2=s-1, u_l^T u_k=-1 for l!=k,
sum_l u_l=0, and sum_l u_l u_l^T=sI on its (s-1)-dimensional span.
Use orthogonal spans for different components. Every simplex vertex
appears twice except u_full, which appears once. Thus the nonempty frame
operator of one component is 2sI-u_full u_full^T, and its sum vector is
-u_full. The empty lift adds the outer product of sum_j u_full,j.
On the r(s-2) directions perpendicular to their respective full vectors,
Q has eigenvalue 2s. On the r full-vector directions it has matrix

    (s+1)I_r+(s-1)J_r.

This has eigenvalues s+1, multiplicity r-1, and
(r+1)s-r+1, multiplicity one. Since rank Q=r(s-1), adding J_N and applying
(1) gives precisely the table.

The rank N-rs is maximal among **all real H matrices** on D(n,r),
irrespective of caps or symmetry. Here is the required forced-span
argument. In a single full cube every maximum intersecting family is an
upward complementary selector: it contains the full set and one member
of every other complementary pair. For any nonempty proper A, there
exist two such families differing just at A,A^c. This is classical
complementary switching; the concrete finite construction in
[the prior proper-cube proof, Section 2](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_boolean_rigidity/PROOF.md)
is credited. For completeness, start with A and all B^c for nonempty
proper subsets B of A, then greedily extend to a maximal intersecting
family. Maximality forces a complementary selector: if T,T^c were both
missing, witnesses incompatible with each would be disjoint. A is
minimal in the resulting family, so replacing A with A^c preserves
intersection. The full set can be included throughout.

The s-1 complementary difference vectors, together with any one selector
indicator, are linearly independent and span an s-dimensional space.
Every such family, supported in its own branch, is a maximum family of
D(n,r). For any real H certificate its core must annihilate its indicator,
by the zero-form identity from Section 3. These r spaces have disjoint
nonempty supports and dimension rs. Thus every H core has nullity at
least rs. Equation (5) attains the resulting bound.

The baseline maximum-family classification and switching are not new.
Primary historical context is
[Loeb--Meyerowitz, The Graph of Maximal Intersecting Families of Sets,
Sections 1-2](https://oeis.org/A007007/a007007.pdf).
The full-cube forced span and its tensor consequences are also credited
prior inputs: see
[the independent Boolean audit, full-cube extension](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_boolean_review3/REVIEW.md),
graph8066. Here those directions are combined across the new union factors.

## 6. Products and overlapping equal Boolean facets

The standard credited tensor mechanism applies because every union above
is capped. More precisely take k>=1 factors D(n_j,r_j), n_j>=2,r_j>=2,
on mutually disjoint supports. Put N_j=r_j(2s_j-1)+1, s_j=2^(n_j-1),
N*=product_j N_j, and

    p=max_j s_j/N_j, S=pN*, T={j:s_j/N_j=p}.

The tensor product is a rational capped H certificate and has lower rank

    N* - sum_(j in T) r_j s_j.                        (7)

Its unit eigenvalue is simple. This lower rank is maximal among all real
H certificates. Its maximum intersecting families are exactly cylinders
of a maximum intersecting family in one factor indexed by T.

To check all quantifiers, put rho_j=s_j/(N_j-s_j)<1. Factor eigenvalues
lie in [-rho_j,1], and their only eigenvalue of absolute value one is a
simple +1. A negative product can equal -max_j rho_j only when exactly
one factor, indexed by T, is at its negative endpoint and all other
factors equal +1. Every other negative product is strictly larger.
This proves the kernel dimension in (7). Maximum-family cylinder
indicators force the same mutually orthogonal centered spaces in every
H certificate, proving universal maximality.

For equality classification the centered maximum-family indicator lies
in that tensor kernel. Hence its indicator is a constant plus a sum of
functions of single eligible factors. A {0,1}-valued additive function
on a Cartesian product can vary in at most one factor: fixing all other
variables shows that any varying summand has range exactly one, while
the range of the sum equals the sum of the individual ranges. Two varying
summands would give total range at least two. It must therefore be a
cylinder. Setting every other
factor to empty shows that its base family is intersecting; its size
is s_j, so it is a maximum family. These tensor/equality arguments are
credited prior mechanisms; the union factors and their forced dimensions
are the new inputs.

There is also a concrete overlapping-facet consequence. Let C be a c-point
core, c>=1, and A_1,...,A_r disjoint n-point petals disjoint from C,
n>=2,r>=2. The downset

    D=union_j 2^(C union A_j) = 2^C times D(n,r)

has N*=2^c N, largest star S=N*/2, and a rational capped H certificate
of universally maximal lower rank N*-2^(c-1). Its maximum intersecting
families are exactly the cylinders of maximum families in the core cube.
Indeed the only tensor eigenvalues -1 use a core-cube eigenvalue -1
and the union's simple +1; the lower kernel has dimension 2^(c-1).
The full-cube forced span from Section 5 proves maximality. For c=1
this gives rank N*-1 and the unique maximum family is the common-point
star. The unit eigenvalue has multiplicity 2^(c-1); upper simplicity is
not asserted when c>1.

## 7. Why the equal-star assumption matters to this construction

Ordinary union transport allows t=max_j s_j and cores
C_j+(t-s_j)I. Those shifted cores need not preserve the cap. Let D be
the full three-point cube plus one isolated singleton. Then N=9,t=4.
Use the cube's complement core C_cube=4P-J_7, and the singleton core
shifted from zero to [3]. Their direct sum yields ordinary H.

For its upper core B=9I_8-J_8-C, put w=5 on all six nonempty proper
cube sets, w=1 on the full cube, and w=6 on the isolated singleton.
Direct exact arithmetic gives

    w^T B w=-37.

Equivalently, with zero empty coordinate, w gives
5*w^T(I-M)w=-37. This refutes cap preservation for the general shifted
direct-sum recipe. It does not exclude capped H on that downset: pairing
the full cube with the isolated singleton makes all four disjoint color
classes have size two. Their ordinary partition core is capped.

[UNEQUAL_FACETS.md](UNEQUAL_FACETS.md) gives a stronger repair for this
example and every unequal pair of Boolean cubes: an explicit aligned
core with strict cap margin, followed by a rational mixture attaining
universally maximal lower rank. Together these formulas cover all
downsets with exactly two maximal members, including arbitrary overlap.
This does not extend the equal-star rule to arbitrary unequal downsets.

## 8. Evidence and trust boundary

The self-contained standard-library checker reconstructs full matrices
using both the factor-entry formula and a separate core lift. It checks
actual downset membership, largest stars, support, symmetry, row sums,
both full rational PSD slacks and their ranks. Cube spectra are checked
by exact nullities at every listed eigenvalue, and the quantitative gap
by an exact PSD check on the constant-vector complement. Mixed factors,
products, common-core facets, the unequal-star negative witness, and
malformed controls are included with their finite coverage in RESULTS.json.
Every nonempty proper target set receives a concrete complementary switch
at cube orders two through five. Separate complete size-s family censuses
at orders two through four verify the actual forced spans.

The all-orders proof is ordinary written linear algebra and the supplied
finite complementary-switching argument. It is not formalized. There is
no numerical SDP, imported census, solver, large certificate corpus,
incomplete-search inference or external runtime input. Source publication
and finite replay are evidence of reproducibility, not independent review.
