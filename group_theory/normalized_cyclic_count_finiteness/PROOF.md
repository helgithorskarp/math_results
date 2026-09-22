# Effective finiteness from normalized cyclic-subgroup counts

For a finite group $G$, put

$$
c(G)=|\{U\le G:U\text{ cyclic}\}|,\qquad
s(G)=|\{U\le G\}|,\qquad r(G)=\omega(|G|),
$$

$$
\eta(G)=c(G)/2^{r(G)},\qquad \lambda(G)=s(G)/2^{r(G)}.
$$

The trivial subgroup is counted. Set $\omega(1)=0$. A **central cyclic
Sylow factor** means a Sylow subgroup of $G$ that is cyclic and contained
in $Z(G)$; it is consequently a coprime direct factor. All groups below
are finite.

## 1. Main theorem

For a real number $K\ge1$, define the following finite set of primes:

$$
\mathcal P_K=
\{p:p\text{ prime},\ p\le4K-2\}
\ \cup\!
\bigcup_{\substack{q\text{ prime},\ i\ge2\\q(i-1)\le2K-2}}
\{p:p\text{ prime},\ p\mid q^i-1\}.
\tag{1}
$$

Let $B(K)=\max\mathcal P_K$, $A(K)=\lfloor2K-1\rfloor$, and

$$
M(K)=\prod_{p\le B(K),\ p\text{ prime}}p^{A(K)}.
\tag{2}
$$

The first set in (1) contains 2, and the union is finite because
$q\le2K-2$ and $i\le1+(2K-2)/q$.

**Theorem A.** If $G$ is solvable and $\eta(G)\le K$, every prime
$p>B(K)$ dividing $|G|$ has a central cyclic Sylow subgroup. Moreover,

$$
G\cong S\times C,\qquad \gcd(|S|,|C|)=1,
\qquad |S|\mid M(K),
\tag{3}
$$

where $C$ is cyclic and $S$ has no central cyclic Sylow subgroup. One may
take $C$ to be the product of all central cyclic Sylow subgroups of $G$.
Thus the isomorphism types of these groups $S$ form a finite set depending
only on $K$.

**Theorem B.** For every $K\ge1$, the set

$$
\{(\eta(G),\lambda(G)):G\text{ solvable},\ \eta(G)\le K\}
\tag{4}
$$

is finite. In particular, both normalized counting spectra on solvable
groups are locally finite.

These are structural theorems, not classifications by enumeration. The
bounds in (2) are deliberately coarse. The solvability hypothesis is used
in the normal-subgroup inductions; no assertion for arbitrary nonsolvable
groups at unrestricted $K$ is made.

## 2. External inputs and elementary consequences

We use Richards's inequality $c(G)\ge\tau(|G|)$, where $\tau$ counts
positive divisors. We also use the following published theorem of Amiri:
if a Sylow $q$-subgroup of a group of order $n$ is neither cyclic nor
generalized quaternion, there is a bijection from $G$ to
$C_{n/q}\times C_q$ under which each element order divides its image's
order. See [SOURCES.md](SOURCES.md) for the precise primary references.
These two inputs are imported, not re-proved by the accompanying code.

Partitioning elements by the cyclic subgroup they generate gives

$$
c(G)=\sum_{g\in G}\frac1{\varphi(o(g))}.
\tag{5}
$$

Since $u\mid v$ implies $\varphi(u)\mid\varphi(v)$, Amiri's theorem and
(5), for $n=q^a m$ with $q\nmid m$, imply

$$
c(G)\ge c(C_{q^{a-1}}\times C_q)\tau(m)
=((a-1)q+2)\tau(m).
\tag{6}
$$

Here $a\ge2$. To check the last elementary formula, an abelian group
$C_{q^{a-1}}\times C_q$ has $q^2-1$ elements of order $q$, and for
$2\le j\le a-1$ it has $q\varphi(q^j)$ elements of order $q^j$.
Equation (5) gives $1+(q+1)+(a-2)q=(a-1)q+2$.

Consequently, under $\eta(G)\le K$,

$$
q(a-1)\le2K-2
\quad\text{if the Sylow }q\text{-subgroup is neither cyclic nor
generalized quaternion}.
\tag{7}
$$

Richards's inequality also gives, without any Sylow restriction,

$$
\eta(G)\ge\prod_{p^a\parallel |G|}\frac{a+1}{2},
\qquad a\le A(K).
\tag{8}
$$

We use standard Sylow theory, elementary abelian minimal normal subgroups
in solvable groups, and Schur–Zassenhaus for an abelian normal Hall
subgroup. Generalized quaternion groups have a unique involution, so
cannot contain an elementary abelian subgroup of rank at least two.

## 3. A coset count and two normal-subgroup inequalities

**Lemma 1 (coprime elementary abelian cosets).** Let $V=\mathbb F_p^d$
and let a $p'$-group $H$ act on $V$. For $h\in H$, put $e=o(h)$ and
$f=\dim C_V(h)$. In the coset $Vh$ of $V\rtimes H$, exactly
$p^{d-f}$ elements have order $e$, and the other $p^d-p^{d-f}$ have order
$pe$. In particular,

$$
\sum_{v\in V}\frac1{\varphi(o(vh))}
=\frac1{\varphi(e)}\left(
c(V)+\frac{p-2}{p-1}(p^{d-f}-1)\right)
\ge\frac{c(V)}{\varphi(e)}.
\tag{9}
$$

**Proof.** Since $p\nmid e$, the map
$P=e^{-1}(1+h+\cdots+h^{e-1})$ is the projection onto $C_V(h)$.
The $e$th power of $(v,h)$ is $(eP(v),1)$. Its order is therefore $e$
when $P(v)=0$ and $pe$ otherwise. The kernel has size $p^{d-f}$.
Now use $\varphi(pe)=(p-1)\varphi(e)$ and
$c(V)=1+(p^d-1)/(p-1)$. This also covers $h=1$ and $p=2$. $\square$

The formula is restated with proof to make this directory self-contained;
it was established in the preceding
[equality contribution](../cyclic_subgroup_solvability_equality/PROOF.md).

**Lemma 2 (quotient monotonicity).** If $N$ is a solvable normal subgroup
of $G$, then $\eta(G)\ge\eta(G/N)$.

**Proof.** First, for every normal subgroup $V$, the map sending a cyclic
subgroup to its image in $G/V$ is surjective: lift a generator of each
cyclic subgroup of $G/V$. Hence $c(G)\ge c(G/V)$.

If $N\ne1$, choose a minimal nontrivial $G$-normal subgroup $V\le N$.
Solvability of $N$ implies $V\cong\mathbb F_p^d$. If $p\mid|G/V|$,
then $r(G)=r(G/V)$, so the preceding surjection proves the desired
one-step inequality. If $p\nmid|G/V|$, Schur–Zassenhaus gives
$G=V\rtimes H$ with $H\cong G/V$. Summing (9) gives
$c(G)\ge c(V)c(H)\ge2c(H)$, while $r(G)=r(H)+1$.
Iterate on $N/V\unlhd G/V$. The case $N=1$ starts the induction.
$\square$

**Lemma 3 (relative count).** If $L<G$ is normal and solvable, then

$$
c(G)-c(L)\ge2^{r(G)-1}.
\tag{10}
$$

**Proof.** Induct on $|L|$. If $L=1$, $G\ne1$ and Richards's bound gives
$c(G)-1\ge2^{r(G)}-1\ge2^{r(G)-1}$.
For $L\ne1$, choose a minimal nontrivial $G$-normal subgroup
$V\le L$, with $V\cong\mathbb F_p^d$. Put $Q=G/V$ and $\bar L=L/V$.

If $p\mid|Q|$, the cyclic-subgroup image map is surjective also after
restricting to subgroups not contained in $L$ and $\bar L$ respectively:
a generator outside $\bar L$ has every lift outside $L$. Thus

$$
c(G)-c(L)\ge c(Q)-c(\bar L)\ge2^{r(Q)-1}=2^{r(G)-1}.
$$

If $p\nmid|Q|$, take $G=V\rtimes H$ as in Lemma 2. The subgroup $L$
is the full preimage of $\bar L$, so a coset $Vh$ is outside $L$ exactly
when the image of $h$ is outside $\bar L$. Equation (5) restricted to
these elements counts $c(G)-c(L)$: all generators of a cyclic subgroup
outside $L$ are outside $L$. Applying (9) only to those cosets yields

$$
c(G)-c(L)\ge c(V)(c(Q)-c(\bar L))
\ge2\cdot2^{r(Q)-1}=2^{r(G)-1}.
$$

Both applications of induction are valid because $\bar L<Q$ is normal
and solvable and has smaller order. $\square$

## 4. The price of a noncentral normal cyclic Sylow subgroup

**Lemma 4.** Suppose that $G$ is solvable and has a normal cyclic Sylow
subgroup $P\cong C_{p^a}$, $a\ge1$. If $P\nleq Z(G)$, then $p$ is
odd and

$$
\eta(G)\ge\frac{p^a+a+1}{4}.
\tag{11}
$$

**Proof.** Write $G=P\rtimes H$ by Schur–Zassenhaus and set
$L=C_H(P)$. The group $L$ is a proper normal subgroup of the solvable
group $H$. A $p'$-automorphism of $C_{p^a}$ that is nontrivial has
nontrivial reduction modulo $p$: the kernel of reduction on the
automorphism group is a $p$-group. Thus its multiplier $u$ has
$\gcd(u-1,p^a)=1$. For $p=2$, the whole automorphism group of
$C_{2^a}$ is a 2-group; the action of the odd-order group $H$ is trivial.
Hence the noncentral case has $p$ odd.

For $h\in L$, the coset $Ph$ contributes $(a+1)/\varphi(o(h))$ to
(5). For $h\notin L$, write $e=o(h)$ and let $u$ be its multiplier.
The identity
$(u-1)(1+u+\cdots+u^{e-1})=u^e-1=0\pmod{p^a}$ implies that every
element of $Ph$ has order exactly $e$. This coset contributes
$p^a/\varphi(e)$. Consequently the exact formula is

$$
c(G)=(a+1)c(H)+(p^a-a-1)(c(H)-c(L)).
\tag{12}
$$

The coefficient $p^a-a-1$ is positive here. Apply $c(H)\ge2^{r(H)}$
and Lemma 3 to the difference, then divide by $2^{r(H)+1}$ to obtain
(11). Equality occurs for $C_{p^a}\rtimes C_2$ with inversion, so this
bound cannot be increased for the stated class. $\square$

In particular, $\eta(G)\le K$ forces $p\le4K-2$ in the noncentral
case of Lemma 4.

## 5. Largest-prime induction

**Proof of Theorem A, prime assertion.** Induct on $|G|$, with $K$ fixed.
The trivial group is immediate. Let $p$ be the largest prime dividing
$|G|$. If $p\le B(K)$ there is nothing to prove. Otherwise $p$ is odd.
Its Sylow subgroup $P$ is cyclic: a noncyclic Sylow $p$-subgroup would
satisfy (7) with $a\ge2$, giving $p\le2K-2\le4K-2\le B(K)$.

Choose a minimal nontrivial normal subgroup $V\cong\mathbb F_q^d$ of
$G$. Lemma 2 gives $\eta(G/V)\le K$, so induction applies to $G/V$.

If $q=p$, cyclicity of $P$ implies $V\cong C_p$. If $p\nmid|G/V|$,
then $P=V$ is normal. Otherwise the Sylow $p$-subgroup of $G/V$ is
central by induction, and its full preimage is the Sylow subgroup $P$.
Again $P\unlhd G$.

Now suppose $q\ne p$. The image of $P$ in $G/V$ is central by
induction, so $VP\unlhd G$. We show that $P$ centralizes $V$.
If $d=1$, its action is trivial because
$|\operatorname{Aut}(C_q)|=q-1<p$. If $d\ge2$, a Sylow $q$-subgroup
contains $V$, and hence is neither cyclic nor generalized quaternion.
Writing $q^a\parallel|G|$, (7) and $a\ge d$ give
$q(d-1)\le2K-2$. Any prime divisor of

$$
|\mathrm{GL}_d(q)|=q^{d(d-1)/2}\prod_{i=1}^d(q^i-1)
\tag{13}
$$

is either $q$, a divisor of $q-1$, or a divisor of $q^i-1$ for an
allowed pair $(q,i)$ in (1). The first two possibilities are smaller
than $p$, and the last is at most $B(K)<p$. Thus $p$ does not divide
$|\operatorname{Aut}(V)|$, so the $p$-group $P$ acts trivially.

It follows that $VP=V\times P$. Its unique Sylow $p$-subgroup $P$ is
characteristic in $VP$, hence normal in $G$. This proves normality of
$P$ in every case. Lemma 4 now forces $P$ to be central, since a
noncentral $P$ would give $p\le4K-2\le B(K)$.

Finally split $G=P\times H$. If $|P|=p^a$, then
$\eta(H)=2\eta(G)/(a+1)\le K$. By induction all primes greater than
$B(K)$ in $H$ also have central cyclic Sylow subgroups; those subgroups
remain central in $G$. This completes the induction. $\square$

**Proof of Theorem A, order bound.** The product $C$ of the central cyclic
Sylow subgroups is a central cyclic normal Hall subgroup. Splitting gives
$G=C\times S$ with coprime orders. A central cyclic Sylow subgroup of
$S$ would also be one of $G$, contrary to the definition of $C$.
The prime assertion therefore bounds all prime divisors of $|S|$ by
$B(K)$. Coprime multiplicativity gives $\eta(S)\le\eta(G)\le K$;
equation (8) bounds every exponent in $|S|$ by $A(K)$. This is (3).
There are only finitely many group multiplication tables of orders
dividing the fixed integer $M(K)$, proving the finiteness assertion.
$\square$

## 6. Locally finite spectra

**Proof of Theorem B.** Apply (3). Both subgroup counts are multiplicative
on direct products of coprime orders, so

$$
(\eta(G),\lambda(G))=
\delta(C)(\eta(S),\lambda(S)),\qquad
\delta(C)=\prod_{p^{a_p}\parallel|C|}\frac{a_p+1}{2}.
\tag{14}
$$

For completeness, every subgroup of a coprime direct product is the
product of its projections: taking suitable powers by the Chinese
remainder theorem separates the two coordinates of every element in
the subgroup. Cyclicity is also preserved in both directions.

There are finitely many choices for $S$ by Theorem A. Each $a_p\le A(K)$
by (8). Factors with $a_p=1$ contribute 1. Each remaining factor is at
least $3/2$, and $\delta(C)\le\eta(G)\le K$ since $\eta(S)\ge1$.
Thus there are at most $\lfloor\log_{3/2}K\rfloor$ remaining factors,
each from the finite set $\{3/2,4/2,\ldots,(A(K)+1)/2\}$.
Only finitely many values of $\delta(C)$ can occur. Equation (14)
proves (4). If $\lambda(G)\le K$, then $\eta(G)\le K$, so local
finiteness for the total-subgroup spectrum follows as well. $\square$

## 7. The three questions in DDGS v2

Theorems 7.1 and 5.8 of
[Das–Dey–Galindo–Sharma v2](https://arxiv.org/html/2604.08040v2)
state that $\eta(G)<4$ and $\lambda(G)<59/8$, respectively, imply
solvability. We import these results only for the corollaries in this
section. Their simple-group estimates are not used in Theorems A or B.

Their fundamental blocks have no central cyclic Sylow subgroup.
Consequently Theorem A answers **Questions 9.1 and 6.1 affirmatively**.
Theorem B answers **both parts of Question 4.16 affirmatively**: only
finitely many normalized values occur in $2\le\eta(G)<4$ and in
$5/2\le\lambda(G)<59/8$.

The following explicit bounds may be useful for eventual classifications:

| Hypothesis on a fundamental block $S$ | Prime ceiling | Divisibility bound |
|---|---:|---|
| $\eta(S)<4$ | 13 | $|S|\mid(2\cdot3\cdot5\cdot7\cdot11\cdot13)^6$ |
| $\lambda(S)<59/8$ | 127 | $|S|\mid\left(\prod_{p\le127}p\right)^{13}$ |

To check these numbers, (1) gives $B(4)=13$ and $B(59/8)=127$.
For $K=4$, the possible pairs $(q,i)$ in the union are
$(2,2),(2,3),(2,4),(3,2),(3,3),(5,2)$; the largest prime produced is 13.
For $K=59/8$, the pairs are $q=2,2\le i\le7$;
$q=3,2\le i\le5$; $q=5,2\le i\le3$; and $(7,2),(11,2)$.
The maximum is $2^7-1=127$. The strict cyclic inequality improves (8)
to $a+1<8$, hence $a\le6$; the other bound gives $a\le13$.
All these small integer factorizations are printed by `verify.py`.

The prime ceiling 13 in the first row is sharp: the dihedral group
$D_{26}=C_{13}\rtimes C_2$ with inversion has $c(D_{26})=15$, so
$\eta(D_{26})=15/4<4$, and has no central cyclic Sylow subgroup.
No sharpness is claimed for the order bounds or the ceiling 127.

## 8. Scope of the evidence

The complete universal argument is above. The exact Python checks enumerate
cyclic subgroups literally, test normal-subgroup quotients and relative
deficits, verify (12) on cyclic prime-power kernels and several complements,
and recompute (1). They do not enumerate all groups in (2), independently
prove the imported results, or constitute peer review or formalization.
No complete list of fundamental blocks or of the attainable normalized
values is claimed. The result makes those classification tasks finite.

See [SOURCES.md](SOURCES.md) for the literature comparison and
[README.md](README.md) for reproduction instructions.
