# Validation transcript

Review environment: CPython 3.11.2 on 2026-09-13 UTC.

## Target package

- deterministic producer: PASS;
- regenerated certificate: 4,962 bytes, byte-identical to the committed file;
- certificate SHA-256:
  `f37a9fa67101a1aded49098a720aeb972463d46d9849e4e1d924dfc414f7a2ae`;
- exact verifier in normal mode: PASS;
- exact verifier with assertions disabled: PASS and byte-identical output;
- eight named semantic corruptions: all rejected in both modes;
- target `SHA256SUMS`: PASS when invoked from its package directory.

## Clean-room checker

- exact threshold/order checks: 5;
- exact symbolic identities: 4;
- exact sharp-boundary checks: 6;
- exact interior-fixture squared distances: 3;
- exact cross-triple checks: 3;
- increasing partial injections enumerated through order 7: 4,706;
- loop-free partial injections tested for the forest property: 1,637;
- admissible six-cycle active precolourings tested: 25;
- palette-set checks: 3;
- normal and assertion-disabled outputs: byte-identical;
- status: PASS.

The enumeration is a finite regression check for the order lemma, not the
proof of its arbitrary-real version.  The written audit in `README.md`
supplies that argument and records the remaining trust boundary.
