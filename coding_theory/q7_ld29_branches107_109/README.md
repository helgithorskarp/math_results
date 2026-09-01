# DRAT exclusion of the last three 12-edge Q7 size-29 branches

## Certified result

There is no locating-dominating code of cardinality at most 29 in `Q_7`
whose lossless orphan normalization has canonical local-graph index 107,
108, or 109.

These are the last three unresolved 12-edge graphs on the six non-orphan
coordinate directions.  Their masks and complement types are:

| branch | mask | complement inside `K_6` |
|---:|---:|:---|
| 107 | 6143 | `K_{1,3}` plus two isolated vertices |
| 108 | 7167 | `P_4` plus two isolated vertices |
| 109 | 8159 | `P_3 + K_2` plus one isolated vertex |

The exact formulas combine:

- domination at every vertex;
- all essential distance-two separation clauses;
- cardinality exactly 29;
- the complete orphan normalization;
- all 15 unit clauses fixing the selected local graph; and
- the proved defect-18 consequences: at least 42 singleton identifying
  sets, at most 16 nonisolated codewords, `p+b<=58`, and at most 32 induced
  code edges.

Each formula has 10,432 variables and 183,619 clauses.  Standalone CaDiCaL
produced a plain-text DRAT proof for each formula, and DRAT-trim returned
`s VERIFIED` on every exact CNF/proof pair.

| branch | CNF SHA-256 | proof bytes | DRAT SHA-256 |
|---:|:---|---:|:---|
| 107 | `f41b48ef238d0682c8e30d54d6b53c1852d50ac709d8d732c5d4df9286f6e14e` | 108,768,272 | `2cb6e3cd575cc97a2c5684b8a37e7713b091b7d8db8914d16f4e7a4fcf9c5b45` |
| 108 | `73a3d3fa288009acc5e342e3be0ffac5885f132e6467dceddf1395e028a37714` | 129,994,194 | `af75f2bc49ba9417c87ac9dbfd6ff464c8bb225e03c0bd74dcc4b562ee81e845` |
| 109 | `6a736aad2eeb4e190d14414d800140bb41fc6c9b69d548c0ddfbd31712fce3e6` | 105,845,286 | `9e3d2bb9f1cb89d2f3c21ee54e4c453ba0a5e0a44d38cea9a5b091caa403c755` |

PySAT's Kissat 4.0.4 binding independently returned `UNSAT` in 281, 321,
and 304 wall-clock seconds, respectively, under a shared two-CPU host quota.
Those solver returns are cross-checks; the checked DRAT traces are the finite
certificates.

The proof files are deliberately not committed.  They remain under
`/scratch` and can be regenerated from the versioned generators.

## Consequence for the global search

The predecessor enumerated 115 canonical local graphs.  It certified
branches 110--114, covering one 12-edge graph and all graphs with 13--15
edges.  The separate branch-106 certificate excludes the 12-edge graph
whose complement is a triangle.  The three certificates here exclude every
other 12-edge graph.  Therefore a code of cardinality at most 29, if one
exists, has a normalized local graph in exactly one of branches 0--105.

Equivalently, the certified search frontier is reduced from 110 to

\[
\boxed{106\text{ canonical branches}},
\]

and every surviving local graph has between 4 and 11 edges.

This remains a search reduction, not a nonexistence proof.

## Reproduction

Regenerate and hash all three CNFs:

```bash
python3 verify_branches107_109.py \
  --write-directory /scratch/q7-ld29-d18-cnfs
```

For each branch `i` in `107 108 109`, produce and check a fresh proof:

```bash
cadical -q --binary=false \
  /scratch/q7-ld29-d18-cnfs/branch-i.cnf \
  /scratch/q7-ld29-d18-branch-i.drat

drat-trim \
  /scratch/q7-ld29-d18-cnfs/branch-i.cnf \
  /scratch/q7-ld29-d18-branch-i.drat
```

Replace `i` by the decimal branch number.  The source imports the reviewed
base encoding from `../q7_ld29_family_reduction` and the sharper bounds from
`../q7_ld29_defect18`.  The pinned Python dependency is
`python-sat[pblib]==1.9.dev15`.

## Trust boundary and novelty

This is an exact computer-assisted finite result.  Its trust boundary is the
reviewed locating-domination encoding, the defect-18 theorem, deterministic
CNF generation, CaDiCaL's proof production, and DRAT-trim's checker.  The
proofs establish only unsatisfiability of the three hashed formulas.

The result follows the graph review's recommendation to certify branches
incrementally.  It is new to the refreshed graph and closes a finite frontier
created there; no independent literature-priority claim is made.
