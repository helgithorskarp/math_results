# Global critical multiplicity for tree stacking

Assembly author: Atlas, agent ID `studio-researcher-1`, researcher.
Contributors: Iris (`studio-researcher-2`), Nova (`studio-researcher-3`),
Rowan (`studio-researcher-4`). Version1, 2026-10-05.
Status at this source freeze: all four component versions have scoped
other-researcher internal checks; this new assembly awaits its own
exact-version internal check by Nova. The proofs below are ordinary
mathematics at the explicitly cited primary theorem boundary.

## 1. Definition and explicit theorem

A pebbling move removes two pebbles from a vertex and adds one at an
adjacent vertex. A stack has nonempty support consisting of exactly one
vertex; an already stacked configuration needs no move. For a finite tree
T with at least two vertices, stack(T) is the least integer k >= 2 such
that every configuration of exactly k pebbles can reach a stack.

Let N(T) count individual functions c:V(T) -> Z_{>=0} of mass
stack(T)-1 that are nonstackable. There is no automorphism quotient. Put

\[
 M(n)=\max_{|V(T)|=n}N(T),\qquad n\geq2.
\]

Relabeling a tree bijects configurations and legal move sequences, so N
is invariant under isomorphism. There are finitely many tree types at
fixed order, and finitely many configurations at a fixed finite mass.
The maximum is therefore well defined. The constructions below also
show N(T) >= 1, so the logarithms are defined.

**Theorem.** For every tree T of order n >= 2,

\[
 \log_2N(T)\leq\frac5{36}n^2+6n.\tag{1}
\]

For every integer n >= 37 there is an explicit tree T_n of order n with

\[
 \log_2 M(n)\geq\log_2N(T_n)
       >\frac5{36}n^2-\frac54n.\tag{2}
\]

Consequently, with the explicit common range n >= 37,

\[
 \frac5{36}n^2-\frac54n<\log_2M(n)
       \leq\frac5{36}n^2+6n,
 \qquad
 \log_2M(n)=\frac5{36}n^2+O(n).\tag{3}
\]

The constants are sufficient, without any optimality assertion. This
does not identify the globally maximizing tree or an optimal linear term.

## 2. The audited inherited counting interface

For n >= 3, let L be the graph leaves, I=V(T) minus L the nonleaves,
and let P be the parents of graph leaves. Use full-tree degrees and
ambient distances to define

\[
 F(v)=\sum_{u\in I}\deg_T(u)2^{\operatorname{dist}_T(v,u)},
 \quad X_p=F(p),\quad
 d_p=|L\cap N_T(p)|,
 \quad P^*=\operatorname*{argmax}_{p\in P}X_p.
\]

All tied maximizing parents are retained. A graph leaf z with parent p
satisfies F(z)=2F(p), since every path from z to a nonleaf passes through
p. The primary estimator is E(v)=1+|L|+F(v), including its leaf correction.
Every internal v has a neighbor of larger F: its neighbor-side
contributions Q_i sum to F(v)-deg_T(v); some Q_i is less than F(v)/2,
and crossing that edge gives 2F(v)-(3/2)Q_i>F(v). Thus all global
E-maximizers are graph leaves, and P* is precisely their parent set.

The inherited classification, rederived in the
[classification component](components/iris_classification_v1/PROOF.md),
gives

\[
 N(T)=\sum_{p\in P^*}\binom{X_p+d_p-1}{d_p-1}.\tag{4}
\]

Its configurations have piles 1+2x_z on leaves adjacent to one p in P*,
sum x_z=X_p, one pebble on every other graph leaf, and zero on nonleaves.
They are counted as individual functions. X_p>0 makes the families for
distinct parents disjoint. At d_p=1 the summand is one.

For precision, the complete equality proof of (4) is not a finite-tree
guess. Iris's Sections3--6 prove the convex branch mass majorant, its
exact evaluation at the global boundary, strict EMPTY slack, the genuine
nonterminal slope kink and convex-chord rigidity, the finite nested
equality walk, and the final terminal sibling split. They also prove the
converse and every-target zero scores. EMPTY is kept distinct from an
occupied numerical-zero message. The independent Atlas check of that
exact source is [recorded here](internal_checks/atlas_classification_v1/REVIEW.md).

The external mathematical inputs to that rederivation are Fairfax-Ball,
[arXiv:2609.31811v1](https://arxiv.org/html/2609.31811v1), Theorems3.3
(exact rooted score criterion) and1.1 (exact least-k>=2 estimator).
The counting classification and potential are prior results; the
immutable sources and bounded prior-work search are in [PRIOR_ART.md](PRIOR_ART.md).

For later use set

\[
 h_p=\max_{u\in I}\operatorname{dist}_T(p,u).
\]

This is the core eccentricity, not a structural deficit. The nonleaf
core is connected, so core distances agree with ambient distances.
The degree sum immediately gives

\[
 0<X_p\leq2(n-1)2^{h_p}.\tag{5}
\]

## 3. The universal maximizing-parent resource budget

We prove, for every n >= 3 and p in P*,

\[
 n\geq h_p+1+\frac95d_p-\frac45d_p2^{-h_p}.\tag{6}
\]

This is the new universal input that lifts the restricted-family exponent
to all trees. Its full proof and normalization are in the
[structural component](components/atlas_structural_v1/PROOF.md), checked
independently by [Nova](internal_checks/nova_structural_v1/REVIEW.md).

Here is the edge-charge argument. Suppose first that T is nonstar, write
p in P*, d=d_p, and let H=ecc_T(p) be the full eccentricity to a graph
leaf. Every farthest nonleaf has a leaf child, and every graph leaf has
a nonleaf parent, so H=h_p+1. In a nonstar H>=2.

Root the tree at p and split full degree contributions into incident
edge ends. An edge whose parent is at depth a contributes3*2^a to F(p)
if its child is nonleaf, and2^a if its child is a graph leaf. Choose a
farthest leaf w at distance H. The H-edge path to it is disjoint from
p's d leaf edges. Put t=2^{H-1}. The path contributes4t-3 and the
root-leaf edges contribute d. The remaining m=n-1-d-H edges have total
normalized weight E, so

\[
 X_p=d+4t-3+tE.\tag{7}
\]

Using just p, with degree at least d+1, and the interior path vertices,
with degrees at least two, gives F(w)/2 >= (d+3)t-2. Maximality of p
among leaf parents gives X_p >= F(w)/2. Hence

\[
 E\geq(d-1)(1-1/t).\tag{8}
\]

For the other direction, a remaining leaf-child edge has normalized
weight at most one. A nonleaf-child edge has weight at most3/4 unless
its parent is at depth H-2, when it weighs3/2. Each such heavy edge
has a nonleaf child at depth H-1 and at least one leaf-child edge at
depth H. Select one as its mate, with normalized weight one. The
child is off the chosen path because its parent edge is off it, and
the mate is not a root-leaf edge. It therefore belongs to the remaining
set. Distinct heavy edges have distinct children and distinct mates;
leaf-child mates cannot themselves be heavy. The pairs are disjoint.

If there are b pairs, they use2b<=m edges and weigh(5/2)b. Every
unpaired edge weighs at most one. Therefore

\[
 E\leq m+\frac12b\leq\frac54m,
 \qquad
 (d-1)(1-2^{1-H})\leq\frac54(n-1-d-H).\tag{9}
\]

Substituting H=h_p+1 and rearranging yields the stronger nonstar form

\[
 n\geq h_p+\frac65+\frac95d
           -\frac45(d-1)2^{-h_p}.\tag{10}
\]

Its right side exceeds that of (6) by1/5+(4/5)2^{-h_p}>0, proving (6)
for nonstars. For a star the sole parent is the center, h_p=0,d=n-1,
X_p=d, and (6) is equality. The stronger nonstar form is not applied
to stars. All ties and d=1 are allowed in the proof; no maximizing-parent
core-endpoint theorem is needed.

## 4. Uniform upper bound with a linear remainder

The [analytic component](components/rowan_upper_v1/PROOF.md) proves this
step as an abstract integer-parameter lemma; its independent
[Iris check](components/rowan_upper_v1/internal_checks/iris_full_v1/REVIEW.md)
also supplies a generating-coefficient derivation of the binomial estimate.
Here its two tree imports, (4) and (6), have been supplied by Sections2--3.

For one p in P*, write h=h_p,d=d_p and x=d-1. Rearranging (6) and
multiplying by5h/9 gives

\[
 hd\leq\frac59h(n-1-h)+\frac49hd2^{-h}.
\]

For integer h>=0, h2^{-h}<=1/2, including h=0. Completing the square
and using d<=n gives the uniform bound

\[
 hx\leq hd\leq\frac5{36}(n-1)^2+\frac29n
             \leq\frac5{36}n^2+\frac29n.\tag{11}
\]

If x=0 the binomial term is one. Otherwise let Z=X_p+x. Equation(5)
gives Z<=3n2^h. Retaining the factorial in the binomial bound,

\[
 \binom Zx\leq(eZ/x)^x,
 \qquad
 \log_2\binom Zx\leq hx+x\log_2(3en/x).\tag{12}
\]

For example x!>=(x/e)^x follows by integrating ln(t) from1 to x.
The function r ln(3e/r) increases on0<r<=1, since its derivative is
ln(3/r)>0. With r=x/n,

\[
 x\log_2(3en/x)\leq n\log_2(3e)<4n.\tag{13}
\]

The strict constant uses e<3 and3e<9<16; no numerical approximation is
needed. Combining (11)--(13), each summand in (4) is at most
2^{5n^2/36+38n/9}. There are at most n summands, all positive, so

\[
 \log_2N(T)\leq\frac5{36}n^2+\frac{38}9n+\log_2n
             \leq\frac5{36}n^2+6n.\tag{14}
\]

This proves (1) at n>=3 without a height cutoff or d>=2 assumption.
At n=2, T=K2: the sole critical obstruction is(1,1), stack(K2)=3,
and N(K2)=1, so (1) also holds. Taking the maximum over trees proves
the upper half of (3).

## 5. The inherited construction at every order n >= 37

Define R(d,e,t) from a t-edge path p=v_0-...-v_t=q by attaching d
graph leaves at p and e disjoint two-edge arms q-a_i-b_i at q.
The order is d+2e+t+1. Its leaf parents are p and the a_i. Summing
their full-degree distance weights gives

\[
 X_p=d-3+(5e+3)2^t,
 \qquad
 X_a=(d+3)2^{t+1}+10e-12.\tag{15}
\]

The construction and its parameters are prior work. The
[lower component](components/nova_lower_v1/PROOF.md) rederives this
literal shape, strict leaf-parent eligibility, sufficient critical
configurations and all-order bound. Its separate
[Rowan check](internal_checks/rowan_lower_v1/REVIEW.md) is the responsible
internal check of Nova's author result; Nova's later assembly check does
not certify his own lower component.

For an arbitrary n>=37, write n=18m+1+s, m>=2 and0<=s<=17, and choose

\[
 d=5m+3,\quad e=2m+2,\quad t=9m-7+s.\tag{16}
\]

These positive parameters have order n and cover all eighteen order
residues. Equations(15)--(16) give

\[
 X_p-X_a=2^t-(15m+8)>0.\tag{17}
\]

At m=2,s=0 this is2^{11}>38. Increasing m multiplies the minimum
exponential by512 while increasing the comparison by15, so induction
proves (17); increasing s only helps. Thus p is the unique maximizing
leaf parent. In particular the critical weak-composition configurations
at p give

\[
 N(R(d,e,t))\geq\binom Yr,
 \quad r=5m+2,
 \quad Y=(10m+13)2^t+10m+2.\tag{18}
\]

Only sufficiency is needed for (18). It also follows from the audited
classification (4). Nova's standalone lower proof instead reconstructs
sufficiency directly from the primary canonical zero-score theorem4.1
and score/estimator theorems, avoiding the converse classification.
Every redistributed graph leaf remains occupied, so no EMPTY/message-zero
identification enters that construction.

Here Y/r>2^{t+1}. Each factor in
binom(Y,r)=product_{i=0}^{r-1}(Y-i)/(r-i) is at least Y/r, because
i(Y-r)>=0. Therefore

\[
 \log_2N(T_n)>(5m+2)(t+1)
             =(5m+2)(9m-6+s)=:A.\tag{19}
\]

The exact identity

\[
 36\left(A-\frac5{36}n^2+\frac54n\right)
   =198m-392+s(107-5s)\tag{20}
\]

is positive: its first term is at least four at m>=2, and its second
term is nonnegative for0<=s<=17. Thus (19)--(20) prove (2) for every
integer n>=37. Together with (14) this proves the theorem. QED.

## 6. Logical and computational limits

The global theorem follows from the ordinary inequalities and audited
classification. No exhaustive enumeration of all large trees is a proof
dependency. The inherited R family, restricted exponent and classification
are prior art; the new claim is the universal tree budget and resulting
all-tree law with a uniform linear error. See [PRIOR_ART.md](PRIOR_ART.md)
for exact attribution and the limits of the novelty screen.

Finite exact controls in the structural and lower components test
their source implementations. Nova and Rowan respectively reproduced
those new controls once, in addition to independently examining the
ordinary proofs. Such replay is not a second independent finite
enumerator or a raw arbitrary-move oracle. The classification and analytic
components require no new computation. The source hashes and exact
other-researcher checks are in [COMPONENTS.md](COMPONENTS.md).

The external score/estimator theorems are ordinary published mathematical
inputs. This source does not claim a new formalization, an audit of the
primary paper's reported formal environment, external peer review,
historical priority, an exact maximizing tree, or an optimal linear term.
