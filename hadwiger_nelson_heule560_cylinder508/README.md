# A complete 508-vertex cylinder decision and the H560 order-506 bound

Five explicit proper colourings prove that every member of the previously
unclassified 194,580-support H560 cylinder is four-colourable. The same witnesses
also cover 367,290 supports before the eight-vertex erasure. Three new
singleton-deletion colourings, combined with earlier positive witnesses, prove:

**Every subgraph of H560 on at most 506 vertices is four-colourable.**

This closes the defined support family below and raises the whole-H560 lower
bound from 504 to 507. It does not close the remaining orders 507 and 508, produce
a smaller obstruction, or improve the 509-vertex record. The pass ends here.

## Exact family

All labels refer to the 632 exact points reconstructed by the
[pair-pilot geometry](../hadwiger_nelson_heule632_pair_pilot/independent.py).
Coordinates use the rational basis
`(1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165))`.
After multiplying coordinates by 96, the checker uses integer radical
coefficients. It tests all 199,396 pairs exactly and obtains 3,112 unit edges;
there is no floating-point geometric predicate.

Let H560 be the induced support in the
[minimization certificate](../hadwiger_nelson_heule632_minimize/certificate.json),
and let M492 be the mandatory set in its
[boundary](../hadwiger_nelson_heule632_minimize/boundary.json). Put

```text
D = {510,512,513,520,521,523,524,535}
G552 = H560 - D
U60 = V(G552) - M492
F = {310,361,362,393,406,407,409,434,500,505,578,604}
A504 = M492 union F
W48 = U60 - F
```

The family decided here consists of **every** induced graph
`G552[A504 union X]`, where `X` ranges over the four-element subsets of W48.
Its size is `binomial(48,4) = 194580`. The earlier
[global decision](../hadwiger_nelson_heule560_global_decision/README.md) specified
this entire cylinder as outside its 35 positive covers and the ten older Kempe
covers. The producer checks that provenance before searching.

The original H560 extension family allows X in `V(H560) - A504`, a 56-element
set. It has `binomial(56,4) = 367290` members. This second closure follows by
lifting the same five witnesses; it required no additional solver search.

## Compact certificate and complete proof

[certificate.json](certificate.json) is 4,270 bytes and contains five full
632-position colour strings. A dot marks an absent vertex. The omitted sets
below are complements inside G552, not inside all 632 points.

| Cover | Omitted set C | Coloured G552 vertices | Coloured H560 vertices after lifting |
| --- | --- | ---: | ---: |
| 1 | `{615}` | 551 | 559 |
| 2 | `{539}` | 551 | 559 |
| 3 | `{498,571}` | 550 | 558 |
| 4 | `{454}` | 551 | 559 |
| 5 | `{440,609,613}` | 549 | 557 |

Each C is nonempty, disjoint from A504, and disjoint from the other four sets.
A four-element X cannot intersect five pairwise disjoint nonempty sets.
Consequently some C is disjoint from X, and the corresponding checked colouring
restricts to a proper colouring of `A504 union X`. This proves the entire
194,580-member family, including every member that was outside all old covers.

For each new witness the checker also pastes its right-side colours with a
matching explicit full-left colour string from the
[separator certificate](../hadwiger_nelson_heule560_separator/certificate.json).
It then checks the resulting colouring of **H560 minus C on every unit edge**.
The same disjoint-set argument therefore proves the 367,290-member original
family, even when X contains vertices of D. It also applies to extensions by
fewer than four vertices.

The checker independently enumerates both exact-508 families in increasing
labelled combination order. Assigning each support to its first covering row
gives counts `[178365,15180,946,87,2]` and `[341055,24804,1326,103,2]`, respectively.
There are no undecided members in either family. The corresponding one-byte
first-cover streams have SHA-256:

```text
194580: 9ab654d8da7cfb94f8a6fcc26e160118dccf629e7d2d059b16cd140ea5606206
367290: f6b4b4acecb848b43dda697330fbd431788b7f38cbdd0179eb954a7bb51dec39
```

## Whole-H560 corollary through order 506

An obstruction must meet every omission set C for which H560 minus C has a
proper four-colouring. The new singleton sets make vertices 454, 539 and 615
mandatory. Together with the earlier mandatory vertices 310, 393 and 578, they
give **M498**.

The checker reconstructs and directly verifies the old positive witnesses for
`{310}`, `{393}`, `{578}`, and these nine pairs:

```text
{358,362} {361,379} {406,455} {407,440} {409,542}
{431,505} {434,530} {500,571} {604,613}
```

The old witnesses are zero-based positive rows `3,2,14` and
`4,1,6,25,28,33,27,12,11` of the global certificate. Their lift when 310 is
absent uses an explicit positive word from the
[left-relation certificate](../hadwiger_nelson_heule560_left_relation/certificate.json).
It does not use or rerun that result's negative or completeness proofs.

The six singleton sets and nine pairs are 15 pairwise disjoint sets outside
M492, each with a directly checked proper-colouring complement in full H560.
The accepted M492 singleton-deletion theorem forces all 492 vertices of M492
into any obstruction. The 15 disjoint sets then force at least 15 further
vertices, so any non-four-colourable subgraph of H560 has at least
`492 + 15 = 507` vertices. Equivalently, M498 plus nine disjoint pairs gives
`498 + 9 = 507`.

Only this whole-H560 corollary imports the prior M492 mandatory theorem. The
five-cover family closure needs neither that theorem, the eight-vertex erasure
equivalence, completeness of the boundary-state tables, nor solver correctness.
It uses the explicitly defined support and checked positive colourings.

## Search and verification

[plan.json](plan.json) was frozen before the search; its SHA-256 is
`399d180a13b3cbd5d9412ee2717b97fe1336bfe49a5069cb267b77a256f5b477`.
The producer used the completed 60-selector equivalence without recomputing it.
Its oracle permits arbitrary recolouring of all 196 right-side vertices,
guards edges by 48 free selectors, and selects among the 20 explicit full-left
interface words. It has 852 variables and 4,977 clauses. The independent
constructor reproduced all 64,995 executed DIMACS bytes, SHA-256
`e6338623d8fbc1c3fc4dc6fa3ccf8eea49397dcdd0b495735d513e06527bbb2e`.

Five complete primary queries were SAT: the 504-vertex base and four uncovered
508-vertex members. Positive growth used 193 direct extensions and 30 bounded
recolouring queries: 23 SAT, seven UNSAT, zero UNKNOWN. One growth trial was
skipped using an old negative core. None of these growth exclusions is a
premise of the final positive proof, and no UNSAT result is claimed as a new
negative certificate. Search took 3.64 seconds in the recorded environment,
with peak RSS 44,340 KiB. [run_summary.json](run_summary.json) records the run.

[verify.py](verify.py) does not import this producer. It reconstructs all host
edges with the prior independent sparse-radical implementation, checks 13,569
new G552 edge inequalities, 13,729 lifted H560 inequalities, and 32,924 old
positive H560 inequalities. It checks the full domains and colour alphabets,
the disjoint-set proofs, both complete support enumerations, and the oracle
bytes. Eight malformed certificates are rejected; 5,461 small coverage cases
and 64 guarded-edge truth cases pass. Normal and optimized Python produced
byte-identical reports, coverage streams and CNFs. These checks take about
2.8 seconds each. See [expected.json](expected.json) and
[validation.json](validation.json).

From the repository root, using fresh output directories:

```sh
python3 -B hadwiger_nelson_heule560_cylinder508/verify.py --out /tmp/hn560-cylinder-check
diff -u hadwiger_nelson_heule560_cylinder508/expected.json /tmp/hn560-cylinder-check/result.json
python3 -O -B hadwiger_nelson_heule560_cylinder508/verify.py --out /tmp/hn560-cylinder-check-opt
cmp /tmp/hn560-cylinder-check/result.json /tmp/hn560-cylinder-check-opt/result.json
```

The verifier requires only Python's standard library (tested with 3.11.2) and
the repository's pinned input files. To regenerate positive covers, use
`python-sat==1.9.dev15`, Glucose 4.1 (`g4`), and:

```sh
python3 -B hadwiger_nelson_heule560_cylinder508/build.py --out /tmp/hn560-cylinder-search
```

Use `--resume` with the same output directory after interruption. Every accepted
positive witness and current target is checkpointed; the exact finite family is
rebuilt on resume. Resource-dependent growth can produce different valid covers;
the published five-cover certificate is the fixed object checked by `verify.py`.
Local logs, checkpoints, DIMACS files and coverage streams are regenerated and
are not committed. No external solver is needed to check the published result.

## Dependencies and remaining scope

The result builds on the exact H632 support, M492 boundary, H560 separator,
completed left-selector result, and the global positive covers. It strengthens
the [earlier order-503 bound](../hadwiger_nelson_heule560_criticality_bound/README.md)
and closes that global result's specified residual cylinder. The prior
[independent global review](../hadwiger_nelson_heule560_global_decision_review1/README.md)
is relevant background.

HN-3's concurrent
[quarter-localized rational-height theorem](../hadwiger_nelson_quarter_rational_heights/README.md)
was inspected and remains a separate geometric result, with no role in this
proof. The remaining H560 507–508 supports have not been classified here. No
new family, boundary-word prefix, or pinned-compression variant is started.
