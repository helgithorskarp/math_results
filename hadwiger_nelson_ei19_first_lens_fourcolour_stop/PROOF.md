# Proof and certificate semantics

## 1. Exact source

The sibling EI19 package defines 19 points as the unique zero, in a rational
box of radius `10^-25`, of the 34 non-anchor squared-unit equations.  Its
contraction proof is replayed after checking the SHA-256 hashes of both the
geometry certificate and checker.  It proves 19 distinct points, exactly the
35 source unit edges, and no other source contact.

The present checker also performs a complete DSATUR three-colour search on
those 35 edges.  Pinning the anchor edge to colours zero and one removes only
colour-name symmetry.  The search exhausts 152 nodes and fails, proving that
the source, and therefore the closure containing it, needs at least four
colours.

## 2. Complete first lens closure

For source points `a != b`, put `d^2=|b-a|^2`.  Outward interval arithmetic
proves `d^2 != 4` for every source pair and classifies exactly 165 pairs with
`d^2<4`.  Their unit circles meet in the two points

```text
(a+b)/2 +/- i(b-a) sqrt(1/d^2 - 1/4).
```

The formula has squared distance one from both centres because the two summands
are perpendicular and

```text
d^2/4 + d^2(1/d^2 - 1/4) = 1.
```

Pairs with `d^2>4` have no common unit neighbour.  Hence the 330 generated
labels are the complete first lens closure, not a selected subset.

## 3. A positive word without collision or edge assumptions

Let `X_i` be the outward coordinate rectangle for formal label `i`, and let
`c_i` be its stored colour.  The checker examines all 60,726 pairs.

If `c_i != c_j`, at least one coordinate projection of `X_i` and `X_j` is
disjoint.  Therefore two labels denoting the same exact point cannot receive
different colours.  The word descends to the collision quotient.

If `c_i = c_j`, the full outward interval for squared distance between
`X_i` and `X_j` excludes one.  Consequently no actual unit pair is
monochromatic.  This includes every incidental lens--lens and source--lens
contact, whether or not it appeared in the numerical selector.

Thus the complete physical graph is four-colourable.  Together with the
embedded EI19 lower bound, its chromatic number is exactly four.

## 4. Outward arithmetic

Every interval endpoint is an integer over `Q=2^160`.  Rational conversion,
addition, subtraction, multiplication, squaring, reciprocal, division and
square root all round outwards using integer floor/ceiling division and
`isqrt`.  No fixed-width integer or floating-point operation occurs in the
proof checker.

The smallest certified same-colour squared-unit exclusion and
different-colour coordinate separation are recorded exactly in
`EXPECTED.json`.  Their positivity, rather than their decimal size, is the
proof obligation.
