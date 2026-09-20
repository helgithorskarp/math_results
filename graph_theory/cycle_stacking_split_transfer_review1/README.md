# Review evidence for the cycle split-path theorem

This directory contains an independent review of
[the split-path source](../cycle_stacking_split_transfer).

Verdict: **accept, with high confidence in the stated scope**.  The complete
proof-premise audit, adversarial examples, dependency boundary, and limitations
are in [REVIEW.md](REVIEW.md).

The verifier uses definition-level legal-move recursion and exhaustively
reconstructs every branch of the proof's inverse-move induction.  It imports no
target code and does not use signed transfer messages.

## Reproduce

Python 3.11+ and the standard library suffice.  From this directory run:

~~~sh
python3 verify.py --check
sha256sum -c SHA256SUMS
~~~

The first command must end with a PASS status.  It checks 3,168 complete small
configuration cases, 35,805 splits, 28,262 inverse-move proof transformations,
7,814 empty-leaf implications, and all four induction branches.

The finite computation corroborates rather than replaces the universal human
proof in REVIEW.md.
