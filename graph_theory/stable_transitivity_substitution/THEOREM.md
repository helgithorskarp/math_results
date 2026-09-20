# Stable transitivity is exact under tournament substitution

## 1. Definitions

Fix an integer `k>=1`.  A **`k`-tournament** `T` is a complete directed
multigraph in which the multiplicities of `x->y` and `y->x` sum to `k` for
every distinct pair `x,y`.  It has a **transitive tournament decomposition**
(TTD) if it is the sum of `k` transitive tournaments, equivalently of `k`
total orders on its vertex set.

The **stable-transitivity number** `m(T)` is the least `a>=0` such that some
`a`-tournament `A` has a TTD and `T+A` has a TTD.  Thus there are total
orders `L_1,...,L_a` and `M_1,...,M_(k+a)` for which

```text
A     = L_1 + ... + L_a,
T + A = M_1 + ... + M_(k+a).                       (1)
```

Let `Q` be a `k`-tournament on `[r]`, and let `T_i` be `k`-tournaments on
pairwise disjoint nonempty vertex sets `V_i`.  Their **substitution**

```text
Q[T_1,...,T_r]
```

is the `k`-tournament `G` that equals `T_i` within `V_i` and, for
`x in V_i`, `y in V_j`, has exactly `Q(i,j)` copies of `x->y`.  Cross-block
multiplicities therefore depend only on the two blocks.

## 2. Exact substitution theorem

**Theorem 1 (substitution maximum).**

```text
m(Q[T_1,...,T_r]) = max(m(Q),m(T_1),...,m(T_r)).    (2)
```

**Proof: lower bound.**  Suppose `A` is an `a`-tournament witnessing
`m(G)<=a`.  Restrict both TTDs in (1) to one representative vertex from each
block.  The restriction of `A` has a TTD, the restriction of `G+A` has a
TTD, and the restriction of `G` is `Q`.  Hence `m(Q)<=a`.

Restricting instead to all vertices of `V_i` shows `m(T_i)<=a` for every
`i`.  Consequently the right side of (2) is at most `m(G)`.

**Proof: upper bound.**  Put

```text
a = max(m(Q),m(T_1),...,m(T_r)).
```

A witness of degree `b<a` can be padded to degree `a`: add the same arbitrary
`a-b` total orders to its stabilizer TTD and to the completed TTD.  We may
therefore choose degree-`a` witnesses and write

```text
A_Q       = L_1 + ... + L_a,
Q + A_Q   = M_1 + ... + M_(k+a),

A_i       = L_(i,1) + ... + L_(i,a),
T_i + A_i = M_(i,1) + ... + M_(i,k+a).             (3)
```

For each `s=1,...,a`, form a global order `N_s` as follows: order the blocks
according to `L_s`, and within block `i` use `L_(i,s)`.  Concatenating these
block orders gives a total order on all vertices.  The sum of the `N_s` is
an `a`-tournament `A` with a TTD.  Its restriction to a block is `A_i`, and
its multiplicities between every pair of blocks are those of `A_Q`.

Similarly, for each `t=1,...,k+a`, order the blocks according to `M_t` and
use `M_(i,t)` inside block `i`.  The resulting global orders have, by (3),
the arc multiplicities of `G+A` both within every block and between every
two blocks.  They are a TTD of `G+A`, so `m(G)<=a`.  Together with the lower
bound this proves (2).  The case `a=0` is the same argument with an empty
stabilizer. `square`

## 3. Strong-component localization

For a `k`-tournament `T`, let its **support digraph** contain `x->y` exactly
when that arc has positive multiplicity.  Let `C_1,...,C_s` be its strongly
connected components.

Between two distinct components all support arcs have one common direction.
Indeed, an arc in each direction (even on different vertex pairs) would give
a directed two-cycle between the corresponding vertices of the condensation,
contrary to its acyclicity.  Since every vertex pair has total multiplicity
`k`, every cross-component pair has all `k` arcs in that common direction.
The condensation is therefore an acyclic tournament, hence a transitive
tournament.  Thus `T` is a substitution into a transitive quotient, also
called the ordinal sum of its strong components.

Applying Theorem 1 gives the following exact formula.

**Corollary 2 (strong-component localization).**

```text
m(T) = max { m(T[C]) : C is a support strong component of T }.       (4)
```

In particular, if

```text
m(n,k) = max { m(T) : T is a k-tournament on n vertices },
```

then

```text
m(n,k) = max { m(W) : W is a strongly connected k-tournament
                        on s vertices for some 1<=s<=n }.            (5)
```

The forward inequality follows from (4).  Conversely, any strongly connected
`W` on `s<=n` vertices can be padded by `n-s` ordered singleton components;
(4) says that the resulting `n`-vertex tournament still has value `m(W)`.
Consequently `m(n,k)` is nondecreasing in `n`.

## 4. Exact infinite extensions of known obstructions

The accepted order-eight computation in
[`stable_tournaments_order8`](../stable_tournaments_order8) exhibits 96
ordinary tournaments `W` with `m(W)=2`.  By taking an ordinal sum with any
number of singleton vertices, (4) gives an explicit ordinary tournament of
every order `n>=8` whose stable-transitivity number is **exactly** `2`, not
merely at least `2` by induced restriction.

The separately proved complete `G8` mixture theorem in
[`stable_transitivity_g8_all_mixtures`](../stable_transitivity_g8_all_mixtures)
states that every degree-`k` extension `W` of `G8` satisfies
`m(W)=ceil(7k/6)`.  Hence for every `k>=1` and `n>=8`, every ordinal-sum
padding of such a `W` has the same exact value.  This second consequence
depends on that computer-assisted `G8` theorem; Theorem 1 and Corollary 2 do
not.

## 5. What is proved structurally and what is checked computationally

Theorem 1 and its corollaries are purely structural and parameter-uniform:
they apply to every degree, quotient size, block size, and number of blocks.
No computation is used in their proof.

`verify.py` is an independent, definition-level finite audit.  It enumerates
all substitutions of ordinary tournaments through total order five and of
`2`-tournaments through total order four.  It computes `m` directly from
TTD profile sets and checks (2).  It also enumerates every tournament in the
same ranges, computes support strong components, and checks (4).  This audit
tests the implementation-facing definitions and boundary cases; it is not a
substitute for the universal proof.
