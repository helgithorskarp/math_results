# Native A159/B214 replacement of Parts136 has no receiving coupling

One fixed receiver-conditioned composition has **508 distinct plane points,
2,187 complete unit edges and chromatic number exactly four**. It retains the
reviewed Parts136 host and adds the archived A159 and B214 forcing gadgets in
their original displayed frames. The two donors have no point or unit contact
with each other. A159 meets the host only at their common origin, with no
additional cross edges; B214 is disjoint from the host and has no host edge.

Consequently **every proper four-colouring of the host extends**, and every
unrestricted relation projected onto host vertices remains unchanged. This
includes all 41,025 reviewed canonical boundary patterns. This is a fixed
construction stop, not a sub-509 five-chromatic graph or an exclusion of
arbitrary replacements for this receiver.

## Frozen geometry and why it was tested

Use the exact Parts509 row numbering. The host is

```text
H = {0} union {374,...,508}.
```

It has 136 points and 564 complete unit edges. The two sources are Parts's
archived `v159e646` nonmonochromatic square-root-seven triangle gadget A and
`v214e977` distance-three unequal-pair gadget B. Their different advertised
forcing features motivated testing their complete union against the reverse
receiver. No transfer of those properties into a new receiving relation was
assumed. The proof below needs neither advertised forcing predicate.

Every input point stays in its native frame. There is no rotation,
translation, deleted source point, optional contact, or search over placements.
The three exact intersections are

```text
H intersection A = {0},   H intersection B = {},   A intersection B = {}.
```

Thus the formal 136+159+214 labels merge to 508 points, with precisely 372
new physical points. The support contains 238 points outside the original
Parts509 parent and outside the registered 644-point quadratic switching
host. It therefore does not merely delete a critical-parent vertex or lie
in that known host. These scope checks were admission checks, not chromatic
signals.

The point tables use the real radical basis

```text
1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165)
```

for each of x and y. Parts509 coefficients have denominator 96; A and B
coefficients have denominator 12 and are multiplied by eight before merging.
The output order is the 136 host points in increasing parent order, the 158
nonorigin A points in source order, then all 214 B points in source order.
No floating-point equality or unit-distance predicate is used.

## Complete graph and universal extension

The checker decides all 128,778 unordered pairs and obtains:

| Edge class | Count |
|---|---:|
| internal to H | 564 |
| internal to A, including its origin edges | 646 |
| internal to B | 977 |
| additional physical edges | 0 |
| host--new edges, all already A's origin edges | 29 |
| new--new edges | 1,594 |

The true receiving interface is exactly the origin. In particular, the
nineteen pins of the original Parts136 cut do not become the interface of
this replacement merely because they were marked in the receiving table.

The certificate supplies a literal proper four-word on the entire graph.
Its restriction to H is the first two-colour boundary fixture from the
receiver package, with boundary pattern `0001010010101010101`. Its
restrictions to A and B are proper donor words. For any proper colouring of
H, globally rename the A word to match the colour of H's origin. Keep the
B word unchanged. The exact edge decomposition proves that these words glue
to a proper colouring of the entire union. This extends every host colouring,
not just the displayed fixture. Since the host itself is induced, the full
projected relation is unchanged in both directions.

The seven retained host vertices with output indices
`[0,25,35,86,24,34,97]` induce eleven edges and have no proper three-word,
checked by all 3^7 assignments. Hence the matching lower bound is four. A
literal proper five-word is also checked; it supplies only an upper bound.

## Reproduce

CPython 3.11 and the standard library suffice:

```sh
python3 -B verify.py --check-expected
python3 -O -B verify.py --check-expected
python3 -B controls.py
sha256sum -c SHA256SUMS
```

The public verifier imports no producer or sibling mathematical module. It
uses squarefree-radicand/gcd products, while the construction script used
subset-mask radical multiplication. They agree on the complete squared-
distance stream, point and edge streams, and byte-identical pinned CNFs.
The four mutation controls reject a bad private B-edge colour, an incorrect
host projection, a bad five-word and a duplicated lower-bound vertex.

For optional witness rediscovery, emit the original ordinary four-colour CNF:

```sh
python3 -B verify.py --emit-pinned-cnf /tmp/parts136-mixed.cnf
/path/to/kissat --time=60 /tmp/parts136-mixed.cnf
```

Variables `x(v,c)=4*v+c+1` encode exactly one of four colours per point.
Every physical edge forbids equal endpoint colours. The 136 unit assumptions
pin the complete supplied host word, not merely its nineteen-pin projection.
There are 2,032 variables and 12,440 clauses. Kissat 4.0.4 returned SAT in
about 0.080 seconds; its entire decoded word is checked literally. Solver
soundness or an UNSAT assertion is not a premise of this stopping proof.
The CNF hash is
`be20258ed3899f78f5661461166f66041a662ef6838698590d537af9c0354ab1`.
Generated CNFs and solver logs remain outside Git.

## Scope, provenance and trust

Retire this one native H/A/B composition. No alternate donor frame, translation,
root, source subset, additional layer or donor swap follows from the result.
The missing coupling is a geometric fact of this frozen placement. It is not
an impossibility theorem for internally interacting replacements, other
frames, or the reverse receiver in general. The earlier Parts373 receiver and
its failed replacements remain separately banked.

The existing mixed-gadget overlap censuses require at least two A/B overlaps
and therefore do not classify this zero-overlap native arrangement. The
reviewed E-field colouring covers the isolated native donor points; it does
not automatically cover their union with the rotated-field Parts136 host.
Neither fact substitutes for the complete reconstruction and word above.

Sources:

- [Parts136 receiver](../hadwiger_nelson_parts136_reverse_receiver/README.md),
  source `119e7444ff958ce30e017dbff9fddfe45f5915f2`.
- [Independent receiver acceptance](../hadwiger_nelson_parts136_reverse_receiver_review1/README.md),
  source `17d29aa89af4f9f09d932b23f0e158b8b9b36d0e`.
- [A159/B214 coordinate provenance](../hadwiger_nelson_nonmono159_214_lowden2/SOURCE.md),
  the published exact transcriptions of the Parts data archive.
- [Parts's paper](https://arxiv.org/abs/2010.12665) reports 509 points and
  2,442 edges. [Haugland v4](https://arxiv.org/html/2608.04542v4) explicitly
  retains 509 as the unrestricted record.

All coordinate inputs are hash-pinned. The argument trusts Python arbitrary-
precision integers, the radical-basis identities, the explicit checker,
the literal word and ordinary hardware. The public checker is distinct from
the construction's arithmetic; both were run by the author. No independent
review or proof-assistant formalization of this new stop is claimed. The
receiver's negative certificates are not needed for the universal extension
proof; only the attributed 41,025 count invokes that reviewed census.
