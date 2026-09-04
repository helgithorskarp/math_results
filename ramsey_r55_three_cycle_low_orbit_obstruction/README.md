# A complete three-cycle automorphism obstruction for Ramsey `K_43`

Let `G` be a graph on 43 vertices with neither a clique nor an independent
set of order five.  Then no nonidentity automorphism of `G` has exactly three
vertex cycles.

Equivalently, for every permutation of cycle type `(a)(b)(c)`, with
`a+b+c=43`, every invariant red/blue coloring of `K_43` contains a
monochromatic `K_5`.

This is an exact computer-assisted obstruction theorem.  Of the 154 unordered
three-cycle types, 79 fail a degree sieve and all 75 survivors have
independently replayed UNSAT certificates.  The 26 types with at most 25 edge
orbits additionally have complete objective classifications.  It does
**not** construct a 43-vertex Ramsey graph or improve the lower bound for
`R(5,5)`.

## Structural reduction

Every vertex of a target graph has degree from 18 through 24.  Its
neighborhood cannot contain a `K_4`, so `R(4,5)=25` gives degree at most 24.
Applying the same argument to the complement gives degree at least 18.

Fix a permutation with cycle lengths `a,b,c`.  Inside a cycle of odd length
`l`, an invariant graph has any even degree in `0,2,...,l-1`; for even `l`,
the antipodal matching allows every degree in `0,1,...,l-1`.  Between cycles
of lengths `l` and `m` there are `gcd(l,m)` edge orbits.  Selecting one adds
`m/gcd(l,m)` to the degree on the first cycle and `l/gcd(l,m)` on the second.
Enumerating these small integer choices proves that 79 of the 154 cycle
types cannot satisfy the degree window.

The number of edge orbits is

```text
floor(a/2) + floor(b/2) + floor(c/2)
  + gcd(a,b) + gcd(a,c) + gcd(b,c).
```

There are 76 types with at most 25 edge orbits.  Fifty already fail the
degree sieve; the other 26 have 23 or 25 Boolean edge-orbit variables and
are classified exactly.  The remaining 49 degree-feasible types have 27 to
43 edge-orbit variables and are certified by SAT proofs.

## Exact minima below the enumeration cutoff

For every five-set `A`, let `M(A)` be the bit mask of edge orbits met by its
ten edges, and let `w(M)` count five-sets with mask `M`.  If `S` is the set
of red edge orbits, the number of monochromatic five-sets is exactly

```text
sum_{M subset S} w(M) + sum_{M subset complement(S)} w(M).
```

`enumerate_three_cycles.cpp` constructs edge orbits directly from the
permutation, enumerates all `C(43,5)=962,598` five-sets, computes all subset
sums with a Boolean-lattice zeta transform, and scans every one of the
`2^23` or `2^25` colorings.  It also recounts the first minimizer by a direct
five-set scan, independently of the transformed lookup.

The checked-in deterministic table [`classification.txt`](classification.txt)
gives the exact minimum, number of minimizers, and first minimizer for every
case.  All minima are positive.  They range from 1,175, at cycle type
`1+20+22`, to 3,035, at `7+17+19`.

## Independent UNSAT certificates

The proof paths ask only the logically sufficient zero-versus-positive
question and do not import the C++ classifier.  For each distinct mask `M`,
they emit the two clauses

```text
OR_{i in M} x_i
OR_{i in M} not x_i,
```

which require both colors on the five-set.  A final unit clause fixes the
first orbit red; global color complementation makes this equisatisfiable.
Across the two edge-orbit strata the 75 instances have 2,515 to 87,311
clauses.  PySAT Glucose 4.2 reports every formula UNSAT and emits the compact
traces in [`proofs/`](proofs/) and [`proofs_high/`](proofs_high/).

`verify_proofs.py` and `verify_high_proofs.py` use only the Python standard
library.  They independently:

- rederives the degree sieve and all three-part partitions of 43;
- canonicalizes every edge under repeated permutation images, rather than
  using the generator's unused-edge orbit walk;
- regenerates every five-set mask and CNF hash;
- checks every proof hash and byte count; and
- replay all 5,153 proof additions by reverse unit propagation, reaching an
  empty clause in every one of the 75 instances.

The traces also contain 39,636 deletion hints.  The checker soundly ignores
them and retains all derived clauses: every retained clause is already a
logical consequence of the original formula, and retaining it only
strengthens unit propagation.  The 75 traces total 998,098 bytes.

Thus solver correctness is outside the trust boundary of the obstruction
claim.  The trusted components are the small reconstruction programs, the
checked proof bytes, the RUP checker, the degree lemma (including the known
equality `R(4,5)=25`), and ordinary C++/Python execution semantics.

## Reproduction

Proof checking requires Python 3.11 or later and a C++20 compiler; it does
not require a SAT solver:

```bash
bash verify.sh
```

Proof regeneration additionally uses the pinned PySAT package:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python generate_proofs.py \
  --proof-dir proofs.regenerated \
  --result proof_manifest.regenerated.json
.venv/bin/python generate_high_proofs.py \
  --proof-dir proofs_high.regenerated \
  --result high_proof_manifest.regenerated.json
```

Generation is deterministic with `python-sat==1.9.dev15`; the regenerated
manifest records the SHA-256 of every omitted DIMACS stream and every proof.
No random choice, floating point, parallelism, network input, or external
instance is used during classification or verification.

## Scope and literature

The theorem concerns only automorphisms with exactly three vertex cycles.  It
says nothing about asymmetric colorings or automorphisms with other cycle
counts.  The 25-edge-orbit threshold separates exhaustive objective
classification from proof-only SAT certification; it is not a mathematical
restriction in the final theorem.

The structured-coloring motivation comes from Exoo's
[*A lower bound for R(5,5)*](https://doi.org/10.1002/jgt.3190130113) and Ge,
Jayasooriya, Qiu, Sun, and Yuan's
[*Study of Exoo's lower bound for Ramsey number R(5,5)*](https://arxiv.org/abs/2212.12630).
McKay and Radziszowski's
[*Subgraph counting identities and Ramsey numbers*](https://doi.org/10.1002/jgt.3190190304)
supplies the established `R(4,5)=25` input.  Angeltveit and McKay's
[*R(5,5) <= 46*](https://arxiv.org/abs/2409.15709) gives current upper-bound
context.  The inspected papers and refreshed Discovery Net graph did not
state this three-cycle obstruction; novelty is claimed only relative to
those checked sources, not as a universal priority claim.
