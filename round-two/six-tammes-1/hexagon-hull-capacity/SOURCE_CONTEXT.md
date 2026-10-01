# Source and scope

Author six-tammes-1, role researcher, 2026-10-01.

The compact coordinate fixture was downloaded from
[Sloane's fifteen-point coordinate file](https://neilsloane.com/packings/dim3/pack.3.15.txt).
A second live fetch on 2026-10-01 matched all 1215 bytes and SHA256
`d1a1d120faf0a7a69441fb8a42ea741da2209b5bd2c45819d16648a49fe0b10f`.
The checker treats its decimals as exact rationals, without trusting their
being exact unit coordinates or an exactly optimal configuration. The proof
is about those explicitly defined reference neighborhoods.

[Cohn's maintained table](https://cohn.mit.edu/spherical-codes/) retains the
unstarred N15 incumbent with cosine
0.59260590292507377809642492233276 and quintic
13t^5-t^4+6t^3+2t^2-3t-1. The
[larger code table](https://spherical-codes.org/) is complementary primary
construction data. The incumbent's approximate geodesic separation and
contact search quality are not proofs of global optimality.

[Musin--Tarasov, N14](https://arxiv.org/abs/1410.2536) proves N14 using
irreducible contact-graph enumeration. The
[irreducible-contact-graph paper](https://arxiv.org/abs/1312.5450),
Proposition 2.6, states the classical at-most-one-isolated-vertex result for
irreducible hexagonal faces. The restrictions "irreducible" and "isolated"
are preserved when describing that literature. A bounded primary-source
search did not locate this nine-template, displacement-tolerant polytope
certificate; no historical-priority assertion is made.

The [author's nonconvex covering theorem](../nonconvex-short-cycles/PROOF.md)
and [six-tammes-2's two-completion reduction](../../six-tammes-2/fourteen-point-completion/PROOF.md)
are complementary published work. This proof imports neither package's
arithmetic nor its mathematical claims. Only the coordinates and certificate
in this directory are required for reproduction.

The initial exact finite diagnostic at packing cosine 0.592606 and edge
threshold 0.592605 found 30 edges and 37 canonical simple six-cycles, of
which nine contained one reference-code point and none contained two.
Three enclosing cycles were convex and six concave. That diagnostic selected
the nine explicit patterns; it is not a proof of uniform capacity for all
six-cycles or a classification of all possible optimizers. The published
certificate independently proves a robust convex-hull restriction for each
listed pattern and does not require the diagnostic's exhaustiveness.
