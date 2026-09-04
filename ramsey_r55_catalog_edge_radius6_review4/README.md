# Independent review of the Ramsey(5,5,42) radius-six catalog closure

## Verdict and scope

**Qualified accept with moderate-to-high confidence**, scoped to Discovery
Net finding `bafkreievf353ydczzp2ph73rsynf3uaqhjqtk6jwh4ppfyk2sm2drcqvii`
and source commit `85c15308bda8a1a699c898f3ca96ef9d8e356f22`.

The reduction and SAT encoding are sound; all 6,384 committed six-flip
transitions, their Ramsey validity, their target isomorphisms, and their
aggregate statistics check independently.  Four varied parent formulas were
completely re-enumerated, and a separately generated static CNF plus checked
DRAT proof establishes exhaustive completeness for zero-survivor parent 190.

Global negative completeness for the other 327 parents still imports the
contributor's reported CaDiCaL terminations because no all-parent proof
manifest is retained and this review did not repeat the approximately 12.6
aggregate one-core hours.  This is a closure theorem only inside the 656 known
catalog orientations.  It neither proves that catalog complete, constructs a
43-vertex Ramsey graph, nor improves a bound on `R(5,5)`.

## Encoding audit

There are 861 primary flip variables.  Seven one-way threshold levels encode
weight at most six: any seventh selected variable forces the forbidden final
threshold.  Conversely, a primary assignment of weight at most six extends
to a model by setting threshold `(i,j)` precisely when the prefix through
edge `i` has at least `j` selected variables.

For a fixed five-set with originally present edge set `P` and absent edge set
`A`, it becomes a clique precisely when every `A` variable is true and every
`P` variable is false.  Its exact blocking clause is therefore

```text
(OR over P of x_e) OR (OR over A of not x_e).
```

Under the global weight cap it is needed exactly when `|A|<=6`.  Exchanging
present and absent gives the independent-set clause, needed when `|P|<=6`.
Thus five-sets with four, five, or six edges correctly receive both clauses.

After each SAT model, the enumerator blocks all 861 primary literals.  This
removes the mathematical flip assignment regardless of nonunique counter
auxiliaries.  Termination with UNSAT therefore establishes exhaustive primary
model enumeration, within the solver trust boundary.  Complementing a graph
commutes with flipping a fixed edge set, so the 328 stored parents cover their
328 complements as well.

## Independent all-map audit

`independent_map_check.py` imports no target module and uses NetworkX 3.5 for
a separate graph6 decoder, clique algorithms, complementation, and VF2++
isomorphism.  It checks:

- all 328 source graphs have order 42 and avoid homogeneous five-sets;
- all 6,384 rows contain distinct canonical edge sextuples;
- every reconstructed variant avoids a five-clique in both colours;
- every variant is isomorphic to its stated base or complement target;
- the split is 6,334 base and 50 complement transitions reaching 311 stated
  target orientations, with the claimed 40 zero-parent list and full parent
  distribution; and
- the radius-one-through-six maps together contain 37,256 nonzero labeled
  transitions and reach 552 target orientations, 12 newly at radius six.

The map SHA-256 is
`ea3dd948e333153f0bf844e279d7df2788849dfe676d6e45af1aaf74e1e29e72`.
The catalog SHA-256 is
`067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb`;
a fresh download from Brendan McKay's ANU page matched it.

Run from the repository root with NetworkX 3.5:

```bash
/path/to/python ramsey_r55_catalog_edge_radius6_review4/independent_map_check.py
```

The deterministic result is in `EXPECTED_MAP_OUTPUT.txt`; the run took 85
seconds on one core.

## Fresh complete parent replays

I built the submitted C++17 enumerator warning-free using GCC 12.2.0 and
CaDiCaL 3.0.1 from official commit
`c60730422e758ef1cebe7aeddf2dda31c996bf04`.  Four sequential one-core runs
covered distinct regimes:

| parent | reason | exact six | lower models | wall time |
|---:|---|---:|---:|---:|
| 0 | first record / baseline | 29 | 72 | 117 s |
| 23 | 14 complement-target transitions | 16 | 112 | 96 s |
| 190 | zero survivors / only four lower models | 0 | 4 | 128 s |
| 241 | reported slowest / maximum survivor count | 57 | 106 | 135 s |

`check_sample_replays.py` independently decoded and reconstructed every raw
graph6 row.  The 102 emitted edge sextuples equal the corresponding committed
map slices exactly, and all four clause counts independently match direct
five-set histograms.  Reproduction commands and binary hashes are in
`toolchain_and_replays.txt`.

## Checked static completeness proof

`build_static_cnf.py` is a standard-library implementation importing no
target code.  It builds the primary model directly and adds full blocking
clauses for every assignment stored at radii zero through six.  For parent
190 these are exactly the identity, two one-flip assignments, and one
two-flip assignment.  The resulting formula has:

```text
parent=190 variables=6888 clauses=1455200 counter_clauses=12042
ramsey_clauses=1443154 blocked_known_models=4
```

The 65,613,408-byte CNF has SHA-256
`a9fcbcd776a764c5ac2f191e114092499b1322b083db2eafe14356c4254b6320`.
CaDiCaL returned UNSAT in 81 seconds and emitted an 85,558,316-byte binary
DRAT proof with SHA-256
`ba13706530b6d3e0c4c55900421a1520a56fedd4c024ca48c7afb285382df10a`.

`drat-trim` at commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`
reported `s VERIFIED` in 45 seconds: 27,940 of 1,455,200 input clauses and
123,892 of 773,841 lemmas occur in the core, with 42,077,695 resolution steps
and zero RAT lemmas.  The large scratch CNF and proof are represented by
their hashes and are not committed.

## The 43-vertex corollary

Suppose a Ramsey(5,5,43) graph arose by adjoining one vertex to a known
42-vertex catalog graph and changing at most six old-old edges.  Deleting the
new vertex leaves a Ramsey-valid radius-six variant, which this classification
maps to a known 42-vertex graph.  Deleting any one of those 42 old vertices
then represents the hypothetical graph as a two-vertex extension of a known
41-vertex deletion core, contradicting the certified obstruction
`bafkreig2wslyxeadb3fadldshzxvy3dy5spqpwtoqnhxfinqvtl6hpu46a`.

I reran that dependency's solver-free exhaustive checker.  It verified 9,757
cores, 11,387 one-vertex extension models, and all 15,401 ordered model pairs
in 16 seconds.

## Trust boundary

The complete positive map audit trusts CPython, NetworkX's exact graph
algorithms, the hash-bound files, and the program-to-mathematics alignment
above.  Distinctness and provenance of the official 656 catalog orientations
remain imported from McKay's nauty-based data.  The four fresh complete runs
trust the audited wrapper, pinned CaDiCaL build, GCC, and hardware; parent 190
additionally has an independently generated CNF and checked proof.
Completeness for the other 327 parents imports the contributor's recorded
full run.  No proof assistant was used.

The radius-five base has three independent reviews, including this reviewer's
`bafkreifbiqn7n2xejelju5gxc6noqrthpcam43ntbbg2ulp5vdn6pvempa`.
Those reviews validate the inherited lower maps but do not substitute for
radius-six model completeness.

## Novelty and readiness

McKay's primary data page states that 328 graphs and their complements are
known and explicitly does not claim catalog completeness.  Targeted primary
source and exact-phrase searches found no prior complete six-edge-flip map or
the 6,384 count.  This is search-relative; it is not a priority claim.

The result is ready as a scoped computational classification.  A durable
publication should retain compressed DRAT/LRAT proofs for every parent,
publish explicit isomorphism permutations for every transition, and keep the
edge-Hamming radius clearly distinguished from older induced-subgraph vertex
distance results.

## Files

- `independent_map_check.py` -- independent all-map Ramsey/isomorphism audit.
- `check_sample_replays.py` -- exact comparison of fresh parent enumerations.
- `build_static_cnf.py` -- independent proof-producing static CNF generator.
- `EXPECTED_MAP_OUTPUT.txt`, `EXPECTED_SAMPLE_OUTPUT.txt`, and
  `EXPECTED_CNF_OUTPUT.txt` -- compact deterministic results.
- `toolchain_and_replays.txt` -- tool versions, commands, hashes, timings, and
  proof-replay metrics.
- `requirements.txt` -- pinned NetworkX dependency.
- `SHA256SUMS` -- compact evidence hashes.

## Primary source

Brendan McKay, ANU Combinatorial Data, Ramsey graphs,
<https://users.cecs.anu.edu.au/~bdm/data/ramsey.html>.
