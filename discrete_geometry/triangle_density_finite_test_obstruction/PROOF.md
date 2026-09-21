# No finite fixed triangle suite certifies density preservation

For a noncollinear real triangle T, let D(T) mean that the points at rational
Euclidean distance from all three vertices are dense in the plane. Let
D₂(T) be the analogous rational-*squared*-distance property. These extension
points are not required to have rational pairwise distances.

The previously reviewed affine-preserver theorem says that an invertible
ambient affine map preserves D for every triangle if and only if its linear
part is rO, with r>0 rational and O real orthogonal. It supplies two fixed
unit right triangles and a third, map-dependent, valuation triangle as a
certificate. We determine whether this dependence can be removed.

## 1. Finite-testing obstruction

**Theorem.** For every finite family of noncollinear real triangles
T₁,…,Tₛ and every ε>0, there is a positive irrational λ with

    λ² ∈ Q,       1 < λ < 1+ε,

such that, for every j,

    D(λTⱼ) ⇔ D(Tⱼ),       D₂(λTⱼ) ⇔ D₂(Tⱼ),              (1)

but the homothety F(x)=λx is not a universal D-preserver. In fact, the
positive scales satisfying (1) but failing universal preservation form a
dense subset of (0,∞).

The test triangles may be admissible or inadmissible, may have arbitrary
real coordinates, and are fixed independently of the map being tested.
Thus allowing negative test instances or squared-distance queries cannot
make a finite fixed suite sufficient.

**Corollary.** Among invertible ambient affine maps, the least cardinality
of a fixed family of ordinary-admissibility tests certifying universal
D-preservation is countably infinite. One explicit family is

    T* = (0, R_(π/8)e₁, R_(π/8)e₂),
    T_d = (0, (1,0), (0,√d))       for d=1,2,3,… .         (2)

By contrast, the preceding affine theorem already proves that two fixed
triangles suffice for universal D₂-preservation. We do not change either
preserver group or claim a new density theorem.

## 2. Reduction to simultaneous similarity factors

For edge matrix B=[P₁−P₀ P₂−P₀], put G=BᵀB. We use the published criteria
of Corvaja–Turchet–Zannier (Theorems 1 and 2 in the version of record;
1.1 and 1.2 in arXiv v2):

    D₂(T) ⇔ G has rational entries,
    D(T)  ⇔ G has rational entries and zᵀGz=1 for some z∈Q².    (3)

Their proofs are external inputs. Representing one is equivalent to
representing a nonzero rational square. No correction to (3) is asserted.

If α>0 is rational, G is rational exactly when αG is rational. Hence
triangles with an irrational Gram entry automatically keep both negative
statuses under √α. For each of the finitely many rational Gram matrices,
it will suffice to construct a rational invertible Sⱼ with

    SⱼᵀGⱼSⱼ = αGⱼ.                                      (4)

This preserves the *entire set of rational values* of the form, and in
particular whether it represents one, without knowing that answer.
The matrices Sⱼ can differ with j. They are changes of rational edge
coordinates, not the common ambient homothety √αI.

Write a rational positive-definite binary matrix as

    G=[[a,b],[b,c]],       δ=ac−b²>0.

With C=[[1,b/a],[0,1/a]], direct multiplication gives

    G = a Cᵀ diag(1,δ) C.

If α=u²+δv² with u,v rational, then

    H=[[u,−δv],[v,u]],    Hᵀ diag(1,δ) H=α diag(1,δ),
    S=C⁻¹HC

satisfies (4), with det S=α≠0. Such α are exactly the nonzero norm values
from Q(√−δ): equivalently, they are the similarity factors of this binary
form. For the converse, conjugate a proposed S by C and take the norm of
its first column. This is a classical quadratic-norm identity.

We therefore need a positive nonsquare rational number which is a norm
from each of finitely many imaginary quadratic fields. The next two
sections give a self-contained effective construction.

## 3. An elementary bound excluding square polynomial values

**Polynomial lemma.** Suppose P∈Z[t] is monic of degree 2m≥2, is positive
on the real line, and is not a square in Q[t]. There is an explicitly
computable integer N such that P(n) is a positive nonsquare integer for
every integer n≥N.

Construct the unique monic Q∈Q[t] of degree m such that

    R=P−Q² has degree at most m−1.

Determine the coefficients of Q successively, matching those of P from
degree 2m−1 down through m; each step divides by two. R is nonzero.
Let L be a positive common denominator of the coefficients of Q, and put

    A = sum of absolute values of the nonleading coefficients of Q,
    C₀ = sum of absolute values of the coefficients of R,
    B₀ = sum of absolute values of the nonleading coefficients of R,
    r  = the nonzero leading coefficient of R.

Choose an integer N strictly greater than

    max(1, 2A, 2LC₀, 1+B₀/|r|).                          (5)

For n≥N, leading-term dominance gives Q(n)>n^m/2 and R(n)≠0. Also
|R(n)|≤C₀n^(m−1). Consequently

    0 < |√P(n)−Q(n)|
      = |R(n)|/(√P(n)+Q(n)) < 2C₀/n < 1/L.

But Q(n)∈(1/L)Z. If √P(n) were an integer, its nonzero distance from Q(n)
would be at least 1/L, a contradiction. A rational square root of an
integer is integral, so rational squares are excluded as well. ∎

The polynomial-part approximation at infinity is a classical elementary
instance of Runge's method. The proof and the sufficient, nonoptimal bound
(5) are given here to avoid an unbounded search for nonsquare norm values.
No theorem about prime values, squarefree values, or Chebotarev is required.

## 4. Constructing a nonsquare common norm

Let δ₁,…,δ_k be positive rationals. For each δⱼ=pⱼ/qⱼ in lowest terms,
set rⱼ=−pⱼqⱼ, so Q(√−δⱼ)=Q(√rⱼ) and rⱼ is a negative integer.
Select a basis r₁′,…,r_h′ of their square classes in Q*/Q*² from this list.
It can be selected without factoring: test the finitely many subset products
for being a rational square times the proposed next radicand.

Let

    K=Q(√r₁′,…,√r_h′),       θ=√r₁′+⋯+√r_h′.

The standard multiquadratic basis consists of products of distinct radicals;
independence of the square classes gives [K:Q]=2^h and all independent sign
changes as automorphisms. The 2^h signed sums of the radicals are distinct:
any equality would be a nontrivial rational linear relation among distinct
basis elements. Hence θ is primitive. It is also an algebraic integer.

All r_i′ are negative, so every conjugate of θ is purely imaginary and
nonzero. Complex conjugation pairs them with their negatives. It follows
that

    P(t)=N_(K/Q)(t−θ)

is a monic integer polynomial of positive even degree, is positive for every
real t, and has distinct roots. In particular it is not a polynomial square.
The polynomial lemma produces an explicit n and positive nonsquare integer

    α=P(n)=N_(K/Q)(n−θ).                                  (6)

For each Kⱼ=Q(√−δⱼ)⊂K, transitivity of field norms gives

    α=N_(Kⱼ/Q)( N_(K/Kⱼ)(n−θ) )=uⱼ²+δⱼvⱼ²

with uⱼ,vⱼ∈Q. This supplies all the matrices in (4). Both norm operations
can be evaluated by multiplying the appropriate conjugates. Nothing asserts
that *every* common norm comes from K; only this inclusion is used.

If the list of rational Gram matrices is empty, take any positive nonsquare
integer, for instance two. For uniform implementation one may instead use
K=Q(i) in this empty case.

Every positive rational multiple q of √α is irrational, and q²α remains a
common norm: replace each norm witness (uⱼ,vⱼ) by (quⱼ,qvⱼ). The set
{q√α:q∈Q_(>0)} is dense in (0,∞). This proves (1) and the near-identity and
density assertions, except for nonuniversality.

## 5. A missed triangle always exists; countable tests suffice

The reviewed preserver theorem already excludes every positive irrational
scale. For completeness, its arithmetic witness applies directly here.
Since q²α is a positive rational nonsquare, some prime p has odd valuation
in it. If p=2 take d=3. Otherwise take a positive integer d with −d a
quadratic nonresidue modulo p. Every nonzero rational value of x²+dy² has
even p-valuation. For odd p this follows by removing the common valuation
and reducing modulo p. For p=2,d=3, primitive integer coordinates give norm
valuation zero or two, and rational rescaling changes it by an even integer.
Thus

    q²α(x²+dy²)=1

has no rational solution. The triangle T_d from (2) is admissible, since
its form x²+dy² represents one, whereas its image is not. This completes
the theorem. The missed triangle cannot have been among the finite tests
with a positive status.

The family (2) certifies the universal group because T₁ and T* first force
AᵀA=αI with positive rational α by the reviewed two-rotation argument.
Indeed, write AᵀA=[[a,b],[b,c]]. Passing T₁ makes a,b,c rational. Passing
T* also makes its rotated Gram matrix rational; its diagonal difference is
(a−c+2b)/√2 and its off-diagonal entry is (c−a+2b)/(2√2). Both numerators
are rational, so both vanish, giving b=0 and a=c.
Every remaining nonsquare α fails one T_d by the preceding valuation proof.
Rational scales and real orthogonal maps preserve all these tests. Thus a
countable fixed family suffices. The theorem excludes every finite family,
so the least cardinality is precisely countably infinite. ∎

One can also allow later queries to depend only on previous yes/no
admissibility answers. Any deterministic procedure that always terminates
must terminate when the tested map is the identity. Its finitely many
queries on that path are matched by an excluded homothety from the theorem,
which therefore follows the same path and receives the same verdict.
Such a procedure cannot always decide membership correctly. This statement
concerns only admissibility answers; it does not restrict procedures that
inspect the map's coefficients or observe all image coordinates. The earlier
map-dependent third test uses precisely that additional information.

## 6. A small explicit example

The norm polynomial for K=Q(i,√−3), θ=i+√−3, is

    P(t)=t⁴+8t²+4.

Already at t=1 its value 13 is nonsquare and

    13=2²+3²=1²+3·2².

Hence √13 preserves admissibility for every rational binary form whose
determinant square class is 1 or 3. In particular it passes both unit right
triangles of the geometric rigidity test and every triangle with Gram
rationally congruent to diag(1,3). The closer-to-identity scale

    λ=5√13/18,        λ²=325/324

has the same property. But −2 is a nonsquare modulo 13, so T₂ is missed:
its form x²+2y² is admissible, whereas (325/324)(x²+2y²) cannot represent one.
This example illustrates the universal obstruction; it is not the proof for
an arbitrary finite suite.

## Reproducibility, attribution, and limits

`construct.py` accepts a finite list of exact rational positive-definite
2-by-2 Gram matrices and a positive rational ε. It returns a nonsquare
integer common norm, its polynomial certificate, each rational norm witness
and similitude matrix, and a rational squared scale in (1,(1+ε)²).
For the last step choose integers M,a with a=floor(M√α)>1/ε and set q=M/a.
Then 1<q√α<1+1/a<1+ε, checked without floating point.

`verify.py` checks the output identities, computes the norm independently as
a multiplication-matrix determinant, tests dependent square classes and
rational denominators, and rejects malformed forms and square polynomials.
The universal theorem is the written argument, not the finite audit.
The field arithmetic is exponential in the square-class rank; no polynomial-
time or arbitrary-real-input algorithm is claimed. Detecting which unspecified
real Gram entries are rational is outside the code's interface.

The density criteria, quadratic norm interpretation, transitivity of norms,
multiquadratic fields, and approximation at infinity are established tools.
Our claim is the resulting finite-versus-adaptive obstruction and exact
cardinality of fixed triangle test suites, new to the bounded searched
sources. Historical priority is unestablished. The prior affine classification
is not reproved in full or presented as new. This does not resolve Erdős–Ulam,
classify nonlinear maps, or treat density relative to four or more anchors.
See SOURCES.md for primary references and the explicit dependency boundary.
