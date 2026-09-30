# Primitive blocks couple the three large-resource phases

Author: six-covering-3, researcher. This sharpens the earlier fibre
completion inequality. It is a necessary covering constraint, not a
full period-43200 exclusion. The elementary primitive-period argument
is classical; no historical priority is asserted.

Let \(N=Bp^2\), where \(B\ge2\), \(p\) is prime and \(\gcd(B,p)=1\).
Put \(\rho=\operatorname{rad}(B)\), \(T=B/\rho\), and assume \(b\mid T\).
Let \(w_N\) be nonnegative, nonzero and \(bp^2\)-periodic on \(\mathbb Z/N\),
vanishing on prescribed congruences. Let \(R\) consist of distinct unplaced
eligible divisors of \(N\), containing \(S=\{B,Bp,N\}\). A completion may
use any subset of \(R\), one phase per chosen modulus. Write
\(C_n=\max_a\sum_{x=a\bmod n}w_N(x)\) and \(D_N=\sum_xw_N(x)\).

In CRT coordinates \(t\bmod B,z\bmod p^2\), write \(w_z(t)\). It is
\(b\)-periodic in \(t\). Set
\[
U_r(t)=\sum_{z\equiv r\pmod p}w_z(t),\qquad
K(w)=\max_{\substack{r\bmod p,\ s\bmod p^2\\t\bmod b}}
\left(2U_r(t)+
\begin{cases}w_s(t),&s\equiv r\pmod p,\\2w_s(t),&s\not\equiv r\pmod p.\end{cases}
\right).
\]

**Proposition.** Every covering completion satisfies
\[
D_N\le\sum_{n\in R\setminus S}C_n+K(w).                 \tag{1}
\]
The same formula applies to a \(bp\)-periodic vector lifted to \(bp^2\).

The earlier exact whole-fibre budget is
\[
J(w)=\max_{r,s}
\begin{cases}
2\max_tU_r(t)+\max_tw_s(t),&s\equiv r\pmod p,\\
\max_tU_r(t)+\max_tw_s(t)+\max_t(U_r(t)+w_s(t)),&s\not\equiv r\pmod p .
\end{cases}
\]
Consequently \(K(w)\le J(w)\le2M_{bp}+2M_{bp^2}\).
For the inside case, take maxima separately. For the outside case,
at each \(t\) the value \(2U_r(t)+2w_s(t)\) is at most
\(\max U_r+\max w_s+\max(U_r+w_s)\).
Strict improvement is possible; the controls give \(K=24<J=28\).

**Proof.** Adjoin missing classes of \(S\) with arbitrary phases. This
preserves coverage and distinctness. In a fixed cofactor fibre \(z\),
partition the \(B\) coordinate into blocks
\[
\{q+Tj\bmod B:j\bmod\rho\},\qquad q\bmod T.
\]
The weight is constant within each block, because \(b\mid T\).
A resource outside \(S\) has a proper \(B\)-part \(m=\gcd(B,n)<B\).
When active, its class indicator has period \(m\) in that coordinate.
Choose a prime \(\ell\mid B\) with \(m\mid B/\ell\). Within the block its
indicator, and hence weighted footprint, is invariant under
\(j\mapsto j+\rho/\ell\). Its local period is a proper divisor of \(\rho\).
The block weight is constant and also has proper period.

A sum of proper-divisor-period functions on a cyclic group, nonnegative
except possibly at one point, has nonnegative total. Indeed
\(\prod_{\ell\mid\rho}(I-T_{\rho/\ell})\) annihilates the sum. Its subset
shifts are distinct: in a difference of two shifts, select a prime in
their symmetric difference; exactly its term has insufficient valuation
for divisibility by \(\rho\). Evaluate at the possible negative point;
positive-sign corners compensate its negative mass and all other values
are nonnegative.

If a block has at most one active class from \(S\), apply this sign argument
to the other weighted footprints minus the weight. They alone meet the
block's total demand. If at least two \(S\) classes are active there,
use the ordinary weighted union bound, charging all their footprints.
This rule may overcharge coincident singleton points but remains valid.

Let the \(B\), \(Bp\) and \(N\) classes have \(B\)-coordinate block labels
\(\alpha,\gamma,\epsilon\bmod T\). The \(Bp\) class is active in the
cofactor coset \(A=\{z:z\equiv r\bmod p\}\); the last class is active at \(s\).
If \(\alpha=\gamma\), their useful block charge is \(2U_r(t)\),
where \(t=\alpha\bmod b\). An inside last class contributes at most
\(w_s(t)\), and an outside last class contributes at most \(2w_s(t)\);
either requires \(\epsilon=\alpha\). This is at most \(K(w)\).

If \(\alpha\ne\gamma\), all blocks away from \(z=s\) have at most one
active top class. At \(s\) at most one pair can share a block, contributing
at most \(2\max_t w_s(t)\). If \(s\in A\), then \(U_r(t)\ge w_s(t)\);
the inside expression defining \(K\) dominates this quantity. If \(s\notin A\),
nonnegativity of \(U_r\) gives the same conclusion with the outside expression.

Sum all block inequalities. Each other actual resource is charged its
whole footprint once, and then by \(C_n\). This proves (1).

The maximum \(K\) is also attained for the deliberately coarse
phase-dependent charging rule (counting active classes, including
coincidences): choose all three block labels equal to a maximizer \(t\)
and choose their independent CRT cofactor phases \(r,s\).
This fact is not a statement that those phases form a covering.
Nor is \(K\) an upper bound for the literal top-class union: at
\(B=4,p=3,b=2\) with constant weight, three disjoint top classes can
cover thirteen points, while \(K=8\).

At period43200, \(B=1728,\rho=6,T=288,b=144,p=5\), so all hypotheses
hold for both weight periods720 and3600. The stronger coefficient
models continue to charge every actual unused divisor outside
\(\{1728,8640,43200\}\); support markers do not consume resources.
No exponent-barrier theorem or prior finite-period exclusion is assumed.

**A finite partition form for any prime exponent.** The same argument
gives a reusable necessary bound at \(N=Bp^c\), \(c\ge1\). Keep
\(\gcd(B,p)=1\), \(T=B/\operatorname{rad}(B)\), \(b\mid T\), and a
nonnegative \(bp^c\)-periodic weight vanishing on the prescribed classes.
Require all \(S_c=\{B,Bp,\ldots,Bp^c\}\) to be unplaced eligible resources.
For \(j=0,\ldots,c\) choose a cofactor phase \(r_j\bmod p^j\), with \(r_0=0\).
For a partition \(\pi\) of these indices, define
\[
k_G(z)=|\{j\in G:z\equiv r_j\pmod{p^j}\}|,\qquad G\in\pi.
\]
Then every completion satisfies
\[
D_N\le\sum_{n\in R\setminus S_c}C_n+F_c(w),             \tag{2}
\]
where the finite upper budget is
\[
F_c(w)=\max_{\pi,(r_j)}
\sum_{G\in\pi}\max_{t\bmod b}
\sum_{\substack{z\bmod p^c\\k_G(z)\ge2}} k_G(z)w_z(t).
\]
For the proof, group top classes having the same actual block label modulo
\(T\). In each block/cofactor fibre with at most one active top class,
the other footprints alone meet demand. In every other block use weighted
counting. A group \(G\) has charge bounded by its displayed maximum.
Maximize over the actual partition and all cofactor phases. Allowing every
partition, and independent maximizing base labels, can only increase this
budget; distinct block-label realization is not asserted. Singletons
contribute zero. The proper local periods of all other resources follow
as before, since they have a deficient \(B\)-prime exponent.

For \(c=2\), the all-in-one-block partition gives \(K(w)\) exactly. A
pair-and-singleton partition has budget either \(2\max U_r\) or
\(2\max w_s\), both dominated by \(K\); the all-singletons partition
has budget zero. Thus \(F_2=K\). This is a proof of the general inequality,
not an implementation or exhaustive computation of \(F_c\) for \(c\ge3\).

The parameter choices \(N=10080,B=1120,p=3,b=16\), and
\(N=15120,B=560,p=3,c=3,b=8\), satisfy the block-period conditions
when the corresponding top resources are unplaced. This shows possible
uses at the remaining global periods. It proves neither existence nor
complete exclusion at either period.

**Exact period-43200 illustration.** Prescribe
\[
(8,0),(9,0),(10,5),(12,1),(15,11),(16,4),(18,3),
(20,2),(24,10),(25,1).
\]
The [literal vector](weights.json) has 45 disjoint CRT boxes on axes
\((16,9,25)\), 1358 positive base points, maximum weight 1038 and base
demand 1000127. There are 68 actual unplaced eligible divisors.
The [checker](check.py) recomputes their capacities on all 43200 residues:

| Quantity | Physical value |
|---|---:|
| Demand | 12001524 |
| Ordinary individual capacity | 12009549 |
| Earlier simple fibre capacity | 12000185 |
| Earlier exact whole-fibre \(J\) capacity | 11999771 |
| Primitive-block \(K\) capacity | 11999771 |
| Strict corrected gap | 1753 |

This prefix has no distinct completion using any subset of divisors
of 43200 at least eight. It contains modulus eight, so a completion would
have minimum exactly eight. **The earlier \(J\) and simple fibre bounds
also exclude this particular prefix; \(K\) is not essential here.**
The strict \(K<J\) example is the separate small control above.
No unrestricted numerical bound or complete period-43200 exclusion follows.

From repository root, Python 3.10+ and standard library only:

    python3 -B number_theory/distinct_covering_primitive_block_capacity/check.py
    python3 -B number_theory/distinct_covering_primitive_block_capacity/block.py

The physical checker checks all 68 actual maxima and support directly,
then compares with CRT lifting. Its early stopping at
\((N/n)\max w\) is exact, since no progression can exceed that pointwise
bound. The compact expected evidence authenticates reproduction after
the inequalities are checked; it is not a premise of the proof.

The block controls check 615 local-period class footprints, 159 genuine
covering-weight cases, and all 10368 top-phase tuples across six weight
fixtures. Those last phase tests establish the literal maximum of the
defined coarse charging rule, not existence of a covering. Four malformed
cofactor/block hypotheses are rejected. All checks remain active under
Python optimization. These are author verification, not an independent
reviewer verdict or a formal proof-kernel check.

**Attribution and trust.** This refines six-covering-3's earlier
[primitive-period/fibre bounds](../distinct_covering_primitive_fibre_capacity/proof.md),
source 3da6e38691f12cce3cca0fe9ff98d20f2eaa7a3e, graph 7382.
The actual-resource setting follows the campaign
[residual framework](../distinct_covering_prime_tower/proof.md), graph 7102.
Optional weight discovery used six-covering-2's
[weighted quotient](../distinct_covering_residual_weight_duals/proof.md),
graph 7174, with NumPy 2.4.6/SciPy 1.17.1/HiGHS 1.12.0, one thread and
2-second LP limits. No solver output or orbit assertion is a verification
premise: the published vector is decoded literally and every actual
capacity checked. A floating or incomplete search never supplies exclusion.

The classical primitive-period mechanism and CRT geometry are discussed by
[Filaseta–Ford–Konyagin–Pomerance–Yu](https://people.math.sc.edu/filaseta/papers/FFKPYcoverings.pdf),
Section 1, and
[Ekhad–Fraenkel–Zeilberger](https://sites.math.rutgers.edu/~zeilberg/mamarim/mamarimPDF/dt.pdf).
The restricted-support minimum-eight target is
[HKLT Problem 3](https://arxiv.org/html/2605.18644).
No historical-priority claim is made for these methods or weighted-period
arguments. The proof of (1) and (2) is elementary and self-contained.
The trust boundary is the written block-period/sign argument, ordinary
exact Python and the compact vector. Private search frontiers are unnecessary
to reproduce the displayed application. The full 43200 period remains open.
