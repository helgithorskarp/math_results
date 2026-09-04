# A low-edge-orbit four-cycle obstruction for Ramsey `K_43`

Let `G` be a graph on 43 vertices with neither a clique nor an independent
set of order five.  If an automorphism of `G` has exactly four vertex cycles,
then its induced action on unordered vertex pairs has more than 34 orbits.

The bound excludes all 393 exactly-four-cycle types with 26 through 34 edge
orbits.  This is an exact computer-assisted obstruction theorem.  It does
**not** construct a 43-vertex Ramsey graph, improve the lower bound for
`R(5,5)`, or exclude the four-cycle actions with 36 or more edge orbits.

## The minimal structured stratum

For cycle lengths `a,b,c,d`, the induced number of edge orbits is

```text
sum_i floor(a_i/2) + sum_{i<j} gcd(a_i,a_j).           (1)
```

The first sum counts cyclic distance classes inside each vertex cycle; the
second counts diagonal classes between two cycles.  Because the four lengths
sum to the odd number 43, either one or three of them are odd.  The first sum
in (1) is then 21 or 20, respectively, while the six gcd terms are each at
least one.  Thus every four-cycle action has at least 26 edge orbits.

Direct enumeration gives 588 unordered four-part partitions of 43.  Their
first five edge-orbit strata contain 131, 33, 82, 120, and 27 types at 26,
28, 30, 32, and 34 orbits, respectively.  The 131 minimum types equivalently
have three odd parts and all six pairwise gcds equal one.

Every vertex of a target graph has degree in `[18,24]`: its neighborhood is
`K_4`-free, the equality `R(4,5)=25` gives the upper bound, and applying the
same argument to the complement gives the lower bound.  Inside a cycle of
odd length `l`, an invariant graph has any even degree in
`0,2,...,l-1`.  For even `l`, the antipodal matching gives every degree in
`0,1,...,l-1`.  Selecting one of the `gcd(l,m)` cross orbits between two
cycles adds `m/gcd(l,m)` and `l/gcd(l,m)` to their respective degrees.

Enumerating these integer choices gives the exact census

```text
edge orbits                 26   28   30   32   34   total
cycle types                131   33   82  120   27     393
degree-infeasible           56   11   35   46    6     154
certificate cases           75   22   47   74   21     239
```

Thus the 239 survivor formulas have 26, 28, 30, 32, or 34 Boolean
edge-orbit variables.

## Exact SAT certificates

For a five-set `A`, let `M(A)` be the set of edge-orbit variables met by its
ten edges.  It is nonmonochromatic exactly when the two clauses

```text
OR_{i in M(A)} x_i
OR_{i in M(A)} not x_i
```

both hold.  `generate_proofs.py` constructs edge orbits by walking the
permutation, enumerates all `C(43,5)=962,598` five-sets, deduplicates their
masks, and emits these clauses.  A final unit clause fixes the first orbit
red; global color complementation makes this equisatisfiable.

The 239 formulas have 2,325 to 21,247 clauses.  PySAT Glucose 4.2 reports
every one UNSAT and emits the checked-in DRUP traces in [`proofs/`](proofs/),
[`proofs_28_30/`](proofs_28_30/), and [`proofs_32_34/`](proofs_32_34/).  The
initial screen was configured to halt on a satisfiable instance and write its
complete red edge list; `screen_strata.py` preserves that optional workflow.

`verify_proofs.py`, `verify_next_proofs.py`, and `verify_mid_proofs.py` do not
import the generators or PySAT.  Using only the standard library, they
independently:

- enumerates four-part partitions with nested loops;
- checks degree feasibility by a direct Cartesian product of cross-orbit
  counts, rather than the generator's reachable-vector dynamic program;
- canonicalizes each edge by taking its least repeated permutation image,
  rather than walking an unused-edge set;
- regenerates every five-set mask, CNF hash, proof hash, and byte count; and
- replay 9,645 proof additions by reverse unit propagation, deriving the
  empty clause in every one of the 239 instances.

The traces contain 51,416 deletion hints.  The checker soundly ignores them
and retains every already derived clause, which can only strengthen unit
propagation.  All 239 traces total 1,108,923 bytes.  Therefore solver
correctness is not trusted for the final UNSAT conclusion.

## Reproduction

Proof checking needs Python 3.11 or later and no third-party package:

```bash
bash verify.sh
```

Proof regeneration additionally needs the pinned SAT package:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python generate_proofs.py \
  --proof-dir proofs.regenerated \
  --result proof_manifest.regenerated.json
.venv/bin/python generate_next_proofs.py \
  --proof-dir proofs_28_30.regenerated \
  --result proof_manifest_28_30.regenerated.json
.venv/bin/python generate_mid_proofs.py \
  --proof-dir proofs_32_34.regenerated \
  --result proof_manifest_32_34.regenerated.json

diff -qr proofs proofs.regenerated
cmp proof_manifest.json proof_manifest.regenerated.json
diff -qr proofs_28_30 proofs_28_30.regenerated
cmp proof_manifest_28_30.json proof_manifest_28_30.regenerated.json
diff -qr proofs_32_34 proofs_32_34.regenerated
cmp proof_manifest_32_34.json proof_manifest_32_34.regenerated.json
```

The manifest records every omitted DIMACS SHA-256 and every proof hash.  With
`python-sat==1.9.dev15`, regeneration is byte-for-byte deterministic.  The
calculation uses one process, exact integer operations, and no randomness,
floating point, network input, or external instance.

## Scope, provenance, and trust boundary

The result excludes 393 exactly-four-cycle types and leaves the other 195
four-cycle types open.  It says nothing about asymmetric colorings or
automorphisms having a different number of vertex cycles.  The edge-orbit
cutoff is a computational scope boundary; 26 is the absolute structural
minimum.

The mathematical trust boundary consists of formula (1), the degree sieve,
the known equality `R(4,5)=25`, the invariant-coloring SAT encoding, the two
independent reconstruction programs, the checked proof bytes, and ordinary
Python semantics.  Proof replay removes Glucose from the final trust
boundary.

McKay and Radziszowski's
[*Subgraph counting identities and Ramsey numbers*](https://doi.org/10.1002/jgt.3190190304)
supplies `R(4,5)=25`.  Exoo's
[*A lower bound for R(5,5)*](https://doi.org/10.1002/jgt.3190130113) and Ge,
Jayasooriya, Qiu, Sun, and Yuan's
[*Study of Exoo's lower bound for Ramsey number R(5,5)*](https://arxiv.org/abs/2212.12630)
motivate structured 43-vertex colorings.  Angeltveit and McKay's
[*R(5,5) <= 46*](https://arxiv.org/abs/2409.15709) supplies current upper-bound
context.  The inspected primary sources and Discovery Net graph at indexed
height 2034 did not state this low-orbit four-cycle obstruction; novelty is
claimed only relative to those checked sources, not as a universal priority
claim.
