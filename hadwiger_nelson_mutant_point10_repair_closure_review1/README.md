# Independent review of the mutant point-10 repair closure

Verdict: **ACCEPT**, at high confidence, for the following exact scoped
theorem. Let `M` be the specified 509-point, 2,447-edge nine-move mutation of
Parts's graph and let

```text
q = ((sqrt(33)-9)/12, (3sqrt(11)-sqrt(3))/12).
```

The complete strict plane unit-distance graph `H=UD(M union {q})` has 510
distinct vertices and 2,456 edges. Its chromatic number is five, while `H-v`
is four-colourable for every one of the 509 parent vertices `v`. Consequently
every arbitrary subgraph of `H` on at most 508 vertices is four-colourable,
the least order of a five-chromatic subgraph inside this host is exactly 509,
and for every point subset `W` of `H` the complete strict unit graph on `W`
is five-chromatic if and only if `M` is contained in `W`.

The reviewed source is
[`hadwiger_nelson_mutant_point10_repair_closure`](../hadwiger_nelson_mutant_point10_repair_closure/README.md)
at commit `53065ba7c2cd481a3febaae34a2dd5f0863cd89d`. Its imported parent is
[`hadwiger_nelson_neutral_mutation_candidate`](../hadwiger_nelson_neutral_mutation_candidate/README.md)
at commit `da761932c49900fe2bfe3ad90b9bdde49bc32577`.

## Scope of acceptance

This is a complete exclusion in one exact finite 510-point support. It is
**not** a 508-point construction, a lower bound for arbitrary plane
unit-distance graphs, a classification of other points added to `M`, or an
exclusion for other mutations. The induced-support equivalence keeps every
physical unit contact among the chosen points; it is not an iff statement for
edge-deleted abstract graphs.

The unrestricted published order record remains Parts's 509-vertex,
2,442-edge construction
([arXiv:2010.12665](https://arxiv.org/abs/2010.12665)). Haugland's August 2026
paper also identifies 509 as the current record; its larger construction
advances the Moser-spindle-free restricted problem, not this order record
([arXiv:2608.04542v4](https://arxiv.org/html/2608.04542v4)). The reviewed
509-point parent has five more edges than Parts's record graph but does not
improve its order.

## Independent physical and positive-certificate audit

[`independent_check.py`](independent_check.py) imports no implementation from
the target or parent. It pins the target, the parent certificate, and the
upstream coordinate and colouring payloads by SHA-256. It rebuilds arithmetic
in the reversed nested tower `Q(sqrt(5))(sqrt(11))(sqrt(3))`, checks all 64
basis products, converts all coordinates to denominator 288, rejects point
collisions, and directly tests all 129,795 host pairs. It recovers exactly
2,456 unit pairs with edge hash
`1e34a544293e9bc182dfcea9022937720068edc5b2a4a1e68223b73dc48aa54f`.
Restricting this stream to the first 509 points gives the parent's exact 2,447
edges. The added point's local neighbours are independently recovered as

```text
18,43,56,64,151,166,237,284,325.
```

The checker directly decodes and checks every positive witness used in the
argument. It reconstructs all 509 parent deletion words, then validates the
506-row cyclic and hinge libraries before selecting extensions. The final 509
host words use 475 base-parent rows, 25 cyclic rows, 6 hinge rows, and the 3
new target rows (for deletions 18, 107, and 275). All pass 1,245,201 retained-
edge checks. Their expanded stream hash is
`ed68e6ef9cb0d1da535f4d67368aa7c383f9aee18b243a969503e606849bac69`.
A deliberately corrupted word is rejected. Normal and optimized Python runs
are byte-identical to [`EXPECTED_OUTPUT.txt`](EXPECTED_OUTPUT.txt).

These checked words alone establish the through-508 exclusion: any such
subgraph omits some parent vertex `v` and is contained in the four-colourable
graph `H-v`. They do not by themselves establish that order 509 is attained;
that matching statement uses the parent's non-four-colourability.

## Independent chromatic lower bound

The parent's canonical 2,036-variable, 13,354-clause CNF was regenerated with
SHA-256
`ba3c9cbcb8958c41282382abbc79a4c307acfa2ea6debb45d2ce15ec0a9058ce`.
Kissat 4.0.4 regenerated the recorded 5,917,687-byte DRAT trace byte-for-byte,
and `drat-trim` returned `s VERIFIED`. Together with the independently checked
parent five-colouring, this proves `chi(M)=5`.

For stronger independence, the review emits a different, symmetry-free CNF.
It has one at-least-one-colour clause per vertex and only equal-colour edge
exclusions—no at-most-one clauses and no triangle pins. This is equivalent to
four-colourability: from any satisfying assignment choose one true colour at
each vertex; edge clauses make the choices proper, and every proper colouring
gives a satisfying assignment. The 2,036-variable, 10,297-clause file has
SHA-256
`4b40b25b1dd695b123c8ce9ed99c97a3f609abfb52217eca3f5a7c4742b55114`.

Kissat 4.0.4 returned UNSAT in 217.597 seconds. Its 194,055,334-byte proof has
SHA-256
`19578b4b6fa64334159afd49bad4bd57c9f57bb517f8557138a884d14cc45029`,
and `drat-trim` verified it. Independently, CaDiCaL 1.9.5 returned UNSAT in
266.788 seconds; its 170,518,970-byte proof has SHA-256
`6cf456434366c79f7d5fab9452181881a840bcf00186f7ac8782cf9426c1c22f`
and was also verified by `drat-trim`. The generated CNFs and proof traces stay
outside Git; exact tool identities and results are recorded in
[`REPRODUCTION_RESULT.json`](REPRODUCTION_RESULT.json).

One minor reproducibility defect does not affect the theorem. The parent
verifier's convenience `--kissat` path always passes `--quiet`, but the cited
Kissat commit when configured with `--no-options` rejects that option. Running
Kissat directly and then using the verifier's `--proof` path succeeds and
reproduces the recorded proof exactly.

## Reproduce

From a complete repository checkout with Python 3.11 or later:

```sh
mkdir -p /scratch/mutant-point10-review
PYTHONDONTWRITEBYTECODE=1 python3 -B \
  hadwiger_nelson_mutant_point10_repair_closure_review1/independent_check.py \
  --cnf-out /scratch/mutant-point10-review/alternative-parent.cnf \
  | diff -u \
      hadwiger_nelson_mutant_point10_repair_closure_review1/EXPECTED_OUTPUT.txt -

(cd hadwiger_nelson_mutant_point10_repair_closure_review1 && \
  sha256sum -c SHA256SUMS)

kissat /scratch/mutant-point10-review/alternative-parent.cnf \
  /scratch/mutant-point10-review/kissat.drat
drat-trim /scratch/mutant-point10-review/alternative-parent.cnf \
  /scratch/mutant-point10-review/kissat.drat

cadical --seed=260914 \
  /scratch/mutant-point10-review/alternative-parent.cnf \
  /scratch/mutant-point10-review/cadical.drat
drat-trim /scratch/mutant-point10-review/alternative-parent.cnf \
  /scratch/mutant-point10-review/cadical.drat
```

The source verifier, its independent same-author audit, and its corruption
controls were also replayed under both normal and optimized Python where
applicable; all matched their published outputs.

## Limits and trust boundary

The review trusts the hash-pinned input bytes, the elementary exact-field and
CNF bridges described above, CPython integer/rational semantics, SHA-256,
ordinary hardware, and `drat-trim`. Solver answers without checked proof traces
are not trusted. The large traces are reproducible but not committed. No proof-
assistant formalization or independent derivation of Parts's original
coordinate corpus is supplied.

Within those limits, I found no collision, missing or spurious unit contact,
malformed colouring, deletion-coverage gap, CNF mismatch, invalid proof, or
scope-changing hidden assumption. Acceptance is warranted for this exact
510-point host theorem, with its non-record and restricted-family status kept
explicit in every downstream use.
