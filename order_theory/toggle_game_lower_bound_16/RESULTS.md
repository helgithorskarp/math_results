# Exact results and validation

## Complete production run

Publisher-authenticated input:

```text
789ecab657f46d926032ffa08a8c6b2a033cc8ea916ddbc513296196df68255d  unlabelled-15.cats.xz
```

The round-robin split had six files of 12,686,127 records and six files of
12,686,126 records.  The record total is therefore 152,233,518.  Every slice
passed, and exact aggregation gave:

```text
PASS order=15 total=152233518 winnable=152233518 max_states_before_goal=16383
workers=12 search_wall_seconds=345
```

This 345-second run used the exact packaged `catalog_search.cpp`.  A preceding
complete run of the inherited, semantically identical checker took 320 seconds
and returned the same twelve slice outputs and aggregate.

The first six one-line slice outputs each have SHA-256
`4ccdccb1fc25a8c445bacc224df3d5405a695cfc643e54f5e130f545102d5c84`;
the last six each have SHA-256
`57004f84b05e329fde3173a66b846d69c646c286f0e4deba4a6b318780d2a551`.
The repetition reflects the two exact slice sizes, not deduplication of input.

Environment: GCC 12.2.0, Linux 6.1.0-52-cloud-amd64, x86-64.  The state search
used no floating point, solver, randomness, or concurrency within a slice.

## Independent and defensive checks

- The production C++ checker and the set/frozenset Python checker both passed
  all 5,994 order-10 lattices.
- An AddressSanitizer plus UndefinedBehaviorSanitizer build passed 18,000 fixed
  order-15 samples with the production result
  `max_states_before_goal=16383` and no diagnostic.
- The independent Python implementation passed the same 18,000 order-15
  entries, selected as the first 6,000, a centered block of 6,000, and the
  last 6,000.  It reconstructs an explicit winning sequence for each sampled
  lattice before accepting it.
- All five source-level unit tests pass.

The canonical sample SHA-256 is
`1841dfc6506adffcd5d386ac3612562deb7b4723c4db7fb5061f1b629930511c`,
recorded in `independent_sample.sh` and the source manifest after reproducible
extraction from the authenticated archive.

The institutional link for the independent Reading/Heitzig--Reinhold order-15
catalogue redirected to an organization login on 2026-09-19.  Accordingly,
this pass did not claim a second full-catalogue reproduction at order 15.
