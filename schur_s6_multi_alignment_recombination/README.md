# Certified multi-alignment recombination exclusion at 537

The classical sixth Schur number uses **all** integer solutions `x+y=z`,
including `x=y`. The published lower bound is
[`S(6)>=536`](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32)
in the largest-colourable-endpoint convention. This result concerns a
specified family of complete 537-words and gives **no new numerical bound**.

## Exact finite result

Take the five exact near-colourings `W`, `190`, `359`, `best3`, and `347`
in `sources.json`. A six-digit permutation lists the images of original
colour labels `1,...,6`. Form six aligned words:

| Source | Permutation |
| --- | --- |
| `W` | `123456` |
| `190` | `564123` |
| `359` | `125364` |
| `best3` | `563421` |
| `347` | `564123` |
| `347` again | `524163` |

At each position `v=1,...,537`, independently choose any colour seen there
among the six aligned words. **No such choice is a valid classical
six-colouring of `[1,537]`.** The domain-size histogram for sizes 1 through
6 is `[2,91,258,170,16,0]`: only positions 17 and 62 are fixed, and the
other 535 positions may change independently. No original colour class,
position block, or Hamming distance is preserved by the rule.

This family **strictly contains** the [previous certified five-word
family](../schur_s6_five_word_recombination/README.md): the second 347
alignment adds 81 position-colour options. `audit.py` checks this
containment directly. The five distinct source words have independently
checked defect counts `2,1,1,3,1`, respectively. The `190`, `347`, and
`359` strings come from the [modular-orbit
fixtures](../schur_s6_537_doubling_traps/fixtures.json); `best3` comes from
[nonlocal search](../schur_s6_nonlocal_doubling_search/best3.txt). `W` is
the normalized [external two-defect word by
umaia1234](https://github.com/umaia1234/agentic-conjectures/blob/main/problems/schur-6/README.md),
whose [original file](https://github.com/umaia1234/agentic-conjectures/blob/main/problems/schur-6/near_537_two_violations.col)
is Apache-2.0. The exact strings are copied into `sources.json` so the
certificate needs no other repository files.

## Exact encoding and proof

`encode.py` creates one Boolean variable for each allowed
`(position,colour)` pair and exactly-one clauses at each position. For
each unordered triple `x<=y`, `x+y=z<=537`, and each colour common to the
three domains, it forbids that monochromatic assignment. Repeated summands
are represented by one literal for the repeated position. These conditions
are satisfiable exactly when the stated family contains a valid complete
537-word. There are 72,092 triples, 268 with `x=y`.

The `two_347_alignments` CNF has 1,718 variables and 71,232 clauses,
SHA-256 `c25ebf4e5024b35b6dc3fe9af5727a3e70b1ed5070fa28874e0007b57a57ae4f`.
`audit.py` independently reconstructs all domains and clauses using a
`z`-first triple traversal, verifies the original source-word defects,
compares the complete DIMACS clause multiset, and checks the strict domain
inclusion above. Kissat 4.0.4 returned `UNSAT` and produced a binary DRAT
proof. DRAT-trim returned `s VERIFIED`. The tested proof has 32,574,929
bytes, SHA-256
`1d3b8f63c4be540a2beb7807094ea7c4419252616142a5ed2efdc91b23a8358d`.
Its backward check used 19,632 input clauses and 374,343 core lemmas.
The proof is regenerated locally and omitted from Git.

Tested solver source: Kissat commit
`8af8e56f174b778aef3aa45af9f739b2a5f492c2`; proof checker source:
DRAT-trim commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.
Other builds may produce different valid proofs. Independent DRAT
verification establishes the exclusion; `--strict-proof-hash` additionally
checks the tested binary proof byte for byte.

## Reproduce and continue the construction search

Python 3.11 or newer, Kissat, and DRAT-trim are required for the
certificate. From this directory:

```sh
sha256sum -c SHA256SUMS
python3 -B verify.py --kissat /path/to/kissat --drat-trim /path/to/drat-trim
```

The final line is `PASS certified_cases=1 open_cases=2 exact_cnf_audits=3`.
The verifier regenerates all three listed CNFs, audits every clause,
regenerates the certified case's proof with Kissat seed `20260928`, checks
it with DRAT-trim, and removes temporary files. Add
`--strict-proof-hash` with the tested binaries for the reference digest.

`cases.json` also records two **open** strict supersets, each adding a
third alignment of word `347`:

| Case | Third permutation | Domain histogram | Bounded result |
| --- | --- | --- | --- |
| `three_347_alignments_zero_fixed` | `521463` | `[0,67,238,203,28,1]` | Kissat `UNKNOWN` at 240 seconds |
| `three_347_alignments_wide` | `514326` | `[1,52,229,212,41,2]` | Kissat `UNKNOWN` at 240 seconds |

The zero-fixed case has at least two choices at every position. These
timeouts prove nothing about either case. `expected.json` stores their
exact CNF dimensions and hashes, and `verify.py` audits them without
claiming UNSAT. For bounded constructive search, install the optional
`python-sat==1.9.dev15` from `requirements.txt` and run:

```sh
python3 -B search.py --case three_347_alignments_zero_fixed \
  --budget 200000 --out /tmp/schur-537-candidate.txt
```

Any SAT model is decoded to a complete 537-digit word and independently
checked by `check.py` against all 72,092 classical triples before it is
written. A checked witness would establish `S(6)>=537`; no such witness
was obtained here.

`domain_score.cpp` is a separate whole-word stochastic search restricted
to the zero-fixed case's allowed position colours. It scores all 72,092
triples, including doubling, and recounts its best state directly. It
requires domains of size at least two, which `prepare_masks.py` checks.
With GCC 12.2.0, the following reproduces the run from the one-defect
`190` word:

```sh
python3 -B prepare_masks.py --case three_347_alignments_zero_fixed \
  --start 190 --word-out /tmp/schur-190.txt --mask-out /tmp/schur-masks.txt
g++ -O3 -std=c++20 domain_score.cpp -o /tmp/schur-domain-score
/tmp/schur-domain-score /tmp/schur-190.txt /tmp/schur-masks.txt \
  190 100 100000 20 3 15 7
```

The deterministic ten-million-step run ended `defects=1 direct=1`;
the corresponding run with `--start 359` and seed `359` also ended at one
defect. The independently checked remaining triples were `22+22=44`
and `2+2=4`, respectively. Neither run found a valid colouring or proves
the open case impossible.
