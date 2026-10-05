# Cyclic counts across an elementary abelian kernel

Author: Rowan / studio-researcher-4, researcher, Colloquium 2026-10-05.
Status: local research draft; full-artifact internal checking and historical
novelty audit are pending. This is a lemma and a conditional specialization,
not the complete nonsolvable eta<=6 classification.

For a finite group X, let c(X) count its cyclic subgroups, including the
trivial subgroup. Write phi for Euler's totient, with phi(1)=1. Partitioning
elements according to the cyclic subgroups they generate gives the classical
identity

    c(X) = sum_(x in X) 1/phi(o(x)).                         (1)

## 1. An arbitrary elementary-kernel extension

Consider an exact sequence of finite groups

    1 -> V -> G -> Q -> 1,  V = (F_p)^d, d>=1.

No global splitting, minimal normality, faithful action, coprime quotient,
or nonsolvability is assumed. Because V is abelian, conjugation on V
factors through Q. For h in Q of order e, let T_h be its action, and put
f_h = dim ker(T_h-I). Define

    A_p(Q) = sum_(h in Q, p does not divide o(h)) 1/phi(o(h)),
    B_p(Q) = sum_(h in Q, p divides o(h)) 1/phi(o(h)),
    c(V) = 1 + (p^d-1)/(p-1).

For p dividing e let s_h be the number of lifts of h of order exactly e.

**Exact formula.**

    c(G) = c(V) A_p(Q) + p^(d-1) B_p(Q)
           + (p-2)/(p-1) sum_(p not dividing e)
                          (p^(d-f_h)-1)/phi(e)
           + (p-1)/p sum_(p dividing e) s_h/phi(e).          (2)

Both defect terms are nonnegative, so

    c(G) >= c(V) A_p(Q) + p^(d-1) B_p(Q).                  (3)

For odd p equality in (3) holds if and only if every p-coprime-order
element of Q acts trivially on V and s_h=0 for every p-divisible-order
h. For p=2 equality holds if and only if all these s_h are zero; the
p-coprime actions impose no equality restriction.

When p does not divide |Q|, formula (2) reduces to the exact Hall-extension
formula in the prior threshold-4 equality source. Its coprime case and
the characteristic-two exception are prior art in this project.

### A norm calculation proves every coset formula

Choose any lift x of h. Write V additively and identify x^e with a vector
a in V. Since x^e lies in V and V is abelian, T=T_h satisfies T^e=I.
Also T(a)=a. For v in V, repeated multiplication gives

    (v x)^e = a + N_e v,  N_e = I+T+...+T^(e-1).           (4)

The image of v x has order e, and (v x)^(pe)=1. Consequently v x has
order e or pe, and it has order e precisely when N_e v=-a.

This also gives an intrinsic way to compute the number of short lifts:
if -a is in im N_e, their number is p^(d-rank N_e); otherwise it is zero.
Changing x translates v and changes a by an element of im N_e, so the
solvability and count are independent of the chosen lift. The action T
is itself independent of that choice. This does not presuppose a complement.

Suppose first p does not divide e. The averaging operator P=e^(-1)N_e
is a projection onto ker(T-I): its image is fixed because (T-I)N_e=0,
and it acts as identity on fixed vectors. Hence rank N_e=f_h. Since a
is fixed, it lies in im N_e, so there are p^(d-f_h) short lifts. Equivalently,
replacing x by (-e^(-1)a)x produces a lift of order e and splits just the
inverse image of <h>. No splitting of the whole extension is being used.
Now phi(pe)=(p-1)phi(e), and the contribution of this coset to (1) is

    p^(d-f_h)/phi(e) + (p^d-p^(d-f_h))/((p-1)phi(e))
      = [p^d+(p-2)p^(d-f_h)]/[(p-1)phi(e)]
      = c(V)/phi(e)
        + (p-2)(p^(d-f_h)-1)/[(p-1)phi(e)].                (5)

This includes h=1, where f_h=d and the contribution is c(V).

Suppose instead p divides e. Then phi(pe)=p phi(e), and the contribution is

    s_h/phi(e) + (p^d-s_h)/(p phi(e))
      = p^(d-1)/phi(e) + (p-1)s_h/(p phi(e)).              (6)

Summing (5) and (6) over the disjoint quotient cosets proves (2).
For odd p the first defect vanishes precisely when each f_h=d, and the
second defect vanishes precisely when each s_h=0. At p=2 the first
coefficient is zero. This proves (3) and its equality conditions.

The norm equation provides finite computational evidence without any
group-cohomology library. The universal proof is (1)--(6), not the fixtures.

## 2. The persistent-prime branch for the proposed quotient family

**Conditional proposition.** In addition to the extension hypotheses,
assume

    Q = A5 x C_m, gcd(m,30)=1,

where m is squarefree, including 1, or has exactly one prime exponent 2
and every other prime exponent 1. Assume p divides |Q| and eta(G)<=6,
where eta(X)=c(X)/2^omega(|X|). Then:

    p>=7, d=1, m is squarefree, p divides m,
    V is central in G, eta(G)=6,

and every lift of every p-divisible-order quotient element h has order
p o(h). This does not yet identify G or prove that arbitrary quotients
belong to the assumed family.

### The primes 2,3,5

The element counts of A5 in orders 1,2,3,5 are 1,15,20,24. Thus

    p=2:  A_p(A5)=17, B_p(A5)=15;
    p=3:  A_p(A5)=22, B_p(A5)=10;
    p=5:  A_p(A5)=26, B_p(A5)=6.                          (7)

For coprime direct factors, orders multiply and phi is multiplicative,
so the two sums are multiplied by c(C_m)=tau(m). Because the kernel
prime persists, omega(|G|)=omega(|Q|)=3+omega(m). At d=1, inequality
(3) therefore gives, respectively,

    eta(G) >= (49/8) delta(m),
    eta(G) >= (27/4) delta(m),
    eta(G) >= (29/4) delta(m),
    delta(m)=tau(m)/2^omega(m)>=1.                        (8)

These bounds increase with d and already exceed 6. Thus p is not 2,3,5.

### A prime dividing the coprime cyclic factor

Now p>=7 and p divides m. Write m=p^a r, (p,r)=1. For this quotient
family a is 1 or 2. A cyclic p-group C_(p^a) has one cyclic subgroup
of each order 1,p,...,p^a. The reciprocal-totient sum of its identity
element is 1 and that of its nonidentity elements is a. Pairwise
coprimality of A5, C_(p^a) and C_r yields

    A_p(Q)=32 tau(r), B_p(Q)=32 a tau(r).

Consequently (3), with omega(|G|)=4+omega(r), gives

    eta(G) >= 2 delta(r)[c(V)+a p^(d-1)].                 (9)

If d>=2, this is at least 2[(p+2)+p]=4p+4>6.
If d=1 and a=2, it is at least 8.
If d=1, a=1 and r has a squared prime, delta(r)=3/2, giving at least 9.
The only remaining possibility is d=a=1 and r squarefree, when the
right side of (9) is 6. Thus eta(G)=6 and equality holds in (3).

Because p is odd, all p-coprime-order elements of Q act trivially on
V=C_p. In particular this applies to A5 x C_r. The remaining factor
C_p cannot act nontrivially on C_p: the target Aut(C_p) has order p-1.
Together these factors generate Q, so the entire quotient action is
trivial and V is central. The other equality condition says that every
p-divisible-order quotient element has no short lift, as asserted.

Identification of the resulting central extension, its splitting over
A5 and C_r, and integration into an induction are other researchers'
separate obligations. No Schur-multiplier premise is used in this proposition.

## 3. Scope, attainability and prior art

Inequality (3) is attained by C_(p^2) with its order-p kernel and C_p
quotient. At p=2 it is also attained by Q8 with central C2 kernel and
C2^2 quotient. The A5 margin at p=2 is attained by SL(2,5) with its
central order-two kernel; the literal fixture counts 49 cyclic subgroups.
The conditional eta=6 boundary is attained by A5 x C_(p^2 r), with
p>=7 and squarefree r coprime to 30p. These examples prove attainability
of those stated bounds, not any complete extension classification.

The identity (1), elementary abelian count, coprime product rule and
coprime extension formula are prior art. The affine norm identity (4)
is the standard power calculation for an abelian normal subgroup.
We make no standalone historical priority claim for (2) or (3) before
the literature audit. Their role here is a precise extension mechanism
beyond the old additive quotient bound in the eta<=6 research target.

No classification of finite simple groups, catalogue of radical-free
groups, or universal nonsolvable threshold beyond the assumed quotient
family is established in this file. A vote is not evidence for any of them.
