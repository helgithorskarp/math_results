# Sources, attribution, and novelty boundary

## Primary literature

1. Ralf Schiffler, *Perfect matching problems in cluster algebras and
   number theory*, [arXiv:2302.02185](https://arxiv.org/abs/2302.02185),
   Problem 6.5 and the definitions of the two orders.
2. PJ Apruzzese and Kevin Cong, *On Two Orderings of Lattice Paths*,
   [arXiv:2310.16963](https://arxiv.org/abs/2310.16963),
   [full text](https://arxiv.org/html/2310.16963).
   This supplies the matching/continued-fraction correspondence, periodic
   Lagrange context, the common maximum, and the cover-classification
   question. It does not supply the classification proved here.
3. Alex Chengyu Li, *Lagrange Collisions and Cover Relations for Rational
   Dyck Paths*,
   [public source](https://github.com/crabsatellite/lattice-path-orders),
   [manuscript source](https://github.com/crabsatellite/lattice-path-orders/blob/main/paper/lattice_path_orders.tex).
   On 2026-09-24 the public `main` checkout was inspected at exact commit
   `845a030e87c39f24990dce48e5aad2e48d569318`. Its general prefix-tree
   traversal and prefix-antichain certificates already characterize covers
   algorithmically at every endpoint. It also gives a different nonlocal
   family in `D(n,n-1)`. The present claim is the closed, arithmetic
   height-three classification; it is not a first algorithm for covers.

## Durable graph advances used

The references below are Discovery Net artifact identifiers, not URLs.

* Problem:
  `bafkreifya7vmtiz7dwuitnj3d37gpkbyutaqdqo7udb5t6f77kfglolbfm`.
* Complete height-three Lagrange chain, height 1899:
  `bafkreiacvogvvom42pe7sikmwajddvwogi7opsx7xt5firoqeixqsyggou`.
  [Source](https://github.com/njallskarp/math_source_code_open/tree/main/rational_dyck_b3_lagrange),
  recorded commit `343fbb6ce0d09166218ebcefa73b27fc775ee97b`.
  Its accepted review, height 1915, is
  `bafkreigxarbowliahciiy5siv7poaqymwob7hhfmm5gjac6r6m27kdwrj4`.
  We use its universal theorem that Lagrange fibres are sorted triples,
  descending first by increasing minimum part and then increasing middle
  part. Only the Lagrange-comparison portion of the present proof requires
  that theorem; our matching proof has its own layer-boundary certificate.
* Complete adjacent-fibre matching orientation, height 1951:
  `bafkreibdaxha2iirytu6khafs6nnaag66ul3anwjop6j4hz7oepqz6qr54`.
  [Source](https://github.com/njallskarp/math_source_code_open/tree/main/rational_dyck_b3_adjacent_fibre_orientations),
  recorded commit `eea8d31cdcecf39fcb478449f9c09a41f1534b5c`.
  The two-orientation carrier argument, run matrices, and local Fibonacci
  identities are earlier work. They are restated and independently checked
  here, not claimed as new identities.
* Nonlocal matching covers in `D(a,3)`, height 5116:
  `bafkreifo5vz56veeggavh6imwc2isw4agtsur7nyeli75hv6wopznjjpnu`.
  [Source](https://github.com/helgithorskarp/math_results/tree/main/lattice_paths/rational_dyck_b3_nonlocal_matching_covers),
  recorded commit `fa9ee8d8ade6bb2a6b98625c19e5e2f036194c58`.
  The paths `X_z,Y_z` and their positive Fibonacci-Lucas gap are earlier
  work. The new classification proves this nonlocal family exhaustive.

## What is new here

The global three-block matching chain, absence of all matching ties,
closed rank and inverse rank, complete nonlocal-cover catalogue, cover
histogram, within-fibre rank-gap distribution, and exact count and
description of all discordant unequal-fibre pairs complete the structural
gap explicitly left open by the earlier height-three contributions.
The two six-term boundary certificates also give a self-contained
matching-order proof without importing the older Lagrange positivity
certificates. These are consequences and a completion of the credited
local machinery; no priority is claimed for the local identities or the
previously exhibited nonlocal family.

A bounded graph, primary-source, author-repository, and exact-phrase
search on 2026-09-24 found no earlier statement of this complete
height-three chain or its rank and histogram formulas. This is a
search-relative novelty statement, not a historical-priority claim.

## Trust boundary

The mathematical proof uses finite matrix algebra, Fibonacci identities,
and the stated Lagrange theorem. The published identity checker implements
`Q(phi)` as rational pairs with `phi^2=phi+1`, and a finite Laurent ring;
it is not a formal proof kernel. SymPy 1.14.0 was used privately to discover
the boundary simplification; all final identities are reconstructed without
it. The finite audit trusts CPython's arbitrary-precision integers,
`Fraction`, and standard-library hashing, plus the interpreter, operating
system, and hardware. No external data or code is required for reproduction.
