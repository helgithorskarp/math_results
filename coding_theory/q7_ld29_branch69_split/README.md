# Full-family split and DRAT exclusion of `Q_7` LD29 branch 69

## Certified result

There is no locating-dominating code of cardinality at most 29 in the
binary 7-cube whose lossless orphan normalization has canonical local-graph
index 69.  The branch has mask `1789`, sorted degree sequence
`(1,3,3,3,4,4)`, four triangles, and independence number three.

The proof combines a hand-checkable full-family reduction with 17 exact
DRAT certificates: one for total Honkala--Laihonen--Ranto family defect at
least 25, and 16 for the complete defect-24 exceptional split.  This closes
one further finite branch; it does not prove that a 29-word code is
impossible.

## Defect-24 full-family reduction

Let `C` be an exact 29-word locating-dominating code after the lossless
normalization

```text
0 in C;
e_i not in C                         (0 <= i < 7);
e_0+e_j not in C                     (1 <= j < 7).
```

Let `H` be the local graph on directions `1,...,6`, with `ij` selected
exactly when `e_i+e_j` is a codeword.  The preceding leaf-aware theorem
gives total family defect `D>=24` in branch 69.  Its local fathers use 12
defect units, have capacity 43, and force 24 distinct missing son slots.
For `q` codeword couples and `M` family vertices, the standard identities
are

$$
p=24+D,\qquad M=104-D-2q,\qquad
a\geq D-5,\qquad 2q\leq34-D.
$$

At `D=24`, exhaustive integer-partition enumeration followed by the
defect-six occupancy inequality leaves exactly

| `q` | extra family defects | unforced missing slots | family-codeword budget |
|---:|:---|---:|---:|
| 5 | `(1,1,5,5)` | 1 | 0 |
| 5 | `(2,5,5)` | 0 | 0 |

Thus there are two noncodeword defect-five centers, each covered by all
seven of its neighbors, and at most one missing son slot beyond those
already forced by the local graph.

### Center separation and cost

The two centers have distance at least five.  Distance one contradicts
their all-codeword neighborhoods.  At distance two, each center is the
alternate common neighbor for a pair in the other family and forces a
missing slot in each family.  At distance three, the two inward neighbors
are codewords at distance two from the opposite center, again forcing two
missing slots.  At distance four, an inward codeword is at distance three
from the opposite center and makes its three distance-two predecessors
fail to be sons.  All cases consume more than the available one slot.

For a possible center `f`, define the following lower bound `kappa(f)` on
additional missing slots.

- Weights at most two are excluded by the normalization and the
  all-codeword-neighborhood condition.
- A weight-three center cannot contain coordinate zero and its other three
  coordinates must form a triangle of `H`; it then occupies the common
  candidate of three local father slots and has `kappa=1` beyond the two
  locally counted triangle collisions.
- At weight four, every selected local word supported inside `f` is a
  codeword in a distinct son position of `f`, so `kappa` is at least the
  number of such local edges.
- At weight five, the non-orphan support has size at least four.  Since
  `alpha(H)=3`, it supports a selected local word at distance three; that
  word makes three predecessor slots fail, so `kappa>=3`.
- Weights six and seven have the safe lower bound `kappa=0`.

The versioned verifier exhausts all `binom(128,2)` unordered center pairs,
requiring distance at least five and total cost at most one.  Exactly 16
pairs remain:

```text
(22,111) (22,113) (22,123) (22,125)
(28,111) (28,113) (28,119) (28,123)
(38, 95) (38,113) (38,123) (38,125)
(44, 95) (44,113) (44,119) (44,123)
```

The integers are seven-bit cube vertices.  Every pair has total cost
exactly one, so the zero-slack capacity state has no possible centers.

## Exact finite split

The strong formula covers `D>=25` with

$$
p\geq49,\qquad a\geq20,\qquad b=29-a\leq9,
\qquad e(Q_7[C])\leq E_7(9)=13,
$$

together with `p+b<=58`.  Each exceptional formula uses the valid `D>=24`
bounds `p>=48`, `b<=10`, `p+b<=58`, and
`e(Q_7[C])<=E_7(10)=15`, then fixes its two centers to be noncodewords and
their fourteen neighbors to be codewords.  This is a relaxation of the
corresponding family case, so unsatisfiability is sufficient.

Every formula contains exact domination and distance-two separation,
cardinality 29, the complete orphan normalization, all 15 local-graph
units, and biconditional count indicators.  The strong formula has 10,432
variables and 183,619 clauses.  Each exceptional formula has 10,432
variables and 183,635 clauses.

CaDiCaL 1.5.3 emitted plain-text DRAT traces.  DRAT-trim
`0.0~git20240428.effa1dc-2` returned `s VERIFIED` on all 17 exact pairs,
with zero RAT lemmas in every core.  The strong checker core has 854,121 of
1,372,510 lemmas and uses 42,025,905 resolution steps.  Exceptional cores
use 581--4,970 lemmas and 16,521--231,369 resolution steps.
PySAT's Kissat 4.0.4 binding independently returned UNSAT on all 17 freshly
regenerated formulas.

| formula | CNF SHA-256 | proof bytes | DRAT SHA-256 |
|:---|:---|---:|:---|
| `d25` | `d9cb1197b68fd318cc8f9c713b2f9ad375a28dfc10e27eccafb3f1370d9323d7` | 217,608,128 | `41ecc5e6a71ae0b56a167e9df615470965039994e17a225476f9bc044f074c14` |
| `f22-g111` | `58992a0e49a6c50d593e165a3e9bdd4dfc742aeab16919c3e2e59796c791e650` | 804,545 | `ca1f2483e5a45f3190b7c9876378b24c1b43654b2b6dc80f71568a65443ae906` |
| `f22-g113` | `3df9c319d8228eed8685e97c94943507ffbbc7506a70eb4dcc18b054a60224f5` | 2,184,187 | `64032867a1bd4ed7a72f180208d2cd22c7e172bc2962699285cab899e7be0de7` |
| `f22-g123` | `755984369a7ce700338696fb1a0cbd8933e05f12e688e07ea8504f2e3fac6b98` | 752,261 | `c3189d71ef580c793ec5ac30fc6dd80052596d3e66bd11a64c6300c962fd8633` |
| `f22-g125` | `c39e3443d7d8325fae5e6be891ffa7446ac17e680b6589a6b66a886fccc96158` | 776,320 | `8276a3c6029061f21c58d756d1247311688ea6ed20cb52170372f2ee7eb34d26` |
| `f28-g111` | `987dad667e32b870283471d0776b031589934db05fac9f9ec71eeac6c639dacc` | 831,159 | `96e30c1ffb92588e25a7c2e74fb9f83fe550659560af0056309cfac2a7ae949c` |
| `f28-g113` | `59070b70bb4274ce03b31062909a0c91944620e291b1cefe47249e1777c57df5` | 989,113 | `b6e2e716c75b6d6749573d2137c56b70d18954671da0cafdae3ab64114fda990` |
| `f28-g119` | `860d12a615b26af325aa23ed51c9ec5f14595076b7f7ad049f95fc112590699a` | 1,065,833 | `a7f926e42bc4a42d31a13d5096bf3c87f7cb8a3b96fd6debb111e08f04569039` |
| `f28-g123` | `e4ba7a50e23f84792857dc2de15b8211860fa2f13a344cb658e9074d5a64fbe5` | 808,608 | `42f42b92d2c5fa85149b0749ab2bec9eea8c183af716c0e534ff7b6c84aa3b61` |
| `f38-g95` | `49a102515be97753ff35b787333c548ebe6241885b2b49eb006561bc2752bc29` | 839,029 | `613a4e44c5416b9be16bf725e7e063b2930c48ace7eaf690c000db5a016b5591` |
| `f38-g113` | `18b87234e74c57811535b7fc4e59104711061c8aaa31617caeb12e77b8824a9d` | 1,488,668 | `c91cf08806cb919163458899207da0abc88a6d419e09a81775a64b8f9279c831` |
| `f38-g123` | `63ebcf5a1d050022fbef5cc845fcc33bec5a3801d6a3b45f365a14183526d573` | 752,664 | `1203f134f0d9e3b31197c73c09b2a5b1e6efe30494f399a63619895e57f664e0` |
| `f38-g125` | `6d8d352c416f266f548f9318c0a88b06cf616973e3a20edbdcdcd751cbd6ebb8` | 792,088 | `d06af30ea0eb58593d3d8f3dbcdb7a5aa6f8395fc3b638d21820e25f9fd604d2` |
| `f44-g95` | `98a737187965efbe56feb49e88145685a5d9f9496b2ed3a05f7ca59ebaf3dae9` | 746,685 | `d2a7fb902141a160e1ac18047b5079864467cb6577b68987f541a012e70d83df` |
| `f44-g113` | `a4affcd150833d3a2ab6f09c1cd4de53203037a20ffd326ef98578c94acc63ea` | 1,920,861 | `7ee3f61fee72e5e460f64a1b770162031d795153e2f0b3f160d3697d44a8d878` |
| `f44-g119` | `0172dbfb83b9235bddab0c5360c052b5b610f0c82eb5eda3cd9a55a6a2ef0bcc` | 753,501 | `742c287d11169879dc45d0cbb3ce759cf492be6be5e1e099c4d4913f5931bb9f` |
| `f44-g123` | `60c466aabb802a1b07d2f2e950cffe7d1ca173696124f4a0a3a2b581f4256aa5` | 749,298 | `8797ac0c1a6ae1e2893cd94e425c37188283ffad4a5c2f6ca7d4cc4e90a24840` |

The CNFs, proof traces, and checker logs remain under `/scratch` and are
deliberately not committed.

## Reproduction

The adapter digest-pins and reuses the generic full-family kernel from
`../q7_ld29_branch79_split`.

```bash
python3 -m venv /scratch/q7-ld29-branch69-split-venv
/scratch/q7-ld29-branch69-split-venv/bin/pip install -r requirements.txt
/scratch/q7-ld29-branch69-split-venv/bin/python \
  verify_branch69_split.py \
  --write-directory /scratch/q7-ld29-branch69-split
```

For every generated formula:

```bash
cadical -q --binary=false FORMULA.cnf FORMULA.drat
drat-trim FORMULA.cnf FORMULA.drat -w
```

The independent solver cross-check is

```bash
/scratch/q7-ld29-branch69-split-venv/bin/python \
  verify_branch69_split.py --solve-kissat
```

Reported environment:

```text
Python                          3.11.2
python-sat[pblib]              1.9.dev15
CaDiCaL                        1.5.3 (sc2021 banner)
CaDiCaL executable SHA-256     c6de62662723ec4a7426c5ca2bc9bfb04c60aad81a423957e3cd1ffadd0f8aa7
DRAT-trim                      0.0~git20240428.effa1dc-2
DRAT-trim executable SHA-256   bc7543a99da8521ddb09af442698956054f11e10d198bd482ac756535244c021
generic-kernel SHA-256         ea313ef366ad3b2da6c4e43d721aef8e96ec9bfa7dafe18c8fdade61c5fdd687
```

## Trust boundary, scope, and novelty

The analytic split depends on the Honkala--Laihonen--Ranto family
partition, the reviewed orphan-local reduction, the leaf-aware `D>=24`
theorem, the full-family separation argument, and an exhaustive 128-vertex
center classification.  The exact exclusions additionally depend on the
deterministic SAT encoding, PySAT totalizers, CaDiCaL proof production, and
DRAT-trim.  DRAT proves exactly the 17 hashed CNFs; the analytic bridge is
separate.

The family method is from I. Honkala, T. Laihonen, and S. Ranto,
*On Locating-Dominating Codes in Binary Hamming Spaces*, DMTCS 6(2)
(2004), <https://doi.org/10.46298/dmtcs.322>.  V. Junnila, T. Laihonen,
and T. Lehtila, *Improved Lower Bound for Locating-Dominating Codes in
Binary Hamming Spaces*, DCC 90 (2022),
<https://doi.org/10.1007/s10623-021-00963-8>, records the prior interval
`28 <= gamma^LD(Q_7) <= 32` and improves the general lower bound only from
dimension ten.

Targeted primary-source and refreshed Discovery Net searches through
2026-09-01 found no full-family split or exact certificate for branch 69.
The result is apparently new to the searched sources; no historical
priority claim is made.
