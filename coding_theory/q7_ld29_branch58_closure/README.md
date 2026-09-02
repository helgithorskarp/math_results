# Couple/dense-ball closure of `Q_7` LD29 branch 58

## Certified result

There is no locating-dominating code of cardinality at most 29 in the binary
7-cube whose lossless orphan normalization has canonical local-graph index
58.  The branch has mask `2012`; its local graph is the triangle-free graph
`K_{3,3}-e`, with sorted degree sequence `(2,2,3,3,3,3)` and stabilizer order
eight.

Together with the preceding exact exclusions, every hypothetical code of
cardinality at most 29 is therefore confined to the 53 branches

```text
0--43, 45--46, 48--49, 51, or 53--56.
```

This closes branch 58; it is not yet a proof that a 29-word code is
impossible.

Adding codewords preserves domination and preserves the distinct old-code
parts of all remaining noncodeword signatures.  Hence any code of size at
most 29 extends to one of size exactly 29, after which the established
lossless normalization applies.  It is therefore enough to exclude the exact
normalized case below.

## Three-way defect reduction

Let `C` be an exact 29-word locating-dominating code after the established
normalization

```text
0 in C;
e_i not in C                         (0 <= i < 7);
e_0+e_j not in C                     (1 <= j < 7).
```

Let `H` be the local graph on directions `1,...,6`, with `ij` selected when
`e_i+e_j` is a codeword, and let

```text
D = sum_F (|I(f_F)|-2)
```

be the total Honkala--Laihonen--Ranto family defect.  The predecessor proves
`D>=23` in branch 58.  For singleton signatures `p`, nonisolated codewords
`b`, codeword couples `q`, and induced code edges, the standard family
identities and the binary edge-isoperimetric bound give

$$
p=24+D,\qquad b\leq34-D,\qquad p+b\leq58,
\qquad e(Q_7[C])\leq E_7(b).
$$

Thus the remaining possibilities split into the following three cases.

| defect | singleton constraint | nonisolated bound | edge bound |
|:---|---:|---:|---:|
| `D=23` | `p=47` | `b<=11` | `E_7(11)=17` |
| `D=24` | `p=48` | `b<=10` | `E_7(10)=15` |
| `D>=25` | `p>=49` | `b<=9` | `E_7(9)=13` |

The `D>=25` formula directly combines the last row with domination, every
essential distance-two separation clause, cardinality 29, the complete
normalization, all 15 local-graph units, and biconditional singleton,
nonisolation, and code-edge indicators.

## Exact `D=23`: a forced couple

Branch 58 has local defect ten, local family capacity 36, and 16 forced
missing son slots.  Exhaustive integer-partition enumeration gives 88
capacity-feasible exact-`D=23` family states.  The defect-six occupancy
inequality leaves 49.  Their distribution by number `q` of codeword couples
is

```text
q=1: 1,  q=2: 2,  q=3: 5,  q=4: 12,  q=5: 29.
```

In particular, every state has a codeword couple.  A couple is an induced
two-codeword component: its endpoints are selected and their other twelve
neighbors are unselected.  Exactly 202 cube edges are compatible with the
fixed local units as possible couples.  The order-eight stabilizer partitions
them into 51 orbits.  The exact-`D=23` aggregate formula introduces one
selector for each representative, makes it imply all 14 defining literals,
and requires at least one selector.

## Exact `D=24`: a couple or a dense closed ball

At exact defect 24, 304 of 314 capacity-feasible states survive the same
occupancy inequality.  Their couple-count distribution is

```text
q=0: 13,  q=1: 26,  q=2: 39,  q=3: 61,  q=4: 78,  q=5: 87.
```

When `q>=1`, the preceding couple-orbit cover applies.  Every one of the 13
states with `q=0` has a family of defect five or six.  For its father `f`,
the identifying set $I(f)=C\cap N[f]$ has size at least seven.
Consequently seven of the eight vertices in some closed ball are codewords.

A dense pattern is a pair `(f,z)` requiring every vertex of `N[f]` other
than `z` to be selected.  There are exactly 526 patterns compatible with the
normalization and local units, partitioned into 129 stabilizer orbits.  If all
eight ball vertices are selected, any choice of `z` supplies such a pattern.
The exact-`D=24` aggregate formula has a complete 180-case disjunction: 51
couple representatives and 129 dense-pattern representatives.

## Exact formulas and checked certificates

All three formulas use the reviewed deterministic locating-domination
encoding and PySAT totalizers.  Standalone CaDiCaL `sc2021`
returned `s UNSATISFIABLE` and emitted a plain-text DRAT trace for each exact
formula.  DRAT-trim returned `s VERIFIED` on every exact CNF/proof pair, with
zero RAT lemmas in every checked core.

| formula | variables | clauses | CNF SHA-256 | proof bytes | DRAT SHA-256 | core/total lemmas | resolution steps |
|:---|---:|---:|:---|---:|:---|---:|---:|
| `branch58-d25-plus` | 10,432 | 183,619 | `00827d7530b93aa91b7d399f3414d05b4c8cdf15e13405d228d21ea3d6441c99` | 1,016,720,190 | `1298b67097ac8a187931acf2ec8a6513713da81f93f4d087fdf14f75b51f19c1` | 3,889,142/6,258,424 | 173,666,355 |
| `branch58-d24-selector` | 11,508 | 194,262 | `9765f05b04dbaaa5b6265422174e051638b77688ff198a9853348c554703007c` | 1,688,414,891 | `960698160d9e83e4c118fd9c4e3fa3091f3b8f2164172f270f679b0e951aadc5` | 5,557,738/10,400,350 | 286,304,564 |
| `branch58-d23-couple-selector` | 11,379 | 193,359 | `2857189787f7a40a2e023997c498f48fb955eb70b3af884e4a194b55c00ac48e` | 3,008,707,985 | `4dfe5b5b95aa543b719529561d626ef4262cf44e6c67beba175dd074178f0783` | 10,668,095/17,534,630 | 466,347,122 |

The compact `certificate_manifest.tsv` records the exact CNF and proof sizes,
hashes, checked-core counts, and checker timings.  The CNFs, proof traces,
solver output, and checker logs remain under `/scratch` and are deliberately
excluded from version control.  PySAT's independent Kissat 4.0.4 binding also
returned UNSAT on the `D=24` and `D=23` selector formulas in 3,223.152 and
6,591.042 seconds, respectively.

In aggregate, the three checked proofs occupy 5,713,843,066 bytes.  Their
cores contain 14,987 original clauses and 20,114,975 of 34,193,404 lemmas,
verified through 926,318,041 resolution steps with zero RAT lemmas.

## Reproduction

Create the pinned environment under `/scratch` and regenerate the analytic
enumeration, orbit quotients, and all three formulas:

```bash
python3 -m venv /scratch/q7-ld29-branch58-closure-venv
/scratch/q7-ld29-branch58-closure-venv/bin/pip install -r requirements.txt
/scratch/q7-ld29-branch58-closure-venv/bin/python \
  verify_branch58_closure.py \
  --write-directory /scratch/q7-ld29-branch58-closure-reproduced
```

For each generated formula, produce and check the external proof under
`/scratch`:

```bash
cadical -q --binary=false FORMULA.cnf FORMULA.drat
drat-trim FORMULA.cnf FORMULA.drat -w
```

The optional independent solver cross-checks are

```bash
/scratch/q7-ld29-branch58-closure-venv/bin/python \
  verify_branch58_closure.py --solve-kissat

/scratch/q7-ld29-branch58-closure-venv/bin/python \
  verify_branch58_closure.py --solve-incrementally
```

Reported environment and source hashes:

```text
Python                                  3.11.2
python-sat[pblib]                       1.9.dev15
CaDiCaL proof producer                  sc2021
CaDiCaL executable SHA-256              c6de62662723ec4a7426c5ca2bc9bfb04c60aad81a423957e3cd1ffadd0f8aa7
DRAT-trim Debian package                0.0~git20240428.effa1dc-2
DRAT-trim executable SHA-256            bc7543a99da8521ddb09af442698956054f11e10d198bd482ac756535244c021
requirements.txt SHA-256                639afc203e4b12224d62c9426902d5784099ba876c5ac2faed92e4659b56caca
certificate_manifest.tsv SHA-256        441f9723b71cb10b4db4522b09be84d30572cb2de7f3563ee8c7225c6e87054e
verify_branch58_d23.py SHA-256           c87ba037a3d0d1b7dcf08742201fed6b6511ae0c50b207fd34ced56891a34cec
verify_branch79_split.py SHA-256         ea313ef366ad3b2da6c4e43d721aef8e96ec9bfa7dafe18c8fdade61c5fdd687
local_graphs.py SHA-256                 35d187198ed332f64551a174096168f101adff309e0dfaf6d94f9ba6d360e1f4
search_q7_ld29.py SHA-256                3d4cc2bd966dbed2e4b585d3725dd37356487ad735eb008e55e730a7b9022614
verify_branch58_closure.py SHA-256       ca071e9047fa4598ba8f1cbb51de7122379ff4dd1bbbe57e717db1f8bb0738d0
```

## Trust boundary and context

The branch closure depends on the reviewed family partition, lossless
orphan-local normalization, and predecessor theorem `D>=23`.  The new hand
bridge is the exact family-state split and the complete couple/dense-ball
stabilizer quotient.  Its Boolean layer depends on the reviewed deterministic
encoding, PySAT totalizers, CaDiCaL proof production, and DRAT-trim.  A DRAT
trace proves only its hashed CNF; the analytic reduction and selector cover
are separate, source-pinned obligations.

The family method is due to I. Honkala, T. Laihonen, and S. Ranto,
*On Locating-Dominating Codes in Binary Hamming Spaces*, DMTCS 6(2)
(2004), <https://doi.org/10.46298/dmtcs.322>.  V. Junnila, T. Laihonen,
and T. Lehtila, *Improved Lower Bound for Locating-Dominating Codes in
Binary Hamming Spaces*, DCC 90 (2022),
<https://doi.org/10.1007/s10623-021-00963-8>, records the prior published
interval `28 <= gamma^LD(Q_7) <= 32`.

Targeted primary-source and refreshed Discovery Net searches through
2026-09-02 found no prior exclusion of this normalized branch.  The result is
apparently new relative to the searched sources; no historical-priority claim
is made.
