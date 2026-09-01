# Full-family separation and DRAT exclusion of `Q_7` LD29 branches 78 and 80

## Certified result

There is no locating-dominating code of cardinality at most 29 in the
binary 7-cube whose lossless orphan normalization has canonical local-graph
index 78 or 80.  These are two of the twenty admissible nine-edge graphs on
the six non-orphan coordinate directions:

| branch | canonical mask | sorted degrees | triangles | independence number |
|---:|---:|:---|---:|---:|
| 78 | 5943 | `(2,2,3,3,4,4)` | 4 | 2 |
| 80 | 5950 | `(2,2,3,3,4,4)` | 4 | 2 |

This closes two additional finite branches.  It does not prove that a
29-word code is impossible.

## Defect-25 theorem

Let `C` be an exact 29-word locating-dominating code after the normalization

```text
0 in C;
e_i not in C                         (0 <= i < 7);
e_0+e_j not in C                     (1 <= j < 7).
```

Let `H` be the local graph on directions `1,...,6`, with `ij` selected
exactly when `e_i+e_j` is a codeword.  In either branch 78 or branch 80,
the total Honkala--Laihonen--Ranto family defect satisfies

$$
D\geq25.
$$

Fathers of defect six are permitted, so the theorem applies to arbitrary
exact 29-codes, including a 29-code obtained by augmenting a hypothetical
smaller code.

### Capacity frontier

The six local fathers use 12 defect units, have total capacity 44, and
force 26 distinct missing son slots: two for every local father--father
edge and two more for every triangle.  For total defect `D`, number `q` of
codeword couples, and number `M` of family vertices, the standard family
identities give

$$
p=24+D,\qquad M=104-D-2q,\qquad
a\geq D-5,\qquad 2q\leq34-D.
$$

After distributing the remaining defect units into parts in
`{1,...,6}`, exact integer enumeration finds no capacity state at `D=23`.
At `D=24`, the standard defect-six occupancy inequality eliminates every
state except

```text
q = 5,
extra family defects = (1,1,5,5),
missing slots beyond the 26 local forced slots = 0,
family-codeword budget = 34-D-2q = 0.
```

A defect-six family with `s` available missing slots forces at least `8-s`
family codewords; this is the inequality used to eliminate the other
states.  The surviving state therefore has two full defect-five families
and no codeword belonging to any family.

### Full-family separation

Let `f` be the father of one of those full defect-five families.  Its
identifying set consists of seven codewords.  Since the family contains no
codeword, `f` and all 21 sons are noncodewords.  Each of the seven
codewords in `I(f)` is isolated: its other six neighbors are precisely the
six sons corresponding to pairs containing it.

The center `f` cannot have weight at most two.  Weight zero is the fixed
codeword, every normalized weight-one vertex has fewer than seven codeword
neighbors, and a weight-two noncodeword has two absent weight-one
neighbors.  If `f` had weight three, all three downward weight-two
neighbors would have to be selected local codewords, so its support would
be a triangle of `H`.  The same weight-three vertex is the candidate son
in three local father slots.  As a father it fills none of them, whereas
the triangle bound charges only two missing slots.  This contradicts the
zero-slack capacity equality.

Suppose `f` has weight four.  If a selected local codeword `w=e_i+e_j`
is at distance two from `f`, their two common neighbors lie in `I(f)`.
They are isolated codewords but are adjacent to the codeword `w`, a
contradiction.  Hence the directions from `{1,...,6}` in the support of
`f` form an independent set in `H`.  They have size at least three, but
both local graphs have independence number two.  Thus every full
defect-five center in the surviving state has weight at least five.

Two distinct full defect-five centers must be at distance at least five.
Indeed, relative to a full center all distance-two vertices are sons and
therefore noncodewords.  All distance-three vertices are also noncodewords:
a codeword there would be adjacent to a distance-two son and enlarge its
two-codeword identifying set.  Centers at distances one through four then
contradict, respectively, the codeword status of every neighbor, the son
status at distance two, or the required codeword neighbor of the second
center at distance two or three from the first.

On the other hand, two subsets of a seven-element set, each of size at
least five, have symmetric difference at most four.  The two required
centers can therefore neither be at distance at least five nor coexist.
This eliminates the last `D=24` state and proves `D>=25`.

The standard-library portion of `verify_branches78_80.py` reconstructs
the 115 canonical local-graph orbits, the complete integer frontier, both
independence numbers, and the finite weight/distance argument.

## Exact formulas and checked certificates

The defect theorem implies

$$
p\geq49,\qquad a\geq20,\qquad b=29-a\leq9,
\qquad e(Q_7[C])\leq E_7(9)=13,
$$

and the family identities also give `p+b<=58`.  Each deterministic formula
contains exact domination and distance-two separation, exact cardinality
29, the complete orphan normalization, all 15 local-graph unit clauses,
biconditional indicators, and precisely those four numerical consequences.
Repeated literals are removed clausewise, a Boolean identity.

Each formula has 10,432 variables, 183,619 clauses, and 3,433,599 bytes.
CaDiCaL 1.5.3 emitted a plain-text DRAT proof for each exact CNF.
DRAT-trim `0.0~git20240428.effa1dc-2` returned `s VERIFIED` on both pairs.
Neither checked core uses a RAT lemma.  PySAT's Kissat 4.0.4 binding
independently returned UNSAT on freshly regenerated formulas.

| branch | CNF SHA-256 | proof bytes | DRAT SHA-256 | core lemmas | resolution steps |
|---:|:---|---:|:---|---:|---:|
| 78 | `26817751225eb282b2de0a3d9c6106b03775f519ae3be515e825b99c70f99524` | 130,657,988 | `d8220bcf6724f4e929a3e6623867b95a929b93c97d22bc990fe1b589c670dbe3` | 454,562 | 26,444,734 |
| 80 | `9f3abd711640d651a95cafbe0f6f47398f62d66d83f964dfb7640feac8af6b2a` | 104,659,129 | `266b7793f9427b5f026c4785858c7b45078b2c5e55b63b025827a573995430c8` | 405,229 | 23,408,358 |

CNFs, proof traces, and checker output remain under `/scratch` and are not
committed.

## Reproduction

Create the environment under `/scratch` and regenerate the exact formulas:

```bash
python3 -m venv /scratch/q7-ld29-d25-branches78-80-venv
/scratch/q7-ld29-d25-branches78-80-venv/bin/pip install -r requirements.txt
/scratch/q7-ld29-d25-branches78-80-venv/bin/python \
  verify_branches78_80.py \
  --write-directory /scratch/q7-ld29-d25-branches78-80
```

For each `b` in `78,80`, produce and check the external certificate:

```bash
cadical -q --binary=false \
  /scratch/q7-ld29-d25-branches78-80/branch-${b}.cnf \
  /scratch/q7-ld29-d25-branch-${b}.drat

drat-trim \
  /scratch/q7-ld29-d25-branches78-80/branch-${b}.cnf \
  /scratch/q7-ld29-d25-branch-${b}.drat -w
```

Run the independent solver cross-check with

```bash
/scratch/q7-ld29-d25-branches78-80-venv/bin/python \
  verify_branches78_80.py --solve-kissat
```

Reported environment and package hashes:

```text
Python                         3.11.2
python-sat[pblib]              1.9.dev15
CaDiCaL Debian package         1.5.3-2
CaDiCaL package SHA-256        ad30fec9e44fc6d7df39ba88efdd3f132bff24a4a6d422e26c73cc2cabbde1b3
DRAT-trim Debian package       0.0~git20240428.effa1dc-2
DRAT-trim package SHA-256      a2613ed11f3b2ee1a183ed64ba265a7d88b9b892cef1a40a9097132ccabcc31f
requirements.txt SHA-256       639afc203e4b12224d62c9426902d5784099ba876c5ac2faed92e4659b56caca
verify_branches78_80.py SHA-256 bb72701b17af8bf50687452ca856d44315f162ff27f21317c6e4c468c4be3ffe
```

## Trust boundary, scope, and novelty

The analytic theorem depends on the Honkala--Laihonen--Ranto family
partition, the reviewed orphan-local reduction, the preceding local-slot
collision count, and elementary Hamming-cube geometry.  Its finite part is
a transparent enumeration of the integer capacity frontier and two
six-vertex graph invariants.  The exact exclusions add the deterministic
encoding, PySAT cardinality encodings, and DRAT-trim to the trust boundary.
DRAT proves only the two hashed formulas; the analytic bridge is separate.

The family method is from I. Honkala, T. Laihonen, and S. Ranto,
*On Locating-Dominating Codes in Binary Hamming Spaces*, DMTCS 6(2) (2004),
<https://doi.org/10.46298/dmtcs.322>.  V. Junnila, T. Laihonen, and
T. Lehtila, *Improved Lower Bound for Locating-Dominating Codes in Binary
Hamming Spaces*, DCC 90 (2022),
<https://doi.org/10.1007/s10623-021-00963-8>, records
`28 <= gamma^LD(Q_7) <= 32` and improves the general lower bound only from
dimension ten.

Targeted primary-source and refreshed Discovery Net searches through
2026-09-01 found no full-family/independence-number specialization or exact
certificate for either local branch.  The new analytic refinement and the
two exclusions are apparently new to the searched sources; no historical
priority claim is made.
