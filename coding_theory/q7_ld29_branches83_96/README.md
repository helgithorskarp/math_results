# Local family-collision bounds and closure of the 10-edge `Q_7` LD29 frontier

## Result

There is no locating-dominating code of cardinality at most 29 in the
binary 7-cube whose lossless orphan normalization has canonical local-graph
index 83 through 96.  These are all 14 admissible ten-edge graphs.

Together with the checked closure of branches 97--114, every hypothetical
code of cardinality at most 29 now lies in exactly one of the 83 branches
0--82, each having between 4 and 9 local edges.  This remains a lossless
finite reduction, not a proof that a 29-word code is impossible.

The new analytic input extends the local family-collision method from the
11-edge frontier.  It proves

$$
D\geq25
$$

for every exact 29-word code in branches 83--96, and the sharper

$$
D\geq26
$$

in branch 89.  Fathers of defect six are allowed, so these statements hold
for arbitrary exact 29-codes, including augmentations of hypothetical
smaller codes.

Consequently, branches other than 89 satisfy

$$
p\geq49,\qquad a\geq20,\qquad b\leq9,
\qquad e(Q_7[C])\leq E_7(9)=13,
$$

while branch 89 satisfies the sharper bounds `p>=50`, `a>=21`, `b<=8`, and
`e(Q_7[C])<=E_7(8)=12`.  Exact SAT formulas with these consequences are
UNSAT in all 14 branches, with checked DRAT certificates.

## Local fathers, leaves, and forced son-slot deficit

Retain the predecessor normalization

```text
0 in C;
e_i not in C                         (0 <= i < 7);
e_0+e_j not in C                     (1 <= j < 7).
```

Let `H` be the local graph on directions `1,...,6`, with `ij` selected when
`e_i+e_j` is a codeword.  A direction of degree at least two gives a father
`e_i` of defect `deg_H(i)-1`.  A degree-one direction gives a son: the local
admissibility condition excludes a two-vertex component, so its unique
neighbor is a father and its two-element identifying set lies in that
father's identifying set.

For every ten-edge branch 83--96, the local fathers use exactly 14 defect
units.  With `F={i:deg_H(i)>=2}`, their total capacity is

$$
L=\sum_{i\in F}\left(1+\binom{\deg_H(i)+1}{2}\right).
$$

Let `Delta` be the total absent-son capacity.  Each edge of `H[F]` forces
two absent oriented slots: the other common neighbor is another father.
An edge to a degree-one direction does not force a slot, because that leaf
is the corresponding son.  Every local triangle forces two further absent
slots, exactly as in the 11-edge argument.  Hence

$$
\Delta\geq2|E(H[F])|+2t(H).
$$

The standard-library verifier reconstructs these exact canonical data.

| branch | mask | sorted degrees | triangles | `L` | forced `Delta` | defect bound |
|---:|---:|:---|---:|---:|---:|---:|
| 83 | 1023 | `(2,2,3,3,5,5)` | 6 | 54 | 32 | 25 |
| 84 | 1791 | `(1,3,3,4,4,5)` | 7 | 52 | 32 | 25 |
| 85 | 1919 | `(2,2,3,4,4,5)` | 6 | 53 | 32 | 25 |
| 86 | 2015 | `(2,3,3,3,4,5)` | 5 | 52 | 30 | 25 |
| 87 | 2046 | `(2,3,3,4,4,4)` | 4 | 51 | 28 | 25 |
| 88 | 4061 | `(3,3,3,3,4,4)` | 3 | 50 | 26 | 25 |
| 89 | 5879 | `(1,3,4,4,4,4)` | 7 | 51 | 32 | 26 |
| 90 | 5951 | `(2,3,3,3,4,5)` | 6 | 52 | 32 | 25 |
| 91 | 6007 | `(2,2,4,4,4,4)` | 6 | 52 | 32 | 25 |
| 92 | 6011 | `(2,3,3,4,4,4)` | 5 | 51 | 30 | 25 |
| 93 | 6014 | `(2,3,3,4,4,4)` | 5 | 51 | 30 | 25 |
| 94 | 6654 | `(3,3,3,3,4,4)` | 4 | 50 | 28 | 25 |
| 95 | 7071 | `(3,3,3,3,3,5)` | 5 | 51 | 30 | 25 |
| 96 | 7101 | `(3,3,3,3,4,4)` | 4 | 50 | 28 | 25 |

## Capacity contradiction

For any exact 29-code, the family identities are

$$
p=24+D,\qquad M=104-D-2q,
\qquad a\geq D-5,qquad 2q\leq34-D.
$$

A general father has defect at most six and capacity

```text
d       1   2   3   4   5   6
h(d)    4   7  11  16  22  29.
```

Let `G(r)` be the maximum capacity from `r` additional defect units.  If
`D<=24`, then `r=D-14<=10`.  Exact dynamic programming, using the largest
possible `q` to minimize `M`, gives

$$
G(D-14)-M\leq-25.
$$

Thus `Delta<=L-25`, but every row in the table forces at least `L-24`, a
contradiction.  Therefore `D>=25` in all 14 branches.

For branch 89 at `D=25`, one has `G(11)=51`, `q<=4`, and `M>=71`, so
`Delta<=L-20=31`; the local geometry forces 32.  Hence branch 89 has
`D>=26`.

The displayed consequences follow from `p=24+D`, `a>=D-5`, and the binary
edge-isoperimetric recurrence.  `verify_local_defect25.py` independently
reconstructs the 115 graph orbits, all table entries, every capacity case,
and `E_7(9)=13`, `E_7(8)=12` using only the Python standard library.

## Exact formulas and certificates

Each formula contains exact domination and distance-two separation,
cardinality 29, the orphan normalization, all 15 local units, biconditional
indicators, `p+b<=58`, and the branch's proved singleton, nonisolation, and
induced-edge bounds.  Repeated literals are removed clausewise.

Every cleaned formula has 10,432 variables, 183,619 clauses, and 3,433,597
bytes.  CaDiCaL 1.5.3 emitted a plain-text DRAT proof for each exact CNF;
DRAT-trim `0.0~git20240428.effa1dc-2` returned `s VERIFIED` on all 14 pairs.
No checked core uses a RAT lemma.  PySAT's Kissat 4.0.4 binding independently
returned UNSAT in every branch.

| branch | CNF SHA-256 | proof bytes | DRAT SHA-256 | core lemmas |
|---:|:---|---:|:---|---:|
| 83 | `752930d0052e755230c08abcbfcfe42738fc431200a344d89b618d52dd4132d3` | 59,722,039 | `c63fa035717c7ab6bf8bd8b27b92df3192c28cd6813f04ba572901bfb6f6062a` | 240,691 |
| 84 | `7f943b89342dcddad4a95a150c7a2bf8bfbf353ff6250cf287a9dca8b5ca8885` | 111,091,636 | `9fe1585ca53a155da22c1914c2a608ef10c423351b4221461aea91992a3eccc5` | 397,836 |
| 85 | `bc17d469ed940c8505b0036de40a9f5ca1286c2bf7e13c45de0d21ff64093621` | 99,399,366 | `4975995fc8c92c14c33b3788660c76e18babb3c9e2759ecc1781578e000bfd20` | 375,929 |
| 86 | `68439ebdc0fad1ec9bc679d97712039154b321ae8ef9c92aea2a72d085b79a3c` | 90,278,985 | `90e29fbb37178994731c62085d0c5e86a228e373ba868a99e57f070afef4c029` | 402,107 |
| 87 | `4c4811e22fb9efaa6feeec11d527378aee48a096c88de8089209a1eac7365dce` | 63,109,782 | `1a351a92139bf7067cc69aae8e42bf29a4a1b9e642240f5e17fe3e1b341affaf` | 248,433 |
| 88 | `841d1b78387c1c8ed113a60c6dce30978773c1d461b35671084241036b4bb695` | 76,477,724 | `6f9ca71a47227a72682a96c2f453382375c05c0c236c9f0cb625c9ebdfb3a9c7` | 330,266 |
| 89 | `91a65e9aea9e0ff8f4d55ccf5a9f037d4095c2c5a6d8447153ba8275f097a392` | 27,638,272 | `536e234c96aeeb967f7fa487a466f33ac4e2cea66128b61709cb782c78bada9c` | 80,025 |
| 90 | `475476f0704a2598b26eb44d062f44e185940c677580971e8d2ee2551de275a1` | 85,224,339 | `eb6ce9f1228a6963e7700bd50d46b270e326efb2f33919661147f788fb39cd1b` | 291,931 |
| 91 | `b3e87d09cab27bd4ccca1b682ecb5159c3f2b654a2f98853a244a799f3a6691b` | 79,934,871 | `250d03f9cadc9295d81d9015606c6045b6320c6980f1a9c9d0c12e6974259240` | 283,009 |
| 92 | `bc73dded850505fbac488d086b5bd01516a99b20d4ccb51710b7b6fdca62e5ff` | 74,077,626 | `963cf02e91621284b3269502a5fdaa116268753398e61833dd3e4d1fdda4d5d7` | 295,562 |
| 93 | `0f6bf0edf4529168968fa6bb18447fd0da6da75083ce7fc1b40a16354a5c99d5` | 76,431,463 | `7adf9cc37c94e37f18eecf05885393b6407ef4ce1c04414e0c5317d85022224e` | 285,512 |
| 94 | `03a2f4116cee54b7741b2e20cecc08dbb6fa873217be0de4f084fb91b75210be` | 39,395,937 | `afbd66e3b29455f14f52b541e587a797f851b955a46b6ed70bf763964383e8d7` | 149,083 |
| 95 | `846625701f72bfb910c1e306f266515e303287e32f1f0b1109c13071e2be8af7` | 95,365,433 | `beebc9254911f3c3a2c223c5ad48ad1877c74dc16c8a75c93f27df3b86fff55a` | 377,191 |
| 96 | `41df9c0b6a874a2494dc1e43086baff6980cf773bb2ec84865a98e9b0a99916c` | 80,276,171 | `0b5216a5dd54a4640502e598987dbcf3972d46cce2996c089a537f4022c088cd` | 334,743 |

The CNFs, roughly 1.0 GB of proof traces, and checker output stay under
`/scratch` and are deliberately not committed.

## Reproduction

```bash
python3 verify_local_defect25.py

python3 -m venv /scratch/q7-ld29-d25-venv
/scratch/q7-ld29-d25-venv/bin/pip install -r requirements.txt
/scratch/q7-ld29-d25-venv/bin/python verify_branches83_96.py \
  --write-directory /scratch/q7-ld29-d25-cnfs
```

For each `b` in `83,...,96`:

```bash
cadical -q --binary=false \
  /scratch/q7-ld29-d25-cnfs/branch-${b}.cnf \
  /scratch/q7-ld29-d25-branch-${b}.drat

drat-trim \
  /scratch/q7-ld29-d25-cnfs/branch-${b}.cnf \
  /scratch/q7-ld29-d25-branch-${b}.drat -w
```

The reported environment used Python 3.11.2,
`python-sat[pblib]==1.9.dev15`, CaDiCaL 1.5.3, DRAT-trim
`0.0~git20240428.effa1dc-2`, and the Kissat 4.0.4 PySAT binding.

## Trust boundary and novelty

The hand theorem depends on the Honkala--Laihonen--Ranto family partition,
elementary cube geometry, and the finite capacity calculation.  The finite
exclusions additionally depend on the reviewed orphan-local reduction, the
deterministic exact encoding, PySAT cardinality encodings, and DRAT-trim.
DRAT proves only the 14 hashed formulas; the analytic bridge is separate.

The family method is from Honkala--Laihonen--Ranto, DMTCS 6(2) (2004),
<https://doi.org/10.46298/dmtcs.322>.  Junnila--Laihonen--Lehtila, DCC 90
(2022), <https://doi.org/10.1007/s10623-021-00963-8>, gives
`28 <= gamma^LD(Q_7) <= 32` and improves lower bounds only from dimension
ten.  Targeted primary-source and graph searches through 2026-09-01 found
no local leaf-aware collision bound or certificates for these 14 branches.
The results are apparently new to the searched sources; no historical
priority claim is made.
