# Defect-5/defect-6 split and closure of four `Q_7` LD29 branches

## Certified result

There is no locating-dominating code of cardinality at most 29 in the binary
7-cube whose lossless orphan normalization has canonical local-graph index
44, 47, 52, or 57.  Together with the preceding branch closures, every
hypothetical code of cardinality at most 29 is now confined to the 54
branches

```text
0--43, 45--46, 48--49, 51, 53--56, or 58.
```

This closes four exact branches; it is not yet a proof that a 29-word code is
impossible.

## Exact finite reduction

Let `C` be an exact 29-word locating-dominating code in the binary 7-cube
after the established lossless orphan normalization

```text
0 in C;
e_i not in C                         (0 <= i < 7);
e_0+e_j not in C                     (1 <= j < 7).
```

Let `H` be the local graph on directions `1,...,6`, with `ij` selected
exactly when `e_i+e_j` is a codeword, and let

```text
D = sum_F (|I(f_F)|-2)
```

be the total Honkala--Laihonen--Ranto family defect.  This directory treats
the following four branches left alongside the already closed branch 50.

| branch | mask | degrees | triangles | stabilizer order |
|---:|---:|:---|---:|---:|
| 44 | 703 | `(1,2,2,3,3,5)` | 3 | 2 |
| 47 | 766 | `(1,2,3,3,3,4)` | 2 | 2 |
| 52 | 1751 | `(1,2,3,3,3,4)` | 2 | 2 |
| 57 | 1916 | `(2,2,3,3,3,3)` | 1 | 2 |

The predecessor proves `D>=24` in every row.  If instead `D>=25`, the
standard family identities and the binary edge-isoperimetric bound give

```text
p >= 49,  b <= 9,  p+b <= 58,  e(Q_7[C]) <= 13.
```

The first exact formula for each branch combines these consequences with
domination, all essential distance-two separation clauses, cardinality 29,
the full normalization, and all 15 local-graph units.

It remains to cover exact defect `D=24`, where `p=48`, `b<=10`, and the
induced code has at most 15 edges.

## Exact-`D=24` family split

Let `q` be the number of codeword couples.  After the 18 or 20 local forced
missing son slots have been charged, complete integer enumeration gives 187
states surviving the defect-six occupancy bound.  If `q=0`, exactly three
remain, identically in all four branches:

| `q` | extra family defects | free missing slots | family-codeword budget |
|---:|:---|---:|---:|
| 0 | `(1,1,1,5,6)` | 1 | 10 |
| 0 | `(1,2,5,6)` | 0 | 10 |
| 0 | `(3,5,6)` | 0 | 10 |

Every row has one defect-five family and one defect-six family.  A defect-six
father is a codeword whose entire closed neighborhood consists of codewords.
If the defect-five father were also a codeword, the two families would force
at least

```text
(7-t_5) + (8-t_6) = 15-(t_5+t_6) >= 14
```

family codewords, exceeding the budget ten.  Hence it is a noncodeword with
all seven neighbors in the code.

Write `x` for the defect-five center and `y` for the defect-six center.  They
have Hamming distance at least five.  Distance zero or one conflicts with
their selected statuses.  At distance two each center consumes a son slot in
the other family.  At distance three, three inward neighbors of `y` destroy
three defect-five slots; at distance four, a neighbor of `y` at distance
three from `x` destroys the three predecessor slots in the defect-five
family.  Every distance at most four therefore exceeds the one available
free slot.

## Local costs and complete selector cover

The predecessor classifies the residual local cost of a noncodeword
defect-five center.  A complementary defect-six cost is obtained as follows.
A weight-three word is a potential local son exactly when its support
contains a wedge of `H`.  After the oriented-edge and triangle deficits have
been charged, one slot remains for each such word.  If the word is in the
closed neighborhood of `y`, it is selected and cannot fill that slot.  The
number of wedge words in `N[y]` is therefore a lower bound on the defect-six
center's residual local cost.

Because `d(x,y)>=5`, the costs charged by the two centers are disjoint.  Their
sum is at most one.  If `q>=1`, one may instead select an induced codeword
couple.  Direct enumeration of all compatible cube edges and all compatible
ordered center pairs, followed by the exact stabilizer quotient, gives the
complete disjunction:

| branch | compatible couples | couple orbits | center pairs | center-pair orbits | total cases |
|---:|---:|---:|---:|---:|---:|
| 44 | 207 | 116 | 122 | 66 | 182 |
| 47 | 204 | 139 | 92 | 62 | 201 |
| 52 | 204 | 143 | 86 | 55 | 198 |
| 57 | 201 | 113 | 69 | 40 | 153 |

For each branch a single aggregate formula assigns a selector to every orbit
representative, makes the selector imply its defining literals, and requires
at least one selector.  Thus UNSAT of that formula excludes every exact
`D=24` code in the branch.

## Exact formulas and certificates

The eight formulas use the reviewed deterministic locating-domination
encoding and PySAT totalizers.  Standalone CaDiCaL `sc2021` returned
`s UNSATISFIABLE` and emitted a plain-text DRAT trace for every formula.

| formula | variables | clauses | CNF SHA-256 | proof bytes | DRAT SHA-256 |
|:---|---:|---:|:---|---:|:---|
| `branch44-d25` | 10,432 | 183,619 | `41d7ffcd93749c5f727b32c68c5e36903c316155ba332775a035222d0bda1189` | 501,071,554 | `19c05fe894ef8ff3fc26d9c97ab72a3f8a8b9bd10dbbb3031efe818ee1416971` |
| `branch44-d24-selector` | 11,510 | 195,325 | `43a34b04a342bf9e41e6f5ad83ac23ee94fa24330c724341f5301e70dbc55330` | 1,154,008,497 | `b718585fa701a3bdf62222fdc313a4c97397962f327b88c395f8d63549b873b4` |
| `branch47-d25` | 10,432 | 183,619 | `c381bdab0d5d58c467278ada5d94a228875e6fb0a9359f681867095ac77c09c1` | 361,795,851 | `0c82d6db2f2c977726e1e8db25ced6e06281d717ad6d1e9584f92d8d2090e0ca` |
| `branch47-d24-selector` | 11,529 | 195,583 | `4e7c73106185d02dbef17714af9e9e645bc254647b2efe682afbbbd3e552f3b5` | 1,055,666,335 | `8c9a90f4d6d3fd9dbc4f8e334d0abbf2ceb642a95a6302df14646c853f730d57` |
| `branch52-d25` | 10,432 | 183,619 | `d5d9e4545fd7a300d63685ccfbe587473c24bae09cb648c3dc26713e6bd18163` | 919,053,964 | `1b131cceb42bc8cc4fdb3f440e5fd5ab85b41c60eba2742fd228bfd209057b1e` |
| `branch52-d24-selector` | 11,526 | 195,527 | `54847e526cfdafa9e97477faf915486df2289e9b6e756ccb84c14008db81c434` | 1,614,465,015 | `21d91d3a624f91760336845d0618f7195607028aaa1852066852322261b2ba29` |
| `branch57-d25` | 10,432 | 183,619 | `e3e860254c7c5ea7b15184a5c575c31398bce9db0c1729d94a3f980e6c5b8a84` | 454,373,091 | `a70c4a9a8cf7a6b34e63efa660bb53b4fd7d11077bc919a7f1d1e4ff0b2c37e1` |
| `branch57-d24-selector` | 11,481 | 194,867 | `8335940367b109c3a3577a0d97e186859ee5ebed4ce77fc568fb12f051cf3c31` | 1,121,850,616 | `8b2a2f977a458891a555c76b868f0b2cf54081a9edeab7bc31a27385c4872d23` |

DRAT-trim returned `s VERIFIED` on all eight exact CNF/proof pairs.  Every
checked core has zero RAT lemmas.  In aggregate the cores contain 41,538
original clauses and 27,034,063 of 44,371,845 proof lemmas, checked through
1,324,508,230 resolution steps.  Consequently neither `D>=25` nor exact
`D=24` is possible in any of the four branches, proving the certified result.

PySAT's Kissat 4.0.4 binding independently returned UNSAT on the four
freshly generated `D>=25` formulas in 770.108, 516.415, 1,351.733, and
715.891 seconds for branches 44, 47, 52, and 57, respectively.  The compact
manifest records exact CNF sizes, proof hashes, checked-core counts, and
checker timings; all 7.18 GB of proof material remains under `/scratch`.

## Reproduction

Create the pinned environment under `/scratch`:

```bash
python3 -m venv /scratch/q7-ld29-sibling-closure-venv
/scratch/q7-ld29-sibling-closure-venv/bin/pip install -r requirements.txt
```

Reconstruct the arithmetic split, every orbit quotient, and all eight exact
formulas:

```bash
/scratch/q7-ld29-sibling-closure-venv/bin/python \
  verify_sibling_closures.py \
  --write-directory /scratch/q7-ld29-sibling-closure-cnfs
```

For each generated formula, produce and check the external proof under
`/scratch`:

```bash
cadical -q --binary=false FORMULA.cnf FORMULA.drat
drat-trim FORMULA.cnf FORMULA.drat -w
```

The optional solver cross-checks are

```bash
/scratch/q7-ld29-sibling-closure-venv/bin/python \
  verify_sibling_closures.py --solve-kissat

/scratch/q7-ld29-sibling-closure-venv/bin/python \
  verify_sibling_closures.py --solve-incrementally
```

All CNFs, traces, and solver/checker logs remain under `/scratch`; only the
deterministic generator, dependency pin, concise manifest, and this proof
description belong in version control.

Reported environment and source hashes:

```text
Python                                  3.11.2
python-sat[pblib]                       1.9.dev15
CaDiCaL proof producer                  sc2021
CaDiCaL executable SHA-256              c6de62662723ec4a7426c5ca2bc9bfb04c60aad81a423957e3cd1ffadd0f8aa7
DRAT-trim Debian package                0.0~git20240428.effa1dc-2
DRAT-trim executable SHA-256            bc7543a99da8521ddb09af442698956054f11e10d198bd482ac756535244c021
requirements.txt SHA-256                639afc203e4b12224d62c9426902d5784099ba876c5ac2faed92e4659b56caca
certificate_manifest.tsv SHA-256        c54a4007a8a48ff0ac97c0b674dc8890f8ae815ca1b7d7d7a51fa359721e4c8c
verify_five_branch_d24.py SHA-256        6cd1880178ab8ed330db4030459a0247fc6e13016e6cf8321bce8ec7ed0e6ada
local_graphs.py SHA-256                 35d187198ed332f64551a174096168f101adff309e0dfaf6d94f9ba6d360e1f4
search_q7_ld29.py SHA-256               3d4cc2bd966dbed2e4b585d3725dd37356487ad735eb008e55e730a7b9022614
verify_sibling_closures.py SHA-256       1069616e39ad4c39e46d0094f91c6e2a9efc13983229033add53cf5551ac4fe6
```

## Trust boundary

The hand bridge depends on the Honkala--Laihonen--Ranto family partition, the
reviewed orphan-local normalization, and the predecessor's certified
`D>=24` theorem.  Its finite component exhausts integer family states, cube
edges, cube centers, and the exact local-graph stabilizers.  The Boolean layer
depends on the reviewed deterministic encoding, PySAT totalizers, CaDiCaL
proof production, and DRAT-trim.  A DRAT trace proves only its hashed CNF;
the analytic split and the complete selector cover are separate obligations.

The family method is due to I. Honkala, T. Laihonen, and S. Ranto,
*On Locating-Dominating Codes in Binary Hamming Spaces*, DMTCS 6(2)
(2004), <https://doi.org/10.46298/dmtcs.322>.  V. Junnila, T. Laihonen,
and T. Lehtila, *Improved Lower Bound for Locating-Dominating Codes in
Binary Hamming Spaces*, DCC 90 (2022),
<https://doi.org/10.1007/s10623-021-00963-8>, records the prior published
interval `28 <= gamma^LD(Q_7) <= 32`.

Targeted primary-source and refreshed Discovery Net searches through
2026-09-01 found no prior exclusion of these four normalized branches.  The
simultaneous closure is apparently new relative to the searched sources; no
absolute historical-priority claim is made.
