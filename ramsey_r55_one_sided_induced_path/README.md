# Induced P5s are forced in both colors of every good43 neighborhood

Every 18-vertex graph with no K4 and no independent 5-set contains an induced
P5. Consequently, in any hypothetical 43-vertex graph with no monochromatic
K5, every 18 vertices in a monochromatic neighborhood contain an induced P5
of that color. In particular, each vertex has such a path among its neighbors
in both colors. This excludes the entire family that is P5-free in either
color, with all other physical edges unrestricted.

The finite proof uses the published classification of 5-vertex-critical
(P5,K4)-free graphs into two graphs, followed by checked exclusions of both
complete 18-vertex extension families. See [PROOF.md](PROOF.md) for the global
bridge, encoding, counting corollaries, and exact trust boundary. The imported
classification is not reproduced here. No historical novelty claim is made.

## Reproduce without a SAT solver

Python 3.11 standard library suffices; tested with CPython 3.11.2:

```sh
python3 ramsey_r55_one_sided_induced_path/reproduce.py --out /tmp/r55-p5-replay
python3 ramsey_r55_one_sided_induced_path/controls.py --out /tmp/r55-p5-controls
```

The first command regenerates both full CNFs, independently audits every
literal constraint, and verifies the committed text RUP proofs. Expected:
G1 has 75 variables, 57,596 clauses, and 275 verified RUP additions;
G2 has 62 variables, 34,197 clauses, and 77 verified RUP additions.
Both finish with an empty clause. The controls check 4,608 two-variable RUP
instances for soundness and reject two deliberate evidence corruptions.

To check the saved proofs using drat-trim as well:

```sh
drat-trim /tmp/r55-p5-replay/G1.cnf ramsey_r55_one_sided_induced_path/G1.proof
drat-trim /tmp/r55-p5-replay/G2.cnf ramsey_r55_one_sided_induced_path/G2.proof
```

Both return `s VERIFIED`. To rediscover the proof with CaDiCaL (optional;
unnecessary for verification), run for each case:

```sh
cadical --seed=0 -t 600 -c 500000 /tmp/r55-p5-replay/G1.cnf /tmp/G1.drat
```

The discovery run used CaDiCaL sc2021 (Debian 1.5.3-2). All settings were the
defaults except the specified seed and limits; CADICAL_* environment overrides
were removed. `VALIDATION.json` records binary hashes and both original UNSAT
receipts. Solver exit 20 denotes UNSAT. Large generated CNFs and raw logs are
not committed: the complete proofs occupy only 9,332 bytes of plain text and
the formulas regenerate in seconds.

`INPUTS.json` holds the exact published core adjacency lists. `EXPECTED.json`
pins the regenerated data and certificates. `SHA256SUMS` pins the public
package. [HANDOFF.md](HANDOFF.md) states the physical interface and the parked
families this result does not recompute or decide.
