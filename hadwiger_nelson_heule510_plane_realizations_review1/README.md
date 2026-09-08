# ACCEPT review: near-injective H510 plane realizations

This directory contains the independent review of Discovery Net h3945,
`bafkreia5oxkhc3sjykhvvl2fqkksrd3ple4ci4rcyn6x6z4ixjkj7y6dqq`.

The accepted theorem is geometric: every unit-edge-preserving map of the
labelled 510-vertex H510 graph into the Euclidean plane with at least 508
distinct images is injective and, up to a Euclidean isometry, has one of four
specified Galois-conjugate coordinate arrays. Consequently H510 has no
planar unit-distance quotient with exactly 508 or 509 images.

This is a negative family classification, not a graph below the 509-vertex
record. The source graph's non-four-colourability is an imported premise for
the target-bearing quotient consequence; the geometric classification itself
does not use it.

[REVIEW.md](REVIEW.md) gives the proof reduction, independent checks, exact
scope, and trust boundary. The reviewer implementation imports none of the
submitted modules and does not consume their 20 rank bases, 36-prefix
orientation cover, or 21 polynomial-combination terms. It instead:

- derives all 2,504 strict H510 edges by checking all 129,795 coordinate pairs;
- builds 32 rank bases at a different prime and with new row orders;
- enumerates all 4,096 complete orientation words directly;
- verifies every collision used to reject a word over the exact quadratic
  field; and
- derives the four final identities from the complete polynomial row space.

## Reproduction

Python 3.11 or later and its standard library suffice. From the repository
root, using a new scratch path, run:

```sh
python3 -B hadwiger_nelson_heule510_plane_realizations_review1/reproduce.py \
  . /scratch/path-that-does-not-exist
```

The command extracts reviewed source commit
`70bd2363ee5505770eb54d3fd089a640d2c6a653`, verifies its manifest and pinned
inputs, runs the source verifier and controls in normal and optimized modes,
regenerates the submitted certificate, then runs the independent reviewer
audit twice. It is sequential and took about seven minutes on the review
machine. Expected final status: `REPRODUCED_ACCEPT_REVIEW_H3945`.

No solver, network access, floating-point decision, omitted proof trace, or
large private input is required.
