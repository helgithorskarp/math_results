# Weighted one-hole search for a classical Schur-six colouring of 537

The sixth classical Schur number is the largest endpoint `N` for which
`[1,N]` admits six colours with no monochromatic `x+y=z`, including `x=y`.
[Fredricksen and Sweet](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32)
gave `S(6)>=536`. **No valid colouring of `[1,537]` or upper-bound
certificate is claimed here.** This is a complete-target search checkpoint.

## A distant one-hole word

The independently reviewed [plain full-target CNF](../schur_s6_unrestricted_fullword_search/README.md)
has 3,222 Boolean variables and 441,145 clauses. `weighted_encode.py` adds
one *duplicate* of each of its 537 at-least-one-colour clauses, giving
441,682 clauses and SHA-256
`59065da7bf54c6f9468a4b578bc0214830d5d5c6af8de44e80dbc004594ddc10`.
Duplicates leave SAT models unchanged but double the local-search cost of
leaving an integer without a colour.

YalSAT source commit `a0fd39f072f2d4693dd5a1977de3c3d3f69c8850`,
`-T 2`, seed `20261304`, returned a Boolean witness in 20.54 seconds.
`extract.py` independently evaluates all 441,682 weighted clauses: its only
two failures are the duplicate at-least-one clauses for position 35. Its
[partial35.txt](partial35.txt) colours all other 536 integers, with no
monochromatic Schur triple among them. It is **not** a 537-colouring. All
six direct fillings of the hole were tested; the fewest defects are 31,
by colour 1, saved as [completed31.txt](completed31.txt). A valid extension
of this fixed partial word must recolour other positions.

## Complete-word continuation

The previously published unrestricted [`fullscore.cpp`](../schur_s6_unrestricted_fullword_search/fullscore.cpp)
allows any of the 537 positions to change to any of six colours. Its scored
equations include all 72,092 unordered Schur triples and 268 doublings.
Two deterministic stages from this one-hole seed reached another distant
[two-defect complete word](best2.txt):

| Input | Seed | Steps | Kick | Global noise | Local noise | Tabu | Output |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `completed31.txt` | `20261315` | 5,000,000 | 10 | 1% | 10% | 5 | [best3.txt](best3.txt) |
| `best3.txt` | `20261316` | 10,000,000 | 10 | 1% | 10% | 5 | [best2.txt](best2.txt) |

The three-defect intermediate has bad triples `1+1=2`, `1+2=3`, and
`1+55=56`. The final word has exactly `1+1=2` and `1+2=3`. Its first
defect is a doubling, so it gives **no new Schur lower bound**. The second
stage found it at step 2,026,336. After the best of all 720 global colour
permutations, it differs at 398 positions from the previous [two-defect
word](../schur_s6_distant_two_defect_search/best2.txt), and at
`422,430,416,426,432` positions from the older `W`, `190`, `359`, `best3`,
and `347` words in [`sources.json`](../schur_s6_multi_alignment_recombination/sources.json).
These are distances between saved words, not bounds on possible solutions.

## Reproduce and audit

From this directory, CPython 3.11 or later suffices for exact checks:

```sh
sha256sum -c SHA256SUMS
python3 -B audit.py > /tmp/schur-six-weighted-audit.json
diff -u expected.json /tmp/schur-six-weighted-audit.json
```

To regenerate the YalSAT partial word with the source commit above:

```sh
python3 -B weighted_encode.py /tmp/schur-six-weighted537.cnf
/path/to/yalsat -T 2 /tmp/schur-six-weighted537.cnf 20261304 \
  > /tmp/schur-six-weighted537.log
python3 -B extract.py /tmp/schur-six-weighted537.log \
  /tmp/schur-six-weighted537.cnf /tmp/schur-six-onehole.txt
cmp partial35.txt /tmp/schur-six-onehole.txt
```

With GCC 12.2.0 or a compatible C++20 compiler, `replay.py` recompiles the
published whole-word search and reproduces both full 537-digit outputs:

```sh
python3 -B replay.py
```

The mathematical evidence for the exact defect counts is the direct
`audit.py` enumeration of every `x<=y`, `x+y=z<=537`, not the YalSAT or
local-search scores.
