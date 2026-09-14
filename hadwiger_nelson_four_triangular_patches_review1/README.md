# Independent review: four concurrent P36 patches

## Verdict

**ACCEPT with high confidence for the exact continuum theorem**, at target
commit `3a921e44cca7cd5a56e71b0dc40ee5e68b9ae368`.

Let

```text
P36 = {a+b*omega : a^2+a*b+b^2 <= 36},
omega = (1+i*sqrt(3))/2.
```

For arbitrary unit complex numbers `alpha_0,...,alpha_3`, the complete strict
plane unit-distance graph on the physical union of the four concurrent
rotated patches `alpha_i P36` is four-colourable. Equal physical points are
merged and every physical unit pair is included. Such a union has at most 505
vertices.

This is a continuum restricted-family exclusion. It is not a global lower
bound, does not construct a five-chromatic graph, and does not improve the
509-vertex unrestricted record.

Reviewed package:
[`hadwiger_nelson_four_triangular_patches`](../hadwiger_nelson_four_triangular_patches/README.md).

## Mathematical reduction audited

The residue map `rho(a+b*omega)=a-b mod 3` separates each patch into a
zero-residue palette `{A,B}` and a nonzero palette `{+,-}`. Each layer has one
independent sign bit and one independent zero-class bit. Internal unit edges
are proper. A cross edge or physical coincidence imposes at most one XOR
equation of each type on its two layers; mixed-residue edges impose none.

For a relative rotation `alpha=x+i*sqrt(3)y`, every nonuniversal contact
between nonzero patch points lies on a rational line

```text
p*x + q*y = k,       x^2 + 3*y^2 = 1.
```

The review rederived this equation and generated its ellipse intersections
directly from every ordered point pair. Thus every phase capable of adding a
nonuniversal unit edge is in a finite exact inventory. Coincidences were also
derived independently as equal-norm ratios and checked as exact Cartesian
equalities.

Every one of the 594 raw event phases has internally consistent pair
requirements. Identical physical patches impose palette equality and may be
contracted. After such contractions, an inconsistent binary constraint graph
on at most four layer vertices contains either a conflicting pair, a simple
triangle, or a simple four-cycle. The pair case is excluded by the raw audit.
Modulo the six units preserving `P36`, the complete remaining census contains
186 active triangles and 8,100 four-cycle representatives. All corresponding
sign and zero systems are consistent. This closes the arbitrary continuum,
not merely the enumerated pictures.

## Clean-room exact computation

`independent_check.py` imports no target code and uses only the Python standard
library. Its main independent choices are:

- prime-support tuples for exact multiquadratic surds, rather than integer
  squarefree-radicand keys;
- direct contact-root generation for every ordered point pair, rather than
  first aggregating primitive lines;
- coordinate-key merging of coincident formal labels, rather than a declared
  coincidence DSU; and
- graph parity propagation, rather than exhaustive bit-word search.

It independently obtains:

- 127 patch vertices, 342 internal edges, and 139 vertices in `P37`;
- 528 primitive contact lines and 594 phases, split 162 rational / 432
  irrational;
- 99 phase classes modulo patch units, split 27 / 72;
- 54 coincidence phases;
- 186 normalized active triangles;
- 4,231 normalized length-two target classes and 8,100 four-cycles; and
- the active-interface histogram `5304,2472,324` for four, five, and six
  active interfaces.

All three entry-level author commitments are reproduced exactly:

```text
inventory  31285b4c110ec1cd5c06ee0c0a71f0d9014bcb91e8de6b59bddca28ddc8da34a
triangles  be221bdb1df2df0eca2b538058bdd97be6b087a4d52d501c0424cad2e0b1cea0
4-cycles   8915b9d8012d3e4653f3089feffe8c00aca6ea4d86fff6019a1a18420bfa8f8d
```

As an additional check absent from the target, the reviewer directly scans
all 3,114,297 unordered physical pairs in the 99 two-layer event
representatives. The direct strict unit-edge sets agree exactly with the
finite inventory. Their unions range from 127 to 253 vertices and from 342 to
702 edges. The review-only two-layer edge/colour commitment is
`8d98bf74ec93162982b0e8191c66452dc06e7cf8ac154da38def55a9fe160ecc`.

The independently reconstructed four-cycle representatives range from 451 to
505 physical vertices and 1,368 to 1,446 strict unit edges. Every coincident
label has one colour and every reconstructed physical edge is bichromatic.
No abstract chromatic graph is substituted for a plane realization.

## Reproduce

From the repository root with CPython 3.11 or later and only the standard
library:

```sh
python3 -B hadwiger_nelson_four_triangular_patches_review1/independent_check.py --check-expected
python3 -O -B hadwiger_nelson_four_triangular_patches_review1/independent_check.py --check-expected
```

The direct physical scans make this intentionally slower than the target
checker. `EXPECTED.json` pins every stable output field. The checker rejects
odd triangle and four-cycle parity controls and requires a consistent forest.

## Scope, graph context, and limitations

- The theorem requires four rotations of this radial `P36` patch about one
  common origin. It does not cover translations, four full triangular
  lattices, other 127-point selections, `P37`, five patches, or other scales.
- The cited committed three-patch theorem is related context, not a premise,
  and has no incoming committed objection in the stale local graph.
- The target contribution is pending rather than committed because Discovery
  Net remains stale at indexed height 4363.
- Primary-source evidence still identifies [Parts's 509-vertex,
  2,442-edge graph](https://arxiv.org/abs/2010.12665) as the unrestricted
  record. [Haugland's later paper](https://arxiv.org/html/2608.04542v4)
  explicitly cites Heule's 1,441-vertex graph as smaller than Haugland's 2,131
  vertices in the Moser-spindle-free restriction.

The remaining trust boundary is the elementary line/cycle reduction, two
reviewer-written exact implementations when combined with the target, normal
Python execution, deterministic enumeration, and SHA-256 collision
resistance. This is not a proof-assistant formalization and makes no historical
priority claim.
