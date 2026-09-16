# One nonuniform 17-copy Snail assembly is four-colourable

The frozen union has **444 distinct plane points and 890 complete unit edges**.
A literal proper four-colour word is checked against the complete physical
graph. This ends the selected construction; it is not a sub-509 five-chromatic
candidate or a general exclusion of Snail blow-ups.

The source is the exact augmented 29-point configuration of
[Dúcz and Varga, arXiv:2606.28157v1](https://arxiv.org/html/2606.28157v1),
called the Snail. Its geometric fractional chromatic number exceeds four,
but its ordinary graph is three-colourable. The present test imposes only
ordinary inequalities on actual unit pairs. It imposes no artificial
congruence-colour constraints.

## Frozen physical construction

Write the source labels as `p,q,v1,...,v27`. Four isometries send the following
ordered source pairs to target pairs:

| Motion | Source pair | Target pair | Orientation |
|---|---|---|---|
| g1 | (p,v11) | (v6,v13) | direct |
| g2 | (p,v11) | (v21,v26) | reflected |
| g3 | (p,v11) | (v8,v18) | direct |
| g4 | (q,v24) | (v6,v3) | reflected |

Each pair has the required exact congruent length. The orientation specifies
one unique isometry. Composition `fg` means apply `g`, then `f`. With indices
cyclic modulo four, freeze

```
R = {identity} union {gi, gi^-1, gi g(i+1), gi g(i+1) g(i+2) : 1<=i<=4}.
U = union {f(Snail) : f in R}.
```

All 17 motions are distinct. The raw order is 17*29=493, before any merging.
The [contract](CONTRACT.json) was saved before the sole chromatic query;
there is no adaptive copy selection. This mixes three congruences involving
`p` with the different congruence involving `q`, in both chiralities. It is a
selected word stencil, not a generator ball, rectangular box or dihedral
closure. Its internal outdegrees for the eight motions `gi,gi^-1` are
`8,2,2,2,2,1,1,1,1,2,2,2,2,1,1,1,1`.

This is a direct finite-graph decision. It does not use or evade the
[uniform full-generator averaging certificate's cap obstruction](../hadwiger_nelson_uniform_folner_certificate_gate/README.md)
by claiming a fractional inequality. The published averaging result supplies
motivation, not a non-four premise for this graph.

## Exact verification

From the repository root, CPython 3.11+ and its standard library suffice:

```sh
python3 -B hadwiger_nelson_snail_nonuniform17_stop/verify.py --check-expected
python3 -O -B hadwiger_nelson_snail_nonuniform17_stop/verify.py --check-expected
python3 -B hadwiger_nelson_snail_nonuniform17_stop/audit.py
python3 -B hadwiger_nelson_snail_nonuniform17_stop/controls.py
```

The checker reconstructs all 493 addresses, merges collisions exactly and
tests all **98,346 distinct-point pairs**. It checks the stored four-word
and a proper five-word on the same complete graph. The latter is obtained
by assigning one vertex a fresh fifth colour; it is not evidence of chromatic
number five. We claim four-colourability, not an exact chromatic number.

The producer and checker use two bases of the same degree-16 number field,
with different multiplication reductions and different residue primes.
`audit.py` compares every coordinate, every address identification and every
edge entry, rather than aggregate counts alone. The graph is connected, with
848 distinct edges inherited from individual copies and **42 additional
physical unit contacts**. It nevertheless has 44 articulation vertices and
51 bridges. These are diagnostics of this fixed union, not a family theorem.

Normal and optimized checks agree. The controls compare all 256 basis products,
16 conjugates and an exact unit triangle, and reject ten corrupted
certificates. See [PROOF.md](PROOF.md) for the exact arithmetic and completeness
argument, [EXPECTED.json](EXPECTED.json) for the result and
[VALIDATION.json](VALIDATION.json) for recorded verification.

## Optional certificate discovery

The optional producer uses Kissat 4.0.4. Give a fresh external work directory:

```sh
python3 -B hadwiger_nelson_snail_nonuniform17_stop/produce.py \
  --work /tmp/hn-snail-nonuniform17 \
  --kissat /path/to/kissat
```

There is one ordinary four-colour CNF, 1,776 variables and 6,669 clauses.
The 60-second / 1,000,000-conflict budget returned SAT; the decoded model was
checked directly. Expanded geometry, CNF and solver output are unnecessary
for verification and are not committed. No UNSAT or UNKNOWN is a premise.

The source table and arithmetic dependencies are hash-pinned in
[SOURCE_PINS.json](SOURCE_PINS.json). The latter are existing repository
packages, not downloaded executables. No external archive, numerical tolerance,
solver or network access is required by the positive certificate checker.
These are author-side computational checks; no independent review of this
new package is claimed.

## Scope and stopping boundary

The result covers exactly this frozen union and its subgraphs. It does not
exclude other nonuniform Snail assemblies. No phase, chirality, word-length,
copy-count or neighbouring generator variant was tried after the four-word.
The earlier dihedral, mixed-box, adaptive-cluster and marked-triangle results
retain their separate scopes.

Parts' [509-point, 2,442-edge graph](https://arxiv.org/abs/2010.12665) remains
the supported unrestricted record; [Haugland v4](https://arxiv.org/html/2608.04542v4)
explicitly retains 509. Its spindle-free result concerns a restricted family.
This package makes no record improvement or literature-priority claim.
No new Discovery broadcast was submitted for this single failed selector.
