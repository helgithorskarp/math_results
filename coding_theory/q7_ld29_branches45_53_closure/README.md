# Codeword-couple closure of `Q_7` LD29 branches 45 and 53

## Certified result

There is no locating-dominating code of cardinality at most 29 in the binary
7-cube whose lossless orphan normalization has canonical local-graph index 45
or 53.  The branches have masks 759 and 1781, respectively.

Together with the preceding exact exclusions, every hypothetical code of
cardinality at most 29 is now confined to the 51 normalized branches

```text
0--43, 46, 48--49, 51, or 54--56.
```

This closes two further branches.  It does not exclude the remaining 51
branches and does not yet prove the exact value of the locating-domination
number of `Q_7`.

## Complete defect split

Use the established exact-29 normalization

```text
0 in C;
e_i not in C                         (0 <= i < 7);
e_0+e_j not in C                     (1 <= j < 7).
```

Let `D` be the total Honkala--Laihonen--Ranto family defect.  The reviewed
predecessor proves `D>=24` in both branches.  For the number `p` of singleton
signatures, number `b` of nonisolated codewords, and induced code edges, the
standard family identities and binary edge-isoperimetric bound give

```text
p = 24+D,  b <= 34-D,  p+b <= 58,  e(Q_7[C]) <= E_7(b).
```

If `D>=25`, the relaxed necessary conditions are

```text
p >= 49,  b <= 9,  p+b <= 58,  e(Q_7[C]) <= 13.
```

One exact locating-domination CNF per branch imposes these bounds together
with cardinality 29, the complete normalization, and all 15 local-graph units.
The checked UNSAT proofs exclude the whole range `D>=25`.

It remains to exclude exact defect `D=24`.  Both local graphs have local
defect 10, local family capacity 36, and forced local missing-slot count 20.
Complete integer-state enumeration followed by the established defect-six
occupancy inequality leaves 89 states in each branch.  Their codeword-couple
distribution is

```text
q=1: 3,  q=2: 5,  q=3: 11,  q=4: 24,  q=5: 46.
```

In particular, every surviving state contains an induced codeword couple.
Such a couple is a cube edge whose endpoints are selected and whose other 12
neighbors are absent.

## Complete symmetry cover

Compatibility with the fixed normalization leaves 206 candidate couple edges
in branch 45 and 203 in branch 53.  The exact stabilizers of the two local
graphs have orders four and one.  Quotienting the candidate edges gives 78 and
203 orbits, respectively.

For each branch, one aggregate exact-`D=24` formula assigns a selector to every
orbit representative.  A selector implies the 14 defining couple literals,
and one selector is required.  Hence every mathematically surviving state is
covered by the formula.  Checked UNSAT of both aggregate formulas excludes
exact defect 24.  Together with the predecessor `D>=24` theorem and the two
`D>=25` exclusions, this closes both branches.

The earlier lossless reduction also covers codes of size below 29: any such
code can be extended to an exact 29-code while preserving
location-domination, after which the normalization applies.

## Exact formulas and certificates

The four formulas use the reviewed deterministic locating-domination encoding
and sequential PySAT totalizers.  Standalone CaDiCaL `sc2021` returned
`s UNSATISFIABLE` and emitted a plain-text DRAT trace for every formula.

| formula | variables | clauses | CNF SHA-256 | proof bytes | DRAT SHA-256 |
|:---|---:|---:|:---|---:|:---|
| `branch45-d25` | 10,432 | 183,619 | `65015fa6405fb52dcc859a52f3b931152dc6b387c029832e70813cd513aa6d7b` | 328,754,589 | `ca68654fa9e7357eb93227ba8486a3810aae2ae548323ff344252a029b2efc8a` |
| `branch45-d24-couple-selector` | 11,406 | 193,737 | `f8d3d640e937edc733e3378ff3c3886137c32817e7efe54ab05891745782ef3d` | 1,041,586,413 | `37d190349aceeaadf7fb9f2007c5ddad53ffaac67894425f76452a3ba0743bc0` |
| `branch53-d25` | 10,432 | 183,619 | `10283e81fd79d35c2cecc45d79506cd0c87b3ba7a82ad34854e03d7bfbdc8be9` | 382,387,319 | `47b29bcc0f6c3d1c540bfa44d48889ad1bba4c52228993344c1dffceb1c1c0e8` |
| `branch53-d24-couple-selector` | 11,531 | 195,487 | `4eb97680c952d41a5ce5a7e654d0fd7ddc7fc148cf6ad83b73f0991b8a1d1045` | 1,060,761,917 | `8a21c45febc039efb7afe5da3a556473488e444724245fcb672c0d5a77ac17c7` |

DRAT-trim returned `s VERIFIED` on all four exact CNF/proof pairs, with zero
RAT lemmas in every checked core.  In aggregate, the 2,813,490,238 proof bytes
have checked cores containing 19,777 original clauses and 10,309,238 of
16,807,176 proof lemmas, verified through 530,658,190 resolution steps.  The
compact manifest records the exact byte counts, hashes, checked-core
statistics, and checker timings.

## Reproduction

Create the pinned environment under `/scratch`:

```bash
python3 -m venv /scratch/q7-ld29-branches45-53-closure-venv
/scratch/q7-ld29-branches45-53-closure-venv/bin/pip install -r requirements.txt
```

Reconstruct the family-state split, both stabilizer quotients, and all four
formulas:

```bash
/scratch/q7-ld29-branches45-53-closure-venv/bin/python \
  verify_branches45_53_closure.py \
  --write-directory /scratch/q7-ld29-branches45-53-closure-reproduced
```

Expected final line:

```text
PASS couple-selector closure excludes branches 45 and 53; 51 normalized branches remain
```

For every generated formula, produce and check the proof under `/scratch`:

```bash
cadical -q --binary=false FORMULA.cnf FORMULA.drat
drat-trim FORMULA.cnf FORMULA.drat -w
```

The optional independent solver routes are `--solve-kissat` for the four
aggregate formulas and `--solve-incrementally` for every exact-24 couple
representative.  They are not part of the certificate reported here.

Reported environment and source hashes:

```text
Python                                  3.11.2
python-sat[pblib]                       1.9.dev15
CaDiCaL proof producer                  sc2021
CaDiCaL executable SHA-256              c6de62662723ec4a7426c5ca2bc9bfb04c60aad81a423957e3cd1ffadd0f8aa7
DRAT-trim Debian package                0.0~git20240428.effa1dc-2
DRAT-trim executable SHA-256            bc7543a99da8521ddb09af442698956054f11e10d198bd482ac756535244c021
requirements.txt SHA-256                639afc203e4b12224d62c9426902d5784099ba876c5ac2faed92e4659b56caca
verify_sibling_closures.py SHA-256       1069616e39ad4c39e46d0094f91c6e2a9efc13983229033add53cf5551ac4fe6
```

The verifier and manifest hashes are intentionally obtained from the final
committed files rather than pre-recorded here.

## Trust boundary and context

The theorem depends on the Honkala--Laihonen--Ranto family partition, the
reviewed lossless orphan normalization, and the reviewed `D>=24` predecessor
for branches 45 and 53.  The new analytic bridge is the complete exact-24
state enumeration and the deduction `q>=1`; the finite symmetry layer
reconstructs every compatible cube edge and both exact stabilizers.

The Boolean layer depends on the reviewed locating-domination encoding,
PySAT totalizers, CaDiCaL proof production, and DRAT-trim.  Each DRAT trace
proves only the unsatisfiability of its hashed CNF.  The deterministic source
connects those formulas to the mathematical cases.  CNFs, proof traces, and
solver/checker logs remain under `/scratch` and are deliberately not committed.

The family method is due to I. Honkala, T. Laihonen, and S. Ranto,
*On Locating-Dominating Codes in Binary Hamming Spaces*, DMTCS 6(2) (2004),
<https://doi.org/10.46298/dmtcs.322>.  V. Junnila, T. Laihonen, and T. Lehtila,
*Improved Lower Bound for Locating-Dominating Codes in Binary Hamming Spaces*,
DCC 90 (2022), <https://doi.org/10.1007/s10623-021-00963-8>, records the
published small-dimension context.

Targeted primary-source and Discovery Net searches through 2026-09-02 found
no prior exclusion of normalized branches 45 and 53.  This is apparently new
relative to those searches; no absolute historical-priority claim is made.
