# Long-cycle restrictions on automorphisms of a hypothetical Ramsey(5,5,43) graph

Let `G` be a graph on 43 vertices with neither a clique nor an independent set
of size five.  The established equality `R(4,5)=25` forces

```text
18 <= degree_G(v) <= 24
```

at every vertex.  This elementary degree window has two useful automorphism
consequences:

1. no automorphism of `G` can simultaneously fix a vertex and have another
   cycle of length at least 25; and
2. no automorphism of `G` can contain a cycle of prime length
   `29`, `31`, `37`, or `41`, regardless of its other cycles.

Together with the separately certified
[`C_43` circulant classification](../ramsey_r55_circulant43_classification),
which excludes an automorphism containing a 43-cycle, this rules out every
prime cycle length at least 29 in the color-preserving automorphism group of a
hypothetical 43-vertex target.

These are proof-level necessary conditions, not a construction and not a
change to the known bounds for `R(5,5)`.

## The degree window

Fix a vertex `v`.  Its open neighborhood induces no `K_4`, because such a
`K_4` together with `v` would be a `K_5`, and it induces no independent
five-set because `G` has none.  Since `R(4,5)=25`,

```text
degree_G(v) <= 24.
```

Apply the same argument after complementing `G`.  Equivalently, among the
`42-degree_G(v)` nonneighbors of `v` there can be neither a `K_5` nor an
independent four-set (the latter would join `v` to make an independent
five-set).  Thus

```text
42 - degree_G(v) <= 24,
```

which gives the lower bound 18.

## Fixed point versus a long cycle

Let `sigma` be an automorphism, let `v` be fixed by `sigma`, and suppose that
`C` is a cycle of `sigma` with length `m >= 25`.  Adjacency from `v` is
constant on `C`: invariance under `sigma` makes `v` adjacent either to every
vertex of `C` or to none.

In the first case, `degree_G(v) >= m >= 25`, contradicting the upper degree
bound.  In the second case, all neighbors of `v` lie among the other
`42-m <= 17` vertices, contradicting the lower degree bound.  This proves the
first claim.  Notice that the remaining vertices may lie in arbitrary cycles;
they need not be fixed.

## Large prime cycles

Suppose an automorphism `sigma` has a cycle of prime length

```text
p in {29,31,37,41}.
```

Let the other cycle lengths be `r_1,...,r_t` and set

```text
L = lcm(r_1,...,r_t),
```

with `L=1` if there are no other cycles.  Each `r_i` is smaller than `p`, so
the prime `p` does not divide `L`.  The power `tau=sigma^L` therefore fixes
every vertex outside the `p`-cycle while acting on that cycle as another
`p`-cycle.  There is at least one outside vertex because `p<43`.  The
fixed-point/long-cycle obstruction applied to `tau` gives a contradiction.

For `p=43`, an order-43 permutation on 43 vertices is a single 43-cycle.  A
coloring invariant under it is circulant after relabeling, and the complete
`2^21` classification in the linked contribution proves that every such
coloring has at least 43 monochromatic `K_5`s.

## Scope and provenance

The only imported theorem in the degree argument is McKay and Radziszowski's
exact value
[*R(4,5)=25*](https://doi.org/10.1002/jgt.3190190304); their
[author-hosted paper](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf)
is also directly available.  The rest is a finite group-action argument.

This note does not classify all possible automorphism cycle types.  Composite
cycles at least 25 can evade the powering argument when their lengths share
factors with other cycles, and cycles of length at most 24 are untouched.
The result is best used as an exact pruning rule in structured or
isomorph-free construction searches.  The derivation is apparently absent
from the inspected Discovery Net `R(5,5)` neighborhood; no historical-priority
claim is made for this elementary corollary.
