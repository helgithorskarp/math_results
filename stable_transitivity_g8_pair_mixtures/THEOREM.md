# Exact stability on every degree-two mixture over `G8`

## Definitions

A `k`-tournament assigns nonnegative integral multiplicities summing to `k`
to the two orientations of every unordered vertex pair.  A transitive
tournament decomposition (TTD) is a sum of total orders.  Its stable-
transitivity number `m(W)` is the least `a` such that some `a`-tournament
`X` has a TTD and `W+X` also has a TTD.

On vertices `0,...,7`, fix the partial tournament

```text
G8 = {(0,1),(0,2),(0,3),(4,0),(6,0),(7,0),
      (1,3),(1,4),(5,1),(1,6),(7,1),(2,3),
      (2,4),(5,2),(6,2),(2,7),(3,5),(3,6),
      (3,7),(4,5)}.
```

The eight unspecified pairs, in certificate order, are

```text
(0,5),(1,2),(3,4),(4,6),(4,7),(5,6),(5,7),(6,7).
```

## Theorem

Let `W` be any 2-tournament whose multiplicity on each displayed arc of
`G8` is two.  The multiplicity of the increasing orientation on each of the
eight unspecified pairs may independently be `0`, `1`, or `2`.  Then

```text
m(W) = 3.                                                (1)
```

In particular, (1) holds for `W=T1+T2` for any two, possibly equal,
tournament completions of `G8`.  Conversely every `W` in the theorem is
such a sum, by choosing the two missing-edge orientations coordinatewise.

## Lower bound

Direct enumeration of the `8! = 40,320` total orders shows that each order
predicts at most 13 of the 20 arcs of `G8`.  Suppose an `a`-tournament
stabilizes `W`.  Reverse every order in its TTD.  The stabilization identity
then becomes a profile of `2+2a` total orders that predicts each fixed `G8`
arc exactly `2+a` times.  Counting predictions gives

```text
20(2+a) <= 13(2+2a),
```

so `a >= 7/3` and hence `a >= 3`.

## Upper bound certificate

Use the 28 increasing pair orientations as coordinates and let `1` be the
all-one vector.  Reversing orders shows that `m(W)<=3` is equivalent to an
eight-order profile with vector sum

```text
W + 3*1.                                                 (2)
```

For a fixed increasing `G8` arc, (2) requires count five; for a fixed
decreasing `G8` arc it requires count three.  If
`d=(d_0,...,d_7) in {0,1,2}^8` records the increasing multiplicities of the
unspecified pairs, their required counts are `3+d_i`.

`pair_profiles.txt` contains eight distinct total-order indices for every
one of the `3^8 = 6,561` vectors `d`.  `verify.py` independently enumerates
the 40,320 total orders, verifies that the certificate covers the ternary
box exactly once in lexicographic order, and checks all 28 equations for
each target.  Thus (2) holds for every `W`, proving `m(W)<=3`.  The lower
bound proves (1).

To recover an explicit stabilization from a certified profile, choose any
three of its eight orders for a set `R`.  Let `X` be the three reversed
orders from `R`, and let `Y` be the other five profile orders.  Equation
(2) gives `W+X=Y`.

## Exchange construction and semigroup interpretation

If two vertices are adjacent in a total order, swapping them changes only
their mutual pair coordinate.  When that pair is unspecified by `G8`, this
move preserves all 20 fixed counts and changes exactly one ternary target
coordinate by one.  Starting with checked profiles for the 256 corners
`{0,2}^8`, the deterministic exchange search in `generate_profiles.py`
reaches all 6,561 targets.  The published certificate records one final
profile per target, so the theorem does not depend on trusting the search.

Algebraically, total-order vectors generate an affine semigroup.  The
certificate says that every lattice point in the degree-two box on this
exposed `G8` face lifts to a degree-eight semigroup element.  It is a
mixture-saturation statement, not an enlargement of a diagonal-ray table.

## Literature status and scope

Davis and Schroeder introduced `m(W)` and asked for its growth in
*Relating tournaments and permutations with xrays*, arXiv:2606.21532v1.
Chindelevitch and Harutyunyan discuss the 20-arc obstacle `G8` and its
predictability `13/20` in *Tournaments determined by three and five voters*,
arXiv:2607.26690v1.  The versions checked on 2026-09-19 do not state (1) or
the degree-two mixture saturation above.  This is a search-relative
novelty statement, not a claim of historical priority.

The theorem concerns only 2-tournament extensions of this labeled `G8`
face.  It does not classify arbitrary 2-tournaments on eight vertices and
does not assert higher-degree box saturation.

Primary sources:

- https://arxiv.org/abs/2606.21532v1
- https://arxiv.org/abs/2607.26690v1

## Trust boundary

The proof trusts the displayed definition, `pair_profiles.txt`, and the
standard-library integer checker `verify.py`.  Floating-point optimization
was used during exploration only and is absent from the correctness
boundary.  `generate_profiles.py` and `corner_profiles.txt` provide an
exact reproducibility route but are likewise unnecessary once the final
certificate has been checked.
