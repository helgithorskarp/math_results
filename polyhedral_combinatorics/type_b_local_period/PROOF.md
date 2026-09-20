# Local simplicity prevents period collapse for type-B facet systems

Work in R^d with the fixed lattice Z^d. A polytope in this note is bounded
and full dimensional, with d>=1. Assume it has an irredundant facet description

    P={x : a_j x <= b_j for j=1,...,m},
    a_j in {+-e_i, +-e_i+-e_l : i!=l},     b_j in Z.           (1)

The signs in a two-coordinate row are independent. The normals are primitive
in Z^d. Integer offsets are required **after** this normalization. For
example, an inequality 2x_i<=1 is outside (1). These are polytopes cut out
by type-B roots with integral offsets; the lattice is not changed to a weight
lattice. No origin-containment assumption is made.

Let N(P) be the nonempty faces F whose affine span contains no point of Z^d.
If N(P) is nonempty, define

    g=min_{F in N(P)} codim(F),
    M(P)={F in N(P): codim(F)=g},    k=d-g.

**Theorem (local facet condition).** Suppose N(P) is nonempty and every
F in M(P) is contained in exactly g facets of P. Then, writing

    L_P(n)=|nP intersect Z^d|=A(n)+(-1)^n B(n),

with A,B in Q[n], one has

    deg B=k,
    [n^k]B=2^(-g-1) sum_{F in M(P)} vol_k(F)>0.               (2)

The volume uses the lattice in the face direction, with unit lattice cube
volume one and point volume one. In fact the directions of these particular
faces are coordinate subspaces. The minimal quasiperiod is exactly two;
the reduced denominator of the Ehrhart series E_P(t) is

    (1-t)^(d+1)(1+t)^(d-g+1).                               (3)

For H_P=(1-t^2)^(d+1)E_P, its zero at -1 has exactly order g and

    [H_P/(1+t)^g]_{t=-1}
       =2^(d-g)(d-g)! sum_{F in M(P)} vol_(d-g)(F)>0.         (4)

The condition concerns only the largest-dimensional faces in N(P). Other
faces, including integral vertices, may be nonsimple. It is a sufficient
condition, not a classification of all polytopes without period collapse.

**Corollary (simple polytopes).** Every simple polytope satisfying (1) has
minimal Ehrhart quasiperiod equal to its vertex denominator: one if it is a
lattice polytope, two otherwise. Equations (2)--(4) apply in the latter case.

We give the complete proof, including a signed-cycle local lemma valid for
every fixed rational scalar product. The only analytic input is the rational
local Euler--Maclaurin theorem of Berline--Vergne, precisely cited in SOURCES.md.

## 1. Integer affine points in signed constraint systems

At a relative interior point of a face, its active facet equations define
its affine span. Regard a two-coordinate equation

    alpha x_i + beta x_l = b,     alpha,beta in {1,-1},

as an edge on {i,l}, with propagation rule

    x_l = tau x_i + c,      tau=-alpha/beta in {1,-1}, c=b/beta in Z.

A unary equation is an integer coordinate pin. Parallel edges are allowed.
A cycle is called unbalanced if the product of its propagation signs is -1.
This includes a two-edge cycle of parallel constraints with independent
normals. A balanced cycle has product +1.

Choose a spanning tree in a connected active component. Every coordinate
then has the form s_i a+c_i, with s_i in {1,-1} and c_i integral. Each nontree
edge imposes either an identity, an inconsistent equation, or an equation
2a=c with integral c. Inconsistency cannot occur on a nonempty face. A pin
fixes a to an integer. Consequently a feasible component either has a free
parameter (choose a=0 to obtain an integral point), or fixes a to an integer
or strict half-integer. In the latter case every component coordinate is a
strict half-integer and there is no pin.

In particular all vertices of P are half-integral, and twice the affine span
of every face contains a lattice point. Rational Ehrhart theory therefore
gives the unique two-residue decomposition in the theorem.

If the affine span of a face has no lattice point, some component fixes a
to a strict half-integer. One nontree equation in that component witnesses
this; the edge together with its tree path is an unbalanced simple cycle,
possibly a two-edge cycle. Write its r equations in its r coordinates as

    Cx=b.                                                   (5)

The determinant has absolute value two. This follows by propagating round
the cycle, or by expanding the two nonzero permutation terms. Modulo two,
C is the incidence matrix of a cycle and has rank r-1. Every column of C
has two entries equal to +-1, so its integer image has even total sum; the
determinant gives

    C Z^r={u in Z^r : sum_i u_i is even}.                    (6)

Since (5) forces strict half-integers, sum_i b_i is odd. Conversely an
unbalanced cycle with odd sum of its integer right sides has a strict
half-integral solution in all its coordinates. Every proper subset of its
edge equations is a forest and has an integral solution for any integer
right sides, by tree propagation.

These are statements about affine equations. Their integral solutions need
not satisfy any inactive inequalities, a distinction essential below.

## 2. Why the local facet hypothesis is enough

We first record an elementary face fact. Suppose a codimension-q face F of
a full-dimensional polytope lies in exactly q facets. Their normals have
rank q because their equations define aff(F). Every subset I of these
facets intersects P in a face of codimension |I| that contains F.

To see the last assertion directly, take x in relint(F). All other facet
inequalities have positive slack. Independence allows a vector w whose
scalar products with the selected facet normals are zero and whose scalar
products with all remaining active normals are -1. For small positive
epsilon, x+epsilon w lies in P and has exactly the selected equalities
active. Thus the intersection has the claimed affine span and dimension.
No assumption about simplicity of the vertices of F was used.

Apply this to F in M(P). Section 1 supplies an unbalanced cycle of length r
among its g active facets, with odd right-side sum. The intersection G of
just those cycle facets is nonempty and has codimension r by the face fact.
Every point of aff(G) has the strict half-integer cycle coordinates forced
by (5), so G belongs to N(P). The definition of g implies r>=g, while the
cycle uses at most g active facets. Hence r=g, and the active system of F
is exactly this cycle: there are no additional pins, branches, or components.

It follows that aff(F) fixes precisely those g coordinates and leaves every
outside coordinate free. In particular the quotient lattice in its transverse
space is the literal coordinate Z^g. This proves the structural assertion
needed to use the next lemma. It is also the step that fails without the
local facet condition: imposing r cycle equalities can then cut out a face
of codimension greater than r.

## 3. Signed-cycle cone lemma

**Lemma.** Let C be a signed unbalanced r-cycle matrix as in (5), r>=2,
and let b be integral with odd coordinate sum. For n integral put

    K_n={y in R^r : Cy<=n b},
    v=C^(-1)b,        K_n=nv+K_0.

For the Berline--Vergne analytic cone function mu defined using any one
fixed rational scalar product and the lattice Z^r,

    mu(K_even)(0)-mu(K_odd)(0)=2^(-r).                     (7)

All quotient functions in the proof use the induced scalar product and
quotient lattice.

**Proof.** Put T=C^(-1) and ell_j(xi)=<xi,T e_j>. By (6), the slack vector
u=nb-Cy gives a bijection between the lattice points of K_n and

    u in Z_{>=0}^r,       sum_j u_j = n (mod 2).

The exponential lattice sum S(K_n), after removing the vertex exponential,
therefore satisfies

    exp(-n<v,xi>) S(K_n)(xi)
      =1/2 [ product_j(1-exp(-ell_j))^(-1)
            +(-1)^n product_j(1+exp(-ell_j))^(-1)].           (8)

This holds first where the sums converge and then meromorphically. The
cone is simplicial because C is invertible. Its faces correspond bijectively
to subsets I of the row indices: D_n(I) has equality on I and retains all
inequalities on the other rows. Its dimension is r-|I|.

For every positive-dimensional D_n(I), the subset I is proper. Choose an
integral z_I with C_I z_I=b_I by the forest property. Then

    v-z_I in ker(C_I)=lin(D_0(I)).

Thus in the quotient map pi_I:R^r -> R^r/lin(D_0(I)),

    pi_I(v)=pi_I(z_I) belongs to pi_I(Z^r).                 (9)

Equations (9) specify the entire lattice bookkeeping: the transverse cones
at D_n(I) differ by an actual integer quotient translation, so their mu
functions agree. The lattice-normalized face integrals obey

    exp(-n<v,xi>) I(D_n(I))(xi)=I(D_0(I))(xi).

Use the cone identity S(K)=sum_D mu(t(K,D)) I(D) at n=0 and n=1,
after removing each vertex exponential. Every positive-dimensional face
term cancels, including the full cone. The only surviving face is the
vertex, so (8) gives

    mu(K_0)(xi)-mu(K_1)(xi)
       =product_j(1+exp(-ell_j(xi)))^(-1).                 (10)

The right side is analytic at zero and equals 2^-r there. Also 2v is
integral, so lattice-translation invariance extends the two cases to all
even and odd n. This proves the lemma. There is no assumption about the
signs of individual mu values, and no raw constant-term extraction from
the singular unsigned product. Neither coordinate sign switches nor odd
cycle length is required. In particular the lemma includes unbalanced
even cycles and digons. QED.

## 4. Assembly, period, and simple polytopes

The imported local Euler--Maclaurin formula, for positive integers n, is

    L_P(n)=sum_{F face of P} mu(t(nP,nF))(0) vol(F) n^dim(F).

The coefficient attached to F is periodic with period dividing the smallest
q for which q aff(F) meets the lattice. Thus all degrees above k=d-g are
constant across even/odd residues. In degree k the only possible variation
comes from M(P). By Section 2 their transverse cones have the form in
Section 3 with r=g. Hence the even-minus-odd coefficient in degree k is
2^-g times their volume sum. Since B is half the difference of the residue
polynomials, this proves (2). Positivity proves exact degree and period.
Equality of residue polynomials extends identities to n=0.

The series of a polynomial of degree k and leading coefficient beta has a
pole of order k+1 with leading limit beta k!. Applied to the alternating
part this gives the exact pole at -1; positive d-volume gives exact order
d+1 at 1. Half-integrality allows no other poles. This proves (3), and
multiplication by (1-t^2)^(d+1) gives (4).

If P is simple, every codimension-q face is contained in exactly q facets,
so the local hypothesis is automatic. If P is not a lattice polytope, one
of its vertices lies in N(P), and the theorem applies. If P is a lattice
polytope, every nonempty face contains an integral vertex and N(P) is empty;
its Ehrhart function is polynomial. Half-integrality makes the vertex
denominator exactly two in the nonlattice case. This proves the corollary.

## 5. Relation to graph polytopes

For P_G={x in [0,1]^d:x_i+x_j<=1 on graph edges}, the previously proved
graph theorem classifies the maximum-dimensional faces in N(P) as those
fixing a shortest odd cycle to 1/2. At such a face, choose all outside
coordinates to be a common sufficiently small positive epsilon. Exactly
the cycle edge inequalities are active. The remaining bounds on nonisolated
vertices may be removed as redundant; each cycle edge inequality is a facet.
Thus the local hypothesis holds with g equal to odd girth, even if the
whole graph polytope is nonsimple. Equations (2)--(4) recover the full graph
theorem, not merely its simple instances. Its independent review is credited
in SOURCES.md; that review does not assess this new extension.

## 6. A sharp limitation and the first dimension of failure

Consider the three-dimensional polytope

    Q={ (x,y,z): x>=0, x<=y<=1-x, x<=z<=1-x }.              (11)

All five inequalities have the permitted primitive normals and integer
offsets. The four base vertices are (0,0,0),(0,1,0),(0,0,1),(0,1,1), and
the remaining vertex is (1/2,1/2,1/2). Its affine span misses Z^3, while
every positive-dimensional face contains a base vertex and hence has an
integral affine point. Thus g=3, but the fractional vertex lies in four
facets. The local condition fails.

Direct slicing gives

    L_Q(n)=sum_(a=0)^floor(n/2) (n-2a+1)^2=binom(n+3,3),

by the elementary even/odd sums of squares. Therefore Q has denominator
two and Ehrhart period one. Q is not a new counterexample: under the
integer determinant-one-in-absolute-value map

    (u,v,w) -> (w,u,v+w),

it is Stanley's classical period-collapse pyramid with base
(0,0,0),(1,0,0),(0,1,0),(1,1,0) and apex (1/2,0,1/2), as recorded by
McAllister--Woods. We use it to locate the failed local implication, not
to claim a new period-collapse construction.

In particular the two cycle equations x=y and x+y=1 already force z=1/2
through the other inequalities, so their intersection with Q has
codimension three, not two. A cycle-length formula without local facet
control is invalid. Local simplicity is sufficient and cannot simply be
deleted from a universal theorem about (1).

Every polygon is simple and every interval with the primitive integer
bounds in (1) is integral. The corollary and (11) consequently show that
**dimension three is the smallest dimension in this facet-normal class
where period collapse can occur**. This is a relative statement about (1);
rational polygons outside this class can exhibit period collapse.

## Verification and novelty boundary

The general signed-system and face arguments are unformalized proofs. The
checker uses independent rational vertex/facet incidence calculations and
direct integer counts to test the hypotheses and formulas on compact
fixtures, including the nonsimple failure. It does not implement or prove
the imported Berline--Vergne construction. Search-relative new scope is the
local facet criterion and its simple type-B-normal consequence; the general
root-normal setting, half-integrality, graph special case, and Stanley
pyramid are credited background. No exhaustive priority claim or
classification without the local condition is made.
