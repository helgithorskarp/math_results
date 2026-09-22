# Optimal non-cancelling toggle words in height three

Here **height** means the number of strict inequalities in a longest chain.
Thus a chain with five elements has height four. No grading or purity is
assumed. Write `0` and `1` for the bottom and top of a finite bounded poset
`P`, and put

\[
\mu(1)=1,\qquad \mu(v)=-\sum_{u>v}\mu(u).
\]

A state is a subset of `P\{1}`, initially empty. A move at `v != 1` is
allowed when `mu(v) != 0` and the principal ideal `down(v)` is either entirely
absent or entirely present; it adds or removes that ideal, respectively.
The goal is `P\{1}`. These conventions agree with Wilhelm's Definition 3.1
[W1]; the same definition makes sense without latticehood.

## The theorem

**Theorem 1.** Every finite bounded poset of height at most three has a
winning word that uses each proper element `v` exactly `|mu(v)|` times.
Every occurrence is an addition if `mu(v)<0`, and a removal if `mu(v)>0`.
Consequently, for arbitrary fixed nonnegative real costs `w_v`, one and the
same word minimizes total move cost and attains

\[
\min\operatorname{cost}=\sum_{v\ne1}w_v|\mu(v)|. \tag{1}
\]

For at least three elements, let `C` be the coatoms, let
`A=P\{0,1}\setminus C`, and set

\[
m=|C|,\quad d(a)=|\{c\in C:a<c\}|,\quad
R=\sum_{a\in A}(d(a)-1).
\]

Then the minimum number of moves is

\[
\ell(P)=m+R+|m-1-R|=2\max\{m-1,R\}+1. \tag{2}
\]

The singleton poset has optimum zero; the two-element chain has optimum one.
The construction below is a polynomial-time algorithm, with no game-state
search. Its output has length `O(|A|+|C|+|E|)` for the incidence graph `E`
defined below.

## 1. The standard signed-count lower bound

In any winning word, let `n_v` be the number of additions at `v` minus the
number of removals there. Taking the indicator of each proper element `u`
in the final state gives

\[
\sum_{u\le v<1}n_v=1.
\]

This triangular linear system has the unique solution `n_v=-mu(v)`.
Hence there are at least `|mu(v)|` moves at every `v`. Multiplying these
coordinatewise inequalities by `w_v>=0` proves the lower bound in (1).
This is the classical Möbius-inversion argument, not a new lower bound;
compare Proposition 4.7 of [AMS] and the original discussion [AM].

For a dot-algebra tree whose leaves are proper principal ideals, the signed
leaf multiplicities obey the identical system: at a difference node, negate
the signs in its right subtree. Thus the same bound also applies to the
weighted number of nonempty leaves in **unrestricted** such expression
trees. A winning word attaining (1) attains this bound as a left-linear tree.

## 2. Height three becomes an incidence graph

Assume now `|P|>=3`. Every element of `A` is an atom. Indeed, an interior
element strictly below `a in A`, followed by a coatom above `a`, would give
a chain with four strict inequalities. Also `d(a)>=1`. Distinct elements of
`A` are incomparable, as are the elements of `C`.

Let `H` be the bipartite graph with vertex set `A` disjoint union `C` and
edge `ac` exactly when `a<c`. An element in `C` can also be an atom; it is
then an isolated vertex of `H`. No vertex of `A` is isolated. We have

\[
\downarrow a=\{0,a\},\qquad
\downarrow c=\{0,c\}\cup N(c).
\]

Directly from the upper recurrence,

\[
\mu(c)=-1,\qquad \mu(a)=d(a)-1,\qquad \mu(0)=m-1-R. \tag{3}
\]

For each connected component `H_i`, write `m_i=|C_i|`,
`R_i=sum_{a in A_i}(d(a)-1)`, and

\[
\beta_i=|E(H_i)|-|A_i|-|C_i|+1=R_i-m_i+1\ge0.
\]

This is its graph cycle rank, including the value zero for an isolated
coatom. If `q` is the number of components and `beta=sum_i beta_i`, then

\[
\mu(0)=q-1-\beta. \tag{4}
\]

The order complex of the proper part is exactly `H`, so (4) is also its
reduced Euler characteristic. Nothing in the proof requires `H` to be
acyclic or crown-free, or to have bounded degrees or bounded order.

## 3. A provisional word for one component

For the next two steps, permit a bottom move without checking the global
value `mu(0)`. Every other move will already be permitted globally. We will
remove or orient all bottom moves correctly before executing the final
word. This distinction matters when the global bottom has Möbius value zero.

Order the coatoms of a component as `c_1,...,c_{m_i}` so that each coatom
after the first shares an atom with some earlier coatom. Such an order
exists by connectivity (for example, use breadth-first traversal of `H_i`).
An isolated coatom is a component with a one-term order.

Start with the addition of `c_1`. At the end of each stage the bottom,
the processed coatoms and all their neighboring atoms are on; all other
elements of this component are off. For the next coatom `c`, let its
already-on neighbors be `a_1,...,a_t`. Connectivity ensures `t>=1`.
Append

\[
a_1,\ 0,\ a_2,\ 0,\ \ldots,\ 0,\ a_t,\ c. \tag{5}
\]

Each atom move is a removal of `{0,a_j}`. Between consecutive removals,
the bottom is added back. After the last removal all of `down(c)` is off,
so `c` can be added. No other previously covered atom was turned off. The
stage invariant is restored.

An atom is removed once for each incident coatom after the first, exactly
`d(a)-1` times. In particular, a degree-one atom is never moved, and any
atom that is moved has positive Möbius value. Each coatom is added once.
The number of bottom additions is

\[
\sum_{j=2}^{m_i}(t_j-1)
=\sum_{a\in A_i}(d(a)-1)-(m_i-1)=\beta_i. \tag{6}
\]

We have obtained a provisional word `W_i` which fills this component and
the bottom. All its bottom moves are additions, and there are exactly
`beta_i` of them. Call their positions addition slots.

## 4. Splicing components eliminates the unwanted bottom moves

**Splicing fact.** Suppose two provisional words fill disjoint sets of
private elements, their ideals intersecting only at the bottom. Replace a
bottom-addition slot of the first word with the entire second word. This
gives a provisional word filling both private sets and the bottom. All
bottom moves remain additions, and their combined number decreases by one.

To verify this, at the replaced slot the bottom is off and every private
element of the inserted word is still off. The inserted word therefore
runs just as it did alone. At its end its private elements and the bottom
are on. Relative to the first word's elements, its net effect is exactly
the replaced bottom addition. Every later move of the first word therefore
has the same legality and effect as before, and it cannot affect the newly
filled private elements. This also proves the fact for words already formed
by earlier splicings.

Initially there are `q` words and `beta` slots. While at least two words
remain and some slot exists, splice another word into a slot. Each merge
reduces both counts by one. Thus exactly `min(beta,q-1)` merges occur.

* If `beta>=q-1`, one word remains, with `beta-q+1=-mu(0)` bottom additions.
  When this number is positive, the bottom has negative Möbius value and
  these additions are allowed. When it is zero, no bottom move remains.
* If `beta<q-1`, there remain `q-beta` words with no slots. Run them in any
  order, inserting a single bottom **removal** between consecutive words.
  A completed word leaves the bottom on; removing it makes the next word's
  bottom and as yet untouched private elements all off. The removals are
  therefore legal, and their number is `q-beta-1=mu(0)>0`.

All atoms and coatoms retain exactly the counts proved in Section 3.
The bottom has now exactly `|mu(0)|` moves, with the required sign. In
particular no zero-Möbius element is ever moved in the final word.
This proves Theorem 1 using Section 1. Equations (2) and (3) follow by
summing the counts. The one- and two-element cases are immediate.

The substitution principle has an elementary predecessor in Monet's
single-element deletion/insertion argument in [AM]. The claim here is the
complete incidence-component construction and its optimization conclusion,
not priority for substitution as a technique.

## 5. Sharp height and expression-tree consequences

**Corollary 2.** The least possible height of an unwinnable finite lattice
is exactly four. The same threshold holds for finite lattices admitting no
winning unrestricted dot-algebra tree of proper nonzero-Möbius ideals.

Theorem 1 supplies the lower bound for both assertions, since its word gives
a left-linear tree. For the first upper bound, [W1, Section 5.1 and
Corollary 7.4] constructs depth-four lattices and proves that suitable
members are unwinnable. For the second, [W2, Section 2 and Theorem 1.1]
uses that same depth-four family and proves that suitable members admit no
winning unrestricted tree. Their depth counts strict inequalities, as does
our height. This corollary **uses those published existence proofs**; this
package does not construct a new explicit height-four counterexample.

In particular every height-at-most-three lattice satisfies both the
left-linearity and sign-coherence strengthenings considered in [AMS,
Section 7]. Among all proper-ideal expression trees, a left-linear tree
already realizes every nonnegative element-weighted leaf-cost optimum (1).

## Scope and evidence

This is a human-readable combinatorial proof, not a computer-assisted
classification. The code checks the construction on a finite prescribed
family; it does not prove the universal quantifier or verify [W1, W2].
The proof is not formally verified or independently peer-reviewed at
publication. No minimum-order improvement, explicit unwinnable lattice,
height-four classification, or historical-priority claim is made.

References and exact attribution are in [SOURCES.md](SOURCES.md).
