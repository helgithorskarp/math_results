# Couple/center closure of `Q_7` LD29 branch 46

## Certified result

There is no locating-dominating code of cardinality at most 29 in the binary
7-cube whose lossless orphan normalization has canonical local-graph index 46.
The branch has mask 763.

Together with the preceding exact exclusions, every hypothetical code of
cardinality at most 29 is now confined to the 50 normalized branches

```text
0--43, 48--49, 51, or 54--56.
```

This closes one further branch.  It does not exclude the remaining 50 branches
and does not yet prove the exact value of the locating-domination number of
`Q_7`.

## Complete defect split

Use the established exact-29 normalization

```text
0 in C;
e_i not in C                         (0 <= i < 7);
e_0+e_j not in C                     (1 <= j < 7).
```

Let `D` be the total Honkala--Laihonen--Ranto family defect.  The reviewed
branchwise predecessor proves `D>=23` in branch 46.  Let `q` be the number of
induced codeword couples: cube edges whose endpoints are selected and whose
other 12 neighbors are absent.

At exact defect 23, complete integer-state enumeration leaves seven states,
with couple counts

```text
q=4: 1,  q=5: 6.
```

Every state contains an `F_7` family.  Even if all free missing slots are
placed in that family, selecting its father would exceed the remaining family
codeword budget.  Thus its father is absent and all seven neighbors are
selected.  The sum of the residual local costs of all `F_7` centers is at
most the free-slot count; the latter is less than twice the number of such
families.  Some center therefore has local cost at most one.  Exact symmetry
reduction leaves 21 possible centers.  One aggregate formula requires at
least four couples and selects one of these 21 full `F_7` configurations.

At exact defect 24, enumeration leaves 131 states, with distribution

```text
q=0: 1,  q=1: 6,  q=2: 10,  q=3: 18,  q=4: 38,  q=5: 58.
```

The 130 states with `q>=1` are covered by the 205 locally compatible couple
positions.  The local graph has trivial stabilizer, so all 205 are distinct
orbits.  The unique `q=0` state has one full `F_7` family and one full `F_8`
family, no free missing slot, and family codeword budget 10.  The `F_8` father
and its closed ball are selected.  Selecting the `F_7` father too would force
15 family codewords, so that father is absent and all its neighbors are
selected.  The centers have distance at least five and zero local cost.
There are 12 compatible ordered center pairs, again 12 orbits.  A second
aggregate formula selects one of the 205 couple cases or 12 center-pair cases.

For `D>=25`, the standard family identities and binary edge-isoperimetric
bound give the relaxed necessary conditions

```text
p >= 49,  b <= 9,  p+b <= 58,  e(Q_7[C]) <= 13,
```

where `p` is the number of singleton signatures and `b` is the number of
nonisolated codewords.  A third aggregate formula imposes these bounds.

All three formulas also impose cardinality 29, the complete normalization,
all 15 local-graph units, and the exact locating-domination constraints.
Their checked UNSAT proofs exclude `D=23`, `D=24`, and `D>=25`, respectively.
The earlier lossless reduction covers smaller codes: any such code can be
extended to an exact 29-code while preserving location-domination.

## Exact formulas and certificates

The deterministic verifier reconstructs the family states, the stabilizer
quotients, and the three CNFs.  Standalone CaDiCaL `sc2021` returned
`s UNSATISFIABLE` and emitted a plain-text DRAT trace for every formula.

| formula | variables | clauses | CNF SHA-256 | proof bytes | DRAT SHA-256 |
|:---|---:|---:|:---|---:|:---|
| `branch46-d23-q4-center-selector` | 13,143 | 218,388 | `23e88ef2fb71f0673fa9310c8381d85e86a09ce66491951340c56a7c3b084723` | 337,136,034 | `891e592baa16e7429ee1b8168be184a981b430dc4777411e3df81780c76d6b55` |
| `branch46-d24-cover` | 11,545 | 195,707 | `a8b8471302f5ae46f59c48145c06de218278c9b9918c0ab15e3367dae0f9a159` | 635,810,837 | `5110d535f1b430b2e947ba8b95a5688cbca2217c4e2a374f4251c5e7df8dcedc` |
| `branch46-d25` | 10,432 | 183,619 | `b75c4fad945e3ad796c8702af40a40b19ceb1cae4900fb651c35b1422b044ab6` | 250,929,662 | `afc556ef6a9da0cb6ee86b5c01d7a0c1693ef72989b6e6e7dcd3d4bc4c6d90d6` |

DRAT-trim returned `s VERIFIED` on all three exact CNF/proof pairs, with zero
RAT lemmas in every checked core.  In aggregate, the 1,223,876,533 proof bytes
have checked cores containing 18,779 original clauses and 5,014,750 of
9,534,922 proof lemmas, verified through 269,651,953 resolution steps.  The
compact manifest records the exact byte counts, hashes, checked-core
statistics, and solver/checker timings.

## Reproduction

Create the pinned environment under `/scratch`:

```bash
python3 -m venv /scratch/q7-ld29-branch46-closure-venv
/scratch/q7-ld29-branch46-closure-venv/bin/pip install -r requirements.txt
```

Reconstruct the analytic split, symmetry covers, and formulas:

```bash
/scratch/q7-ld29-branch46-closure-venv/bin/python \
  verify_branch46_closure.py \
  --write-directory /scratch/q7-ld29-branch46-closure-reproduced
```

Expected final line:

```text
PASS aggregate formulas exclude branch 46; 50 normalized branches remain
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
Python                                  3.11.2
python-sat[pblib]                       1.9.dev15
CaDiCaL proof producer                  sc2021
CaDiCaL executable SHA-256              c6de62662723ec4a7426c5ca2bc9bfb04c60aad81a423957e3cd1ffadd0f8aa7
DRAT-trim Debian package                0.0~git20240428.effa1dc-2
DRAT-trim executable SHA-256            bc7543a99da8521ddb09af442698956054f11e10d198bd482ac756535244c021
requirements.txt SHA-256                639afc203e4b12224d62c9426902d5784099ba876c5ac2faed92e4659b56caca
verify_minimal_defect_couples.py SHA-256 a0200279d73eb139a04ea0be45ad94b4cd40651ae2847223abb8c8bd718d52ee
verify_sibling_closures.py SHA-256       1069616e39ad4c39e46d0094f91c6e2a9efc13983229033add53cf5551ac4fe6
```

The new verifier and manifest hashes are intentionally obtained from the
final committed files rather than pre-recorded here.

## Trust boundary and context

The theorem depends on the Honkala--Laihonen--Ranto family partition, the
reviewed lossless orphan normalization, and the reviewed `D>=23` predecessor
for branch 46.  The new analytic bridges are the complete exact-23 and
exact-24 state enumerations, the forced-center arguments, and the exhaustive
symmetry covers.

The Boolean layer depends on the reviewed locating-domination encoding,
PySAT totalizers, CaDiCaL proof production, and DRAT-trim.  Each DRAT trace
proves only the unsatisfiability of its hashed CNF.  The deterministic source
connects those formulas to the mathematical cases.  CNFs, proof traces, and
solver/checker logs remain under `/scratch` and are deliberately not committed.

The family method is due to I. Honkala, T. Laihonen, and S. Ranto,
*On Locating-Dominating Codes in Binary Hamming Spaces*, DMTCS 6(2) (2004),
<https://doi.org/10.46298/dmtcs.322>.  V. Junnila, T. Laihonen, and T. Lehtila,
*Improved Lower Bound for Locating-Dominating Codes in Binary Hamming Spaces*,
DCC 90 (2022), <https://doi.org/10.1007/s10623-021-00963-8>, records the
published small-dimension context.

Targeted primary-source and Discovery Net searches through 2026-09-02 found
no prior exclusion of normalized branch 46.  This is apparently new relative
to those searches; no absolute historical-priority claim is made.
