# Center-orbit certificates raise `Q_7` LD29 branches 45 and 53 to `D>=24`

## Certified result

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

be the total Honkala--Laihonen--Ranto family defect.  If `H` has canonical
index 45 or 53, then

```text
D >= 24.
```

| branch | mask | sorted degrees | triangles | local capacity | forced deficit | independence number |
|---:|---:|:---|---:|---:|---:|---:|
| 45 | 759 | `(1,1,3,3,4,4)` | 4 | 36 | 20 | 3 |
| 53 | 1781 | `(1,2,3,3,3,4)` | 3 | 36 | 20 | 3 |

This improves the preceding branchwise bound `D>=23`.  It implies, in
either branch,

```text
p >= 48,  a >= 19,  b=29-a <= 10,  e(Q_7[C]) <= E_7(10)=15.
```

It does not yet exclude either branch and therefore does not by itself
reduce the 53-branch unresolved frontier.

## Exact defect-23 reduction

At `D=23`, the standard family identities and the established local
collision/occupancy inequalities leave exactly the same three states in
both branches:

| codeword couples `q` | extra family defects | free missing slots | family-codeword budget |
|---:|:---|---:|---:|
| 5 | `(1,1,1,5,5)` | 1 | 1 |
| 5 | `(1,2,5,5)` | 0 | 1 |
| 5 | `(3,5,5)` | 0 | 1 |

Every row contains two defect-five families.  Their fathers are
noncodewords: even assigning the only free missing slot to a selected
defect-five father would force at least six codewords into its family,
exceeding the complete family-codeword budget one.  All seven neighbors of
each father are therefore codewords.

The two centers have mutual Hamming distance at least five.  The established
one-slack full-family separation lemma excludes center distances one through
four: those distances respectively force a center to be a codeword, consume
one slot in each family, consume the two inward-neighbor slots, or consume at
least three predecessor slots.

## Complete center cover

The verifier classifies every one of the 128 possible center words.  The
unavoidable local cost, measured in missing son slots beyond the 20 already
forced by `H`, is as follows.

- Weights at most two are incompatible with the normalization and the
  all-codeword neighborhood.
- A weight-three center is possible only on a triangle of `H`, at cost one.
- A weight-four center costs the number of selected local edges in its
  support.  Because the independence number is three, cost zero is possible
  only when the orphan coordinate is present and the other three directions
  are independent.
- A weight-five center costs at least three: its non-orphan support contains
  a selected edge, whose distance-three relation consumes three predecessor
  slots.
- Weights six and seven have local cost zero.

No pair of zero-cost centers is at distance at least five, so the two
zero-slack states are impossible.  In the one-slack state exhaustive exact
enumeration leaves 20 unordered pairs in branch 45 and 12 in branch 53.
The stabilizer of branch 45 has order four and reduces its pairs to seven
orbits.  Branch 53 has trivial stabilizer, so its twelve pairs are already
inequivalent.  The 19 representatives are

```text
branch 45: (14,105) (14,113) (14,119) (14,123)
           (26,105) (26,111) (26,125)
branch 53: (22,111) (22,113) (22,123) (22,125)
           (28,111) (28,113) (28,119) (28,123)
           (44,95)  (44,113) (44,119) (44,123)
```

Words are encoded as integers from 0 through 127, with bits corresponding
to coordinates `0,...,6`.

## Exact certificate split

At `D=23`, the family bounds give

```text
p >= 47,  b <= 11,  p+b <= 58,  e(Q_7[C]) <= E_7(11)=17.
```

For each orbit representative, the exact formula imposes these necessary
conditions, fixes both centers outside `C`, and fixes all fourteen of their
neighbors inside `C`.  It also contains exact domination, every essential
distance-two separation clause, cardinality 29, the full orphan
normalization, all 15 local-graph units, and biconditional singleton,
nonisolation, and code-edge indicators.

Each formula has 10,432 variables and 183,635 clauses.  CaDiCaL `sc2021`
returned UNSAT and emitted a plain DRAT trace for every formula.  DRAT-trim
returned `s VERIFIED` on all 19 exact formula/proof pairs; every checked core
used zero RAT lemmas.  The aggregate certificate statistics are

```text
proof bytes          24,864,441
core clauses             27,728
core / total lemmas  47,367 / 365,815
resolution steps      1,940,327
```

PySAT's independent Kissat 4.0.4 binding also returned UNSAT on all 19
freshly regenerated formulas.  Thus no `D=23` state survives, and the
predecessor `D>=23` theorem proves `D>=24` in both branches.

## Reproduction

Create the environment and all generated files under `/scratch`:

```bash
python3 -m venv /scratch/q7-branches45-53-d24-venv
/scratch/q7-branches45-53-d24-venv/bin/pip install -r requirements.txt
/scratch/q7-branches45-53-d24-venv/bin/python \
  verify_branches45_53_d24.py \
  --write-directory /scratch/q7-branches45-53-d24-regenerated
```

For every generated CNF, produce and check the external certificate with

```bash
cadical -q --binary=false FORMULA.cnf FORMULA.drat
drat-trim FORMULA.cnf FORMULA.drat -w
```

Run the independent solver cross-check with

```bash
/scratch/q7-branches45-53-d24-venv/bin/python \
  verify_branches45_53_d24.py --solve-kissat
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
verify_branches45_53_d24.py SHA-256          e454f5bd525fa9a7fc212fab962b28978ae88ab4d8d7cb0d88f4401b50574d5e
certificate_manifest.tsv SHA-256             ee91c5dc3b97c172aacbc622045014eeadd59529f52a092d0239430198493760
```

The CNFs, DRAT traces, solver output, and checker logs remain under
`/scratch` and are deliberately not committed.  The manifest pins the exact
formula/proof hashes, sizes, and checker statistics.

## Trust boundary, sources, and scope

The analytic bridge depends on the Honkala--Laihonen--Ranto family
partition, the reviewed orphan-local reduction and branchwise defect ladder,
the earlier one-slack center-separation lemma, and elementary Hamming-cube
geometry.  Its finite part is a deterministic enumeration of integer states,
all 128 center positions, graph stabilizers, and pair orbits.  The external
DRAT traces prove unsatisfiability only for the 19 hashed formulas; the
analytic bridge and encoding generator remain source-level obligations.

The family method is due to I. Honkala, T. Laihonen, and S. Ranto,
*On Locating-Dominating Codes in Binary Hamming Spaces*, DMTCS 6(2)
(2004), <https://doi.org/10.46298/dmtcs.322>.  V. Junnila, T. Laihonen,
and T. Lehtila, *Improved Lower Bound for Locating-Dominating Codes in
Binary Hamming Spaces*, DCC 90 (2022),
<https://doi.org/10.1007/s10623-021-00963-8>, records the prior small-
dimension context.

Refreshed primary-source and Discovery Net searches through 2026-09-02
(graph height 1065) found no defect-24 specialization for branches 45 and
53.  This is apparently new relative to the searched sources; no absolute
historical-priority claim is made.
