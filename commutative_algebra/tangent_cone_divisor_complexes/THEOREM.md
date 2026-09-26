# Filtered divisor complexes for tangent-cone Betti numbers

Research note, 26 September 2026. Status: complete mathematical argument submitted
for review, with exact computational checks; not a claim of independent peer
verification or publication priority.

## 1. Statement and conventions

Let $S=\langle n_1<\cdots<n_e\rangle$ be a numerical semigroup with its minimal
generators, $k$ any field, and

$$
R=k[[t^S]],\qquad G=\operatorname{gr}_{\mathfrak m}R,
\qquad P=k[x_1,\ldots,x_e].
$$

The presentation $P\to G$ sends $x_v$ to the initial class of $t^{n_v}$.
Define the maximum factorization length

$$
\operatorname{ord}(a)=\max\left\{\sum_v c_v:
               a=\sum_v c_v n_v,\ c_v\in\mathbb N\right\}\quad(a\in S).
$$

In particular, $\operatorname{ord}(0)=0$. Membership in $S$ is required in
every expression involving this function; no order is assigned to a gap.
For $F\subseteq[e]$, put $n_F=\sum_{v\in F}n_v$. Define

$$
D_{s,j}=\{F\subseteq[e]:s-n_F\in S,
                    \operatorname{ord}(s-n_F)+|F|\ge j\}.
\tag{1}
$$

These are abstract simplicial complexes, possibly the void complex. The void
complex has no faces and zero augmented chain groups. It is distinct from
$\{\varnothing\}$, whose sole augmented chain group is $k$ in degree $-1$.
All homology below is augmented/reduced, including relative homology defined by
the quotient of augmented chain complexes. These conventions include $i=0$.

**Theorem.** Give $P$ the fine grading $\deg x_v=(n_v,1)$, and give the basis
class $u_a\in G$ the degree $(a,\operatorname{ord}(a))$. Then, for every
$i\ge0$, $s\in\mathbb Z$, and $j\in\mathbb Z$,

$$
\operatorname{Tor}_i^P(G,k)_{(s,j)}
\cong\widetilde H_{i-1}(D_{s,j},D_{s,j+1};k).
\tag{2}
$$

Consequently the usual graded Betti numbers, with $\deg x_v=1$, are

$$
\beta_{i,j}^P(G)=\sum_s
\dim_k\widetilde H_{i-1}(D_{s,j},D_{s,j+1};k).
\tag{3}
$$

Each summand can also be computed by the reduced homology of a single explicit
complex on at most $e+1$ vertices. Both the construction and the proof hold,
unchanged, for any positive affine semigroup $S\subseteq\mathbb N^d$, with $s$
and the $n_v$ interpreted as vectors and $R$ replaced by $k[S]$ when defining
the associated graded ring.

For the numerical case set

$$
m=n_1,\quad M=n_e,\quad B=(m-1)M,\quad
T=B+\sum_{v=2}^e n_v.
\tag{4}
$$

Every nonzero summand in (3) has $0\le s\le T$ and
$0\le j\le\lfloor s/m\rfloor$. Thus (3) is an explicitly finite algorithm.
This cutoff is a sufficient bound, not an optimality claim.

## 2. Proof of the homology formula

**Basis and multiplication.** The monomial $t^a$ belongs to $\mathfrak m^q$
exactly when $\operatorname{ord}(a)\ge q$. Hence $G$ has a $k$-basis
$\{u_a:a\in S\}$, with $u_a$ in degree $\operatorname{ord}(a)$, and

$$
u_a u_b=\begin{cases}
u_{a+b},&\operatorname{ord}(a+b)=\operatorname{ord}(a)+\operatorname{ord}(b),\\
0,&\operatorname{ord}(a+b)>\operatorname{ord}(a)+\operatorname{ord}(b).
\end{cases}
\tag{5}
$$

The inequality is always in this direction by concatenating maximal
factorizations. This also proves that the asserted fine grading is a ring
grading. Minimality of the generators gives $\operatorname{ord}(n_v)=1$.
For the complete local ring each graded quotient has the same monomial basis as
in the uncompleted semigroup ring, so completion changes none of these statements.

**The sets in (1) are complexes.** If $v\in F$, write $a=s-n_F$. Then

$$
\operatorname{ord}(a+n_v)+|F\setminus\{v\}|
\ge\operatorname{ord}(a)+1+|F|-1.
$$

Removing a vertex cannot decrease the value used in (1), and the new residual
remains in $S$. Thus $D_{s,j+1}\subseteq D_{s,j}$ are subcomplexes of the
ordinary squarefree-divisor complex of $s$.

**Koszul strands.** Compute $\operatorname{Tor}^P(G,k)$ using the Koszul complex
$K_\bullet(x_1,\ldots,x_e;G)$. Its component of homological degree $i$ and fine
degree $(s,j)$ has the basis

$$
u_{s-n_F}e_F,\quad |F|=i,\quad s-n_F\in S,\quad
\operatorname{ord}(s-n_F)+|F|=j.
\tag{6}
$$

These are exactly the faces of dimension $i-1$ in
$D_{s,j}\setminus D_{s,j+1}$. Orient faces by the order $1<\cdots<e$.
For the term obtained by removing $v$, the Koszul coefficient is multiplication
by $u_{n_v}$. By (5), it is 1 precisely when

$$
\operatorname{ord}(s-n_F+n_v)=\operatorname{ord}(s-n_F)+1.
$$

In this case the boundary face still has value $j$. Otherwise its value is
strictly greater than $j$, so it lies in $D_{s,j+1}$ and is zero in the relative
chain group. Both differentials have the same alternating sign. The assignment
$u_{s-n_F}e_F\mapsto F$ is therefore an isomorphism of chain complexes, shifted
by one. This proves (2). Forgetting the first component of the grading proves (3).
The same argument applies to a positive affine semigroup: positivity bounds
factorization lengths at any fixed element, and every step above is unchanged.

**A single absolute complex.** Write $D=D_{s,j}$ and $L=D_{s,j+1}$. If $L$
is void, put $C_{s,j}=D$. Otherwise adjoin a new vertex $v$ and put

$$
C_{s,j}=D\cup(v*L).
\tag{7}
$$

The cone $v*L$ is nonempty and has an acyclic augmented chain complex, even if
$L=\{\varnothing\}$. There is a short exact sequence

$$
0\longrightarrow\widetilde C_\bullet(v*L;k)
\longrightarrow\widetilde C_\bullet(C_{s,j};k)
\longrightarrow\widetilde C_\bullet(D,L;k)\longrightarrow0.
$$

The last quotient identifies each surviving face in $D\setminus L$ with itself.
It follows that $\widetilde H_q(C_{s,j};k)\cong\widetilde H_q(D,L;k)$ in every
degree, including $-1$. In particular the theorem answers the literal request
for homology of simplicial complexes, as well as providing the smaller relative
description.

## 3. Effective support bound

**Order stabilization.** If $a\in S$ and $a>B=(m-1)M$, then

$$
a-m\in S,\qquad \operatorname{ord}(a)=\operatorname{ord}(a-m)+1.
\tag{8}
$$

To prove this, consider a maximal-length factorization of $a$. If it contains
no $m$, every term is strictly greater than $m$. If it has at least $m$
terms, the first $m+1$ partial sums, including 0, have two equal residues modulo
$m$. The intervening nonempty block of $r\le m$ terms has sum $qm$ with
$q>r$. Replacing that block by $q$ copies of $m$ increases the factorization
length, a contradiction. Thus a maximal factorization containing no $m$ has
at most $m-1$ terms, and its value is at most $B$. For $a>B$, a maximal
factorization therefore contains $m$; removing it and using the reverse
concatenation inequality proves (8).

Now let $s>T$ and let $F\subseteq\{2,\ldots,e\}$. If $s-n_F\in S$, then
$s-n_F>B$, so (8) gives

$$
\operatorname{ord}(s-n_F)+|F|
=\operatorname{ord}(s-n_F-m)+|F|+1.
\tag{9}
$$

If $s-n_F\notin S$, neither is $s-n_F-m$. It follows that for every $j$,
membership of $F$ and $F\cup\{1\}$ in $D_{s,j}$ is equivalent. Thus each
nonvoid $D_{s,j}$ is a cone with apex 1. In the pair
$(D_{s,j},D_{s,j+1})$, both complexes are cones or void, so its augmented
relative homology is zero. Equivalently, adding vertex 1 contracts the relative
chain complex. This proves the bound on $s$.

For a surviving face $F$, (6) gives

$$
j=\operatorname{ord}(s-n_F)+|F|
\le (s-n_F)/m+|F|\le s/m.
$$

Also $s,j\ge0$. The special case $S=\mathbb N$, with $e=m=M=1$, has $T=0$
and only $\beta_{0,(0,0)}=1$, as required.

## 4. Relation to the classical formula and the open question

Problem 1 in [Moscariello–Sammartano, *Open problems on relations of numerical
semigroups*, arXiv:2406.00790v2](https://arxiv.org/html/2406.00790v2) asks for
simplicial descriptions of these Betti numbers. Equations (1)–(3), or the absolute
version (7), provide such a description without restrictions on $S$ or $k$.

The underlying homological method is classical. In particular, Proposition 1.1
of [Bruns–Herzog, *Semigroup rings and simplicial complexes*, 1997, pp. 186–187](https://www.home.uni-osnabrueck.de/wbruns/brunsw/pdf-article/SimpSemi.published.pdf)
computes Betti numbers of a monomial quotient of a positive affine semigroup ring
by relative squarefree-divisor homology. The following reduction explains precisely
how it applies here.

Let

$$
\widehat S=\langle(n_1,1),\ldots,(n_e,1)\rangle,\qquad
J=\langle X^{(a,\ell)}:(a,\ell)\in\widehat S,
                                  \ell<\operatorname{ord}(a)\rangle.
$$

The nonmaximal-length elements form a semigroup ideal: adding a factorization of
length $r$ preserves strict inequality because
$\operatorname{ord}(a+b)\ge\operatorname{ord}(a)+\operatorname{ord}(b)
\ge\operatorname{ord}(a)+r$. The monomial quotient therefore satisfies

$$
k[\widehat S]/J\cong G,
$$

by sending a maximal-length monomial to $u_a$ and every other monomial to zero.
This preserves the indicated presentation by the same $e$ polynomial variables.
The Bruns–Herzog divisor pair uses *attainability* of the length $j-|F|$, whereas
(1) uses only its comparison with the maximum length. These pairs can be different,
but their relative chain bases and their differentials are identical: in either
case precisely the maximal-length faces survive. Section 2 proves this directly
without relying on the reduction.

Thus the contribution is an explicit tangent-cone application of established
machinery, its maximum-length form, the absolute-complex formulation, and a
finite arithmetic cutoff. No new general theory of relative divisor complexes
is claimed. Targeted primary-source searches did not locate this exact application;
that is not a priority guarantee. The asserted answer to Problem 1 remains subject
to expert review of the argument and its match to the intended question.

## 5. A characteristic-independence consequence

**Corollary.** If $e\le4$, every fine and ordinary graded Betti number of $G$
is independent of the characteristic of $k$. This also holds for the positive
affine-semigroup version with at most four minimal generators.

Indeed, (7) uses at most five vertices, and every simplicial complex on at most
five vertices has torsion-free integral reduced homology. Here is an explanation
of the latter standard fact. After padding the ground set to five vertices,
integral [combinatorial Alexander duality](https://arxiv.org/abs/0710.1172) identifies
$\widetilde H_q(K;\mathbb Z)$, for $q\ge1$, with
$\widetilde H^{2-q}(K^*;\mathbb Z)$. Cohomology in degrees at most 1 is
torsion-free: in degree 1 this follows from the universal coefficient theorem
and the freeness of $H_0$; lower degrees are immediate. Degree 0 homology and
the augmented degree $-1$ are themselves free. Full, void, and empty-face-only
complexes satisfy the same conclusion directly. The universal coefficient theorem
now shows that all the dimensions in (2) are characteristic independent.
This is a consequence of classical topology and the formula, with no separate
novelty claim for the small-embedding-dimension conclusion.
It also follows directly from Bruns–Herzog, Corollary 1.4(a), through the
monomial-quotient presentation in Section 4.

The subsequent note [FIVE_GENERATORS.md](FIVE_GENERATORS.md) strengthens this to
five minimal generators. Its additional ingredient is an arithmetic obstruction
to the six-vertex projective plane, using factorizations supported on facets.

## 6. Checks and trust boundary

For $S=\langle6,7,15\rangle$, the standard-graded tangent-cone ideal is

$$
(xz,z^2,y^3z,y^6)\subset k[x,y,z].
$$

The total Betti numbers are $(1,4,4,1)$; the nonzero graded entries, besides
$\beta_{0,0}=1$, are

$$
\beta_{1,2}=2,\ \beta_{1,4}=\beta_{1,6}=1,\quad
\beta_{2,3}=\beta_{2,7}=1,\ \beta_{2,5}=2,\quad\beta_{3,6}=1.
$$

The last nonzero homological degree is 3, so this test includes a tangent cone
that is not Cohen–Macaulay. The code also checks a nonmonomial tangent-cone ideal,
that of $\langle6,7,10\rangle$, and examples of embedding dimensions 4, 5, and 6.
See README.md for the exact corpus, commands, and compact expected output.

The general theorem is proved by the chain identification and arithmetic argument,
not inferred from a finite computation. The Python implementation uses unbounded
integers, rational arithmetic, and exact prime-field arithmetic. The independent
check trusts Singular's elimination, local standard bases, and minimal-resolution
algorithms. Neither computational path is a proof-assistant formalization, and
agreement between two programs is not independent human peer review.
