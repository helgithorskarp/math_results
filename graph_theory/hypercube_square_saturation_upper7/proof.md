# A construction with asymptotic upper constant seven

For the cube graph $Q_n$, call a spanning subgraph **square-saturated** if
it contains no four-cycle and adding any missing cube edge creates one.
Every four-cycle of a cube is a two-dimensional face.

We give a self-contained proof of

$$
\limsup_{n\to\infty}\frac{\operatorname{sat}(Q_n,Q_2)}{2^n}\le7,
\qquad
\liminf_{n\to\infty}\frac{\operatorname{sat}(Q_n,Q_2)}{2^n}\le\frac{11}{2}.
$$

The construction adapts the parity construction of Johnson and Pinto,
Section 4.2, with a smaller second dominating set and unequal block lengths.
The proof below includes all saturation cases; it does not import a
computer-generated classification or a solver's infeasibility claim.

## 1. A finite syndrome template

Let $q=2^t$, $t\ge2$, and let $V=\mathbb F_2^t$.
Choose independent vectors $a,b$, put $c=a+b$, and choose a linear functional
$\chi:V\to\mathbb F_2$ with $\chi(a)=\chi(b)=1$.
Let $W=V\setminus\{0,a,b,c\}$. Define a graph $R$ on $V$ with edges

1. $0v$ for every $v\ne0$;
2. $ac$;
3. $aw$ for $w\in W$ with $\chi(w)=0$, and $bw$ for $w\in W$ with $\chi(w)=1$.

Thus $|E(R)|=(q-1)+1+(q-4)=2q-4$.
Put $C_0=\{0\}$, $D_0=\{a,b\}$, and $A_0=C_0\cup D_0$.
Both $C_0$ and $D_0$ are independent dominating sets of $R$; every edge
of $R$ has an endpoint in $A_0$.

An **affine square** means a four-cycle whose four distinct vertices sum
to zero. The graph $R$ contains no affine square. Indeed, $A_0$ is a vertex
cover. A four-cycle with three vertices in $A_0$ would require an outside
vertex adjacent to both $a$ and $b$, and none exists. A four-cycle with
exactly two vertices in $A_0$ must have them opposite. The pair $a,b$ has
no common outside neighbor. For the pair $0,a$, the common outside
neighbors are $c$ and the points of $W$ with $\chi=0$.
An affine square would require two such neighbors differing by $a$.
Translation by $a$ changes $\chi$, while $c+a=b$ belongs to $A_0$.
This is impossible. For $0,b$, the same argument applies to the common
outside neighbors in $W$ with $\chi=1$.

Moreover, every missing edge incident to $A_0$ completes an affine square:

- for $ab$, use the existing path $a,c,0,b$;
- for $bc$, use $b,0,a,c$;
- for a missing $aw$, necessarily $w\in W$ and $\chi(w)=1$;
  use $a,w+a,0,w$;
- for a missing $bw$, necessarily $w\in W$ and $\chi(w)=0$;
  use $b,w+b,0,w$.

These are all missing edges incident to $A_0$.

## 2. Lifting the template to a Hamming block

Let $\ell=q-1$. Index the coordinates of $Q_\ell$ by the nonzero vectors
of $V$, and define the syndrome

$$\sigma(x)=\sum_{v\in V\setminus\{0\}}x_vv.$$

Include a cube edge $xy$ in $H_\ell$ exactly when
$\sigma(x)\sigma(y)\in E(R)$. Put

$$C_\ell=\sigma^{-1}(C_0),\qquad
D_\ell=\sigma^{-1}(D_0),\qquad A_\ell=C_\ell\cup D_\ell.$$

The syndrome is surjective. Each fiber has size $2^\ell/q$, and each
unordered pair of distinct syndromes corresponds to exactly $2^\ell/q$
cube edges, in the coordinate indexed by their difference. Consequently,

$$
|C_\ell|=\frac{2^\ell}{q},\quad
|D_\ell|=\frac{2\cdot2^\ell}{q},\quad
|A_\ell|=\frac{3\cdot2^\ell}{q},\quad
e(H_\ell)=\left(2-\frac4q\right)2^\ell.
$$

The sets $C_\ell,D_\ell$ are disjoint independent dominating sets in
$H_\ell$, and $A_\ell$ covers its edges. Every cube square projects to an
affine square with distinct vertices: its two coordinate labels are
distinct nonzero vectors and hence independent over $\mathbb F_2$.
Therefore $H_\ell$ is square-free.

The four explicit paths in Section 1 lift through any cube edge with the
corresponding syndrome pair. To see this, if that edge is in coordinate
$k$, an affine square witness supplies a second nonzero label $j\ne k$;
the face in coordinates $j,k$ through the edge has precisely those four
syndromes. Thus every missing cube edge with an endpoint in $A_\ell$ has
a square witness in $H_\ell$. No saturation claim is needed for missing
edges with both endpoints outside $A_\ell$.

## 3. Two blocks and a small exceptional set

Take powers of two $p,q\ge4$ and write

$$n=(p-1)+(q-1)+r,\qquad r\ge0.$$

Use coordinate blocks $I,J,K$ of lengths $p-1,q-1,r$ and write a vertex
as $(x,y,z)$. Use the graphs and sets of Section 2 in the first two blocks,
with subscripts $I,J$. The third block may be empty.

Construct an initial graph by the following union of edges:

1. Every copy of $H_I$ along block $I$, and every copy of $H_J$ along block $J$.
2. For a fixed $x\in C_I$, edges in the complementary coordinates $J\cup K$
   whose lower endpoint in those coordinates has even Hamming weight;
   for $x\in D_I$, use odd lower weight instead.
3. Apply the preceding rule with $I,x$ and $J,y$ exchanged.

Here the lower endpoint of an edge is the endpoint with zero in its changing
coordinate. Delete every edge incident to

$$B=A_I\times A_J\times\{0,1\}^r.$$

Call the remaining graph $G$. Its exceptional set has size

$$|B|=\frac{9\cdot2^n}{pq}.$$

### Square-freeness

Every edge of $G$ has an endpoint whose $I$-part is in $A_I$ or whose
$J$-part is in $A_J$. Suppose a square exists and choose, after exchanging
the blocks if necessary, a vertex whose $I$-part is in $A_I$.
No vertex of that square can have its $J$-part in $A_J$: if a free
coordinate changes that part, the square also contains the corresponding
vertex with the original $I$-part, which would be in $B$ and incident to
no edge. If no coordinate changes that part, the conclusion is immediate.

Count the square's free coordinates in $I$.
With two, its edges lie in $H_I$, which is square-free.
With zero, its edges would all lie in a single parity class of edges of
the complementary cube. Each square has two edges of each lower-weight
parity, so it cannot be complete.
With one, the two complementary edges require both $I$-parts to be in
$A_I$. They have the same lower-weight parity outside $I$, so both
$I$-parts must lie in $C_I$ or both in $D_I$.
The two $I$-edges would then be edges of $H_I$ within one of these
independent sets, a contradiction.

### Saturation away from the exceptional set

Consider a missing edge whose endpoints avoid $B$.
First suppose its changing coordinate is in $I$; the case of $J$ is symmetric.

If $y\notin A_J$ and an endpoint's $I$-part belongs to $A_I$, the boundary
witness from Section 2, in the fixed $y,z$ layer, saturates it. None of
that witness's edges was deleted.

If $y\notin A_J$ and both $I$-parts avoid $A_I$, let $\epsilon$ be the
lower endpoint's Hamming weight outside $J$, reduced modulo two.
Choose an $H_J$-neighbor of $y$ in $C_J$ when $\epsilon=0$, or in $D_J$
when $\epsilon=1$. Domination provides this neighbor. The two copies of
that $H_J$-edge and the parity edge in the neighboring layer give a square
witness; both $I$-parts avoid $A_I$, so it avoids $B$.

If $y\in A_J$, both $I$-parts must avoid $A_I$. The missing edge has
the wrong parity for the class $C_J$ or $D_J$ containing $y$.
Choose an $H_J$-neighbor of $y$ in the other class, which exists by
domination. That class uses the opposite parity, so the edge is present
there. Again the two copies of the $H_J$-edge complete a witness avoiding $B$.

Finally suppose the changing coordinate is in $K$.
If $x\in A_I$ or $y\in A_J$, exactly one of these holds. A missing
edge has the wrong parity for that fixed part, and a neighbor in its
other dominating class supplies a witness just as above.
If both fixed parts avoid their respective $A$ sets, choose a neighbor
of $x$ in $C_I$ or $D_I$ matching the edge's lower parity outside $I$.
The resulting witness has $y\notin A_J$, so it also avoids $B$.

This exhausts all missing edges away from $B$.

### Deterministic completion

Process the cube edges incident to $B$ in lexicographic order. Add an edge
if adding it would not create a square. Square-freeness is preserved.
Every rejected edge has a square witness at rejection, which remains
after later additions; every initially saturated edge also keeps its
witness. The final graph is square-saturated, with at most $n|B|$ added
edges. This is a finite, deterministic construction.

## 4. Counting and choice of lengths

All counts in this section are upper bounds before deletion, so overlaps
between the edge rules can only help. The two sets of internal edges cost

$$2^n\left(4-\frac4p-\frac4q\right).$$

In a cube of dimension at least two, precisely half the edges in each
coordinate have even lower weight. The complementary dimensions here
are at least three. The parity edges therefore cost at most

$$\frac34\,2^n\left(\frac{n-p+1}{p}+\frac{n-q+1}{q}\right).$$

After completion, the resulting graph has at most $2^n F(n;p,q)$ edges,
where the exact rational coefficient is

$$
\boxed{F(n;p,q)=\frac52+\frac{3n-13}{4}
       \left(\frac1p+\frac1q\right)+\frac{9n}{pq}.}
$$

For every $n\ge6$, let $q$ be the largest power of two with $2q\le n+2$.
Use $p=q$ if $n+2<3q$, and $p=2q$ otherwise. These choices satisfy
$p+q-2\le n$, so the construction applies.

For fixed $p,q$, $F$ increases with $n$. In the first case $n\le3q-3$, and

$$F(n;q,q)\le7+\frac{16}{q}-\frac{27}{q^2}.$$

In the second case $n\le4q-3$, and

$$F(n;2q,q)\le7+\frac{39}{4q}-\frac{27}{2q^2}.$$

Since $q\to\infty$, this proves the limsup bound seven. It also gives the
explicit, deliberately nonoptimal uniform estimate

$$\operatorname{sat}(Q_n,Q_2)<\left(7+\frac{48}{n+2}\right)2^n
\quad(n\ge6).$$

Indeed, in the first case $n+2<3q$, so $16/q<48/(n+2)$;
in the second $n+2<4q$, so $39/(4q)<48/(n+2)$.

On the subsequence $n=2q-2$ with $p=q$,

$$F(2q-2;q,q)=\frac{11}{2}+\frac{17}{2q}-\frac{18}{q^2},$$

which proves the stated liminf bound. Neither a matching lower bound nor
convergence of the normalized saturation number is claimed.

## Scope and validation

This is a complete proof attempt, pending independent review. The universal
claim rests on the written construction and proof, including the syndrome
lifting argument and all parity cases. `verify_template.py` checks finite
quotients and exact rational arithmetic. `construct.py` expands small cubes;
`verify.py` independently checks their edge lists using adjacency and
three-edge paths. Finite checks do not prove the universal quantifiers.
No SAT result, floating-point calculation, or external classification is
an assumption of the theorem. No formal proof-assistant check is claimed.

Reference: J. R. Johnson and T. Pinto, *Saturated Subgraphs of the Hypercube*,
Combinatorics, Probability and Computing 26 (2017), 52–67,
[arXiv:1406.1766](https://arxiv.org/abs/1406.1766), Section 4.2.
