# Locally finite normalized subgroup-count spectra for all finite groups

All groups in this note are finite. Write
$$
c(G)=|\{H\le G:H\text{ is cyclic}\}|,\qquad
s(G)=|\{H\le G\}|,\qquad r(G)=\omega(|G|),
$$
$$
\eta(G)=c(G)/2^{r(G)},\qquad
\lambda(G)=s(G)/2^{r(G)}.
$$
Both counts include the trivial subgroup, and $\omega(1)=0$.
Let $R(G)$ denote the solvable radical. A **central cyclic Sylow
factor** is a Sylow subgroup that is cyclic and contained in $Z(G)$.

## 1. Statements and constants

For a real number $K\ge1$, put
$$
\gamma=\prod_{p<16,\ p\ {\rm prime}}\frac{16}{p}
       =\frac{16^6}{30030}=\frac{8388608}{15015},
\qquad
D(K)=\lceil\gamma K^4\rceil,
\tag{1}
$$
$$
A(K)=\lfloor2K-1\rfloor,\qquad
E(K)=\lfloor2K\rfloor^{\lfloor K\rfloor},
$$
$$
B(K)=\max\left\{D(K),\
       \left\lceil4D(K)(K-1)+2\right\rceil,\
       E(K)\right\},\qquad
M(K)=\prod_{p\le B(K),\ p\ {\rm prime}}p^{A(K)}.
\tag{2}
$$
These are explicit finite bounds; computing or factoring $M(K)$ is
unnecessary for the proof.

**Theorem A (bounded core).** If $\eta(G)\le K$, then
$$
|G/R(G)|\le D(K),
\tag{3}
$$
and every prime $p>B(K)$ dividing $|G|$ has a central cyclic Sylow
subgroup. Consequently
$$
G\cong S\times C,\qquad \gcd(|S|,|C|)=1,\qquad |S|\mid M(K),
\tag{4}
$$
where $C$ is the product of all central cyclic Sylow subgroups of
$G$, and $S$ has no such Sylow subgroup. In particular, only finitely
many isomorphism types of $S$ occur for a fixed $K$.

**Theorem B (joint spectrum).** For every $K\ge1$, the set
$$
\{(\eta(G),\lambda(G)):\eta(G)\le K\}
\tag{5}
$$
is finite. Thus each normalized counting spectrum has only finitely
many values in any bounded real interval.

There is no solvability assumption in either theorem. The
[preceding contribution](../normalized_cyclic_count_finiteness/PROOF.md)
proved the solvable case with substantially smaller prime bounds.
The new steps here are the radical-index bound (3) and a relative
counting argument for arbitrary normal subgroups. The short elementary
lemmas used again below are included with proofs.

These results bound orders after cyclic coprime factors have been removed.
They do not give a list of the remaining groups or the attained values.

## 2. Published inputs

We use the following three external results, in addition to standard
Sylow theory, Schur--Zassenhaus for abelian normal Hall subgroups, and
elementary facts about solvable radicals.

1. **Richards's minimum:** $c(G)\ge\tau(|G|)$, where $\tau$ counts
   positive divisors.
2. **Amiri's order-divisibility bijection:** if a Sylow $q$-subgroup
   of a group of order $n$ is neither cyclic nor generalized quaternion,
   there is a bijection from that group to $C_{n/q}\times C_q$ such
   that each element order divides its image's order.
3. **Lucchini, Lemma 1.1(a) (1998):** if a finite group $Q$ has no
   nonidentity abelian normal subgroup, then
   $|H||C_Q(H)|\le|Q|$ for every $H\le Q$.

See [SOURCES.md](SOURCES.md) for the exact statements, primary links, and
what was independently read. The code does not prove these inputs.
In particular, no classification of finite simple groups or group
database is being reproduced here.

Every element generates a cyclic subgroup with $\varphi(o(g))$
generators, whence
$$
c(G)=\sum_{g\in G}\frac1{\varphi(o(g))}.
\tag{6}
$$
If $L\le G$, restricting this sum to $G\setminus L$ gives
$c(G)-c(L)$: all generators of a cyclic subgroup not contained in
$L$ lie outside $L$.

Richards's bound gives
$$
\eta(G)\ge\prod_{p^a\parallel |G|}\frac{a+1}{2}\ge1.
\tag{7}
$$
Consequently $\eta(G)\le K$ bounds every exponent $a$ by $A(K)$.

If $q^a\parallel |G|$ and its Sylow subgroup satisfies Amiri's
hypothesis, the bijection and (6), using
$u\mid v\Rightarrow\varphi(u)\mid\varphi(v)$, give
$$
c(G)\ge ((a-1)q+2)\tau(|G|/q^a).
$$
Indeed $C_{q^{a-1}}\times C_q$ has $q^2-1$ elements of order $q$
and $q\varphi(q^j)$ of order $q^j$ for $2\le j\le a-1$, so its
cyclic count is $(a-1)q+2$. It follows that
$$
q(a-1)\le2K-2.
\tag{8}
$$
An elementary abelian subgroup $\mathbb F_q^d$ with $d\ge2$ cannot
lie in a cyclic or generalized quaternion group. Thus, whenever $G$
contains such a subgroup,
$$
q(d-1)\le2K-2,\qquad d\le\lfloor K\rfloor.
\tag{9}
$$

## 3. Passing through a solvable kernel

**Lemma 1 (coprime elementary abelian cosets).** Suppose
$G=V\rtimes H$, where $V=\mathbb F_p^d$ and $p\nmid|H|$.
For $h\in H$, put $e=o(h)$ and $f=\dim C_V(h)$. Exactly
$p^{d-f}$ elements of $Vh$ have order $e$; all others have order
$pe$. Moreover
$$
\sum_{v\in V}\frac1{\varphi(o(vh))}
=\frac1{\varphi(e)}
 \left(c(V)+\frac{p-2}{p-1}(p^{d-f}-1)\right)
\ge \frac{c(V)}{\varphi(e)}.
\tag{10}
$$

**Proof.** The averaging operator
$P=e^{-1}(1+h+\cdots+h^{e-1})$ projects $V$ onto $C_V(h)$.
Since $(v,h)^e=(eP(v),1)$, the order is $e$ on its kernel and
$pe$ otherwise. The kernel has the asserted size. Now use
$\varphi(pe)=(p-1)\varphi(e)$ and
$c(V)=1+(p^d-1)/(p-1)$. This includes $h=1$ and $p=2$.
$\square$

**Lemma 2 (two monotonicities).** If $N\unlhd G$ is solvable, then
$$
\eta(G)\ge\eta(G/N).
\tag{11}
$$
If in addition $N\le L<G$ with $L\unlhd G$, define
$$
\Delta(G,L)=\frac{c(G)-c(L)}{2^{r(G)}}.
$$
Then
$$
\Delta(G,L)\ge\Delta(G/N,L/N).
\tag{12}
$$
Neither $G$ nor $L$ is assumed solvable.

**Proof.** Induct on $|N|$, with $N=1$ immediate. Choose a minimal
nontrivial $G$-normal subgroup $V\le N$. Because $N$ is solvable,
$V\cong\mathbb F_p^d$. Put $Q=G/V$.

If $p\mid|Q|$, then $r(G)=r(Q)$. The cyclic-subgroup image map onto
$Q$ is surjective: lift a generator of each cyclic subgroup. The same
is true after restricting to cyclic subgroups not contained in $L$
and $L/V$, respectively. This gives both one-step inequalities.

If $p\nmid|Q|$, the subgroup $V$ is normal Hall, so
$G=V\rtimes H$ with $H\cong Q$. Summing (10) over all $h$ gives
$c(G)\ge c(V)c(Q)\ge2c(Q)$. For the relative assertion, $L$ is a
union of $V$-cosets, so sum (10) only over those outside $L$.
It gives
$$
c(G)-c(L)\ge c(V)(c(Q)-c(L/V))
          \ge2(c(Q)-c(L/V)).
$$
Here $r(G)=r(Q)+1$, proving both one-step inequalities after
normalization. Induct on the solvable normal subgroup $N/V$ of $Q$.
$\square$

## 4. A bound for the quotient by the solvable radical

**Lemma 3.** For every finite $G$,
$$
|G/R(G)|\le\gamma\,\eta(G)^4.
\tag{13}
$$

**Proof.** First let $Q$ have trivial solvable radical. It has no
nonidentity abelian normal subgroup. Since $H\le C_Q(H)$ for cyclic
$H$, Lucchini's lemma gives $o(x)\le\sqrt{|Q|}$ for every $x\in Q$.
By (6),
$$
c(Q)\ge |Q|/\sqrt{|Q|}=\sqrt{|Q|}.
\tag{14}
$$
This also holds for $Q=1$.

For every positive integer $n=\prod p^{a_p}$,
$$
\frac{2^{4\omega(n)}}n
=\prod_{p\mid n}\frac{16}{p^{a_p}}
\le\prod_{p<16,\ p\ {\rm prime}}\frac{16}{p}=\gamma.
\tag{15}
$$
Factors with $p\ge16$ are at most 1, and exponents can only decrease
the product. Combining (14) and (15) yields
$$
\eta(Q)^4
=\frac{c(Q)^4}{2^{4r(Q)}}\ge\frac{|Q|}{\gamma}.
$$
For $Q=G/R(G)$, the radical is trivial, and (11) gives
$\eta(Q)\le\eta(G)$. This proves (13). $\square$

For completeness, $R(G/R(G))=1$ because the preimage of a solvable
normal subgroup of that quotient would be a solvable normal extension
of $R(G)$. Under $\eta(G)\le K$, (13) implies (3).

## 5. Relative counts without solvability

**Lemma 4.** For every proper normal subgroup $L<G$,
$$
\Delta(G,L)\ge
2^{-r(G/R(G))-1}\ge \frac1{2|G/R(G)|}.
\tag{16}
$$

**Proof.** Set $N=L\cap R(G)$, $U=G/N$, and $J=L/N$.
The subgroup $N$ is solvable and normal in $G$, so (12) gives
$\Delta(G,L)\ge\Delta(U,J)$. Also $J$ embeds into $G/R(G)$.
Write $T=U/J\cong G/L\ne1$.

Every nontrivial cyclic subgroup of $T$ is the image of a cyclic
subgroup of $U$ not contained in $J$. Richards's bound gives
$$
c(U)-c(J)\ge c(T)-1
          \ge 2^{r(T)}-1\ge2^{r(T)-1}.
$$
Since $r(U)\le r(J)+r(T)$ and $r(J)\le r(G/R(G))$,
$$
\Delta(U,J)\ge2^{-r(J)-1}
            \ge2^{-r(G/R(G))-1}.
$$
Finally $2^{r(Q)}\le |Q|$ for every finite group $Q$, including the
trivial group. This proves (16). $\square$

When $G$ is solvable, this recovers
$c(G)-c(L)\ge2^{r(G)-1}$. The use of $L\cap R(G)$, rather than
quotienting by all of $R(G)$, keeps the distinguished subgroup inside
the quotient operation in (12).

## 6. Normal cyclic Sylow subgroups

**Lemma 5.** Suppose $\eta(G)\le K$ and $G$ has a normal cyclic
Sylow subgroup $P\cong C_{p^a}$, $a\ge1$, that is not central. Then
$p$ is odd and
$$
\eta(G)\ge\frac{a+1}{2}
 +\frac{p^a-a-1}{4D(K)}.
\tag{17}
$$
In particular,
$$
p^a\le4D(K)(K-1)+2.
\tag{18}
$$

**Proof.** Split $G=P\rtimes H$ by Schur--Zassenhaus, and put
$L=C_H(P)\lneq H$. The automorphism group of a cyclic 2-group is a
2-group, so an odd-order complement acts trivially when $p=2$.
Thus $p$ is odd.

For odd $p$, the kernel of
$\operatorname{Aut}(C_{p^a})\to\operatorname{Aut}(C_p)$ is a
$p$-group. Every nontrivial automorphism in the image of the
$p'$-group $H$ therefore has a multiplier $u$ with $u-1$ a
unit modulo $p^a$. For $h\notin L$, put $e=o(h)$. The identity
$$
(u-1)(1+u+\cdots+u^{e-1})=u^e-1=0\pmod{p^a}
$$
shows that every element of $Ph$ has order $e$. The coset
contributes $p^a/\varphi(e)$ to (6). For $h\in L$, its contribution
is instead $(a+1)/\varphi(e)$, by coprimeness. Hence the exact identity
is
$$
c(G)=(a+1)c(H)+(p^a-a-1)(c(H)-c(L)).
\tag{19}
$$
This identity imposes no solvability assumption on $H$ or $L$.

By (11), $\eta(H)=\eta(G/P)\le K$, so (3) gives
$|H/R(H)|\le D(K)$. Applying (16) to $L\lneq H$ gives
$c(H)-c(L)\ge2^{r(H)}/(2D(K))$.
Use $c(H)\ge2^{r(H)}$ and $r(G)=r(H)+1$ in (19) to obtain (17).
Its coefficient $p^a-a-1$ is positive here. Rearranging gives
$$
p^a\le4D(K)K-(2D(K)-1)(a+1)
    \le4D(K)(K-1)+2,
$$
since $a+1\ge2$ and $2D(K)-1>0$. $\square$

## 7. Bounding all primes in the core

**Proof of Theorem A.** The radical assertion is already proved.
For the prime assertion, induct on $|G|$, fixing $K$.
If the largest prime divisor $p$ of $|G|$ is at most $B(K)$,
there is nothing to prove; the trivial group is immediate. Assume
$p>B(K)$, and let $P$ be a Sylow $p$-subgroup.

Since $B(K)\ge E(K)\ge2$, the prime $p$ is odd. If $P$ were
noncyclic, (8) would give $p\le2K-2$. This contradicts
$p>B(K)\ge E(K)\ge\lfloor2K\rfloor>2K-2$.
Therefore $P$ is cyclic.

If $R(G)=1$, (3) gives $|G|\le D(K)\le B(K)$, another
contradiction. Thus $R(G)\ne1$. Choose a minimal nontrivial
$G$-normal subgroup $V\le R(G)$, with
$V\cong\mathbb F_q^d$. By (11), $\eta(G/V)\le K$, so the
inductive prime assertion applies to this quotient.

If $q=p$, cyclicity of $P$ forces $V\cong C_p$. If the quotient
has order coprime to $p$, then $P=V$ is normal. Otherwise its
Sylow $p$-subgroup is central by induction, and its full preimage
is exactly $P$. Again $P$ is normal.

Suppose $q\ne p$. The image of $P$ is central in $G/V$, so
$VP\unlhd G$. We show that $P$ acts trivially on $V$.
If $d=1$, this follows from
$|\operatorname{Aut}(C_q)|=q-1<p$.
If $d\ge2$, (9) gives $q\le2K-2$ and
$d\le\lfloor K\rfloor$. Every prime divisor of
$$
|\mathrm{GL}_d(q)|=
q^{d(d-1)/2}\prod_{i=1}^d(q^i-1)
$$
is either $q<p$, or divides a number
$$
q^i-1\le\lfloor2K\rfloor^{\lfloor K\rfloor}-1
      =E(K)-1<p.
$$
Thus $p\nmid|\operatorname{Aut}(V)|$, and the $p$-group $P$
acts trivially. Now $VP=V\times P$, whose unique Sylow
$p$-subgroup $P$ is characteristic. Therefore $P\unlhd G$.

In every case $P$ is normal. Lemma 5 and (2) force it to be central.
Split $G=P\times H$. Writing $|P|=p^a$, coprime
multiplicativity gives
$\eta(H)=2\eta(G)/(a+1)\le K$.
Induction applied to $H$ proves the prime assertion for every
prime greater than $B(K)$, completing the induction.

Let $C$ now be the product of all central cyclic Sylow subgroups.
It is a central cyclic normal Hall subgroup, so $G=C\times S$
with coprime orders. A central cyclic Sylow subgroup of $S$ would
also be one of $G$, contradicting the choice of $C$.
Thus the prime assertion bounds every prime in $|S|$ by $B(K)$.
Moreover $\eta(S)\le\eta(G)\le K$, so (7) bounds every exponent
by $A(K)$. This proves $|S|\mid M(K)$.
There are only finitely many multiplication tables of the resulting
bounded orders. $\square$

## 8. Finiteness of the spectra

**Proof of Theorem B.** Both cyclic and total subgroup counts are
multiplicative on direct products of coprime orders. Indeed every
subgroup is the product of its projections: taking suitable powers
separates the coordinates of each element by the Chinese remainder
theorem. That product is cyclic exactly when both projections are cyclic.

Apply Theorem A to write $G=S\times C$. Then
$$
(\eta(G),\lambda(G))
=\delta(C)(\eta(S),\lambda(S)),\qquad
\delta(C)=\prod_{p^a\parallel|C|}\frac{a+1}{2}.
\tag{20}
$$
The choices for $S$ lie in a finite set. By (7), every exponent
$a$ is at most $A(K)$. Exponent-one factors contribute 1.
Every remaining factor is at least $3/2$, and
$\delta(C)\le\eta(G)\le K$.
There are therefore at most $\lfloor\log_{3/2}K\rfloor$
remaining factors, each from the finite set
$\{(a+1)/2:2\le a\le A(K)\}$.
Only finitely many values of $\delta(C)$ occur, proving (5).
Finally $\eta(G)\le\lambda(G)$, so a bound on $\lambda$
also gives a bound on $\eta$; the total-subgroup spectrum is
locally finite as well. $\square$

## 9. Scope and checks

The universal argument is the proof above. Its new nonsolvable
bridges are (13), (12), and (16); the cyclic Sylow identity and
elementary abelian coset calculation are restated from the preceding
work. The three published premises in Section 2 remain external
trust boundaries.

The exact controls use explicit nonsolvable permutation and matrix
groups, solvable radicals computed from normal subgroups, quotient
and relative counts, and scalar extensions with nonsolvable
complements and centralizers. Counts come from literal sets of
powers and are cross-checked with (6). They do not enumerate the
groups allowed by (4), certify the external theorems, or replace
independent review.

For the small solvability ranges in Das--Dey--Galindo--Sharma v2,
the preceding solvable theorem already answered Questions 6.1, 9.1,
and 4.16. The present contribution establishes finiteness at every
bounded normalized count, including the full nonsolvable range.
The earlier sharper constants for solvable groups remain useful.
See [SOURCES.md](SOURCES.md) for comparison with Gao--Garonzi's prior
bound in terms of the unnormalized count $c(G)$.
