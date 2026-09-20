# Full Ehrhart period for simple bimodular polytopes

All lattices in the ambient space are Z^d. A polytope is bounded and full
dimensional, with d>=1. An **integral facet description** means

    P={x in R^d:A x<=b},      A,b integral,

with exactly one inequality for each actual facet. The rows need not be
primitive: 2x<=1 is allowed. Rescaling a row can change the arithmetic
conditions below, so the description is fixed. Unimodular changes of
ambient coordinates and integer translations preserve the conditions.

For a full-column-rank integral matrix A with d columns, define

    Delta(A)=max{|det A_J|: J is a set of d rows}.

We call A **bimodular** when Delta(A)<=2. This bounds only full-column-rank
square minors, not every smaller minor. It is the convention used by
Naegele--Santiago--Zenklusen in the primary source cited in SOURCES.md.

**Theorem 1 (simple bimodular polytopes).** If P has a bimodular integral
inequality description and is simple, its minimal Ehrhart quasiperiod
equals its vertex denominator: one if it is a lattice polytope, and two
otherwise. Redundant input inequalities may first be removed.

We prove a more general local theorem, including the exact leading parity
coefficient. This is a sufficient condition, not a classification of every
polytope with full period.

## 1. The active-image criterion

Suppose 2P is a lattice polytope. Let N be the nonempty faces F for which
aff(F) intersects Z^d in the empty set. If N is nonempty, put

    g=min_{F in N} codim F,       k=d-g,
    M={F in N:codim F=g}.

For F contained in exactly g facets, let A_F be their g-by-d normal matrix,
and b_F their right sides. Its rows are independent. Define

    Lambda_F=A_F Z^d subset Z^g,
    delta_F=[Z^g:Lambda_F].

**Theorem 2 (local image-index criterion).** If every F in M lies in exactly
g facets and satisfies delta_F=2, then the unique polynomials A_P,B_P in
Q[n] such that

    L_P(n)=|nP intersect Z^d|=A_P(n)+(-1)^n B_P(n)

satisfy

    deg B_P=k,
    [n^k]B_P=2^(-g-1) sum_{F in M} vol_k(F)>0.             (1)

Here vol_k uses the direction lattice lin(F-F) intersect Z^d, with lattice
cube and point volume one. The directions need not be coordinate subspaces.
Consequently the exact quasiperiod is two and the reduced denominator of
E_P(t)=sum_{n>=0}L_P(n)t^n is

    (1-t)^(d+1)(1+t)^(d-g+1).                              (2)

If H_P=(1-t^2)^(d+1)E_P, its zero at -1 has exactly order g, with

    [H_P/(1+t)^g]_{t=-1}
      =2^(d-g)(d-g)! sum_{F in M} vol_(d-g)(F)>0.           (3)

If N is empty, all vertices are integral and L_P is a polynomial. Theorem 2
imposes no condition on those integral polytopes.

## 2. Face subsets and a full-support parity relation

**Lemma 3 (facet subsets).** If a codimension-q face F lies in exactly q
facets, every subset I of those facets intersects P in a face of codimension
|I|, whose affine span is defined by exactly those equations.

**Proof.** The active normals have rank q since their equations define
aff(F). Take x in relint F. Linear independence gives a vector w with
scalar product zero on the selected normals and -1 on the other active
normals. For sufficiently small positive epsilon, x+epsilon w satisfies
exactly the selected equalities: all originally inactive inequalities
remain slack. Rank gives the asserted affine span and codimension. The
empty subset gives P itself. QED.

**Lemma 4 (minimality forces full support).** Under the hypotheses of
Theorem 2, for every F in M,

    Lambda_F={u in Z^g:sum_i u_i is even},
    sum_i (b_F)_i is odd.                                 (4)

**Proof.** An index-two subgroup of Z^g is the kernel of a unique nonzero
homomorphism epsilon:Z^g -> Z/2, represented by a nonzero binary row vector.
Since aff(F) has no integer point, b_F is not in Lambda_F, so epsilon b_F=1.
If the support I of epsilon were a proper subset of the g rows, the system
(A_F)_I x=(b_F)_I would also have no integral solution. By Lemma 3 it defines
the affine span of a nonempty face of codimension |I|<g, contrary to the
definition of g. Thus every coordinate of epsilon is one, proving (4).
This is a binary lattice relation, not a claim of linear dependence of the
facet normals over R. QED.

In particular, projection of Lambda_F to any proper subset of coordinates
is all of that coordinate integer lattice. Hence every proper subsystem
(A_F)_I z=(b_F)_I has an integral solution. These are affine solutions;
they need not satisfy the other inequalities of P.

## 3. The quotient lattice and its local parity jump

Fix F in M. Let W=ker A_F=lin(F-F), V=R^d/W and pi:R^d -> V. Since W is
rational, L=pi(Z^d) is a lattice in V. The induced real-linear isomorphism

    C:V -> R^g,       C(pi(x))=A_F x

sends L bijectively onto Lambda_F. Thus the transverse lattice really is
the active-image lattice; it is not automatically the coordinate Z^g.
Choose any lattice basis of L if standard coordinates on V are desired.
In those coordinates C is a square integral matrix of determinant +-2.

The transverse supporting cone of nP at nF is

    K_n={y in V: Cy<=n b_F}=n v+K_0,     v=C^-1 b_F.

It is simplicial. By (4), 2v belongs to L, while v does not. Fix any one
rational positive-definite scalar product, using its induced products and
quotient lattices throughout the Berline--Vergne construction.

**Lemma 5 (index-two local jump).** With the notation above,

    mu(K_even)(0)-mu(K_odd)(0)=2^-g.                       (5)

**Proof.** Integer slacks u=n b_F-Cy give a bijection between y in K_n
intersect L and

    u in Z_{>=0}^g,       sum_i u_i=n mod 2.

Write ell_j(xi)=<xi,C^-1 e_j>. Removing the vertex exponential from the
exponential lattice sum gives

    exp(-n<v,xi>) S(K_n)(xi)
     =1/2 [product_j(1-exp(-ell_j))^-1
            +(-1)^n product_j(1+exp(-ell_j))^-1].           (6)

This holds in a convergence chamber and hence meromorphically. A
positive-dimensional face D_n(I) of this cone is defined by equality on
a proper subset I of rows. By (4), there is z_I in L with
(Cz_I)_I=(b_F)_I. Consequently

    v-z_I in ker C_I=lin D_0(I).

The shift v is therefore an actual lattice translation in the quotient
by lin D_0(I). Integer-translation invariance makes the transverse mu
functions for D_n(I) independent of n. The face integrals satisfy

    exp(-n<v,xi>) I(D_n(I))(xi)=I(D_0(I))(xi).

Apply the local cone identity S(K)=sum_D mu(t(K,D)) I(D) at n=0 and n=1,
after removing the corresponding vertex exponentials. All positive-face
terms cancel, including the full cone. The only term left is the vertex,
so (6) gives

    mu(K_0)(xi)-mu(K_1)(xi)
       =product_j(1+exp(-ell_j(xi)))^-1.

This difference is analytic at zero with value 2^-g. Since 2v is in L,
the statement extends to all even/odd n by lattice translation. This
argument includes g=1 and requires neither graph coordinates nor signs
of individual mu values. QED.

## 4. Assembly and proof of Theorem 2

We explicitly import Berline--Vergne's local Euler--Maclaurin formula:

    L_P(n)=sum_{F nonempty face}
             mu(t(nP,nF))(0) vol(F) n^dim F.

The coefficient attached to F is periodic with period dividing the least
q for which q aff(F) meets the lattice. This is their Corollary 30 in the
41-page version cited in SOURCES.md. The cone identity and translation
invariance used above are their Theorems 19(d) and 20(a).

Because 2P is a lattice polytope, every coefficient has period dividing
two. All faces of dimension greater than k have integral affine spans,
so those degrees are constant across residues. In degree k, precisely
the faces in M can vary. Lemma 5 makes their even-minus-odd jump equal
to 2^-g times the sum of their normalized volumes. B_P is half the
difference of the residue polynomials, proving (1). Positivity proves
exact degree and minimal quasiperiod two. Equality of residue polynomials
also establishes the assertion at n=0.

A degree-k polynomial with leading coefficient beta contributes a pole
of order k+1 to its generating function, with leading limit beta k!.
The alternating part therefore has an exact order k+1 pole at -1.
Positive d-volume gives order d+1 at +1, and half-integrality permits
no other poles. This proves (2), and direct multiplication gives (3).

## 5. Bimodularity supplies the arithmetic hypothesis

**Lemma 6 (projected image index).** Let A be an integral matrix of rank d
with Delta(A)<=2. For any q independent rows D of A,

    [Z^q:D Z^d] belongs to {1,2}.

**Proof.** Extend those rows to a nonsingular d-by-d row submatrix B of A,
putting D first. Projection to the first q coordinates induces a
surjection

    Z^d/B Z^d -> Z^q/D Z^d.

The first finite group has order |det B|, either one or two. The order of
the second divides it. No bound on a smaller minor is used. QED.

At every vertex of P, choose d independent active rows. Their determinant
has absolute value one or two, so Cramer's rule gives 2v integral. Thus
2P is a lattice polytope. After removing redundant inequalities, Delta
cannot increase. At a codimension-g face in exactly g facets, Lemma 6
gives index one or two. A nonintegral affine RHS excludes index one.
Therefore every bimodular P satisfying the local facet condition meets
Theorem 2. For a simple polytope the facet condition is automatic, proving
Theorem 1. This does not require a nondegenerate inequality description
before redundant rows are removed.

## 6. A finite arithmetic certificate and precise inclusion

For an integral full-row-rank q-by-d matrix D, its image index is the gcd
of the absolute values of its q-by-q minors. Moreover,

    Dz=b has an integral solution
    iff gcd(maximal minors of [D|b])=gcd(maximal minors of D).   (7)

These are classical Smith-normal-form facts: integer row and column
operations preserve the gcd, and a diagonal Smith form makes the index
the product of its invariant factors. Appending b replaces the image
lattice Lambda by Lambda+Zb. The indices agree exactly when b was already
in Lambda. If the active rows are dependent, first choose an independent
subset defining the same consistent affine system. Formula (7), the actual
facet incidence, and half-integrality give a finite certificate for the
local hypothesis. No polynomial-time face-enumeration bound is claimed.

The preceding type-B theorem is included in Theorem 2: its signed-system
proof establishes half-integrality and reduces every relevant active
system to one unbalanced g-cycle with determinant +-2 in its coordinate
quotient. Thus its active image has index two. This inclusion does not
claim that all type-B matrices are globally bimodular: two disjoint
unbalanced blocks can produce determinant four. The local criterion
contains both that earlier theorem and the bimodular corollary.

## 7. Independent boundaries of the two hypotheses

The classical Stanley pyramid

    Q={x>=0, x<=y<=1-x, x<=z<=1-x}

has an integral bimodular description: all its 3-by-3 minors have absolute
value at most two. It has four integral base vertices and the apex
(1/2,1/2,1/2), which lies in four facets. Its only nonintegral-affine face
is that apex, so the local facet condition fails, and

    L_Q(n)=sum_{a=0}^{floor(n/2)}(n-2a+1)^2=binom(n+3,3).

Thus even bimodularity cannot replace simplicity in a universal assertion.
This is the same known example credited by McAllister--Woods, not a new
counterexample.

Conversely, their triangle T=conv((0,0),(1,1/2),(2,0)) is simple and half
integral, and has integral facet inequalities

    -y<=0,       -x+2y<=0,       x+2y<=2.

Only the fractional apex has a nonintegral affine span. Its active normal
matrix has determinant absolute value four; its image index is four, not
two. Nevertheless L_T(n)=binom(n+2,2). This excludes replacing the image
condition by half-integrality alone. Again the construction and formula
are known prior work. Both controls have integral primitive offsets, so
the failures do not rely on the new allowance of nonprimitive rows.

As a positive nonprimitive example, [0,1/2] has L(n)=floor(n/2)+1, g=1,
and B=1/4. This case is consistent with the known maximal-period theorem
for the second-leading Ehrhart coefficient; the substantive new scope is
the higher-codimension criterion and its bimodular consequence.

## Evidence and novelty boundary

The new work is the full-support image-lattice argument and its application
to simple bimodular systems, with the precise face-volume coefficient.
The local analytic character calculation generalizes the reviewed type-B
argument and is credited as such. The root-system result, Smith normal
form, determinant bounds, half-integrality, and both collapsing examples
are not claimed as new. The proof is unformalized and imports
Berline--Vergne; the previous review does not review this extension.

Exact finite checks use general integer-image membership, noncoordinate
face lattices and literal lattice counts. They corroborate rather than
prove the universal result by extrapolation. The primary papers checked
on bounded-determinant counting and maximal Ehrhart periods do not state
the displayed bimodular no-collapse theorem. This is a bounded novelty
check, not a priority certificate or a full nonsimple classification.
