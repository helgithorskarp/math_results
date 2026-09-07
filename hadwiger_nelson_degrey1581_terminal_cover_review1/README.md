# Independent review of the de Grey 1,581-vertex terminal cover

Verdict: **accepted at source commit
`2fcf486bbe0b09af8bb4094c48ca14ce15bbdcd1`**.

The accepted theorem is precise and limited: for the strict unit-distance graph
`G` on the specified de Grey 1,581-point support, there are 511 distinct
vertices `v` for which `G-v` has a proper four-colouring. Therefore every
subgraph of `G` with at most 510 vertices is four-colourable. This covers
arbitrary vertex subsets and arbitrary edge deletions inside this fixed host.
It is not a sub-509 five-chromatic construction, a record improvement, a
classification of other supports, or a proof about every unit-distance graph.

## Independent checks

[audit.py](audit.py) imports no code from the reviewed terminal-cover package.
It treats that package's `seeds.json` and `certificate.json` as input data and:

1. reruns the pinned SymPy geometry implementation from the prior independent
   [residue-section review](../hadwiger_nelson_degrey1581_residue_sections_review1),
   reconstructing all 1,581 points and all 7,877 strict unit edges;
2. derives the two 791-point halves, their sole shared vertex, their 3,938
   edges each, the unique bridge, and the half inversion independently in
   integer radical coordinates;
3. independently parses the 34 seed, 127 inversion, and 93 patch records,
   validates all 254 omission words and their terminal separation, and checks
   1,001,762 half-edge inequalities;
4. obtains 511 distinct global deletions, constructs each 1,580-vertex word by
   a fresh palette search, and directly checks 4,020,265 full-host edge
   inequalities; and
5. reproduces the submitted global word-stream SHA-256
   `120c1af011ce288286f7f1ad41a9163aa9ce112e4479f4964bd149413a431be3`.

The last logical step is elementary and was re-derived: a subgraph on at most
510 vertices omits at least one member `v` of the 511-element certified set.
Restricting the verified colouring of `G-v` gives a four-colouring even when
the subgraph has deleted further edges.

## Reproduction

From the repository root, use Python 3.11+ and SymPy 1.14.0:

```sh
python3 -m venv /scratch/research-team-v2/tmp/reviewer-1/terminal-cover-review-venv
/scratch/research-team-v2/tmp/reviewer-1/terminal-cover-review-venv/bin/pip \
  install -r hadwiger_nelson_degrey1581_terminal_cover_review1/requirements.txt
/scratch/research-team-v2/tmp/reviewer-1/terminal-cover-review-venv/bin/python -B \
  hadwiger_nelson_degrey1581_terminal_cover_review1/audit.py \
  --target hadwiger_nelson_degrey1581_terminal_cover \
  --expected hadwiger_nelson_degrey1581_terminal_cover_review1/expected.json
```

The independent geometry phase intentionally checks every candidate surviving
two unrelated modular filters in a SymPy algebraic number field. It is the
slow part of the audit and used one local process.

Reviewed Discovery contribution:
`bafkreih7ynv6eqb33smgovf7dkhsnllvczjdhgc5ztsy53scpc3trazm2e`.
The reviewed directory is unchanged from source commit
`2fcf486bbe0b09af8bb4094c48ca14ce15bbdcd1`.

## Trust boundary

The geometry implementation is reused from the independently published prior
review rather than copied into this directory. Its exact source is pinned to
SHA-256 `b4992abfcbfca9d91b23765db742cd279b78d45b9b56784bddd3def1daf456f9`.
That code independently transcribes de Grey's 39 seeds, uses SymPy exact
construction, filters pairs with the different primes 3,061 and 3,251, and
confirms survivors with `AlgebraicField`/ANP arithmetic. This audit reruns that
code, then independently handles all new half-interface and certificate logic.

The remaining trust base is the seed transcription, the linear independence
of the displayed squarefree-radical basis, CPython and SymPy exact arithmetic,
SHA-256 collision resistance, and the short restriction argument above. No
SAT result, UNKNOWN interpretation, floating-point comparison, exhaustive
search claim, or imported assertion that the full graph is five-chromatic is
used in this verdict.
