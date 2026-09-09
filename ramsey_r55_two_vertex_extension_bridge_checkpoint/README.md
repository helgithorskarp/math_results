# A failed catalog obstruction for the two-vertex extension property

The 24-vertex graph in [WITNESS.json](WITNESS.json) has no K4 and no
independent 5-set, and its specified 17 vertices have neither a K4 nor an
independent 4-set. Thus the proposed statement that no Ramsey(4,5;24) graph
contains an induced Ramsey(4,4;17) graph is false.

**The declared global43 gate remains unproved.** This witness assigns only
24 vertices. No complete43 family, retained q10 child, or q7-r5 task was
excluded by this pass, and no good43 was constructed. The completed action
is a reproducible falsification checkpoint; no subsequent extension or
gluing search was started. No historical novelty is claimed for this graph.

## Check the counterexample without a catalog or solver

From the repository root, using Python 3.11 standard library:

```sh
python3 ramsey_r55_two_vertex_extension_bridge_checkpoint/verify_witness.py \
  ramsey_r55_two_vertex_extension_bridge_checkpoint/WITNESS.json \
  --out /tmp/r55-two-vertex-bridge-check.json
```

Expected: `VERIFIED_BRIDGE_COUNTEREXAMPLE`, with 10,626 host red four-sets,
42,504 host blue five-sets, and 2,380 four-sets in each color of the chosen
17-set checked directly. Its 17 induced degrees all equal 8. The checker
uses a dense adjacency matrix and literal combinations; it imports neither
the search implementation nor a Ramsey theorem. [EXPECTED.json](EXPECTED.json)
records the exact output. Hashes are in `SHA256SUMS`.

The witness is zero-based record **90** of the official
[Ramsey(4,5;24) catalog](https://users.cecs.anu.edu.au/~bdm/data/r45_24.g6),
containing 352,366 graph6 records. The catalog SHA-256 is
`83ca4028f206b2fa4315ef219b8c2c57c7835209673dd8183d8fb4353bd4fdd0`.
Optional `--catalog /path/to/r45_24.g6` checks the digest and exact record.
Catalog completeness is unnecessary to verify this positive counterexample.

## Why this was tested

A good43 graph has no clique or independent set of order five. The selected
complete global family consisted of every graph for which some pair u,v
lacks at least one of the four outside red/blue contact patterns. All other
physical edges were unrestricted. Excluding that family would establish
that every good43 graph is **2-existentially closed**.

Use the classical bounds R(3,5)<=14, R(4,4)<=18 and R(4,5)<=25. A good43
has degrees 18 through 24 in each color. Rename the pair's color red, and
let a be its number of common red neighbors. Since those neighbors have
no red triangle or blue K5, a<=13. The red/blue and blue/red contact counts
are d(u)-1-a and d(v)-1-a, hence at least 4 each. These are consequences of
the same elementary caps used in the existing
[module-resilience argument](../ramsey_r55_module_resilience/README.md).

The blue/blue cell is nonempty too. Otherwise all blue neighbors of u
would be red neighbors of v. On that set a blue K4 extends with u, while
a red K4 extends with v. Its size is at least 18, contradicting R(4,4)<=18.

The remaining missing-pattern case is a=0: an edge uv in no red triangle.
Then A=N_red(u)-{v} is red-K4-free because of u, and blue-K4-free because
v is blue to all of A. Therefore |A|<=17, and the degree bound forces
d_red(u)=18. The same holds for v, with B=N_red(v)-{u} of order 17.

Now N_blue(u) has 24 vertices and contains B. In the blue color it is a
Ramsey(4,5;24) graph, and its restriction to B is Ramsey(4,4;17). Thus
absence of that induced-subgraph pattern from the entire order24 catalog
would have excluded the last case and achieved the global gate.

The displayed witness refutes this sufficient catalog obstruction. It does
not supply the other 19 vertices, the second endpoint's complete contacts,
or any of the remaining constraints of a good43. Consequently the
2-existential-closure question for good43 is left open by this checkpoint.

## Discovery and stop boundary

[GATE.json](GATE.json) was fixed before the scan. It allowed one full-catalog
scan capped at 600 seconds, stopping immediately at any positive witness or
UNKNOWN. The search sought a 17-set by deleting vertices that hit every
independent 4-set. It used the necessary 8-regularity of Ramsey(4,4;17)
graphs to peel impossible vertices, deriving that regularity solely from
R(3,4)<=9. No prescribed 17-vertex graph, automorphism, orbit, or symmetry
source was used.

The scan stopped after 91 records and 5,866 search nodes, at record 90;
elapsed search time was about 0.008 seconds. Earlier search outcomes are not used
as exclusion certificates. The independent dense checker establishes
the entire positive result without trusting the scanner's pruning.
[FAILED_GATE.json](FAILED_GATE.json) records the original discovery receipt
and the catalog-membership audit. The initial scan source and raw outputs
are retained in the private durable campaign checkpoint; they are unnecessary
to reproduce the mathematical counterexample.

The existing h4015 induced-path theorem and h4009 edge window are unchanged.
The h4001 ledger remains 518 complete task exclusions and 122 unresolved
selected full tasks. The h3987 ledger remains 99 closed and 161 unresolved
q10 children, with its existing forced edge in 29 residual F22 children;
those physical decisions remain with team-r55-1. Counts at these different
levels are not combined.

The global gate failed, and no new Discovery Net mathematical claim is
submitted for it. Do not continue from this local witness by a fixed-core
extension, paired-neighborhood decomposition, stronger cap, or alternate
backend. Any later milestone needs a different complete global family or
a new measurable global reduction.
