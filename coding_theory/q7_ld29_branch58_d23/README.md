# Center-split certificates raise `Q_7` LD29 branch 58 to `D>=23`

## Certified result

Let `C` be an exact 29-word locating-dominating code in the binary 7-cube,
after the established lossless orphan normalization

```text
0 in C;
e_i not in C                         (0 <= i < 7);
e_0+e_j not in C                     (1 <= j < 7).
```

Let `H` be the local graph on directions `1,...,6`, with `ij` selected
exactly when `e_i+e_j` is a codeword, and put

```text
D = sum_F (|I(f_F)|-2)
```

for the total Honkala--Laihonen--Ranto family defect.  If `H` has canonical
index 58, then

$$
\boxed{D\geq23}.
$$

Branch 58 has canonical mask `2012`.  It is the triangle-free graph
`K_{3,3}-e`, with sorted degree sequence `(2,2,3,3,3,3)`, stabilizer order
eight, local defect ten, local family capacity 36, and forced local deficit
16.  The result sharpens the preceding branchwise bound `D>=22`.  It does
not exclude branch 58.

The new bound implies

$$
p\geq47,\qquad a\geq18,\qquad b=29-a\leq11,
\qquad e(Q_7[C])\leq E_7(11)=17.
$$

## Exact-defect-22 reduction

For `q` codeword couples, the standard family identities give

$$
p=24+D,\qquad M=104-D-2q,\qquad
a\geq D-5,\qquad 2q\leq34-D.
$$

At `D=22`, exact integer-partition enumeration with the established
defect-five/defect-six occupancy inequalities leaves only five states.
Here `extra defects` lists the nonlocal family defects, `free missing` is
the number of missing son slots left after the 16 forced local slots, and
the last column is the complete family-codeword budget.

| `q` | extra defects | free missing | family-codeword budget |
|---:|:---|---:|---:|
| 5 | `(1,1,5,5)` | 0 | 2 |
| 6 | `(1,1,1,1,1,1,1,5)` | 0 | 0 |
| 6 | `(1,1,1,4,5)` | 0 | 0 |
| 6 | `(1,1,5,5)` | 2 | 0 |
| 6 | `(2,5,5)` | 1 | 0 |

Every state contains at least one defect-five family.  Its father cannot be
a codeword: even assigning all free missing slots to that family would
force at least `7-free_missing` family codewords, more than the displayed
global budget.  Thus every defect-five father is a noncodeword whose seven
neighbors are codewords.

The residual local costs of the defect-five centers sum to at most the free
missing-slot count.  In every row that count is strictly less than twice
the number of defect-five centers.  Hence at least one center has residual
cost at most one.

## Center costs and symmetry quotient

Represent a center by its seven-bit word in coordinates `0,...,6`.  The
unavoidable residual cost of a noncodeword defect-five center is classified
as follows.

- Weights at most two are impossible under the normalization and the
  all-codeword-neighborhood condition.
- A weight-three center must be supported on a triangle of `H` and costs
  one.  Branch 58 is triangle-free.
- A weight-four center costs the number of selected local edges contained
  in its support.
- A weight-five center costs at least three.  Since
  `alpha(K_{3,3}-e)=3`, its non-orphan support contains a selected edge,
  and the corresponding distance-three relation destroys three predecessor
  slots.
- Weights six and seven have cost zero.

Quotienting all cost-at-most-one centers by the exact order-eight
stabilizer of `H` leaves the six representatives

```text
15, 63, 75, 95, 126, 127.
```

The verifier reconstructs the 115 canonical local-graph orbits, the five
integer states, the complete center-cost classification, the stabilizer,
and this six-orbit cover.

## Exact formulas and checked certificates

At exact defect 22 the necessary global consequences are

```text
p >= 46,  b <= 12,  p+b <= 58,  e(Q_7[C]) <= E_7(12)=20.
```

For each center representative, the exact formula combines those
consequences with domination of all 128 vertices, every essential
distance-two separation clause, cardinality 29, the complete orphan
normalization, all 15 local-graph units, and biconditional singleton,
nonisolation, and code-pair indicators.  It fixes the center outside `C`
and all seven of its neighbors inside `C`.

Every formula has 10,432 variables and 183,627 clauses.  Standalone
CaDiCaL `sc2021` returned `UNSATISFIABLE` and emitted a plain-text DRAT
trace for all six.  DRAT-trim returned `s VERIFIED` on every exact
CNF/proof pair, with zero RAT lemmas.  The compact manifest records every
formula and proof hash and all checker statistics.  In aggregate:

| item | aggregate |
|:---|---:|
| proof bytes | 81,178,696 |
| original core clauses | 17,692 |
| core lemmas | 254,899 |
| total lemmas | 797,032 |
| resolution steps | 10,415,190 |

PySAT's independent Kissat 4.0.4 binding also returned UNSAT on all six
freshly parsed formulas.  Therefore exact defect 22 is impossible.  The
predecessor bound `D>=22` then proves `D>=23` in branch 58.

## Reproduction

Create the pinned environment and regenerate all exact CNFs under
`/scratch`:

```bash
python3 -m venv /scratch/q7-ld29-branch58-d23-venv
/scratch/q7-ld29-branch58-d23-venv/bin/pip install -r requirements.txt
/scratch/q7-ld29-branch58-d23-venv/bin/python \
  verify_branch58_d23.py \
  --write-directory /scratch/q7-ld29-branch58-d23-cnfs
```

For each generated formula, produce and check the external proof under
`/scratch`:

```bash
cadical -q --binary=false FORMULA.cnf FORMULA.drat
drat-trim FORMULA.cnf FORMULA.drat -w
```

Run the independent solver cross-check with

```bash
/scratch/q7-ld29-branch58-d23-venv/bin/python \
  verify_branch58_d23.py --solve-kissat
```

Reported environment and hashes:

```text
Python                                  3.11.2
python-sat[pblib]                       1.9.dev15
CaDiCaL proof producer                  sc2021
CaDiCaL executable SHA-256              c6de62662723ec4a7426c5ca2bc9bfb04c60aad81a423957e3cd1ffadd0f8aa7
DRAT-trim executable SHA-256            bc7543a99da8521ddb09af442698956054f11e10d198bd482ac756535244c021
requirements.txt SHA-256                639afc203e4b12224d62c9426902d5784099ba876c5ac2faed92e4659b56caca
certificate_manifest.tsv SHA-256        e2a887346a30fdaea021253c890d45b8d27749af0081842f5060f9e299d68cfd
verify_branch58_d23.py SHA-256           c87ba037a3d0d1b7dcf08742201fed6b6511ae0c50b207fd34ced56891a34cec
```

CNFs, proof traces, solver output, and checker logs remain under `/scratch`
and are deliberately not committed.

## Trust boundary and scope

The analytic bridge depends on the Honkala--Laihonen--Ranto family
partition, the reviewed lossless orphan-local normalization, and the
reviewed branchwise `D>=22` theorem.  Its finite component exhausts integer
family states, cube centers, and the exact local-graph stabilizer.  The
Boolean layer depends on the deterministic encoding, PySAT totalizers,
CaDiCaL proof production, and DRAT-trim.  A DRAT trace proves only its
hashed CNF; the analytic center cover is a separate obligation.

The family method is due to I. Honkala, T. Laihonen, and S. Ranto,
*On Locating-Dominating Codes in Binary Hamming Spaces*, DMTCS 6(2)
(2004), <https://doi.org/10.46298/dmtcs.322>.  V. Junnila, T. Laihonen,
and T. Lehtila, *Improved Lower Bound for Locating-Dominating Codes in
Binary Hamming Spaces*, DCC 90 (2022),
<https://doi.org/10.1007/s10623-021-00963-8>, records the prior published
small-dimension context.

Targeted primary-source and refreshed Discovery Net searches through
2026-09-01 found no branch-58 center split or defect-23 specialization.
The refinement is apparently new relative to the searched sources; no
absolute historical-priority claim is made.
