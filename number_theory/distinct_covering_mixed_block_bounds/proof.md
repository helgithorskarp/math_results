# Mixed weights for primitive-block covering bounds

Actual author: **six-covering-2, researcher**. This is a self-contained
extension of six-covering-3's
[primitive-block inequality](../distinct_covering_primitive_block_capacity/proof.md)
(source 234569d6f32f1ad96958ed3300050d9ce7acef1e, graph7420). It allows an
arbitrary coprime cofactor and adds an unrestricted weight component.
The new closed formula below evaluates the four-resource budget for \(pq\).
The prime-cube formula is reproduced with attribution below.
No historical priority or new numerical bound for
\(L_{\min}(8)\) is asserted.

## Statement and finite budget

Let \(N=BC\), with integers \(B,C\ge2\) and \(\gcd(B,C)=1\). Write
\(\rho=\operatorname{rad}(B)\), \(T=B/\rho\), and choose \(b\mid T\).
Prescribe congruences with distinct moduli dividing \(N\). Let \(R\) be a
set of distinct unplaced eligible divisors of \(N\), containing
\[
S=\{Bd:d\mid C\}.
\]
A completion uses any subset of \(R\), at most one phase for each modulus,
and covers all residues modulo \(N\) together with the prescribed classes.
Every member of \(S\) must be eligible and unplaced. Eligibility can, for
example, mean modulus at least eight. The lemma does not presume that all
divisors in \(R\) are used, or that the completion's actual LCM equals \(N\).

For any nonnegative weight \(f\) on \(\mathbb Z/N\), set
\[
D_N(f)=\sum_{x\bmod N}f(x),\qquad
C_n(f)=\max_{a\bmod n}\sum_{x\equiv a\pmod n}f(x).
\]
Let \(u,v\ge0\) both vanish on the prescribed congruences. The weight
\(u\) is unrestricted; \(v\) is \(Q=bC\)-periodic. In CRT coordinates
\((t\bmod B,z\bmod C)\), write \(v_z(t)\); it depends only on \(t\bmod b\).

For every \(d\mid C\), choose \(a_d\bmod d\). For a partition \(\pi\) of
the divisors of \(C\), define
\[
k_G(z)=|\{d\in G:z\equiv a_d\pmod d\}|,
\]
\[
F_C(v)=\max_{\pi,(a_d)}\sum_{G\in\pi}\max_{t\bmod b}
 \sum_{\substack{z\bmod C\\k_G(z)\ge2}} k_G(z)v_z(t).       \tag{1}
\]
This is a finite, nonnegative upper budget, including when \(v=0\).
Different groups may choose maximizing labels independently; simultaneous
realization of distinct block labels is not required by this relaxation.

**Mixed-weight lemma.** Every covering completion satisfies
\[
\boxed{D_N(u+v)\le
 \sum_{n\in R\setminus S}C_n(u+v)
 +\sum_{n\in S}C_n(u)+F_C(v).}                          \tag{2}
\]
Taking \(u=0\) gives the arbitrary-cofactor primitive-block inequality.
Taking \(v=0\) gives the ordinary individual-resource capacity inequality.
Taking \(C=p^c,u=0\) recovers the finite partition form in six-covering-3's
cited result. The new mixed form retains full-period weights outside \(S\).

## Proof

We first prove the local sign fact. On \(\mathbb Z/\rho\), let \(h\) be a
sum of functions, each invariant under a shift \(\rho/\ell\) for some
prime \(\ell\mid\rho\). If \(h\ge0\) except possibly at one point, then
\(\sum_jh(j)\ge0\). To see this, let \(\tau_s h(j)=h(j+s)\). The operator
\[
\prod_{\ell\mid\rho}(I-\tau_{\rho/\ell})
\]
annihilates every summand and hence \(h\). Its subset shifts are distinct:
in a difference of two subset sums, reduce modulo a prime \(\ell\) in
their symmetric difference; only the term \(\rho/\ell\) is nonzero.
At a possibly negative point \(j_0\), expansion of the zero identity gives
\[
-h(j_0)=\sum_{\substack{A\ne\varnothing\\|A|\text{ even}}}
h\left(j_0+\sum_{\ell\in A}\rho/\ell\right)
-\sum_{|A|\text{ odd}}
h\left(j_0+\sum_{\ell\in A}\rho/\ell\right).
\]
All displayed other values are nonnegative. Thus the positive-sign
corners compensate any negative value; adding the remaining nonnegative
values proves the claim. A constant function has the required invariance.

Adjoin missing classes of \(S\) with arbitrary phases, preserving coverage
and distinctness. Fix a cofactor coordinate \(z\) and partition the
\(B\)-coordinate into primitive blocks
\[
\{q+Tj\bmod B:j\bmod\rho\},\quad q\bmod T.
\]
The weight \(v_z\) is constant on each block. Any used resource
\(n\in R\setminus S\) factors as \(n=md\), where \(m=\gcd(n,B)<B\)
and \(d\mid C\). Choose \(\ell\mid B\) prime with \(m\mid B/\ell\),
which exists because \(m\) is a proper divisor. When its class is active
at \(z\), its indicator on the block is invariant under
\(j\mapsto j+\rho/\ell\): this changes the \(B\)-coordinate by
\(B/\ell\), a multiple of \(m\). The same holds for its weighted footprint.

An active top class has one \(B\)-coordinate point in one primitive
block. In a block with at most one active top class, let \(h\) be the sum
of the outside-class weighted footprints minus the constant demand
weight \(v_z\). Since the prescribed classes have zero weight, coverage
implies \(h\ge0\) except possibly at the one top-class point. The local
sign fact shows that the outside footprints alone meet this block's
total weighted demand. In a block with \(k\ge2\) active top classes,
the ordinary weighted union bound instead charges their \(k\) footprints,
of total \(kv_z(q)\). Counting coincident top points repeatedly remains
a valid upper bound.

Group top classes with the same actual primitive-block label modulo
\(T\). This gives a partition of \(d\mid C\); their CRT cofactor phases
are the \(a_d\). Summing the block inequalities gives
\[
D_N(v)\le\sum_{n\text{ used outside }S}\Phi_n(v)+F_C(v),   \tag{3}
\]
where \(\Phi_n(f)\) is the footprint of that resource at its **actual**
chosen phase. Maximizing separately over base labels and then partitions
can only enlarge the top charge, giving (1). Importantly, no outside
phase has yet been maximized in (3).

Ordinary weighted counting for \(u\), on the same completion with its
adjoined top classes, gives
\[
D_N(u)\le\sum_{n\text{ used outside }S}\Phi_n(u)
                +\sum_{n\in S}\Phi_n(u).
\]
Add this to (3). For every outside resource, combine its two footprints
at the same phase before maximizing:
\(\Phi_n(u)+\Phi_n(v)=\Phi_n(u+v)\le C_n(u+v)\).
For a top resource, \(\Phi_n(u)\le C_n(u)\). Add the nonnegative capacities
of any unused outside resources in \(R\). This proves (2).

## Two-prime cofactor

Let \(C=pq\), for distinct primes \(p,q\). The four divisors are
\(1,p,q,pq\). Write
\[
U_r(t)=\sum_{z\equiv r\pmod p}v_z(t),\quad
V_s(t)=\sum_{z\equiv s\pmod q}v_z(t),
\]
\[
M_p=\max_{r,t}U_r(t),\quad M_q=\max_{s,t}V_s(t),\quad
M=\max_{z,t}v_z(t).
\]
Let \(i\bmod pq\) be the CRT intersection of \(r\bmod p\) and \(s\bmod q\),
and let \(c=1\) if \(a\equiv r\pmod p\) or \(a\equiv s\pmod q\), and
\(c=2\) otherwise. Set
\[
H_{pq}=\max_{r,s,a,t}
\{2U_r(t)+2V_s(t)-v_i(t)+c\,v_a(t)\}.
\]
Then
\[
\boxed{F_{pq}(v)=\max\{H_{pq},\ 2\max(M_p,M_q)+2M\}.}      \tag{4}
\]

Here is an exhaustive partition argument, valid for arbitrary nonnegative
real weights. The all-in-one group gives \(H_{pq}\): before the last
singleton class, the useful charge is
\(2\mathbf1_{z=r\bmod p}+2\mathbf1_{z=s\bmod q}-\mathbf1_{z=i}\).
Adding the singleton raises that charge by one inside the union and by
two outside it. If a partition has at most one group of size greater than
one, merging the singleton groups into it cannot decrease
\(k\mathbf1_{k\ge2}\) pointwise. Thus its budget is dominated by the
all-in-one group. The only other partitions are the three pair-pair
partitions, with optimized budgets
\(2M_p+2M\), \(2M_q+2M\), and \(4M\), respectively. The phases of the two
pairs are independent, so these values are attained in the relaxed
budget (1). Since \(M_p,M_q\ge M\), the third is dominated. This proves (4).

## Prime-cube cofactor: attributed reproduction

Six-covering-3 published this formula in the
[primitive-partition realization result](../distinct_covering_primitive_partition_realization/proof.md)
(source42b081df2c78e4e58ca8f9978f5e5e8642d0916b, graph7464)
before this artifact. We include a self-contained proof and exact formula
controls as a reproduction of that part, not a new prime-cube claim.
The support-aware realization statements in that artifact are not
asserted or independently verified here.

Let \(C=p^3\), with \(p\) prime. Now use
\(U_r=\sum_{z=r\bmod p}v_z\), \(V_s=\sum_{z=s\bmod p^2}v_z\),
\(M_1=\max U_r\), and \(M_3=\max v_z\). Set
\[
H_{p^3}=\max_{r,s,a,t}\{2U_r(t)+\alpha V_s(t)+\gamma v_a(t)\},
\]
where \(\alpha=1\) if \(s\equiv r\pmod p\) and \(\alpha=2\) otherwise;
\(\gamma=1\) if \(a\equiv r\pmod p\) or \(a\equiv s\pmod{p^2}\),
and \(\gamma=2\) otherwise. Then
\[
\boxed{F_{p^3}(v)=\max\{H_{p^3},\ 2M_1+2M_3\}.}           \tag{5}
\]
The same argument handles every partition with at most one nonsingleton
group. Before adding the last singleton, the all-in-one charge is
\(2U_r+V_s\) when the \(p^2\)-coset lies inside the \(p\)-coset, and
\(2U_r+2V_s\) when they are disjoint. The final singleton gives \(\gamma\).
The three pair-pair partitions have budgets
\(2M_1+2M_3\), \(2M_2+2M_3\), and \(2M_2+2M_3\), where
\(M_2=\max V_s\le M_1\). This proves (5).
Both maximum terms in (4) and (5) are necessary: the exact fixtures
include strict examples in each direction. These are maxima of the
defined charging rule, not top-class union bounds or covering witnesses.

## Physical units and exact illustrations

The budget \(F_C(v)\) is charged directly in physical units in (2).
Although \(D_N(v)=(N/Q)D_Q(v)\), there is no \(N/Q\) multiplier on \(F_C\).
If one divides the inequality by \(N/Q\), the corresponding budget is
\((Q/N)F_C\). The checker computes actual footprints on all \(N\) residues.

For \(N=10080\) take \(B=288,b=48,C=35\); for \(N=15120\) take
\(B=432,b=72,C=35\). Prescribe just \(x\equiv0\pmod8\), let
\(v(x)=\mathbf1_{x\not\equiv0\pmod8}\), and let \(u(x)=\mathbf1_{x=1\bmod N}\).
Both weights vanish on the prescribed class and \(v\) is \(bC\)-periodic,
while \(u+v\) is not. The top resources are all unplaced. In both cases
\(F_{35}=25\), the four \(u\)-capacities sum to four, and the ordinary top
capacities sum to52. Thus (2) improves the ordinary capacity by exactly
**23**, retaining the unrestricted point weight. The full mixed capacity
still exceeds demand: neither root is excluded by these illustrations.

The checker also verifies eighteen mixed-weight cases against a small
genuine covering, proper local-period footprints, all15 partitions and
all phase tuples for25 four-resource weight fixtures, and an external
positive control using six-covering-1's
[published 77-class period20160 covering](../distinct_covering_min8_20160/cover.json)
(source 1b26a5217c02c00ede618b445dc935a88839391a, graph7286,
independently reviewed at7302). This is a reproduction of that input for
checking the inequality; no new construction is claimed. The exact
input digest is pinned in the checker and expected evidence.

The written proof supplies the universal mathematical argument. The finite
controls use ordinary exact Python, not a proof assistant or solver
verdict. They cannot establish a general identity merely by sampling.
The implementation supports the two four-divisor cofactors; the general
cofactor theorem is written, not an implemented arbitrary-size enumeration.
The private search frontiers and discovery LPs are not verification inputs.
No independent review of this new lemma is claimed.

The actual-resource weighted setting also appears in six-covering-2's
[residual weight framework](../distinct_covering_residual_weight_duals/proof.md)
(source b9d39eb740a866e07237be1c78b834d1ab6ea718, graph7174).
The assigned numerical target comes from the confirmed campaign brief.
[Zhang–Zhang](https://arxiv.org/html/2607.19029) gives
\(L_{\min}(7)=10080\); it does not settle \(L_{\min}(8)\).
[HKLT Problem3](https://arxiv.org/html/2605.18644) concerns the separate
pure-235 support frontier. Both primary sources were read on2026-09-30.
These references give context; (2), (4), and (5) have self-contained proofs.
