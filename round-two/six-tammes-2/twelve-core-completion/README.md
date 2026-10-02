# Twelve fixed incumbent points: arbitrary three-point completion

Actual author **six-tammes-2**, role **researcher**, 2026-10-02.

For the twelve exact incumbent positions with labels
`0,1,2,4,5,6,7,8,9,10,11,12` and pair parameter tau, there are exactly four
labeled three-point completions. Complete Gram equalities identify three
with the known asymmetric incumbent and one with the known cyclic incumbent.
The proof assumes no contacts on the added points. A linear stability bound
holds for product relaxation `0<=delta<=10^-7`: the added triple is within
`2100000 delta` of a completion, after exchanging its labels.

These are fixed positions at tau. The complete variable twenty-contact frame,
its arbitrary three-addition capacity, motif occurrence, and global Tammes-15
optimality remain separate. Independent review and formalization of this
new theorem are pending. See the full [proof](PROOF.md),
[dependency boundaries](DEPENDENCIES.md), and [literature](LITERATURE.md).

## Reproduce

Python 3.11 or later on Unix; the verifier uses only the standard library.
From this directory:

```sh
python3 -B check.py --start 0 --count 2500 --output result.json
python3 -B audit.py
python3 -B controls.py
python3 -B -O audit.py
python3 -B -O controls.py
```

The first command executes all 1,014 independent-active-triple candidates.
It checks root isolation, the H metric, all incumbent units/products,
positive dependence proving boundedness, the cap, every determinant,
Cramer identity, selected infeasibility witness, short norm, and exact unit
identification. It raises an exception on an unresolved exact sign or an
incorrect predicate. `--start` and `--count` permit explicitly partial runs;
a partial receipt proves only its stated range. The 50-second local guard
is operational: a timeout is incomplete evidence, not nonexistence.

The auxiliary audit checks all 420 pair bounds for the four completions,
1,125 whole-Gram entries including reconstruction of the known cyclic code,
and the constants/domains of the ordinary stability mass argument.
Controls reject 20 semantic damages and accept two harmless representations.
All validation guards use explicit exceptions, so Python `-O` does not remove
them. The author actually completed the whole final predicate range and
both auxiliary normal/optimized runs; [VALIDATION.json](VALIDATION.json)
records execution results and source pins. It is same-author evidence.

[INPUT.json](INPUT.json) contains five rational coefficients per algebraic
coordinate in the credited basis `(p0,p5,p11)`. [PLAN.json](PLAN.json) contains
three fixed combination-ordered tables. Tokens S,N,I-letter,U-letter mean
singular, strictly short feasible, infeasible by that plane, or exactly that
unit choice. Both JSON files bind the complete original target cohort.
The quintic arithmetic kernel is vendored and credited; no external source,
private data, solver, floating computation or network is needed to verify.

[select.py](select.py) is optional heuristic discovery using NumPy 1.24.2.
It proposes literal witnesses but supplies no mathematical verdict. Its
floating `packing_max` metadata and `heuristic_matches` proposals in INPUT
are nonbinding; `audit.py` independently verifies the proposed Gram maps
by exact identities. The public verifier never imports the selector.
The selector is not needed for reproduction of the proof.

[MANIFEST.json](MANIFEST.json) lists compact files and roles.
[SHA256SUMS](SHA256SUMS) binds all other published files. Keep generated
results outside the source directory when publishing; result files and
bytecode are ignored. No large proof corpus accompanies this certificate.
