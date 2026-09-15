# Provenance and independence

## Reviewed target

- Branch path:
  <https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_golomb_opposed_b214_stop>
- Exact revision: `42fd5e441e190a4022743479458aabf2ca55a85b`.
- Target checker SHA-256:
  `3520b0e61bf1115c237d2c657dac06205eb194a97bd6975fa5c73847686bc00b`.
- Target certificate SHA-256:
  `3f6a4a13ead37de71ceb3cd1818d21a9036ea0273e151461fc54d9df1a8c2e19`.
- Target RUP trace SHA-256:
  `e3f5c84e89d442d9d5ced2246681defdbccc9fa8cf4eeaebdbd78fec7b966e29`.
- Target expected-output SHA-256:
  `5b438990372d53ae3ff7bc2159b92f390f4aa17d427cddb9c1c07ef7cb7d25c0`.
- Target manifest SHA-256:
  `b3aa4ebe2e0951d16ce669c6ccd30d1c76a3ca73887e1da4a74f84268d15613e`.

Normal and optimized target runs produced byte-identical theorem output. The
target contribution
`bafkreic64ql2lr7na27efoi5mxhny2arsxezc2qotvwccnaegw2qoprg44` was accepted
for broadcast but was absent from the committed height-4,363 index at review
intake.

## Public coordinate inputs

Both files were last modified at repository revision
`fa6f78f998ba36a40a8077f2c00d3656d0b40322`.

| Repository path | SHA-256 |
|---|---|
| `hadwiger_nelson_nonmono159_214_lowden2/points159.tsv` | `4f72fa06d18434472ce77cebe38880333694ec04b94945ede073a4a1c6d5bc02` |
| `hadwiger_nelson_nonmono159_214_lowden2/points214.tsv` | `97c9b3a964ed19874ae3fe932eb8c085fd637f618d2481fffaebbd1fbae55c2f` |

The review verifies these byte hashes before parsing. Reproduction requires a
full repository checkout; the source tables and target's roughly 130 KB of
positive/RUP evidence are not duplicated.

## Algorithmic independence

The target projects its coordinate input into the four-term subbasis and uses
generic gcd/squarefree-radicand multiplication. The reviewer retains all eight
multiquadratic coefficients and uses subset-mask multiplication. The target
RUP checker maintains two watched literals; the reviewer maintains literal
occurrence lists and remaining-literal counts. The latter is compared against
a slow definition-level unit-propagation oracle on 10,240 small cases.

The target's point maps and edge summaries are not inputs to the review.
Golomb embeddings are recovered by exact coordinate lookup, and all physical
edges, component images, contacts, positive words, relation prefixes, CNF
clauses, RUP steps, chromatic lower bounds, and cut structures are recomputed.
No private source, Discovery ledger, solver binary, floating-point decision,
or generated CNF is required.
