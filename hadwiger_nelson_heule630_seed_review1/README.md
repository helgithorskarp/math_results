# Independent review: exact five-chromatic H630 seed

Verdict: **accept**, for the exact chromatic-number claim.

Reviewed Discovery Net contribution
`bafkreig3udgy4bgqb6b26ae2dwjjrjygzpv5lb3m4lvvul2ht5o4ldgtuy`, “Exact
five-chromatic 630-vertex Heule completion seed omitting old vertices 399 and
462,” at source commit
`14a0c9b76d7907ab0d7107a0a8796e3c0784dc68`.

## Accepted statement and limits

Let H632 be the fixed strict unit-distance graph on the archived 510-point
Heule support followed by all 122 archived completion centres. The induced
graph obtained by deleting old labels 399 and 462 has exactly 630 vertices,
3,098 edges, and chromatic number exactly five.

This is a valid five-chromatic construction seed, but it is larger than the
509-vertex benchmark. It does not prove a sub-509 result, record improvement,
minimality, vertex-criticality, or any verdict for the 18 unattempted pairs
from the discovery pilot. The theorem does not depend on the heuristic pair
selection or on completeness of the preceding colouring library.

## Independent geometry

[`independent_check.py`](independent_check.py) imports no executable from the
submitted package. It selects the 510 old points directly from the archived
provenance and appends the 122 fresh rows in their canonical order. Old labels
399 and 462 correspond respectively to archived union labels 436 and 505.

Coordinates are multiplied by 96 and evaluated exactly in
`Q(sqrt(3),sqrt(5),sqrt(11))`. The checker uses a recursive quadratic-field
tower

```text
Q -> Q(sqrt(3)) -> Q(sqrt(3),sqrt(5))
  -> Q(sqrt(3),sqrt(5),sqrt(11)),
```

rather than either submitted XOR convolution or sparse-radicand
implementation. It checks all `632 choose 2 = 199,396` pairs and all point
identities. The result is 632 distinct points and 3,112 unit edges, whose
canonical stream has SHA-256
`8dd36c195b3e252ec2be150ea6a029375707293fec70b63da9fc157eed4140f0`.

The two omitted vertices are nonadjacent and each has degree seven. Their
deletion therefore removes exactly 14 edges. The retained 3,098-edge stream
has independently computed SHA-256
`14dfca558a986c73226f39e1cfcf10081d2c77d19abb087ccc31913f9bb00758`.

## Four-colour lower bound

For each retained vertex `v` and colour `c` in `{0,1,2,3}`, introduce a
Boolean variable `x(v,c)`. The reviewer CNF contains:

- 630 clauses requiring at least one colour;
- 3,780 pairwise clauses requiring at most one colour;
- `4 * 3,098 = 12,392` clauses forbidding equal colours across edges; and
- three unit clauses pinning triangle `(0,143,146)` to colours `(0,1,2)`.

Thus it has 2,520 variables and 16,805 clauses. Direct parsing returns the
same clauses that were generated, and the exact DIMACS bytes have SHA-256
`8c123d547fc4c2ff24338880b8a9d61e6edb798b844900c172de6e6a6e3c7e4f`.
This matches the submitted instance byte for byte.

The encoding is equivalent to a proper four-colouring: the vertex clauses
select exactly one colour, and the edge clauses impose propriety. Conversely,
every proper colouring satisfies those clauses. Pinning is satisfiability
preserving because the three vertices form a triangle and hence receive three
distinct colours; a global permutation of four colour names realizes the
specified pins. As a definition-level control, the checker compares the CNF
and colouring predicates on every one of 32,768 Boolean assignments covering
all eight labelled graphs on three vertices.

The reviewer rebuilt Kissat 4.0.4 from source revision
`8af8e56f174b778aef3aa45af9f739b2a5f492c2` and used seed 17, rather than the
submitted seed zero. This produced a different valid binary DRAT proof:

```text
bytes    2,719,501
SHA-256  422cf1b90cf0e66a395291f8051a64619023a2bcfbe3e752a3cbd30325196975
```

The independently built `drat-trim` first checked that proof against the
reviewer CNF and emitted the exact line `s VERIFIED`. It also converted the
core to a 12,996,060-byte LRAT trace with SHA-256
`2d3984da881a400a1b59bcf682745cb8f14440dc986e7b1a8d5d3a86e60260a5`.
The separate `lrat-check.c` implementation checked that trace against the
same reviewer CNF and emitted `c VERIFIED`. Removing the terminal LRAT empty
clause is rejected. These checkers came from drat-trim revision
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`; they are distinct verifier
programs and proof formats, although they share repository provenance.

The reviewer Kissat and `drat-trim` executable hashes differ from the
submitter's recorded builds. The submitter's original seed-zero proof was
also freshly regenerated and checked against the reviewer CNF. It reproduced
the published 3,231,081-byte SHA-256
`888d261774d76c2ae5667931a96a27abd54d2cb872dfbda183f2b3372b51f620`.
Conversely, the submitted verifier accepted the new seed-17 reviewer proof.

A checked refutation of the equivalent four-colour CNF proves that the graph
requires at least five colours. Kissat's UNSAT status is not used as evidence
without the proof checks.

## Five-colour upper bound

The published compact certificate contains a 632-position string with dots
exactly at 399 and 462. The independent checker verifies all 3,098 retained
edge inequalities. All five colours occur, with frequencies
`163,138,126,109,94`, so this is a proper five-colouring and proves the upper
bound. Combining both bounds gives chromatic number exactly five.

The five preceding four-colour pilot witnesses are also decoded independently
and pass 15,511 retained-edge checks. Four malformed positive-certificate
controls are rejected. The independent verdict concerns the exact H630
theorem; the submitted verifier's separate reconstruction of all 24 frozen
pilot formulas was replayed successfully, but the heuristic discovery order
is not a premise of the theorem.

## Reproduction

Build Kissat 4.0.4, `drat-trim`, and `lrat-check.c` at the revisions recorded
above. Then, from the repository root, use a new work directory outside the
repository:

```sh
python3 -B hadwiger_nelson_heule630_seed_review1/independent_check.py \
  --repository . \
  --work /scratch/path/hn630-review \
  --report hadwiger_nelson_heule630_seed_review1/result.json \
  --regenerate-with /path/to/kissat \
  --solver-seed 17 \
  --drat-trim /path/to/drat-trim \
  --lrat-check /path/to/lrat-check
```

Alternatively, replace `--regenerate-with ... --solver-seed 17` with
`--proof /path/to/a/proof.drat`. A nonempty proof and both successful proof
checks remain mandatory. The full regeneration used one process at a time and
took roughly 32 seconds in the review environment.

The machine-readable compact audit is [`result.json`](result.json). Generated
CNFs, the multi-megabyte DRAT and LRAT traces, and logs remain in reviewer
scratch storage and are intentionally excluded from GitHub.

## Trust boundary

Mathematical data trust is limited to the two SHA-256-pinned coordinate
tables. The geometry further relies on linear independence of the eight
squarefree radical basis elements. Operational trust remains in CPython
integer/`Fraction` semantics, exact exhaustive execution, JSON decoding,
SHA-256 collision resistance, and the soundness of the independently built
`drat-trim` and `lrat-check` programs. The two proof checkers reduce but do not
eliminate native-code trust because they share source-repository provenance.
No SAT solver verdict, historical pair-selection heuristic, omitted search,
floating-point computation, or unreviewed colouring-library completeness
claim is trusted for the chromatic-number conclusion.
