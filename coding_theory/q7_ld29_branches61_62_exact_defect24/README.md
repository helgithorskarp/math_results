# Exact defect concentration in `Q_7` LD29 branches 61 and 62

## Certified result

If a locating-dominating code of cardinality at most 29 in the binary
7-cube has lossless orphan-normalized local-graph index 61 or 62, then its
total Honkala--Laihonen--Ranto family defect is exactly

$$
\boxed{D=24}.
$$

The preceding one-slack full-family split proves `D>=24` in both branches.
This contribution excludes `D>=25` by two exact DRAT certificates.  It does
not exclude the remaining `D=24` layer, so neither local branch is closed.

The canonical local masks are `5941` and `5948`; both have sorted degree
sequence `(2,2,3,3,3,3)`, two triangles, and independence number two.

## Finite reduction

Let `C` be an exact 29-word locating-dominating code after the established
lossless normalization

```text
0 in C;
e_i not in C                         (0 <= i < 7);
e_0+e_j not in C                     (1 <= j < 7).
```

For total family defect `D`, singleton signatures `p`, isolated codewords
`a`, and nonisolated codewords `b=29-a`, the reviewed family identities and
edge bound give

$$
p=24+D,\qquad a\geq D-5,\qquad p+b\leq58,
\qquad e(Q_7[C])\leq E_7(b).
$$

Consequently `D>=25` implies

$$
p\geq49,\qquad b\leq9,\qquad p+b\leq58,
\qquad e(Q_7[C])\leq E_7(9)=13.
$$

For each branch, the deterministic exact formula contains domination of all
128 vertices, every essential distance-two separation clause, exact
cardinality 29, the complete orphan normalization, all 15 local-graph unit
clauses, biconditional singleton/nonisolation/code-edge indicators, and
precisely the four displayed numerical consequences.  Thus it is a
relaxation of every normalized code in that branch with `D>=25`; UNSAT is
sufficient to exclude that entire defect range.

Each formula has 10,432 variables, 183,619 clauses, and 3,433,600 bytes.

| branch | CNF SHA-256 | Kissat 4.0.4 | proof bytes | DRAT SHA-256 | core/total lemmas | resolution steps |
|---:|:---|---:|---:|:---|---:|---:|
| 61 | `bc3e7209f890eb96f370a8df089d66d8c279a2a0e0ab645c19cb8ddecd6267d7` | UNSAT, 979.141 s | 368,730,733 | `243f1ab9432c83b9bc4c5832528ffd19348dfbe7559730d331e31bd3f6d80a2b` | 1,466,469/2,429,447 | 81,103,403 |
| 62 | `571a3d012d5e0f84731967f7b345b2fee137a11e51cc0ee49ffcb068687a0360` | UNSAT, 837.726 s | 315,122,629 | `96da4954844413ce1f143fef26026570f5eed834a886e67a879467b7287fcc03` | 1,269,453/2,091,544 | 68,860,806 |

CaDiCaL `sc2021` independently returned `UNSATISFIABLE` and emitted the two
plain-text DRAT traces.  DRAT-trim returned `s VERIFIED` on both exact
formula/proof pairs, with zero RAT lemmas in either checked core.  The core
used 4,102 original clauses in branch 61 and 4,119 in branch 62.

`verify_exact_defect24.py` pins the SHA-256 of the source verifier for the
`D>=24` predecessor, reconstructs all 115 local-graph orbits, regenerates
both exact formulas, and checks their dimensions and SHA-256 digests.

## Reproduction

Create the environment under `/scratch` and regenerate both formulas:

```bash
python3 -m venv /scratch/q7-ld29-branches61-62-d25-venv
/scratch/q7-ld29-branches61-62-d25-venv/bin/pip install -r requirements.txt
/scratch/q7-ld29-branches61-62-d25-venv/bin/python \
  verify_exact_defect24.py \
  --write-directory /scratch/q7-ld29-branches61-62-d25
```

Produce and check each external certificate:

```bash
cadical -q --binary=false FORMULA.cnf FORMULA.drat
drat-trim FORMULA.cnf FORMULA.drat -w
```

Run the independent solver cross-check with

```bash
/scratch/q7-ld29-branches61-62-d25-venv/bin/python \
  verify_exact_defect24.py --solve-kissat
```

Reported environment and hashes:

```text
Python                              3.11.2
python-sat[pblib]                   1.9.dev15
CaDiCaL                             sc2021
CaDiCaL executable SHA-256          c6de62662723ec4a7426c5ca2bc9bfb04c60aad81a423957e3cd1ffadd0f8aa7
DRAT-trim Debian package            0.0~git20240428.effa1dc-2
DRAT-trim executable SHA-256        bc7543a99da8521ddb09af442698956054f11e10d198bd482ac756535244c021
requirements.txt SHA-256            639afc203e4b12224d62c9426902d5784099ba876c5ac2faed92e4659b56caca
predecessor verifier SHA-256        c91531e6cc12c993a2a59a8e83b2bcede8fba8fc50d4589eac415b28670456c9
verify_exact_defect24.py SHA-256     9500400daf4723912f56e5a0e3464a876fc18f52d279831ee38b1c34f6aef71e
```

CNFs, traces, and solver/checker output remain under `/scratch` and are not
committed.

## Trust boundary and scope

The exact-defect conclusion combines the independently checked predecessor
`D>=24` theorem with the deterministic Boolean encoding, PySAT totalizers,
CaDiCaL proof production, and DRAT-trim.  DRAT proves only the two hashed
`D>=25` relaxations; the analytic lower bound is a separate dependency.

The family method is from I. Honkala, T. Laihonen, and S. Ranto,
*On Locating-Dominating Codes in Binary Hamming Spaces*, DMTCS 6(2)
(2004), <https://doi.org/10.46298/dmtcs.322>.  V. Junnila, T. Laihonen,
and T. Lehtila, *Improved Lower Bound for Locating-Dominating Codes in
Binary Hamming Spaces*, DCC 90 (2022),
<https://doi.org/10.1007/s10623-021-00963-8>, records the prior interval
`28 <= gamma^LD(Q_7) <= 32`.

Targeted primary-source and refreshed Discovery Net searches through
2026-09-01 found no exact defect concentration or certificate for these two
local branches.  This computational narrowing is apparently new to the
searched sources; no historical-priority claim is made.
