# One-slack full-family split for `Q_7` LD29 branches 61 and 62

## Certified result

Every locating-dominating code of cardinality at most 29 in the binary
7-cube whose lossless orphan normalization has canonical local-graph index
61 or 62 has total Honkala--Laihonen--Ranto family defect

$$
\boxed{D\geq24}.
$$

The two branches have canonical masks `5941` and `5948`.  Both local graphs
have sorted degree sequence `(2,2,3,3,3,3)`, two triangles, and independence
number two.  The proof combines a hand-checkable full-family reduction with
twelve exact DRAT certificates, six for each branch.  It improves the
preceding branchwise bound `D>=23`; it does **not** exclude either branch.

## Defect-23 full-family reduction

Let `C` be an exact 29-word locating-dominating code after the established
lossless normalization

```text
0 in C;
e_i not in C                         (0 <= i < 7);
e_0+e_j not in C                     (1 <= j < 7).
```

Let `H` be the local graph on directions `1,...,6`, with `ij` selected
exactly when `e_i+e_j` is a codeword.  The preceding lower-frontier ladder
gives `D>=23` in branches 61 and 62.  In either graph the local fathers use
ten defect units, have capacity 36, and force 20 distinct missing son slots.
For `q` codeword couples, `M` family vertices, `p` singleton signatures, and
`a` isolated codewords, the standard identities are

$$
p=24+D,\qquad M=104-D-2q,\qquad
a\geq D-5,\qquad 2q\leq34-D.
$$

At `D=23`, exact integer-partition enumeration and the defect-six occupancy
inequality leave only

| `q` | extra family defects | free missing slots | family-codeword budget |
|---:|:---|---:|---:|
| 5 | `(1,1,1,5,5)` | 1 | 1 |
| 5 | `(1,2,5,5)` | 0 | 1 |
| 5 | `(3,5,5)` | 0 | 1 |

Every row has two defect-five families.  Their fathers are noncodewords: even
with the one available missing slot, a selected defect-five father would put
at least six codewords in its family, exceeding the displayed budget one.
Thus all seven neighbors of each father are codewords.

### Separation and center costs

The two centers have mutual distance at least five.  At distances one, two,
three, or four, respectively, the full-family conditions force a center to
be a codeword, consume a missing slot in each family, again consume two
slots through the inward neighbors, or consume at least three predecessor
slots.  None is compatible with total slack at most one.

The normalization and the independence number two give the following
exhaustive cost classification for a center, where cost counts missing slots
beyond the 20 already forced locally:

- weights at most two are impossible;
- weight three is possible only on a triangle of `H`, at cost one;
- weight four costs the number of supported selected local edges, hence at
  least one;
- weight five costs at least three; and
- weights six and seven have local cost zero.

In either zero-slack row both centers would have weight at least six, so their
distance would be at most two.  In the one-slack row, two centers of total
cost at most one and distance at least five can only be a weight-three
triangle `A` and the weight-six set

$$
\{0,1,\ldots,6\}\setminus\{a\}\quad(a\in A).
$$

Each local graph has two triangles and hence exactly six exceptional pairs.
`verify_branches61_62_split.py` pins the reviewed predecessor verifiers,
reconstructs all 115 local-graph orbits, enumerates the arithmetic states,
and checks all 128 possible centers to prove that this list is exhaustive.

## Exact exceptional split

At `D=23` the family bounds give

$$
p\geq47,\qquad a\geq18,\qquad b=29-a\leq11,
\qquad e(Q_7[C])\leq E_7(11)=17,
$$

together with `p+b<=58`.  For every exceptional pair, the exact formula
imposes these consequences and fixes both centers outside `C` and all their
fourteen neighbors inside `C`.  These constraints are relaxations of the
corresponding full-family cases, so UNSAT excludes every surviving `D=23`
configuration.

Every formula contains exact domination and distance-two separation,
cardinality 29, the complete orphan normalization, all 15 local-graph units,
and biconditional singleton, nonisolation, and code-pair indicators.  Each
has 10,432 variables and 183,635 clauses.  CaDiCaL `sc2021` emitted the DRAT
traces below.  DRAT-trim returned `s VERIFIED` with zero RAT lemmas for all
twelve formula/proof pairs.  PySAT's Kissat 4.0.4 binding independently
returned UNSAT on freshly regenerated formulas.

| branch/pair | CNF SHA-256 | proof bytes | DRAT SHA-256 | core/total lemmas | resolution steps |
|:---|:---|---:|:---|---:|---:|
| 61 `f70-g125` | `f4e6e3063025e380c1d8e4bdb8b4011a7e654de593939893a82dad0d3df984b4` | 1,069,957 | `60aed9e7bd01a7cf4a8f036f6b7716cb9ecca6fdd689341face532ab4a05c359` | 3,165/16,372 | 129,964 |
| 61 `f70-g123` | `a58f7e922b0e69805aeeb3b6160592a2c5388e9b9f8cdac787b6efc944e87214` | 988,099 | `071b0c16e29e8dea9cc2cc303dfa00ea35991194333b3f6c8d487f3def0987d5` | 3,280/14,508 | 148,293 |
| 61 `f70-g63` | `6e0e1af9fac6bcd2ef0911609a6f4ca10455980ca763a625b899383bc619f62e` | 815,712 | `be360fcafe9db2a11383467edc759a665bc81511e18bf7541eef7053e1df01a0` | 1,370/12,319 | 50,275 |
| 61 `f56-g119` | `2bac9b66ec4c38169bcf8a6cd584995b72fef5a676365ae7a2d0a00b152990db` | 1,097,501 | `c80384edd981c1fd577f1c67603a6c17ad8390cf93da2e07f40616fd1f87df2d` | 3,486/16,177 | 150,508 |
| 61 `f56-g111` | `a7473865e1ba903ef7869c023a154cb1fdc2b8c585bfde60207d8a9a7edc4967` | 1,031,296 | `3e29046121de6b2afc6c220e26d21f9ff20cb00f49598fd87361e2a8fb7d1f3c` | 3,007/15,713 | 120,377 |
| 61 `f56-g95` | `df24f5951951af7d3b43b0b6f04fb03bb0d50ab02f5c6b1744fa1bedb314f781` | 1,127,337 | `cabcac4eda3ae93f797efd068a0a39264f6f0b71de53d32e88b1a2a2c85cc9c9` | 1,710/15,880 | 58,382 |
| 62 `f50-g125` | `d1b9c55ae2aec498a52001bac3a58a8d9557e71f22a17d4183d7bac7962fd224` | 2,072,146 | `de3ae8455e5e3c2c538319b61a79916a617310bc61aa1231d67b47fdb79a5f74` | 4,072/40,883 | 173,005 |
| 62 `f50-g111` | `7bc7711344341e7d03623b756aec50d4120663b3b483ccab30b7cb83986f30c5` | 1,054,783 | `9d60df0cb6d69898736bcfeca329e36fefed65e4abdcb4bda451dfcb5a6785c3` | 2,133/15,740 | 80,292 |
| 62 `f50-g95` | `fc679ae0eb673785bbb719aab4b0822bc65b13ba1a136f985835697d98057427` | 914,284 | `70db2870184cb97f4ee0b8612126d3114efda6803d204f964726cc2d95e56e07` | 2,682/14,011 | 112,976 |
| 62 `f56-g119` | `54997ab8189fa936ada28908449e21d238e1773fc342190ea0e58ce6e808aada` | 1,361,150 | `0934546fbe30866769635ec57f802d57a644613082f6e276dddbe089dba6d7a0` | 4,249/40,044 | 170,107 |
| 62 `f56-g111` | `49367548736f044fe39af17af681fc28b59f9ef9a391e5e97a444dcca9a77230` | 1,903,848 | `1949cd4d1e4a5fe11a786b6d78122d4c3d6483bd7afb67110e90032936167b56` | 4,565/46,718 | 197,602 |
| 62 `f56-g95` | `576548f3b467c5e8832d55d00f2d92c6115b37c3008c216a51917c77b2fb0fe1` | 933,194 | `662051cc93b3efc6bbfaf66f469394cd9deb85200aefbf27507e10b0b3f8ad2f` | 2,766/14,129 | 108,077 |

## Reproduction

Create the environment under `/scratch` and regenerate all twelve formulas:

```bash
python3 -m venv /scratch/q7-ld29-branches61-62-venv
/scratch/q7-ld29-branches61-62-venv/bin/pip install -r requirements.txt
/scratch/q7-ld29-branches61-62-venv/bin/python \
  verify_branches61_62_split.py \
  --write-directory /scratch/q7-ld29-branches61-62
```

For every generated CNF, produce and check the external certificate:

```bash
cadical -q --binary=false FORMULA.cnf FORMULA.drat
drat-trim FORMULA.cnf FORMULA.drat -w
```

Run the independent solver cross-check with

```bash
/scratch/q7-ld29-branches61-62-venv/bin/python \
  verify_branches61_62_split.py --solve-kissat
```

Reported environment and hashes:

```text
Python                                      3.11.2
python-sat[pblib]                           1.9.dev15
CaDiCaL                                     sc2021
CaDiCaL executable SHA-256                  c6de62662723ec4a7426c5ca2bc9bfb04c60aad81a423957e3cd1ffadd0f8aa7
DRAT-trim Debian package                    0.0~git20240428.effa1dc-2
DRAT-trim executable SHA-256                bc7543a99da8521ddb09af442698956054f11e10d198bd482ac756535244c021
requirements.txt SHA-256                    639afc203e4b12224d62c9426902d5784099ba876c5ac2faed92e4659b56caca
verify_lower_frontier_bounds.py SHA-256     acde98fb29c8673d57ceddc47b36e5b46a62a0cfa13ed542886e96fbaf0c4852
verify_branch79_split.py SHA-256            ea313ef366ad3b2da6c4e43d721aef8e96ec9bfa7dafe18c8fdade61c5fdd687
verify_branches61_62_split.py SHA-256        c91531e6cc12c993a2a59a8e83b2bcede8fba8fc50d4589eac415b28670456c9
```

CNFs, proof traces, solver output, and checker output remain under
`/scratch` and are not committed.

## Trust boundary, scope, and novelty

The analytic theorem depends on the Honkala--Laihonen--Ranto family
partition, the reviewed orphan-local reduction and defect ladder, and
elementary Hamming-cube geometry.  Its finite component is a transparent
enumeration of integer states, six-vertex graph invariants, and 128 center
positions.  The exact split additionally depends on the deterministic
encoding, PySAT totalizers, CaDiCaL proof production, and DRAT-trim.  DRAT
proves exactly the twelve hashed formulas; the analytic bridge is separate.

The family method is from I. Honkala, T. Laihonen, and S. Ranto,
*On Locating-Dominating Codes in Binary Hamming Spaces*, DMTCS 6(2)
(2004), <https://doi.org/10.46298/dmtcs.322>.  V. Junnila, T. Laihonen,
and T. Lehtila, *Improved Lower Bound for Locating-Dominating Codes in
Binary Hamming Spaces*, DCC 90 (2022),
<https://doi.org/10.1007/s10623-021-00963-8>, records the prior interval
`28 <= gamma^LD(Q_7) <= 32`.

Targeted primary-source and refreshed Discovery Net searches through
2026-09-01 found no one-slack full-family split or exact certificate for
these two local branches.  The result is apparently new to the searched
sources; no historical-priority claim is made.
