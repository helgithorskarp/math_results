# Exact physical order and unavoidable core of the EI interface assembly

This package closes the record-scale direct-overlap question for the reduced
Exoo--Ismailescu interface composition. It gives two exact results.

The target comparison is current as of 8 September 2026. Parts constructed a
[509-vertex, 2,442-edge five-chromatic unit-distance graph](https://arxiv.org/abs/2010.12665),
and Haugland's August 2026 paper still identifies 509 as the
[current unrestricted vertex record](https://arxiv.org/abs/2608.04542).

* Canonical realizations of the two minimum-support compositions have **48,405**
  and **48,365 distinct points**. They are non-four-colourable by the previously
  certified interface implications and T375 terminal theorem. The smaller
  realization replaces the formal attachment bound 320,517 by an exact physical
  order, but is far above 508.
* Every realization in the same staged architecture already has at least
  **755 distinct points** after the two G40 hosts and the orientation-independent
  parts of the 96 compulsory G49 attachments. This is before the five optional
  pairs per host and before any T375 attachment. Consequently no choice of
  reflections, endpoint orders, or coincident copies in this fixed staged
  mechanism can reach 508 by physical overlap alone.

The second statement is deliberately scoped. It is not a lower bound for
arbitrary unit-distance constructions, for subgraphs created by emergent
cross-edges inside the 48,365-point host, or for a replacement of G40, G49, or
T375. No graph on at most 508 vertices is obtained.

## Dependencies and conventions

The logical interface theorem is the hash-pinned
[53-pair/eight-triangle result](../hadwiger_nelson_ei_interface_minima/README.md).
It follows Exoo and Ismailescu,
[The chromatic number of the plane is at least 5 -- a new proof](https://arxiv.org/abs/1805.00157v1).
The terminal gadget is the hash-pinned
[T375 construction](../hadwiger_nelson_small_triangle_forcer375/README.md).
The present package imports exact arithmetic only after checking every file in
[dependency_hashes.json](dependency_hashes.json).

Coordinates are stored in
\(\mathbb Q(\sqrt3,\sqrt{11},\sqrt{247})\), scaled by 36. A plane point is a
pair of eight-coefficient vectors. All equality, distance, placement, union,
and hashing operations use exact rational arithmetic.

## The unavoidable 16-point kernel

G40 has 48 compulsory distance-pair premises. The two outer copies therefore
require 96 G49 attachments in every successful support. For a fixed unordered
host pair, there are four labelled G49 placements: two endpoint orders times
two reflections. Reflection across the terminal axis fixes each endpoint-order
support set, while the two endpoint orders give different sets. Their common
intersection contains exactly 16 points.

Any permitted G49 copy contains that 16-point kernel, transported to its host
pair. Thus the union of the two G40 hosts and all 96 transported kernels is a
subset of every staged realization, even when different formal copies overlap.

Up to a global plane isometry, the outer geometry has 32 cases. Normalize the
shared terminal to the origin and the first distant terminal to a fixed point.
The second distant terminal is one of the two circle intersections at radius
8/3 and distance 1 from the first. Each labelled G40 copy then has two terminal
orders and two reflections. Hence there are
\(2\cdot4\cdot4=32\) cases. Exact enumeration gives 79 outer G40 points and
755 points after the compulsory kernels in every case.

[direct_audit.py](direct_audit.py) independently rebuilds and intersects all
four G49 images at all \(32\cdot96=3,072\) pair occurrences. It agrees with
the transported-kernel computation at every case.

## Exact physical orders of both minimum supports

The two minimum G40 supports have masks 151 and 1682. Their exact canonical
orders are respectively 48,405 and 48,365. Both have 106 formal G49 attachments,
80 distinct support sets, 848 formal triangle obligations, and 642 distinct
physical target triangles. The G40/G49 layers have respectively 2,325 and 2,333
points; later coincidences make mask 1682 the smaller completed union.

One T375 copy per distinct target triangle suffices: its conditional statement
depends only on the physical marked triangle, so repeated obligations at the
same three points share the same copy. Attaching one exact isometric image to
each of the 642 triangles gives 48,365 distinct points. Extra coincidences and
extra unit edges cannot invalidate the restriction proof. The exact sorted
point-set hashes are pinned in [expected.json](expected.json).

## Reproduction and trust boundary

From this directory in a full repository checkout, run:

```bash
python3 -B verify.py
python3 -B direct_audit.py
python3 -B controls.py
python3 -O -B verify.py
sha256sum -c SHA256SUMS
```

Python 3.11+ and the standard library suffice. [verify.py](verify.py) checks
dependency hashes, reconstructs all 32 unavoidable cores, and constructs both
explicit unions. [direct_audit.py](direct_audit.py) performs the slower
definition-level intersection audit. [controls.py](controls.py) checks the
outer-circle normalization, enumerated case order, set-intersection identity,
and malformed inputs. Expected results and all source hashes are pinned.

The non-four-colourability conclusion depends on the published G40 and G49
interface implications and the T375 terminal theorem; those colour searches
are not rerun here. Remaining trust is the cited theorems, elementary finite
set and isometry arguments, CPython exact integer arithmetic, these checkers,
ordinary hardware, and the source transcriptions. There is no proof-assistant
formalization or external-author review claim.
