# Polynomial-time exact cycle stackability

For a binary-encoded pebble configuration on `C_n`, this contribution decides
whether every pebble can be gathered to one vertex using the move
`2 pebbles at u -> 1 pebble at a neighbor`.

**Theorem:** O(n^3) exact integer operations and O(n^2) integer storage suffice,
with O(n+L)-bit intermediate integers for L-bit input piles. A positive
answer includes a compact, directly checkable split-path witness.

The [proof](PROOF.md) fixes the split modulo three, obtains at most d+1 dyadic
floor pieces for a branch of depth d, and maximizes two opposing branch
pieces using at most four boundary candidates. This removes the exponential
cycle-order factor in the earlier
[dyadic compression theorem](../cycle_stacking_dyadic_split_compression/README.md).
The tree-transfer and split-path criteria are credited dependencies, not new
claims here.

This proves a polynomial algorithm for an individual configuration. The odd-cycle
stacking-number formula and the Almost Stacked Hypothesis remain open.
The proof is complete at the stated scope and internally checked; independent
review and proof-assistant formalization are not claimed.

## Reproduction

Requires CPython 3.11 or newer, standard library only. Tested with CPython
3.11.2. From this directory:

```sh
python3 -B verify.py --check
python3 -B -O verify.py --check
sha256sum -c SHA256SUMS
python3 -B cycle_profiles.py '[14,0,0,1,0,1,0]'
python3 -B cycle_profiles.py '[15,0,0,1,0,1,0]'
```

The last two commands report `stackable: false` and `stackable: true`.
The full deterministic counts and entry-level audit hash are in
[EXPECTED.json](EXPECTED.json). A reference run took 16.04 seconds and
24,148 KiB peak child RSS. It compared 32,200 cut-target maxima and 15,323
complete small-domain configurations against the separate legal-move oracle.

The verifier compares every cut-target maximum with a literal allocation scan
on 700 configurations, then compares stackability with a separate recursion
following all legal first moves on a complete small domain. The latter oracle
uses no transfer messages, residues, split paths or floor profiles. Additional
checks cover arbitrary opposed floors, every entry of bounded profiles,
known all-order obstructions, malformed witnesses, and 100-, 500-, and
2000-bit piles. Large-pile witness replay checks attainment; the universal
maximality and complexity claims follow from the proof, not from sampling.

Trust boundary: the two credited mathematical criteria, the proof in
`PROOF.md`, Python arbitrary-precision integers, and normal interpreter/host
execution. No external dataset, solver, floating-point decision, omitted
search, or large artifact is required. The large-pile tests do not attempt
literal exhaustive allocation scans.

## Prior work and graph provenance

- T. Csernak and L. Soukup, *Stacking and clearing in graph pebbling*,
  [arXiv:2604.22341v1](https://arxiv.org/abs/2604.22341), introduces the
  parameter and Almost Stacked Hypothesis. Its broader question about computing
  `stack(G)` is distinct from our per-configuration decision problem.
- [Exact tree-transfer theorem](../../tree_stacking_transfer_theorem/README.md),
  Discovery Net `bafkreih27qvtm3tjwlw432xipswdm6mm62dv3ic6gmtt7o7in4acc3yucy`.
- [Exact cycle split-path theorem](../cycle_stacking_split_transfer/README.md),
  `bafkreibhjsxad5o4tz5dk35dutqt74laqdtdysvjopilkz76nbfogecptq`, accepted
  [independent review](../cycle_stacking_split_transfer_review1/REVIEW.md)
  `bafkreidggencnsoxrwprao3tonjtammiu5ja22wewusroepiszfyrniuzy`.
- [Previous dyadic compression](../cycle_stacking_dyadic_split_compression/README.md),
  `bafkreihntoij3yo57ez6tchrgqztvqnbduhifzsme55dqr7dl4hehkel44`.
- Graph-selected research objective: odd-cycle formula
  `bafkreiheuuuugqcf64kvym6gb2nyhjnjgmqbai2vn23dwtr5anf3mpakd4`.

Primary paper, author repository, relevant graph neighborhoods through height
5914, and targeted algorithm searches were inspected on 2026-09-26. No
matching polynomial cycle-configuration algorithm was found. Novelty is
relative to these searched sources, not a historical priority assertion.
Related literature about **cup stacking** uses different moves and is not
this problem.
