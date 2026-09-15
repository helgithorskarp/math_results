# Provenance and independence

## Reviewed target

- Branch path:
  <https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_frozen_bowtie_palette_coupler>
- Exact revision: `18b6c94617ca9807f7f9f3da2ba42e10e6780df6`.
- Target certificate SHA-256:
  `aca337a68dd2ca33fafd393486d6ed8368bd26112c8e8bd8ddcfaf36961b360d`.
- Target expected-output SHA-256:
  `894b9616480848e49d2614c563bc00f039295edfd43b68a1d835f07c2be4ee74`.
- Target checker SHA-256:
  `2472e8d485ce55ea300aa94c5183fe6de349290342e8439c33c95aff6bff9029`.
- Target producer SHA-256:
  `2160b95cb8b9dce5216fa38804e19a56298dc47e122a350f46ec580a7aafaabf`.

The target normal and optimized checker runs, corruption controls,
independent producer comparison, and SHA-256 manifest all passed before this
review package was written.

## Coordinate input

The public `source29.tsv` has SHA-256
`3631210e31697804a86437cc7b6f734870097e22de50e5c4721ecea6ab633924`.
The review copy is byte-identical to both the target file and
`hadwiger_nelson_frozen_centre_transfer/points.tsv` at revision
`ef05942eeebba29628dc02f37a5792ac7d4122b8`.

The review rechecks every source distance and the complete terminal relation
used here. It does not reconstruct the earlier 43-point Polymath source from
cosets; the 29 coordinate rows and their byte identity are an explicit trust
boundary.

## Algorithmic independence

The target checker uses generic gcd-based radical products and singleton
domain recursion. Its separate producer uses radical bitmasks, direct
restricted-growth terminal enumeration, and DSATUR.

The reviewer instead uses closed-form quartic squaring, brute named-word
enumeration followed by canonicalization, and a fixed-order frontier dynamic
program. Complete point, edge, distance, and allowed-pattern hashes agree, not
merely aggregate counts. Small exhaustive controls compare the frontier DP
against a definition-level brute-force oracle independently of the target.

No private source, solver log, Discovery ledger, credential, or unpublished
large artifact is required by this package.
