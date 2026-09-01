# DRAT exclusion of `Q_7` size-29 local branch 59

## Certified finite result

There is no locating-dominating code of cardinality at most 29 in the
binary 7-cube whose lossless orphan normalization has canonical local-graph
index 59.  This is the eight-edge graph with canonical mask `5873`, sorted
degree sequence `(1,2,3,3,3,4)`, and four triangles.

This excludes one branch from the lower frontier.  It does not prove that a
29-word code is impossible; many canonical branches remain open.

## Analytic input and exact formula

The branchwise defect-ladder theorem proves `D>=24` in branch 59.  Its
standard consequences are

$$
p\ge48,\qquad a\ge19,\qquad b=29-a\le10,
\qquad e(Q_7[C])\le E_7(10)=15,
$$

and the family identities also give `p+b<=58`.

The deterministic formula contains:

- exact domination of all 128 vertices;
- every essential distance-two separation clause;
- exact cardinality 29;
- the complete orphan normalization;
- all 15 unit clauses fixing local graph 59;
- biconditional singleton, nonisolation, and code-pair indicators;
- `p>=48`, `b<=10`, `p+b<=58`, and `e(Q_7[C])<=15`.

Repeated endpoint literals in the predecessor's separation clauses are
removed clausewise, a Boolean identity.  The resulting DIMACS instance has

```text
variables  10,432
clauses   183,619
bytes   3,433,600
SHA-256 a548059e35430ff142b1a4cc719c401a945f24e9041c91626460525c521cfddf
```

CaDiCaL 1.5.3 returned `UNSATISFIABLE` and emitted a 514,801,349-byte
plain-text DRAT proof with SHA-256

```text
f939d7ea72f7f7f85aff597f82214fed0b5dec7323f57a24af3386aa9df4bd32
```

DRAT-trim `0.0~git20240428.effa1dc-2` independently returned `s VERIFIED`.
Its checked core used 2,070,218 of 3,027,388 lemmas and 107,748,250
resolution steps, with zero RAT lemmas.  PySAT's independent Kissat 4.0.4
binding also returned UNSAT on a freshly regenerated copy of the same
digest-checked formula.

## Reproduction

Create the environment under `/scratch`:

```bash
python3 -m venv /scratch/q7-ld29-branch59-venv
/scratch/q7-ld29-branch59-venv/bin/pip install -r requirements.txt
```

Regenerate and hash the exact CNF:

```bash
/scratch/q7-ld29-branch59-venv/bin/python verify_branch59.py \
  --write-cnf /scratch/q7-ld29-d24-branch59.cnf
```

Produce and check the external proof:

```bash
cadical -q --binary=false \
  /scratch/q7-ld29-d24-branch59.cnf \
  /scratch/q7-ld29-d24-branch59.drat

drat-trim \
  /scratch/q7-ld29-d24-branch59.cnf \
  /scratch/q7-ld29-d24-branch59.drat -w
```

Run the independent solver cross-check:

```bash
/scratch/q7-ld29-branch59-venv/bin/python verify_branch59.py --solve-kissat
```

The proof trace, CNF, and solver/checker output remain under `/scratch` and
are deliberately not committed.

Reported versions and package hashes:

```text
Python                         3.11.2
python-sat[pblib]              1.9.dev15
CaDiCaL Debian package         1.5.3-2
CaDiCaL package SHA-256        ad30fec9e44fc6d7df39ba88efdd3f132bff24a4a6d422e26c73cc2cabbde1b3
DRAT-trim Debian package       0.0~git20240428.effa1dc-2
DRAT-trim package SHA-256      a2613ed11f3b2ee1a183ed64ba265a7d88b9b892cef1a40a9097132ccabcc31f
requirements.txt SHA-256       639afc203e4b12224d62c9426902d5784099ba876c5ac2faed92e4659b56caca
verify_branch59.py SHA-256     b1d0ad1c5cdf101fcfab2600e3fa33f3732ee54d4e51b4d0809d438ef35951d0
```

## Trust boundary, scope, and novelty

The checked DRAT trace establishes exactly that the hashed CNF is
unsatisfiable.  The mathematical conclusion additionally depends on the
reviewed family/orphan reduction, the branchwise `D>=24` analytic bridge,
the deterministic encoding, Python/PySAT's totalizer generation, and
DRAT-trim.  Kissat is an independent solver cross-check, not the proof
checker.

The family method originates in Honkala--Laihonen--Ranto, *DMTCS* 6(2)
(2004), <https://doi.org/10.46298/dmtcs.322>.  Junnila--Laihonen--Lehtila,
*Designs, Codes and Cryptography* 90 (2022),
<https://doi.org/10.1007/s10623-021-00963-8>, records the prior
small-dimension bounds.  Targeted primary-source and refreshed graph
searches through 2026-09-01 found no exact certificate for this canonical
branch.  This is apparently new to the searched sources; no historical
priority claim is made.
