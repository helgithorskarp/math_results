# Provenance

## Reviewed artifacts

- Geometry certificate SHA-256:
  `e079c2d86f0b3574e6e24d9fc18a9abc2d8b7d7fe111ba011d5978875d5fc732`.
  It first entered the repository at
  `4e900a233cd6de3ced408cfb81bd9b25844afc2b`.
- Relation certificate SHA-256:
  `ffc789b63d1818f91d5fedb30bcc17996c26bb4de254602fb414115ab81554ac`.
  It entered at `a0fa3ac2b53ab0d538ec376a5fbe011accd41665`.

The review pins bytes, not a moving branch tip.

## External source integrity

The target attributes the flexible parameterization to Parcly Taxel's Shibuya
implementation.  The review retrieved

<https://raw.githubusercontent.com/Parcly-Taxel/Shibuya/218097c9971db2b60ab94a0b8dae20d76741cc43/shibuya/graphs/pegg.py>

and independently obtained SHA-256
`2ba335b24fd02294030595d9b0ae055b30b10b4dfc886f183eb27321c0de75c1`,
matching the target provenance.  The fish edge set in `verify.py` is rebuilt
from that routine's construction operations and closure equations.

The original graph attribution is R. Hochberg and P. O'Donnell, *Some
4-Chromatic Unit-Distance Graphs without Small Cycles*, Geombinatorics 5
(1996), 137--141.  The review does not claim novelty for the fish or its
flexibility.

## Record sources

- J. Parts, [Graph minimization, focusing on the example of 5-chromatic
  unit-distance graphs in the plane](https://arxiv.org/abs/2010.12665).
- E. Haugland, [A Moser-spindle-free 5-chromatic unit distance graph on 2131
  vertices in the plane](https://arxiv.org/abs/2608.04542).

These support the bounded record statement in the README.  No inference from
the local Discovery ledger is used to establish publication priority.
