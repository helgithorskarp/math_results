# DRAT exclusion of Q7 size-29 orphan-local branch 106

## Certified finite result

There is no locating-dominating code of cardinality at most 29 in `Q_7`
whose lossless orphan normalization has local-graph representative 106.
This representative has mask `4095` and is the 12-edge graph

\[
K_6-K_3,
\]

where the missing triangle is on coordinate directions `4,5,6` in the
canonical labeling `1,...,6`.

The predecessor reduced every hypothetical code of cardinality at most 29
to one of canonical branches 0--109.  The defect-18 theorem strengthens the
necessary global bounds to

\[
p\geq42,qquad a\geq13,qquad e(Q_7[C])\leq32.
\]

Adding those bounds to the exact domination, distance-two separation,
cardinality-29, orphan-normalization, and 15 local-graph unit clauses gives
a CNF with

```text
variables = 10432
clauses   = 183619
sha256    = b239814a4d9e7b86cad4bf07cedd0723515c2ca7bb86930fd8fa6e36082829f3
```

Standalone CaDiCaL 1.5.3 returned `UNSATISFIABLE` and emitted a plain-text
DRAT proof.  Its exact proof hash was

```text
ae4446bfa09b2db7957953ae81cef03f6c041a664dfb4aba0442c136ec25dd45
```

DRAT-trim `0.0~git20240428.effa1dc-2` checked the exact CNF/proof pair and
returned

```text
s VERIFIED
```

The 78 MiB proof trace is deliberately not committed.  It remains under
`/scratch` and can be regenerated from the versioned source.  As a
solver-level cross-check independent of the DRAT-producing run, PySAT's
Kissat 4.0.4 binding also returned `UNSAT` on the same formula.

This removes one of the four 12-edge local graphs that survived the previous
certified reduction.  Exactly 109 canonical branches remain unresolved.

## Reproduction

Regenerate and hash the exact CNF:

```bash
python3 verify_branch106.py \
  --write-cnf /scratch/q7-ld29-d18-branch106.cnf
```

Produce and check a fresh proof:

```bash
cadical -q --binary=false \
  /scratch/q7-ld29-d18-branch106.cnf \
  /scratch/q7-ld29-d18-branch106.drat

drat-trim \
  /scratch/q7-ld29-d18-branch106.cnf \
  /scratch/q7-ld29-d18-branch106.drat
```

The generator imports the reviewed base encoding from
`../q7_ld29_family_reduction` and the sharper structural bounds from
`../q7_ld29_defect18`.  The pinned Python dependency is
`python-sat[pblib]==1.9.dev15`.

## Scope and trust boundary

This is an exact computer-assisted branch exclusion, not a proof that no
29-word code exists.  The mathematical trust boundary consists of the
reviewed SAT encoding, the defect-18 theorem, deterministic CNF generation,
CaDiCaL's DRAT output, and DRAT-trim's checker.  The checked proof establishes
unsatisfiability of precisely the hashed CNF.  It does not say anything about
the other 109 branches.

The branch is a new finite consequence of the graph's existing reduction;
no independent literature-priority claim is made.  Incremental certification
of the remaining 12-edge branches 107--109 is the closest next target.
