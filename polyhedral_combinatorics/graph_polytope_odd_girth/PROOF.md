# Odd girth determines the parity pole of a graph polytope

Let G be a finite simple graph on d>=1 vertices. Include isolated vertices
by defining the bounded graph polytope

    P_G={x in [0,1]^d : x_u+x_v<=1 for every edge uv of G}.

Without isolated vertices this is the usual fractional stable-set polytope.
It is full dimensional. Put

    L_G(n)=|nP_G intersect Z^d|,
    F_G(t)=sum_(n>=0) L_G(n)t^n,
    H_G(t)=(1-t^2)^(d+1) F_G(t).

The unreduced denominator in H_G is part of the normalization.

**Theorem.** If G is bipartite, L_G is a polynomial and has minimal
quasiperiod one. Otherwise let g be the length of a shortest odd cycle
and let C_g(G) contain its unoriented shortest odd cycles, each counted
once. Write k=d-g. For C in C_g(G), define

    F_C=P_G intersect {x_v=1/2 for all v in V(C)}.

This is a k-dimensional face. Let vol_k(F_C) denote volume in the remaining
coordinate directions, normalized so their unit lattice cube has volume
one; a zero-dimensional point has volume one. Then the unique decomposition

    L_G(n)=A_G(n)+(-1)^n B_G(n),     A_G,B_G in Q[n],

satisfies

    deg B_G=k,
    [n^k]B_G(n)=2^(-g-1) sum_(C in C_g(G)) vol_k(F_C)>0.       (1)

Consequently the minimal quasiperiod is exactly two. The reduced
denominator of F_G is, up to a nonzero constant,

    (1-t)^(d+1) (1+t)^(d-g+1).                              (2)

The zero of H_G at -1 has exactly order g, and

    [H_G(t)/(1+t)^g]_(t=-1)
       =2^k k! sum_(C in C_g(G)) vol_k(F_C)>0.                (3)

Thus the Ehrhart quasipolynomial distinguishes bipartiteness and recovers
the shortest odd-cycle length. No statement about gamma positivity or
real-rootedness is made.

## 1. The local Euler--Maclaurin input

We use the rational local Euler--Maclaurin theorem of Berline--Vergne;
see SOURCES.md for the exact version and locations. Fix the standard
rational Euclidean scalar product and the lattice Z^d. Its analytic cone
function mu has these properties:

- mu is invariant under translation by the lattice of its ambient quotient.
- For an affine rational pointed cone K,

      S(K)(xi)=sum_(D face of K) mu(t(K,D))(xi) I(D)(xi),       (4)

  where S is the lattice exponential sum, I the lattice-normalized
  exponential integral, and t(K,D) the affine transverse cone, with the
  quotient lattice. Analytic functions on quotient dual spaces are pulled
  back by the fixed orthogonal projection.
- For a rational polytope P and positive integer n,

      |nP intersect Z^d|=sum_(F face of P)
          mu(t(nP,nF))(0) vol(F) n^(dim F).                  (5)

  The factor mu(t(nP,nF))(0) is periodic in n with period dividing the least
  q>0 for which q aff(F) contains a lattice point.

These are imported theorems, not established by our finite checker. In
particular, (5) identifies each coefficient by faces of exactly its
dimension. It also makes the affine-span lattice condition, rather than
the denominator of individual vertices alone, the relevant invariant.

## 2. Active equality components and affine lattices

At a relative interior point of a face F, record all active equalities:

    x_v=0 or x_v=1,      x_u+x_v=1 for active edges uv.

They define aff(F). Call the coordinate equalities pins, and let J be the
graph of active edges, keeping isolated vertices. On each connected
component of J, the edge equations propagate values alternately as a and
1-a.

If the component is bipartite and unpinned, a is a free real parameter,
so the equality rank on s vertices is s-1. Setting a=0 gives an integral
solution. If it is bipartite and pinned, feasibility makes all pins
consistent, fixes a to zero or one, and the rank is s. If the component
is nonbipartite, an odd cycle forces a=1/2, every coordinate in that
component equals 1/2, and the rank is s. Such a component cannot be pinned
on a nonempty face. These statements include isolated free or pinned
coordinates.

Therefore

    aff(F) contains an integer point
       iff every active-edge component is bipartite.        (6)

Only the affine equations are at issue: the integral point need not belong
to F. For every face, twice its affine span contains an integer point.
At a vertex every component has full rank, so all coordinates lie in
{0,1/2,1}. This also directly proves that P_G has denominator dividing two.
Ehrhart theory gives the displayed two-residue decomposition of L_G.

If G is bipartite, all its vertices are integral by this argument, so L_G
is polynomial. Henceforth assume G has finite odd girth g.

Every nonbipartite active component contains at least g vertices and
contributes at least g to the equality rank. Thus

    aff(F) contains no integer point ==> codim(F)>=g.        (7)

If equality holds in (7), there is exactly one nonbipartite component,
on g vertices, and no other positive-rank component or pin. That component
contains a g-cycle using all its vertices. A shortest odd cycle has no
chord: a chord splits it into two cycles, one of which is odd and shorter.
Thus the active component is exactly one shortest odd cycle C; all other
coordinates are free in aff(F).

Conversely, setting the coordinates of any shortest odd cycle to 1/2 is
equivalent to imposing equality on its g edge inequalities. Their normals
have rank g. The resulting intersection is a face F_C. Set all other
coordinates to a common epsilon with 0<epsilon<1/2. Every inequality
outside C is then strict, since C has no chord. Hence dim(F_C)=d-g,
aff(F_C) contains no integer point, and vol_k(F_C)>0.

It follows that the faces in (7) of maximum possible dimension are
**precisely** the F_C, one for each unoriented shortest odd cycle. There is
no overcount: a shortest cycle is induced, so its vertex set determines
its cycle edges. Distinct cycles give distinct affine coordinate faces.

By (5), every Ehrhart coefficient of degree greater than k=d-g is constant
in n. All possible parity variation in degree k comes from these F_C.
It remains to calculate its sign and rule out cancellation.

## 3. A universal local jump at an odd-cycle face

The tangent directions along F_C are exactly the outside coordinate
directions. Their quotient lattice is Z^g in the coordinates of C, not a
rescaled or projected nonstandard lattice. At a relative interior point
only the g cycle edge inequalities are active. Thus the affine transverse
cone of nP_G at nF_C is

    K_n={y in R^g : y_i+y_(i+1)<=n cyclically},
    v_n=(n/2)1,      K_n=v_n+K_0.                           (8)

This is a full-dimensional pointed simplicial cone. Let S be cyclic shift,
C=I+S, and

    T=C^(-1)=(1/2)sum_(j=0)^(g-1)(-S)^j.

Since g is odd, C Z^g is exactly the lattice of even-total-sum integer
vectors. One proof is that C has determinant 2, every image has even
coordinate sum, and that parity sublattice has index 2. Equivalently the
displayed inverse shows that every coordinate of 2Tu is congruent to
sum u_i modulo two.

For the slack vector u=n1-Cy, lattice points of K_n correspond bijectively
to

    u in Z_(>=0)^g,      sum u_i = n (mod 2),
    y=v_n-Tu.

Write ell_j(xi)=<xi,T e_j>. In a common convergence region, and then as
meromorphic functions, the parity filter yields

    exp(-<v_n,xi>) S(K_n)(xi)
      = (1/2) [ product_j (1-exp(-ell_j))^(-1)
             +(-1)^n product_j (1+exp(-ell_j))^(-1) ].        (9)

We now extract the *local mu coefficient*, not a raw constant term of a
singular generating function. Every positive-dimensional face D_n of K_n
has a proper subset of the cycle inequalities active. That subset is a
forest of paths, so its equations y_i+y_(i+1)=1 have an integer solution z.
For the corresponding face D_0 of K_0 this says

    v_1-z in lin(D_0).

The quotient projection of v_1 is therefore a lattice vector. The cones
t(K_n,D_n) differ from t(K_0,D_0) by n times that quotient lattice vector,
so their mu functions agree for all integer n. Also

    exp(-<v_n,xi>) I(D_n)(xi)=I(D_0)(xi).

Apply (4) to K_0 and K_1, removing their vertex exponentials. Every term
from a positive-dimensional face cancels in the difference. The remaining
zero-dimensional face term is mu(K_0)-mu(K_1), because I({v_n}) is the
vertex exponential. Equation (9) therefore proves the analytic identity

    mu(K_0)(xi)-mu(K_1)(xi)
       =product_j (1+exp(-ell_j(xi)))^(-1).

At xi=0 this gives the universal positive jump

    mu(K_even)(0)-mu(K_odd)(0)=2^(-g).                     (10)

Even/odd here means integer n of the indicated parity; translating K_n by
an integer all-ones vector changes n by two and leaves mu unchanged.
The cancellation argument works with the same rational scalar product
throughout. It accounts for every proper-face term and all quotient-lattice
normalizations; it does not assume positivity of arbitrary mu values.

## 4. Assembly and the exact pole

For a face whose affine span contains an integer point, the coefficient
in (5) is independent of n. By Section 2 the only remaining faces of
dimension k are the F_C. Applying (10) to (5) thus gives

    [n^k](L_even(n)-L_odd(n))
       =2^(-g) sum_C vol_k(F_C).

Here L_even and L_odd are the unique residue polynomials evaluated at the
same formal variable n. Since B_G=(L_even-L_odd)/2, this proves (1), and
the strict positivity proves that no period collapse occurs.

The generating function of a degree-k polynomial b n^k+lower terms has a
pole of exact order k+1 at t=1 with leading limit b k!. Replacing t by -t,

    lim_(t -> -1) (1+t)^(k+1) sum_(n>=0) (-1)^n B_G(n)t^n
       =k! [n^k]B_G.

The A_G series is analytic at -1. Positive d-dimensional volume gives a
pole of exact order d+1 at 1, and period dividing two allows no other
poles. This proves (2). Finally,

    H_G/(1+t)^g=(1-t)^(d+1)(1+t)^(k+1)F_G,

whose limit at -1 is 2^(d+1) k! [n^k]B_G. Substituting (1) proves (3).
The proof covers disconnected graphs and isolated vertices; neither
connectedness nor a nonsimplicial-vertex exclusion is assumed.

## 5. A counting specialization and a necessary hypothesis

Suppose every shortest odd cycle is dominating, meaning that each outside
vertex has a neighbor on that cycle. On F_C every outside coordinate is
then at most 1/2. All inequalities between outside coordinates become
automatic, so F_C is the k-cube [0,1/2]^k in its free coordinates. If c_g
is the number of shortest odd cycles, formulas (1) and (3) simplify to

    [n^k]B_G = c_g/2^(d+1),
    [H_G/(1+t)^g]_(t=-1)=k! c_g.                            (11)

For example, in the complete graph K_d (d>=3), g=3 and c_g=binom(d,3),
so the residual is d!/6. The general face-volume formula is necessary:
take a triangle on 0,1,2 and attach the path 2-3-4. Its only shortest-cycle
face has free coordinates 0<=x_3<=1/2, 0<=x_4<=1, x_3+x_4<=1, of area
3/8, not 1/4. Formula (11) cannot be used without domination.

## Attribution and verification boundary

Half-integrality and bipartite integrality of fractional stable-set
polytopes are established background. The odd-cycle case of the pole is
also prior. The graph-first precursor isolates parity at a single odd-cycle
vertex; this proof instead identifies all relevant faces for an arbitrary
graph and proves that their leading contributions cannot cancel.

The claimed new scope, relative to the searched sources, is the exact
odd-girth order and the positive shortest-cycle-face volume formula for
all finite simple graphs. Berline--Vergne's rational local Euler--Maclaurin
formula is an explicit external mathematical premise. The exact Python
checker corroborates the graph and lattice conventions, coefficients and
poles; it does not formalize that theorem or prove the universal claim by
finite extrapolation. Independent review of this proof is not asserted.
