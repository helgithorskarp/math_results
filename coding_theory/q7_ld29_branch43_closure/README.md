# Couple/center closure of `Q_7` LD29 branch 43

## Certified result

There is no locating-dominating code of cardinality at most 29 in the binary
7-cube whose lossless orphan normalization has canonical local-graph index 43.
The branch has mask 639, sorted local degrees `(1,1,3,3,3,5)`, and four
triangles.

Together with the preceding exact exclusions, every hypothetical code of
cardinality at most 29 is now confined to the 49 normalized branches

```text
0--42, 48--49, 51, or 54--56.
```

This closes one further branch.  It does not exclude the remaining 49 branches
and does not yet prove the exact value of the locating-domination number of
`Q_7`.

## Complete defect split

Use the established exact-29 normalization

```text
0 in C;
e_i not in C                         (0 <= i < 7);
e_0+e_j not in C                     (1 <= j < 7).
```

Let `D` be the total Honkala--Laihonen--Ranto family defect and let `q` be
the number of codeword couples, i.e. two-vertex components of the induced
graph `Q_7[C]`.  The reviewed branchwise predecessor proves `D>=23` in
branch 43.  The local fathers use ten defect units, have total family
capacity 37, and force 20 absent son slots.

At exact defect 23, complete integer-state enumeration leaves seven states:

```text
q=4: 1,  q=5: 6.
```

Every state contains a defect-five (`F_7`) family.  Even if every free missing
slot is assigned to one such family, selecting its father would exceed the
complete family-codeword budget.  Hence the father is absent and all seven
neighbors are selected.  The sum of the residual local costs of all `F_7`
centers is at most the free-slot count; the latter is less than twice the
number of these families.  Some center therefore has cost at most one.

The order-12 stabilizer of the local graph reduces the 24 possible centers to
ten representatives:

```text
14 28 45 63 101 108 111 125 126 127
```

One aggregate formula imposes at least four exact codeword-couple indicators
and requires one of these full noncodeword-center configurations.

At exact defect 24, enumeration leaves 131 states, with distribution

```text
q=0: 1,  q=1: 6,  q=2: 10,  q=3: 18,  q=4: 38,  q=5: 58.
```

The 130 states with `q>=1` are covered by all locally compatible couple
positions.  There are 208 positions and 55 orbits under the local stabilizer.
The unique `q=0` state is

```text
(q, extra family defects, free missing slots, family-codeword budget)
(0, (1,1,1,5,6), 0, 10).
```

It contains one full `F_7` family and one full defect-six (`F_8`) family.
The `F_8` father and its closed ball are selected.  Selecting the `F_7`
father too would force 15 family codewords, so that father is absent and all
its neighbors are selected.  Zero slack forces both centers to have zero
local cost, and full-family separation gives mutual distance at least five.
There are 18 compatible ordered center pairs and four stabilizer orbits:

```text
(101,31) (101,59) (101,62) (101,122)
```

A second aggregate formula requires one of the 55 couple cases or four
center-pair cases.

For `D>=25`, the standard family identities and the binary
edge-isoperimetric bound give the relaxed necessary conditions

```text
p >= 49,  b <= 9,  p+b <= 58,  e(Q_7[C]) <= 13,
```

where `p` is the number of singleton signatures and `b` is the number of
nonisolated codewords.  A third formula imposes these bounds.

All formulas also impose cardinality 29, exact locating-domination, the
complete normalization, and all 15 local-graph units.  Their checked UNSAT
proofs exclude `D=23`, `D=24`, and `D>=25`.  The earlier lossless reduction
covers smaller codes by extending any such code to an exact 29-code.

## Exact formulas and certificates

The deterministic verifier reconstructs the family states, stabilizer
quotients, and all three CNFs.  Standalone CaDiCaL `sc2021` returned
`s UNSATISFIABLE` and emitted a plain-text DRAT trace for every formula.

| formula | variables | clauses | CNF SHA-256 | proof bytes | DRAT SHA-256 |
|:---|---:|---:|:---|---:|:---|
| `branch43-d23-q4-center-selector` | 13,162 | 218,990 | `c736109ae8ea728adc60d7e4915eaf892b397348536fb38ff246244ce4de20bd` | 163,609,346 | `98b1d33aad63bc391092a8c7c2ed8d91dac7e5da5a5b0a08091094811f0afdf0` |
| `branch43-d24-cover` | 11,387 | 193,479 | `a5f4b7ada5b2ea01b46bd4beed14216bee92ec0c08840417e6f66de8905b5b3e` | 999,203,074 | `4143683e79ee0b3c9e40ab0e2c6c1882a6bfd4d3d2735c61b1f5cbfce746a7bf` |
| `branch43-d25` | 10,432 | 183,619 | `284886102c5cc0d897ab04da660feec55c7c4368c0399c39d82db8c26fa84d76` | 388,161,745 | `c98812938992e18f2f63c308f4965079c874f75ad56455cbdfa6ed0eb6e96639` |

DRAT-trim returned `s VERIFIED` on all three exact CNF/proof pairs, with zero
RAT lemmas in every checked core.  In aggregate, the 1,550,974,165 proof
bytes have checked cores containing 16,588 original clauses and 5,473,262 of
9,959,174 proof lemmas, verified through 265,936,348 resolution steps.  The
compact manifest records the exact byte counts, hashes, checked-core
statistics, and solver/checker timings.

## Reproduction

Create the pinned environment under `/scratch`:

```bash
python3 -m venv /scratch/q7-ld29-branch43-closure-venv
/scratch/q7-ld29-branch43-closure-venv/bin/pip install -r requirements.txt
```

Reconstruct the analytic split, symmetry covers, and formulas:

```bash
/scratch/q7-ld29-branch43-closure-venv/bin/python \
  verify_branch43_closure.py \
  --write-directory /scratch/q7-ld29-branch43-closure-reproduced
```

Expected final line:

```text
PASS aggregate formulas exclude branch 43; 49 normalized branches remain
```

For every generated formula, produce and check the proof under `/scratch`:

```bash
cadical -q --binary=false FORMULA.cnf FORMULA.drat
drat-trim FORMULA.cnf FORMULA.drat -w
```

The optional independent solver route is `--solve-kissat`; it is not part of
the certificate reported here.

Reported environment and source hashes:

```text
Python                                   3.11.2
python-sat[pblib]                        1.9.dev15
CaDiCaL proof producer                   sc2021
CaDiCaL executable SHA-256               c6de62662723ec4a7426c5ca2bc9bfb04c60aad81a423957e3cd1ffadd0f8aa7
DRAT-trim Debian package                 0.0~git20240428.effa1dc-2
DRAT-trim executable SHA-256             bc7543a99da8521ddb09af442698956054f11e10d198bd482ac756535244c021
requirements.txt SHA-256                 639afc203e4b12224d62c9426902d5784099ba876c5ac2faed92e4659b56caca
verify_branch43_closure.py SHA-256        1391006c4572971d8295859208ae3230528cd37274344b4b2382afef688c18d3
certificate_manifest.tsv SHA-256         1802612ea8b02c8f8d66be676a712bfa26b2f717d0899ce72c3d34dabe1b3784
verify_minimal_defect_couples.py SHA-256  a0200279d73eb139a04ea0be45ad94b4cd40651ae2847223abb8c8bd718d52ee
verify_sibling_closures.py SHA-256        1069616e39ad4c39e46d0094f91c6e2a9efc13983229033add53cf5551ac4fe6
```

## Trust boundary and context

The theorem depends on the Honkala--Laihonen--Ranto family partition, the
reviewed lossless orphan normalization, and the reviewed `D>=23` branchwise
predecessor.  The new analytic bridges are the complete exact-23 and exact-24
state enumerations, forced-center arguments, and exhaustive stabilizer
quotients.

The Boolean layer depends on the reviewed locating-domination encoding,
PySAT totalizers, CaDiCaL proof production, and DRAT-trim.  Each DRAT trace
proves only the unsatisfiability of its hashed CNF.  The deterministic source
connects those formulas to the mathematical cases.  CNFs, proof traces,
solver output, and checker logs remain under `/scratch` and are deliberately
not committed.

The family method is due to I. Honkala, T. Laihonen, and S. Ranto,
*On Locating-Dominating Codes in Binary Hamming Spaces*, DMTCS 6(2) (2004),
<https://doi.org/10.46298/dmtcs.322>.  V. Junnila, T. Laihonen, and T.
Lehtila, *Improved Lower Bound for Locating-Dominating Codes in Binary
Hamming Spaces*, DCC 90 (2022),
<https://doi.org/10.1007/s10623-021-00963-8>, records the published
small-dimension context.

Targeted primary-source and Discovery Net searches through 2026-09-02 found
no prior exclusion of normalized branch 43.  This is apparently new relative
to those searches; no absolute historical-priority claim is made.
