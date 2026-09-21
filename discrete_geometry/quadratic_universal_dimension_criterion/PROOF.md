# A complete coefficient criterion for the quadratic half-total bound

All dimensions below are Hausdorff dimensions. Sets are nonempty and
compact. Write

    Q(x,y,z) = a*x^2 + b*y^2 + c*z^2 + d*x*y + e*x*z + f*y*z
               + g*x + h*y + i*z + j,

with arbitrary real coefficients. Degree smaller than two is allowed.

## Theorem

The following statements are equivalent.

1. For every A,B,C contained in R with
   S = dim_H A + dim_H B + dim_H C <= 2,
   we have dim_H Q(A x B x C) >= S/2.
2. Both conditions (L) and (R) below hold.

Condition (L), the coordinate-line condition, is the conjunction

    a != 0  OR  (d=e=0 AND g != 0),
    b != 0  OR  (d=f=0 AND h != 0),
    c != 0  OR  (e=f=0 AND i != 0).

Condition (R) says that at least one of the following affine polynomials
is not identically zero:

    J_x(y,z) = (d*f-2*b*e)*y + (2*c*d-e*f)*z + d*i-e*h,
    J_y(x,z) = (d*e-2*a*f)*x + (2*c*d-e*f)*z + d*i-f*g,
    J_z(x,y) = (d*e-2*a*f)*x + (2*b*e-d*f)*y + e*h-f*g.

Thus the theorem is a finite equality/inequality test on nine coefficients;
the constant j is immaterial. Condition (L) is exactly that every restriction
to a line parallel to a coordinate axis is a nonconstant polynomial.
No equality between a product's Hausdorff dimension and the sum of its
factor dimensions is assumed anywhere.

## 1. Constant coordinate lines are an obstruction

For fixed y,z, the x restriction is

    a*x^2 + (d*y+e*z+g)*x + constant.

It is nonconstant for every y,z precisely when the first clause of (L)
holds. If a=0 and either d or e is nonzero, the affine equation
 d*y+e*z+g=0 has a solution. If a=d=e=0 and g=0, every x restriction is
constant. The other two variables give the remaining clauses.

If a constant coordinate line exists, vary its free coordinate over [0,1]
and fix the other two coordinates at that line. The dimension sum is one
and the image is a singleton. This disproves statement 1. Thus (L) is
necessary even without any assumption about additive structure.

## 2. The coefficient-map rank alternative

Separate the pinned coordinate z:

    Q(x,y,z) = c*z^2 + z*L_z(x,y) + R_z(x,y),
    L_z = e*x+f*y+i,
    R_z = a*x^2+b*y^2+d*x*y+g*x+h*y+j.

Then J_z is the determinant of D(L_z,R_z); the analogous definitions give
J_x and J_y. This is the coefficient-map rank principle used by
Arala--Chow, Lemma 1.5, and Pham's projection argument. For completeness,
the elementary real algebra needed here follows.

Suppose Q depends on all three variables and all three J's vanish.
Consider which of d,e,f are nonzero.

- If none is nonzero, Q is a sum of three univariate polynomials.
- If exactly one is nonzero, permute variables to make it d. The identities
  J_x=J_y=0 force c=i=0, so Q is independent of z, a contradiction.
- If exactly two are nonzero, permute variables to make them d,e. The
  x coefficient of J_z is d*e, a contradiction.
- If all three are nonzero, the displayed identities force

      a=d*e/(2*f),  b=d*f/(2*e),  c=e*f/(2*d),
      h=f*g/e,     i=f*g/d.

  Consequently, with T=x+(f/e)*y+(f/d)*z,

      Q = (d*e/(2*f))*T^2 + g*T + j.

In all possible cases Q=G(H(x)+K(y)+L(z)) for univariate polynomials.
Conversely, for a polynomial of degree at most two depending on all
variables, this additive form forces either a sum of univariate
polynomials or a univariate quadratic of a linear form: compare the degree
in each variable with deg G. In either case all three J's vanish.

In particular, if (L) holds then Q depends on every variable, and failure
of (R) is exactly this additive polynomial obstruction. This algebraic
alternative is a known ingredient, not a new classification claimed here.

## 3. A compact Cantor obstruction to additive structure

Let

    E = { sum_(n>=1) u_n*27^(-n) : every u_n belongs to {0,...,8} }.

Then dim_H E=log(9)/log(27)=2/3. One direct verification uses the 9^r
level-r cylinder intervals for the upper bound and the uniform cylinder
measure, of mass 9^(-r), for the lower bound. Level-r starting points are
separated by at least 27^(-r), and each cylinder has length
(4/13)*27^(-r). If 27^(-(r+1)) <= rho < 27^(-r), a ball of radius rho
meets at most four such cylinders, so its measure is at most
4*9^(-r) <= 36*rho^(2/3). The mass distribution principle proves the
lower bound. This is the standard separated-digit Cantor argument.

Digitwise addition involves no carries, and every digit from 0 to 24 is
the sum of three digits from 0 to 8. Hence

    E+E+E = { sum_(n>=1) v_n*27^(-n) : v_n in {0,...,24} }.

The 25^r cylinder cover gives

    dim_H(E+E+E) <= log(25)/log(27) < 1.

Suppose Q=G(H(x)+K(y)+L(z)) depends on all variables. Then H,K,L and G
are nonconstant. Choose a closed interval for each of H,K,L on which its
derivative is bounded away from zero. Their images contain intervals
r_1+epsilon*E, r_2+epsilon*E, r_3+epsilon*E for suitable real r_i and a
common epsilon>0. Define A,B,C by the three inverse branches. These branches
are bi-Lipschitz, so each factor has dimension 2/3, while

    Q(A x B x C) = G(r_1+r_2+r_3 + epsilon*(E+E+E)).

G is Lipschitz on the relevant compact interval. The image therefore has
dimension at most log(25)/log(27)<1=S/2. If (L) holds and (R) fails,
Section 2 supplies exactly this obstruction. Thus (R) is also necessary.
For a fully explicit example, Q=x^2+y^2+z^2 and A=B=C=sqrt(1+E) satisfy
(L) but fail the universal bound.

## 4. The positive-factor case from the sharp projection theorem

We use the following external theorem of Ren--Wang, *Furstenberg sets
estimate in the plane*, arXiv:2308.08819v3, Theorem 1.2. If K is a Borel
subset of R^2 and 0<=u<=min(dim_H K,1), then

    dim_H{theta in S^1 : dim_H pi_theta(K)<u}
        <= max(2*u-dim_H K,0).                         (RW)

This theorem is an analytic input; it is not established by our code.

Assume Q depends on all variables and satisfies (R). We first prove the
half-total bound when alpha=dim_H A, beta=dim_H B and gamma=dim_H C are
all positive and S=alpha+beta+gamma<=2. The argument also explains the
positive-factor case of Pham's displayed bound without invoking that bound
as an assumption.

Permute variables so J_z is nonzero, and denote the dimensions of the two
unpinned factors by alpha,beta and that of the pinned z factor by gamma.
Set P=(L_z,R_z).

If gamma>=S/2, some restriction z -> Q(x,y,z) with (x,y) in A x B is
nonconstant. Indeed, if c=0 its linear coefficient L_z cannot vanish on
the entire product of two infinite sets unless L_z is the zero polynomial;
that would make Q independent of z. If c!=0 every such restriction is
nonconstant. A nonconstant univariate polynomial preserves the Hausdorff
dimension of a compact set: outside its finitely many critical points it
is locally bi-Lipschitz, and a countable compact exhaustion covers that
complement. Thus dim_H Q(A x B x C)>=gamma>=S/2.

It remains to treat gamma<S/2. Fix 0<u<S/2. Choose
0<alpha'<alpha and 0<beta'<beta so that

    s=alpha'+beta' > u,        s+gamma > 2*u.

Choose probability Frostman measures mu,nu on A,B with respective
exponents alpha',beta'. Both are atomless. The zero set of the nonzero
affine polynomial J_z has (mu x nu)-measure zero: if its y coefficient
is nonzero, every vertical fibre is a singleton; if not, it is either
empty or a single vertical line. Fubini and atomlessness apply.

The regular set J_z!=0 has a countable cover by compact rectangles with
P bi-Lipschitz on each, obtained by shrinking inverse-function neighborhoods.
At least one rectangle I x J has positive product measure. Restrict and
normalize mu and nu to I and J. Their product remains an s-Frostman
measure supported on (A intersect I) x (B intersect J). Its image under P
is supported on a compact set K with dim_H K>=s. This step uses a lower
bound from Frostman measures, not product-dimension additivity.

For z in C, put theta(z)=(z,1)/sqrt(1+z^2). This map is bi-Lipschitz on
any bounded interval containing C, so dim_H theta(C)=gamma. By (RW),

    dim_H{theta : dim_H pi_theta(K)<u}
        <= max(2*u-dim_H K,0)
        <= max(2*u-s,0) < gamma.

Some z in C consequently satisfies dim_H pi_theta(z)(K)>=u. Since

    Q(x,y,z)=c*z^2 + sqrt(1+z^2)*pi_theta(z)(P(x,y)),

the full image has dimension at least u. Taking the supremum over
u<S/2 proves the half-total bound, including S=2. The pin may depend on u;
we claim a bound for the full image, not a single endpoint-optimal pin.

## 5. Zero-dimensional factors and completion

Suppose (L) and (R) both hold. If all three factor dimensions are positive,
Section 4 applies. Otherwise at most two are positive. Let m be their
maximum, so S<=2*m. Fix any points of the other two nonempty factors and
vary a factor of dimension m. By (L) this restriction is a nonconstant
univariate polynomial, so its image has dimension m. The full image has
dimension at least m>=S/2. If S=0 the desired inequality is automatic.
Together with Sections 1--3 this proves the equivalence.

## Scope and provenance

The universal coefficient criterion combines established projection and
rank ingredients with the exact missing coordinate-line condition. The
collapsing example x(y+z), {0}, [0,1], [0,1] is already in Pham's later
arXiv:2603.03567, Remark 1.10(i); it is not claimed as a new counterexample.
The earlier arXiv:2510.15118v2 Theorem 1.4(ii) motivates checking the
universal quantifiers. Only its intended quadratic regime is considered.
The journal landing page was checked, but the full journal version was
not available for comparison. No assertion about a journal correction is
made. The positive-measure theorem of Koh--Pham--Shen and the Euclidean
Falconer conjecture are separate from the criterion proved here.
