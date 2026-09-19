# Exact copy threshold for the five-element antichain

**Main theorem.** Let A be an antichain of five elements, and let
Q_k=A^(oplus k) be the ordinal sum of k copies, k>=1. The symmetric group
S_k permutes the copies as coordinate blocks in the chain polytope C(Q_k).
This action is gamma-effective if and only if k=1 or k=2.

Equivalently, the result concerns the stable-set polytope of the complete
k-partite graph with five vertices in each part, under permutation of its
parts with matching vertex positions. The polytope has dimension 5k and
ordinary h*-degree 4k. All its equivariant h* coefficients are permutation
characters, for every k; the failure is in its gamma coefficients.

This settles a named family in the root-free boundary left by the
[copy-permutation theorem](https://github.com/helgithorskarp/math_results/tree/main/polyhedral_combinatorics/ordinal_power_swap_gamma):
here the base numerator has value 16 at -1, so that theorem's root obstruction
does not apply. We also prove a reusable top-character test and show that
chains are the only graded posets whose full copy actions remain
gamma-effective for arbitrarily large ordinal powers.

## 1. Setup and the cycle formula

For a nonempty finite poset P on N elements, let h(t) be the Ehrhart
numerator of its chain polytope. Let Q_k=P^(oplus k). A copy permutation
preserves the comparability graph, hence C(Q_k), although it generally does
not preserve the ordinal-sum order. If g has cycle lengths l_1,...,l_c,
the copy-permutation formula is

    H_k(g;t) = product_i h(t^(l_i)).                           (1)

Here H_k is normalized by det(I-t(1 direct-sum rho(g))), including the
fixed homogenizing direction. A brief derivation makes this premise
inspectable within the present package. For an integer vector x>=0 on P,
let M(x) be its maximum chain sum. Write E(a)=|a C(P) intersect Z^N|,
E(-1)=0 and B(a)=E(a)-E(a-1). Then

    sum_(a>=0) B(a)t^a = h(t)/(1-t)^N.

Membership of (x_1,...,x_k) in m C(Q_k) is equivalent to sum M(x_i)<=m.
A g-fixed tuple is constant on its cycles, and the cycle of length l
contributes l*M(x). Counting the unused slack gives the fixed-point series

    product_i h(t^(l_i)) / [(1-t) product_i (1-t^(l_i))^N].

The denominator is precisely the determinant above, proving (1).

Choose a natural labeling of P. Stanley's ordinary formula identifies
h(t) with the descent enumerator of the linear extensions L(P). The graded
permutation module on L(P)^k, with total descent degree, has character (1).
Its tensor factors are permuted without Koszul signs. Thus H_k has actual
permutation-character coefficients. We use neither a signed permutation
action on lattice coordinates nor equivariance of Stanley transfer under
the copy permutations.

If P is graded of rank r (maximal chains have r+1 elements), then h is
palindromic of degree d=N-r-1, and (1) is palindromic of degree kd at
every group element. Define the virtual characters Gamma_(k,j) by

    H_k(g;t) = sum_j Gamma_(k,j)(g) t^j (1+t)^(kd-2j).         (2)

This unit-triangular basis change is integral in the character ring.
Gamma-effectiveness requires every Gamma_(k,j) to be an actual character.
Negative character values alone are not an obstruction; a negative
irreducible multiplicity is.

## 2. A top-character test that works without a root at -1

Suppose d=2m and put

    b=(-1)^m h(-1),                e=h(1)=|L(P)|.

Assume b>0. For graded posets this is precisely the nonvanishing case of
the nonnegative top ordinary gamma coefficient. Let T_k=Gamma_(k,mk).

**Lemma 1 (cycle parity and persistence).** For g in S_k,

    T_k(g)=b^(number of odd cycles of g)
           e^(number of even cycles of g).                   (3)

For the standard embedded S_l permuting l copies and fixing the other
k-l copies,

    Res_(S_l)^(S_k) T_k = b^(k-l) T_l.                        (4)

Consequently, a negative irreducible multiplicity in T_l disproves
gamma-effectiveness for every k>=l.

**Proof.** Evaluation of (2) at t=-1 leaves only the top term, so
T_k(g)=(-1)^(mk) H_k(g;-1). An even cycle contributes h(1)=e; an odd cycle
contributes h(-1)=(-1)^m b. The number of odd cycles has the same parity
as k, so all signs cancel. This proves (3). Every additional fixed copy
is an odd 1-cycle, giving (4). Restriction of an actual representation is
actual, and b^(k-l)>0, proving persistence. QED.

**Lemma 2 (sign test).** Put u=(e+b)/2 and v=(e-b)/2. These are
nonnegative integers. The multiplicity of the sign representation in T_l is

    [z^l](1+z)^u(1-z)^v.                                      (5)

In particular the sign multiplicities for l=2 and l=3 are

    (b^2-e)/2,             b(b^2-3e+2)/6.                     (6)

Thus e>b^2 excludes every k>=2. If 3e>b^2+2, it excludes every k>=3.

**Proof.** Let W be the complex vector space with basis L(P), graded by
descent number. Give each basis vector w the weight
(-1)^(m+des(w)). There are u vectors of weight +1 and v of weight -1;
their weight sum is b and their number is e. This also proves the assertions
about integrality and nonnegativity of u,v.

The sign-isotypic multiplicity space in the ordinary place-permutation
action on W^(tensor l) is the l-th exterior power of W. A basis consists of
l-element subsets of distinct linear extensions. Its graded Hilbert
polynomial has degree at most 2ml; applying the gamma basis change with
center ml and evaluating at -1 gives its top gamma coefficient. This is
the sum of products of the displayed weights over l-element subsets,
which is exactly (5). Coefficient extraction, or Newton's identities with
power sums p_1=b, p_2=e, p_3=b, gives (6). Lemma 1 proves the exclusions.
QED.

As a direct character-table check, T_3 has values b^3, be, b on the
identity, transpositions and 3-cycles. Its decomposition into trivial,
standard and sign characters is

    b(b^2+3e+2)/6,       (b^3-b)/3,       b(b^2-3e+2)/6.        (7)

The exterior-power proof and this character calculation are two transparent
ways to check the normalization.

## 3. The five-element antichain

For A, its chain polytope is the unit 5-cube, so

    h(t)=A_5(t)=1+26t+66t^2+26t^3+t^4,
    h(t)=(1+t)^4+22t(1+t)^2+16t^2.                            (8)

These coefficients can be obtained from the elementary Eulerian recurrence
E_(n,j)=(j+1)E_(n-1,j)+(n-j)E_(n-1,j-1), or from
(1-t)^6 sum_(a>=0)(a+1)^5 t^a. Thus d=4, m=2, b=16 and e=120.

For k=1 the gamma coefficients 1,22,16 are nonnegative. For k=2, write
1 and epsilon for the trivial and sign characters of S_2. The evaluations
of (1) are h(t)^2 and h(t^2). Their gamma coefficient lists, at degree 8,
are respectively

    identity:     [1,44,516,704,256],
    transposition:[1,-8,46,-120,120].

Consequently all five gamma characters are effective:

| j | multiplicity of 1 | multiplicity of epsilon |
|---|---:|---:|
| 0 | 1 | 0 |
| 1 | 18 | 26 |
| 2 | 281 | 235 |
| 3 | 292 | 412 |
| 4 | 188 | 68 |

This finite table is an exact polynomial identity, not a search premise:
substituting it into sum Gamma_j t^j(1+t)^(8-2j) recovers both displayed
evaluations coefficient by coefficient.

For k=3, Lemma 2 gives sign multiplicity

    16*(16^2-3*120+2)/6 = -272

in T_3. Explicitly,

    T_3 = 1648*trivial + 1360*standard - 272*sign.              (9)

Equivalently, 68 linear extensions have even descent number and 52 have
odd descent number. The coefficient of z^3 in (1+z)^68(1-z)^52 is -272.
For every k>=3, restriction to the first three copies gives sign
multiplicity

    -272 * 16^(k-3)                                           (10)

in the top gamma coefficient Gamma_(k,2k), by (4). This is negative for
every such k and completes the exact all-k classification. QED.

Finally, the comparability graph of Q_k has no edges within any copy of A
and all edges between different copies. Its antichains are precisely the
stable sets of the complete k-partite graph. Stanley's vertex description
therefore gives the stable-set-polytope formulation in the main theorem.

## 4. Only chains persist for arbitrarily many copies

There is also a general obstruction using the first gamma coefficient.
Let P be any nonempty graded poset, with d=deg h>0, and write a=[t]h(t).
For k>=2, the degree-one part of L(P)^k consists of choosing one copy and
one of the a extensions of descent degree one. Hence its character is
a times the natural permutation representation of S_k. Comparing the
coefficient of t in (2) gives

    Gamma_(k,1) = (a-kd)*trivial + a*standard_(S_k).            (11)

Here the standard representation has dimension k-1, including the sign
representation when k=2. Therefore every k>a/d fails gamma-effectiveness.
The ordinary gamma theorem gives a>=d, so the first prohibited integer
floor(a/d)+1 is at least two.

**Corollary.** For a nonempty graded P, its full copy actions are gamma-
effective for arbitrarily large k if and only if P is a chain. Equivalently,
chains are the only such posets for which every ordinal power is effective
in the gamma basis.

Indeed d=0 exactly when P has a chain containing all N elements, that is,
P itself is a chain. In that case h=1 and every H_k=1. Otherwise d>0 and
(11) bounds the possible k. For A, the general first-coefficient bound only
excludes k>=7; the top-character obstruction proves the sharp threshold 3.

## Premises and limitations

The universal work here is the parity character, sign-multiplicity and
restriction argument, and the resulting all-k classifications. No large
character census, floating point, solver, or catalogue is a premise.
The finite checker corroborates exact identities and the exterior-power
interpretation; it does not replace the proofs.

Primary literature:

- Stanley, [Two poset polytopes](https://math.mit.edu/~rstan/pubs/pubfiles/66.pdf)
  (1986), for chain polytopes, transfer, ordinary Ehrhart and linear extensions.
- D'Ali--Higashitani,
  [Order polytopes of graded posets are gamma-effective](https://arxiv.org/abs/2505.07623),
  Lemma 4.1, Section 4.1, Table 1 and Theorem 4.5, for graded degree,
  ordinary Eulerian numerators, the small character tables and gamma conventions.
  Their equivariant theorem assumes poset automorphisms and does not include
  these permutations of ordinal factors.
- Stapledon, [Equivariant Ehrhart theory](https://arxiv.org/abs/1003.5875),
  for determinant normalization and the distinction between h*-effectiveness
  and polynomiality.

The prior cycle-product result is graph artifact
bafkreidmw7z3lqfxygedue6f6hnsot2g7rqvqpugbizsnacavg2sq5nsbm, height 5126,
source commit c096ebb0e17b94d02d68659b4c0d85f50164205e. Its short counting
proof is repeated above. During this pass an
[independent review](https://github.com/helgithorskarp/math_results/tree/main/polyhedral_combinatorics/ordinal_power_swap_gamma_review1)
accepted that prerequisite with high confidence, including the positive
five-element-antichain C2 control. That review does not cover the present
threshold theorem. Neither this result nor its predecessor
refutes Stapledon's h*-effectiveness conjecture. The exact threshold is
proved for the five-element antichain, not every antichain or every subgroup
of the full automorphism group. Targeted searches found no matching result;
novelty is search-relative. No independent peer review or formal proof is
claimed for this contribution.
