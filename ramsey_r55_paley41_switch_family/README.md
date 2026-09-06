# Entire Paley(41) switching class excluded for Ramsey(5,5)

Every Seidel switch of Paley(41) has a monochromatic K5. Therefore no
43-vertex Ramsey(5,5) graph can contain an induced 41-vertex subgraph in
that switching class, even with arbitrary relabeling and arbitrary edges
touching the other two vertices. This excludes a complete family of
2^123 distinct labeled 43-vertex graphs; it does **not** exclude all
43-vertex graphs or improve a Ramsey bound. No target graph was found.

The [proof and exact scope](PROOF.md) explain the normalization, full-family
formula, physical obstruction, and certificate logic. The result imposes
no automorphism or degree condition and does not use the parked H92/H93
neighborhood-gluing route. No novelty or independent-review claim is made.

## Fast, solver-free reproduction

Python 3.11.2, standard library only. From this directory:

```sh
python3 check_certificate.py obstruction.dimacs certificate.drat.txt
python3 certificate_controls.py obstruction.dimacs certificate.drat.txt
python3 -O check_certificate.py obstruction.dimacs certificate.drat.txt
python3 -O certificate_controls.py obstruction.dimacs certificate.drat.txt
```

Expected status: `VERIFIED_PALEY41_SWITCH_CLASS_EXCLUSION`.
The 20,499-byte physical obstruction contains 1,184 clauses on the 40
normalized switch bits. The 39,073-byte certificate contains 501 additions
(284 RUP, 217 RAT) and 1,669 deletions. The standalone checker validates
the physical K5 meaning of every input clause and every proof step.
Observed direct verification time: about 0.64 seconds.

Certificate hashes:

```text
67eb55fbd11e5973a23e5a0f58cb37ceda4d763fc17d4984e45bbf2bc34c5005  obstruction.dimacs
0c834bdd845eb921d30d66e97694c6a2873021f05582bb3a61c5807414866aa2  certificate.drat.txt
```

The certificate controls check 512 tiny formulas, with 27,648 semantic RUP
tests and 27,648 semantic RAT tests (including new-variable pivots), plus
two positive proof regressions and eleven rejected corruptions. They run
with explicit checks that remain enabled under `python3 -O`.

## Reconstruct the complete 43-vertex formula

```sh
python3 controls.py
python3 generate.py run
python3 verify.py run/family.cnf --output run/verification.json
```

Expected: 123 variables, 137,950 clauses, 3,990,811 DIMACS bytes; SHA-256:
`ad5b38c36beb6c1cf0b5e573662f8bf05057b6d1a6130da551c0f098224bf594`.
The generator took 7.62 seconds; the independent reconstruction took
4.54 seconds. It audited all 962,598 physical five-sets and compared exact
clause sets. Pattern controls covered all 1,096 labeled base graphs on
3,4,5 vertices and 33,856 switch truth cases, plus nine malformed inputs.
`summary.json`, `verification.json`, and the two control summaries record
the compact deterministic outputs.

## Optional solver/proof-extraction reproduction

This is not needed to check the committed theorem certificate.

```sh
python3 decide.py run --kissat /path/to/kissat --drat-trim /path/to/drat-trim
python3 check_certificate.py run/core.cnf run/trimmed.drat
```

Kissat 4.0.4, source `8af8e56f174b778aef3aa45af9f739b2a5f492c2`;
DRAT-trim source `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.
The wrapper makes one invocation with `--time=300 --no-binary`, a 330-second
wall limit, and default solver settings. On this run it returned UNSAT
in 5.53 wall seconds, exit 20, with maximum solver RSS 29,884 KiB.
The original 480,577-byte DRAT trace was checked in 1.22 wall seconds,
exit 0, with `s VERIFIED`; observed child-process RSS high-water mark
after proof checking was 71,868 KiB. See `result.json` for hashes.

The wrapper refuses to overwrite a prior solver log, reports incomplete
runs as no conclusion, and directly checks every physical five-set if SAT
is returned. That SAT-output branch was not exercised by this UNSAT run;
it is not part of the theorem's certificate trust base.

Generated full formulas, untrimmed proofs, logs, and runtime state remain
outside the repository. They can be regenerated from source; the compact
obstruction and trimmed trace are included. No solver or checker binary
is bundled. The checks are not proof-assistant formalization or external
independent review.
