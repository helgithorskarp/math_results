# Independent review of the point606 530-vertex critical core

Verdict: **ACCEPT**, at high confidence, for the following exact scoped claim.
The graph specified by the reviewed certificate is a strict plane
unit-distance graph on 530 distinct points and 2,648 complete unit edges; it
has chromatic number five; and deleting any one vertex leaves a four-colourable
graph.  It is therefore 5-vertex-critical.

The reviewed source is
[`hadwiger_nelson_point606_criticality_gate`](../hadwiger_nelson_point606_criticality_gate/README.md)
at commit `e9d715e5be1defc32ef6bd87b7f0381220f03055`.  No Discovery Net contribution
was submitted for that source, so this review has no target artifact relation.

## Scope of acceptance

This is **not** a record construction.  The accepted graph has 530 vertices,
22 more than the campaign's at-most-508 target and 21 more than Parts's
published 509-vertex graph.  It proves nothing about whether a different
at-most-508 induced subgraph of the 586-point host exists.  It also does not
validate the target author's inconclusive conditional-selector follow-on,
intermediate solver-only UNSAT answers, or any other deletion order.

As a global benchmark check, Parts reports a 509-vertex, 2,442-edge
five-chromatic plane unit-distance graph in
[arXiv:2010.12665](https://arxiv.org/abs/2010.12665).  Haugland's August 2026
paper still calls 509 the current record; its new 2,131-vertex graph advances
the Moser-spindle-free restricted problem, not the unrestricted order record
([arXiv:2608.04542v4](https://arxiv.org/html/2608.04542v4)).

## Independent geometric and positive-certificate audit

[`independent_check.py`](independent_check.py) imports no code from the
reviewed package.  It pins the target certificate and all upstream coordinate
and colouring-library inputs by SHA-256.  It parses the original scale-96
integer table and all rational completion coordinates, rescales them to the
common denominator 288, and implements multiplication directly in the
bit-mask basis of `Q(sqrt(3),sqrt(5),sqrt(11))`.

All 171,405 host pairs are tested by exact integer arithmetic.  The checker
finds 586 distinct points and 3,090 unit edges, including exactly 2,442 edges
among the original 509 points.  It independently confirms

```text
q606 = (-(1+sqrt(33))/6, (sqrt(3)+sqrt(11))/6)
N(q606) = {37,51,69,142,180,198,530}.
```

Removing the 56 certificate labels gives 530 distinct points and all 2,648
unit contacts, with the target point- and edge-stream hashes.  The checker
then directly tests the supplied five-colouring on every edge.  It expands
the 451 compressed references to old colouring words, reads the 79 new literal
words, and checks all 530 single-vertex deletions against the independently
reconstructed core.  This makes 1,398,144 deletion-word edge checks.  Four
length, palette, and monochromatic-edge corruptions are rejected.

The older libraries are used only as compressed positive witness data.  Their
previous nonexistence claims are not premises of this review: every imported
word is expanded and checked directly on the present graph.

## Independent non-four-colourability certificate

The target's original CNF gives each vertex a nonempty set of colours, forbids
adjacent vertices from sharing any true colour, and pins a unit triangle.
This is equisatisfiable with graph four-colourability: choosing any true colour
at each vertex gives a proper colouring, and every proper colouring satisfies
the clauses after a global permutation on the pinned triangle.  The target
workflow regenerated its 2,058,905-byte DRAT proof byte-for-byte, and
`drat-trim` accepted it.

For a stronger independence check, this review emits a structurally different
CNF.  It requires **exactly one** colour per vertex using all pairwise at-most-
one clauses and applies **no symmetry breaking**.  Its 2,120 variables and
14,302 clauses have SHA-256
`1f82ca98fb1fa37caa70c955b053df309e972edd4ca5638d13b04206803b3b44`.
The encoding was exhaustively compared with its definition on all 33,297
Boolean assignments to all graphs through three vertices.

Kissat 4.0.4 returned UNSAT in 65.789 seconds.  Its 61,970,993-byte proof has
SHA-256
`31f7f4c60224833cf3522a21d1a872c1b6ee376249a7fff6eeba40e93f994082`;
`drat-trim` returned `s VERIFIED`.  Independently, CaDiCaL 1.9.5 returned UNSAT
in 70.909 seconds.  Its 62,414,368-byte proof has SHA-256
`3af994c7f39b32be367724c1e04aaf9f10fdc5806d64f2402c47328c8bf346d9`;
`drat-trim` also returned `s VERIFIED`.  Proofs and CNFs are generated outside
Git; compact identities and timings are recorded in
[`REPRODUCTION_RESULT.json`](REPRODUCTION_RESULT.json).

The explicit five-colouring and checked alternative UNSAT proof establish
`chi(G)=5`.  For every vertex `v`, the checked four-colouring of `G-v` proves
`chi(G-v)<=4`.  Every proper induced subgraph is contained in one of these
deletion graphs, so the stated vertex-critical conclusion follows.  No
edge-critical claim is made.

## Reproduce

With Python 3.11 or later, from the repository root:

```sh
mkdir -p /scratch/point606-review
PYTHONDONTWRITEBYTECODE=1 python3 \
  hadwiger_nelson_point606_criticality_gate_review1/independent_check.py \
  --cnf-out /scratch/point606-review/alternative.cnf \
  | diff -u \
      hadwiger_nelson_point606_criticality_gate_review1/EXPECTED_OUTPUT.txt -
(cd hadwiger_nelson_point606_criticality_gate_review1 && \
  sha256sum -c SHA256SUMS)

kissat --seed=260914 -f /scratch/point606-review/alternative.cnf \
  /scratch/point606-review/kissat.drat
drat-trim /scratch/point606-review/alternative.cnf \
  /scratch/point606-review/kissat.drat

cadical --seed=260914 /scratch/point606-review/alternative.cnf \
  /scratch/point606-review/cadical.drat
drat-trim /scratch/point606-review/alternative.cnf \
  /scratch/point606-review/cadical.drat
```

## Limits and trust boundary

The large proof traces are not committed.  A reader must regenerate or obtain
one of the hash-pinned traces to replay non-four-colourability; the Python
checker alone verifies only geometry and positive colourings.  The audit
trusts the pinned exact coordinate and witness bytes, CPython integer/rational
semantics, SHA-256, ordinary hardware, and `drat-trim`.  Solver verdicts alone
are not trusted.  No proof-assistant formalization or independent derivation
of the upstream Parts coordinate corpus is supplied.

Within those limits, I found no point collision, missed unit contact, invalid
colouring, coverage gap, CNF error, hidden interface restriction, or failed
proof certificate.  Acceptance of this physical 530-vertex critical graph is
warranted, while its explicit failure to improve the 509 record must remain
part of every downstream citation.
