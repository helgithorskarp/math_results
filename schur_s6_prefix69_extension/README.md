# An exact extension threshold for a 69-entry Schur-six prefix

The labelled 69-entry word in `prefix69.txt` has a six-colouring through 338,
given by `witness338.txt`, but **no** six-colouring through 339. Thus no
six-colouring of `[1,537]` can begin with this labelled prefix (or any global
permutation of its six colours). This is a scoped exclusion, not a new upper
bound for the sixth Schur number. Every classical triple `x+y=z`, including
`x=y`, is included.

The prefix is the first 69 entries of the published [`best4.txt`](https://github.com/helgithorskarp/math_results/blob/main/schur_s6_nonlocal_doubling_search/best4.txt).
The 338-entry witness was obtained by a SAT solver and is checked by
`check.py` without trusting that solver. A previous diagnostic had fixed 80
entries and reported UNSAT for 537 without a proof certificate. This result
shortens the fixed prefix to 69, lowers the impossible endpoint to 339, and
provides a DRAT checking route.

## Reproduce the claim

Use CPython 3.11, [CaDiCaL 1.9.5](https://github.com/arminbiere/cadical/tree/146207318796f094dcded87349a64f0c6927309e)
and [drat-trim](https://github.com/marijnheule/drat-trim/tree/2e3b2dc0ecf938addbd779d42877b6ed69d9a985).
The commands below write generated files to `/tmp`; adapt the executable
paths if installed elsewhere.

```sh
python3 -B check.py
python3 -B encode.py --n 339 --output /tmp/schur-prefix69-n339.cnf
python3 -B audit.py /tmp/schur-prefix69-n339.cnf
sha256sum /tmp/schur-prefix69-n339.cnf
cadical -q -n /tmp/schur-prefix69-n339.cnf /tmp/schur-prefix69-n339.drat
drat-trim /tmp/schur-prefix69-n339.cnf /tmp/schur-prefix69-n339.drat
```

Expected witness-check output is `PASS n=338 prefix=69 triples=28561 defects=0`.
The independent clause audit prints
`PASS n=339 clauses=177873 triples=28730 prefix=69`.
The CNF is `2034` variables and `177873` clauses, SHA-256
`b454847f2307822f31a2054b461096f1addc85bf3a48179caed4f8a5b6bb1dc2`.
CaDiCaL 1.9.5 at source commit above, compiled with GCC 12.2, returned
`s UNSATISFIABLE`; its raw binary DRAT proof had SHA-256
`70406c65d476271ab08ba944cc313fee1a7f45818d7cba284b52c298309a3efa`.
The independently run `drat-trim` returned `s VERIFIED` and reported 19,010
input clauses and 138,294 learned clauses in the proof core. The exact DRAT
bytes are not required to trust CaDiCaL: the regenerated proof must pass
`drat-trim` against the emitted CNF. The raw proof is 16,811,935 bytes, so it
is deliberately omitted from this compact source publication. Solver output
alone is not the certificate; the checking command is essential.

The CNF gives each integer exactly one of six colours. For each unordered
`x<=y` with `x+y<=339`, and each colour, it forbids all three entries from
having that colour. When `x=y`, duplicate literals yield a two-literal clause.
Finally the 69 unit clauses fix the prefix. `audit.py` checks the category,
validity, uniqueness, and count of every CNF clause independently of the
encoder; these checks establish that every required clause occurs exactly
once and that no extra restriction was added. A satisfying assignment would be
exactly a forbidden 339-entry extension, so a verified UNSAT proof establishes
the stated exclusion. Every longer extension would restrict to 339.

No claim is made about the adjacent 68-entry prefix: our bounded CaDiCaL runs
there returned `UNKNOWN` at 20 and 30 seconds. The 338-entry witness shows
that 339 is the first impossible endpoint for the 69-entry prefix.
