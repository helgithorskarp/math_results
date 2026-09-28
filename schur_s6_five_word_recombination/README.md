# Certified five-word recombination exclusion for the 537 Schur-six target

## Exact statement and scope

The [classical sixth Schur number](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32)
asks for a six-colouring of every integer in `[1,N]` with no monochromatic
`x+y=z`, **including `x=y`**. The published lower bound is `S(6)>=536` in
the largest-colourable-endpoint convention. This result gives **no new bound**.

Take the five explicit 537-digit words in `sources.json`. Each is a valid
colour assignment with only one, two, or three Schur violations; none is a
valid classical 537-colouring. Relabel their colour digits by the following
global permutations, where the six-digit string gives the image of input
colours `1,2,3,4,5,6` in that order:

| Word | Permutation | Original violations |
| --- | --- | --- |
| `W` | `123456` | `12+12=24`, `12+24=36` |
| `190` | `564123` | `22+22=44` |
| `359` | `125364` | `2+2=4` |
| `best3` | `563421` | `5+41=46`, `5+46=51`, `46+51=97` |
| `347` | `564123` | `22+22=44` |

At each position `v=1,...,537`, choose **independently** one of the colours
appearing at `v` in these five relabelled words. There is **no** six-colouring
of `[1,537]` in this recombination family. The complete allowed-colour
domain histogram is: 2 positions have one choice, 112 have two, 285 have
three, 134 have four, and 4 have five. This is a nonlocal family with no
fixed old colour classes, position blocks, or Hamming-distance limit. It is
also a strict restriction of all possible six-colourings, so its exclusion
does not prove `S(6)<=536`.

The source words have independent provenance. `W` is the normalized
[public two-defect word from umaia1234](https://github.com/umaia1234/agentic-conjectures/blob/main/problems/schur-6/README.md),
whose [original class file](https://github.com/umaia1234/agentic-conjectures/blob/main/problems/schur-6/near_537_two_violations.col)
is Apache-2.0. Words `190`, `347`, and `359` are the [previously published
modular-orbit fixtures](../schur_s6_537_doubling_traps/fixtures.json).
`best3` is the [previous nonlocal-search word](../schur_s6_nonlocal_doubling_search/best3.txt).
The exact strings are repeated here so verification does not depend on
those other files. `audit.py` checks every original violation directly.

## Certificate

For each position and each colour in its allowed domain, `encode.py` creates
one Boolean variable. Exactly-one clauses choose a colour at every position.
For each unordered integer triple `x<=y`, `x+y=z<=537`, and each colour
common to its three domains, a clause forbids that monochromatic choice.
The 72,092 triples include 268 doubling triples with `x=y`; repeated
vertices have just one literal in a clause. Thus the CNF is satisfiable
**if and only if** the stated five-word family contains a valid complete
537-colouring.

The canonical DIMACS has 1,637 variables and 60,640 clauses, SHA-256
`8817015cc4d8d041bee9c36de87e1929042b0a62fdcab35999948188ac404958`.
An independent `z`-first implementation in `audit.py` rebuilds the domains,
recounts every source word's violations, and compares the exact clause
multiset. CaDiCaL 1.9.5 produced an UNSAT DRAT proof; DRAT-trim verified it
with `s VERIFIED`. The tested binary proof has 4,942,527 bytes and SHA-256
`22c9a7b09401a697df20b8ae5a3c1861af3998ba217c32b13c32cea2c0d45049`.
Its backward check used 13,413 input clauses and 65,247 core lemmas. The
proof file is generated locally and is not stored in Git.

The tested solver source was CaDiCaL commit
`146207318796f094dcded87349a64f0c6927309e`; the checker source was
DRAT-trim commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.
`expected.json` records the canonical dimensions and digests. Other solver
builds may produce different proofs; successful independent DRAT verification
is the decisive check, while `--strict-proof-hash` additionally checks the
particular binary proof above.

## Reproduce

Requires Python 3.11 or newer for `hashlib.file_digest`, plus CaDiCaL and
DRAT-trim binaries. From this directory:

```sh
sha256sum -c SHA256SUMS
python3 -B encode.py --cnf /tmp/schur-five-recombine.cnf
python3 -B audit.py --cnf /tmp/schur-five-recombine.cnf
python3 -B verify.py --cadical /path/to/cadical --drat-trim /path/to/drat-trim
```

The final line of `verify.py` begins `PASS DRAT_verified=yes`, with the CNF
hash above. The verifier regenerates the CNF, runs the independent audit,
runs CaDiCaL with seed `20260928`, checks the proof with DRAT-trim, then
deletes the generated CNF and proof. With the cited solver and checker
versions, add `--strict-proof-hash` to reproduce the exact proof digest.
`check.py` separately recounts all classical triples for any proposed
537-digit word.

For further **constructive** searches, `encode.py --set 347=425316` changes
one global alignment, while `search.py` solves an alignment with PySAT and
independently checks any SAT model as a complete word. Install the optional
`python-sat==1.9.dev15` dependency from `requirements.txt`, then run:

```sh
python3 -B search.py --set 347=425316 --budget 200000 \
  --out /tmp/schur-537-candidate.txt
```

For this wider alignment, that bounded probe returned `UNKNOWN`; it has no
exclusion certificate. `diagnostics.json` records 20 bounded four-word
alignment probes and four additional five-word variants to prevent duplicate
search effort. Their timeouts and one unverified solver-UNSAT output are
**not** part of the certified statement. A verified SAT word in any
alignment would establish `S(6)>=537`, regardless of this fixed-alignment
exclusion.
