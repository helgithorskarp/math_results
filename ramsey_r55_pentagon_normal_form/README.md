# Complete 842-variable pentagon family for Ramsey(5,5;43)

Every good 43-vertex graph has a representative in one explicitly defined
family with **61 fixed pairs and 842 free physical pairs**, subject to the
published `N_5=21` theorem cited below. A complete Ramsey CNF for that family
has **1,369,076 clauses**. This removes 40 variables and 369,148 clauses
beyond a single forced `K2 join C5` anchor. No graph automorphism is imposed.

This completes a material global representation reduction. Satisfiability
has not been decided; no 43-vertex Ramsey graph or improved defect score
is reported. See [PROOF.md](PROOF.md) for the family, both implications,
algorithm, exact counts and trust boundaries.

## Reproduce

Requires Python 3.11 or newer, standard library only. From this directory:

```sh
python3 -B reproduce.py /tmp/r55-pentagon-frame-replay
```

Use a fresh path outside the repository. The command emits the complete
61,068,978-byte formula, audits every physical five-set in both colors,
repeats the independent audit and controls under `python -O`, and verifies
candidate transport, decoding and physical defect preservation. It compares
all results to committed expected JSON. Generated formulas remain in the
external directory; no solver is invoked. `validation.json` records the
observed completed replay and timings.

Formula SHA256:
`f3116aba2b377f84af984b4e604dca21e795b9f9c0c8e1ae3948dabc49261969`.

## Use the full candidate interface

An edge-list file starts with `n m`, followed by exactly `m` distinct red
edges `u v`, with `0 <= u < v < n`; omitted pairs are blue.

```sh
python3 -B normalize.py control43.edges > /tmp/r55-frame.json
python3 -B verify.py control43.edges /tmp/r55-frame.json
python3 -B export.py control43.edges /tmp/r55-frame.json /tmp/r55-moved.edges /tmp/r55-free.bits
python3 -B encode.py /tmp/r55-frame.cnf
python3 -B check_cnf.py /tmp/r55-frame.cnf
python3 -B evaluate.py /tmp/r55-frame.cnf /tmp/r55-free.bits
python3 -B decode.py /tmp/r55-free.bits /tmp/r55-decoded.edges
python3 -B verify_graph.py /tmp/r55-decoded.edges
```

A normalizer result is either a physical monochromatic five-set or a
permutation and a whole-graph complement bit. A frame result proves only
membership in the required representation. The included 43-vertex control
has **seven defects** and its formula evaluation must report false.
For a prospective target, `verify_graph.py` must report order 43 and zero
red and blue five-sets. It uses literal subset enumeration and separate
bit-intersection clique recursion.

Bits are 0/1 characters, one per lexicographically ordered free unordered
pair; 1 means red. The decoder consumes exactly 842 bits and reconstructs
all 903 physical pairs. A future SAT model must first be converted to this
complete assignment format. `export.py` requires a successful frame
certificate; it does not accept an obstruction result.

The normalizer accepts orders 27 through 63 for controls and reuse. Its
proof of successful obstruction-or-frame output applies at order at least
43. Below 43 it may return `no_frame_found`, which is not an exclusion.

## Dependencies and provenance

- The root `J` existence comes from the elementary
  [pentagon forcing proof](../ramsey_r55_induced_pentagon_forcing/PROOF.md),
  source commit `514d32b01e495ee9df818e19bf2e0ae58ba52084`, Discovery Net
  `bafkreiffqyzfkpxkeaujbuacmzhduxnxs2pj2phancs3vm4q3yo5gdzu5e` (h3593).
  The [global incidence theorem](../ramsey_r55_pentagon_incidence/PROOF.md),
  source commit `b2fe2b7085afc6a8a06c2ccb2bbb6b56a5c13bdf`, ref
  `bafkreiedu3cnxvh6sq4wfliygoxw2hhipq36uih7mgncqvj7bmkmgfu76i` (h3615),
  supplies the stronger root count. Its bounds `W>=906` and `P>=18` stay
  unchanged.
- An independent [review of these proofs](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_global_pentagon_incidence_review1),
  commit `06a3ea15158d08f9c26d244973baad11aa4e663c`, was accepted at h3619,
  ref `bafkreid7njskfjcp2z3pxnfy66gw7msutuvh2uclfrlpca77xbmlclqpp4`.
  That review concerns the earlier results, not the present reduction.
- Paul W. Dyson and Brendan D. McKay,
  [Ramsey numbers for regular induced subgraphs, arXiv:2604.08215v3](https://arxiv.org/html/2604.08215v3),
  Theorem 1.2 gives `N_5=21`. This is an imported computational theorem.
  Section 5.1 reports a complete generation and independent comparison
  only through order 15 for this part. We did not rerun that classification.
  Its threshold is already published and is stronger than our prior
  elementary order-42 pentagon threshold.
- `control42.edges` is decoded from the first record of McKay's
  [sample Ramsey(5,5;42) graph file](https://users.cecs.anu.edu.au/~bdm/data/r55_42some.g6).
  The downloaded file's SHA256 was
  `067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb`.
  Only the individual graph is used, with goodness independently checked;
  no catalog completeness is assumed.
- `control43.edges` decodes `known_secondary_q7` from the committed
  [novelty fixtures](../ramsey_r55_c5_semidirect_c8_cayley_obstruction/novelty_fixtures.json)
  as present at repository base `63041cb67599273f2b1df888a4e1e1cfb0e91cf4`.
  Packed bits there enumerate all 903 unordered pairs lexicographically,
  with the least significant bit first. Its one red and six blue defects
  are recounted here, without any new candidate search.

The published regular-five theorem also implies the mathematical
impossibility of the formerly investigated sufficient 22-vertex
K4/I5/C5-free branch. That old SAT run still has solver status UNKNOWN and
no proof trace; it was not resumed or retrospectively relabeled UNSAT.
All parked neighborhood-gluing, retained-core and product scopes stay
parked. This family permits arbitrary cross pairs and does not reuse them.

The prepublication refresh through Discovery Net height 3628 found the
separate [M214 moment and pentagon-count projection survivor](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_global_square_p4)
(h3625). Its aggregate pentagon counts do not assert compatible physical
placements. The present physical covering form is compatible with that
limited conclusion and does not decide its moment relaxation. The new
independent acceptance of the teammate's Paley43 ordering obstruction
(h3627) also leaves this unrestricted family untouched. Neither is a proof
premise here.

## Artifact map

`frame.py` and `encode.py` generate the complete formula. `check_cnf.py`
independently audits physical coverage. `polynomial.py` counts by generating
functions. `normalize.py`, `verify.py`, `export.py`, `decode.py`,
`verify_graph.py` and `evaluate.py` implement the candidate interface and
physical validation. `controls.py` checks exhaustive small truth assignments,
relabelings, complements, malformed inputs and every coordinate's decoding.
`reproduce.py` runs the complete gate. Small graphs, certificates and
expected reports are included; large formulas, the literature HTML and the
sample graph collection are deliberately omitted and are unnecessary for
replay. `SHA256SUMS` covers every other file in this directory.
