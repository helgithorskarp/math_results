# Validation transcript

Environment: CPython 3.11.2 and g++ 12.2.0 on 2026-09-13 UTC.

## Target replay

- all target source and certificate hashes: PASS;
- release build with `-O3 -Wall -Wextra -Wpedantic -Wconversion`: PASS;
- full release verifier versus `expected.json`: byte-identical;
- full assertion-disabled verifier with undefined-behaviour sanitizer: PASS;
- undefined-behaviour reports: zero;
- three-factor explicit cases: 3,504;
- two-factor contact quadratics: 5,064;
- exact physical unordered pairs: 433,052,116;
- target certificate bytes: 204,793;
- target certificate SHA-256:
  `2795687647a8f8d2b01d6d7c844d3d0d06afd9b3000f5a24341d03b5b3c26765`;
- target semantic and range controls: PASS in normal release and optimized
  sanitized modes.

## Clean-room audit

- source graph: 7 vertices, 11 edges, no three-colouring and a
  four-colouring;
- nonzero source differences: 34;
- source-difference norms: 7;
- in-field three-factor phase pairs: 1,716;
- outside-field three-factor phase pairs: 6,528;
- locally colourable outside-field pairs: 3,024;
- explicit three-factor collision descents: 3,504;
- three-factor root-inventory SHA-256:
  `1018a08df44c3829722fe38c97b27eb7e8840a2c077e62c525cbcd7afb5dbb7a`;
- two-factor collision phases / conjugation representatives: 30 / 16;
- retained two-factor contact quadratics: 5,064;
- two-factor inventory SHA-256:
  `a0eca8921a9c0f2278f840283593bb1fe054c990db259f9ca3a9a8fd1d4577f0`;
- two-factor event-edge stream SHA-256:
  `49ac13469e90d93a56403b353a804915eaa6d65055d3f17177cc3a766030b198`;
- used words checked on all 1,617 Cartesian product edges: 483;
- every two-factor event edge and word descent: PASS;
- normal and assertion-disabled output: byte-identical;
- status: PASS.

The independently reviewed base-field implementation and all unit-trace
algebra, geometry and alternate-representation suites also reproduced their
pinned expected outputs and manifests.
