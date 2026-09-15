# Proof and trust boundary

## 1. Exact planar realization

Represent an element of `K=Q(sqrt(3),sqrt(11))` by its four rational
coefficients in the basis `(1,sqrt(3),sqrt(11),sqrt(33))`.  In the supplied
source all coordinate coefficients are integers divided by 12.  Addition and
subtraction preserve this representation.

For two distinct unit vectors `p-r` and `q-r`, put `x=p+q-r`.  Then

```text
x-p = q-r,   x-q = p-r,
```

so both have norm one.  Therefore every generated label is a genuine plane
point with its two prescribed contacts.  Exact coefficient equality merges
collisions.  After each simultaneous round the verifier discards ownership
information and checks all unordered pairs by expanding `dx^2+dy^2` in the
four-element basis.  Linear independence of that basis over `Q` makes the
test exact.

This establishes the coordinate and complete-edge claims summarized in the
three certificate rows.  It also proves the natural next-round count 1,020;
that count is a budget boundary, not a chromatic assertion about the next
round or its subsets.

## 2. Strict colour-relation inclusions

A named four-colour relation on `A subset B` is the image of the proper
four-colourings of `B` under restriction to `A`.  Restriction is always a
subset of the proper colourings of `A` because all strict unit edges induced
on `A` remain present.

For each claimed strict inclusion, the certificate contains:

1. a proper named four-colouring of the smaller support;
2. a sound unit-propagation contradiction when its singleton colours are
   imposed on the larger exact graph; and
3. a proper four-colouring of the larger graph, proving its relation is not
   empty.

The propagation rule is elementary.  If a neighbour is fixed to colour `c`,
delete `c` from the current vertex's list.  A singleton list fixes its vertex
and can be used in the same way.  An empty list is impossible in any extension.
The checker records and revalidates an adjacent singleton for every deletion;
the first and second witnesses reach empty lists after respectively 20 and 40
deletions.  This is a positive, locally checkable impossibility certificate,
not a trusted SAT `UNSAT` verdict.

The checked `S2` word supplies the required nonempty relations by restriction.
The two inclusions are therefore strict.

## 3. Exact chromatic number

The `S2` word is a proper four-colouring of all 2,084 reconstructed edges and
restricts to the earlier supports.  Conversely `S0` contains the seven source
vertices of a Moser spindle.  Their complete strict graph has eleven edges.
The checker exhausts all 2,187 named three-colour assignments and finds none
proper.  Hence each of `S0,S1,S2` has chromatic number exactly four.

## Trust boundary

The proof trusts the displayed reflection identity, linear independence of
the standard multiquadratic basis, Python integer arithmetic, SHA-256 for
identity checking, complete finite loops and ordinary hardware.  The sibling
source certificate is hash-pinned and only its listed exact coordinates are
used; its earlier colouring theorem is not imported.  No floating predicate,
SAT result, hidden graph file, abstract realization, formal proof assistant or
independent review is a premise.

The theorem is scoped to the frozen source and two simultaneous rounds.  It
does not imply that the full plane graph is four-colourable, that every
reflection construction is four-colourable, or that a sub-509 five-chromatic
graph does not exist.
