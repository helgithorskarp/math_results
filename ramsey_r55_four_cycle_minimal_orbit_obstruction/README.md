# Complete four-cycle automorphism obstruction for Ramsey `K_43`

Let `G` be a graph on 43 vertices with neither a clique nor an independent
set of order five.  Then no automorphism of `G` has exactly four vertex
cycles.

This is an exact computer-assisted obstruction theorem covering all 588
unordered four-part cycle types.  It does **not** construct a 43-vertex
Ramsey graph, improve the lower bound for `R(5,5)`, or exclude asymmetric
graphs or automorphisms with a different number of vertex cycles.

## Structured census and degree obstruction

For cycle lengths `a,b,c,d`, the induced number of edge orbits is

```text
sum_i floor(a_i/2) + sum_{i<j} gcd(a_i,a_j).           (1)
```

The first sum counts cyclic distance classes inside each vertex cycle; the
second counts diagonal classes between two cycles.  Since the four lengths
sum to the odd number 43, (1) is at least 26.

Every vertex of a target graph has degree in `[18,24]`: its neighborhood is
`K_4`-free, the equality `R(4,5)=25` gives the upper bound, and applying the
same argument to the complement gives the lower bound.  Inside an odd cycle
of length `l`, an invariant graph has any even degree in `0,2,...,l-1`.
Inside an even cycle it has any degree in `0,1,...,l-1`, because the
antipodal matching contributes one.  Selecting one of the `gcd(l,m)` cross
orbits between two cycles adds `m/gcd(l,m)` and `l/gcd(l,m)` to the two
respective degrees.  Enumerating these exact integer choices gives:

```text
edge orbits        types   degree-infeasible   certificate cases
         26          131                  56                  75
         28           33                  11                  22
         30           82                  35                  47
         32          120                  46                  74
         34           27                   6                  21
         36           47                   8                  39
         38           57                  13                  44
         40           23                   1                  22
         42           17                   4                  13
         44           20                   3                  17
         46            5                   0                   5
         48           12                   0                  12
         50            4                   0                   4
         52            1                   0                   1
         54            4                   0                   4
         56            2                   0                   2
         60            1                   0                   1
         62            1                   1                   0
         66            1                   1                   0
      total          588                 185                 403
```

Thus the degree test alone eliminates 185 cycle types.  The remaining 403
formulas have 26 through 60 Boolean edge-orbit variables.

## Exact SAT certificates

For a five-set `A`, let `M(A)` be the set of edge-orbit variables met by its
ten edges.  It is nonmonochromatic exactly when both clauses

```text
OR_{i in M(A)} x_i
OR_{i in M(A)} not x_i
```

hold.  The generators construct edge orbits by walking the permutation,
enumerate all `C(43,5)=962,598` five-sets, deduplicate their masks, and emit
these clauses.  A final unit clause fixes the first orbit red; global color
complementation makes this equisatisfiable.

The 403 formulas have 2,325 to 100,437 clauses.  PySAT Glucose 4.2 reports
all of them UNSAT and emits the checked-in traces in [`proofs/`](proofs/),
[`proofs_28_30/`](proofs_28_30/),
[`proofs_32_34/`](proofs_32_34/), and
[`proofs_36_plus/`](proofs_36_plus/).  The initial screen was configured to
halt on a satisfiable instance and write its complete red edge list;
`screen_strata.py` preserves that optional workflow.

The verifier programs do not import the generators or PySAT.  Using only the
standard library, they independently:

- enumerate all four-part partitions of 43;
- check degree feasibility by a Cartesian product of cross-orbit counts,
  rather than the generator's reachable-vector dynamic program;
- canonicalize each edge by taking its least repeated permutation image,
  rather than walking an unused-edge set;
- regenerate every five-set mask, CNF hash, proof hash, and byte count; and
- replay 56,574 proof additions by reverse unit propagation, deriving the
  empty clause in every one of the 403 instances.

The traces contain 193,621 deletion hints.  The checker soundly ignores
them and retains every already certified derived clause: by induction those
clauses are consequences of the original formula, and retaining them can
only strengthen unit propagation.  All 403 traces total 6,425,526 bytes.
Therefore solver correctness is not trusted for the final UNSAT conclusion.

## Reproduction

Proof checking needs Python 3.11 or later and no third-party package:

```bash
bash verify.sh
```

The high-stratum checker supports `--only-cycle-type` and
`--exclude-cycle-type` so its unusually expensive `1+6+18+18` replay can be
run separately without changing the default all-case semantics.

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
.venv/bin/python generate_high_proofs.py \
  --proof-dir proofs_36_plus.regenerated \
  --result proof_manifest_36_plus.regenerated.json

diff -qr proofs proofs.regenerated
cmp proof_manifest.json proof_manifest.regenerated.json
diff -qr proofs_28_30 proofs_28_30.regenerated
cmp proof_manifest_28_30.json proof_manifest_28_30.regenerated.json
diff -qr proofs_32_34 proofs_32_34.regenerated
cmp proof_manifest_32_34.json proof_manifest_32_34.regenerated.json
diff -qr proofs_36_plus proofs_36_plus.regenerated
cmp proof_manifest_36_plus.json proof_manifest_36_plus.regenerated.json
```

Each manifest records every omitted DIMACS SHA-256 and every proof hash.
With `python-sat==1.9.dev15`, regeneration is byte-for-byte deterministic.
The calculation uses one process, exact integer operations, and no
randomness, floating point, network input, or external instance.

## Scope, provenance, and trust boundary

The result excludes exactly-four-cycle automorphisms.  It says nothing about
asymmetric colorings or automorphisms having a different number of vertex
cycles.

The mathematical trust boundary consists of formula (1), the degree sieve,
the known equality `R(4,5)=25`, the invariant-coloring SAT encoding, the
independent reconstruction code, the checked proof bytes, and ordinary
Python semantics.  Proof replay removes Glucose from the final trust
boundary.

McKay and Radziszowski's
[*Subgraph counting identities and Ramsey numbers*](https://doi.org/10.1002/jgt.3190190304)
supplies `R(4,5)=25`.  Exoo's
[*A lower bound for R(5,5)*](https://doi.org/10.1002/jgt.3190130113) and Ge,
Jayasooriya, Qiu, Sun, and Yuan's
[*Study of Exoo's lower bound for Ramsey number R(5,5)*](https://arxiv.org/abs/2212.12630)
motivate structured 43-vertex colorings.  Angeltveit and McKay's
[*R(5,5) <= 46*](https://arxiv.org/abs/2409.15709) supplies current
upper-bound context.  The inspected primary sources and Discovery Net graph
at indexed height 2034 did not state this complete four-cycle obstruction;
novelty is claimed only relative to those checked sources, not as a
universal priority claim.
