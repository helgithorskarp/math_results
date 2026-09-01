# Codeword-couple closure of `Q_7` LD29 branches 61 and 62

## Certified result

There is no locating-dominating code of cardinality at most 29 in the binary
7-cube whose lossless orphan normalization has canonical local-graph index
61 or 62.  Equivalently, both branches are empty.

The proof has two parts.  The predecessor establishes that every code in
either branch would have total Honkala--Laihonen--Ranto family defect exactly
`D=24`.  At this exact layer, finite family arithmetic forces at least one
codeword couple.  A single DRAT-certified formula for each branch then
excludes all possible locations of such a couple, modulo the complete local
stabilizer.

The canonical local masks are `5941` and `5948`.  Both have sorted degree
sequence `(2,2,3,3,3,3)`, two triangles, independence number two, and an
order-four stabilizer fixing the orphan coordinate.

## Why exact defect 24 forces a couple

Let `q` be the number of codeword couples.  The six local fathers in either
branch use ten defect units, have capacity 36, and force 20 distinct missing
son slots.  For total defect `D=24`, the remaining defect partitions are
enumerated together with

```text
family vertices          M = 104-D-2q,
family-codeword budget       34-D-2q,
defect-six occupancy cost    max(0, 8r-s),
```

where `r` is the number of extra defect-six families and `s` is the free
missing-slot budget.  Exactly 89 arithmetic states survive in each branch:

| couples `q` | 1 | 2 | 3 | 4 | 5 |
|---:|---:|---:|---:|---:|---:|
| states | 3 | 5 | 11 | 24 | 46 |

There is no state with `q=0`.  Thus a hypothetical exact-defect-24 code has
an adjacent pair `c_1,c_2` with

```text
I(c_1) = I(c_2) = {c_1,c_2};
```

in other words, an isolated edge component in the graph induced by the
codewords.

## Exhausting the couple locations

The established lossless normalization fixes

```text
0 in C;
e_i not in C                         (0 <= i < 7);
e_0+e_j not in C                     (1 <= j < 7),
```

and fixes all 15 weight-two local-graph literals.  Exactly 200 of the 448
cube edges remain compatible with these unit clauses as possible codeword
couples.  The order-four local stabilizers partition them into 58 orbits in
branch 61 and 76 orbits in branch 62.

For each orbit representative `uv`, a selector implies that `u,v` are
codewords and that their other twelve neighbors are noncodewords.  One final
clause requires at least one selector.  This is lossless: every forced
couple can be carried to a representative by a coordinate permutation that
preserves the normalized branch.

The common exact formula also contains domination of all 128 vertices,
every essential distance-two separation clause, exact cardinality 29, the
complete normalization, biconditional singleton/nonisolation/code-edge
indicators, and the exact-defect-24 consequences

```text
singleton signatures p = 48,
nonisolated codewords b <= 10,
p+b <= 58,
induced code edges <= E_7(10) = 15.
```

Both selector formulas are UNSAT.  CaDiCaL `sc2021` emitted plain-text DRAT
traces, and DRAT-trim returned `s VERIFIED` on both exact formula/proof
pairs.  The certificate measurements and hashes are recorded in
`certificate_manifest.tsv`.

| branch | variables | clauses | CNF SHA-256 | proof bytes | DRAT SHA-256 | core/total lemmas | resolution steps |
|---:|---:|---:|:---|---:|:---|---:|---:|
| 61 | 11,386 | 193,457 | `685d071c82ce9325653f438d90f7822a12f6f666f713af4c9dabc5cecb4f51db` | 1,107,470,946 | `672c2cbbf6bba06408c0dcb7628fa36dc17e4a9622b789f767f7e6d79a0c51ad` | 3,743,287/6,202,229 | 216,497,208 |
| 62 | 11,404 | 193,709 | `af2c03482eff31a48d492b42bb919a507e18399e83c6aa96edb05c56a5f8e897` | 1,119,486,852 | `43be85229ed3ee21598d12200f6eecae5346236e304f64eb4e91a48381bd4d9a` | 3,816,807/6,307,699 | 224,272,585 |

The checked cores use 4,728 and 5,100 original clauses, respectively, with
zero RAT lemmas in either core.

As a solver-level cross-check independent of the selector disjunction,
PySAT CaDiCaL 1.9.5 was run incrementally on the common base formula with
each representative's fourteen defining literals as assumptions.  All 58
and all 76 calls returned UNSAT.

## Reproduction

Create the environment under `/scratch` and regenerate the formulas:

```bash
python3 -m venv /scratch/q7-ld29-couple-closure-venv
/scratch/q7-ld29-couple-closure-venv/bin/pip install -r requirements.txt
/scratch/q7-ld29-couple-closure-venv/bin/python \
  verify_couple_closure.py \
  --write-directory /scratch/q7-ld29-couple-closure
```

Produce and check each external certificate:

```bash
cadical -q --binary=false FORMULA.cnf FORMULA.drat
drat-trim FORMULA.cnf FORMULA.drat -w
```

The slower independent orbit-by-orbit cross-check is available as

```bash
/scratch/q7-ld29-couple-closure-venv/bin/python \
  verify_couple_closure.py --solve-incrementally
```

Reported environment:

```text
Python                              3.11.2
python-sat[pblib]                   1.9.dev15
CaDiCaL proof producer              sc2021
CaDiCaL executable SHA-256          c6de62662723ec4a7426c5ca2bc9bfb04c60aad81a423957e3cd1ffadd0f8aa7
DRAT-trim Debian package            0.0~git20240428.effa1dc-2
DRAT-trim executable SHA-256        bc7543a99da8521ddb09af442698956054f11e10d198bd482ac756535244c021
requirements.txt SHA-256            639afc203e4b12224d62c9426902d5784099ba876c5ac2faed92e4659b56caca
verify_couple_closure.py SHA-256     881a95c59153bd77fd81858a21ff176a087a809caf65bcd7be634cede89d4699
```

CNFs, proofs, solver output, and checker logs remain under `/scratch` and
are not committed.

## Trust boundary and context

The branch exclusion combines the independently certified predecessor
`D=24` theorem, exact integer enumeration of the family-capacity states, an
exhaustive local-stabilizer orbit computation, a deterministic Boolean
encoding, PySAT totalizers, CaDiCaL proof production, and DRAT-trim.  The
DRAT certificates establish UNSAT only for the two hashed selector formulas;
the analytic exact-defect and forced-couple reductions are separate,
version-pinned dependencies.

The family method is due to I. Honkala, T. Laihonen, and S. Ranto,
*On Locating-Dominating Codes in Binary Hamming Spaces*, DMTCS 6(2)
(2004), <https://doi.org/10.46298/dmtcs.322>.  V. Junnila, T. Laihonen,
and T. Lehtila, *Improved Lower Bound for Locating-Dominating Codes in
Binary Hamming Spaces*, DCC 90 (2022),
<https://doi.org/10.1007/s10623-021-00963-8>, records the published interval
`28 <= gamma^LD(Q_7) <= 32`.

Targeted primary-source and refreshed Discovery Net searches through
2026-09-01 found no prior exclusion of these normalized branches.  The
branch closure is apparently new relative to the searched sources; no
historical-priority claim is made.
