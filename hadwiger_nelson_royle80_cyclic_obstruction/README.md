# Royle-80 cyclic unit-distance obstruction

This package closes a natural target-scale realization family for the
Hadwiger--Nelson problem.  The 80-vertex Royle graph is a positive abstract
source: Exoo and Goedgebeur report that it is 5-chromatic, 8-regular, and of
girth 5.  If this graph admitted a plane unit-distance realization, it would
be far below Parts's 509-vertex benchmark, still identified as the record in
[Haugland's 17 August 2026 survey](https://arxiv.org/html/2608.04542v4#S1).

The exact result here is narrower and negative:

> The Royle graph has no injective edge-preserving unit-distance realization
> in the plane that carries its displayed semiregular automorphism
> `v -> v+4 mod 80` to a Euclidean isometry.

Only four of the graph's 16 edge orbits are needed.  Two self-orbits force the
squared radii of the first two 20-cycles to sum to one.  Two cross-orbits then
force the same pair of nonzero orbit vectors to be perpendicular before and
after an 11-step rotation.  No primitive order-20 rotation permits this.
[PROOF.md](PROOF.md) gives the full argument.

## Source graph

The LCF table is Table 4 of Geoffrey Exoo and Jan Goedgebeur, “Bounds for the
smallest k-chromatic graphs of given girth,” *Discrete Mathematics &
Theoretical Computer Science* 21(3), 2019,
[doi:10.23638/DMTCS-21-3-9](https://doi.org/10.23638/DMTCS-21-3-9),
[paper](https://dmtcs.episciences.org/5259/pdf).  Their LCF convention says an
entry `t` in row `i` supplies all edges
`{i+4j, i+4j+t}` modulo 80 for `0 <= j < 20`.

The local verifier reconstructs this table and confirms 80 vertices, 320
edges, degree 8, girth 5, the 20-fold automorphism, all 16 edge orbits, and a
proper five-colouring.  The lower bound `chi(G)>=5` is imported from the cited
peer-reviewed source; this compact package does not independently replay that
source's exhaustive four-colourability computation.

## Reproduction

Python 3.10 or newer is sufficient; the verifier uses only the standard
library.

```bash
python3 -B verify.py
python3 -B controls.py
sha256sum -c SHA256SUMS
```

The first command must end with
`VERIFIED_ROYLE80_C20_EQUIVARIANT_OBSTRUCTION`.  The second replays the valid
certificate and confirms rejection of altered LCF, colouring, and proof-orbit
certificates.  `EXPECTED.json` pins the complete verification receipt.

## Scope

The theorem decides the symmetry-preserving four-orbit realization family.  It
does not rule out an asymmetric realization of the Royle graph, and it does
not produce a new plane unit-distance graph or improve the 509-vertex record.
