# Global tree-stacking critical multiplicity through order 22

## Results

For a finite tree $T$, let $N(T)$ be the number of non-stackable pebbling
configurations of maximum possible mass $\operatorname{stack}(T)-1$.  The
sibling-leaf classification gives

$$
N(T)=\sum_{p\in P^*}\binom{X_p+d_p-1}{d_p-1},
$$

where $P^*$ is the set of parents of maximum-score leaves, $d_p$ is the
number of leaf neighbors of $p$, and $X_p$ is their common excess.

This artifact proves a core-endpoint reduction, gives a linear-time rerooting
evaluator for $N(T)$, and extends the exact global census from order 19
through order 22.

### Core-endpoint theorem

**Theorem.** In a nonstar tree, the parent of every maximum-score leaf has
exactly one nonleaf neighbor. Equivalently, every maximizing sibling class is
attached at a leaf of the tree's nonleaf core.

Let $z$ be a maximum-score leaf with parent $p$. Suppose that $p$ has
$k\ge2$ nonleaf-neighbor components $C_1,\ldots,C_k$, and put

$$
R_i=\sum_{\substack{v\in C_i\\ \deg(v)>1}}
\deg(v)2^{d(p,v)}.
$$

Then

$$
X(z)=\deg(p)+\sum_iR_i.
$$

Choose $i$ with $R_i\le\sum_{j\ne i}R_j$, and choose any graph leaf $w$ in
$C_i$. If $L=d(p,w)\ge2$, the contributions to $X(w)$ from $p$ and the
components other than $C_i$ alone give

$$
X(w)\ge2^{L-1}\left(\deg(p)+\sum_{j\ne i}R_j\right)
\ge2\left(\deg(p)+\sum_{j\ne i}R_j\right)>X(z),
$$

a contradiction. Thus $k\le1$. In a connected nonstar tree $k=0$ is
impossible, proving the theorem.

If $C$ is the nonleaf core and $r_v$ is the number of graph leaves attached
to $v\in C$, the theorem reduces all candidate maximizing classes to the
leaves of $C$, with exact score

$$
X_v=\sum_{u\in C}(\deg_C(u)+r_u)2^{d_C(u,v)}.
$$

### Linear-time exact evaluator

Put $w(v)=\deg_T(v)$ at nonleaves and $w(v)=0$ at leaves, and define

$$
F(v)=\sum_x w(x)2^{d(v,x)}.
$$

Root $T$ arbitrarily. For a child $c$, let

$$
D(c)=\sum_{x\text{ in the }c\text{-subtree}}w(x)2^{d(c,x)}.
$$

A postorder pass computes every $D(c)$. If $p$ is the parent of $c$, splitting
the potential into the $c$-subtree and its complement gives

$$
\boxed{F(c)=2F(p)-3D(c).}
$$

A preorder pass therefore computes all $F(v)$ in $O(|V(T)|)$ exact integer
operations. For a graph leaf $z$, $X(z)=F(z)/2$. Grouping the maximizing
leaves by parent and applying the sibling-class binomial formula then gives
$N(T)$ in linear time (apart from big-integer output cost).

### Exact global census

The complete census gives a unique global maximizer at each new order:

| order | unlabeled trees checked | unique maximizer | exact $N(T)$ |
|---:|---:|:---:|---:|
| 20 | 823,065 | $B(6,6,7)$ | 34,704,830,468,464 |
| 21 | 2,144,505 | $B(6,6,8)$ | 1,096,246,556,385,904 |
| 22 | 5,623,756 | $B(6,6,9)$ | 34,852,713,682,289,776 |

Here $B(d,e,\ell)$ joins two hubs by an $\ell$-edge path and attaches $d$
and $e$ leaves at its ends. Together with the prior census, the global
maximizer is the star through order 14 and a unique symmetric double broom at
every order from 15 through 22. This is finite evidence, not a proof for all
orders.

## A sharp warning for a proposed asymptotic route

A tempting strengthening of the core-endpoint theorem is the following. If a
maximizing parent has $d$ leaf neighbors and internal height $h$, perhaps

$$
h\le n-2d-1. \tag{H}
$$

Inequality (H) would immediately extend the sharp caterpillar exponent
$\log_2 M_n=n^2/8+O(n\log n)$ to all trees. It holds for every tree through
order 21, but is false at order 22. The census finds exactly one violating
unlabeled tree at that order.

Its maximizing hub $p$ has eight leaf neighbors. Join $p$ by a path of five
edges to a vertex $q$, and attach four disjoint two-edge arms to $q$. Then
$n=22$, the internal height from $p$ is $h=6$, while $n-2d-1=5$. The eight
leaves at $p$ have excess 741; the four opposite leaves have excess 732.
Thus the eight-leaf class is genuinely maximizing and

$$
N(T)=\binom{748}{7}=25{,}272{,}745{,}154{,}211{,}192.
$$

This does not challenge the symmetric-double-broom extremal conjecture: its
count is below
$N(B(6,6,9))=34{,}852{,}713{,}682{,}289{,}776$. It shows that a proof of the
global $1/8$ exponent cannot rely on (H) without an additional near-extremal
or multiplicity-sensitive argument.

## Reproduction

Use GCC 12.2.0, Python 3.11.2, and NetworkX 3.5.

```bash
python3 -m venv /scratch/tree-global-venv
/scratch/tree-global-venv/bin/pip install -r requirements.txt

# Independent distance-versus-reroot cross-check on all 986 trees through 12,
# followed by a NetworkX order-19 census:
/scratch/tree-global-venv/bin/python census_global.py \
  --min-order 19 --max-order 19 --cross-check-order 12

# Fast exact WROM/Beyer-Hedetniemi level-sequence census:
g++ -std=c++20 -O3 -DNDEBUG -march=native \
  -Wall -Wextra -Wpedantic census_global.cpp -o /scratch/census_global
for n in 19 20 21 22; do /scratch/census_global "$n"; done

# Independent structural scan through order 19:
/scratch/tree-global-venv/bin/python check_balance.py --max-order 19
```

The Python reroot evaluator agreed with the direct all-pairs-distance
implementation on all 986 nonisomorphic trees through order 12. Its complete
order-19 run independently reproduced the previous maximum
$1{,}478{,}942{,}057{,}502$ and unique $B(5,5,8)$ maximizer.

The C++ program is a direct implementation of the WROM free-tree generator
and Beyer--Hedetniemi rooted-tree successor used by NetworkX. It pins the
unlabeled-tree counts at every requested order, uses an exact arbitrary-size
integer for binomial counts, and reproduced the Python order-19 result before
running the three new orders. A separate AddressSanitizer/UndefinedBehaviorSanitizer
build completed the order-16 census without a diagnostic.

Fresh generated records remain under `/scratch` and are not committed:

```text
order 19  sha256=0db1365af8133188e9ef371591dc0b0b3eceaf4b72efe8c0c8eeceebcbf50be9
order 20  sha256=fe74d3a8fdf003d97cb6cbc20481ba0263b132962947f3436f0df96b9aafa07b
order 21  sha256=6fb10d276075004e947bbe9ef6ea48b5ff890b6f6f0593956e9b53eddf5d0464
order 22  sha256=3da8a148524f21a7c421ad51154ee2741a3217a9fe18aa757c72b3aead9322e2

census_global.cpp  sha256=7ab2b37eeaf80353e667f7a0849bf4cd0ce25ca321daf531346862e494a770a0
census_global.py   sha256=943045bb33abbf0085707cf8d6188513add9b71b9c59d70ce6ab06edad6d658c
check_balance.py   sha256=a5e8d764a0fbc6b299f265c09e090d30be457ecaeaed6b9b6121dbb8d88b1f6e
requirements.txt   sha256=d617f742c7feb29397a1f1e407db73a1d623b09b362c52e969f81358cfd167c5
```

## Status, novelty, and trust boundary

The core-endpoint reduction and reroot identity are mathematical theorems.
The order-20 through order-22 classifications and the order-22 failure of
(H) are exact computational findings. Their trust boundary is the stated
free-tree generator, evaluator, implementations, compiler/runtime, and
independent cross-checks. All mathematical decisions use exact integers; no
random sampling, heuristic pruning, floating point, SAT solver, or external
proof log is involved.

The Csernák--Soukup paper and the committed Discovery Net graph were searched
through 2026-09-01. The paper introduces stacking and a conjectural tree
threshold but does not classify critical configurations or study their
multiplicity. No source was found containing this core-endpoint reduction,
these census extensions, or the order-22 obstruction. The results are
therefore apparently new to the searched sources, not a priority claim.

- T. Csernák and L. Soukup, *Stacking and clearing in graph pebbling*,
  arXiv:2604.22341v1 (2026), <https://arxiv.org/abs/2604.22341>.
- NetworkX 3.5 nonisomorphic-tree generator documentation and source,
  <https://networkx.org/documentation/stable/reference/generated/networkx.generators.nonisomorphic_trees.nonisomorphic_trees.html>.
