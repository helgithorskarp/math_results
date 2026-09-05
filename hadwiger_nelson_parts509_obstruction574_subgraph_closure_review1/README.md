# Independent review: H574 subgraph closure

## Verdict

**Accepted, with the stated scope.** Every subgraph on at most 508 vertices
of the one explicit 574-vertex unit-distance graph `H=L union X` is
four-colourable. This rules out a strict improvement of the 509-vertex record
by vertex deletion inside this particular host.

It does not produce a smaller five-chromatic graph, prove that the 509 forced
vertices induce a five-chromatic graph, establish vertex-criticality of H, or
close the larger 677-point coordinate universe. The non-four-colourability of
H is context, not a premise of this positive-certificate theorem.

Reviewed Discovery Net contribution:
`bafkreicrocfo2rqsaeiqluhgrt36mw4ypwprnmo6hhe4j7fns2gpw5c7aq`.
The reviewed directory is unchanged from source commit
`6fd4065d7351caf6959453351fe6f5545c54a2e1`.

## Mathematical bridge

Let F be a set of distinct vertices of a graph H, with a proper
four-colouring of `H-v` for every `v in F`. Any subgraph J of H on fewer than
`|F|` vertices omits some `v in F`, so J is a subgraph of `H-v`; restricting
that colouring gives a proper four-colouring of J. This also covers
non-induced subgraphs because deleting edges preserves a proper colouring.

Here the certificate provides 309 deletion colourings for L-vertices
`0,...,308`. The prior positive certificate provides another 200 for the
distinct vertices in X. Thus `|F|=509`, and the lemma covers every subgraph
through order 508. The 65 untested L-vertex deletions are irrelevant to this
specific threshold.

## Independent exact audit

[independent_check.py](independent_check.py) imports no submitted module and
does not use the author's expected-result file. It reads the primitive point
tables directly and performs exact integer arithmetic in the basis

```text
1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165).
```

These square classes are independent, so equality is coefficientwise. The
checker tests all 164,451 unordered pairs of the 574 distinct points at common
denominator 288. It recovers exactly 2,707 strict unit edges, whose canonical
stream has SHA-256
`37d330b472e101c001e04aca6a1dc52ddf4f048d025adce0794f4e521682f575`.

The checker then assembles the 200 earlier colourings from their indexed
L-witness and X strings, reads the 309 new full strings, requires exactly one
deletion marker at the claimed vertex, and checks every surviving edge. All
509 colourings pass, totaling 1,372,888 retained-edge incidences. The assembled
witness family has SHA-256
`fff0bfe209c128f6dc7dc697f997b9d58f593eeb7907d5fc26c85cf2b8870d3b`.
Controls reject a missing deletion marker, a forced monochromatic edge, and
truncated deletion coverage.

The submitted verifier independently returned the same graph and certificate
counts in about five seconds. The clean-room checker completed in about 12.3
seconds. Neither route invokes a SAT solver or trusts an UNSAT result; the
explicit positive colourings are the certificate.

[report.json](report.json) pins the six primitive input hashes and records the
derived geometry, coverage, witness digest, and theorem boundary.

## Reproduction

From the repository root with CPython 3.11 or later:

```sh
python3 -B hadwiger_nelson_parts509_obstruction574_subgraph_closure/verify.py
python3 -B hadwiger_nelson_parts509_obstruction574_subgraph_closure_review1/independent_check.py \
  --repository . \
  --report /scratch/hn574-subgraph-closure-review1.json
cmp hadwiger_nelson_parts509_obstruction574_subgraph_closure_review1/report.json \
  /scratch/hn574-subgraph-closure-review1.json
cd hadwiger_nelson_parts509_obstruction574_subgraph_closure_review1
sha256sum -c SHA256SUMS
```

Expected terminal facts are 574 distinct vertices, 2,707 unit edges, 509
distinct deletion witnesses, 1,372,888 retained-edge checks, and closure
through order 508.

## Trust boundary

The coordinate, pool, interface-witness, and certificate files are imported
as the explicit definition and positive data; their exact hashes are pinned.
The geometry and every witness are rechecked independently. Remaining trust
lies in the ordinary finite-set argument, this compact checker, CPython and
hardware, and SHA-256. There is no floating-point distance test, solver trust,
negative proof trace, proof-assistant formalization, or claim of external peer
review. Reviewer scratch output is preserved under
`/scratch/research-team-v2/tmp/reviewer-1/hn574_subgraph_closure_review1`;
no reviewer-owned process remains active.
