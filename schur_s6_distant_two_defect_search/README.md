# A distant two-defect complete word for Schur six at 537

The classical sixth Schur number is the largest endpoint `N` for which
`[1,N]` has a six-colouring with no monochromatic `x+y=z`, **including
`x=y`**. [Fredricksen and Sweet](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32)
published `S(6)>=536`. A complete valid 537-word would improve it.
**No such colouring or unrestricted upper-bound certificate is claimed here.**

This checkpoint continues the [unrestricted complete-word search](../schur_s6_unrestricted_fullword_search/README.md)
in a distant search region. It contains ten independently audited 535-coloured
partial words and a deterministic two-stage whole-word continuation that
reaches a [new two-defect word](best2.txt). Its only bad triples are
`3+3=6` and `3+6=9`. The first is a doubling, so the word is **not** a
Schur colouring.

## Whole-word search path

YalSAT source commit `a0fd39f072f2d4693dd5a1977de3c3d3f69c8850`,
on the [plain complete 537 CNF](../schur_s6_unrestricted_fullword_search/README.md),
seed `20261005`, `-T 2`, returned its Boolean witness in 20.86 seconds.
`extract.py` checks all 3,222 variable signs and directly checks every
classical Schur triple among coloured positions. The [partial word](partials/20261005.partial)
has holes at 10 and 20, with no bad coloured triple. The best of its 36
direct completions has 29 defects; [completed29.txt](completed29.txt) assigns
colour 1 at both holes. The complete-word search then used the previously
published [`fullscore.cpp`](../schur_s6_unrestricted_fullword_search/fullscore.cpp),
which allows every position to change to any of six colours and scores all
72,092 unordered Schur equations.

| Source | Seed | Steps | Kick | Global noise | Local noise | Tabu | Best |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `completed29.txt` | `20261102` | 5,000,000 | 20 | 3% | 15% | 7 | [three defects](best3.txt) |
| `best3.txt` | `20261203` | 10,000,000 | 10 | 1% | 10% | 5 | [two defects](best2.txt) |

The intermediate three-defect word has bad triples `3+3=6`, `3+6=9`, and
`12+15=27`. The second run found the two-defect word at step 4,590,561.
`replay.py` rebuilds the search binary, reruns both stages, compares the full
537-digit outputs byte for byte, and rechecks their triples. This is a
heuristic construction path, not a proof that fewer than two defects are
impossible.

Twelve independent `-T 2` YalSAT seeds `20261001` through `20261012` were
each allowed 45 wall seconds, with four processes running concurrently.
Ten returned saved two-hole words; `20261007` and `20261012` timed out without
a witness. The exact checker enumerates all Schur triples in every saved
partial word and all 36 direct completions of each:

| Seed | Holes | Fewest defects on direct completion |
| --- | --- | ---: |
| `20261001` | 202, 404 | 30 |
| `20261002` | 7, 14 | 17 |
| `20261003` | 2, 4 | 13 |
| `20261004` | 13, 26 | 18 |
| `20261005` | 10, 20 | 29 |
| `20261006` | 3, 6 | 25 |
| `20261008` | 2, 4 | 12 |
| `20261009` | 5, 10 | 9 |
| `20261010` | 13, 26 | 21 |
| `20261011` | 2, 4 | 14 |

With 5-million-step continuations for each saved partial word except the
`20261009` 10-million-step run, only `20261005` reached three defects; the
others ended at four or five. This is a finite search observation only.
Three further 20-million-step runs from `best2.txt` (seeds `20261204` to
`20261206`, respectively parameters `(kick,global,local,tabu)` of
`(10,1,10,5)`, `(20,3,15,7)`, `(40,5,20,10)`) stayed at two defects.
A CaDiCaL 1.9.5 complete-CNF phase-hint probe from `best2.txt`, with a
500,000-conflict budget, returned `UNKNOWN` after 75.52 seconds. These
observations give no exclusion or numerical bound.

The new `best2.txt` is not a colour permutation of any of the five earlier
near words in [`sources.json`](../schur_s6_multi_alignment_recombination/sources.json).
The minimum Hamming disagreements after all 720 global colour permutations
are `414,428,425,421,427` against `W`, `190`, `359`, `best3`, and `347`.
The direct checker computes these distances as well as the bad triples.

## Check and replay

From this directory, CPython 3.11 or later and the standard library suffice
for the exact checks:

```sh
sha256sum -c SHA256SUMS
python3 -B audit.py > /tmp/schur-six-two-defect-audit.json
diff -u expected.json /tmp/schur-six-two-defect-audit.json
```

To regenerate the seed partial word, first generate the full plain CNF using
the sibling `encode.py` and build YalSAT from the commit above:

```sh
python3 -B ../schur_s6_unrestricted_fullword_search/encode.py \
  --mode plain /tmp/schur-six-537-plain.cnf
/path/to/yalsat -T 2 /tmp/schur-six-537-plain.cnf 20261005 \
  > /tmp/schur-six-seed-20261005.log
python3 -B extract.py /tmp/schur-six-seed-20261005.log \
  /tmp/schur-six-seed-20261005.partial
cmp partials/20261005.partial /tmp/schur-six-seed-20261005.partial
```

With GCC 12.2.0 or a compatible C++20 compiler, replay the two complete-word
continuations:

```sh
python3 -B replay.py
```

The direct `audit.py` result, not YalSAT's scores or the stochastic replay,
is the evidence for the exact two-defect statement. The trust boundary is the
537-digit public fixtures and a direct enumeration of all equations.
