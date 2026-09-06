# H517: the three-large-deletion family is four-colourable

**Every graph obtained from the fixed H517 support by deleting three large
vertices and six small vertices is four-colourable.** Consequently every
subgraph retaining at most 372 large and at most 136 small vertices is
four-colourable, including graphs with deleted edges.

Together with the [previous two-large closure](../hadwiger_nelson_heule517_large2_pilot/README.md),
this proves that every non-four-colourable H517 subgraph on at most 508
vertices must retain **at least 137 small vertices and at most 371 large
vertices**. It must delete at least four large vertices. The unrestricted
at-most-508 family remains open. No record graph or unconditional
137-small lower bound for larger graphs is asserted.

## Exact support and evidence

G is the fixed [H517 graph](../hadwiger_nelson_heule517_family_pilot/README.md):
the 510 increasing union-certificate labels marked `510`, followed by
completion-centre indices 327,439,671,1040,1074,1377,1383. G indices
0..509 are those sorted union labels; 510..516 are the seven centres
in that order, not original Heule or Parts indices.

Coordinates have denominator 96 in the positive-radical basis
1,sqrt(3),sqrt(5),sqrt(15),sqrt(11),sqrt(33),sqrt(55),sqrt(165).
L consists of the points whose sqrt(5),sqrt(15),sqrt(55),sqrt(165)
coefficients vanish in both axes, and S is the complement. The complete
exact graph has 517 distinct points, |L|=375, |S|=142 and 2555 unit
edges: 1920 in L, 605 in S and 30 cross-edges. The checker reconstructs
all 133386 pair distances. [manifest.json](manifest.json) pins the
coordinate inputs, positive certificates and reused code.

Initial evidence consists of 526 full-pilot rows, 202 small134 rows and
86 two-large rows. The latest source commit is
`86287fd43140e23790f97a3d267299585f0335e7`. All 814 positive witnesses
are checked directly. Their inclusion antichain has 571 rows and forces
397 individual vertices: 271 large and 126 small. A row with omitted
set D is a proper four-colouring of G minus D, so every
non-four-colourable subgraph must intersect D.

## Exhaustive coupled reduction and proof

The 16 initially nonforced small vertices are reconstructed from the
singleton witnesses. Of all binomial(16,6)=8008 six-element omission
sets, exactly 38 avoid containing a pure-small cut. Every other small
omission is already covered by an inherited colouring. There is no
symmetry reduction or sampling.

For a surviving small omission set O, consider every inherited cut whose
small part is contained in O. Its large part has size one or two. A
singleton large part forbids omission of that vertex. A two-element
large part forbids every large omission triple containing that pair.
Exhausting the remaining triples over all 38 cases leaves **749066**
candidates not yet covered by the inherited witnesses. This is not a
count of non-four-colourable graphs.

The new [certificate.json](certificate.json), 60944 bytes, supplies 108
full colour strings over `.0123`, of length 517 in G order. D is exactly
the increasing list of dots. `native_index` identifies the zero-based
original run position and is only provenance. No native run file is
needed to decode a public witness. The rows comprise 70 singletons,
25 pairs, 12 triples and one four-set.

The independent checker validates all 108 complete colourings and then
checks **every one of the 749066 surviving triples A**. In each case
some new D is contained in O union A. The colouring of G minus D
restricts to that candidate. Cases discarded earlier inherit an old
colouring. This proves the entire three-large/six-small deletion family.
Any subgraph with at most 372 large and at most 136 small vertices can
be enlarged to one of those supports, proving the stronger restriction
statement, including edge-deleted graphs.

For the record-order corollary, the previous two-large theorem already
colours every at-most-508 subgraph having at most 135 small vertices.
If a graph of that order has exactly 136 small vertices, it has at most
372 large vertices and the new theorem applies. Any remaining
non-four-colourable graph must therefore have at least 137 small
vertices, leaving at most 371 large vertices.

The new family theorem needs only exact geometry, positive witnesses
and finite enumeration. The target-order corollary additionally invokes
the published two-large theorem, Discovery Net
`bafkreier76meo5hh34flh5u7mb6sja2l6dg37wp2deg53xg4qvss45mc5i`.
This checker does not rerun that already completed family proof. Its
certificate and solver-free checker remain public in the linked source.

## Frozen native decision

The [plan](plan.json) fixed at most 256 full-graph queries, each with
100000 conflicts and 4 GiB address space. The producer cycles through
the lexicographic surviving small omission sets and chooses each case's
lexicographically least uncovered large triple. Every candidate has
exactly 372+136=508 vertices. Coverage can remove candidates in any case,
so a case need not receive a query of its own.

The oracle is the full activated H517 four-colouring formula with all
517 activations specified: 2585 variables and 10738 clauses. It has
four colour variables per vertex, a guarded at-least-one colour clause,
four inequalities per unit edge, and an origin-colour normalization
guarded by the origin's activation. Inactive vertices can have every
colour variable false. Adjacent true-colour sets are disjoint, so
at-most-one constraints are unnecessary. Decoding selects one true
colour per active vertex and checks every retained unit edge.

Each positive colouring is greedily extended over omitted large
vertices and then omitted small vertices, and checked again. Only
candidates avoiding the remaining D are removed. No completeness
assumption for the intact-L 20-pattern relation is imposed after L
deletions.

The entire family closed after **152 queries, all SAT**, touching 36
of the 38 small cases. There were no UNKNOWN answers or negative
targets. The run took 25.1051 seconds, peak RSS 99068 KiB. No bound
was extended. All 152 native witnesses are preserved locally; each
omitted public row is subsumed by one of the 108 retained rows.
[run_summary.json](run_summary.json) records the outcome.

The producer preserves the frozen bounded negative-target branch:
a fresh Kissat proof, independent DRAT check, and checked five-colouring
would be required. That branch was not exercised. No negative SAT
answer or proof trace is needed for this closure.

## Reproduce and inspect the trust boundary

From this directory in a full checkout, Python 3.11.2 and the standard
library suffice:

```bash
python3 -B verify.py --report /scratch/heule517-large3-check.json
sha256sum -c SHA256SUMS
```

Expected output includes `six_sets_checked=8008`,
`large_triples_checked=749066`, `remaining_triples=0` and
`negative_solver_proof_required=false`. The corollary fields explicitly
record their dependence on the prior two-large theorem. To reproduce
that prerequisite separately, run its public `verify.py` as documented
in its directory.

[verify.py](verify.py) imports the hash-pinned independent monomial
geometry routine, not the producer or any SAT solver. It checks all
814 inherited positive rows (2068268 edge inequalities), all 108 new
rows (274371 inequalities), all six-small omissions, and the complete
large-triple cover.

The author also ran `--work /path/to/native-run`, checking all 152 native
witnesses (385584 edge inequalities), their public subset and subsumption,
the full round-robin candidate sequence, every removal count and the
actual activated CNF entry by entry. The audit took 14.9821 seconds,
including 3.8436 seconds for the coupled cover.
[verification.json](verification.json) records it. A public-only run
proves the same new family theorem without native files. The checker
is independently implemented and author-run; no separate-author review
or formalization is claimed.

Discovery used python-sat 1.8.dev24 and CaDiCaL 1.9.5. The reproducible
bounded producer invocation is:

```bash
python3 -B run.py --work /scratch/heule517-large3-fresh \
  --kissat /path/to/kissat --drat /path/to/drat-trim
```

Kissat 4.0.4 and drat-trim would be used only for a negative target.
The actual activated formula has SHA256
`21fcfe71a6162a4ac3577456d50e607479dd2358001991e814e49aa95ff29a9f`.
Native formulas, logs and checkpoints remain outside the repository.
The proof boundary is exact coordinate data, Python integer arithmetic,
colouring decoding and the complete finite cover. No floating-point
approximation, negative solver trust or omitted large proof is needed.

## Completed boundary and separate shared work

The three-large/six-small family is closed. The next proposed bounded
target family deletes four large and five small vertices, retaining
371+137=508. It can reuse all verified colourings. That level has not
started; no background job or unfinished proof remains.

HN-3's full fixed heptagon-spindle rotation closure was inspected at
source `edc54718fba597ce37f5377fca70213bda133784`, Discovery Net height
3124. Its last 480 elimination graphs close every remaining contact
equation, and its theorem covers every rotation of those fixed factors.
Changed factors or additional points are outside that result. The
geometric family supplies no premise here. Neither lane has established
a record improvement.
