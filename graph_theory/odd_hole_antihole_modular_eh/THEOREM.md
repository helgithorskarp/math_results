# A sharp odd-hole/antihole modular Erdős--Hajnal hierarchy

All graphs are finite and simple.  Write `alpha(G)` and `omega(G)` for the
independence and clique numbers.

## 1. Substitution classes

If `F` has vertices `1,...,t` and the graphs `G_1,...,G_t` are disjoint, the
substitution `F(G_1,...,G_t)` replaces vertex `i` by `G_i`, making two
modules complete or anticomplete according as their vertices are adjacent or
nonadjacent in `F`.

Fix an integer `h>=2`.  Let `M_h` be the smallest class containing `K_1` and
closed under substitution whenever the outer graph is

1. a perfect graph; or
2. an odd hole `C_(2r+1)` or its complement, for some `r>=h`.

Equivalently, every prime quotient in the modular decomposition is perfect
or is one of those permitted odd holes and odd antiholes.  The class is
hereditary: perfect graphs are closed under induced subgraphs, and every
proper induced subgraph of an odd hole or odd antihole is perfect.

Set

```text
q_h = log_(2h+1)(2h),       p_h = 1/q_h = log_(2h)(2h+1).
```

## 2. The weighted odd-hole inequality

### Lemma 1

Let `r>=2`, `n=2r+1`, and give the vertices of `C_n` two systems of
nonnegative weights `a_i,b_i`.  Define

```text
A = max { sum_(i in S) a_i : S is stable in C_n },
B = max { sum_(i in K) b_i : K is a clique in C_n },
p_r = log_(2r)(2r+1).
```

Then

```text
sum_i (a_i b_i)^p_r <= (A B)^p_r.                 (1)
```

The same assertion holds when the outer graph is the odd antihole
`complement(C_n)`, because complementation exchanges the two maxima and we
may exchange `a` with `b`.

### The two normalized polytopes

The result is immediate if `AB=0`, so normalize `A=B=1`.  Index the cycle
modulo `n`.  Then `b` belongs to

```text
P_b = {x>=0 : x_i+x_(i+1)<=1 for every i}.         (2)
```

The vertices of `P_b` are the zero-one incidence vectors of stable sets of
the cycle, together with the all-`1/2` vector.  Indeed, a vertex having a
zero coordinate lies in the edge relaxation of a path, which is integral.
At an all-positive fractional vertex every cycle-edge inequality must be
tight (otherwise an alternating perturbation is possible), and the unique
solution is all-`1/2`.

The normalized vector `a` belongs to the antiblocker

```text
P_a = {x>=0 : x(S)<=1 for every stable set S of C_n}.  (3)
```

Its vertices are the zero-one incidence vectors of cliques of `C_n`
(the empty set, single vertices, and cycle edges), together with

```text
u = (1/r,...,1/r).                                  (4)
```

Here is a proof of the only nonstandard direction.  We use the standard
odd-antihole stable-set polytope description

```text
K = conv{0, e_i, e_i+e_(i+1)}
  = {x>=0 : x(S)<=1 for every stable S of C_n,
             x(V)<=2}.                              (5)
```

This is the odd-antihole specialization of the vertex-packing polytope
description; (5) can also be obtained directly by deleting a coordinate,
using the integral path polytope, and restoring the sole rank inequality.

For `x in P_a`, put `t=x(V)`.  The `n` maximum stable sets of `C_n` each
have size `r` and contain every vertex exactly `r` times.  Summing their
inequalities gives

```text
t <= n/r = 2+1/r.                                   (6)
```

We need one refinement.  Let `S` be any stable set, `s=|S|`, and
`d=r-s`.  Define the `n` maximum stable sets

```text
I_j = {j+1,j+3,...,j+2r-1}  (indices modulo n).
```

Since `S` is stable, the `2s` vertices in `S union (S+1)` are distinct.
Keep the `2d+1` sets `I_j` with

```text
j notin S union (S+1).
```

A vertex of `S` occurs in exactly `d+1` kept sets, while every other vertex
occurs in exactly `d`: among the removed adjacent pairs, a maximum stable set
contains one vertex from each pair except its unique omitted adjacent pair.
Summing these `2d+1` valid inequalities yields

```text
d t + x(S) <= 2d+1.                                 (7)
```

If `t<=2`, (5) puts `x` in `K`.  Suppose `t>2`.  Restricting (3) to the
path obtained by deleting vertex `i` and using the perfect path polytope
gives `sum_(j!=i)x_j<=2`, hence

```text
x_i >= t-2.                                         (8)
```

Put `lambda=r(t-2)`, so `0<lambda<=1` by (6).  If `lambda=1`, (8) and the
sum force `x=u`.  Otherwise set

```text
y = (x-lambda*u)/(1-lambda).
```

It is nonnegative by (8), has `y(V)=2`, and (7), with `d=r-s`, gives

```text
y(S) <= [1-d(t-2)-lambda*s/r]/(1-lambda) = 1
```

for every stable set `S`.  Thus (5) gives `y in K`, and
`x=lambda*u+(1-lambda)y`.  Consequently

```text
P_a = conv(K union {u}),                            (9)
```

which proves the asserted vertex list.

### Completing Lemma 1

For fixed `b`, the left side of (1) is convex in `a`, and conversely.  Its
maximum over `P_a x P_b` is therefore attained at a pair of vertices.  There
are four cases.

1. An integral clique and an integral stable set intersect in at most one
   vertex, so the sum is at most one.
2. If `a=u` and `b` is integral, the support of `b` has size at most `r`,
   giving at most `r(1/r)^p_r=r^(1-p_r)<1`.
3. If `a` is integral and `b` is all-`1/2`, the clique has size at most two,
   giving at most `2(1/2)^p_r=2^(1-p_r)<1`.
4. For the two fractional vertices, the sum is exactly

   ```text
   (2r+1)(1/(2r))^p_r = 1,
   ```

   by the definition of `p_r`.

This proves Lemma 1.  The all-fractional pair also shows that its exponent is
best possible.

## 3. A common exponent for all permitted lengths

The function

```text
p(x) = log_x(x+1)
```

is strictly decreasing for `x>1`: differentiating reduces the sign to
`x log x < (x+1)log(x+1)`.  Therefore `p_r<=p_h` whenever `r>=h`.
After normalization every product `a_i b_i` lies in `[0,1]`, so Lemma 1
implies

```text
sum_i (a_i b_i)^p_h <= 1                            (10)
```

for every permitted odd hole and odd antihole.

For a perfect outer graph, (10) follows from Chvátal's polyhedral
characterization.  After `A=B=1`, the clique-normalized vector is a convex
combination of stable-set incidence vectors, so `sum_i a_i b_i<=1`; since
`p_h>1`, the sum of the `p_h` powers is also at most one.

We have therefore proved the common weighted inequality

```text
sum_i (a_i b_i)^p_h <= (A B)^p_h                   (11)
```

for every allowed outer quotient.

## 4. Sharp product and homogeneous-set theorem

### Theorem

Every nonempty `G in M_h` satisfies

```text
alpha(G) omega(G) >= |V(G)|^q_h,                    (12)
max(alpha(G),omega(G)) >= |V(G)|^(q_h/2).           (13)
```

Both exponents and the leading constant one are sharp.  The statements hold
for every nonempty induced subgraph of `G`.

### Proof

Induct through a substitution expression

```text
G = F(G_1,...,G_t).
```

Put `n_i=|V(G_i)|`, `a_i=alpha(G_i)`, and `b_i=omega(G_i)`.  Projection
through modules gives

```text
alpha(G) = max_(S stable in F) sum_(i in S) a_i = A,
omega(G) = max_(K clique in F) sum_(i in K) b_i = B.
```

By induction, `n_i <= (a_i b_i)^p_h`.  Summing and applying (11) gives

```text
|V(G)| <= sum_i (a_i b_i)^p_h <= (A B)^p_h.
```

Raise to `q_h=1/p_h` to obtain (12); (13) follows from the geometric mean.
Heredity of `M_h` gives the induced-subgraph statement.

For sharpness let `n=2h+1` and form the balanced two-level block

```text
Z_h = C_n(complement(C_n),...,complement(C_n)).
```

It has

```text
|V(Z_h)|=n^2,     alpha(Z_h)=omega(Z_h)=2h.
```

The `k`-fold lexicographic power of `Z_h` has order `n^(2k)` and both
parameters `(2h)^k`.  Hence equality holds simultaneously in (12) and (13)
for every `k`.  No larger exponent, or the same exponent with a leading
constant greater than one, is valid throughout `M_h`.

## 5. Scope

This is a sharp theorem for a hereditary modular host class.  It does not
prove the Erdős--Hajnal conjecture for a new fixed forbidden graph, and it is
not a theorem about all graphs excluding a long hole or antihole.  Those
statements have different quantifiers.  Its new content is the uniform
weighted odd-hole/antihole inequality, the exact length hierarchy, and the
sharp modular closure theorem.

