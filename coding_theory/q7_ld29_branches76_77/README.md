# Defect-25 rigidity and DRAT exclusion of `Q_7` LD29 branches 76--77

## Certified result

There is no locating-dominating code of cardinality at most 29 in the
binary 7-cube whose lossless orphan normalization has canonical local-graph
index 76 or 77.  These are two of the twenty admissible nine-edge graphs on
the six non-orphan coordinate directions:

| branch | canonical mask | sorted degrees | triangles |
|---:|---:|:---|---:|
| 76 | 5875 | `(1,3,3,3,4,4)` | 5 |
| 77 | 5919 | `(2,2,3,3,3,5)` | 5 |

This closes two additional finite branches.  It does not prove that a
29-word code is impossible.

## Sharper analytic bridge

Let `C` be an exact 29-word code after the normalization

```text
0 in C;
e_i not in C                         (0 <= i < 7);
e_0+e_j not in C                     (1 <= j < 7).
```

Let `H` be the graph on directions `1,...,6`, with `ij` selected exactly
when `e_i+e_j` is a codeword.  In the Honkala--Laihonen--Ranto family
partition, write

$$
D=\sum_F (|I(f_F)|-2)
$$

for the total family defect.  Then branches 76 and 77 both satisfy

$$
D\geq25.
$$

This sharpens the preceding leaf-aware bound `D>=24` in these two branches.
Fathers of defect six are permitted, so the theorem applies to arbitrary
exact 29-codes, including a 29-code obtained by augmenting a hypothetical
smaller code.

### Local slots

A direction of degree at least two in `H` is a father.  The local fathers
consume 12 defect units.  A defect-`d` father has capacity

$$
h(d)=1+\binom{d+2}{2},
$$

so `h(1),...,h(6) = 4,7,11,16,22,29`.  The two local configurations have

| branch | local capacity `L` | forced missing slots `delta_0` |
|---:|---:|---:|
| 76 | 43 | 26 |
| 77 | 45 | 28 |

Here every edge between local fathers forces two absent oriented son slots,
and every local triangle forces two further slots.  These counts reproduce
the preceding local-collision theorem.

For total defect `D`, number `q` of codeword couples, and number `M` of
family vertices, the standard identities give

$$
p=24+D,\qquad M=104-D-2q,\qquad
a\geq D-5,\qquad 2q\leq34-D.
$$

After the 12 local defect units, distribute the remaining defect as an
integer partition `P` with parts in `{1,...,6}`.  At `D=23` no capacity
state survives the forced local slots.  At `D=24`, the complete capacity
frontier is the same in both branches:

| `q` | extra defects `P` | free missing slots `s` | family-codeword budget |
|---:|:---|---:|---:|
| 3 | `(6,6)` | 1 | 4 |
| 4 | `(1,5,6)` | 0 | 2 |
| 4 | `(6,6)` | 3 | 2 |
| 5 | `(1,1,1,1,1,1,6)` | 0 | 0 |
| 5 | `(1,1,4,6)` | 0 | 0 |
| 5 | `(1,5,6)` | 2 | 0 |
| 5 | `(6,6)` | 5 | 0 |

A defect-six father has identifying set equal to its entire closed
neighborhood, so the father is a codeword.  Its seven slots pairing the
father with a neighboring codeword can only contain that neighboring
codeword.  Consequently, `k` defect-six families with at most `s` missing
slots contain at least `8k-s` family codewords.

Every row in the table has `8k-s` strictly larger than its displayed global
family-codeword budget `34-D-2q`.  Thus every `D=24` state is impossible and
`D>=25` follows.  The standard-library portion of
`verify_branches76_77.py` reconstructs the two local graphs, the complete
integer frontier, and every strict occupancy contradiction.

## Exact formulas and certificates

The new defect bound implies

$$
p\geq49,\qquad a\geq20,\qquad b=29-a\leq9,
\qquad e(Q_7[C])\leq E_7(9)=13,
$$

and the family identities also give `p+b<=58`.  Each deterministic formula
contains exact domination and distance-two separation, exact cardinality 29,
the complete orphan normalization, all 15 local units, biconditional
indicators, and precisely those four numerical consequences.  Repeated
literals are removed clausewise, a Boolean identity.

Each formula has 10,432 variables, 183,619 clauses, and 3,433,599 bytes.
CaDiCaL 1.5.3 emitted a plain-text DRAT proof; DRAT-trim
`0.0~git20240428.effa1dc-2` returned `s VERIFIED` on both exact pairs.
Neither checked core uses a RAT lemma.  PySAT's Kissat 4.0.4 binding
independently returned UNSAT on freshly regenerated formulas.

| branch | CNF SHA-256 | proof bytes | DRAT SHA-256 | core lemmas | resolution steps |
|---:|:---|---:|:---|---:|---:|
| 76 | `6955a5b3bcbff062a20967a981ab4d1257d5524d7a0db86ad6a2e28786c29369` | 133,997,049 | `31e850113ecb8547840c0da3d834b5a09250245fbf4bb4cb3dc5c4aaceea5952` | 551,044 | 31,541,114 |
| 77 | `041eaf6fc23e01e20c09a4c86983570d084d02b50631f5ca1c8bfbecd150987c` | 91,441,743 | `b2373cec758bfed77fb6e5a03ecae5836074f02bc6b6ad7bb6090b5ea8eaefbf` | 353,028 | 19,450,205 |

## Reproduction

Create an environment under `/scratch` and regenerate the exact formulas:

```bash
python3 -m venv /scratch/q7-ld29-d25-branches76-77-venv
/scratch/q7-ld29-d25-branches76-77-venv/bin/pip install -r requirements.txt
/scratch/q7-ld29-d25-branches76-77-venv/bin/python \
  verify_branches76_77.py \
  --write-directory /scratch/q7-ld29-d25-branches76-77
```

For each `b` in `76,77`, produce and check the external certificate:

```bash
cadical -q --binary=false \
  /scratch/q7-ld29-d25-branches76-77/branch-${b}.cnf \
  /scratch/q7-ld29-d25-branch-${b}.drat

drat-trim \
  /scratch/q7-ld29-d25-branches76-77/branch-${b}.cnf \
  /scratch/q7-ld29-d25-branch-${b}.drat -w
```

Run the independent solver cross-check with

```bash
/scratch/q7-ld29-d25-branches76-77-venv/bin/python \
  verify_branches76_77.py --solve-kissat
```

Reported environment and source hashes:

```text
Python                         3.11.2
python-sat[pblib]              1.9.dev15
CaDiCaL Debian package         1.5.3-2
DRAT-trim Debian package       0.0~git20240428.effa1dc-2
requirements.txt SHA-256       639afc203e4b12224d62c9426902d5784099ba876c5ac2faed92e4659b56caca
verify_branches76_77.py SHA-256 c2f7a8f4cf99d0601e2a472992fb5af563981b925ad910f0e820101b8fbe8c29
```

CNFs, proof traces, and checker output remain under `/scratch` and are not
committed.

## Trust boundary, scope, and novelty

The analytic theorem depends on the Honkala--Laihonen--Ranto family
partition, the reviewed orphan-local reduction, the preceding local-slot
collision count, and elementary Hamming-cube geometry.  Its finite part is
a transparent enumeration of seven integer states.  The exact exclusions
add the deterministic encoding, PySAT cardinality encodings, and DRAT-trim
to the trust boundary.  DRAT proves only the two hashed formulas; the
analytic bridge is separate.

The family method is from I. Honkala, T. Laihonen, and S. Ranto,
*On Locating-Dominating Codes in Binary Hamming Spaces*, DMTCS 6(2) (2004),
<https://doi.org/10.46298/dmtcs.322>.  V. Junnila, T. Laihonen, and
T. Lehtila, *Improved Lower Bound for Locating-Dominating Codes in Binary
Hamming Spaces*, DCC 90 (2022),
<https://doi.org/10.1007/s10623-021-00963-8>, records
`28 <= gamma^LD(Q_7) <= 32` and improves the general lower bound only from
dimension ten.

Targeted primary-source and refreshed graph searches through 2026-09-01
found no defect-25 specialization or exact certificate for either local
branch.  The new analytic refinement and the two exclusions are apparently
new to the searched sources; no historical-priority claim is made.
