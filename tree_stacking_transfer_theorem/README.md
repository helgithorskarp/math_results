# Exact tree stacking by transfer messages

## Results

Let (T) be a finite tree with at least two vertices.  A pebbling move removes
two pebbles from one vertex and places one on an adjacent vertex.  A
configuration is stackable if it can reach a configuration supported at one
vertex, and (operatorname{stack}(T)) is the least (t\geq 2) for which every
configuration of size (t) is stackable.

For (z\in V(T)), Csernák and Soukup define

\[
\sigma_T(z)=
\sum_{\substack{v=z\text{ or }\deg(v)>1}}
\deg(v)2^{d(z,v)}+1,
\qquad
E_T(z)=\sigma_T(z)+\operatorname{leaf}(z),
\]

where (operatorname{leaf}(z)) is the number of leaves different from (z),
and

\[
\operatorname{estim}(T)=\max_z E_T(z).
\]

This contribution proves their conjecture:

\[
\boxed{\operatorname{stack}(T)=\operatorname{estim}(T).}
\]

It proves two stronger results as part of the argument.

1. For a fixed configuration, stackability at **every** target is decided by
   one pair of integer messages per edge.  All messages and targets are
   computed in (O(|V(T)|)) integer operations.
2. If (|V(T)|\geq3), (r) is any nonleaf, and
   (|c|\geq\operatorname{estim}(T)), then (c) can be stacked at the
   prescribed vertex (r).  Thus the conjectured threshold works
   simultaneously for every nonleaf target.

The proof is exact and constructive.  No SAT/SMT solver, floating-point
decision, or unverified external certificate is used.

## 1. Exact branch transfers

Define

\[
g(s)=2s-3\max\left(1,\left\lceil\frac{s}{2}\right\rceil\right)
=
\begin{cases}
2s-3,&s\leq1,\\
s/2,&s\geq2\text{ even},\\
(s-3)/2,&s\geq3\text{ odd}.
\end{cases} \tag{1}
\]

For an oriented edge (x\to y), let (B_{x\to y}) be the component on the
(x)-side of (T-xy).  Its message (m_{x\to y}) is defined recursively,
starting at its terminal leaves.  If (c) is zero on this component, put
(m_{x\to y}=0).  Otherwise put

\[
m_{x\to y}
=g\!\left(c(x)+\sum_{w\sim x,\,w\ne y}m_{w\to x}\right). \tag{2}
\]

For a possible final target (r), define its root score

\[
q_r(c)=c(r)+\sum_{x\sim r}m_{x\to r}. \tag{3}
\]

### Transfer theorem

For every (r\in V(T)), the configuration (c) can be stacked at (r) if
and only if

\[
q_r(c)\geq1. \tag{4}
\]

Consequently (c) is stackable if and only if at least one root score is
positive.

### Proof of the transfer theorem

Temporarily attach the root (x) of a branch (B) to an external parent
(y).  A clearance of (B) leaves every vertex of (B) empty.  Its net
transfer is the final number of pebbles at (y) minus the initial number at
(y).

We prove by induction on (B) the following sharper interface statement.

* Every clearance of (B) has net transfer (delta\leq m_B) and
  (delta\equiv m_B\pmod3).
* If (y) initially has (n) pebbles and (n+m_B\geq1), a clearance
  attaining transfer (m_B) exists and ends with (n+m_B) pebbles at (y).
  Conversely, any clearance ending with a positive pile at (y) forces
  (n+m_B\geq1).

The empty branch has message zero and is immediate.  Suppose the branch is
nonempty.  Let (m_i) be its child messages and set

\[
s=c(x)+\sum_i m_i.
\]

For an arbitrary clearance, induction gives child transfers
(delta_i=m_i-3h_i), where (h_i\geq0).  If (u) moves go from (x) to
(y), and (z) go in the other direction, balance at (x) gives

\[
z=2u-a,
\qquad
\delta=u-2z=2a-3u,
\qquad
a=c(x)+\sum_i\delta_i=s-3\sum_i h_i. \tag{5}
\]

Because the branch starts nonempty and finishes empty, (u\geq1).  Also
(z\geq0), so (u\geq\lceil a/2\rceil).  Therefore

\[
\delta\leq g(a)\leq g(s),
\qquad
\delta\equiv g(s)\pmod3. \tag{6}
\]

The second inequality follows directly from the three cases in (1): moving
down by a nonnegative multiple of three never increases (g).  This proves
the upper bound and congruence.

For attainability, first clear the children with their maximal transfers.
Such child operations can be scheduled by doing positive transfers first,
zero transfers next, and negative transfers last.  A child of transfer (h)
is executable when the current pile plus (h) is at least one.  If the
desired pile after all child operations is at least one, the stated order has
enough pebbles at every step.

It remains to clear (x).  The four cases are explicit.

* If (s=2k\geq2), make (k) moves (x\to y).
* If (s=2k+1\geq3), first make (k) moves (x\to y), leaving one pebble at
  (x).  Then make (y\to x) and (x\to y).  The condition
  (n+g(s)=n+k-1\geq1) says exactly that (y) has the two pebbles needed for
  the reverse move after receiving the first (k).
* If (s=1), make (y\to x) and then (x\to y).  Here
  (n+g(1)\geq1) is exactly (n\geq2).
* If (s\leq0), first make (2-s) moves (y\to x).  The child clearances
  then leave two pebbles at (x), and one move (x\to y) finishes.  The
  required initial bank is
  (2(2-s)=1-g(s)), exactly the condition (n+g(s)\geq1).

This proves the branch interface.  At a target (r), process incident
branches in the same positive/zero/negative order.  They can all be cleared
if (q_r\geq1).  Conversely, in any sequence ending at (r), the actual
transfer of each incident branch is at most its message, so the positive final
pile is at most (q_r).  This proves (4).

All directed messages follow from one postorder and one preorder traversal,
which proves the linear-time claim.

## 2. Structural deficits and canonical obstructions

For each oriented edge define a positive odd structural deficit

\[
a_{x\to y}=
\begin{cases}
1,&x\text{ has no neighbor other than }y,\\
3+2\displaystyle\sum_{w\sim x,\,w\ne y}a_{w\to x},&\text{otherwise}.
\end{cases} \tag{7}
\]

Partitioning the degree/distance sum into the components at (z), or simply
inducting in (7), gives

\[
H(z):=\sum_{x\sim z}a_{x\to z}=\sigma_T(z)-1. \tag{8}
\]

For every vertex (z), define (kappa_z) by putting (H(z)) pebbles at
(z), one pebble at every graph leaf different from (z), and zero
elsewhere.  Then

\[
\|\kappa_z\|=H(z)+\operatorname{leaf}(z)=E_T(z)-1. \tag{9}
\]

Every root score of (kappa_z) is zero.  At (z), each incident branch not
containing the heavy pile has message (-a_{x\to z}), so (8) gives score zero.
Now move across an edge away from (z).  If the next vertex is a leaf, then
(a=1), (g(1)=-1), and its unit pebble is cancelled.  If it is internal,
write (a=3+2P), where (P) is the sum of the deficits in its forward
branches.  Equation (1) gives (g(a)=P), which is cancelled by their messages
of total (-P).  Induction away from (z) proves that every score is zero.
By the transfer theorem, (kappa_z) is non-stackable.

Choosing a vertex maximizing (E_T(z)) proves

\[
\operatorname{stack}(T)\geq\operatorname{estim}(T). \tag{10}
\]

## 3. Convex extremal bound for a prescribed nonleaf target

We next bound every configuration which cannot be stacked at a fixed nonleaf
(r).  The essential point is that the maximum mass of a branch, as a
function of its transfer budget, has a convex majorant.  Convexity forces all
available budget into a single branch and ultimately into a single heavy
vertex.

Consider a rooted branch (B).  Its terminal vertices are the graph leaves in
that component.  Let (a(B)) be given by (7), and let (ell(B)) be its number
of terminal leaves.  If its message is (m), then (m\geq-a(B)); call

\[
x=m+a(B)\geq0 \tag{11}
\]

its excess.  We recursively define a real-valued mass majorant (F_B(x)).
For a one-vertex branch,

\[
a(B)=\ell(B)=1,
\qquad F_B(x)=1+2x. \tag{12}
\]

For an internal branch with children (B_1,\ldots,B_d), put

\[
A=\sum_i a(B_i),
\quad L=\sum_i\ell(B_i),
\quad a(B)=3+2A,
\quad \ell(B)=L, \tag{13}
\]

and define the convex increasing change of variable

\[
b_a(x)=
\begin{cases}
x/2,&0\leq x\leq a-1,\\
2x-\dfrac{3(a-1)}2,&x\geq a-1.
\end{cases} \tag{14}
\]

Then set

\[
F_B(x)=L+\max\left(
b_a(x),
\max_i\bigl(F_{B_i}(b_a(x))-\ell(B_i)\bigr)
\right). \tag{15}
\]

Induction shows that (F_B) is convex and nondecreasing and that
(F_B(0)=\ell(B)).  Indeed, the functions
(F_{B_i}(x)-\ell(B_i)) are convex, nondecreasing, and zero at zero; their
maximum with (x) has the same properties, and composition with the convex
nondecreasing function (b_a) preserves them.

### Branch mass bound

Every configuration on (B) with excess (x) has norm at most (F_B(x)).

For the inductive step, let (x_i=m_i+a(B_i)) be the child excesses, let
(k=c(x_B)) be the pile at the branch root, and let (s=k+\sum_i m_i).
The total local budget is

\[
B_0=k+\sum_i x_i=s+A. \tag{16}
\]

If (m<0), then (s=(m+3)/2) and (11)--(14) give
(B_0=b_a(x)).  If (m\geq0), the preimages in (1) give
(s\leq2m+3), hence again (B_0\leq b_a(x)).

If (G) is convex, nondecreasing, and (G(0)=0), then

\[
G(u)+G(v)\leq G(u+v) \tag{17}
\]

for (u,v\geq0): convexity bounds (G(u)) and (G(v)) by their respective
fractions of (G(u+v)).  Apply this to the maximum of the identity function
and all child gains (F_{B_i}-\ell(B_i)).  Equations (15)--(17) show that
splitting (B_0) between the root pile and several children cannot beat
putting the whole budget into one place.  The inductive mass bound follows.

The bound is exact whenever (x\geq a(B)).  In that range
(b_a(x)\geq A+3>a(B_i)) for every child.  If the first term in (15) is
largest, place the whole budget at the branch root and put unit pebbles at all
terminal leaves.  If child (i) is largest, put its other child branches at
their minimum messages and use the inductively exact configuration in child
(i).  Thus an exact maximizer always has one heavy vertex, unit pebbles at
the other terminal leaves, and zero elsewhere.

### The fixed-target bound

Delete the fixed nonleaf target (r), obtaining branches (B_i).  Write

\[
a_i=a(B_i),\qquad \ell_i=\ell(B_i),\qquad
A=\sum_i a_i=H(r),\qquad L=\sum_i\ell_i.
\]

If (c) cannot be stacked at (r), then (3) gives

\[
c(r)+\sum_i(m_i+a_i)\leq A. \tag{18}
\]

The branch mass bound and (17) now imply

\[
\|c\|\leq
L+\max\left(A,\max_i(F_{B_i}(A)-\ell_i)\right). \tag{19}
\]

Because (r) has at least two branches, (A>a_i) for every (i), so all
terms in (19) are in the exact range.  The first term is the canonical
configuration (kappa_r).  Every child term is some (kappa_z) with
(z\in B_i).  One way to see the latter identification is to follow the
single branch receiving all excess.  If (p,v) are consecutive vertices on
that path, put

\[
O=\sum_{w\sim v,\,w\ne p}a_{w\to v},
\qquad
P=\sum_{u\sim p,\,u\ne v}a_{u\to p}.
\]

Then (a_{v\to p}=3+2O), (H(p)=a_{v\to p}+P), and direct substitution in
(14) gives

\[
b_{a_{v\to p}}(H(p))=3+O+2P=H(v). \tag{20}
\]

Thus the excess passed down the chosen path is always (H) at the current
vertex, and the final heavy pile is (H(z)=\sigma_T(z)-1).  Equations
(9), (19), and (20) prove

\[
\|c\|\leq\max_z(E_T(z)-1)=\operatorname{estim}(T)-1. \tag{21}
\]

Hence every configuration of size at least (operatorname{estim}(T)) stacks
at every prescribed nonleaf.  Together with (10), this proves the boxed
formula.  The two-vertex tree has no nonleaf; directly,
(operatorname{stack}(K_2)=3=\operatorname{estim}(K_2)).

## Reproducible implementation and checks

`tree_stackability.py` implements the two tree sweeps for all transfer
messages, all root scores, the structural deficits, the vertex estimates, and
the canonical obstructions.  It uses only the Python standard library.

`verify_transfer_theorem.py` contains an independent raw move-DAG oracle.  For
each configuration it recursively follows every legal first move and records
all final support vertices reachable by any move sequence.  A fresh run with
Python 3.11.2 and NetworkX 3.5 compared the oracle with the message theorem for
all 273,315 configurations of weights 1 through 10 on all 24 nonisomorphic
trees of orders 2 through 7.  It also checked:

* the structural-deficit formula against a separate distance/BFS evaluation;
* all 11,005 canonical configurations on the 986 nonisomorphic trees through
  order 12, including zero root scores and the exact claimed norms; and
* every configuration at the conjectured threshold on all six trees of
  orders 3 through 5, confirming stackability at every nonleaf in 66,504
  boundary cases.

The deterministic record hash was

```text
c27613e486d413a672e33a593e47914642314b933061db54d2412ad10cb3b7d2
```

Source hashes:

```text
tree_stackability.py          7511262d3b52aefeced1e78d589d36482104e67ba1968cac24542221f27e9d41
verify_transfer_theorem.py    65d5191570a8b6b7cc4d1cc4054493d25c5ae05416c69b52c7f0beb4c0730ef4
requirements.txt              d617f742c7feb29397a1f1e407db73a1d623b09b362c52e969f81358cfd167c5
```

Reproduce with:

```bash
python3 -m venv /scratch/tree-transfer-venv
/scratch/tree-transfer-venv/bin/pip install -r requirements.txt
/scratch/tree-transfer-venv/bin/python verify_transfer_theorem.py \
  --max-exact-order 7 \
  --max-exact-weight 10 \
  --max-structural-order 12 \
  --max-boundary-order 5
```

Run the linear-time analyzer, for example, with:

```bash
python3 tree_stackability.py \
  --edges 0-1,1-2,2-3,1-4 \
  --config 1,0,0,17,1
```

This prints zero at every target for the order-five canonical obstruction and
reports the tree estimate (20).

## Status, novelty, and trust boundary

The formula and fixed-target strengthening are proved mathematical results.
The finite checks corroborate the transfer theorem and extremal identities but
are not used to extrapolate the general theorem.  The hand proof uses exact
integer balance, congruence modulo three, and elementary convexity.  The
implementation trust boundary is the displayed Python source, Python integer
arithmetic, NetworkX's nonisomorphic-tree generator in the verifier, and the
runtime/hardware.

The primary source and its companion repository were refreshed through
2026-09-01.  The arXiv record still has only version 1; it states the tree
formula as a conjecture, proves the upper bound only under the Almost Stacked
Hypothesis, reports trees only through order seven, and explicitly asks about
efficient computation on trees.  Targeted searches and the refreshed
Discovery Net graph found no proof of the conjecture or exact per-configuration
tree transfer algorithm.  The results here are therefore apparently new to
the searched sources, not a literature-priority claim.

Primary source:

* T. Csernák and L. Soukup, *Stacking and clearing in graph pebbling*,
  arXiv:2604.22341v1 (2026), <https://arxiv.org/abs/2604.22341>.
* Authors' companion code, commit
  `701cdd93dd19869a9b90947edd6361efd81cfc1f`,
  <https://github.com/lajossoukup/pebbling>.

This result refines the earlier exact order-eight census, double-star theorem,
and universal lower bound in this repository.
