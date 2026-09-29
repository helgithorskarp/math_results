# Globally sound cuts for complete Schur-six search at 537

The classical Schur number `S(6)` uses the largest six-colourable endpoint,
with `x=y` included in `x+y=z`. The published lower bound is
[`S(6)>=536`](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32).
This directory supplies reproducible complete 537 SAT targets using two
previously proved necessary conditions. **No 537-colouring or upper-bound
certificate was found.** All bounded solver runs below ended `UNKNOWN`.

## Why the cuts preserve every possible solution

The [reviewed Fredricksen–Sweet distance theorem](../schur_s6_fredricksen_sweet_distance_review4/REVIEW.md)
says that every valid 537 word differs from the exact
[`baseline.txt`](../schur_s6_fredricksen_sweet_distance/baseline.txt) in at least
54 of its first 536 positions, **under every global colour permutation**.
`encode.py` adds a PySAT totalizer for `at least 54` of the negative literals
`-X(v,baseline[v])`, where `X(v,c)` means position `v` has colour `c`.

The [reviewed four-class splitting theorem](../schur_s6_three_colour_trades/SPLITTING.md)
says that every valid 537 word splits at least four of the six old classes
of the exact external [`seed537.txt`](../schur_s6_external_class_trade/seed537.txt).
For each old class `i`, a selector `s_i` implies that class is not
monochromatic: for every new colour `c`, the clause
`-s_i OR -X(v_1,c) OR ... OR -X(v_m,c)` contains all its old members.
One positive clause for each three-selector subset forces at least four
selectors true. Conversely, any word splitting at least four classes extends
to these selectors, so the encoding loses no valid 537 word. This condition
is also invariant under relabelling.

The [previous complete first-occurrence encoding](../schur_s6_unrestricted_fullword_search/README.md)
orders all six colours by their first use (`rgs`). Its globally normalized
formula with both cuts remains complete. For independent three-branch search,
the [published branch argument](../schur_s6_537_branch_portfolio/README.md)
fixes colours of `1`, `2`, and `537` to `1`, `2`, and `b=1,2,3`.
Within branches 1 and 2, colours 3–6 remain freely permutable; in branch 3,
colours 4–6 remain freely permutable. The optional `--first-use` clauses order
the first use of those free labels. The distance theorem holds under every
relabel and splitting depends only on whether a class is monochromatic,
so these symmetry choices are compatible with both cuts.

| Complete target | Variables | Clauses | SHA-256 of generated CNF |
| --- | ---: | ---: | --- |
| Global `rgs` with both cuts | 10,785 | 600,188 | `e6a7ef74120a19a7ce6bdec3597608f06675523dd5560d38a87d90667a9b13df` |
| Branch 1 with both cuts and first use | 9,711 | 595,897 | `d3c81ede2d18bf1964c2326bdc532a6f339badb5d1b1d65cfdfa37477a43ac4c` |
| Branch 2 with both cuts and first use | 9,711 | 595,897 | `6dd9f9898aff3ec8928867c762f28c2cf06aaffa6933afc16759b3f3ab8df439` |
| Branch 3 with both cuts and first use | 9,174 | 593,750 | `97844b22dc79d95de21d9b74bd73a1c4742ca1451458f58edc6cdaa01c09c6d8` |

The first 3,222 colour variables use `6(v-1)+c`. Auxiliary numbers are
allocated after the base formula's variables. The distance totalizer adds
4,872 variables and 148,253 clauses; the splitting cut adds six selectors
and 56 clauses. All 72,092 unordered Schur equations, including 268
doublings, remain in every target.

## Reproduction and audit

Use CPython 3.11 or later with `python-sat==1.9.dev15`. Run from the
repository root. The earlier base encoders have independent clause audits;
[`audit.py`](audit.py) checks the exact base CNF SHA and prefix, every appended
clause and final dimensions. It also exhaustively tests the totalizer
interface on all assignments of two through six variables and every bound.

```sh
python3 schur_s6_unrestricted_fullword_search/encode.py \
  --mode rgs /tmp/schur-rgs537.cnf
python3 schur_s6_global_cut_search/encode.py --base-mode rgs \
  --base /tmp/schur-rgs537.cnf --distance --splitting \
  --out /tmp/schur-globalcuts537.cnf
python3 schur_s6_global_cut_search/audit.py --mode rgs \
  --base /tmp/schur-rgs537.cnf --target /tmp/schur-globalcuts537.cnf \
  --distance --splitting
```

To reproduce branch `b`, use the published **plain** base CNF and set
`--base-mode plain --branch b --distance --splitting --first-use` in
`encode.py`, and use `--mode plain` with the same other switches in
`audit.py`. The branch argument adds the two unit clauses
for colours of 2 and 537; the plain base already fixes colour 1. The
generated CNFs and raw solver logs are omitted from git because they are
deterministically regenerated from compact source and published inputs.

For any `SAT` log from Kissat, run
`python3 schur_s6_global_cut_search/check_model.py LOG WORD`. The checker extracts
exactly one colour per position and independently enumerates all 72,092
classical equations before writing a 537-digit word. A solver's `UNSAT`
status alone is **not** an upper-bound certificate; a DRAT proof must be
saved and independently checked with a tool such as `drat-trim` against the
exact generated CNF. The proof of each extra cut above is also part of the
trust boundary for such a certificate.

## Bounded search observations

Kissat 4.0.4 (source commit `8af8e56f174b778aef3aa45af9f739b2a5f492c2`)
ran with `--sat --time=180`. None of these statuses is an exclusion.

| Target | Seed | Result | Conflicts |
| --- | ---: | --- | ---: |
| Branch 3, distance only | 20261003 | `UNKNOWN` | 830,894 |
| Branch 3, splitting only | 20261003 | `UNKNOWN` | 915,998 |
| Branch 3, both cuts, no first use | 20261003 | `UNKNOWN` | 845,290 |
| Branch 3, first use only | 20261003 | `UNKNOWN` | 822,832 |
| Branch 3, both cuts and first use | 20261003 | `UNKNOWN` | 753,618 |
| Branch 1, both cuts and first use | 20261004 | `UNKNOWN` | 821,417 |
| Branch 2, both cuts and first use | 20261005 | `UNKNOWN` | 761,383 |
| Global `rgs` with both cuts | 20260930 | `UNKNOWN` | 718,118 |

A separate CaDiCaL 1.9.5 phase-hint run from the published distant
two-defect word on branch 3 with both cuts and first use returned `UNKNOWN`
at 500,000 conflicts (63.87 seconds). The seed was relabelled to satisfy
the branch and free-colour first-use convention. These results show that
the present budgets did not find a colouring or proof; conflict counts do
not measure distance to a solution.
