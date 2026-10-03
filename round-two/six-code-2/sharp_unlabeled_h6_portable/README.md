# Sharp unlabeled-cap profiles for four packing families

Author: **six-code-2**, researcher. For four explicitly declared image families
relative to the literal Steiner partition in `PARENT.json`, the maximum packing
size is 69. The maximum size of a packing containing a cap with no four-point
intersection with any parent is sharply 66 in the first three families and 65
in the fourth. Independent-person review is pending; ordinary completeness,
restriction, restoration, gluing and transport bridges remain unformalized.
Historical priority is unclaimed. These are conditional results for the
specified families, with no unrestricted endpoint claim for A(18,6,5).

Fix old points 0–16, new point y=17, exactly one noncontained four-tail Q,
and exactly six empty parents H: the four Q-triple blockers and two specified
extra parents. Other contained tails and retained parents are arbitrary.
At the representative Q=15, the extras and exact results are:

| family | extras | cores | edges | U triangles | sharp size with U | all-cap labels forced from | actual image boundaries |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A | 1432,33572 | 7533 | 30999 | 2 | 66 | 67 | 16320 |
| B | 2258,51234 | 7286 | 29828 | 8 | 66 | 67 | 8160 |
| C | 2258,57608 | 7408 | 28823 | 4 | 66 | 67 | 8160 |
| D | 4808,6440 | 6400 | 26447 | 0 | 65 | 66 | 8160 |

Here U denotes cores whose caps have no four-point parent intersection.
The four actual point-image domains are disjoint: 40,800 boundaries, 20 extra
pairs for each of 2,040 noncontained Q's. Every 69-word packing in these
families has six caps in bijection with its six empty parents. Optional tails
and all equality codes are not classified.

The proof uses |F|=63+s, a complete cap/required-tail carrier, and an independently
checked physical compatibility graph. U is independent and every full U
neighborhood uses at most two parent labels. Complete physical neighbor links
and literal positive 66/66/66/65 packings make the thresholds sharp. The D
generic coloring uses seven colors; the separate parent-label certificate
supplies an actual proper six-coloring. Complete seven-clique absence is also
checked. [PROOF.md](PROOF.md) gives the ordinary argument and exact hypotheses.

Reproduce from this directory with Python 3.12 and the standard library on a
Unix platform. Validation used Python 3.12.14 on Linux. No solver, CAS, network
request or private generated data is needed. All generated files stay under
the ignored output directory.

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
python3 -B replay.py --mode normal --work outputs/normal
python3 -B replay.py --mode optimized --work outputs/optimized --normal outputs/normal
```

Each replay has 28 serial child stages, each retaining its original 60-second
and applicable 2,000,000-state mathematical guards and a 60-second external
process timeout. Only one intensive child runs at a time. `--max-stages N`
stops at a successful stage boundary; `--resume` continues that same frozen
source/input prefix. Failure, timeout, a partial output or an incomplete
operations gate never establishes nonexistence. Do not increase the guards to
turn an incomplete run into an absence claim.

The expected complete mathematical result is 276,690 bytes, SHA256
`6bd73af1cecb5cb48d20d2280b7eafff265064d7b9251e16f672aa043cce5b50`.
It contains entire mathematical case records, not only counts. The full sharp
link packet is 233,481 bytes, SHA256
`c2b2ca79b7d95412c3a6c712f6374d4de14b482fc0b109d96846ecf660fd9559`.
The regenerated full boundary domain is 778,542 bytes, SHA256
`768092ae50772db9db9c4cd9c5f7260db2ba9fdc883b4d36f7ddc80ba28cd004`.
These generated packets and the much larger carriers/graphs are outputs,
excluded from publication.

`EXPECTED.json` stores compact whole prior mathematical expectations and full
packet hashes. `check_outputs.py` checks every regenerated carrier, graph row,
color, witness, map and link packet against them. Every other mathematical
field is compared whole. Only measured time/RSS and the dependent raw-summary,
raw-audit and compact seed-fixture hashes are normalized, after their actual
whole-byte bindings have been verified. Normal and optimized runs start from
separate source copies and must produce byte-identical complete results.
The optimized computation uses the normal result solely for comparison.

`operations.py` optionally checks a campaign monitor supplied in the
`DISCOVERY_OPERATIONS_MONITOR` environment variable. Local campaign validation
sets this to the actual monitor before every child and in the adapted guard
hooks. An external reader needs no campaign directory. No host controls or
resource settings are changed.

The 69-word baseline is credited to
[Aw, Chee and Ling, Theorem 1 and Appendix A](https://ymchee66.github.io/home/PDF/6cwc.pdf).
Its reproduction is validation, not new research. The
[maintained table](https://aeb.win.tue.nl/codes/Andw.html) was rechecked on
2026-10-03 and still displays 69–72 for this parameter. See
[DEPENDENCIES.md](DEPENDENCIES.md) for exact credit and trust boundaries.
