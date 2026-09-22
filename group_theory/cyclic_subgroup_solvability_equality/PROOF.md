# Equality at the cyclic-subgroup solvability threshold

Write $c(G)$ for the number of cyclic subgroups of a finite group,
including the trivial subgroup, and write $\omega(G)=\omega(|G|)$
for the number of distinct prime divisors of its order.

**Theorem.** For a finite **nonsolvable** group $G$,
$$
c(G)=2^{\omega(G)+2}
\quad\Longleftrightarrow\quad
G\cong A_5\times C_m,\qquad
m\text{ squarefree},\quad (m,30)=1.
\tag{1}
$$
The value $m=1$ is allowed. This does not classify solvable groups
with the same numerical value.

The lower bound $c(G)\ge 2^{\omega(G)+2}$ for nonsolvable groups is
already Theorem 7.1 of Das–Dey–Galindo–Sharma [DDGS]. Their Remark 7.2
already supplies the examples on the right of (1). The contribution
here is their necessity, with an equality argument for arbitrary
solvable radicals. The proof uses the simple-group estimates of [DDGS];
it is not a new proof of the classification of finite simple groups.

## 1. Counting facts and an exact extension formula

Partitioning a group by the generators of its cyclic subgroups gives
$$
c(X)=\sum_{x\in X}\frac1{\varphi(o(x))}.
\tag{2}
$$
Consequently
$$
c(X\times Y)\ge c(X)c(Y),
\tag{3}
$$
with equality when $(|X|,|Y|)=1$. Indeed
$\varphi(\operatorname{lcm}(a,b))\le\varphi(a)\varphi(b)$:
this is checked prime by prime, and is an equality for coprime $a,b$.
Apply this to (2). No necessity claim about equality in (3) is needed.

If $N\triangleleft X$, the map sending a cyclic subgroup to its
image in $X/N$ is onto. Its fiber over the trivial subgroup has
size $c(N)$. Therefore
$$
c(X)\ge c(X/N)+c(N)-1.
\tag{4}
$$
This is also Das–Sharma [DS], Lemma 2.3(2). In particular, a nontrivial
normal subgroup makes the quotient count strictly smaller.

**Extension lemma.** Let $V\cong(\mathbb F_p)^d$, $d\ge1$, and let
a finite group $H$ of order prime to $p$ act linearly on $V$.
For $h\in H$ put $f(h)=\dim_{\mathbb F_p}C_V(h)$. Then
$$
\begin{split}
c(V\rtimes H)
&=c(V)c(H)+
\frac{p-2}{p-1}
\sum_{h\in H}\frac{p^{d-f(h)}-1}{\varphi(o(h))},\\
c(V)&=1+\frac{p^d-1}{p-1}.
\end{split}
\tag{5}
$$
In particular $c(V\rtimes H)\ge c(V)c(H)$. For odd $p$,
equality holds precisely when the action is trivial. For $p=2$,
equality holds for **every** action.

To prove (5), let $h$ have order $e$, and let $T$ be its action.
As $p\nmid e$, the averaging map
$$
P=\frac1e\sum_{j=0}^{e-1}T^j
$$
is an idempotent with image $C_V(h)$. Thus
$$
(v,h)^e=(ePv,1).
$$
The order of $(v,h)$ is $e$ for the $p^{d-f(h)}$ vectors in
$\ker P$, and is $pe$ for all other vectors. The quotient order
ensures that no smaller order is possible. Since
$\varphi(pe)=(p-1)\varphi(e)$, the contribution of the coset $Vh$
to (2) is
$$
\frac{p^d+(p-2)p^{d-f(h)}}{(p-1)\varphi(e)}.
$$
Subtract $c(V)/\varphi(e)$ and sum over $h$. Every summand in the
defect is nonnegative. For odd $p$ it vanishes exactly when each
$f(h)=d$, proving the equality statement.

The characteristic-two exception is real:
$(C_2)^2\rtimes C_3\cong A_4$ with nontrivial action has
$c(A_4)=8=4\cdot2$.

Formula (5) also applies to any extension with elementary abelian
normal Hall subgroup $V$: such an extension splits. For completeness,
this special splitting statement follows by averaging a cocycle.
Choose a normalized section of the quotient $H$, with additive
cocycle $a(g,h)\in V$. Associativity gives
$$
a(g,h)+a(gh,k)=g\,a(h,k)+a(g,hk).
$$
Define $B(g)=|H|^{-1}\sum_{k\in H}a(g,k)$ in $V$. Summing gives
$$
a(g,h)=B(g)+gB(h)-B(gh).
$$
Changing the section by $-B(g)$ makes its cocycle zero, producing a
complement. This argument covers nonfaithful actions as well.

## 2. A general principle for equality

The following statement separates the elementary extension argument
from any particular simple-group estimate.

**Transfer theorem.** Fix a real constant $\kappa>1$. Suppose every
finite nonabelian simple group $S$ satisfies
$$
c(S)\ge\kappa\,2^{\omega(\operatorname{Aut}S)}.
\tag{6}
$$
Then every finite nonsolvable group $G$ satisfies
$$
c(G)\ge\kappa\,2^{\omega(G)}.
\tag{7}
$$
Moreover, equality in (7) holds exactly for
$$
G\cong S\times C_m,
\tag{8}
$$
where $S$ is nonabelian simple with
$c(S)=\kappa\,2^{\omega(S)}$, and $m$ is squarefree and coprime
to $|S|$.

For such an $S$, (6) automatically forces
$\omega(\operatorname{Aut}S)=\omega(S)$.

We prove the lower bound and its equality characterization together
by induction on $|G|$.

### Trivial solvable radical

Suppose first that $\operatorname{Rad}(G)=1$. Its socle has the form
$$
L=\prod_{i=1}^r S_i^{m_i},
$$
with pairwise nonisomorphic nonabelian simple $S_i$, and $m_i\ge1$.
The elementary socle facts used here are: a minimal normal subgroup
of a finite group is a direct power of a simple group; distinct minimal
normal subgroups commute; and an abelian minimal normal subgroup lies
in the solvable radical.

The centralizer $C_G(L)$ is trivial. Otherwise, as a nontrivial
normal subgroup, it contains a minimal normal subgroup $M$ of $G$.
Then $M\le L\cap C_G(L)$, so $M$ is abelian, a contradiction.
Conjugation therefore embeds $G$ in
$$
\operatorname{Aut}(L)\cong
\prod_{i=1}^r\bigl(\operatorname{Aut}(S_i)\wr\operatorname{Sym}(m_i)\bigr).
$$
Here automorphisms permute the isomorphic simple direct factors and
act individually on them; different isomorphism types cannot mix.

Set $a_i=\omega(\operatorname{Aut}S_i)$,
$b_i=\omega(m_i!)$, and $M=\sum_i m_i$. Then
$$
\omega(G)\le\sum_i(a_i+b_i),\qquad
b_i\le m_i-1,\qquad a_i\ge1.
$$
Hence $\sum_i m_i a_i\ge\omega(G)$, and (3), (6) give
$$
c(G)\ge c(L)\ge\prod_i c(S_i)^{m_i}
\ge\kappa^M2^{\sum_i m_i a_i}
\ge\kappa^M2^{\omega(G)}.
\tag{9}
$$
If $M\ge2$, this is strictly greater than the right side of (7).

Thus equality requires $L=S$ simple. If $G>S$, the subgroup
generated by any element outside $S$ is a further cyclic subgroup,
so
$$
c(G)>c(S)\ge\kappa2^{\omega(\operatorname{Aut}S)}
\ge\kappa2^{\omega(G)}.
$$
Equality therefore forces $G=S$, with the simple equality specified
in (8). The lower bound holds in all these cases.

### Nontrivial solvable radical

Let $N\le\operatorname{Rad}(G)$ be a minimal nontrivial normal
subgroup of $G$. Then $N\cong(\mathbb F_p)^d$.
The quotient $Q=G/N$ is nonsolvable, since an extension of solvable
groups is solvable.

If $p\mid|Q|$, then $\omega(Q)=\omega(G)$; (4) and induction give
$$
c(G)\ge c(Q)+c(N)-1
>\kappa2^{\omega(G)}.
\tag{10}
$$
Thus this case never gives equality.

If $p\nmid|Q|$, the splitting and extension lemma yield
$$
c(G)\ge c(N)c(Q)\ge2\kappa2^{\omega(Q)}
=\kappa2^{\omega(G)}.
\tag{11}
$$
Equality in (11) forces $c(N)=2$ and equality for $Q$.
Since $c((\mathbb F_p)^d)=1+(p^d-1)/(p-1)$, we have $d=1$.
Induction gives $Q\cong S\times C_m$ as in (8).

If $p$ is odd, equality in (5) forces the action on $N=C_p$
to be trivial. If $p=2$, $\operatorname{Aut}(C_2)=1$ gives the
same conclusion directly. Hence $G\cong C_p\times Q$.
The prime $p$ does not divide $|Q|$, so adjoining it preserves
squarefreeness and coprimality in (8). This proves necessity.

Conversely the coprime product formula and
$c(C_m)=2^{\omega(m)}$ for squarefree $m$ establish equality
for every group in (8). The induction is complete.

The hypothesis $\kappa>1$ is used in (9); no assertion at
$\kappa=1$ is made.

## 3. The simple-group input and its strictness

We now apply the transfer theorem with $\kappa=4$.
Theorem 7.3 of [DDGS] proves (6). The proofs in its Appendices B–E
also give
$$
c(S)>4\,2^{\omega(\operatorname{Aut}S)}
\quad\text{unless }S\cong A_5.
\tag{12}
$$
Strictness is not part of their stated Theorem 7.3, so the precise
reason for reading it from the proofs matters:

* **Alternating groups, Appendix B.** The $n=6$ count and the
  $7\le n\le21$ comparisons are strict. For $n\ge22$, the lower
  bound counts subgroups generated by prime cycles. The omitted trivial
  subgroup adds one even if a displayed numerical comparison is weak.
  The graph's earlier alternating-socle result also proves this
  strictness independently within that family.
* **$\operatorname{PSL}(2,q)$, Proposition C.2.** The infinite
  even and odd parameter estimates are strict. Its remaining even
  parameters are $4,8,16,32$, and its remaining odd parameters are
  $5,7,9,11,13,25,27$. The displayed comparisons are strict except
  for $q=4,5$, both isomorphic to $A_5$.
* **Other Lie types, Appendix D.** Each uniform lower bound comes
  from conjugates of a nontrivial cyclic subgroup generated by a regular
  semisimple element, through Lemma D.1. If $B$ denotes any subsequent
  numerical lower estimate of that conjugacy-orbit size, one has
  $c(S)\ge1+B$, since the trivial subgroup is outside the orbit.
  Their proofs establish $B\ge4\,2^{\omega(\operatorname{Aut}S)}$
  in the covered ranges. Thus these conclusions are strict. Small
  exceptional isomorphisms return to the preceding families.
* **Residual cases, Appendix E.** Every one of the twelve rows in
  Table 7 and the nine rows covering all 26 sporadic groups in Table 8
  has a lower bound strictly exceeding its comparison threshold.
  Their Proposition E.1 explicitly records this fact.

This is an audit of how equality behaves in the cited arguments,
not an independent verification of the underlying Lie theory or their
character-table computations. Those are external premises of (1).
The transfer theorem and extension formula do not depend on them.

Finally $A_5$ has 15 involutions, 20 elements of order 3, and 24
elements of order 5, so
$$
c(A_5)=1+15+\frac{20}{2}+\frac{24}{4}=32
=4\,2^{\omega(60)}.
$$
Its automorphism group has the same prime support. Equation (12)
and the transfer theorem prove (1).

## 4. Scope of the evidence

The universal conclusions come from the written arguments above,
with the specified external simple-group input. The accompanying exact
Python checks count literal cyclic subgroups of explicit finite groups,
compare them with element-order counts and (5), and test boundary
examples, nonfaithful actions, and the characteristic-two exception.
They do not enumerate all finite groups or independently certify CFSG,
the character-table library, or the uniform simple-group estimates.
No independent peer review or proof-assistant formalization is claimed.

## References

[DDGS] A. Das, H. K. Dey, C. Galindo, K. Sharma,
*Group Structure from Subgroup and Cyclic Subgroup Counts*,
[arXiv:2604.08040v2](https://arxiv.org/abs/2604.08040v2),
9 September 2026. Theorems 7.1 and 7.3, Remark 7.2, Section 8,
and Appendices B–E.

[DS] A. Das, K. Sharma,
*Solvability of Groups via Cyclic Subgroup Count*,
[arXiv:2604.23664](https://arxiv.org/abs/2604.23664),
Lemma 2.3 and Theorem A.
