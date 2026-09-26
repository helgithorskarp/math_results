# Pendant forests have an exact two-choice maximum for line-graph signature

Author proof; independent review pending.

For a real symmetric matrix `A`, write `sig(A)=n_+(A)-n_-(A)`, counting
zero eigenvalues in neither term. All graphs are finite, simple and connected.
Write `s(H)=sig(A(L(H)))`, `M(H)=Q(H)-2I`, and `c(H)=|E(H)|-|V(H)|+1`.

## Theorem

Fix a host graph `H`. Let `P(H)` consist of all graphs obtained by attaching
arbitrary finite pendant trees to vertices of `H`, with each tree joined
to its attachment vertex by one edge. The empty collection is allowed.
For `S` contained in `V(H)`, let `H_S` be `H` with exactly one new leaf at
each vertex of `S`.

For every `G` in `P(H)` there is a constructively determined `S` such that

```
c(H_S)=c(G)=c(H),       s(G) <= s(H_S),
|V(H_S)| <= min(|V(G)|, 2|V(H)|).                       (1)
```

Consequently the infinite optimization has the exact finite expression

```
max_{G in P(H)} s(G)
 = max_{S subset V(H)} s(H_S)
 = 1-c(H) + max_S { sig(M(H)+2 diag(1_S)) - |S| }.       (2)
```

This is domination for the objective, not equality of inertia or response
of individual attachments. It applies in particular when `H` is a 2-core,
but does not require that hypothesis. The size bound is in terms of the
fixed host; it is not a bound in terms of cyclomatic number alone.

## 1. Reused rooted-tree invariant, with proof

For a rooted tree `(T,r)` put

```
C_T=Q(T)-2I+e_r e_r^T,
sigma(T)=sig(C_T),             rho(T)=(C_T^-1)_(r,r).
```

If the root has `k` child trees with states `(sigma_i,rho_i)`, eliminating
their blocks leaves

```
a=k-1-sum_i rho_i,
sigma=sum_i sigma_i+sign(a),   rho=1/a.                 (3)
```

The singleton has state `(-1,-1)`. Inductively the reduced numerators and
denominators of all child responses are odd. On a common odd denominator,
the numerator of `a` is `k-1-k=1 mod 2`. Thus `a` never vanishes, every
`C_T` is nonsingular, and the parity property persists.

The following simultaneous invariant is the antecedent proved in the
Discovery Net core-branch bound (reference in SOURCES.md):

```
sigma <= 0;
sigma = 0  implies rho = 1;
sigma = -1 and rho < 0 implies rho = -1.                (4)
```

Here is its short induction to make the dependency explicit. If `a<0`,
the new signature is negative. If `a>0` and every child signature were
zero, all child responses would be one and `a=-1`, a contradiction. Hence
the new signature is nonpositive. If the new signature is `-1` and `a<0`,
all child signatures vanish, giving `a=-1` and `rho=-1`. If the new
signature is zero, then `a>0`, exactly one child has signature `-1`, and
all other children have response one. For that exceptional child,
`a=-rho_i>0`; the induction hypothesis gives `rho_i=-1`, hence `rho=1`.
In particular, a signature-minus-one tree always satisfies `rho>=-1`.

## 2. A local domination inequality valid in every symmetric host

A collection of trees at a single attachment vertex has the aggregate
state

```
sigma_x=sum_T sigma(T),       d_x=sum_T (1-rho(T)).       (5)
```

Its effect, after exact Schur complementation, is to add `sigma_x` to the
signature and `d_x` to that host diagonal. For **every** real symmetric
matrix `K` and coordinate vector `e`, including singular `K`,

```
sigma_x + sig(K+d_x ee^T)
 <= sig(K)                         if sigma_x != -1,
 <= -1 + sig(K+2ee^T)               if sigma_x  = -1.   (6)
```

There are just three cases:

* If `sigma_x=0`, every tree has signature zero, so (4) gives `d_x=0`.
* If `sigma_x=-1`, exactly one tree has signature `-1`; every other tree
  contributes zero correction. Equation (4) gives `d_x=1-rho<=2`.
  Since `(2-d_x)ee^T` is positive semidefinite, eigenvalue monotonicity
  proves the second inequality in (6).
* If `sigma_x<=-2`, a rank-one perturbation changes signature by at most
  two. Therefore `sigma_x+sig(K+d_x ee^T)<=sig(K)`.

The last bound follows, for either sign of `d_x`, from rank-one
interlacing: each of the positive and negative indices changes by at
most one. No host inverse or defined host response is required.

Thus no attachment and a single leaf, with states `(0,0)` and `(-1,2)`
in the `(signature,diagonal correction)` convention, dominate all possible
pendant forests at that vertex. They both belong to the admissible family,
so their pointwise maximum is the exact local upper envelope.

## 3. Simultaneous replacement and the maximum

Eliminating all attached trees gives

```
sig M(G) = sum_x sigma_x + sig(M(H)+diag(d_x)).          (7)
```

Choose the explicit subset

```
S={ x in V(H) : sigma_x=-1 }.                          (8)
```

At each vertex apply (6), taking `K` to include all other diagonal
corrections already present. Replace its entire forest by a leaf if it
belongs to `S`, and by nothing otherwise. Each replacement weakly
increases the total signature. Inequality (6) holds for every `K`, so
interactions between different attachment vertices cause no gap in this
successive argument. The final graph is `H_S`, proving
`sig M(G)<=sig M(H_S)`.

The unsigned incidence identities `NN^T=Q` and `N^TN=A(L)+2I` give

```
s(G)=sig M(G)-c(G)+1.                                 (9)
```

Attaching or removing trees preserves `c`. Equations (7)--(9) prove the
signature and cycle assertions in (1). A selected vertex originally had
at least one tree vertex, so replacing it by one leaf never increases
order; there are at most `|V(H)|` selected vertices. This proves the size
assertion. Conversely every `H_S` belongs to `P(H)`, and eliminating its
`|S|` leaf pivots gives `sig M(H_S)=-|S|+sig(M(H)+2diag(1_S))`. This proves
(2), including existence and attainment of the maximum.

## 4. Consequences and exact limitations

For a fixed 2-core `H`, an upper bound on line-graph signature holds for
every pendant forest if and only if it holds for every subset of distinct
single leaves. Thus any counterexample with that core has one of order at
most `2|V(H)|`, with the same cyclomatic number and at least its signature.
An exact decision procedure uses at most `2^|V(H)|` inertia calculations on
matrices of order `|V(H)|`. This is a finite algorithm for a fixed host;
unbounded degree-two subdivisions still prevent a fixed-`c` finite bound.

The subset quantifier cannot be replaced by checking each vertex
separately using this argument. For example the abstract symmetric host
`K=(8J_3-18I_3)/27` has signature `-1` and inverse
`2J_3-(3/2)I_3`. Each individual leaf-style update has net change `-1`,
whereas all three together have net change `+1`, since `K+2I_3` is
positive definite. This is an algebraic caution about simultaneous
updates, not a claimed graph counterexample.

The theorem does not establish `2s(G)<=c(G)+1`, classify its equality
graphs, preserve nullity, or prove one-leaf stability implies all-forest
stability. The rooted invariant, Schur complement, rank-one interlacing,
and incidence identity are antecedents. The new conclusion is the exact
two-choice domination and fixed-host optimization formula.

## Evidence and trust boundary

The proof above is universal and does not depend on a computation.
`verify.py` audits rooted states, arbitrary symmetric hosts (including
singular ones), simultaneous graph attachments, literal line graphs,
and the complete subset formula on small hosts. An integer
characteristic-polynomial sign count provides a different calculation
from the rational rooted recursion and symmetric elimination.
The checker is author validation, not independent peer review or formal
verification. It uses only exact integers and fractions, no external
dataset, solver, floating-point spectrum, or omitted large certificate.
