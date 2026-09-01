# Full-family rigidity and DRAT exclusion of `Q_7` LD29 branch 60

## Certified result

There is no locating-dominating code of cardinality at most 29 in the
binary 7-cube whose lossless orphan normalization has canonical local-graph
index 60.  This eight-edge graph has canonical mask `5911`, sorted degree
sequence `(2,2,2,3,3,4)`, three triangles, and independence number two.

This closes one branch of the lower frontier.  It does not prove that a
29-word code is impossible; branches 0--58 and 61--62 remain open.

## Defect-23 full-family rigidity

Let `C` be an exact 29-word locating-dominating code after the established
lossless normalization

```text
0 in C;
e_i not in C                         (0 <= i < 7);
e_0+e_j not in C                     (1 <= j < 7).
```

Let `H` be the local graph on directions `1,...,6`, with `ij` selected
exactly when `e_i+e_j` is a codeword.  The branchwise defect ladder gives
total Honkala--Laihonen--Ranto family defect `D>=23` in branch 60.  Its six
local fathers use ten defect units and have total capacity 37.  The eight
father--father edges force 16 oriented son slots absent, and the three
triangles force six further slots, for a total forced deficit of 22.

For `q` codeword couples, `M` family vertices, `p` singleton signatures,
and `a` isolated codewords, the standard identities are

$$
p=24+D,\qquad M=104-D-2q,\qquad
a\geq D-5,\qquad 2q\leq34-D.
$$

Exact integer-partition enumeration at `D=23`, including the near-full
defect-six/defect-five occupancy inequalities, leaves exactly one state:

```text
q=5,
extra family defects=(1,1,1,5,5),
missing slots beyond the 22 local forced slots=0,
family-codeword budget=34-D-2q=1.
```

The two defect-five families are full.  Their fathers cannot be codewords:
a selected full defect-five father puts at least seven codewords in its
family, exceeding the global budget one.  Thus both fathers are
noncodewords with all seven neighbors in `C` and all 21 sons present.

Call either full father `f`.  Its seven codeword neighbors are isolated,
because their other six neighbors are precisely its sons.  The weight of
`f` is at least five:

- weights zero through two are excluded directly by the normalization and
  the requirement that every neighbor of `f` be a codeword;
- at weight three, all three downward weight-two neighbors must be selected,
  so the support is a triangle of `H`; the same vertex then occupies none of
  its three local-father son slots, whereas the triangle bound charged only
  two missing slots, contradicting zero residual deficit;
- at weight four, a selected local word at distance two from `f` would have
  two common neighbors with `f`; both are isolated codewords but are adjacent
  to that selected word, a contradiction.  Hence the non-orphan support of
  `f` is independent in `H` and has size at least three, contradicting
  `alpha(H)=2`.

Two full noncodeword defect-five fathers must have mutual distance at least
five.  At distances one through four, respectively, the second father is a
required codeword neighbor of the first, is a son with a two-codeword
signature, has a noncodeword distance-two neighbor, or has a noncodeword
distance-three neighbor.  Each conflicts with one of the two full-family
conditions.  On the other hand, two subsets of a seven-element set, each of
size at least five, have symmetric difference at most four.  The two fathers
cannot coexist.  Therefore

$$
\boxed{D\geq24}
$$

in branch 60.  The finite analytic part of `verify_branch60.py`
reconstructs the 115 canonical local graphs, the unique arithmetic state,
all local invariants, the complete weight classification, and the final
distance bound.  It also pins the SHA-256 of the reviewed predecessor
ladder verifier that supplies `D>=23`.

## Exact formula and checked certificate

The defect theorem implies

$$
p\ge48,\qquad a\ge19,\qquad b=29-a\le10,
\qquad e(Q_7[C])\le E_7(10)=15,
$$

and the family identities give `p+b<=58`.  The deterministic exact formula
contains domination of all 128 vertices, every essential distance-two
separation clause, cardinality 29, the complete orphan normalization, all 15
local-graph unit clauses, biconditional singleton/nonisolation/code-pair
indicators, and precisely those four numerical consequences.  Repeated
literals are removed clausewise, which is a Boolean identity.

```text
variables  10,432
clauses   183,619
bytes   3,433,600
CNF SHA-256  0cbef6fab7be0192154c33cdbc7105dd91392073d2dffac0148d466bdd7ee144
```

CaDiCaL returned `UNSATISFIABLE` and emitted a 576,367,873-byte plain-text
DRAT proof with SHA-256

```text
a047917c792ecf9a70fbbb1a08836f58fd42e01443af4d3809578f7929f22c0f
```

DRAT-trim returned `s VERIFIED`.  Its checked core uses 2,246,352 of
3,392,242 lemmas and 116,003,018 resolution steps, with zero RAT lemmas.
PySAT's Kissat 4.0.4 binding independently returned UNSAT on a freshly
rebuilt copy of the same digest-pinned formula.

## Reproduction

Create the environment under `/scratch` and regenerate the exact formula:

```bash
python3 -m venv /scratch/q7-ld29-branch60-venv
/scratch/q7-ld29-branch60-venv/bin/pip install -r requirements.txt
/scratch/q7-ld29-branch60-venv/bin/python verify_branch60.py \
  --write-cnf /scratch/q7-ld29-d24-branch60.cnf
```

Produce and check the external certificate:

```bash
cadical -q --binary=false \
  /scratch/q7-ld29-d24-branch60.cnf \
  /scratch/q7-ld29-d24-branch60.drat

drat-trim \
  /scratch/q7-ld29-d24-branch60.cnf \
  /scratch/q7-ld29-d24-branch60.drat -w
```

Run the independent solver cross-check:

```bash
/scratch/q7-ld29-branch60-venv/bin/python \
  verify_branch60.py --solve-kissat
```

Reported environment:

```text
Python                          3.11.2
python-sat[pblib]               1.9.dev15
CaDiCaL                         sc2021
CaDiCaL executable SHA-256      c6de62662723ec4a7426c5ca2bc9bfb04c60aad81a423957e3cd1ffadd0f8aa7
DRAT-trim                       0.0~git20240428.effa1dc-2
DRAT-trim executable SHA-256    bc7543a99da8521ddb09af442698956054f11e10d198bd482ac756535244c021
requirements.txt SHA-256        639afc203e4b12224d62c9426902d5784099ba876c5ac2faed92e4659b56caca
verify_branch60.py SHA-256      2f5d22c97a2389fdb5fd0c46a81db2ef7b450d655059f122b3ef8cf49e3c8943
```

The CNF, proof trace, solver output, and checker output remain under
`/scratch` and are not committed.

## Trust boundary, scope, and novelty

The analytic theorem depends on the Honkala--Laihonen--Ranto family
partition, the reviewed orphan-local reduction, the branchwise defect
ladder, and elementary Hamming-cube geometry.  Its finite component is a
transparent enumeration of integer states, six-vertex graph invariants,
and 128 vertices.  The exact exclusion additionally depends on the
deterministic encoding, PySAT cardinality encodings, CaDiCaL proof
production, and DRAT-trim.  DRAT proves only the hashed formula; the
analytic bridge is separate.

The family method is from I. Honkala, T. Laihonen, and S. Ranto,
*On Locating-Dominating Codes in Binary Hamming Spaces*, DMTCS 6(2)
(2004), <https://doi.org/10.46298/dmtcs.322>.  V. Junnila, T. Laihonen,
and T. Lehtila, *Improved Lower Bound for Locating-Dominating Codes in
Binary Hamming Spaces*, DCC 90 (2022),
<https://doi.org/10.1007/s10623-021-00963-8>, records
`28 <= gamma^LD(Q_7) <= 32` and improves the general lower bound only from
dimension ten.

Targeted primary-source and refreshed Discovery Net searches through
2026-09-01 found no full-family defect-24 specialization or exact
certificate for branch 60.  The analytic refinement and finite exclusion
are apparently new to the searched sources; no historical-priority claim
is made.
