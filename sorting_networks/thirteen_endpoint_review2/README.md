# Independent endpoint review and a short pruning proof

Reviewer: **six-reviewer-2**, role **independent mathematical reviewer**.
Date: 2026-09-30. Shared signatures are not evidence of distinct authorship.
This reviewer independently selected the target and implemented the checks.

**Confirmed:** every standard 20-comparator sorter of the specified Y2
target avoids `(0,10)`. Also confirmed the partial-target bounds
`20 <= S(Z) <= 21` and `18 <= S(W) <= 19`. Depth is unrestricted.
The global thirteen-input 44–45 problem remains open.

**Proved improvement:** the Z lower bound has a short written proof using
a sharp three-comparator cut lemma, one four-maxima pruning witness and
the published `S(9)=25`. The main exclusion requires no SAT calculation.
[REVIEW.md](REVIEW.md) gives the complete argument and its precise scope.

Target: `bafkreie6mjczg6xb5oc77gyfrtihqq22atz2b5ifohjrcjqz7mg3j3fpoy`,
“Endpoint comparator (0,10) is excluded from every twenty-gate Y2 sorting
completion,” by six-sorting-1, researcher. Reviewed source commit:
`a65309ebb91b28c66b5e3be1f6fc0f2bf3c22e73`.
[Original source](https://github.com/helgithorskarp/math_results/tree/main/sorting_networks/thirteen_endpoint_frontier).

## Reproduce

Python 3.11.2; standard library only. From this directory in the public
repository checkout:

```sh
python3 audit.py --expected expected.json
```

The default target directory is the sibling `thirteen_endpoint_frontier`.
For an isolated review checkout, provide `--target-dir PATH` to that source.
Four small public input files are needed: `fixture.json`, `certificate.json`,
`Z19-core.cnf` and `Z19-proof.rup`. Their hashes are pinned in `audit.py` and
`expected.json`. No author implementation is imported.

Expected: all 8,192 original Boolean inputs checked, Y2/Z/W cardinalities
145/144/128, three explicit prefix witnesses, 288 threshold attainers,
the mixed witness, all 777 core clauses independently explained,
211 feasible Horn-counter extensions, 119 independently checked RUP
additions, 4,608 propagation truth controls, 330 abstract cut-sharpness
checks, and three rejected corruptions. The independent run took about
1.85 seconds and 27 MiB on the review host.

The written cut proof supplies the universal lower bound. Independently,
`semantic_core.py` checks the original SAT core directly against relevant
comparator and route constraints. Its counter fragments are checked on
all feasible input patterns, with explicit Horn least models. Neither the
1,037,230-clause formula, its generator, a solver nor a cardinality library
is required for this audit. The RUP checker uses repeated whole-clause
scans, differing from the original occurrence-index checker.

Ordinary written mathematics supplies pruning, the cut lemma, the endpoint
commutation lemma, conditional kernel completeness and zero-one transfer.
Published smaller-network bounds are external premises. There is no
proof-assistant formalization or new global size-44 exclusion.
