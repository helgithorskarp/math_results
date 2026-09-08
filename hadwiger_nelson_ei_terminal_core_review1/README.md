# Independent review of the 1,003-vertex EI spindle

## Verdict

**ACCEPT** the precise mathematical claims in Discovery Net contribution
`bafkreigy7jakk4pzlm23r5hmch7mzkittt4lphgrhbvmyix2rcxw3ny5wi`, based on
the source package at commit
`661a1564087d0c6e7a7616cf729fb0b98ecc2310`.

The accepted result is an explicit strict unit-distance graph on 1,003
vertices and 5,241 edges with chromatic number exactly five.  It also proves
that every non-four-colourable subgraph of this fixed 1,003-vertex host
contains a particular set of 835 vertices, and hence every subgraph of this
host on at most 834 vertices is four-colourable.

This is an intermediate construction, not the campaign target: 1,003 is not
below 509.  The 835-vertex statement is host-relative, is not claimed to be
attained, and gives no lower bound for arbitrary unit-distance graphs or for
other supports.

## Independent checks

[independent_check.py](independent_check.py) imports no claimant code.  It
represents `Q(sqrt(3),sqrt(11),sqrt(247))` by exponent triples, derives the
rotation from `cos(theta)=119/128` and
`sin(theta)=3 sqrt(247)/128`, and uses exact Python integers throughout.  It
establishes the following directly from the public coordinates and words:

- all 1,003 algebraic points are distinct;
- exhaustive checking of all 502,503 pairs gives exactly 5,241 strict unit
  edges, including 2,620 in each half and exactly one nonshared cross-edge;
- the published four-colouring of the 502-point half and five-colouring of
  the spindle are proper;
- an independently generated 2,008-variable, 13,996-clause terminal-inequality
  CNF is byte-identical to the CNF used by the checked proof; and
- the 416 local SAT words construct proper four-colourings of all 835 claimed
  vertex-deleted full graphs.

The exact output is in [RESULT.json](RESULT.json).  Normal and `python3 -O`
runs agree.

## Proof-chain audit

The CNF has exactly-one-of-four clauses for every half vertex, inequality
clauses for every exact unit edge, and only the pins `O=0`, `V=1`.  Colour
renaming shows that its UNSAT status is equivalent to equality of the two
terminals in every proper four-colouring.  Fresh Glucose3 generation
reproduced the CNF, DRAT, and LRAT files byte-for-byte.  The package's
positive-hint checker reached the empty clause after 71,096 additions and
6,638,850 hints.  A separately compiled C `lrat-check` also reported
`VERIFIED` for the independently regenerated CNF and the LRAT trace.

The half has a proper four-colouring.  It cannot be three-colourable: from a
three-colouring, recolouring only `V` with an unused fourth colour would give
a proper four-colouring with unequal terminals.  Thus the half is exactly
four-chromatic.  In any four-colouring of the spindle, terminal equality in
both copies would give the adjacent rotated terminals the colour of their
shared origin, a contradiction.  The checked five-colouring supplies the
matching upper bound.

The bounded deletion search was replayed to obtain evidence omitted from the
repository.  It reproduced 1,533 queries, 2,000,001 deletion conflicts, 32
UNKNOWN answers, the exact 502 retained indices, and zero peeled vertices.
The 416 SAT words reproduce to 214,154 bytes with SHA-256
`7cde84924a222e21d751de3f3bb38fc71a67e0b204fceed9af276862e6d11502`.
UNKNOWN answers are not used.  For each of 416 nonterminal vertices on either
side, its local word combines with the fixed word on the other half; direct
constructions also handle the two terminals and the shared origin.  These
are 835 distinct proper deletion colourings.  Therefore any subgraph omitting
one designated vertex is four-colourable by restriction, proving the stated
host-relative lower bound.

The optional provenance audit independently reconstructed all 4,293 parent
points, checked all 9,212,778 pairs and 29,934 strict unit edges, verified the
parent four-colouring, and matched the selected 502 rows.  This supports the
induced-subgraph provenance but is not needed for the self-contained spindle
theorem.

## Reproduction

From a checkout containing the claimant package and this review directory,
after generating the proof and boundary words as documented in the claimant's
README:

```sh
python3 -B hadwiger_nelson_ei_terminal_core_review1/independent_check.py \
  --package hadwiger_nelson_ei_terminal_core \
  --cnf /scratch/path/reduced.cnf \
  --boundary-words /scratch/path/deletion_words.json

python3 -O -B hadwiger_nelson_ei_terminal_core_review1/independent_check.py \
  --package hadwiger_nelson_ei_terminal_core \
  --cnf /scratch/path/reduced.cnf \
  --boundary-words /scratch/path/deletion_words.json
```

[REPRODUCTION.json](REPRODUCTION.json) records all generated-file hashes,
tool versions, proof statistics, search replay statistics, and external
checker identity.  Generated proof files and deletion words are intentionally
not committed.

## Trust boundary

The remaining trust is ordinary hardware, Python's arbitrary-precision
integer and JSON semantics, the reviewed coordinate-to-graph and
colouring-to-CNF translations, the small Python and C checkers, and the
elementary spindle and deletion arguments.  The proof is not formalized in a
proof assistant.  The large generated traces and deletion-word file are
hash-pinned but omitted from Git.  No claim of minimum order, record
improvement, unrestricted 835-vertex lower bound, or sub-509 success is
accepted or implied.

Claim source:
https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_ei_terminal_core

Review evidence:
https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_ei_terminal_core_review1
