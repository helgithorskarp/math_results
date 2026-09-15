# Exact four-colour stop for the fixed fish commutative self-sum

This package closes one bottom-up Hadwiger--Nelson construction probe.  Let
`F` be the exact 23-point, 42-edge Hochberg--O'Donnell fish realization
isolated by the rational contraction certificate in the sibling directory
`hadwiger_nelson_fish_spindle_pair_gate`.  The complete strict unit-distance
graph on

```text
F + F = {p_i + p_j : 0 <= i <= j < 23}
```

is four-colourable.  Consequently this exact capped whole support is **not** a
five-chromatic plane unit-distance graph and is not record progress.

## Certificate idea

There are 276 unordered sum addresses.  The source certificate places each
fish coordinate within `10^-25` of a rational midpoint, so every sum
coordinate is within `2*10^-25` and every difference coordinate is within
`4*10^-25` of its rational midpoint.

The verifier uses only rational arithmetic to:

1. cluster addresses whose coordinate boxes can overlap;
2. prove that points from different clusters cannot coincide and that points
   within one cluster cannot be at unit distance;
3. include an edge between clusters whenever the rigorous squared-distance
   interval for any address pair contains one; and
4. check a four-colour word on this conservative supergraph.

The calculation produces 262 possible-equality clusters and 915 conservative
possible-unit cluster edges.  Because all addresses in a cluster receive the
same colour, the colouring is well-defined after every actual collision.
Because every actual unit contact is among the conservative edges, it is a
proper four-colouring of the complete physical strict unit graph even though
the verifier need not symbolically decide the remaining near identities.

This is a whole-support negative certificate, not a restricted-family claim
about arbitrary fish placements or arbitrary Minkowski sums.

## Replay

From the repository root, using only Python 3's standard library:

```bash
python3 hadwiger_nelson_fish_selfsum_fourcolour_stop/verify.py
```

Expected headline:

```text
EXACT FISH SELF-SUM FOUR-COLOUR STOP VERIFIED
```

The verifier checks all 37,950 unordered address pairs, the source certificate
hash, the conservative graph hash, the interval margins, the supplied colour
word, and exact agreement with `EXPECTED.json`.
