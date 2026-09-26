# Independent analytic and exact PSD review of the seven-factor Gaussian sign

26 September 2026. **Verdict: accept the complete theorem at its stated
scope.** I found no mathematical defect in R8's
[seven-factor proof](../gaussian_seven_factor_kernel/PROOF.md), reviewed
at source commit `f5bbd92be43517c18a6958acf900ddd67bac62f8`.

For every bounded probability law mu on R3, contraction T on its support,
variance s>0 and j>=0, the theorem gives `b_(j+7,j)>=0`, strictly unless
all support distances are preserved. Its explicit distance-loss bound
and every polarized weight-coefficient sign are accepted as well.
Together with the separately reviewed q<=6 result, this signs every
beta row through N=7. The first general unsigned entry is `b_(8,0)`.
This is a finite-energy comparison, not full majorisation or a new
Kneser--Poulsen theorem.

I authored the earlier R5 centroid-projection proof and examined the
then-unsigned kernel numerically. I did not develop R8's exact recentering
bridge or its Gram certificates. For this review I read the author's
written proof and scope notes, but did not read, import or execute the
author programs or expected record. The reviewer checker was written from
the mathematical matrix definitions. It derives an independent compact
certificate rather than using the author's eigenvalue lists or elimination
output. This is independent checking of the new argument, not independent
authorship of all upstream premises.

## 1. The finite-base identity really is exact

Let alpha=5/2, p>0, and w_1,...,w_7 be arbitrary real Euclidean vectors.
For x>=0 define

    A=p+sum x_i,  W=sum x_i w_i,  m=W/A,
    E(x)=sum x_i |w_i|^2-|W|^2/A,
    F(x)=A^(-alpha) exp[-E(x)/2].

With H=sum h_i and d_i=w_i-m, direct expansion gives

    E(x+h)-E(x)
      =sum h_i |d_i|^2-|sum h_i d_i|^2/(A+H).             (1)

The contribution of the fixed base p at zero is included in A; it must
not be dropped when recentering. Put u_i=h_i/A and c_i=sqrt(A)d_i.
Equation(1) yields exactly

    F(x+h)/F(x)
      =(1+sum u_i)^(-alpha)
       exp[-sum u_i |c_i|^2/2
                  +|sum u_i c_i|^2/(2(1+sum u_i))].        (2)

In extracting the square-free coefficient of u_1...u_7, the quadratic
exponential chooses a matching M. Its diagonal terms have squared variables
and cannot contribute. The m_M disjoint edges contribute
`product_(ij in M) G_ij/(1+sum u_i)^(m_M)`, with G_ij=c_i.c_j.
The exponential factorial cancels the orders of the selected edges.
On the unmatched labels, the linear exponential contributes a_i=G_ii/2
and the remaining scalar power contributes a rising factorial. The sign
is always (-1)^7 because each edge consumes two labels. Thus the author's
matching formula L_7 satisfies

    (-1)^7 partial_1...partial_7 F(x)=F(x) A^(-7) L_7(G(x)). (3)

Integrating each derivative over [0,1] gives the alternating vertex sum.
All derivatives are analytic on a neighborhood of this compact cube because
A>=p>0. Hence no large-p approximation, exchange of divergent series or
unjustified inverse transform enters the claimed finite-base bridge.

## 2. The homogeneous reduction and reciprocal step

Sorting a matching term by Gram degree k gives

    L_7(G)=sum_(k=0)^7 (alpha)_(7-k) S_k(G),
    S_k=sum_M [product_(ij in M)G_ij/(alpha)_(m_M)]
                         e_(k-m_M)((a_i)_(i unmatched)).   (4)

This follows from `(alpha+m)_(7-k-m)=(alpha)_(7-k)/(alpha)_m`;
the degree conditions on the elementary symmetric polynomial are exactly
what makes the factorial length nonnegative.

S_0=1, and

    S_1=(1-1/alpha)sum_i a_i+|sum_i c_i|^2/(2alpha)>=0.

When all a_i>0, replacing c_i by c_i/a_i sends each diagonal a_i to
1/a_i and each edge G_ij to G_ij/(a_i a_j). Complementing the unused
diagonal labels term by term proves

    S_(7-k)(G)=(product_i a_i) S_k(G').                    (5)

G' remains a Gram matrix. Continuity extends the conclusion to zero
vectors; for example, first replace G by G+epsilon I. There is no rank
restriction in the Gram claim, so this approximation is legitimate.
It is enough to verify S_2,S_3>=0 on all real PSD7x7 matrices.

## 3. The trace identities and correction have the right signs

Use ordered k-tuples of distinct labels and the principal tensor-Gram
matrix H_k with entry `product_r G_(x_r,y_r)`. It is PSD. The aligned
matrix C_k has entry `1/(alpha)_m`, where m is the number of different
coordinates; pairs with a shared label in different coordinates have
entry zero. Counting the orientations and orders of m edges gives

    S_k=trace(C_k H_k)/(2^k k!).                            (6)

The coefficient of a monomial with m edges and k-m diagonal factors is
`1/[2^(k-m)(alpha)_m]`, agreeing with the direct matching definition.
The reviewer code compares every monomial in these identities, not just
values at numerical or rational Gram samples: 231 monomials for k=2 and
665 for k=3.

For B_2=35 C_2, equation(6) gives `S_2=trace(B_2 H_2)/280`.
For B_3=315 C_3+63(P_alt-P_sym), the two six-permutation blocks have
traces det(G_A) and per(G_A), respectively. Therefore

    15120 S_3=trace(B_3 H_3)
                  +63 sum_(|A|=3)[per(G_A)-det(G_A)].      (7)

For a symmetric3x3 matrix the correction equals
`2 sum_i G_ii G_jk^2`, with {i,j,k}=A, so it is nonnegative on a PSD
Gram. Both the direction and the factor63 in (7) are correct. The code
checks this full polynomial identity from the integer matrix and a
separate enumeration of disjoint edges and loops.

## 4. A different exact PSD certificate

The author certifies the 42x42 and210x210 matrices by full annihilating
polynomials with specified roots and, separately, fraction-free elimination.
This review instead reconstructs them from (6)-(7), forms an exact cyclic
subspace, and derives the needed polynomials without input eigenvalues.

Here is why the reduction checks the WHOLE matrix. Each B is symmetric and
commutes with the S7 action relabelling its ordered tuples. The action is
transitive. If a polynomial q(B) kills the first coordinate vector e_0,
it kills every coordinate vector: for a permutation P sending e_0 to e_i,

    q(B)e_i=q(B)P e_0=P q(B)e_0=0.                         (8)

The checker verifies commutation entry by entry for all six adjacent
transpositions, and verifies that their orbit of e_0 contains every index.
These are 10,584 and264,600 exact entry comparisons, respectively. Thus
(8) is a proved completeness argument, not heuristic orbit sampling.

Starting with e_0, exact Gram--Schmidt on B times each new basis vector
produces an orthogonal integer basis of the cyclic subspace. Its dimensions
are5 and10. The zero final residual proves invariance; all orthogonality
and tridiagonal entries are checked. If n_i is the squared norm of its
i-th vector and h_ij is its B-form, the characteristic polynomial is
derived from the recurrence

    q_(i+1)(t)=(t-h_ii/n_i)q_i(t)
                    -h_(i,i-1)^2/(n_i n_(i-1)) q_(i-1)(t). (9)

The resulting monic coefficients are integers. A separate integer Horner
evaluation verifies q(B)e_0=0; (8) then verifies q(B)=0 on the full space.
For q(t)=sum_j c_j t^j of degree d, the checker also verifies

    (-1)^(d+j)c_j>=0 for every j.

It follows for every x>0 that

    (-1)^d q(-x)=sum_j (-1)^(d+j)c_j x^j>=x^d>0.           (10)

No negative real number is a root. Symmetry and q(B)=0 therefore prove
B>=0. This argument needs neither numerical eigenvalues nor the author's
factorizations. The derived coefficients, matrix/basis hashes and all
completeness counts are in [EXPECTED.json](EXPECTED.json).

Two meaningful rejection controls accompany the certificate. A changed
single diagonal entry fails the equivariance test. Removing the three-tuple
correction produces a different cyclic polynomial which fails the PSD
coefficient test. The checker never treats a truncated Krylov calculation
or an unverified polynomial as a certificate; its safety cap fails loudly.

Because the trace of a product of PSD matrices is nonnegative, (6)-(10)
establish S_2,S_3>=0. Equations(4)-(5) give

    L_7(G)>=(5/2)_7=11486475/128>0

for every real PSD7x7 G, including its singular boundary.

## 5. Transfer, constants and equality

The remaining Gaussian factors in (3) are positive. On the cube,
A<=p+7 and `F(x)>=(p+7)^(-5/2) exp[-sum_i |w_i|^2/2]`.
The cube has volume one, giving exactly

    K_p(w)>=(5/2)_7 (p+7)^(-19/2) exp[-sum_i |w_i|^2/2].    (11)

I independently checked the replica normalization: differentiating
`m^(-3/2) E exp[-Q_m(t)/(2s)]` along the standard R6 lift, then using
exchangeability and dividing by m(m-1), gives

    a_(m-2)=(1/(4s)) E[delta_12 integral_0^1
                              m^(-5/2) exp[-Q_m(t)/(2s)]dt].

Coupling the seven remaining replica positions and expanding over their
subsets gives the claimed beta factor `(j+8)binom(j+7,j)/(4s)`.
No extra binomial or factor of two is missing.

If both endpoint supports lie in B_R after separate translations, then
the lifted points also lie in B_R, Q0<=p R^2, and each normalized remaining
vector has norm at most2R/sqrt(s). Substitution into (11) gives the stated
`exp[-(p+28)R^2/(2s)]` lower bound. The rational compact-family corollary
uses `(p+7)^(-19/2)>=(p+7)^(-10)` and e<4 in the correct direction.
The radius2l constant must not be reused for the radius3l rounded family.

All expectations have nonnegative pair loss. If its mean is positive,
(11) gives strictness. If it is zero, continuity and full support of
mu times mu force every support distance to be preserved. An affine
isometry then identifies the endpoint laws, giving zero for every beta.
The finite tuple grouping used for polarized weights has positive
normalization and includes repetitions; hence it inherits the same sign.
Bounded support justifies the finite differentiations and integrations,
and no finite atom assumption was introduced for the main theorem.

## 6. Reproduction and limits

Run the [independent checker](independent_check.py) from this directory:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
```

Normal and optimized CPython3.11.2 produce the same compact record and
`R5_SEVEN_FACTOR_INDEPENDENT_PSD_REVIEW_PASS`. Arbitrary-precision integers,
Fraction arithmetic and the Python interpreter are computational trust
boundaries. Finite algebra verifies the two universal matrix certificates;
it is not a sample extrapolation to all Gram matrices. The written analytic
identities, spectral theorem, Gaussian integration and support argument
remain ordinary unformalized mathematics.

The proof correctly credits the matching formula to R2's earlier derivation,
the [pair-conditioned identity](../gaussian_beta_pair_conditioning/PROOF.md),
and [R5's projection theorem](../gaussian_beta_projection/PROOF.md). The new
finite-base use and PSD argument are R8's contribution. The primary problem
remains [Aishwarya--Li, arXiv2609.07041v2](https://arxiv.org/html/2609.07041v2).
Historical priority, external peer review and formalization are not claimed.

The accepted global coupling criterion still requires ALL beta entries.
This review supplies no sign for b_(8,0), the unrestricted Hankel condition,
the R1 contact flux, or the unsampled compact frontier. It does not iterate
the 7/50 defect bound or change the scopes of the separate all-threshold
flap and rigid-hull theorems.
