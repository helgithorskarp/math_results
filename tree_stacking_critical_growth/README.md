# Superexponential critical multiplicity in tree stacking

## Result

For a finite tree `T`, let `N(T)` be the number of non-stackable pebbling
configurations of maximum possible mass `stack(T)-1`.  The exact
sibling-leaf classification gives

$$
N(T)=\sum_{p\in P^*}\binom{X_p+d_p-1}{d_p-1},
$$

where `d_p` is the number of leaf neighbors of a maximizing parent `p`, and
`X_p` is the heavy leaf's excess in two-pebble units.

This note identifies a family with superexponentially many such
configurations and determines the sharp quadratic exponent among
caterpillars.

### Double-broom formula

Let `B(d,e,ell)` be the tree obtained by joining two hubs by a path of `ell`
edges and attaching `d` leaves to the left hub and `e` leaves to the right
hub.  Assume `1 <= d <= e` and `ell >= 1`.  Then the leaves on the `d`-leaf
side are maximizing.  They are the only maximizing leaves when `d < e`,
while both sides maximize when `d=e`.  Their excess is

$$
X_d=2^\ell(e+3)+d-3.
$$

Consequently

$$
N(B(d,e,\ell))=
\begin{cases}
\displaystyle
\binom{2^\ell(e+3)+2d-4}{d-1},&d<e,\\[6pt]
\displaystyle
2\binom{2^\ell(d+3)+2d-4}{d-1},&d=e.
\end{cases} \tag{1}
$$

### Sharp quadratic exponent for caterpillars

Let

$$
M_n^{\rm cat}=\max\{N(T):T\text{ is a caterpillar on }n\text{ vertices}\}.
$$

Then

$$
\boxed{\log_2 M_n^{\rm cat}=\frac{n^2}{8}+O(n\log n).} \tag{2}
$$

More explicitly, for `n >= 6`, symmetric double brooms give

$$
M_n^{\rm cat}\ge
2^{\left\lfloor (n-3)^2/8\right\rfloor+1}, \tag{3}
$$

and every nonstar caterpillar satisfies

$$
N(T)\le
2n^{(n-3)/2}
2^{\left\lfloor (n-3)^2/8\right\rfloor}. \tag{4}
$$

The star has

$$
N(K_{1,n-1})=\binom{2n-3}{n-2}=2^{O(n)},
$$

so it does not affect (2).  Thus even on trees, maximum-mass non-stackable
configurations can have genuinely superexponential multiplicity.

## Proof

### Leaf excess as an exponential distance score

Let `z` be a graph leaf.  The structural-deficit identity

$$
H(z)=1+\sum_{\deg(v)>1}\deg(v)2^{d(z,v)}
$$

gives

$$
X(z):=\frac{H(z)-1}{2}
=\sum_{\deg(v)>1}\deg(v)2^{d(z,v)-1}. \tag{5}
$$

The leaves with maximum `X(z)` are exactly the leaves used by the
sibling-leaf classification.

For `B(d,e,ell)`, a left leaf has distance `i+1` from the `i`-th core
vertex.  The core degrees are `d+1,2,...,2,e+1`, so (5) gives

$$
X_d=(d+1)+\sum_{i=1}^{\ell-1}2^{i+1}+(e+1)2^\ell
=2^\ell(e+3)+d-3. \tag{6}
$$

Similarly,

$$
X_e=2^\ell(d+3)+e-3,
$$

and hence

$$
X_d-X_e=(2^\ell-1)(e-d). \tag{7}
$$

Equations (6)--(7) identify the maximizing sibling classes.  Substitution in
the exact count formula proves (1).

### Endpoint convexity

Consider a nonstar caterpillar.  Write its nonleaf core as
`v_0,...,v_ell`, and let `r_i` be the number of pendant leaves at `v_i`.
Thus `r_0,r_ell >= 1`.  Put `q_i=deg(v_i)`.  Every leaf at `v_i` has excess

$$
X_i=\sum_{j=0}^\ell q_j2^{|i-j|}. \tag{8}
$$

For every interior index, each summand in (8) satisfies

$$
2^{|i-1-j|}+2^{|i+1-j|}>2\,2^{|i-j|}.
$$

Therefore `X_i` is strictly convex along the core.  Its maximum occurs only
at an endpoint.  Hence a nonstar caterpillar has at most two maximizing
sibling-leaf classes.

### Balance and compression

Suppose the left endpoint is maximizing, and write

$$
d=r_0,\qquad e=\sum_{i=1}^\ell r_i.
$$

Split the degrees in (8) into the symmetric bare-path degrees
`1,2,...,2,1` and the pendant contributions `r_i`.  The bare-path
contribution cancels in `X_0-X_ell`, so

$$
0\le X_0-X_\ell
=\sum_{i=0}^\ell r_i(2^i-2^{\ell-i}). \tag{9}
$$

The `i=0` coefficient is `-(2^ell-1)`, while every other coefficient is at
most `2^ell-1`.  Equation (9) forces

$$
e\ge d. \tag{10}
$$

For fixed `d,e,ell`, moving every nonleft pendant leaf to `v_ell` only
increases `X_0`.  The resulting tree is the double broom, and (6) gives

$$
X_0\le2^\ell(e+3)+d-3, \tag{11}
$$

with equality exactly when all nonleft pendant leaves are already at the
right endpoint.

The order is `n=ell+1+d+e`.  By (10),

$$
\ell\le n-2d-1.
$$

Also (11) gives

$$
X_0+d-1\le n2^\ell.
$$

The contribution of this endpoint class is therefore at most

$$
\binom{X_0+d-1}{d-1}
\le n^{d-1}2^{\ell(d-1)}. \tag{12}
$$

Writing `x=d-1`,

$$
\ell(d-1)\le x(n-3-2x)
\le\left\lfloor\frac{(n-3)^2}{8}\right\rfloor. \tag{13}
$$

There are at most two endpoint classes and `d-1 <= (n-3)/2`, so (12)--(13)
prove (4).

For the lower bound, choose `d=x+1` and

$$
\ell=n-2d-1,
$$

where the integer `x` maximizes `x(n-3-2x)`.  For `n>=6` this is a valid
symmetric double broom and the maximum equals
`floor((n-3)^2/8)`.  From (1),

$$
N(B(d,d,\ell))
=2\binom{2^\ell(d+3)+2d-4}{d-1}
\ge2^{\ell(d-1)+1},
$$

because the numerator factors dominate
`(2^ell(d+3))^(d-1)` and `(d-1)! <= (d-1)^(d-1)`.
This proves (3), and hence (2).

## Exact finite census

The standalone checker exhausts all oriented caterpillar core profiles
through order 22.  The star is the unique maximizer through order 14.  At
order 15 it is overtaken by `B(4,4,6)`:

$$
N(B(4,4,6))=30{,}577{,}800
>N(K_{1,14})=20{,}058{,}300.
$$

The exact global census of every nonisomorphic tree through order 19 finds a
unique maximizer at every order.  The global maximizer is the star through
order 14, then:

| order | maximizing double broom | exact `N(T)` |
|---:|:---:|---:|
| 15 | `B(4,4,6)` | 30,577,800 |
| 16 | `B(5,5,5)` | 383,736,990 |
| 17 | `B(5,5,6)` | 5,930,563,870 |
| 18 | `B(5,5,7)` | 93,247,009,310 |
| 19 | `B(5,5,8)` | 1,478,942,057,502 |

This finite census does **not** prove that a double broom is globally
extremal among all trees at every order.  That stronger statement remains a
natural conjecture.

## Reproduction

Use Python 3.11.2 and NetworkX 3.5.

```text
python3 -m venv /scratch/tree-count-venv
/scratch/tree-count-venv/bin/pip install -r requirements.txt

# Formula checks and every caterpillar profile through order 22:
/scratch/tree-count-venv/bin/python critical_growth.py \
  --max-caterpillar-order 22

# Also exhaust every nonisomorphic tree through order 19:
/scratch/tree-count-venv/bin/python critical_growth.py \
  --max-caterpillar-order 22 --max-tree-order 19
```

The program checks 512 closed-form double-broom cases directly against the
distance-degree count.  It separately compares the compressed caterpillar
formula with explicit graph construction for every oriented profile through
order 12.  The full run checked 1,048,575 oriented caterpillar profiles
through order 22 and 522,958 nonisomorphic trees through order 19.  An
additional comparison against the earlier directed-deficit implementation
agreed on all 986 nonisomorphic trees through order 12.

Fresh full-run record (not committed):

```text
tree_stacking_critical_growth_full.json
sha256=7da91c9ab829f14d82a628d32d49d951ed22b49808d4ec3d9fcc7d661f7acf34

critical_growth.py
sha256=cb7c627eac5f7e599c7334613ae6f46b022117f0bf0b154be70a06b9e1a529ce

requirements.txt
sha256=d617f742c7feb29397a1f1e407db73a1d623b09b362c52e969f81358cfd167c5
```

Large generated JSON records belong under `/scratch` and are not committed.

## Status, novelty, and trust boundary

The double-broom formula and caterpillar asymptotic are mathematical theorems
conditional only on the already proved sibling-leaf classification.  The
finite all-tree statements are exact computational results.  Their trust
boundary is NetworkX 3.5's `nonisomorphic_trees`, the distance-degree
implementation, and the named Python runtime; all decisions use exact
integers.

The primary stacking paper and authors' repository were searched through
2026-09-01.  They introduce the parameter and conjecture the tree threshold,
but do not classify or count critical configurations.  Targeted searches did
not locate this double-broom multiplicity formula or the caterpillar growth
law.  The results are therefore apparently new to the searched sources, not
a priority claim.

- T. Csernák and L. Soukup, *Stacking and clearing in graph pebbling*,
  arXiv:2604.22341v1 (2026), <https://arxiv.org/abs/2604.22341>.
- Authors' computation repository, inspected through 2026-09-01:
  <https://github.com/lajossoukup/pebbling>.
