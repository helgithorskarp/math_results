# Validation — six-vdw-2, researcher

2026-10-01. Same-author independent model implementations and strict
solver-independent exact proof replay; no new independent peer verdict
or formalization is claimed.

All44 two-exception models have exact refutations: K=2 at every
normalized distance1..22 and K=42 at every normalized distance1..22.
The complete cases cover33284415996035072 labeled quotient words,
not all2^88 H7 patterns. The two ordinary QR orientations are retained
as phase-zero positive controls. The whole H7 family remains open.

The initial complete serial proposal/replay runs took62.568s (opposed)
and42.085s (agreed). Independent literal signed-coset auditors traverse
all380072 actual field pairs, retain375760 APs and remove4312 through
zero. Only identical signed supports are aggregated into26488 entries.
Every complete clause set is compared, with the normalization unit.
Exhaustive small words check1404 rotations/color normalizations per
kind,2808 in total, supplementing the universal22-orbit cover proof.

Fresh release-source regeneration and optimized model audits all passed:

| Kind | Fresh complete proof run | Optimized model audit | Peak child KiB |
| --- | ---: | ---: | ---: |
| Two opposed pairs, K=2 |45.027s |15.303s |69328 |
| Two agreed pairs, K=42 |42.261s |13.969s |68728 |

Overall fresh+optimized sequence117.506s. All reference CNF and RUP
proof bytes matched. Every one of the44 RUP proofs was checked in
normal and optimized Python,101701 additions/1018620 propagation
hints per full replay. The byte-identical strict checker already has
its256-small-CNF and malformed-proof controls in the cited original
source; native statuses are not proof premises.

The new `--resume` branch was tested on the complete K=2 corpus:
30.649s, peak child69684KiB. It reused only hash-validated complete
proposal/conversion checkpoints and repeated all22 definition audits,
normalization/QR controls and both exact proof modes. Final success
and reference proof-byte equality were verified from its actual output.
The source-integrity control in controls.py rejected a changed pinned
helper in normal and optimized Python before any solver call.

Python3.11.2, GCC12.2.0, python-sat1.8.dev24, six1.17.0 and
CaDiCaL195. All jobs serial/native threads one, under standing1CPU/
2GiB scope. Proposal budget50000 conflicts/external30s; conversion
internal25s/external30s. Largest initial completed conflict count2383.
No timeout/UNKNOWN was used for any of the44 claimed refutations,
and no resource limit or budget was increased.

Separate exploratory joint88/132-variable covers remain UNKNOWN;
those outcomes do not strengthen this negative result or classify H7.
The new combined phase band3<=K<=41 imports the preceding K1/43/44
cuts and the earlier order>=11 classification for nonQR K0. Those
premises are identified explicitly in README/PROOF and source pins.
No [1,3704] coloring or interval W bound is established.

Current primary check2026-10-01: Monroe Table1 still gives the two-color/
seven-term >3703 seed; Table2 uses prime617 and the opposite argument
convention. Narrow primary-domain queries for617/antipodal/order-seven
returned no matching external theorem. This is bounded inspection,
without historical-priority or universal-current-status claims.
