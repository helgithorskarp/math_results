# The nonsolvable cyclic-count gap at six

Author: Atlas, studio-researcher-1, researcher in the 2026-10-05 Colloquium.
Version 2: assembly from the exact internally checked component proofs.
The original conditional draft is preserved unchanged in
[checks/atlas_induction_input_v1.md](checks/atlas_induction_input_v1.md).
The induction and Hall argument were independently checked by Nova and Iris,
respectively; the three inputs now have their own completed internal checks.
Separate check records identify the exact final assembly they cover.
These are internal checks, not external peer review or formal verification.

All groups are finite. Let c(X) count all cyclic subgroups, including the
trivial subgroup, let omega(X)=omega(|X|), and put eta(X)=c(X)/2^omega(X).
Write tau(n) for the number of positive divisors and
delta(n)=tau(n)/2^omega(n). Empty products equal one.

## 1. Theorem and proved input lemmas

**Theorem.**

Every nonsolvable G with eta(G)<=6 is A5 x C_m, with gcd(m,30)=1 and either
m squarefree (including m=1), or exactly one prime exponent equal to 2 and
all the others equal to 1. Conversely these have eta=4 and eta=6, respectively.

The induction uses these three lemmas, whose complete proofs and exact
internally checked versions are identified after their statements:

**B6 (radical-free base, Nova's lane).** If Rad(X)=1 and eta(X)<=6 for a
nonsolvable X, then X is isomorphic to A5.

Nova's [complete proof](../nonsolvable_cyclic_count_base/PROOF.md), version 2,
has SHA256 15297f64ee862035c7438dbe244c5d5403107c06f3cb69c8e24df9c2c6b36ab0.
Atlas's [internal check](checks/atlas_base_v1.md) covers its measure/order
bound, finite-family completeness reduction, outer primes, simple margins,
socle transfer and almost-simple overgroups. CFSG and the standard simple
order, small-isomorphism and automorphism data are explicit classical
imports. The independent finite count evidence is documented in
[BASE_CHECK.md](BASE_CHECK.md); sampled counts alone do not establish B6.

**E (arbitrary elementary-kernel bound and equality, Rowan's lane).** For a
nontrivial elementary abelian normal subgroup V=F_p^d of X, put Q=X/V and

    A_p(Q) = sum_{h in Q, p does not divide o(h)} 1/phi(o(h)),
    B_p(Q) = sum_{h in Q, p divides o(h)} 1/phi(o(h)).

Then

    c(X) >= c(V) A_p(Q) + p^(d-1) B_p(Q),
    c(V) = 1 + (p^d-1)/(p-1).

For odd p, equality implies that every p-coprime-order element of Q acts
trivially on V. For the rank-one specialization with
Q=A5 x C_(p r), p>5, and r squarefree and coprime to 30p, equality therefore
implies V is central in X. The action factors through Q because V is abelian.
This lemma does not assume that X/V splits. Rowan's
[exact coset/norm proof](../elementary_kernel_cyclic_count/PROOF.md) has SHA256
813c8449357199d7db6ff9ac3f13725b6239dbb44f2bb721a78f748a90adc7de.
Nova's [internal check](checks/nova_elementary_kernel_v1.md) accepts the
universal formula, inequality, equality conditions and the stated
persistent-prime specialization, with separately reproduced finite fixtures.

**C (central boundary, Iris's lane).** Let V=C_p be central in X, p>5, with
X/V=A5 x C_(p r), r squarefree and coprime to 30p. If eta(X)<=6, then
X=A5 x C_(p^2 r). In particular eta(X)=6. This requires identification of
the central extension, not just triviality of its action. Iris's
[broader central-extension proof](../central_prime_cyclic_count_boundary/PROOF.md)
has SHA256 ea938c7b0313e008db5e7632a144d06c4a8038576f24714a99fdec294a59a769.
It implies precisely C, as recorded in Rowan's
[internal check](../central_prime_cyclic_count_boundary/internal_checks/rowan_v1/REVIEW.md).

Each lemma's hypotheses are established in the induction before it is used.
Standard elementary finite-group structure, including minimal normal
subgroups of solvable normal groups, is also used below.

## 2. Counting and one-step quotient monotonicity

Generators of cyclic subgroups partition X, so

    c(X) = sum_{x in X} 1/phi(o(x)).                         (1)

If gcd(|X|,|Y|)=1, the element order in X x Y is o(x)o(y) and totients
multiply, so c(X x Y)=c(X)c(Y). In particular c(C_m)=tau(m).

If V is normal in X, the map from cyclic subgroups of X to those of X/V
is surjective: lift a generator of each cyclic subgroup. Thus c(X)>=c(X/V).
If V=F_p^d and p divides |X/V|, the prime supports coincide, hence

    eta(X) >= eta(X/V).                                    (2)

If p does not divide |X/V|, V is a normal Hall subgroup. Such an extension
splits; a proof for the abelian-kernel case is included here to state the
trust boundary. Let H=X/V act on V, and choose a section with additive
cocycle a(g,h). Associativity says

    a(g,h) + a(gh,k) = g a(h,k) + a(g,hk).

Since |H| is invertible in F_p, set
B(g)=|H|^(-1) sum_{k in H} a(g,k). Summing this identity over k gives

    a(g,h)=B(g)+g B(h)-B(gh).

Changing the section by -B(g) makes the cocycle zero. Thus X=V semidirect H.

For h in H of order e, let f(h)=dim C_V(h). The averaging projection
P=e^(-1)sum_{j=0}^{e-1}h^j has image C_V(h). Exactly p^(d-f(h)) elements
of the coset Vh have order e, and all the others have order pe, because
(v,h)^e=eP(v). Substituting in (1) yields the exact formula

    c(X) = c(V)c(H)
         + (p-2)/(p-1) sum_{h in H}
             (p^(d-f(h))-1)/phi(o(h)).                     (3)

The defect is nonnegative, including p=2. Hence c(X)>=c(V)c(H)>=2c(H).
Here omega(X)=omega(H)+1, which proves (2) in this case as well. Notice
that this monotonicity does not presume the classification or the base B6.

## 3. Proposition H: the new-prime Hall branch

Let V=F_p^d be normal in X, and suppose

    Q=X/V=A5 x C_m, gcd(m,30)=1, p does not divide 60m.

No restriction on the exponents in m is needed for this proposition.
Then p>=7 and:

1. If d>=2, eta(X)>=2(p+2)>=18.
2. If d=1, a nontrivial action of Q on V implies
   eta(X)>=eta(Q)+p-2>=9.
3. If d=1 and the action is trivial, X=Q x C_p.

**Proof.** The preceding splitting gives X=V semidirect Q. Also

    c(Q)=32 tau(m), omega(Q)=3+omega(m), eta(Q)=4 delta(m)>=4.

For d>=2, c(V)>=p+2; (3) gives
eta(X)>=c(V)eta(Q)/2>=2(p+2).

For d=1, the action is a homomorphism Q -> Aut(C_p)=F_p^*, an abelian
group. Since A5 is perfect, its action is trivial. The kernel is therefore
K=A5 x C_ell for a divisor ell of m. If the action is nontrivial, ell<m.
Here f(h)=1 on K and f(h)=0 outside K. Formula (3) becomes

    c(X)=2c(Q)+(p-2)(c(Q)-c(K))
        =64 tau(m)+32(p-2)(tau(m)-tau(ell)).                (4)

Let k=omega(m). Nontrivial action implies k>=1. Write
m=product_{i=1}^k q_i^{a_i} and ell=product q_i^{b_i}, with 0<=b_i<=a_i.
Choose j with b_j<a_j. Then

    tau(ell) <= a_j product_{i!=j}(a_i+1),
    tau(m)-tau(ell) >= product_{i!=j}(a_i+1) >= 2^(k-1).

Dividing (4) by 2^(4+k) gives the exact action defect

    eta(X)=eta(Q)+2(p-2)(tau(m)-tau(ell))/2^k
           >=eta(Q)+p-2>=9.                               (5)

If the action is trivial, the split extension is the direct product.
This includes m=1, when the action is necessarily trivial. QED.

Formula (4) is also obtained by writing X=A5 x (C_p semidirect C_m) and
using the known cyclic-extension formulas. No priority is asserted for
this counting formula or its elementary derivation.

## 4. Induction proving the theorem

Using the three proved lemmas, we argue by induction on |G|.

If Rad(G)=1, B6 gives G=A5, which is the m=1 case.

Otherwise choose a minimal nontrivial G-normal subgroup V inside Rad(G).
Then V=F_p^d with d>=1. Its quotient Q=G/V is nonsolvable: if Q were
solvable, the extension by the abelian V would make G solvable. By (2),
eta(Q)<=eta(G)<=6. Since |Q|<|G|, induction gives

    Q=A5 x C_m,
    gcd(m,30)=1,
    m squarefree or with exactly one squared prime.

If p does not divide |Q|, Proposition H forces d=1 and trivial action,
since all its other branches give eta(G)>6. Thus G=Q x C_p. Adjoining
this new prime to m preserves its allowed exponent profile and gcd(m,30)=1.

Suppose now p divides |Q|. For p=2,3,5, the element-order histogram of A5
is 1,15,20,24 at orders 1,2,3,5. It gives

    p       A_p(A5)   B_p(A5)   2A_p(A5)+B_p(A5)
    2          17       15                  49
    3          22       10                  54
    5          26        6                  58.

The coprime cyclic factor C_m multiplies A_p and B_p by tau(m).
Input E, c(V)>=2 and p^(d-1)>=1 therefore give, respectively,

    eta(G)>= (49/8)delta(m), (54/8)delta(m), (58/8)delta(m).

Each exceeds 6 because delta(m)>=1. These cases are impossible.

For p>5, write m=p^a r with gcd(r,30p)=1. By the allowed quotient
profile, a is 1 or 2. Set D=32tau(r). The p-coprime elements of the
cyclic p^a factor have total reciprocal-totient weight 1, and those of
p-divisible order have total weight a. Thus A_p(Q)=D and B_p(Q)=aD.
Input E gives

    eta(G)>=2delta(r)(c(V)+a p^(d-1)).                     (6)

If d>=2, c(V)>=p+2, so (6) is already greater than 6. For d=1 its
right side is 2delta(r)(a+2). If a=2 it is at least 8. If a=1 but r
has the quotient's squared prime, it is at least 9. Consequently the
only remaining case is

    d=1, a=1, r squarefree, eta(G)=6,

with equality in E. Its equality interface makes V central. To spell
out the last implication: all p-coprime elements of Q act trivially;
these include A5 and C_r. The remaining C_p also acts trivially on V
because Aut(C_p) has order p-1. These factors generate Q, so the
whole action is trivial. Input C now gives G=A5 x C_(p^2 r), the second
allowed family. This completes the necessity proof.

Conversely, for the stated products the factor orders are coprime, so

    eta(A5 x C_m)=4 tau(m)/2^omega(m)
                 =4 product_{q^a || m}(a+1)/2.

This is 4 for a squarefree m, including m=1, and 6 for exactly one
squared prime and all others to the first power. These groups are
nonsolvable because they have a quotient A5. QED.

## 5. Scope, internal checks and provenance

The original conditional induction had SHA256
208096e0a2ba2021dbb713d7ef0741bd4d9b74e6c61bfeb17623d0fd4cd91ee4.
Nova's [induction check](checks/nova_induction_v1.md) independently verifies
sections 1, 2 and 4 of that input and the containment of E and C in their
component proofs. Iris's [Hall check](checks/iris_hall_v1.md) independently
verifies Proposition H and its splitting/counting prerequisites. Those
reports are preserved byte-for-byte and retain their original scopes.
The component exact-version checks above close the inputs left conditional
in that original draft. This version changes status, source links and
provenance; the counting equations and induction cases are unchanged.
The final assembly receives a separate exact-version interface check;
its acceptance and limitations are recorded in README.md.

The quotient monotonicity and formula (3) are also prior repository
results. The eta=4 necessity classification and the product examples are
prior art. The proposed new content is the universal necessity at eta<=6,
including absence of nonsolvable values in (4,6) and identification of the
eta=6 boundary. No vote establishes mathematical correctness or novelty.
The bounded literature screen is not an exhaustive priority certificate.
Current source comparisons and graph provenance are recorded in SOURCES.md.
