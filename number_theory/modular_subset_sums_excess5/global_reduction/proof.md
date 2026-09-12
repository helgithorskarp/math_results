# Reconstruction, counting, and a one-parameter exclusion criterion

Let \(n\ge1\) and \(N=2^n+t\), with \(t\ge3\) odd. A subset \(A\subset\mathbb Z/N\mathbb Z\)
of size \(n\) is **sum-distinct** if all its \(2^n\) subset sums, including
the empty sum, are different. Write \(S(A)\) for those sums, \(T_A=\sum A\),
and \(H_A=(\mathbb Z/N\mathbb Z)\setminus S(A)\). Set

\[
K_A=H_A-T_A/2.
\]

Division by two is in the odd-order group. Sign equivalence permits
changing individual element signs; unit/sign equivalence also permits a
common unit dilation. A sum-distinct set contains neither zero nor an
opposite pair, so it has exactly \(2^n\) distinct sign variants.

## 1. A sharp threshold excluding every doubling cycle

The signed doubling graph has vertices \([a]=\{a,-a\}\), \(a\in A\), and
edges \([a]\to[b]\) when \([2a]=[b]\). Its indegrees and outdegrees are at
most one.

**Theorem 1.** If \(2^n>(t-1)^2/4\), the signed doubling graph of every
sum-distinct \(A\) is acyclic. The strict threshold is attained by examples
for infinitely many odd \(t\).

**Proof.** Suppose a cycle has \(k\) vertices and starts at an element of
additive order \(d\mid N\). Up to signs the cycle is
\(U=\{a,2a,\ldots,2^{k-1}a\}\), where \(k\) is the least positive integer
with \(2^k\equiv\pm1\pmod d\). Changing signs translates subset sums and
preserves injectivity. All \(2^k\) subset sums of \(U\) are in the subgroup
\(\langle a\rangle\) of odd order \(d\), so \(2^k\le d\). The congruence
forces \(2^k\ge d-1\); thus \(d=2^k+1\), and these sums cover all but one
element of this subgroup.

Write \(q=N/d\) and \(L=2^{n-k}\). Distinct subsets of \(A\setminus U\)
must have distinct sums in the quotient by \(\langle a\rangle\). Otherwise
two translates of the \((d-1)\)-element set \(S(U)\) would lie in the same
\(d\)-element coset and intersect, contradicting injectivity. Hence \(L\le q\)
and

\[
t=dq-(d-1)L=d(q-L)+L. \tag{1}
\]

If \(L\ge2\), then \(L\) is even and \(q\) odd, so \(q-L\ge1\).
Equation (1) gives \((d-1)+L\le t-1\), whence

\[
2^n=(d-1)L\le ((t-1)/2)^2.
\]

If \(L=1\), then \(q=1\) would give \(t=1\), which is excluded.
Thus \(q\ge3\), so \(t\ge2d+1\) and
\(2^n=d-1\le(t-3)/2\le(t-1)^2/4\). This proves the exclusion.

For sharpness, take any \(k\ge1\), \(d=2^k+1\), \(N=d^2\), and

\[
A=\{2^i:0\le i<k\}\cup\{d2^i:0\le i<k\}.
\]

Its subset sums are uniquely \(x+dy\), \(0\le x,y\le d-2\), by base-\(d\)
representation. Thus \(n=2k\), \(t=2d-1=2^{k+1}+1\), and
\(2^n=(t-1)^2/4\). The second block is a signed doubling cycle on \(k\)
vertices. The threshold is therefore sharp as a universal acyclicity
criterion. This is not a claim that the counting bound below is sharp.
\(\square\)

## 2. Reconstruction and a uniform counting improvement

We use the full **Glaudo–Kravitz Theorem 1.5**, including embeddings of
proper odd cyclic subgroups. For a group without 2-torsion, two finite
multisets have translates of the same subset-sum multiset if and only if
one can pass between them by a sequence of these moves:

1. change an element's sign;
2. replace an embedded dilate of \(U_d=\{1,2,\ldots,2^{k-1}\}\) by another
   unit dilate, where \(k\) is the least positive integer satisfying
   \(2^k\equiv\pm1\pmod d\), for any odd \(d\ge3\).

All indicated initial lists consist of powers of two. The second move
requires an entire signed doubling cycle, irrespective of the embedding.

**Theorem 2.** Suppose \(2^n>(t-1)^2/4\). Then \(K_A\) determines \(A\)
up to element signs. In particular the number \(F_t(N)\) of actual
sum-distinct \(n\)-subsets satisfies

\[
F_t(N)\le 2^n\binom{(N-1)/2}{(t-1)/2}
       =O_t\bigl(N^{(t+1)/2}\bigr). \tag{2}
\]

Also, the uncentered subset-sum set \(S(A)\) determines \(A\) exactly.

**Proof.** If \(K_A=K_B\), then \(S(A)\) and \(S(B)\) are translates.
Because both are sum-distinct, equality as sets is equality of the
subset-sum multisets appearing in the reconstruction theorem. Start
its sequence of moves at \(A\). Theorem 1 excludes every cycle, including
cycles in proper subgroups. Sign changes preserve the signed graph, so
no first move of the second type can ever occur. All moves are sign
changes, proving the assertion.

Complementary subsets have sums adding to \(T_A\). No subset sum equals
\(T_A/2\), since it would equal the sum of the complementary, distinct
subset. Consequently \(K_A\) consists of zero and \((t-1)/2\) different
nonzero opposite pairs. There are at most the binomial number in (2)
such sets. Changing signs translates \(H_A\) and changes its center by
the same amount, so it preserves \(K_A\). Every sign class contains
exactly \(2^n\) subsets, proving (2).

Finally if \(S(A)=S(B)\), then
\(\sum S(A)=2^{n-1}T_A=2^{n-1}T_B\) in the group. Since 2 is invertible,
\(T_A=T_B\). The already proved sign equivalence writes \(B\) as a sign
flip of a subset \(D\subseteq A\), so \(2\sum D=0\). Injectivity of
subset sums forces \(D\) empty. \(\square\)

At excess five, (2) holds already when \(n\ge3\) and gives

\[
F_5(N)\le (N-5)(N-1)(N-3)/8=O(N^3). \tag{3}
\]

This is an unrestricted bound, including every chain-free set. The
modular paper states an \(O(N^{(t+3)/2})\) estimate for fixed odd excess;
(2) improves that stated exponent by one for every odd \(t\ge3\).
The desired excess-five \(O(N^2)\) estimate is still open here.

The strict condition cannot simply be weakened even for reconstruction.
At \(N=289\), \(n=8\), \(t=33\), let
\(P=\{1,2,4,8\}\), \(A=P\cup17P\), and
\(B=P\cup17\{3,6,12,7\}\). The second blocks have subset sums equal to
the order-17 subgroup with respectively 272 and 238 omitted. The first
block gives 16 different quotient residues, so both full sets are
sum-distinct. Thus \(S(B)=S(A)-34\); their centers also differ by -34,
and their centered holes agree. Their signed element classes differ.
Here \(2^8=(33-1)^2/4\). This example explains why embeddings of proper
subgroups in the reconstruction theorem must be retained.

## 3. Five holes have a unit offset

Now fix \(t=5\), \(n\ge5\). Write \(K_A=\{0,\pm u,\pm v\}\), with
the two nonzero signed pairs distinct, and
\(Q(X)=1+X^u+X^{-u}+X^v+X^{-v}\).

For any \(d>1\) dividing \(N\), evaluation at a primitive \(d\)-th root
\(\zeta\) gives

\[
Q(\zeta)=-\zeta^{-T_A/2}\prod_{a\in A}(1+\zeta^a),\qquad
\operatorname{Norm}_{\mathbb Q(\zeta)/\mathbb Q}Q(\zeta)
 =2^{k_d\varphi(d)}, \tag{4}
\]

where \(k_d=|\{a\in A:d\mid a\}|\). To justify the norm, if \(d\nmid a\)
write \(1+\zeta^a=(1-\zeta^{2a})/(1-\zeta^a)\): the automorphism
\(\zeta\mapsto\zeta^2\) makes its norm one. A factor with \(d\mid a\)
has norm \(2^{\varphi(d)}\). The phase and sign have norm one.

**Theorem 3.** Each of \(\gcd(u,N),\gcd(v,N)\) is 1 or 3, and at most
one is 3. Thus at least one offset is a unit. After unit dilation every
centered hole set has the form

\[
K_b=\{0,\pm1,\pm b\},\quad
2\le b\le(N-1)/2,\quad \gcd(b,N)\in\{1,3\}. \tag{5}
\]

**Proof.** If a prime divisor \(p\mid N\) divides both offsets, the norm
in (4) is \(5^{p-1}\), impossible. If a prime \(p\ge5\) divides just
one offset, that norm is the product of the conjugates of
\(3+\zeta+\zeta^{-1}\). Every conjugate is strictly greater than one,
so the norm is an integer greater than one. It is odd: modulo 2, the
relevant polynomial is \(X^2+X+1\), coprime to \(\Phi_p(X)\), since
its roots have order 3 and \(p\ne3\). Thus the resultant, and hence
the norm, is odd, contradicting (4).

If 9 divides an offset and \(N\), the other offset is coprime to 3 by
the first argument. Apply the same reasoning with \(d=9\):
\(\Phi_9(X)=X^6+X^3+1\) is coprime to \(X^2+X+1\) modulo 2 (its value
at a root of order 3 is 1). Again the norm is odd and greater than one.
This excludes every gcd other than 1 or 3, and their simultaneous value
3 was already excluded. Normalizing a unit offset and taking the other
offset's least absolute representative gives (5). \(\square\)

This gives the additional unrestricted bound

\[
F_5(N)\le 2^n\left[\binom{\varphi(N)/2}{2}
 +\mathbf1_{3\mid N}\frac{\varphi(N)\varphi(N/3)}4\right]. \tag{6}
\]

Indeed the centered holes have two unit signed pairs, or one unit pair
and one pair of gcd 3. Theorem 2 makes their choice determine one sign
class. Formula (6) remains an upper bound, not a feasibility assertion.

## 4. An exact determinant condition covering every set

First, every nonunit element of \(A\) has gcd 3 with \(N\), and at most
one exists. For completeness, if \(d=\gcd(a,N)>1\), the numbers of
represented sums in each class modulo \(d\) are even. Each missing count
is therefore positive and odd, so \(d\le5\). Since \(5\nmid N\), \(d=3\).
Two such elements would make all three represented counts divisible by
4; for even \(n\), \(N/3\equiv3\pmod4\), requiring at least nine holes.

If \(3\mid N\), applying (4) with \(d=3\) to (5) shows that the number
of nonunits is exactly one when \(3\mid b\), and zero otherwise:
\(Q(\zeta_3)\) is respectively 2 or -1, with norms 4 or 1.

Let \(C_b\) be the \(N\)-by-\(N\) circulant matrix with entry 1 in
position \((i,j)\) when \(i-j\in K_b\), and 0 otherwise. Then every
admissible core in (5) satisfies

\[
\det C_b=
\begin{cases}5,&\gcd(b,N)=1,\\20,&\gcd(b,N)=3.\end{cases} \tag{7}
\]

To prove this, multiply all \(N\) Fourier eigenvalues. The trivial one
is 5. At the other roots, (4)'s first identity applies. Their phase
product and sign product are one, because \(N\) is odd. For an element
\(a\) of gcd \(d_a\),
\(\prod_{j=0}^{N-1}(1+\zeta_N^{ja})=2^{d_a}\), by grouping equal roots
of its odd order. Omitting \(j=0\) divides this by 2. Hence

\[
\det C_b=5\,2^{\sum_{a\in A}(\gcd(a,N)-1)},
\]

which is (7). This is an integer equality, not a numerical approximation.

For a prime \(p\equiv1\pmod N\) and an element \(w\in\mathbb F_p\) of
exact order \(N\), put

\[
R_p(b)=\prod_{j=1}^{(N-1)/2}
(1+w^j+w^{-j}+w^{bj}+w^{-bj}).
\]

Pairing \(j\) and \(-j\) in the determinant proves the exact necessary
test

\[
R_p(b)^2\equiv
\begin{cases}1,&\gcd(b,N)=1,\\4,&\gcd(b,N)=3\end{cases}\pmod p. \tag{8}
\]

There are no chosen anchors or unexamined component profiles in this
reduction: every admissible set has a core in (5), and every such core
must pass (8) for every usable prime. By Theorem 2, a core determines
at most one unit/sign equivalence class. Passing a finite list of tests
does not by itself prove that a core is realizable.

## 5. Complete finite consequence and remaining obligation

The three published types \(B_0,B_1,B_2\) have centered holes, up to unit
dilation, respectively

\[
\{0,\pm1,\pm2\},\quad \{0,\pm1,\pm3\},\quad
\{0,\pm3,\pm4\}. \tag{9}
\]

For \(B_0\) this follows from its consecutive subset sums. For \(B_1\),
its two intervals of sums give offsets \(2m+1,2m+2\); dilation by 2
gives signed offsets 3 and 1. For \(B_2\), its four intervals give
offsets 1 and \(m+2\); dilation by 4 gives signed offsets 4 and 3.
Here \(m=2^{n-2}\). Their inequivalence and counts are proved in the
[long-chain theorem](../proof.md).

To generate all normalized cores from (9), choose either offset that
is a unit, divide the other by it, and take a least absolute residue.
The finite certificate applies (8) to every candidate in (5) for
**each \(5\le n\le14\)**. Its survivors are exactly those normalized
cores from (9). Every other core has an explicit modular determinant
obstruction. Theorem 2 then proves the **complete unrestricted
classification** in this range, with exactly the three types and
\(3\,2^{n-1}\varphi(N)\) subsets. There is no enumeration of only
chain-containing sets in this computation.

The all-\(n\) contributions are Theorems 1–3, the improved counting
bound, and the exact one-parameter necessary formulation (5), (7).
The computation supplies additional complete finite cases, not the
justification for these uniform statements. For \(n\ge15\), neither
the full classification nor an unrestricted \(O(N^2)\) bound is proved
here. A uniform bound on the number of admissible cores, or a theorem
forcing every core into (9), would close the intended next step.

The proof uses Glaudo–Kravitz Theorem 1.5 as an external mathematical
premise. Everything else above is proved explicitly. The finite
corollary additionally trusts the exact Python enumeration, modular
arithmetic and coverage proof. Independent matrix determinants check
small controls, and literal subset sums check the known types and sharp
boundary examples. No proof-assistant formalization, independent peer
review, or uniform inference from a tested range is claimed.
