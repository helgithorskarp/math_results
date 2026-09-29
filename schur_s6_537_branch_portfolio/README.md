# A complete three-branch search for a Schur-six colouring of 537

The sixth classical Schur number is the largest endpoint whose integers
admit six colours without a monochromatic `x+y=z`, **including `x=y`**.
[Fredricksen–Sweet](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32)
established `S(6)>=536`; a [July 2026 paper](https://arxiv.org/abs/2607.15034)
still uses that bound. A checked six-colouring of `[1,537]` would improve
it. **No such word or upper-bound certificate was obtained here.**

## Why these three branches are complete

In any valid colouring, `1` and `2` have different colours because
`1+1=2`. Globally rename their colours to 1 and 2. If 537 has either of
those colours, it lies in branch 1 or 2. Otherwise, rename its colour to 3;
it lies in branch 3. The three cases therefore cover **every** six-colouring
of `[1,537]`, up to global colour permutation. The cases can be solved
independently; checked refutations of all three would imply `S(6)=536`
using the published 536-word. One checked SAT model would instead prove
`S(6)>=537`.

[`encode.py`](encode.py) gives Boolean variable `6(v-1)+c` the meaning
"integer `v` has colour `c`". Exactly-one clauses and every one of the
72,092 unordered equations `x<=y`, `x+y=z<=537` form the base formula.
Each branch adds units `colour(1)=1`, `colour(2)=2`, and
`colour(537)=b` for `b=1,2,3`. A doubling produces a two-literal
prohibition. Each formula has 3,222 variables and 441,147 clauses.
[`audit.py`](audit.py) independently regenerates the complete clause
multiset in a different triple order. The three CNF SHA-256 digests are
in [`expected.json`](expected.json). The generated 8 MB formulas and
solver logs stay outside this repository.

## Bounded search observations

Kissat 4.0.4, source commit
`8af8e56f174b778aef3aa45af9f739b2a5f492c2`, with `--sat` and the
specified 180-second budgets, returned `UNKNOWN` in all three branches:

| `b` | seed | conflicts | result |
| ---: | ---: | ---: | --- |
| 1 | 20261004 | 818,506 | `UNKNOWN` |
| 2 | 20261005 | 716,126 | `UNKNOWN` |
| 3 | 20261003 | 754,409 | `UNKNOWN` |

YalSAT 1.0.1, source commit `a0fd39f072f2d4693dd5a1977de3c3d3f69c8850`,
ran for 120 seconds per branch with zero unsatisfied clauses as its target.
The minimum reported clause counts were 2 for branch 1 with `--probsat`
(seed 20261011), 4 for branch 2 with `--walksat` (seed 20261012), and 2
for branch 3 with default settings (seed 20261013). These are Boolean
clause scores, **not** checked counts of monochromatic Schur equations;
no satisfying witness was returned. All statuses and scores are bounded
observations, not exclusions.

## Reproduce and extend

Python 3.11 or later and its standard library suffice to generate and
audit a branch:

```sh
python3 -B encode.py 1 /tmp/schur-six-branch1.cnf
python3 -B audit.py 1 /tmp/schur-six-branch1.cnf
sha256sum /tmp/schur-six-branch1.cnf
sha256sum -c SHA256SUMS
```

Replace `1` by `2` or `3` for the other cases. `search.py` regenerates
and audits the exact formula before calling Kissat. It directly checks
all classical Schur equations in any returned SAT word and writes a
537-digit witness only after that check:

```sh
python3 -B search.py --branch 1 --kissat /path/to/kissat \
  --seconds 180 --seed 20261004
```

For an `UNSAT` report, supply `--drat-trim /path/to/drat-trim` to generate
and independently verify the solver proof. Without this, the script marks
`UNSAT` **unverified**. An `UNKNOWN` status or a local-search score says
nothing about the existence of a 537-colouring. For the YalSAT observation,
run, for example, `timeout --signal=INT 120s /path/to/yalsat --probsat
/tmp/schur-six-branch1.cnf 20261011` and inspect its final minimum; use
`--walksat` for branch 2 and no option for branch 3.
