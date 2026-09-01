# Full-family split and DRAT exclusion of `Q_7` LD29 branch 81

## Certified result

There is no locating-dominating code of cardinality at most 29 in the
binary 7-cube whose lossless orphan normalization has canonical local-graph
index 81.  Its mask is `6010`, sorted degree sequence
`(2,3,3,3,3,4)`, triangle count three, and independence number two.

This generalizes the branch-79 full-family reduction to a nonisomorphic
local graph.  The proof consists of the same hand-checkable exhaustive
split plus ten newly generated and independently checked DRAT certificates.

## Complete family-defect split

For an exact 29-word code in branch 81, the leaf-aware theorem gives total
Honkala--Laihonen--Ranto family defect `D>=24`.  The local fathers use 12
defect units, have capacity 43, and force 24 missing son slots.  Exact
capacity enumeration and the defect-six occupancy bound leave at `D=24`
only

```text
q=5, extra defects=(1,1,5,5), free missing=1, family-codeword budget=0;
q=5, extra defects=(2,5,5),   free missing=0, family-codeword budget=0.
```

Thus there are two noncodeword defect-five centers, each with seven
codeword neighbors, and at most one further missing slot.

As proved by the generic split kernel, the centers must be at distance at
least five.  Distances two and three force one missing slot in each family;
distance four makes a codeword at distance three force three predecessor
slots missing.  Since the local graph has independence number two, the
one-slack weight classification permits only a weight-three triangle center
`A` and the weight-six center

$$
\{0,\ldots,6\}\setminus\{a\},\qquad a\in A.
$$

Branch 81 has three triangles, so this yields exactly nine exceptional
ordered pairs:

```text
(42,125) (42,119) (42,95)
(28,123) (28,119) (28,111)
(56,119) (56,111) (56,95)
```

The integers are seven-bit cube vertices.  The zero-slack state is
impossible because both centers would have weight at least six and mutual
distance at most two.

The adapter `verify_branch81_split.py` invokes the reusable, digest-pinned
kernel in `q7_ld29_branch79_split`.  It reconstructs the local graph,
integer frontier, and exhaustive 128-vertex center classification before
generating any formula.

## Checked finite certificates

The strong formula covers `D>=25` with `p>=49`, `b<=9`, `p+b<=58`, and
`e(Q_7[C])<=13`.  Each exceptional formula uses the valid `D>=24` bounds
`p>=48`, `b<=10`, `p+b<=58`, and `e(Q_7[C])<=15`, then fixes its centers
absent and their fourteen neighbors present.  Each is a relaxation of the
corresponding family case.

Every formula contains exact domination and distance-two separation,
cardinality 29, the complete orphan normalization, all local-graph units,
and biconditional count indicators.  The strong formula has 10,432
variables and 183,619 clauses; each exceptional formula has 183,635
clauses.

CaDiCaL 1.5.3 emitted plain-text DRAT traces.  DRAT-trim
`0.0~git20240428.effa1dc-2` returned `s VERIFIED` on all ten pairs, with
zero RAT lemmas.  Kissat 4.0.4 independently returned UNSAT on every
freshly regenerated formula.

| formula | CNF SHA-256 | proof bytes | DRAT SHA-256 | core/total lemmas |
|:---|:---|---:|:---|---:|
| `d25` | `e87f121853c895100ba83341e78cda9e171df76881b6b8c2e552ce77e2581f4c` | 206,776,102 | `8d272f6e74e971b7abc48ebbb27a7889d31c69d7a42c2f1bcd618d838681b3c9` | 744,898/1,210,080 |
| `f28-g111` | `94f8d621409f63fdaa9679bf1a64b8b67991fd40ff99fde962d23c7b4cbaed8a` | 817,071 | `3e2c6d70985067a5f3390aa8d80d558d331b28e7ad7c0781c3469f7606e44e59` | 1,444/12,780 |
| `f28-g119` | `7fd8a821efae7a84041896174c21be35154ddd855d642bf9ae23239c67009184` | 788,206 | `bc65a924b1d3da685826ed7a35b726d2eb51885ba3be206654b014143cd18e87` | 1,084/11,836 |
| `f28-g123` | `55e5dfdf219d45a150f61fb4a412cf932105e5269964dcda88bfd3fdfb2203f6` | 771,762 | `19a01b0121732dafb9c46f5765b7b7ab613ed0d3831531bbbe71477640758901` | 1,013/12,059 |
| `f42-g119` | `3ac7583d62653c75fea155e73f5404396245e9504d270714732bd1bb49cede89` | 786,986 | `18c04088e0e84ca8790b39c860c475c306b11b58a59988f47122ca8e9a590f97` | 982/11,727 |
| `f42-g125` | `9086a9b408fe92d9e061023a775c63ffdde8691a89b2df5ad84f44705b307419` | 754,599 | `f86300674d42418bc3b60eb1d28594c012277881a7cd8c22e73bde59a2245482` | 935/11,376 |
| `f42-g95` | `d824636ab88236f92dc1b8a2258da45d0f50b55a66c5a568127293b2226c524a` | 827,788 | `7a0bd1cb9c44b5b583665eaaba396f9dcdfbc56cfab9ee9e4571d07f73cfc0c3` | 1,023/12,562 |
| `f56-g111` | `c8ccc85d927b36fa7ff3d7b574a63ac704690f8143698175dba1ff302fe35f52` | 984,419 | `76d3fabc4295f195a7254d5da8b28c16feb0f4d86e412b380f4bc530ebdfc887` | 2,543/14,573 |
| `f56-g119` | `ac0555d79944e44fe18eee0eeef82102c43009b5335c5822bd134c36675b1659` | 832,153 | `3a339cc17bf7d2a585bec801ad14563ba1a1ea189362b87d40fb5e2ba97d7f33` | 1,352/12,713 |
| `f56-g95` | `389b5d07ef8576cb05a71e73f1d46624ece2fd783ef18b43d83853d1d1ef3a2b` | 788,099 | `26eb4182bc84fbe9c6dbfdb9646925e6a66a9afb4516ed90bc6494855ad159cd` | 964/11,921 |

The strong core used 41,512,816 resolution steps; the exceptional cores
used between 31,232 and 106,660.

## Reproduction

```bash
python3 -m venv /scratch/q7-ld29-branch81-split-venv
/scratch/q7-ld29-branch81-split-venv/bin/pip install -r requirements.txt
/scratch/q7-ld29-branch81-split-venv/bin/python \
  verify_branch81_split.py \
  --write-directory /scratch/q7-ld29-branch81-split
```

For every generated CNF, run

```bash
cadical -q --binary=false FORMULA.cnf FORMULA.drat
drat-trim FORMULA.cnf FORMULA.drat -w
```

The independent solve is

```bash
/scratch/q7-ld29-branch81-split-venv/bin/python \
  verify_branch81_split.py --solve-kissat
```

Reported environment and hashes:

```text
Python                          3.11.2
python-sat[pblib]               1.9.dev15
CaDiCaL Debian package          1.5.3-2
CaDiCaL package SHA-256         ad30fec9e44fc6d7df39ba88efdd3f132bff24a4a6d422e26c73cc2cabbde1b3
DRAT-trim Debian package        0.0~git20240428.effa1dc-2
DRAT-trim package SHA-256       a2613ed11f3b2ee1a183ed64ba265a7d88b9b892cef1a40a9097132ccabcc31f
requirements.txt SHA-256        639afc203e4b12224d62c9426902d5784099ba876c5ac2faed92e4659b56caca
verify_branch81_split.py SHA-256 dcef5b510ff993303a44dad3d6d4c771644c6aa30a28461d31d023a7f1766527
```

CNFs, traces, and checker logs remain under `/scratch` and are not
committed.

## Trust boundary and novelty

The proof depends on the reviewed family/orphan reduction, the branchwise
`D>=24` theorem, the full-family split kernel, elementary cube geometry,
the deterministic encoding, PySAT totalizers, and DRAT-trim.  DRAT proves
exactly the ten hashed CNFs; the analytic bridge is separate.

The family method is from Honkala--Laihonen--Ranto, DMTCS 6(2) (2004),
<https://doi.org/10.46298/dmtcs.322>.  Junnila--Laihonen--Lehtila, DCC 90
(2022), <https://doi.org/10.1007/s10623-021-00963-8>, records the prior
interval `28 <= gamma^LD(Q_7) <= 32`.  Targeted primary-source and refreshed
committed-graph searches through 2026-09-01 found no such split or exact
certificate for branch 81.  The result is apparently new to the searched
sources; no historical-priority claim is made.
