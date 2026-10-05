# Odd-prime equality with a minimal normal kernel

Rowan / studio-researcher-4, researcher. Author draft, 2026-10-05;
independent internal check pending. A separate consequence of the fixed
core equality formula; no change to the shared eta<=6 target.

**Proposition.** Suppose V=F_p^d is a nontrivial minimal normal subgroup
of a finite group G, Q=G/V, and p is odd. If equality holds in the
elementary-kernel cyclic-count bound

    c(G)=c(V) A_p(Q)+p^(d-1) B_p(Q),

then V is central and d=1. No hypothesis on Q, faithful action,
global splitting or nonsolvability is required.

**Proof.** The core equality conditions say every element of Q whose
order is prime to p acts trivially on V. Let rho:Q->GL(V) be the quotient
action; it is well-defined because V is abelian. For any q in Q, write
q=q_p q_(p'), using the commuting p-part and p-coprime part in its cyclic
subgroup. The latter is killed by rho, so rho(q)=rho(q_p) has p-power
order. Every element of the finite image A=rho(Q) therefore has p-power
order. Cauchy's theorem shows |A| is a power of p.

Let A act on the underlying finite set V. All nontrivial orbit sizes
are divisible by p. Since |V|=p^d, the number of fixed vectors is
divisible by p. Zero is fixed, so there are at least p fixed vectors,
including a nonzero vector. Thus

    C_V(G)=V intersection Z(G)

is a nontrivial G-normal subgroup of V. Minimal normality gives
C_V(G)=V, so V is central. Every order-p subgroup of a central
elementary abelian group is G-normal; minimality therefore forces d=1.
This proves the proposition.

Only elementary orbit-stabilizer and Cauchy facts enter beyond the core
counting/equality lemma. In particular no irreducible-module theorem,
CFSG, Schur multiplier or classification of the quotient is imported.

## Why both extra hypotheses matter

Minimal normality cannot simply be omitted. The odd-prime modular family
in `SUPPLEMENT.md` has a noncentral elementary abelian kernel of dimension2,
equality in the same bound, and a nonsplit extension. Its fixed central
line is a proper nontrivial normal subgroup of the kernel.

The odd-prime restriction cannot be omitted. In A4 the normal V4 is
minimal normal: a 3-cycle permutes its three nonzero vectors transitively,
so no order-two subgroup is normal. Nevertheless the action is nontrivial
and c(A4)=8=c(V4)c(C3), attaining the characteristic-two bound. This is
the existing core fixture and an acknowledged classical exception.

The proposition may simplify equality analysis for a minimal normal
kernel in an induction. It does not by itself exclude any base groups,
identify a central extension, or complete the campaign classification.
Its historical novelty is deliberately unclaimed.
