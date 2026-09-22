# Sharp homogeneous-set growth in the perfect-or-pentagon modular class

All graphs are finite and simple.  Write `alpha(G)` and `omega(G)` for the
independence and clique numbers.

## 1. The class

If `F` has vertices `1,...,t` and `G_1,...,G_t` are pairwise vertex-disjoint
graphs, the substitution

```text
F(G_1,...,G_t)
```

keeps every edge inside a module `G_i`, makes `G_i` complete to `G_j` when
`ij` is an edge of `F`, and makes them anticomplete otherwise.

Let `M_5` be the smallest class containing `K_1` with the following closure
rule: if every `G_i` is in `M_5` and the outer graph `F` is either perfect or
isomorphic to `C_5`, then `F(G_1,...,G_t)` is in `M_5`.  We call these graphs
**pentagon-perfect modular** in this note.

The class is hereditary.  Indeed, an induced subgraph restricts each module
and replaces `F` by an induced subgraph.  Induced subgraphs of perfect graphs
are perfect, while every proper induced subgraph of `C_5` is perfect.
Gallai's modular decomposition gives the equivalent description that every
prime quotient is perfect or `C_5`.

Put

```text
q = log_5(4),       p = 1/q = log_4(5).
```

Thus `p>1` and `4^p=5`.

## 2. The weighted outer-graph inequality

### Lemma

Let `F` be either a perfect graph or `C_5`.  Give its vertices two systems of
nonnegative weights `a_i,b_i`, and put

```text
A = max { sum_(i in S) a_i : S is stable in F },
B = max { sum_(i in K) b_i : K is a clique in F }.
```

Then

```text
sum_i (a_i b_i)^p <= (A B)^p.                       (1)
```

### Perfect outer graphs

The assertion is immediate if `A B=0`, so normalize `A=B=1`.  The vector
`b` satisfies every clique inequality of `F`.  Chvátal's polyhedral
characterization of perfect graphs says that it is therefore a convex
combination of incidence vectors of stable sets of `F`.  Consequently

```text
sum_i a_i b_i <= A = 1.
```

Since `p>1` and all products are nonnegative,

```text
sum_i (a_i b_i)^p <= (sum_i a_i b_i)^p <= 1,
```

which proves (1).

### The exceptional outer graph `C_5`

Index the cycle modulo five.  After the same normalization, `a` and `b`
belong respectively to

```text
P_a = {x>=0 : x_i+x_(i+2)<=1 for every i},
P_b = {x>=0 : x_i+x_(i+1)<=1 for every i}.          (2)
```

Each polytope has exactly twelve vertices: the eleven zero-one incidence
vectors of stable sets in its constraint cycle, together with

```text
(1/2,1/2,1/2,1/2,1/2).                              (3)
```

For completeness, this familiar odd-cycle fact follows directly.  If one
coordinate is zero, the remaining constraint graph is a path and its edge
inequality polytope is integral.  If all coordinates are positive at a
fractional vertex, all five cycle inequalities must be tight (otherwise an
alternating perturbation is possible); their unique solution is (3).

For fixed `b`, the left side of (1) is convex in `a`, and conversely.  Its
maximum on `P_a x P_b` is therefore attained at a pair of vertices.  There
are only three types.

1. Two zero-one vertices have supports that are respectively a clique and a
   stable set of the original `C_5`.  Their intersection has size at most
   one, so the sum in (1) is at most one.
2. If exactly one vertex is (3), the zero-one support has size at most two,
   so the sum is at most `2(1/2)^p<1`.
3. If both are (3), the sum is

   ```text
   5(1/4)^p = 1
   ```

   because `4^p=5`.

This proves the lemma.  The exact enumeration in `verify.py` independently
audits the finite polytope statement and every vertex-pair type.

## 3. Product theorem

### Theorem

Every nonempty `G` in `M_5` satisfies

```text
alpha(G) omega(G) >= |V(G)|^q,       q=log_5(4).     (4)
```

Therefore every such graph contains a clique or stable set of size at least

```text
|V(G)|^(q/2) = |V(G)|^(log_5 2).                    (5)
```

The same conclusions hold for every nonempty induced subgraph of `G`.

### Proof

Induct on a substitution expression.  The assertion is equality for `K_1`.
Write a larger graph as

```text
G = F(G_1,...,G_t),
```

where `F` is perfect or `C_5`.  Set

```text
n_i = |V(G_i)|,   a_i = alpha(G_i),   b_i = omega(G_i).
```

Stable sets and cliques project exactly through the modules, so

```text
alpha(G) = max_(S stable in F) sum_(i in S) a_i = A,
omega(G) = max_(K clique in F) sum_(i in K) b_i = B. (6)
```

The induction hypothesis and `p=1/q` give

```text
n_i <= (a_i b_i)^p.
```

Summing and applying the lemma,

```text
|V(G)| = sum_i n_i
        <= sum_i (a_i b_i)^p
        <= (A B)^p.
```

Raising to the power `q` and using (6) proves (4).  Inequality (5) follows
from `max(alpha,omega)>=sqrt(alpha omega)`.  Heredity of `M_5` gives the
induced-subgraph assertion.

## 4. Exact sharpness

Let `X_0=K_1` and recursively set

```text
X_(k+1) = C_5(X_k,X_k,X_k,X_k,X_k).
```

These are the lexicographic powers of `C_5`.  Module projection gives

```text
|V(X_k)|=5^k,
alpha(X_k)=omega(X_k)=2^k.
```

Hence equality holds in (4) and (5):

```text
alpha(X_k)omega(X_k)=4^k=(5^k)^q,
max(alpha(X_k),omega(X_k))=2^k=(5^k)^(log_5 2).
```

No larger homogeneous-set exponent is valid on `M_5`, even with an arbitrary
fixed positive leading constant.

## 5. Scope

This is an exact theorem for a substitution-closed hereditary host class.  It
does not prove the Erdős--Hajnal conjecture for a new forbidden graph, nor does
it improve the current bound for all `C_5`-free graphs.  Those statements have
different quantifiers.  The contribution is the sharp product invariant, the
weighted `C_5` lemma, and the extension from perfect graphs through arbitrary
nested pentagon modules.
