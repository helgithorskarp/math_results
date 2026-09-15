# Provenance and trust boundaries

## Fixed sources

The reviewed mathematical source is the immutable commit
[`eb1263c7f9ac2b80120cd9521a6f99d2da435a7b`](https://github.com/helgithorskarp/math_results/tree/eb1263c7f9ac2b80120cd9521a6f99d2da435a7b/hadwiger_nelson_opposed241_conditional_core).
Its later receipt-only commit does not alter the mathematical package.

The independent checker pins these inputs by SHA-256:

- target `certificate.json`:
  `37e1397276f931ee1b9b63f4ca5c343a2ac129fa3b1c6d526e4c151031a750e4`;
- B214 `points214.tsv`:
  `97c9b3a964ed19874ae3fe932eb8c085fd637f618d2481fffaebbd1fbae55c2f`;
- Parts receiver-coordinate `points.tsv`:
  `f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50`.

The 343-point opposed-B214 parent was published at
[`42fd5e441e190a4022743479458aabf2ca55a85b`](https://github.com/helgithorskarp/math_results/tree/42fd5e441e190a4022743479458aabf2ca55a85b/hadwiger_nelson_golomb_opposed_b214_stop)
and independently accepted at
[`5ed67074e4008c0549f8c2e35dc1bf2e86485891`](https://github.com/helgithorskarp/math_results/tree/5ed67074e4008c0549f8c2e35dc1bf2e86485891/hadwiger_nelson_golomb_opposed_b214_review1).
This review nevertheless reconstructs the parent geometry before selecting
the new core.

The native-role stop imports the whole-field theorem at
[`825d763c59e6e299f2c7df4b8c93b13dece6d511`](https://github.com/helgithorskarp/math_results/tree/825d763c59e6e299f2c7df4b8c93b13dece6d511/hadwiger_nelson_nonmono_field_obstruction),
independently accepted at
[`0d54b52f753674be64f78b6aa57754d873464347`](https://github.com/helgithorskarp/math_results/tree/0d54b52f753674be64f78b6aa57754d873464347/hadwiger_nelson_nonmono_field_obstruction_review3).

## What was independently established

The review does not import the source verifier or coloring algorithm. It
independently parses the fixtures, carries out arbitrary-precision radical
arithmetic, constructs all physical unit edges, exhausts the conditional
coloring search with a different state representation, validates all positive
witnesses, and derives the contact and connectivity strengthenings.

The target's optional, unpublished RUP trace is not used. The matching CNF
hash checks the stated Boolean serialization but the proof of nonextension in
this package is the direct DSATUR enumeration.

## Trust and limitations

Finite exact checks trust CPython 3.11+ integer arithmetic, file parsing, the
review source, and the three pinned transcriptions. No third-party solver or
floating-point comparison is used. The DSATUR completeness and Tarjan
coverage arguments are ordinary unformalized mathematics; neither has been
checked in a proof assistant. Small exhaustive controls reduce implementation
risk but do not eliminate this trust boundary.

The identification of the coordinate fixtures with their historical graph
sources is imported from the cited provenance. The field-theorem application
is imported rather than reproved. The review did not enumerate the core's
full 95-input relation, search globally for a smaller core, test all 991 edges
for conditional criticality, or perform any receiver computation.

The source Discovery contribution was accepted for broadcast with CheckTx
code 0 but remained absent from the stale committed index when this review
began (local index height 4363, RPC height 4364). That status is pending, not
committed, and is not a premise of the review.
