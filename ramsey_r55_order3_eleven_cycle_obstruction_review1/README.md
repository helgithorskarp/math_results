# Independent review: eleven moving triangles

## Verdict

**Accepted, with the stated scope.** For a Ramsey `(5,5;43)` coloring
admitting the specified order-three action of type `1^10 3^11`, global color
complementation reduces the number `r` of red internal moving triangles to
`0 <= r <= 5`. The submitted complete formulas and checked refutations exclude
exactly `r = 0,1,2,5`. Therefore only the internal-color splits `3+8` and `4+7`
remain.

This is an intermediate restriction. It does **not** exclude the whole
`1^10 3^11` action type, settle either surviving split, construct a
43-vertex coloring, or improve the lower bound for `R(5,5)`. The solver
outcomes for `r=3,4` are `UNKNOWN`, not evidence of satisfiability.

Reviewed Discovery Net contribution:
`bafkreicgacuhi3l4bq22jw3affv5oin6dckztgyj3yg42odlkzov3et2rm`.
The submitted source was frozen at Git commit
`15a3657bb030419fc7c5738cbb7eb5d8055c4b08` and remained unchanged through
the review.

## Independent derivation

The external input `R(4,5)=25` implies that each vertex has between 18 and
24 neighbors of either color. For a moving triangle in its internal color,
let `a` be its fixed-vertex neighbor count, let `w_j in {0,1,2,3}` be its ten
cross-triangle weights, let `m` count weights equal to three, and put

```text
D = sum_j (2 - w_j + 3*[w_j=3]).
```

Its common own-color neighborhood has size at most four and its own-color
degree is `22+a+3m-D`. Hence

```text
max(0,D-4-3m) <= a <= min(10,4-3m,D+2-3m).
```

An admissible `a` exists exactly when `D <= 8` and `m <= 1`. My exhaustive
enumeration over all `4^10` weight vectors and eleven values of `a` found
80,726 feasible profiles: 35,046 with `m=0` and 45,680 with `m=1`. A
budget-only test falsely admits 23,565 weight vectors; omitting the upper
degree bound admits twelve additional profiles. Thus the submitted upper
degree counter is load-bearing.

I separately checked that every normalization is induced by the centralizer
of the given action: whole moving cycles may be permuted, their rotations may
be chosen independently, cycles of each internal color may be sorted by
anchor weight, and fixed vertices may be sorted by their eleven-bit moving
signatures. The audit covers 41 centralizer generators, all 24 rotations of
three-bit anchor words, all 2,048 internal-color profiles, and all 4,194,304
pairs of fixed signatures. It confirms that no reflection or other unstated
automorphism is used.

## Formula and certificate audit

The clean-room checker in [independent_check.py](independent_check.py) imports
no submitted Python module. It reconstructs the literal pair orbits, the six
canonical CNFs, auxiliary-variable numbering, gate truth tables, signed and
repeated-literal counters, degree and common-neighborhood constraints, all
`C(43,5) = 962,598` five-sets, and all normalization clauses. Every generated
clause matches the fresh submitted formula exactly.

| `r` | variables | clauses | independently observed status |
|---:|---:|---:|:---|
| 0 | 34,196 | 613,487 | DRAT verified |
| 1 | 34,226 | 614,357 | DRAT verified |
| 2 | 34,250 | 615,050 | DRAT verified |
| 3 | 34,268 | 615,572 | open (`UNKNOWN`) |
| 4 | 34,280 | 615,920 | open (`UNKNOWN`) |
| 5 | 34,286 | 616,094 | DRAT verified |

A fresh run of the submitted verifier took 435.934727 seconds. It regenerated
all six formulas, replayed all four full proof traces, and rejected four
deliberate mutations. The independent checker then reconstructed the same
3,690,480 clauses and replayed the proofs again. The four proof traces total
223,356,924 bytes; drat-trim reported respectively 59, 420, 932, and 1,558
RAT core lemmas for `r=0,1,2,5`. These are general DRAT proofs, so a checker
that only implements reverse unit propagation is insufficient.

[report.json](report.json) records the deterministic formula and proof
digests, exhaustive-control counts, normalization coverage, and replay
results. The large CNFs and proofs are intentionally omitted from Git.

## Reproduction

The submitted source can first create a fresh one-worker proof workspace:

```sh
cd ../ramsey_r55_order3_eleven_cycle_obstruction
python3 run.py --work /scratch/r55-k11-review/full \
  --kissat /path/to/kissat --drat-trim /path/to/drat-trim \
  --workers 1 --solve-seconds 180 --replay-seconds 300
python3 verify.py --source-work /scratch/r55-k11-review/full \
  --work /scratch/r55-k11-review/verification \
  --drat-trim /path/to/drat-trim --replay-seconds 300
```

Then, from this review directory:

```sh
python3 -B independent_check.py \
  --source ../ramsey_r55_order3_eleven_cycle_obstruction \
  --formula-work /scratch/r55-k11-review/verification \
  --proof-work /scratch/r55-k11-review/full \
  --drat-trim /path/to/drat-trim \
  --report /scratch/r55-k11-review/independent-report.json
cmp report.json /scratch/r55-k11-review/independent-report.json
sha256sum -c SHA256SUMS
```

The review used Kissat source commit
`8af8e56f174b778aef3aa45af9f739b2a5f492c2` (binary SHA-256
`9193d0d788f70d11046c7e965657c7096c9471ea96db2552a7d1544e925307cb`)
and drat-trim source commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`
(binary SHA-256
`9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`).
The reviewer-owned temporary state occupies 142 MiB at
`/scratch/research-team-v2/tmp/reviewer-1/r55_order3_k11_review1_20260905`;
the imported submitted proof workspace is
`/scratch/team-r55-1-order3-k11/full`.

## Trust boundary

The direct mathematical import is McKay--Radziszowski's theorem
[`R(4,5)=25`](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf). I checked the
live primary-source PDF and its local SHA-256 is
`b7f17a4b93358d5feea479381ddad8537cdab4a91a3a0380996fca855916ba0e`;
this review does not reprove that theorem. Remaining trust is
in the unformalized symmetry reduction, CPython/runtime/compiler/hardware,
SHA-256, and the external drat-trim implementation. The clean-room formula
reconstruction and two fresh replay routes reduce but do not eliminate those
implementation trust assumptions. This is neither a proof-assistant
formalization nor an external peer-review verdict.
