# Cross six-cycles force preservation of the source field

**Theorem.** Let `F` be a real subfield, `K=F(i sqrt(3))`, and `P,Q subset K`.
If an arbitrary Euclidean isometry `g` places an alternating unit six-cycle
on six distinct points of `P union g(Q)`, then `g(K)=K`.

The cycle need not be induced. The theorem does not require connected
source graphs, bounded denominators, bounded order, or disjointness away
from the six selected points. Reflections are included.

For `E=Q(i sqrt(3),i sqrt(11))`, the established field colouring then
four-colours the **entire strict union graph**. Thus every cross-six-cycle
placement of the fixed alternative `B292/V214` construction is closed,
including every disjoint 506-vertex such placement. Four-colourability of
arbitrary `F(i sqrt(3))` is not asserted.

[PROOF.md](PROOF.md) gives the uniform argument. Circle-intersection
centres over the source field are quadratic. Centres of two pairs that
share a point cannot generate different quadratic extensions when their
squared separation lies in the real source field. This puts the isometry
in one quadratic extension. Outside the field-preserving case, the
six-cycle would then lie on two lines through a common field point.
The six unit equations force a primitive cube-root multiplier between the
two triples, placing the moving vertices back in the source field.

Combined with the prior
[four-cycle gluing](../hadwiger_nelson_cross_four_cycle_gluing/README.md)
and [single-hub reduction](../hadwiger_nelson_mixed506_single_hub_reduction/README.md),
a non-four-colourable disjoint mixed506 placement must have no cross cycle
of length four or six and at most one cross-degree-at-least-three vertex,
of degree at most ten. In the absence of a hub, its nontrivial cross
components are paths or even cycles of length at least eight.

**No five-chromatic graph or record improvement is produced.** The remaining
cycles and acyclic attachments are not classified here. No teammate pool
or parked Parts overlap family is enumerated.

## Reproduction

Use Python 3.11 or later, standard library only, from this directory:

```sh
python3 identities.py > /tmp/cross-six-identities.json
cmp expected_identities.json /tmp/cross-six-identities.json
python3 examples.py > /tmp/cross-six-examples.json
cmp expected_examples.json /tmp/cross-six-examples.json
python3 audit_examples.py > /tmp/cross-six-audit.json
cmp expected_audit.json /tmp/cross-six-audit.json
sha256sum -c SHA256SUMS
```

- `identities.py` expands 11 polynomial identities in a sparse rational
  polynomial ring. It verifies the circle-offset norm, coefficients for
  two independent quadratic centres, the orthogonality determinant, the
  cross-edge minimal-polynomial reduction, and the six-cycle eliminations.
- `examples.py` constructs eight exact small geometries in
  `Q(i,sqrt(3),sqrt(5),sqrt(11),sqrt(13))`. It checks strict unit edges,
  physical point identifications, alternating six-cycles and explicit
  proper colourings. Field membership is decided in the exact radical
  basis, not from approximate coordinates.
- `audit_examples.py` imports neither program. It reconstructs every
  example's squared distances from rational Gram formulas and trigonometric
  values at multiples of 60 degrees. A depth-first traversal counts the
  cycles, independently of the generator's `K3,3` matching method. Every
  edge stream, point identification, colouring and cycle count agrees.
  It checks 124 pairs of source-labelled points, or 112 pairs after the
  physical identifications in the eight separate examples.

All three programs ran in under 0.06 seconds each on the producing host
with CPython 3.11.2. The maximum child peak RSS across the serial workflow
was 15,544 KiB. Runtime is not a proof assumption.

These are checks of identities, examples and implementation boundaries.
**The uniform theorem is proved in the document; it is not inferred from
eight examples or an exhaustive placement search.**

## Boundary evidence

The examples include a regular hexagon, a reflected hexagon, a connected
seven-point wheel with an overlapping component centre, and a collinear
six-cycle. Two exact paths exercise an external translation and a
non-base quadratic rotation, including a path through the common centre.

The boundary controls are explicit:

- The source triple `{3/7,5/7,-8/7}` and multiplier `(-1+i sqrt(3))/2`
  give a six-cycle but do not preserve `Q(i)`. The specified field
  hypothesis therefore cannot simply be dropped.
- `P={+/-i sqrt(3)/4}`, `Q={+/-(1+2i sqrt(3))/4}`, and
  `u=(1-2i sqrt(3))/sqrt(13)` give a cross four-cycle with `u outside E`.
  This separates field preservation from the prior four-colourability
  theorem for cross four-cycles.
- Two pairs with the same midpoint have centres in different quadratic
  extensions and squared separation `7/4`. This checks the exception that
  the shared-vertex lemma excludes.
- A labelled six-cycle with a repeated plane point is rejected as a
  six-distinct-point witness. In the wheel, 16 labelled cycles reduce to
  seven valid six-distinct-point cycles; the folded control has one
  labelled cycle and none on six distinct plane points.

`expected_examples.json` contains explicit colour sequences and complete
cross-edge lists. Strict edges are hashed as sorted `i,j` lines, with
source order first `P`, then previously unseen points of `g(Q)`.
The certificate is compact; no graph dump or external solver trace is used.

## Dependencies and trust

The geometric theorem is self-contained apart from elementary field and
plane geometry. Its `E`-colourability application uses the independently
reviewed [field theorem](../hadwiger_nelson_nonmono_field_obstruction/PROOF.md).
The combined residual statement additionally uses the two earlier
structural theorems linked above. Source gadget
[provenance](../hadwiger_nelson_nonmono159_214_lowden2/SOURCE.md) and the
[fixed inner construction](../hadwiger_nelson_nonmono159_moser_triple/PROOF.md)
are unchanged. These documents are pinned in the manifest.

The proof is unformalized. The checks use exact rational arithmetic and
ordinary Python execution and are author cross-checks, not external peer
review. They do not machine-check the field-independence or geometric
quantifiers. No priority claim is made for the elementary mechanisms.
