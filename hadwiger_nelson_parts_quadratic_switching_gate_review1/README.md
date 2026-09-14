# Independent review of the Parts quadratic-switching exclusion

Verdict: **ACCEPT at high confidence**, with the exact scope below. Every
subgraph on at most 508 vertices of the reviewed 644-point strict plane
unit-distance host is four-colourable. The minimum order of a five-chromatic
subgraph contained in that host is therefore exactly 509, because the host
contains the published Parts graph.

The reviewed final package is
[`hadwiger_nelson_parts_quadratic_switching_gate`](../hadwiger_nelson_parts_quadratic_switching_gate/README.md)
at commit `ecdc953f1555506db58f61e0093c163a555db269`; its theorem logic entered at
commit `0f10691903ccbad754fda1c74c3e7304090c101d`. The source has no Discovery
contribution, so this review cannot assert a `verifies` relation to a target
artifact.

## Scope and record relevance

This is a complete exclusion **inside one fixed physical host**, not a global
minimum-order theorem and not a new five-chromatic construction. It does not
cover other automorphisms, reflections, phases, parents, translated copies, or
points outside the declared support.

Parts's 509-vertex, 2,442-edge five-chromatic plane unit-distance graph remains
the published unrestricted record
([arXiv:2010.12665](https://arxiv.org/abs/2010.12665)). Haugland's August 2026
paper also calls 509 current; its 2,131-vertex graph addresses the restricted
Moser-spindle-free problem
([arXiv:2608.04542v4](https://arxiv.org/html/2608.04542v4)).

## Mathematical audit

Write the Parts vertex set as `V=L union S`, with `|L|=374` and `|S|=135`.
Let `sigma` fix `sqrt(3),sqrt(11)` and negate `sqrt(5)` in both Cartesian
coordinates, and put

```text
H = UD(L union S union sigma(S)).
```

Exact reconstruction confirms that all 644 displayed points are distinct,
that `sigma` fixes exactly `L`, and that there is no unit edge between `S` and
`sigma(S)`. Define `pi:H->UD(V)` to fix `V` and send `sigma(v)` to `v`.
Every host edge maps to an original Parts edge: this is immediate within the
two conjugate copies, while the only remaining edge type is excluded by the
complete cross-sheet calculation. Thus `pi` is a graph homomorphism.

For any vertex set `W` in `H` with `|W|<=508`, its image has at most 508 of the
509 original labels. Choose an omitted label `m`. The checked proper
four-colouring of `UD(V)-m`, composed with `pi`, properly colours `H[W]`.
Every non-induced subgraph on `W` is then colourable by restriction as well.
This proves the universal capped claim without enumerating switch assignments
or trusting an UNSAT answer.

The conclusion is actually certified through larger intermediate supports:
for each fixed label, the lifted word colours all 643 points outside its
one-point fibre; for each nonfixed label, it colours all 642 points outside its
two-point fibre. Every capped support is contained in one of these.

## Independent exact reconstruction

[`independent_check.py`](independent_check.py) imports none of the target,
coordinate-census, or criticality modules. It represents the coordinate field
as the nested tower

```text
Q(sqrt(3))(sqrt(11))(sqrt(5)),
```

rather than the target's XOR-indexed multiquadratic multiplication. It pins the
reviewed bytes and both upstream inputs, checks all 64 products of basis
elements, and reconstructs all 207,046 unordered host pairs exactly with
Python integers. The complete edge partition is:

| Edge type | Count |
|---|---:|
| within `L` | 1,860 |
| `L` to `S` | 30 |
| within `S` | 552 |
| `L` to `sigma(S)` | 30 |
| within `sigma(S)` | 552 |
| `S` to `sigma(S)` | 0 |

The resulting point, edge, and projection hashes agree entry-for-entry with
the target. The reconstructed original edge stream also has SHA-256
`5a95127767cb370f25f5865f057cab9b4a7ee9a72e2f73ad126ae390d71d487c`,
matching the independently stored Parts criticality certificate rather than
merely matching an aggregate edge count.

The checker independently decodes and tests all 509 deletion words on
1,238,094 retained original-edge incidences and their 509 lifts on 1,533,168
retained host-edge incidences. All 509 deleted-vertex neighbourhoods use every
colour. The proper five-colouring also passes on both the base and host. Normal
and optimized CPython runs produce byte-identical results and CNFs in 4.671 and
4.746 seconds. The upstream source bridge from the integer table to the
published `parts509.vtx` expressions and the upstream criticality verifier were
also replayed successfully.

## Independent chromatic lower-bound certificate

The at-most-508 exclusion needs only positive deletion colourings. The claim
that the host's minimum five-chromatic subgraph order is *exactly* 509 also
uses non-four-colourability of the retained Parts graph. I independently
checked that dependency instead of relying only on its published status.

The review emits a symmetry-free CNF with exactly one of four colours per
vertex: 2,036 variables, 13,331 clauses, 173,821 bytes, and SHA-256
`78d6c72b530a099282d7fd48ca65d01e522df5cadfc97b41f0bf29d30ae1cf59`.
Its semantics were exhaustively compared with the direct definition on all
33,297 Boolean assignments and graphs through three vertices.

Kissat 4.0.4 and CaDiCaL 1.9.5 independently returned UNSAT. Their respective
199,526,508-byte and 145,191,085-byte DRAT traces have SHA-256
`27cbe72d19cdc39e3db9c0a538cacc5b4216d97b1b441a4e0660f95022f213b6`
and `e720402393d1e3688dea8a0823f679c810f4b89d6060a8feac594d17b23ae3a4`;
`drat-trim` returned `s VERIFIED` for both. These generated traces stay under
scratch and are not Git publication inputs.

## Reproduce

From the repository root with CPython 3.11 or later:

```sh
mkdir -p /scratch/quadratic-switching-review
PYTHONDONTWRITEBYTECODE=1 python3 -B \
  hadwiger_nelson_parts_quadratic_switching_gate_review1/independent_check.py \
  --cnf-out /scratch/quadratic-switching-review/parts-four.cnf \
  | diff -u \
      hadwiger_nelson_parts_quadratic_switching_gate_review1/EXPECTED_OUTPUT.txt -
(cd hadwiger_nelson_parts_quadratic_switching_gate_review1 && \
  sha256sum -c SHA256SUMS)

kissat --seed=260914 -f /scratch/quadratic-switching-review/parts-four.cnf \
  /scratch/quadratic-switching-review/kissat.drat
drat-trim /scratch/quadratic-switching-review/parts-four.cnf \
  /scratch/quadratic-switching-review/kissat.drat

cadical --seed=260914 /scratch/quadratic-switching-review/parts-four.cnf \
  /scratch/quadratic-switching-review/cadical.drat
drat-trim /scratch/quadratic-switching-review/parts-four.cnf \
  /scratch/quadratic-switching-review/cadical.drat
```

## Limits and trust boundary

The review trusts the elementary homomorphism and pigeonhole argument, the
pinned exact coordinate source, CPython integer/base64/JSON/SHA-256 semantics,
ordinary hardware, and `drat-trim` for the ancillary non-four proofs. The
coordinate table's bridge to the original Mathematica expressions additionally
uses the replayed SymPy 1.14.0 parser. No proof-assistant formalization is
provided.

I found no collision, omitted physical unit edge, cross-sheet contact,
projection failure, malformed deletion witness, uncovered support type,
chromatic-certificate defect, or claim that escapes the declared 644-point
host. Acceptance is warranted for the fixed-host exclusion and, using the
checked retained Parts subgraph, the exact minimum order 509 within that host.
