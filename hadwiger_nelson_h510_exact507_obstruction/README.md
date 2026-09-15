# Heule H510 has no plane unit-edge map with exactly 507 images

Let `H510` be Marijn Heule's 510-vertex, 2,504-edge five-chromatic
unit-distance graph in the exact labelled form pinned by the accepted parent
package.

**Exact computer-assisted theorem.** There is no map

```text
p : V(H510) -> R^2
```

taking every source edge to distance one and having exactly **507 distinct
images**. The map is allowed arbitrary real coordinates, arbitrary extra unit
distances, and arbitrary identifications of nonadjacent source vertices.

The accepted predecessor already excludes 508 and 509 images and classifies
the 510-image drawings. Together, the two results imply that every
noninjective plane unit-edge map of `H510`, if one exists, has at most **506**
images. This is a negative realization theorem, not a five-chromatic plane
graph and not an improvement on the published 509-vertex record. Maps with at
most 506 images remain open.

## Reduction at collision deficit three

Exactly three lost images give one of three fibre shapes:

```text
(4,1,...,1),  (3,2,1,...,1),  (2,2,2,1,...,1).
```

The parent certificate supplies 20 independently checked bases of 501
rhombus equations. A rhombus equation can fail only when one of its two
opposite source pairs is identified. For a proposed fibre partition, mark the
parent bases hit by its failed equations.

If some basis is unhit, the map lies in the parent's full rank-nine linear
kernel. Its complete orientation tree has 34 rejected prefixes and two
survivors. Each rejected prefix forces three image losses. At the exact-507
boundary those are the whole collision partition; 18 prefixes collapse a
source edge and 16 give a quotient `K2,3`. The two survivors are the parent's
four injective Galois drawings.

If all 20 bases are hit, the verifier exhausts the three fibre shapes. All
rank-defect candidates are impossible:

| non-singleton fibre shape | candidates | source-edge collapse | quotient `K2,3` |
|---|---:|---:|---:|
| three pairs | 35,854 | 4,056 | 31,798 |
| triple and pair | 4,094 | 59 | 4,035 |
| quadruple | 1,931 | 0 | 1,931 |

The enumeration has 8,486 three-row covers. Four triples already hit every
basis. Quadruple fibres whose obstruction needs at least four rows are found
by an independent dense-opposition enumeration of 1,897,832 four-sets before
the rank mask test.

The apparently infinite “arbitrary last collision” branches are finite. When
two rows, or a triple alone, already hit all bases, the partial quotient has a
literal `K2,3`. A final identification can remove that witness only by merging
its two degree-three vertices or two of its three common neighbours. The
verifier checks precisely these four quotient-class pairs. This is a necessary
condition, not a heuristic.

The complete argument is in [PROOF.md](PROOF.md).

## Reproduce

Python 3.11 or later and the standard library suffice. From the repository
root:

```bash
python3 -B hadwiger_nelson_h510_exact507_obstruction/verify.py --check-expected
python3 -O -B hadwiger_nelson_h510_exact507_obstruction/verify.py --check-expected
python3 -B hadwiger_nelson_h510_exact507_obstruction/controls.py
sha256sum -c hadwiger_nelson_h510_exact507_obstruction/SHA256SUMS
```

The normal verifier took 149 seconds under CPython 3.11.2 on the producing
host. It first replays the accepted parent verifier, then rebuilds the quotient
census. It uses no SAT/SMT solver, floating point, numerical tolerance, random
seed, omitted proof trace, or external data download. `expected.json` pins the
counts and two canonical obstruction-stream hashes.

The controls exhaust 184,620 nonedge contractions of all six-vertex labelled
graphs whose source has no `K2,3`; the optimized local detector agrees with a
brute-force quotient scan in every case, including 15,300 positive cases.

## Scope, dependencies, and campaign decision

The proof imports the exact H510 graph, 20 rank bases, orientation cover, and
polynomial endgame from the independently accepted
[`hadwiger_nelson_heule510_plane_realizations`](../hadwiger_nelson_heule510_plane_realizations/README.md)
package. Their exact files are hash-pinned in `inputs.json`, and the parent
verifier is rerun before the new census. The new collision enumeration is
author-run checking, not an independent-author review or proof-assistant
formalization.

This closes only the exact 507-image layer of this fixed abstract carrier. It
does not show that arbitrary 507-point unit-distance graphs are four-colourable
and does not classify H510 maps with 506 or fewer images. In accordance with
the construction campaign's positive-realization gate, H510 is retired here
rather than extended to another count-only quotient layer.

The comparison source is Parts,
[*Graph minimization, focusing on the example of 5-chromatic unit-distance graphs in the plane*](https://arxiv.org/abs/2010.12665),
whose 509-vertex construction remains the unrestricted published record in
[Haugland's August 2026 primary-source discussion](https://arxiv.org/html/2608.04542v4).
The source graph is from
Heule, [*Computing Small Unit-Distance Graphs with Chromatic Number 5*](https://arxiv.org/abs/1805.12181).
