# Full-family split and DRAT exclusion of `Q_7` LD29 branches 70--71

## Certified result

There is no locating-dominating code of cardinality at most 29 in the
binary 7-cube whose lossless orphan normalization has canonical local-graph
index 70 or 71.

| branch | mask | sorted degrees | triangles | independence number |
|---:|---:|:---|---:|---:|
| 70 | 1887 | `(2,2,3,3,3,5)` | 4 | 3 |
| 71 | 1915 | `(2,2,2,4,4,4)` | 4 | 3 |

The proof generalizes the branch-69 full-family split.  Each branch is
covered by one strong `D>=25` formula and a complete split into 16
defect-24 exceptional formulas.  All 34 exact CNFs have independently
checked DRAT certificates.  This closes two further finite branches; it
does not prove that a 29-word code is impossible.

## Common defect-24 split

After the lossless orphan normalization, the local fathers in either graph
use 12 Honkala--Laihonen--Ranto defect units, have capacity 45, and force
26 distinct absent son slots.  With total defect `D`, couples `q`, and
family vertices `M`, the standard identities are

$$
p=24+D,\qquad M=104-D-2q,\qquad
a\geq D-5,\qquad 2q\leq34-D.
$$

The universal theorem gives `D>=18`.  For `D=18,...,23`, exact integer
partitions give

```text
D                 18  19  20  21  22  23
G(D-12)           29  33  37  41  45  51
max(total deficit) 4   7  12  15  20  25
```

The last row is `45+G(D-12)-min M`; it is always below the 26 forced
slots.  Hence both branches have `D>=24`.

At `D=24`, capacity enumeration followed by the defect-six occupancy
inequality leaves exactly

```text
q=5, extra defects=(1,1,5,5), free missing=1, family-codeword budget=0;
q=5, extra defects=(2,5,5),   free missing=0, family-codeword budget=0.
```

Thus there are two noncodeword defect-five centers with all seven
neighbors selected and at most one extra missing slot.  The standard
separation argument puts their distance at least five: distances 1--4
contradict an all-codeword neighborhood or force at least two missing
slots.

The center cost is the same as in branch 69.  A valid weight-three center
is a local triangle and costs one; a weight-four center costs at least its
number of supported local edges; a weight-five center costs at least three
because independence number three forces a selected local word in its
support; and weights six and seven receive the safe lower bound zero.
Weights at most two are impossible.  Exhaustion of all 8,128 unordered
vertex pairs at distance at least five and total cost at most one gives
exactly 16 cases per branch:

```text
branch 70:
(22,111) (22,113) (22,123) (22,125)
(26,111) (26,113) (26,119) (26,125)
(42, 95) (42,113) (42,119) (42,125)
(63, 70) (70,113) (70,123) (70,125)

branch 71:
(14,113) (14,119) (14,123) (14,125)
(28,111) (28,113) (28,119) (28,123)
(42, 95) (42,113) (42,119) (42,125)
(63, 70) (70,113) (70,123) (70,125)
```

Every listed pair has cost exactly one; therefore the zero-slack state has
no candidate.

## Exact formulas and certificates

For each branch, the strong formula covers `D>=25` using `p>=49`, at most
nine nonisolated codewords, `p+b<=58`, and at most 13 induced code edges.
The exceptional formulas use the valid `D>=24` bounds `p>=48`, `b<=10`,
`p+b<=58`, and at most 15 induced edges, then fix the two centers absent
and their fourteen neighbors present.  They are relaxations of the
corresponding family cases.

Every formula additionally contains exact domination and distance-two
separation, exact cardinality 29, the full orphan normalization, all 15
local units, and biconditional count indicators.  A strong formula has
10,432 variables and 183,619 clauses; an exceptional formula has 10,432
variables and 183,635 clauses.

CaDiCaL 1.5.3 emitted plain-text DRAT traces.  DRAT-trim
`0.0~git20240428.effa1dc-2` returned `s VERIFIED` on all 34 exact pairs,
with zero RAT lemmas in every core.  The strong records are:

| branch | CNF SHA-256 | proof bytes | DRAT SHA-256 | core/total lemmas | resolution steps |
|---:|:---|---:|:---|---:|---:|
| 70 | `c15e526b8e8acf4801cfe8d2a14aeeca9183ffa4c873bee9a99d60ea937999bf` | 210,933,348 | `57fb644055dc66a49686e0c3273d360f597c5355ea1a5e0e46f40b9de43bbcdf` | 852,687/1,368,811 | 42,410,328 |
| 71 | `9975be3ae30866bfa171a27a86cc7ada85f3282dedf1781d93d0c80b1f9f1bf2` | 139,994,770 | `80c23b3fbe7124842a6c4139a92c6368515e94ebe34851c79948504a8f829e28` | 572,791/918,255 | 32,043,956 |

The 32 exceptional proofs have 734,660--2,131,542 bytes; their cores use
577--5,819 lemmas and 17,638--258,051 resolution steps.  The versioned
`certificate_manifest.tsv` records every formula name, exact CNF hash,
proof byte count, proof hash, and checker statistic.  CNFs, traces, and
checker logs stay under `/scratch` and are deliberately not committed.
PySAT's Kissat 4.0.4 binding independently returned UNSAT on all 34 freshly
regenerated formulas.

## Reproduction

The verifier digest-pins and reuses the branch-69 split kernel.

```bash
python3 -m venv /scratch/q7-ld29-branches70-71-venv
/scratch/q7-ld29-branches70-71-venv/bin/pip install -r requirements.txt
/scratch/q7-ld29-branches70-71-venv/bin/python \
  verify_branches70_71_split.py \
  --write-directory /scratch/q7-ld29-branches70-71
```

For every generated formula:

```bash
cadical -q --binary=false FORMULA.cnf FORMULA.drat
drat-trim FORMULA.cnf FORMULA.drat -w
```

An independent Kissat cross-check is available with

```bash
/scratch/q7-ld29-branches70-71-venv/bin/python \
  verify_branches70_71_split.py --solve-kissat
```

The reported environment used Python 3.11.2,
`python-sat[pblib]==1.9.dev15`, CaDiCaL 1.5.3, DRAT-trim
`0.0~git20240428.effa1dc-2`, and the Kissat 4.0.4 PySAT binding.

## Trust boundary and novelty

The analytic proof depends on the Honkala--Laihonen--Ranto family
partition, the reviewed orphan-local reduction, elementary cube geometry,
and exhaustive integer/128-vertex enumeration.  The finite exclusions add
the deterministic SAT encoding, PySAT totalizers, CaDiCaL proof production,
and DRAT-trim to the trust boundary.  DRAT proves only the 34 hashed
formulas; the analytic bridge is separate.

The family method is from Honkala--Laihonen--Ranto, DMTCS 6(2) (2004),
<https://doi.org/10.46298/dmtcs.322>.  Junnila--Laihonen--Lehtila, DCC 90
(2022), <https://doi.org/10.1007/s10623-021-00963-8>, records the prior
interval `28 <= gamma^LD(Q_7) <= 32`.  Targeted primary-source and
Discovery Net searches through 2026-09-01 found no full-family split or
exact certificates for branches 70--71.  The result is apparently new to
the searched sources; no historical-priority claim is made.
