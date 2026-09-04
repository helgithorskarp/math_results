# No order-eleven automorphism in a Ramsey `(5,5,43)` coloring

Let `G` be a graph on 43 vertices with neither a clique nor an independent
set of order five.  Then `Aut(G)` contains no element of order eleven.
Consequently, by Cauchy's theorem, `11` does not divide `|Aut(G)|`.

This is an exact computer-assisted structural theorem.  It does not
construct a 43-vertex Ramsey graph and does not improve a bound on `R(5,5)`.

## Exhaustion of cycle types

An order-eleven permutation has only fixed points and eleven-cycles.  If `f`
is its number of fixed points and `k>0` its number of eleven-cycles, then

```text
f + 11*k = 43.
```

The only possibilities are

```text
1^10 11^3,   1^21 11^2,   1^32 11^1.
```

For the canonical action with the fixed points first and each moving cycle
in a consecutive block, its edge orbits comprise

```text
C(f,2)                    fixed--fixed singleton orbits,
f*k                       fixed--cycle eleven-edge orbits,
5*k                       within-cycle eleven-edge orbits,
11*C(k,2)                 between-cycle eleven-edge orbits.
```

One Boolean variable records each edge orbit's color.  For every one of the
`C(43,5)=962,598` five-sets, the formula projects its ten edges to distinct
orbit variables and adds the two clauses requiring both colors.  Duplicate
clauses are removed.

## Exact centralizer normalization

The centralizer of the order-eleven action supplies three compatible
normalizations:

1. Sort the `k` cycles by their five internal-distance bits.
2. In that cycle order, sort the `f` fixed vertices by their `k` incidence
   bits to the cycles.
3. Choose cycle zero as phase anchor and independently rotate each other
   cycle until its eleven-bit cross word with the anchor is lexicographically
   least among its rotations.

Cycle permutations, fixed-point permutations, and independent rotations are
all in the centralizer.  Internal profiles and fixed-to-cycle incidences are
phase invariant, so each step preserves the previous ones.  Thus these
blocking clauses retain at least one representative of every invariant
coloring orbit.

For `1^32 11^1`, one additional exact degree consequence is used.  The known
equality `R(4,5)=25` forces every target degree into `[18,24]`.  Sorting the 32
fixed-to-cycle incidence bits makes them a threshold word.  If `T` is their
number of ones and `S` is the number of red internal distances of the moving
eleven-cycle, every moving vertex has degree

```text
T + 2*S.
```

For each of the 32 internal patterns, two conditional boundary clauses
encode `18 <= T+2*S <= 24`.  `test_exact.py` checks all `33*32=1,056`
threshold/internal assignments.  No color unit, auxiliary variable,
heuristic clause, or random choice is used in any case.

The resulting exact instances and proofs are:

| fixed points | 11-cycles | variables | clauses | RUP additions | deletions | proof bytes |
|---:|---:|---:|---:|---:|---:|---:|
| 10 | 3 | 123 | 177,074 | 15,002 | 15,770 | 1,116,802 |
| 21 | 2 | 273 | 208,332 | 4,039 | 1,000 | 223,410 |
| 32 | 1 | 533 | 535,001 | 20 | 0 | 225 |
| total | | | | 19,061 | 16,770 | 1,340,437 |

## Independent reconstruction and proof replay

`generate_formula.py` constructs each edge orbit by minimizing over the
eleven powers of the permutation.  The standalone `verify.py` does not
import that generator or PySAT.  It instead uses disjoint-set union under one
permutation step, independently rebuilds the Ramsey clauses and symmetry
breakers using integer pattern enumeration, verifies each omitted DIMACS
hash and checked proof hash, and replays every proof addition by reverse unit
propagation.

PySAT Glucose 4.2 generated the traces in [`proofs/`](proofs/).  The verifier
soundly ignores deletion hints and retains every already certified derived
clause.  Inductively these clauses are consequences of the original formula,
and retaining them can only strengthen unit propagation.  Every trace derives
the empty clause, so Glucose correctness is not part of the final trust
boundary.

## Reproduction

Proof checking needs Python 3.11 or later and no third-party package:

```bash
bash verify.sh
```

Proof regeneration additionally needs the pinned SAT package:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

mkdir -p proofs.regenerated
for fixed in 10 21 32; do
  python3 generate_formula.py --fixed "$fixed" "f${fixed}.regenerated.cnf"
  .venv/bin/python generate_proof.py \
    "f${fixed}.regenerated.cnf" "proofs.regenerated/f${fixed}.drat"
done
.venv/bin/python build_manifest.py \
  --proof-dir proofs.regenerated --result result.regenerated.json

diff -qr proofs proofs.regenerated
cmp result.json result.regenerated.json
```

The checked-in manifest records the omitted formula hashes and all proof
hashes.  With `python-sat==1.9.dev15`, formulas, proofs, and the manifest
regenerate byte-for-byte.  The computation is single-process and uses exact
integer operations with no randomness, floating point, network input, or
external instance.

## Scope and provenance

This theorem excludes order-eleven elements, not all nontrivial
automorphisms.  Its centralizer normalizations adapt the method in the sibling
[`order-seven obstruction`](../ramsey_r55_no_order7_automorphism), while the
formulas, proofs, and independent verifier here are separate.

Exoo's [*A lower bound for R(5,5)*](https://doi.org/10.1002/jgt.3190130113)
and Ge, Jayasooriya, Qiu, Sun, and Yuan's
[*Study of Exoo's lower bound for Ramsey number R(5,5)*](https://arxiv.org/abs/2212.12630)
provide the structured-coloring context.  McKay and Radziszowski's
[*Subgraph counting identities and Ramsey numbers*](https://doi.org/10.1002/jgt.3190190304)
supplies `R(4,5)=25`.  Angeltveit and McKay's
[*R(5,5) <= 46*](https://arxiv.org/abs/2409.15709) gives current upper-bound
context.  The inspected primary sources and Discovery Net graph at indexed
height 2034 did not state this order-eleven obstruction.  Novelty is claimed
only relative to those inspected sources, not as a universal priority claim.
