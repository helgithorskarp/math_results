# Unrestricted complete-word search for classical Schur six at 537

The sixth classical Schur number is the greatest `N` whose integers `1,...,N`
can be assigned six colours without a monochromatic `x+y=z`, **including
`x=y`**. Fredricksen and Sweet's [published construction](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32)
gives `S(6)>=536`. A verified complete 537-word would improve that bound.
This directory contains full-domain searches: every position can take every
colour, subject only to a sound global relabelling of the six colours.
**No 537-colouring or unrestricted upper-bound certificate was obtained.**

## Exact complete SAT targets

In the plain CNF, Boolean variable `6(v-1)+c` asserts that position `v` has
colour `c`. Exactly-one clauses enforce one colour per position. For every
`x<=y`, `x+y=z<=537`, and each `c`, a clause prohibits the monochromatic
triple; a doubling `x=y` gives a two-literal clause. There are 72,092 such
unordered equations, including 268 doublings. The only extra clause sets
the colour of 1 to 1, which is sound because colours may be globally renamed.

The `rgs` CNF additionally normalizes colour names by first occurrence.
Auxiliary `U(v,c)` means that colour `c` has appeared among positions
`1,...,v`. Clauses define `U(v,c)` exactly, and `C(v)=c>1` requires
`U(v-1,c-1)`. Thus the first appearances of used colours are ordered
`1,2,...`. Every valid word has such a relabelling, so a satisfying
assignment to this CNF still corresponds to a complete classical 537-word,
and an independently certified refutation would apply to **all** six-colourings
of `[1,537]`. This is the standard interchangeable-colour symmetry used in
[Schur SAT work](https://www.cs.utexas.edu/~marijn/Schur/); no novelty is
claimed for the symmetry rule.

| Encoding | Variables | Clauses | CNF SHA-256 |
| --- | ---: | ---: | --- |
| Plain | 3,222 | 441,145 | `fd6503a79cfeb53c614fe436669f192e81416b6e7292069938cf607f41b070e2` |
| First occurrence (`rgs`) | 5,907 | 451,879 | `332e4b211a672836c68320f9403b0454462a96df2071aefcc2a72f809820eb7c` |

`audit.py` constructs both clause multisets independently using a different
triple order and matches every generated clause. It also exhausts all 20,736
assignments of four positions in three colours and their auxiliary bits:
exactly the 14 canonical words satisfy the symmetry definition. This control
checks the finite encoding; the relabelling argument above establishes why
the 537 encoding loses no colouring.

## Bounded search observations

Kissat 4.0.4, source commit
`8af8e56f174b778aef3aa45af9f739b2a5f492c2`, returned `UNKNOWN` on the
plain CNF after 600 seconds and 2,981,103 conflicts (`--sat`, seed
`20260929`). It returned `UNKNOWN` on the first-occurrence CNF after 300
seconds and 1,511,371 conflicts (`--sat`, seed `20260930`). These runs give
no exclusion. `search.py` regenerates and audits either complete CNF, invokes
Kissat, and definitionally checks any returned SAT model before saving a
537-digit word. If a solver ever reports UNSAT, pass `--drat-trim` so the
proof is independently checked; solver text alone is not treated as a result.

An independent whole-word route used YalSAT source commit
`a0fd39f072f2d4693dd5a1977de3c3d3f69c8850` on the plain CNF, seed
`20260928`. Its `-T 2` target returned a Boolean assignment with exactly two
unsatisfied clauses in 10.50 seconds. `extract_yalsat.py` independently
checks all 441,145 clauses: the two failures are the at-least-one-colour
clauses for positions 2 and 4. The resulting [partial537.txt](partial537.txt)
has 535 singly coloured positions and no monochromatic Schur triple among
those positions. **It is not a 537-colouring.** All 36 ways to colour the two
holes were checked: the unique best direct completion colours both 2 and 4
with colour 2 and has 11 defects, saved as
[completed11.txt](completed11.txt).

The partial word is distant from the five previously published near words in
[`sources.json`](../schur_s6_multi_alignment_recombination/sources.json):
the minimum disagreements on its 535 coloured positions over all 720 global
colour permutations are `401,421,407,409,414` for `W`, `190`, `359`,
`best3`, and `347`, respectively. It therefore explores a genuinely different
region of the complete-word search.

Starting from that 11-defect completion, `fullscore.cpp` ran 10,000,000
unrestricted recolouring steps (seed `20260930`, 100 restarts of 100,000
steps, kick 20, global noise 3%, local noise 15%, tabu 7). The saved
[best4.txt](best4.txt) has precisely four independently checked defects:
`1+1=2`, `1+2=3`, `4+4=8`, and `4+5=9`. The preceding [doubling-safe four-defect
word](../schur_s6_nonlocal_doubling_search/best4.txt) is a different search
state. No heuristic score is used as a Schur bound.

## Reproduce

Python 3.11 or newer is enough for the exact encoders and checkers:

```sh
sha256sum -c SHA256SUMS
python3 -B encode.py --mode plain /tmp/schur-plain537.cnf
python3 -B audit.py --mode plain /tmp/schur-plain537.cnf
python3 -B encode.py --mode rgs /tmp/schur-rgs537.cnf
python3 -B audit.py --mode rgs /tmp/schur-rgs537.cnf
python3 -B check_partial.py
python3 -B check.py best4.txt
```

The last command reports four defects, including two doublings. For the
complete SAT route, build Kissat from the commit above and run, for example:

```sh
python3 -B search.py --mode rgs --kissat /path/to/kissat \
  --seconds 300 --seed 20260930
```

The local-search partial can be replayed with the YalSAT commit above:

```sh
/path/to/yalsat -T 2 /tmp/schur-plain537.cnf 20260928 > /tmp/yalsat537.log
python3 -B extract_yalsat.py /tmp/yalsat537.log /tmp/schur-plain537.cnf \
  --out /tmp/partial537.txt
cmp partial537.txt /tmp/partial537.txt
```

For the complete-word stochastic continuation, GCC 12.2.0 was used:

```sh
g++ -O3 -std=c++20 fullscore.cpp -o /tmp/schur-fullscore
python3 -B replay.py --binary /tmp/schur-fullscore
```

`phase_search.py` is an optional complete SAT probe with the four-defect word
as CaDiCaL phase hints; install the pinned `python-sat` in `requirements.txt`
to run it. All 537 positions remain unrestricted. A 200,000-conflict run
returned `UNKNOWN` after 28.84 seconds. The exact bounded statuses are in
`expected.json`; `UNKNOWN` conveys no bound.
