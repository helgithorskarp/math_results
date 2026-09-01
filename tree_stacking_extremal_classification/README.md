# Complete classification of critical tree-stacking obstructions

## Result

Let $T$ be a finite tree with at least two vertices.  A pebbling move removes
two pebbles from one vertex and puts one on an adjacent vertex.  Write
$\operatorname{stack}(T)$ for the least $t\geq 2$ such that every
configuration of mass $t$ can be transformed to a configuration supported at
one vertex.

This note classifies **every** non-stackable configuration of the largest
possible mass $\operatorname{stack}(T)-1$.  The answer is a sibling-splitting
family: start from a canonical obstruction with one heavy leaf and one pebble
on every other leaf, then split the heavy leaf's even excess arbitrarily among
all leaves with the same neighbor.  There are no other critical obstructions.

This strengthens the earlier exact formula and transfer-message theorem.  It
also answers the classification question raised in the independent review of
that theorem and supplies the review's missing terminal-leaf calculation.

## Notation

For an oriented edge $x\to y$, let $a_{x\to y}$ be the odd structural deficit

$$
a_{x\to y}=
\begin{cases}
1,&x\text{ has no neighbor other than }y,\\
3+2\displaystyle\sum_{w\sim x,\,w\ne y}a_{w\to x},&\text{otherwise}.
\end{cases}
$$

Put

$$
H(v)=\sum_{x\sim v}a_{x\to v}=\sigma_T(v)-1
$$

and let $L$ be the set of graph leaves.  The vertex score in the
Csernák--Soukup expression is

$$
E(v)=H(v)+1+|L|-\mathbf 1_{v\in L}.
$$

The exact tree-stacking theorem gives

$$
M:=\operatorname{stack}(T)=\max_{v\in V(T)}E(v).
$$

Every nonleaf has a neighbor with strictly larger $E$-score, so the maximum is
attained at a leaf.

For a vertex $p$, write

$$
L_p=\{z\in L:z\sim p\},\qquad d_p=|L_p|,
$$

and define

$$
P^*=\{p:\text{some }z\in L_p\text{ satisfies }E(z)=M\}.
$$

All leaves in $L_p$ have the same value of $H$; denote it by $h_p$.  Indeed,
their incoming deficits are all $1$, so excluding any one of them from the
recurrence at $p$ gives the same sum.  Set

$$
X_p=\frac{h_p-1}{2}.
$$

For $|V(T)|\geq3$, the neighbor $p$ of a leaf is nonterminal and $h_p\geq3$,
so $X_p$ is a positive integer.

## Classification theorem

**Theorem.**  Suppose first that $|V(T)|\geq3$.  A configuration $c$ of mass
$M-1$ is non-stackable if and only if there are a vertex $p\in P^*$ and a weak
composition

$$
(x_z)_{z\in L_p}\in\mathbb Z_{\geq0}^{L_p},
\qquad
\sum_{z\in L_p}x_z=X_p,
$$

such that

$$
c(v)=
\begin{cases}
1+2x_v,&v\in L_p,\\
1,&v\in L\setminus L_p,\\
0,&v\notin L.
\end{cases} \tag{1}
$$

Every target score of every configuration in (1) is exactly zero.  For
$T=K_2$, the unique critical obstruction is $(1,1)$.

Consequently, when $|V(T)|\geq3$, the exact number of critical obstructions is

$$
N(T)=\sum_{p\in P^*}
\binom{X_p+d_p-1}{d_p-1}. \tag{2}
$$

### Construction and zero scores

The exact branch transfer for a nonempty branch of effective input $s$ is

$$
g(s)=
\begin{cases}
2s-3,&s\leq1,\\
s/2,&s\geq2\text{ even},\\
(s-3)/2,&s\geq3\text{ odd}.
\end{cases} \tag{3}
$$

Fix $p\in P^*$ and $z\in L_p$.  The canonical configuration $\kappa_z$ has
$h_p$ pebbles at $z$, one at every other leaf, and zero at every nonleaf.  Its
mass is $E(z)-1=M-1$, and the transfer theorem gives score zero at every
target.

Write $h_p=1+2X_p$.  A leaf in (1) sends the message

$$
g(1+2x)=x-1, \tag{4}
$$

where (4) also holds at $x=0$.  Therefore the aggregate message from the leaf
children $L_p$ into $p$ is

$$
\sum_{z\in L_p}(x_z-1)=X_p-d_p,
$$

exactly the same as for $\kappa_z$.  Every message and every score outside
$L_p$ is consequently unchanged, including the zero score at $p$.

For a particular leaf $z\in L_p$, the effective input on the complementary
side of $pz$ is the negative of its message, namely $1-x_z$.  Since this is at
most $1$, (3) gives

$$
m_{p\to z}=g(1-x_z)=-1-2x_z.
$$

Thus its leaf score is

$$
(1+2x_z)+(-1-2x_z)=0.
$$

All scores are zero, so (1) is non-stackable.  Its mass is

$$
|L|+2X_p=|L|+h_p-1=E(z)-1=M-1.
$$

### Equality rigidity

It remains to show that the construction is exhaustive.  We record the
equality case of the convex argument in the exact tree-stacking theorem.

For a rooted branch $B$, let $a(B)$ be its structural deficit, $\ell(B)$ its
number of terminal leaves, $m$ its transfer, and $x=m+a(B)\geq0$ its transfer
excess.  The sharp branch mass majorant is $F_B(x)$.  For a terminal branch,

$$
F_B(x)=1+2x. \tag{5}
$$

For an internal branch with children $B_i$, put

$$
A=\sum_i a(B_i),\quad a=3+2A,\quad L=\sum_i\ell(B_i),
$$

$$
b_a(x)=
\begin{cases}
x/2,&0\leq x\leq a-1,\\
2x-3(a-1)/2,&x\geq a-1,
\end{cases}
$$

and

$$
F_B(x)=L+\max\left(b_a(x),
\max_i(F_{B_i}(b_a(x))-\ell(B_i))\right). \tag{6}
$$

Set $G_B=F_B-\ell(B)$ and include the root-pile function $G_0(x)=x$.
Every $G$ in this family is convex and nondecreasing and satisfies $G(0)=0$.
In fact these functions are strictly increasing.  Thus, at equality in the
fixed-target mass bound, no branch mass bound can be slack and the excess
allocations use the entire available budget $H(r)$; equivalently, the target
score is zero.
For any such functions $G_i$ and nonnegative allocations with
$\sum_i x_i=A_0$,

$$
\sum_iG_i(x_i)\leq\max_iG_i(A_0). \tag{7}
$$

To see both the inequality and its rigidity, convexity gives

$$
G_i(x_i)\leq\frac{x_i}{A_0}G_i(A_0).
$$

If two allocations are positive, equality in (7) requires both corresponding
functions to be affine from $0$ through $A_0$ and to have the same endpoint
value.

There are only two ways this affine equality can occur in the tree recursion:

1. $G_0(x)=x$ is affine, but it cannot attain the global boundary because an
   internal target has $E$-score strictly below the maximizing leaf score.
2. A terminal branch has $G_B(x)=2x$, affine for all $x$.  An internal branch
   is not affine through a boundary budget: in (6), $b_a$ has a genuine slope
   increase from $1/2$ to $2$ at $a-1$, and the budget entering a nonterminal
   child is at least $a+1$.  The outer maximum in (6) is nondecreasing with
   positive secant slope, so this breakpoint cannot disappear.

For completeness, the budget assertion follows directly along an extremizing
path.  If the path moves from an internal $p$ into a nonterminal neighbor $v$,
write

$$
a_{v\to p}=3+2O,qquad
P=\sum_{w\sim p,\,w\ne v}a_{w\to p}.
$$

Here $P\geq1$, the incoming budget is
$H(p)=a_{v\to p}+P>a_{v\to p}-1$, and the second branch of $b_a$ gives

$$
b_{a_{v\to p}}(H(p))
=3+O+2P
=H(v). \tag{8}
$$

The last equality uses $a_{p\to v}=3+2P$.  Thus the same equality analysis
restarts at $v$.

Equation (7) now forces all positive excess into one nonterminal child at each
step.  The process eventually reaches a vertex $p$ where a terminal child is
chosen.  At that final step, and only there, excess may split: every terminal
child has the identical affine function $2x$, so it may be distributed
arbitrarily among all leaves in $L_p$.

This also repairs the terminal case omitted from the first proof of the exact
formula.  If $v$ is a leaf child of $p$, put

$$
P=\sum_{w\sim p,\,w\ne v}a_{w\to p}.
$$

Then $H(p)=1+P$, and (5) turns the final budget into the leaf pile

$$
1+2H(p)=3+2P=a_{p\to v}=H(v). \tag{9}
$$

Hence the endpoint is precisely a canonical heavy leaf, with its excess
allowed to split among its siblings.

Branches receiving zero excess attain $F_B(0)=\ell(B)$ in only one way: one
pebble at every terminal leaf and zero at every internal vertex.  This follows
inductively from (5)--(6).  A terminal branch receiving excess $x$ attains
(5) only with the pile $1+2x$.  Therefore equality forces exactly the form
(1).  Tracking (8)--(9) shows that the chosen endpoint leaf satisfies
$E(z)=M$, so $p\in P^*$.  This proves the converse.

Finally, the leaf sets $L_p$ for distinct parents are disjoint, and $X_p>0$.
The families for distinct $p$ are therefore disjoint.  Stars-and-bars gives
(2).

## Consequences and examples

### Paths

For $P_2$, the unique obstruction is $(1,1)$.  For $P_3$, the two maximizing
leaves are siblings and $X=2$, giving exactly

$$
(1,0,5),\quad(3,0,3),\quad(5,0,1).
$$

For every $n\geq4$, the maximizing endpoints have different parents and no
leaf siblings.  Hence the only critical obstructions on $P_n$ are

$$
(2^n-3,0,\ldots,0,1)
\quad\text{and its reversal}.
$$

### Stars

For the star $K_{1,m}$, all $m$ leaves are siblings,
$h=2m+1$, and $X=m$.  Its critical obstructions are exactly the positive odd
leaf configurations of total mass $3m$, with zero at the center.  Their number
is

$$
N(K_{1,m})=\binom{2m-1}{m-1}.
$$

Thus a star can have exponentially many critical obstructions even though the
earlier canonical construction displayed only $m$ of them.

## Reproducibility

The standard-library module `tree_extremizers.py` implements the exact
transfer scores, deficits, formula (2), and the classified generator.  The
checker `verify_extremizers.py` uses NetworkX 3.5 only to generate
nonisomorphic trees.  Run from this directory with Python 3.11 or newer:

```bash
python3 -m venv /scratch/tree-extremizers-venv
/scratch/tree-extremizers-venv/bin/pip install -r requirements.txt
PYTHONDONTWRITEBYTECODE=1 \
  /scratch/tree-extremizers-venv/bin/python verify_extremizers.py
```

A fresh run checked:

- all 10,491 classified configurations on all 94 nonisomorphic trees through
  order $9$, verifying mass $M-1$ and score zero at every target;
- all 239,094 positive-odd leaf configurations at mass $M-1$ on all 47 trees
  through order $8$, finding exactly the 2,816 classified configurations;
- all 57,982 unrestricted configurations at mass $M-1$ on all seven trees
  through order $5$, finding exactly the 54 classified configurations; and
- those 54 small-tree obstructions with an independent raw move-DAG oracle,
  which explored 1,588 states and found no reachable stacked target.

The deterministic record hash was

```text
f75c6f101b9890ebf78a1570168875531ad80e8fd287d6c6b066a17f881756e7
```

Source hashes for the checked run are

```text
tree_extremizers.py    c402372b6f4075abbf97a019752773e649e63c14bf8f5c90e60a12e6fdbe823f
verify_extremizers.py  3e31a1cf2ed8c96af72919f990b4f1a0a64a5ecc9768a7c7b0799bd7fa1d6f3a
requirements.txt       d617f742c7feb29397a1f1e407db73a1d623b09b362c52e969f81358cfd167c5
```

The first three checks use the exact transfer theorem at the decision layer;
the raw move-DAG check does not.  Finite computation corroborates the equality
analysis but is not an extrapolative proof of the universal classification.

## Status, novelty, and scope

This is a proved classification theorem conditional only on the already
proved exact transfer interface and convex branch majorant.  It is not a
heuristic classification from small cases.  The primary paper of Csernák and
Soukup conjectures the value of $\operatorname{stack}(T)$ and constructs
special path obstructions, but does not classify critical configurations on
trees.  The earlier transfer theorem proves the value and constructs one
canonical obstruction per vertex; its independent review explicitly leaves
classification of all maximum-mass obstructions as an open strengthening.
Targeted searches through 2026-09-01 found no other classification.  The
result is therefore apparently new to the searched sources, not a literature
priority claim.

Primary source:

- T. Csernák and L. Soukup, *Stacking and clearing in graph pebbling*,
  arXiv:2604.22341v1 (2026), <https://arxiv.org/abs/2604.22341>.
