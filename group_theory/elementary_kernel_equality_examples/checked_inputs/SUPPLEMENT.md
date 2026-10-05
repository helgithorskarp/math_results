# A noncentral nonsplit equality family

Rowan / studio-researcher-4, researcher. Author draft, 2026-10-05;
independent internal check pending. This supplements the frozen core proof
without altering its mathematical version or22-fixture reference run.
No historical novelty is claimed for the classical modular p-group.

For an odd prime p define

    M_p = C_(p^2) semidirect C_p,

where a generator of C_p acts on C_(p^2) by multiplication by1+p.
Its normal form consists of pairs (a,b) in Z/(p^2) x Z/p, with

    (a,b)(c,d)=(a+(1+p)^b c mod p^2, b+d mod p).

The multiplier has order p modulo p^2, so this is a valid semidirect
product of order p^3. Project (a,b) to a mod p. Its kernel is

    V={(p u,v):u,v in F_p}=F_p^2.

The kernel is abelian because (1+p)^v p u=p u modulo p^2. It is
noncentral: conjugation by x=(1,0) sends (p u,v) to (p(u-v),v).

The quotient M_p/V is C_p. For all pairs (a,b), binomial expansion gives

    (a,b)^p = (a sum_(j=0..p-1)(1+p)^(jb),0)
              = (p a,0) modulo p^2,

since (1+p)^(jb)=1+jb p modulo p^2, and
b p^2(p-1)/2 is divisible by p^2 for odd p. Hence all lifts of a
nonidentity quotient element have order p^2. There is no order-p lift
of a quotient generator, so the extension by this V does not split.
This is compatible with the displayed semidirect product: its displayed
normal cyclic factor C_(p^2) is a different kernel.

There are p^2-1 elements of order p and p^3-p^2 elements of order p^2.
Thus

    c(M_p)=1+(p^2-1)/(p-1)+(p^3-p^2)/(p(p-1))=2p+2.

For Q=C_p the core formula has A_p(Q)=B_p(Q)=1,
c(V)=p+2 and p^(d-1)=p. The lower bound is exactly2p+2.
Every p-divisible coset has s_h=0; the only p-coprime quotient element
is the identity. Equality therefore holds although V is noncentral.
This shows why equality in the arbitrary-extension bound cannot imply
centrality without the additional quotient-family/rank-one assumptions.

The affine norm explanation is explicit. The action matrix of x is
T=[[1,-1],[0,1]], T^p=I; the norm I+T+...+T^(p-1) is zero over F_p.
The lift power x^p=(p,0) is the nonzero vector(1,0), so the norm equation
has no solution. This combines a nontrivial action with a genuine
cyclic-extension obstruction.

At p=2 the same group is D8 and the same order formula fails: for odd
a, (a,1) has order2, whereas (a,0) has order4. The coset over the
quotient generator has two short lifts and two long lifts. Thus c=7,
the bound is6, and the p-divisible defect is1. Here the kernel-V4
extension DOES split. The affine norm is nonzero and cancels the lift
power for the short lifts. This validates the odd-prime restriction.

`verify_modular_family.py` constructs the normal forms, walks literal
powers and cyclic-subgroup sets, counts every quotient coset and checks
the centrality/splitting distinctions for p=2,3,5. Its small output is
corroboration of this uniform elementary calculation, not an all-groups
census. These p-groups are solvable; none is a counterexample to the
shared nonsolvable eta<=6 classification.
