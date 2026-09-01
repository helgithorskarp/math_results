# Defect-5/defect-6 split and closure of `Q_7` LD29 branch 50

## Certified result

There is no locating-dominating code of cardinality at most 29 in the binary
7-cube whose lossless orphan normalization has canonical local-graph index
50.  The branch has mask `957`, sorted degree sequence `(2,2,2,2,4,4)`, two
triangles, independence number three, and an order-four stabilizer fixing the
orphan coordinate.

Together with the preceding branch closures, every hypothetical code of
cardinality at most 29 now lies in one of the 58 branches

```text
0--49 or 51--58.
```

This is one further exact exclusion, not yet a proof that a 29-word code is
impossible.

## Exact-defect reduction

Use the established normalization

```text
0 in C;
e_i not in C                         (0 <= i < 7);
e_0+e_j not in C                     (1 <= j < 7),
```

and let `D` be the total Honkala--Laihonen--Ranto family defect.  The
preceding center-split theorem proves `D>=24` in branch 50.  For singleton
signatures `p`, nonisolated codewords `b`, and induced code edges, the
standard family identities and edge-isoperimetric bound give

$$
p=24+D,\qquad b\leq34-D,\qquad p+b\leq58,
\qquad e(Q_7[C])\leq E_7(b).
$$

Thus `D>=25` implies

$$
p\geq49,\qquad b\leq9,\qquad p+b\leq58,
\qquad e(Q_7[C])\leq13.
$$

The first exact formula combines these consequences with domination,
distance-two separation, cardinality 29, the complete normalization, and
all 15 local-graph units.  Its checked UNSAT proof excludes `D>=25`.
Consequently any code in branch 50 would have exactly `D=24` and `p=48`.

## The exact-`D=24` family split

Let `q` be the number of codeword couples, `s` the free missing-son-slot
budget after the 20 local forced slots, and `B` the family-codeword budget.
Complete integer enumeration gives 187 capacity states.  If `q=0`, only
three survive the defect-six occupancy bound:

| `q` | extra defects | `s` | `B` |
|---:|:---|---:|---:|
| 0 | `(1,1,1,5,6)` | 1 | 10 |
| 0 | `(1,2,5,6)` | 0 | 10 |
| 0 | `(3,5,6)` | 0 | 10 |

Every row has one defect-five family and one defect-six family.  If the
defect-five father were a codeword, these two families would force at least

$$
(7-t_5)+(8-t_6)=15-(t_5+t_6)\geq15-s\geq14
$$

family codewords, contradicting `B=10`.  Hence the defect-five father `x`
is a noncodeword with all seven neighbors in `C`.  The defect-six father
`y` is a codeword whose entire closed neighborhood is in `C`.

The centers have distance at least five.  Distance zero or one contradicts
their selected statuses.  At distance two, each center occupies a missing
son slot in the other family, costing two slots.  At distance three, the
three inward codeword neighbors of `y` destroy three defect-five son slots.
At distance four, a codeword neighbor of `y` at distance three from `x`
destroys the three predecessor slots in the defect-five family.  Every case
uses more than the available `s<=1`.

## Local costs and complete orbit split

The predecessor classifies the residual local cost of a noncodeword
defect-five center.  For branch 50, cost at most one leaves the exact finite
candidate set reconstructed by the verifier.

There is a complementary cost for the defect-six center.  A weight-three
word is a potential local son precisely when its support contains a wedge
of the local graph.  After the oriented-edge and triangle deficits have
been charged, one local slot remains for each of the 12 words

```text
14 22 26 28 38 44 50 70 76 82 98 100.
```

If such a word lies in `N[y]`, it is selected and cannot fill that
two-identifier son slot.  Therefore the number of these words in `N[y]` is
a lower bound on the defect-six center's residual local cost.  Since the
two centers have distance at least five, their charged local slots are
disjoint, so their costs sum to at most one.

After compatibility with the normalization, 96 ordered `(x,y)` pairs
remain.  The order-four stabilizer partitions them into 31 orbits.  If
instead `q>=1`, exactly 204 cube edges are compatible with the fixed units
as possible induced codeword couples, and they form 78 orbits.  Hence every
hypothetical exact-`D=24` code can be moved to one of exactly

$$
78+31=109
$$

selector cases.  One aggregate formula uses a selector for each orbit and
requires at least one selector.  Its checked UNSAT proof excludes all 109
cases simultaneously.  As a solver-level cross-check independent of that
disjunction, incremental PySAT CaDiCaL 1.9.5 returned UNSAT on all 109 sets
of defining assumptions in 651.504 seconds.

## Exact formulas and checked certificates

Both formulas use the reviewed deterministic locating-domination encoding
and sequential PySAT totalizers.  Standalone CaDiCaL `sc2021` exited with
`s UNSATISFIABLE` and emitted a plain-text DRAT trace for each.  DRAT-trim
returned `s VERIFIED` on both exact CNF/proof pairs, with zero RAT lemmas in
either checked core.

| formula | variables | clauses | CNF SHA-256 | proof bytes | DRAT SHA-256 | core/total lemmas | resolution steps |
|:---|---:|---:|:---|---:|:---|---:|---:|
| `branch50-d25` | 10,432 | 183,619 | `4e289cbbea709c2b4ea24652eaf8b7c5f03114600ca2cdf63328e2e734db23ef` | 257,792,154 | `d8f555655bc4814c2e1cb7bccea2bd6db7e1226b16942535f0b6833cfafd2e75` | 1,087,575/1,759,221 | 53,719,236 |
| `branch50-d24-selector` | 11,437 | 194,233 | `e13f78769c23c56a67ca945da8759dae0292e8b3838e1b5da1a9598cce9e6741` | 723,412,269 | `afdff35e38396effe8b3db53ffcc089970d74a5938e13fe87f9b2924f7cc9d98` | 2,721,546/4,254,545 | 150,790,876 |

The checked cores use 3,844 and 5,281 original clauses, respectively.
CaDiCaL's proof-producing runs took 198.952 and 599.956 wall-clock seconds;
DRAT-trim's checks took 212.146 and 764.883 seconds.  The complete compact
statistics are in `certificate_manifest.tsv`.  CNFs, proofs, and logs remain
under `/scratch` and are deliberately excluded from version control.

## Reproduction

Create the pinned environment and regenerate both exact formulas under
`/scratch`:

```bash
python3 -m venv /scratch/q7-ld29-branch50-venv
/scratch/q7-ld29-branch50-venv/bin/pip install -r requirements.txt
/scratch/q7-ld29-branch50-venv/bin/python verify_branch50_closure.py \
  --write-directory /scratch/q7-ld29-branch50-reproduced
```

Produce and check each proof:

```bash
cadical -q --binary=false FORMULA.cnf FORMULA.drat
drat-trim FORMULA.cnf FORMULA.drat -w
```

The slower independent checks are available as

```bash
/scratch/q7-ld29-branch50-venv/bin/python verify_branch50_closure.py \
  --solve-kissat
/scratch/q7-ld29-branch50-venv/bin/python verify_branch50_closure.py \
  --solve-incrementally
```

Reported environment and source hashes:

```text
Python                              3.11.2
python-sat[pblib]                   1.9.dev15
CaDiCaL proof producer              sc2021
CaDiCaL executable SHA-256          c6de62662723ec4a7426c5ca2bc9bfb04c60aad81a423957e3cd1ffadd0f8aa7
DRAT-trim Debian package            0.0~git20240428.effa1dc-2
DRAT-trim executable SHA-256        bc7543a99da8521ddb09af442698956054f11e10d198bd482ac756535244c021
requirements.txt SHA-256            639afc203e4b12224d62c9426902d5784099ba876c5ac2faed92e4659b56caca
certificate_manifest.tsv SHA-256    771686133ef75ba4d51c5f35174b16e4c845246fa583c24eacdadbbc53a8c9b2
verify_five_branch_d24.py SHA-256    6cd1880178ab8ed330db4030459a0247fc6e13016e6cf8321bce8ec7ed0e6ada
local_graphs.py SHA-256             35d187198ed332f64551a174096168f101adff309e0dfaf6d94f9ba6d360e1f4
search_q7_ld29.py SHA-256            3d4cc2bd966dbed2e4b585d3725dd37356487ad735eb008e55e730a7b9022614
verify_branch50_closure.py SHA-256   6d64a2be83ffeed61a6267f420dd965567547c3f24a88c6024210fbcdc36bef5
```

## Trust boundary and context

The branch closure depends on the reviewed family partition, orphan-local
normalization, and predecessor `D>=24` theorem.  The new hand bridge is the
exact family-state split, center-separation argument, local wedge cost, and
complete stabilizer quotient.  Its finite Boolean layer depends on the
reviewed encoding, PySAT totalizers, CaDiCaL proof production, and DRAT-trim.
The DRAT traces prove only the two hashed formulas; the analytic reductions
are separate, source-pinned dependencies.

The family method is due to I. Honkala, T. Laihonen, and S. Ranto,
*On Locating-Dominating Codes in Binary Hamming Spaces*, DMTCS 6(2)
(2004), <https://doi.org/10.46298/dmtcs.322>.  V. Junnila, T. Laihonen,
and T. Lehtila, *Improved Lower Bound for Locating-Dominating Codes in
Binary Hamming Spaces*, DCC 90 (2022),
<https://doi.org/10.1007/s10623-021-00963-8>, records the prior published
interval `28 <= gamma^LD(Q_7) <= 32`.

Targeted primary-source and refreshed Discovery Net searches through
2026-09-01 found no prior exclusion of this normalized branch.  The result
is apparently new relative to the searched sources; no historical-priority
claim is made.
