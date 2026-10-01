# A wider restricted tube for the degree-nine displacement functional

Actual author **six-sendov-2**, role **researcher**, 2026-10-01.
Status: ordinary written author proof with a reproducible exact rational
certificate; unformalized, independent review pending. The angular
interpretation, scalar optimizer and scalar curvature bound are credited
inputs identified in [LITERATURE.md](LITERATURE.md).

## 1. Statement and normalization

For a balanced nonzero real eight-vector theta, put

    mu_k = sum_j theta_j^k,   e = (1,...,1)/sqrt(8),
    P = I-ee^T,   C = P diag(theta) P restricted to e-perp,
    w = diag(theta)e,
    Psi = sum over distinct lambda of ||Pi_lambda w||^4,
    J = 122 mu_2 + (224 mu_4 - 5760 Psi)/mu_2.

The projections are onto full eigenspaces, including at collisions.
This is the credited angular displacement functional. We use maximum
normalization max_j |theta_j|=1, rather than unit Euclidean normalization.

Take alpha_1,alpha_2,alpha_3 >= 0 and define

    S = alpha_1+alpha_2+alpha_3,
    theta = (1-alpha_1,1-alpha_2,1-alpha_3,-1,-1,-1,S/2+x,S/2-x).

Assume the closed conditions

    0 <= S <= 1/100,    x >= 0,    1/16 <= u=x^2 <= 1/9.       (1)

Then theta is balanced and max-normalized; the last two coordinates
have magnitude at most 1/3+1/200<1. Independent deficits can create six
actual coordinate values. All coincidences between values are allowed.
Permutations and reflection theta -> -theta preserve the conclusions.
One of the two unit triples stays fixed throughout this tube.

Let the credited scalar function and algebraic optimizer be

    j(u) = (2058+21912u-15876u^2+19224u^3+3402u^4)
           /((3+u)(1+3u)^2),

    T(u) = 26634-231084u-907290u^2+376920u^3
           +971190u^4+224532u^5+30618u^6,
    u_* = the unique root of T in (2/25,9/100),
    J_* = j(u_*),
    theta_* = (1,1,1,-1,-1,-1,sqrt(u_*),-sqrt(u_*)).

The cited scalar theorem supplies, for 0<=u<=1/4,

    J_* - j(u) >= 450 (u-u_*)^2.                            (2)

**The new restricted-tube estimate is**

    j(u)-J(theta) >= 200 S.                                 (3)

Consequently, throughout (1),

    J_*-J(theta) >= 200 S + 450(u-u_*)^2.                    (4)

Equality J=J_* occurs precisely at the theta_* multiset. If O_* is its
permutation orbit after division by sqrt(6+2u_*), then also

    dist(theta/sqrt(mu_2),O_*)^2 <= (J_*-J(theta))/40.         (5)

The coefficient and total-deficit range in (3) are new in this restricted
domain. The credited unrestricted local theorem allows both unit triples
to move, but has S<=1/100000 and 2/25<=u<=9/100. Neither domain contains
the other in all its parameters. Its stronger distance constant 1/90
remains credited; (5) is a conservative bound on the present larger tube.
We do not assert a whole six-level maximum, a global theorem for every
profile with a saturated triple, or a first-power Tang--Zhang endpoint.

## 2. A filtered three-moment bound on the full compression

Write s_r=tr(C^r), with s_0=7, and b_i=w^T C^i w. Consider the symmetric
matrices

    B_i = C^i(I-C^2),  i=0,1,2,
    G_ij = s_(i+j)-2s_(i+j+2)+s_(i+j+4),
    r_i = b_i-b_(i+2),
    D = det G,   N = r^T adj(G) r.                          (6)

These formulas use the full seven-dimensional compression; they do not
delete repeated coordinate blocks. For any balanced real eight-vector
with D>0, we have the reusable bound

    Psi >= N/D,
    J <= Jhat := 122mu_2+(224mu_4-5760N/D)/mu_2.             (7)

Indeed, with the Frobenius inner product let W=ww^T. Its orthogonal
projection onto the symmetric matrices commuting with C is

    Q_C(W) = sum_lambda Pi_lambda W Pi_lambda.

Each block is a rank-one matrix on the full eigenspace, so
||Q_C(W)||_F^2=sum_lambda ||Pi_lambda w||^4=Psi. The polynomial space
span{B_0,B_1,B_2} lies in this commutant. Its Gram matrix is G and its
inner products with W are r. G is positive semidefinite, and D>0 makes
it positive definite. Orthogonal projection onto this smaller space has
squared norm r^T G^(-1)r=N/D. Nested orthogonal projections prove (7).
This argument includes collisions without choosing individual vectors
inside an eigenspace. The projection principle is classical.

The filter is exact along the entire credited reference face

    theta_ref(x)=(1,1,1,-1,-1,-1,x,-x),  0<=u=x^2<1.

Its slope polynomial is h(z)=(z^2-1)^3(z^2-u). The elementary balanced
Schur identities give

    det(zI-C)=h'(z)/8,
    w^T(zI-C)^(-1)w=z-8h(z)/h'(z).

Thus C has eigenvalues +1,-1 (multiplicity two each), 0, and +/-delta,
where delta^2=(1+3u)/4. The unit eigenvalues have zero w-weight. The other
three weights are

    r_0=4u/(1+3u),
    r_(+delta)=r_(-delta)=3(1-u)^2/(8(1+3u)).

A quadratic polynomial times 1-z^2 interpolates arbitrary values at
0,+delta,-delta and vanishes at the zero-weight unit eigenvalues. The
pinching Q_C(W) is therefore in span{B_i}, so (7) is an equality here.
The checker also verifies the complete polynomial identities

    D_ref = 81(1-u)^4(1+3u)^3/4096,
    N_ref = 81(1-u)^4(1+3u)[9(1-u)^4+512u^2]/131072.         (8)

D_ref>0 for 0<=u<1. Inserting N_ref/D_ref into J gives exactly j(u).
At u=1 the filtered Gram matrix has rank one; no division by its zero
determinant is justified. The domain (1) stays away from this boundary.
The general bound (7) is not a claim that Jhat<=J_* globally.

## 3. Complete polynomial encoding

All algebra for (3) takes place in Q[u,S,A_2,A_3], where

    A_2=sum_(i<j) alpha_i alpha_j,   A_3=alpha_1 alpha_2 alpha_3.

The Newton power sums p_k=sum_i alpha_i^k have p_0=3 and are generated
from the elementary symmetric functions S,A_2,A_3. The exact moments
through order eight are

    mu_k = 3(-1)^k + sum_(j=0)^k (-1)^j binom(k,j) p_j
           + 2 sum_(j even,0<=j<=k) binom(k,j)(S/2)^(k-j)u^(j/2).

In particular mu_1=0 as a polynomial. To obtain s_r for 1<=r<=8,
expand tr((diag(theta)P)^r) with P=I-ee^T. A word with no rank-one
factors contributes mu_r. A word with k>=1 rank-one factors, at cyclic
gaps g_1,...,g_k summing to r, contributes

    (-1)^k 8^(-k) product_i mu_(g_i).

Cyclic trace and P^2=P identify this trace with tr(C^r). The extra
eigenvalue zero in the full eight-dimensional matrix contributes nothing
for r>=1; s_0 must be seven. The checker enumerates all 2^r words, not
an inferred recurrence or sampled fit.

The Schur identity in Section 2 gives a second, exact moment series.
If f(t)=1+sum_(k>=1) mu_k t^k/8, then, since mu_1=0,

    1-1/f(t) = sum_(i>=0) b_i t^(i+2).

In particular the five required coupling moments are

    b_0=mu_2/8,
    b_1=mu_3/8,
    b_2=mu_4/8-mu_2^2/64,
    b_3=mu_5/8-mu_2 mu_3/32,
    b_4=mu_6/8-(2mu_2 mu_4+mu_3^2)/64+mu_2^3/512.            (9)

Equations (6) now define complete rational-coefficient polynomials D,N.
Let j_N,j_D be the numerator and denominator of j in Section 1, and put

    F = [(j_N-200S j_D)mu_2-j_D(122mu_2^2+224mu_4)]D
        +5760j_D N.                                       (10)

Then F>=0, together with D>0, mu_2>0 and j_D>0, is precisely the
cleared-denominator form of Jhat<=j(u)-200S.

For nonnegative alpha_i, the elementary inequalities

    0<=A_2<=S^2/3,  0<=A_3<=S^3/27

allow the substitution A_2=S^2 Y/3, A_3=S^3 Z/27 with 0<=Y,Z<=1.
For S=0 all alpha_i vanish and any Y,Z give the same moments. For
S>0 choose Y=3A_2/S^2 and Z=27A_3/S^3. We prove signs on the entire
rectangular domain in Y,Z, which can include elementary triples not
realizable by nonnegative alpha_i. No realizability premise is needed
for that overestimate.

After this substitution, F is divisible by S exactly. The checker
verifies division and multiplication back, and proves the following
two continuous-domain signs on the one closed box

    u in [1/16,1/9], S in [0,1/100], Y,Z in [0,1].

| Polynomial | Coordinate degrees (u,S,Y,Z) | Bernstein coefficients |
| --- | --- | ---: |
| substituted F/S | (11,21,9,7) | 21,120, all strictly positive |
| substituted D | (7,18,7,6) | 8,512, all strictly positive |

For clarity, affine substitution first maps each interval to [0,1].
For a power coefficient a_m in one coordinate of degree n, its
contribution to the Bernstein coefficient of index i>=m is
a_m binom(i,m)/binom(n,m). Apply this conversion to all four coordinates.
The resulting tensor-product Bernstein basis is nonnegative and sums
to one, including at the boundary. Strict positivity of every coefficient
therefore implies strict positivity of the polynomial on the closed box.
The entire inverse conversion back to the affine power polynomial is
also checked for both polynomials.

The exact minima, full polynomial hashes and coefficient-vector hashes
are in [expected.json](expected.json). Every coefficient is regenerated
from (6), (9), (10) and the Newton/trace formulas. No coefficient tensor
or private computation is a required external input.

For S>0, F>0 and D>0 prove J<=Jhat<j(u)-200S. For S=0, (8) gives
J=j(u). Thus (3) holds on every closed face of (1). Equation (2)
proves (4) and its equality assertion.

## 4. Distance to the credited orbit

Write v=theta_ref(x). The difference theta-v has coordinates
(-alpha_1,-alpha_2,-alpha_3,0,0,0,S/2,S/2), so

    ||theta-v||^2=sum_i alpha_i^2+S^2/2 <= 3S^2/2.

Both ||theta|| and ||v|| are at least sqrt(6):
mu_2=6+2u-2S+sum_i alpha_i^2+S^2/2>=6+1/8-1/50>6.
For nonzero vectors a,b, elementary normalization gives

    ||a/||a|| - b/||b|||| <= 2||a-b||/min(||a||,||b||).

Hence the first normalization distance is at most S. The reference
profiles at x and sqrt(u_*) differ by norm sqrt(2)|x-sqrt(u_*)|,
giving a normalized distance at most (2/sqrt(3))|x-sqrt(u_*)|.
Here x+sqrt(u_*)>1/2, using x>=1/4 and u_*>2/25, so this is at most
(4/sqrt(3))|u-u_*|. A matching permutation in O_* and the triangle
inequality yield

    dist^2 <= 2S^2+(32/3)(u-u_*)^2
            <= S/50+(32/3)(u-u_*)^2
            <= [200S+450(u-u_*)^2]/40.

Combining with (4) proves (5).

## 5. Check boundary and remaining frontier

The standalone checker also uses seven rational profiles, including
S=0, endpoint scalar values, S=1/100 and three distinct positive deficits.
For each it constructs the literal full 8x8 compression and checks its
moments, all eight trace powers, all five coupling moments, the nine
filtered Gram entries and the adjugate quotient. Independently, it projects
ww^T onto the full symmetric commutant using all 28 commutation equations
in 36 variables with the correct off-diagonal Frobenius weights. This
recovers the defining full-eigenspace Psi and checks both inequalities
in (7) and the local bound. It does not substitute a scalar secular
quotient for the defining matrix in these controls.

These finite controls complement the written universal matrix argument;
they do not prove a universal identity by sampling or constitute an
independent review. Python exact arithmetic and the implementation remain
part of the computational trust boundary. The manifest is mandatory in
verification mode and compared in full, under normal and optimized Python.
The explicit author manifest-generation option is not verification.

The five-level maximum remains credited. The six-to-eight-level maximum
and unrestricted complex first-power inequality remain open in this work.
Two bounded global cover proposals during development stopped incomplete;
they establish neither a complete cover nor mathematical exclusion.
The present result offers a larger local terminal region for a future
complete structural argument, while requiring the fixed unit triple.
