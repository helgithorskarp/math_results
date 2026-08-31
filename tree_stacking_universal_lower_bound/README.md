# Universal lower bound for the Csernák--Soukup tree estimate

For every finite tree $T$ with at least two vertices,

$$
\operatorname{stack}(T)\ge \operatorname{estim}(T).
$$

Thus the Csernák--Soukup conjecture
$\operatorname{stack}(T)=\operatorname{estim}(T)$ reduces to its upper-bound
direction.  The proof explicitly constructs, for every leaf $r$, an
almost-stacked non-stackable configuration of norm
$\sigma_T(r)+\operatorname{leaf}(r)-1$.

## The estimate is maximized at a leaf

Let $L(T)$ and $I(T)$ denote the leaves and nonleaves.  The definition can be
rewritten, for every root $q$, as

$$
E(q):=\sigma_T(q)+\operatorname{leaf}(q)
=1+|L(T)|+\sum_{v\in I(T)}\deg(v)2^{d(q,v)}. \tag{1}
$$

The weighted exponential-distance sum on the right is maximized at a leaf.
Indeed, if $q$ is internal and $A_i$ is the contribution from the $i$th
component of $T-q$, moving from $q$ into that component changes the sum $F$
to $2F-3A_i/2$.  If no neighbor increased it, every $A_i$ would be at least
$2F/3$, impossible because $q$ has at least two neighbors and
$\sum_iA_i<F$.  Hence $\operatorname{estim}(T)=E(r)$ for some leaf $r$.

## Rooted clearance costs

Fix a leaf $r$ and root $T$ at $r$.  For $v\ne r$, define an odd positive
integer $A(v)$ recursively by

$$
A(v)=
\begin{cases}
1,&v\text{ is a leaf},\\
3+2\sum_{w\text{ child of }v}A(w),&v\text{ is internal}.
\end{cases} \tag{2}
$$

If $s$ is the neighbor of $r$, expansion of (2), followed by weighted edge
counting, gives

$$
A(s)=\sum_{\ell\in L(T)\setminus\{r\}}2^{d(s,\ell)}
+3\sum_{v\in I(T)}2^{d(s,v)}
=\sigma_T(r)-1. \tag{3}
$$

The last equality uses $d(r,v)=d(s,v)+1$ and
$\deg(v)=1+\#\{\text{children of }v\}$.

## Edge-flow lemma

Put one pebble on every leaf other than $r$, put $A(s)$ pebbles on $r$, and
put zero elsewhere.  Call this configuration $c_r$.

For a branch rooted at $v$, let $u$ and $z$ count moves from $v$ to its parent
and in the reverse direction.  If the branch finishes empty and the total net
input from its children is $S$, vertex balance gives

$$
z=2u-S,\qquad \delta:=u-2z=2S-3u, \tag{4}
$$

where $\delta$ is the branch's contribution to its parent.  A branch that
starts nonempty must have $u\ge1$.

Induction using (2)--(4) shows that an ordinary branch containing only the unit
leaf pebbles satisfies

$$
\delta\le-A(v),\qquad \delta\equiv-A(v)\pmod3. \tag{5}
$$

Now fix any proposed final target $t$ and follow the path
$r=v_0,v_1,\ldots,v_k=t$.  The heavy leaf first contributes at most

$$
\frac{A(v_1)-3}{2}
=\sum_{w\text{ child of }v_1}A(w).
$$

After the off-path branches cancel by (5), the effective input before the next
path edge is at most $A(v_2)$ and is congruent to it modulo $3$.  More
generally, if $A$ is odd, $S\le A$, and $S\equiv A\pmod3$, then (4) implies

$$
\delta\le
\begin{cases}
-1,&A=1,\\
(A-3)/2,&A>1.
\end{cases} \tag{6}
$$

To check (6), write $S=A-3h$ and split according to the parity of $h$; if
$S\le0$, the inequality is immediate from $u\ge1$.  Iterating (6) along the
path shows that at an internal target the path contribution is at most the
sum of the target's ordinary child costs, which (5) cancels.  At a leaf target
other than $r$, the path contributes at most $-1$, cancelling its initial unit
pebble.  At target $r$, (5) makes the rest of the tree contribute at most
$-A(s)$, cancelling the heavy pile.

Thus every possible target has final pile at most zero.  The configuration is
non-stackable and, by (3), has norm

$$
A(s)+\operatorname{leaf}(r)
=\sigma_T(r)+\operatorname{leaf}(r)-1.
$$

Choosing a maximizing leaf in (1) proves the theorem.

## Exact finite validation

The supplied patch instruments the previously published complete order-eight
frontier enumerator.  At weight $\operatorname{estim}(T)-1$ it constructs the
configuration above for every maximizing root and asserts membership in the
exact non-stackable frontier.  A fresh run checked every maximizing root of
all 23 unlabeled eight-vertex trees and ended with
`COMPLETE trees=23 all_equal=true`.

```bash
cp ../tree_stacking_order8/enumerate_tree8_stacking.cpp \
  /scratch/verify_order8_critical_witnesses.cpp

patch /scratch/verify_order8_critical_witnesses.cpp \
  < critical_witness_assertions.patch

g++ -std=c++20 -O3 -DNDEBUG -march=native \
  -Wall -Wextra -Wpedantic \
  /scratch/verify_order8_critical_witnesses.cpp \
  -o /scratch/verify_order8_critical_witnesses

/scratch/verify_order8_critical_witnesses \
  ../tree_stacking_order8/tree8_catalog.tsv \
  > /scratch/tree8-critical-witness-test.log
```

The computation is corroboration only; the theorem is the general edge-flow
proof above.  No solver, random search, floating-point decision, or external
certificate is used.  The full frontier run inherits the exact-integer and
compiler/runtime trust boundary documented with the order-eight census.

```text
critical_witness_assertions.patch  3c364eed49f13286fd386b95e22e402395a3885ad6ddcaaa92ab6c29bd711c8a
```

## Novelty and source

The searched primary paper defines $\operatorname{estim}(T)$, proves the
conditional upper bound under the Almost Stacked Hypothesis, and conjectures
equality, but does not state or prove this general lower bound.  The lemma is
apparently new to the searched sources, not a priority claim.

- T. Csernák and L. Soukup, *Stacking and clearing in graph pebbling*,
  arXiv:2604.22341v1 (2026), <https://arxiv.org/abs/2604.22341>.
