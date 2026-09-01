# Full-family split and DRAT exclusion of `Q_7` LD29 branch 79

## Certified result

There is no locating-dominating code of cardinality at most 29 in the
binary 7-cube whose lossless orphan normalization has canonical local-graph
index 79.  The branch has mask `5949`, sorted degree sequence
`(2,3,3,3,3,4)`, three triangles, and independence number two.

The proof combines a hand-checkable full-family reduction with ten exact
DRAT certificates: one for total family defect at least 25 and nine for the
complete defect-24 exceptional split.  This closes one additional finite
branch; it does not prove that a 29-word code is impossible.

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
gives total Honkala--Laihonen--Ranto family defect `D>=24` in branch 79.

The local fathers use 12 defect units, have capacity 43, and force 24
distinct missing son slots.  With `q` codeword couples and `M` family
vertices, the standard identities are

$$
p=24+D,\qquad M=104-D-2q,\qquad
a\geq D-5,\qquad 2q\leq34-D.
$$

At `D=24`, exact integer-partition enumeration followed by the defect-six
occupancy inequality leaves exactly two states:

| `q` | extra family defects | free missing slots | family-codeword budget |
|---:|:---|---:|---:|
| 5 | `(1,1,5,5)` | 1 | 0 |
| 5 | `(2,5,5)` | 0 | 0 |

Thus both states have two defect-five fathers, no family codewords, and at
most one missing slot beyond the 24 already forced locally.  Each father is
a noncodeword covered by seven codewords.

### Separation of the two centers

If the centers are at distance one, each lies in the other's all-codeword
neighborhood, a contradiction.  At distance two, each center is the
alternate common neighbor for a pair in the other family, forcing one
missing slot in each family.  At distance three, the two inward neighbors
are codewords at distance two from the opposite center, again forcing two
missing slots.  At distance four, an inward codeword is at distance three
from the opposite center; its three distance-two predecessors must all
fail to be sons, forcing three missing slots.  Therefore the centers are
at distance at least five even in the one-slack state.

### Weight classification

The local graph has independence number two.  A possible center has:

- no weight at most two, by the normalization and its seven-codeword
  neighborhood;
- weight three only when supported on a triangle of `H`, consuming the one
  extra local triangle slot;
- weight four at a cost of at least one missing family slot, because its
  non-orphan support contains a selected local edge and that weight-two
  codeword occupies the corresponding distance-two son position;
- no weight five with one unit of slack, because a supported local
  codeword is then at distance three and forces three predecessor slots
  missing; or
- weight six or seven without this local cost.

With two centers at distance at least five and total cost at most one, the
only possibility is a weight-three triangle `A` together with a weight-six
center `B`.  Their distance is at least five exactly when

$$
B=\{0,1,\ldots,6\}\setminus\{a\}
\quad\text{for some }a\in A.
$$

Branch 79 has three triangles, hence exactly nine exceptional ordered
pairs.  The zero-slack state is already impossible: both centers would
have weight at least six and hence mutual distance at most two.

`verify_branch79_split.py` independently reconstructs all 115 local-graph
orbits, the integer frontier, the independence number, and an exhaustive
128-vertex check that these are precisely the nine exceptional pairs.

## Exact finite split

For `D>=25`, the strong formula imposes

$$
p\geq49,\qquad a\geq20,\qquad b\leq9,
\qquad e(Q_7[C])\leq E_7(9)=13,
$$

together with `p+b<=58`.  The nine exceptional formulas use the valid
`D>=24` bounds `p>=48`, `b<=10`, `p+b<=58`, and
`e(Q_7[C])<=E_7(10)=15`, then fix each center to be a noncodeword and all
fourteen center-neighbors to be codewords.  These are relaxations of the
corresponding family cases, so their unsatisfiability is sufficient.

All formulas contain exact domination and distance-two separation, exact
cardinality 29, the complete orphan normalization, all 15 local-graph
units, and biconditional indicators.  The strong formula has 10,432
variables and 183,619 clauses; each exceptional formula has the same
variables and 183,635 clauses.

CaDiCaL 1.5.3 emitted plain-text DRAT traces.  DRAT-trim
`0.0~git20240428.effa1dc-2` returned `s VERIFIED` on all ten pairs, with
zero RAT lemmas in every core.  PySAT's Kissat 4.0.4 binding independently
returned UNSAT on freshly regenerated formulas.

| formula | CNF SHA-256 | proof bytes | DRAT SHA-256 | core/total lemmas |
|:---|:---|---:|:---|---:|
| `d25` | `8602da5601d1d76a2d9b87c97eaaa873b226fdc5fee9c33a3eec48fc6263f4c7` | 138,059,301 | `b4e36efe205ff8ba1d9109a6702ffb3b02d9ecf67c13fa0b3454abcf560b6f91` | 569,184/930,026 |
| `f50-g111` | `e82f5f76a760c0ddda7d4661dc6dbe1f2b25afd080c7b17d7cf157a1f3e4f66a` | 812,790 | `2916e6366dc86b692877a816f9456ddbb9916b72664334145fed5b26d1e53715` | 1,129/11,917 |
| `f50-g125` | `819299c5c3037940085e6a3b3532c58ca15d8f07c912af0b7cd561591e5acdca` | 783,632 | `15ed38acac84e1f910d6267bfc1710f827620a5cca9b22275ba38d9e488e2974` | 1,207/11,819 |
| `f50-g95` | `be9fb55033aebb4bc3459794c7cc9ed89f4618200fffe440babbd4c1ee236c80` | 778,641 | `91622b907114edf4b69fba834e1937e4a2608c105d9414b1401ee3dfe98479c0` | 1,259/11,703 |
| `f56-g111` | `b057d94ecb7f251a24407072f87fc07bfdd2710a34232f5588f34f051dbc8c51` | 821,355 | `8e5d594bc3e5a812b45b792ceeeb79dbbc2e763aa07175f7462882d367324f70` | 1,120/12,287 |
| `f56-g119` | `0bfa2b9f9ffaaeb2f3c824d701dd5eca797a4fc0f466f4bc75ed396cbf05f29c` | 827,011 | `6692f09b02b1877728fc6dcb7a6beba5092ad60fdbb2089c5c76ada55fa766e9` | 1,699/12,428 |
| `f56-g95` | `12011f5b20655aec332d162e6e72d4eacbc1efb02fe9f66b88bc5bc999784ba1` | 1,123,418 | `9c17defb4c8762a9d67b715afa14321a6c6a0028832019c2de3e8556c866d7b9` | 2,123/16,652 |
| `f70-g123` | `7991caaaf93d46d6f8a840d61e1a6a418bf23b5edf1fc84f437397125fb716b9` | 801,306 | `b64a59168d342aee75ff71e807645801413ce0ea1feb04b03f99c220a218234e` | 1,398/12,051 |
| `f70-g125` | `eaf57ddda6b7529d74ad180224437c52dc95bc21f0d7501a246683cf41712907` | 810,458 | `2801d1115f4d0558668f39b8a3a70c7dafd59992eef23299723e7d429dde7261` | 1,283/12,089 |
| `f70-g63` | `97616bacb9eb75734c18117ef298a27ff7251fd9f51a41001aa06fcda49eca17` | 741,486 | `8a96f2d86e327d0a1f182fb988e8f1ed964cd5456e354c98def32dca3fc5f0bb` | 734/11,271 |

The strong checker core used 30,250,388 resolution steps.  The exceptional
cores used between 28,469 and 90,302 steps.

## Reproduction

```bash
python3 -m venv /scratch/q7-ld29-branch79-split-venv
/scratch/q7-ld29-branch79-split-venv/bin/pip install -r requirements.txt
/scratch/q7-ld29-branch79-split-venv/bin/python \
  verify_branch79_split.py \
  --write-directory /scratch/q7-ld29-branch79-split
```

For every generated CNF:

```bash
cadical -q --binary=false FORMULA.cnf FORMULA.drat
drat-trim FORMULA.cnf FORMULA.drat -w
```

Run the independent solver cross-check with

```bash
/scratch/q7-ld29-branch79-split-venv/bin/python \
  verify_branch79_split.py --solve-kissat
```

Reported environment and hashes:

```text
Python                         3.11.2
python-sat[pblib]              1.9.dev15
CaDiCaL Debian package         1.5.3-2
CaDiCaL package SHA-256        ad30fec9e44fc6d7df39ba88efdd3f132bff24a4a6d422e26c73cc2cabbde1b3
DRAT-trim Debian package       0.0~git20240428.effa1dc-2
DRAT-trim package SHA-256      a2613ed11f3b2ee1a183ed64ba265a7d88b9b892cef1a40a9097132ccabcc31f
requirements.txt SHA-256       639afc203e4b12224d62c9426902d5784099ba876c5ac2faed92e4659b56caca
verify_branch79_split.py SHA-256 ea313ef366ad3b2da6c4e43d721aef8e96ec9bfa7dafe18c8fdade61c5fdd687
```

CNFs, traces, and checker logs remain under `/scratch` and are not
committed.

## Trust boundary and novelty

The analytic split depends on the Honkala--Laihonen--Ranto family
partition, the reviewed orphan-local reduction, the preceding branchwise
`D>=24` theorem, and elementary cube geometry.  Its finite reduction is a
small transparent integer, graph, and 128-vertex enumeration.  The exact
exclusions add the deterministic encoding, PySAT totalizers, and DRAT-trim
to the trust boundary.  DRAT proves exactly the ten hashed formulas; the
analytic bridge is separate.

The family method is from Honkala--Laihonen--Ranto, DMTCS 6(2) (2004),
<https://doi.org/10.46298/dmtcs.322>.  Junnila--Laihonen--Lehtila, DCC 90
(2022), <https://doi.org/10.1007/s10623-021-00963-8>, records the prior
small-dimension interval `28 <= gamma^LD(Q_7) <= 32`.  Targeted
primary-source and Discovery Net searches through 2026-09-01 found no
full-family center split or exact certificate for branch 79.  The result is
apparently new to the searched sources; no historical-priority claim is
made.
