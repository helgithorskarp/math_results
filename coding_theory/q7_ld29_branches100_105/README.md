# Local family-collision rigidity and closure of the 11-edge `Q_7` LD29 frontier

## Result

There is no locating-dominating code of cardinality at most 29 in the
binary 7-cube whose lossless orphan normalization has canonical local-graph
index 100, 101, 102, 103, 104, or 105.

Together with the existing certificates for branches 97--99 and 106--114,
this closes the entire 11--15-edge local frontier.  Every hypothetical code
of cardinality at most 29 now lies in exactly one of the 97 canonical
branches 0--96, each having between 4 and 10 local edges.  This is a lossless
search reduction, not a proof that a 29-word code is impossible.

The main new hand-checkable ingredient is a local family-collision lemma.
In every one of branches 100--105, any exact 29-word code has total
Honkala--Laihonen--Ranto family defect

$$
D\geq27.
$$

The proof allows fathers of defect six, so it applies to an arbitrary exact
29-word code, not only to a minimum code.  Consequently it also covers the
exact 29-word code obtained by augmenting a hypothetical smaller code in the
predecessor's lossless reduction.

The defect bound gives

$$
p\geq51,\qquad a\geq22,\qquad b=29-a\leq7,
\qquad e(Q_7[C])\leq E_7(7)=9,
$$

where `p` counts singleton identifying sets, `a` and `b` count isolated and
nonisolated codewords, and `e(Q_7[C])` is the number of induced code edges.
Clean exact SAT formulas using these consequences are UNSAT for all six
branches.  Every formula has a checked DRAT certificate.

During the mandatory final graph refresh, an independent dynamic-pair
certificate for branches 100--102 had landed concurrently.  Accordingly,
the status of the six finite exclusions is:

- branches 100--102 independently reproduce that result, while the new
  defect-27 lemma gives a stronger analytic reduction and warning-free
  proofs that are 43, 87, and 57 times smaller, respectively; and
- branches 103--105 are the new exclusions that complete the 11-edge
  frontier.

The concurrent source is
<https://github.com/helgithorskarp/math_results/tree/614bebf9e9ee0a67ea8b6689d17ad2bc15ad4524/coding_theory/q7_ld29_branches100_102_dynamic>.

## The local family-collision lemma

Use the predecessor's normalization

```text
0 in C;
e_i not in C                         (0 <= i < 7);
e_0+e_j not in C                     (1 <= j < 7).
```

Let `H` be the graph on coordinate directions `1,...,6` in which `ij` is an
edge exactly when `e_i+e_j` is a codeword.  For branches 100--105, `H` has
11 edges and minimum degree at least two.  Therefore

$$
I(e_i)=\{0\}\cup\{e_i+e_j:ij\in E(H)\}
$$

has size at least three.  Each `e_i` is a father whose defect is
`d_i=deg_H(i)-1`, and the six local fathers use

$$
\sum_i d_i=2|E(H)|-6=16
$$

units of total defect.

A defect-`d` father has capacity

$$
h(d)=1+\binom{d+2}{2}.
$$

For an arbitrary exact 29-code a father can have defect six, so the complete
capacity list needed below is

```text
d       1   2   3   4   5   6
h(d)    4   7  11  16  22  29.
```

Let `M` be the number of vertices in all families and let

$$
\Delta=\sum_F h(d_F)-M
$$

be the number of absent son slots relative to full family capacity.

Every oriented edge `ij` of `H` forces an absent local son slot.  In the
family of father `e_i`, the pair of codewords `{0,e_i+e_j}` has `e_j` as its
other common neighbor.  But `e_j` is itself a father, not a son.  Thus the
11 edges force 22 absent slots.

Every triangle `ijk` forces two further absent slots.  The word
`e_i+e_j+e_k` is the candidate son in one slot for each of the three fathers
`e_i,e_j,e_k`, but a vertex can be a son of at most one father.  Distinct
triangles give distinct words, and these slots are disjoint from the
oriented-edge slots.  If `t(H)` denotes the triangle count, then

$$
\boxed{\Delta\geq22+2t(H).}
$$

The six canonical cases have the following exact data.

| branch | mask | sorted degrees | `t(H)` | local capacity `L` | forced `Delta` |
|---:|---:|:---|---:|---:|---:|
| 100 | 6015 | `(2,3,4,4,4,5)` | 8 | 60 | 38 |
| 101 | 6142 | `(2,4,4,4,4,4)` | 7 | 59 | 36 |
| 102 | 6655 | `(3,3,3,3,5,5)` | 8 | 60 | 38 |
| 103 | 7103 | `(3,3,3,4,4,5)` | 7 | 59 | 36 |
| 104 | 7166 | `(3,3,4,4,4,4)` | 6 | 58 | 34 |
| 105 | 8157 | `(3,3,4,4,4,4)` | 6 | 58 | 34 |

## Capacity contradiction below defect 27

For every exact 29-word locating-dominating code, the family partition
identities and inequalities are

$$
p=24+D,\qquad M=104-D-2q,
\qquad a\geq D-5,\qquad 2q\leq34-D,
$$

where `q` is the number of codeword couples.

Let `G(r)` be the largest total capacity obtainable by partitioning `r`
units of defect into parts in `{1,...,6}` with the capacities `h` above.
The standard dynamic program

$$
G(0)=0,\qquad
G(r)=\max_{1\leq d\leq\min(6,r)}(G(r-d)+h(d))
$$

gives the following complete table for a putative `16 <= D <= 26`.  The
display uses the largest possible `q`, which minimizes `M` and is therefore
the most permissive choice.

| `D` | `r=D-16` | `G(r)` | max `q` | min `M` | `G(r)-M` |
|---:|---:|---:|---:|---:|---:|
| 16 | 0 | 0 | 9 | 70 | -70 |
| 17 | 1 | 4 | 8 | 71 | -67 |
| 18 | 2 | 8 | 8 | 70 | -62 |
| 19 | 3 | 12 | 7 | 71 | -59 |
| 20 | 4 | 16 | 7 | 70 | -54 |
| 21 | 5 | 22 | 6 | 71 | -49 |
| 22 | 6 | 29 | 6 | 70 | -41 |
| 23 | 7 | 33 | 5 | 71 | -38 |
| 24 | 8 | 37 | 5 | 70 | -33 |
| 25 | 9 | 41 | 4 | 71 | -30 |
| 26 | 10 | 45 | 4 | 70 | -25 |

The six local fathers have capacity `L`, while all remaining fathers have
capacity at most `G(D-16)`.  Thus `D<=26` would imply

$$
\Delta\leq L+G(D-16)-M\leq L-25.
$$

But the last column of the first table is at least `L-24` in every branch.
This contradiction proves `D>=27`.

Now `p=24+D>=51` and `a>=D-5>=22`, hence `b<=7`.  All induced code edges
have both endpoints among the `b` nonisolated codewords.  The binary-layer
edge-isoperimetric recurrence gives `E_7(7)=9`.  Also `p+b<=58`, since a
nonisolated codeword labels at most one singleton signature and an isolated
codeword labels at most two.  These are precisely the new structural bounds
used in the formulas.

`verify_local_defect27.py` reconstructs all 115 local graph orbits and every
number in both calculations using only the Python standard library.

## Exact formulas and certificates

Each formula contains:

- domination at every vertex;
- every essential distance-two separation clause;
- cardinality exactly 29;
- the complete orphan normalization;
- all 15 unit clauses fixing the selected local graph;
- biconditional indicators for singleton signatures, nonisolated
  codewords, and induced code edges; and
- the proved bounds `p>=51`, `b<=7`, `p+b<=58`, and `e(Q_7[C])<=9`.

The predecessor's separation clauses contained 2,688 repeated endpoint
literal occurrences.  The new generator removes repeated occurrences
clause by clause.  This is a Boolean identity, leaves the variable and
clause counts unchanged, reduces every CNF by 8,484 bytes, and makes
DRAT-trim's input parse warning-free.

Each cleaned formula has 10,432 variables, 183,619 clauses, and 3,433,597
bytes.  CaDiCaL 1.5.3 returned UNSAT and emitted a plain-text DRAT proof;
DRAT-trim `0.0~git20240428.effa1dc-2` returned `s VERIFIED` on every exact
pair.  PySAT's Kissat 4.0.4 binding independently returned UNSAT.

| branch | CNF SHA-256 | proof bytes | DRAT SHA-256 | core lemmas |
|---:|:---|---:|:---|---:|
| 100 | `aca52d0151fe1c517a336d2dd9a53a2ba5b3585b8539e6068ac647eb2e1fa113` | 8,279,422 | `287f98a9ef17977ceccc5d6e2ad9f1711e1e8c471ab0b2fc30446bb5e8d8c240` | 15,426 |
| 101 | `c1caefd18c0496a55c19540168dc823388e11d167348c0f86616901940e7921e` | 2,245,375 | `3ad475d1a7c63132785a1e4bdc08d5055115640258957df2f6bf20b899f80b09` | 6,376 |
| 102 | `54baf336bf5be635c4a8cf7c0de47753c538b7f49982f40c6c90b9d8c5b7efd5` | 7,089,846 | `3db8d2868bbcd3c1f31a6950e00ed1b12aec9932ed6d8677e48ddcb9f038d242` | 12,884 |
| 103 | `957a1e8df8027d53570844d4de962aad74638792a7d480b7eb5786850d584169` | 9,891,980 | `635f6b691130bcccdc95d828b655d94094a3a85167e773f9bc768dfe54e4a6ea` | 21,327 |
| 104 | `985792613b77973a4b195cf26f2b20f6c0b6231d34c009ee10093ae004cc690a` | 6,454,571 | `8bbd3b17936e643d8458a3324679e6853aa6fbdd50818469de85981a38706102` | 7,780 |
| 105 | `b04bc5d1f2fb792db707bb4a8feeaefe0dabb50b2c469b44aa08661d219fa451` | 6,701,933 | `69cc79b8fc659d9ca2f238c602035459933d4d94160bbbc50234e0b223ce1c9c` | 12,126 |

No RAT lemma was used in any checked proof core.  CNFs, proof traces, and
checker output remain under `/scratch` and are deliberately not committed.

## Reproduction

Run the hand-checkable finite verifier:

```bash
python3 verify_local_defect27.py
```

Create a scratch virtual environment, install the pinned dependency, and
regenerate all exact CNFs:

```bash
python3 -m venv /scratch/q7-ld29-d27-venv
/scratch/q7-ld29-d27-venv/bin/pip install -r requirements.txt
/scratch/q7-ld29-d27-venv/bin/python verify_branches100_105.py \
  --write-directory /scratch/q7-ld29-d27-cnfs
```

For every `b` in `100 101 102 103 104 105`, produce and check a fresh proof:

```bash
cadical -q --binary=false \
  /scratch/q7-ld29-d27-cnfs/branch-${b}.cnf \
  /scratch/q7-ld29-d27-branch-${b}.drat

drat-trim \
  /scratch/q7-ld29-d27-cnfs/branch-${b}.cnf \
  /scratch/q7-ld29-d27-branch-${b}.drat -w
```

The reported environment used Python 3.11.2,
`python-sat[pblib]==1.9.dev15`, CaDiCaL 1.5.3, DRAT-trim
`0.0~git20240428.effa1dc-2`, and the Kissat 4.0.4 PySAT binding.

## Trust boundary, scope, and novelty

The hand theorem depends on the Honkala--Laihonen--Ranto family partition,
the elementary radius-one ball geometry of the binary cube, and the finite
capacity calculation reconstructed by the standard-library verifier.  The
finite exclusion additionally depends on the reviewed lossless orphan-local
reduction, the exact SAT encoding, deterministic PySAT cardinality
encodings, and DRAT-trim.  DRAT proves only the unsatisfiability of the six
hashed formulas; relevance to every code of size at most 29 uses the
analytic reductions.

The family method originates in I. Honkala, T. Laihonen, and S. Ranto,
*On Locating-Dominating Codes in Binary Hamming Spaces*, DMTCS 6(2)
(2004), 265--282, <https://doi.org/10.46298/dmtcs.322>.  The published
small-dimension context is V. Junnila, T. Laihonen, and T. Lehtila,
*Improved Lower Bound for Locating-Dominating Codes in Binary Hamming
Spaces*, Designs, Codes and Cryptography 90 (2022), 67--85,
<https://doi.org/10.1007/s10623-021-00963-8>; its table gives the interval
28--32 for dimension seven and its improved lower bound applies only from
dimension ten onward.

Targeted primary-source and citation searches through 2026-09-01 found no
previous local son-slot collision bound.  The final graph refresh did find
the concurrent branch 100--102 certificates described above, but no result
for branches 103--105.  Thus the defect-27 theorem and exclusions of
103--105 are new to the refreshed graph and apparently new to the searched
sources; the 100--102 certificates are an independent, substantially more
compact reproduction and refinement.  No historical-priority claim is
made.
