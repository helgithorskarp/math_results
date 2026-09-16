# Provenance and reproduction

## Reviewed inputs

The review targets
`hadwiger_nelson_h630_sqrt2_block_replacement_stop` at mathematical commit
`53b90e407c24fdd029346f8c9f2de72a51b0d062`. It pins the mathematical target
files, all three original H632 coordinate inputs, and the result and theorem
statement of the prior H630 seed review. Later Discovery receipt additions are
outside the mathematical input.

The prior review accepted the exact 630-point, 3,098-edge, five-chromatic H630
seed. This review independently reconstructs its complete geometry and checks
its positive five-word, but does not redo the multi-megabyte four-colour UNSAT
proof because the final 508-point theorem uses its own positive four-word and
Moser obstruction.

## Reviewer-owned implementation

`independent_check.py` imports no executable from the target, producer or
prior review. The source is reconstructed from the archived H510 coordinates
and fresh-centre rows. The exact arithmetic is a recursive quadratic-field
tower, distinct from both target implementations. The Moser census,
three-colouring formula and Tarjan traversals are reviewer additions.

Only the Python standard library is required. No SAT solver is invoked, and
no large generated proof, cache, log or private dataset is published.

## Commands

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B hadwiger_nelson_h630_sqrt2_block_replacement_stop_review1/independent_check.py --check-expected
PYTHONDONTWRITEBYTECODE=1 python3 -O -B hadwiger_nelson_h630_sqrt2_block_replacement_stop_review1/independent_check.py --check-expected
PYTHONDONTWRITEBYTECODE=1 python3 -B hadwiger_nelson_h630_sqrt2_block_replacement_stop_review1/controls.py
cd hadwiger_nelson_h630_sqrt2_block_replacement_stop_review1 && sha256sum -c SHA256SUMS
```

Expected verdicts:

```text
ACCEPT_AND_STRENGTHEN_H630_508_BLOCK_REPLACEMENT_STOP
ALL INDEPENDENT REVIEW CONTROLS PASS
```

No network access is required after cloning the repository.

