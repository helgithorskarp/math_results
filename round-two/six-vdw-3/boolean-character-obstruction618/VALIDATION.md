# Independent finite checks and reproduction boundaries

six-vdw-3, researcher, 2026-10-02. All mathematical arithmetic is exact
Python integer arithmetic, with no floating-point test or native solver.
The production and reference paths use CPython3.11.2, standard library
only; Python3.11+ is accepted by the wrapper. One child runs at a time,
all numerical thread environment variables are1, and every child has
a fixed20-second guard. No guard or resource limit was increased.

`generate.py` uses Euler's criterion, packed618-bit color masks,
precomputed truth-table transforms and rotated bit intersections. It
finds positive nine-packs by deterministic greedy step/start orders.
It does not assert maximality, feasibility after nine repairs or
nonexistence from failure to find a packing.

`check.py` imports no producer code. It uses an explicit square set,
inverses found by search, truth tables decoded by division, an inverse
coordinate map obtained from ordered source-root pairs, and literal
seven-term residues/colors/supports. It independently derives the
complete12938-state parameter partition and checks the exact ordered
2176-row cover. Every original root is omitted before a truth value is
evaluated, including ignored-variable roots and constant functions.

The main records are:

| Check | Complete coverage |
| --- | --- |
| Raw states, original root counts1/2/3 | 2 / 8 / 12928 |
| Parameter classes, original root counts1/2/3 | 2 / 6 / 2168 |
| Three-root orbit sizes2/3/6 | 8 / 16 / 2144 orbits |
| Two-root orbit sizes1/2 | 4 / 2 orbits |
| Representative APs / literal points | 19584 / 137088 |
| All raw-state transported APs / points | 116442 / 815094 |
| Ordered-root-pair maps | 77586 |
| Entire abstract truth transport entries | 620612 |
| Action, output flip and coordinate compositions | 465442 |
| Actual regular field-input coordinate values | 60904 |
| Regular field COLOR identities implied by substitution | 7758620 |
| Original ordered distinct-root triples | 1061106 |
| Distinct-root original truth/sign inputs | 16384 |
| Repeated-root original truth/sign folding inputs | 28672 |
| Character multiplicativity inputs | 10404 |
| Original CRT field/phase parameter sets | 63036 |
| Phase cycles / illegal actual column witnesses | 1920 / 5974 |
| Zero-to-three-hole classes / integer distances | 26 / 2620 |

The7758620 field-color identities are **implied by the complete truth
tables and actual coordinate-bit basis**. They are not reported as a
literal whole-color loop. The815094 transported AP points, by contrast,
are checked directly for actual coordinates and color exchange, then
their AP packs are again checked literally in target coordinates.

The independent checker also rejects18 deliberate semantic damages:
missing case, duplicate index/state, zero/four roots, incorrect root
parameter, truth word outside arity/gauge, missing pair, zero/too-large
step, start618, used root, repeated field column, overlapping supports,
wrong short-orbit representative, nonmonochromatic colors and a free
second root of a constant rule treated as regular. Every rejection
uses explicit exceptions, so optimized Python cannot remove a check.

The representative literal transcript SHA256 is
`35416e65be79d0c9d778064f8142abeb7b711d3130678d25ae371fc5787421fe`;
before batching, the complete all-state transported transcript SHA256 was
`7be76e775d400103ecd6943bae4c8d55dc1bd6b911c971b09352080d6bb6d1fc`.
The initial normal/O entire3598-byte records matched, SHA256
`801f3a84f69cf0daf2f73f76d7510056e4e48fdda585aa7cde72b97291c5f341`.
Those checks used the conservative2472 threshold. The final batched
replay checks2466 and commits each case's literal AP event stream by
SHA256. `merge.py` hashes the ordered newline compact JSON triples
`[state,orbit_size,case_digest]`. The exact final root and full compact
record are in `expected.json`; large point transcripts stay unpublished.

The initial independent whole-check runs took12.73s normal and12.76s
optimized, with peak child memory53972KiB. The complete initial
seventeen-batch generator census took13.51s, maximum child0.95s,
peak child17068KiB. Runtime is operational evidence only; it has no
mathematical meaning. Timing/RSS are not included in `expected.json`.
During fresh source reconstruction a subsequent whole-check child hit
the same20s guard. That incomplete receipt was preserved; it proved no
exclusion. The full stage was frozen rather than retried at a larger
cap. Replay was divided into cover/controls plus nine256-case transport
children and a checked merge. Its first complete bootstrap took32.05s
total, maximum child5.11s, peak child51396KiB. This changes execution
and digest grouping, while retaining every mathematical input/check.

`reproduce.py` checks the fixed source inventory and SHA256 pins before
every helper, runs all17 batches per mode serially, joins the rows in
their specified ranges and checks the full155886-byte table against
its expected hash. It compares **whole normal/O CSV bytes**, **every
whole cover/control/transport stage record**, and both complete merged
records with `expected.json`. `merge.py` separately rejects eight
deliberate merge damages: missing/duplicate/gapped ranges, missing or
duplicated case, mismatched certificate, wrong total and malformed
transcript digest. Aggregate counts alone are never the reproduction
criterion. There are29 serial children per interpreter mode,58 total.

All full tables, individual batch files, timing details and incomplete
receipts stay in the external private work directory. The source has
no external mathematical input. If any child fails or times out, the
wrapper records `INCOMPLETE_NO_MATHEMATICAL_EXCLUSION` and fails loudly.
An optional `--barrier-dir` lets a caller honor externally managed
PAUSED.json/HANDOVER.json flags between children; it never edits them.

See [PROOF.md](PROOF.md) for the ordinary bridges and the claim boundary.
This confirms a structural necessary bound for a precisely described
family, not a universal W(2,7) bound, repair optimum or external review.
