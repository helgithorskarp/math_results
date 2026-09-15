# A 241-point core for a complete Golomb-colouring obstruction

This exact **241-point, 991-edge strict plane unit-distance graph** forbids
the complete Golomb four-colouring `0121212203`, while allowing
`0121212023`. It is exactly four-chromatic, not a five-chromatic candidate.

The graph is a subset of the reviewed 343-point opposed-B214 source. One
fixed deletion order removed 102 points while preserving the first word's
nonextension. All ten Golomb vertices are retained. Each of the remaining
231 private vertices has a checked deletion witness extending the forbidden
word. Thus **every proper induced subset of this fixed core containing the
ten Golomb vertices admits that word**. This is relative vertex minimality,
not a minimum-order theorem over the 343-point parent or other geometries.

The retained left and right pieces have 121 and 176 points and share 56.
Their union has 47 additional physical contacts between private points.
Deleting those 47 constraints admits the forbidden word even with all shared
vertices identified. Reinstating the complete physical graph forbids it.
The core is connected, has minimum degree four and no articulation or bridge.
Consequently the full-input loss is not a pendant or one-point attachment
phenomenon. It also gives strict projection loss on the full 121-point left
input: restrict the contact-deleted word and the surviving whole word to it.

The native Golomb roles in Parts373 are
`[0,153,150,169,166,161,158,53,65,59]`. Exact coordinate accounting finds
137 overlaps, so adding the core would cost 104 points and give 477 total.
**That native role is closed by the reviewed whole-field four-colouring**:
both supports lie in `E=Q(i*sqrt(3),i*sqrt(11))`. This is a budget calculation
and a known-theorem preflight, not a new receiver search or candidate. No
receiver pattern table was queried. There is no finite finishing construction
supplied here; the core is banked without another deletion order or docking.

## Reproduce

From the repository root, with Python 3.11+ and no third-party dependency:

```sh
python3 -B hadwiger_nelson_opposed241_conditional_core/verify.py --check-expected
python3 -O -B hadwiger_nelson_opposed241_conditional_core/verify.py --check-expected
python3 -B hadwiger_nelson_opposed241_conditional_core/controls.py
```

The checker reconstructs every one of the core's 28,920 pairs exactly and
checks all positive words. An exhaustive domain search proves the conditional
nonextension in 6,259 nodes, with 3,130 conflicting leaves. It does not trust
a SAT verdict or an unavailable proof file. A separately generated SAT/RUP
certificate was also checked locally; it is optional corroboration described
in [PROVENANCE.md](PROVENANCE.md), not needed for public replay.

The certificate includes the vertex labels and 231 short deletion words.
The full projected relation of this smaller core was **not** enumerated.
The upstream 95-to-66 relation is not asserted for this subset. See
[PROOF.md](PROOF.md) for the exact quantifiers and encoding.

[Parts's 509-point/2,442-edge construction](https://arxiv.org/abs/2010.12665)
remains the supported unrestricted record; [Haugland v4](https://arxiv.org/html/2608.04542v4)
also calls 509 current. This conditional four-chromatic core does not improve it.
