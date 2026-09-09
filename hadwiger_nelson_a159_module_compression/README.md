# Exact obstruction to compressing A159 for five-module synthesis

**Deleting any one of the 156 private vertices of the specified A159 graph
allows every four-colour assignment on its three terminals.** Consequently
every proper terminal-preserving vertex reduction has the same unrestricted
extension property. Any subgraph of this source that forbids a monochromatic
terminal triangle must retain all 159 vertices.

Together with a geometric degree bound and Brooks' theorem, this proves
that **at most five such proper reductions, joined only through terminal
overlaps and terminal unit edges, always form a four-colourable graph**.
This rules out the proposed five-module construction using 100 private
vertices per module from A159 deletions. It is a quantified obstruction to
one synthesis architecture, not a record improvement. The
[proof](PROOF.md) states all hypotheses and excluded cases.

The [156 positive witnesses](certificate.json) are compact and checked
without a SAT solver. The exact coordinate input is the archived Parts
[points159.tsv](../hadwiger_nelson_nonmono159_214_lowden2/points159.tsv),
with [documented provenance](../hadwiger_nelson_nonmono159_214_lowden2/SOURCE.md).
Terminals are indices 141,142,144, with all three squared distances 7.
Every one of the 12,561 point pairs is tested in exact Q(sqrt3,sqrt11)
arithmetic. Input files are SHA-256 pinned.

The four positive nonmono patterns are inherited from
[h3194](../hadwiger_nelson_long_terminal_gluing/README.md) and checked again.
No advertised negative forcing property or minimality claim is assumed.
This package complements the
[h4051 five-module handoff](../hadwiger_nelson_four_module_synthesis/HANDOFF.md);
it does not duplicate HN-3's terminal-geometry question.

## Reproduce the proof check

From the repository root, with CPython 3.11.2 and its standard library:

```bash
python3 -B hadwiger_nelson_a159_module_compression/verify.py --check-expected
python3 -O -B hadwiger_nelson_a159_module_compression/verify.py --check-expected
```

The [expected output](EXPECTED.json) reports 156 deletion witnesses,
9,984 decoded boundary extensions, 6,367,872 retained-edge checks and seven
rejected corruptions. Normal and optimized Python give identical output.
The exact edge list was also compared entry by entry with the independent
producer arithmetic; the certificate check alone needs no producer output.

`certificate.json` has SHA-256
`8bd5e4a87223a454b0d666ee182ae11c47bc4709a9f15c3ccdb050cfdc04963b`.
Each row identifies one deleted vertex and a 159-character word. Its sole
`-` marks the deleted vertex; all other entries lie in `0123`, and the three
terminal entries are `000`. All 156 private indices must appear exactly
once in ascending order. Hashes identify inputs and evidence; the proof
comes from checking the words and the written restriction argument.

## Optional witness rediscovery

With `python-sat==1.9.dev15` installed in the selected Python environment:

```bash
python -B hadwiger_nelson_a159_module_compression/discover.py \
  --out /tmp/hn-a159-deletion-rebuild
python3 -B hadwiger_nelson_a159_module_compression/verify.py \
  --certificate /tmp/hn-a159-deletion-rebuild/certificate.json \
  --producer-edges /tmp/hn-a159-deletion-rebuild/producer_edges.json
```

The output directory must be new. The producer issues exactly 156 incremental
Glucose42 queries, each with a one-million-conflict budget. The pinned run
gave 156 SAT answers, no unresolved cases, 33,218 conflicts and 45,304
decisions in 2.95 seconds including exact graph construction. A different
valid witness library is accepted; its hash need not match the original.
No UNSAT assertion, hidden trace or solver-completeness premise enters the
result. Incomplete discovery output fails the complete-coverage checker.

The standard exactly-one encoding has x(v,c)=4v+c+1 for v=0..158,
c=0..3, and activation a(v)=637+v. A unit edge vw has clauses
`not a(v) or not a(w) or not x(v,c) or not x(w,c)` for each c.
Every vertex retains an exactly-one colour constraint, including the
inactive one; its colour is ignored on decoding. Terminals are pinned to
colour zero. Query v assumes only a(v) false and every other activation
true. Therefore satisfying assignments correspond exactly to colourings
of A-v with monochromatic terminals, together with an arbitrary colour on
v. Palette symmetry makes choosing terminal colour zero harmless.
There are 795 variables and 3,700 base clauses; the canonical DIMACS hash
and discovery statistics are in [DISCOVERY.json](DISCOVERY.json).

The producer uses an eight-radical multiplication table. The checker imports
no producer or inherited geometry implementation, using the explicit square
formula in the four-dimensional basis 1,sqrt3,sqrt11,sqrt33. This supplies
independence from both the solver encoding and the producer's unit-edge
calculation. Remaining trust lies in Python integer arithmetic, the
independence of this radical basis, decoding, the input coordinates,
Brooks' theorem for the assembly corollary, and the unformalized proof.
These are author-run checks; reviewer-1 has not issued an independent verdict.

The completed gate and [durable synthesis handoff](HANDOFF.md) preserve the
next interface. No new gadget, mixed assembly or repair search is included.
