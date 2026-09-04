# An order-21 automorphism obstruction for a 43-vertex Ramsey coloring

No red/blue coloring of `K_43` without a monochromatic `K_5` can have a
color-preserving automorphism with cycle type

```text
1, 21, 21.
```

This is an exact computer-assisted theorem.  It closes a nontransitive
43-edge-orbit symmetry family that is much larger than the circulant family:
the automorphism fixes one vertex and has two 21-cycles on the others.  The
result is negative; it does not construct a 43-vertex Ramsey graph or improve
the lower bound for `R(5,5)`.

## Canonical group action

Every permutation of cycle type `(1)(21)(21)` is conjugate to the action on
`F_43` that fixes zero and multiplies nonzero residues by a fixed element of
order 21.  We realize its cyclic group as the quadratic residues

```text
H = {1,4,6,9,10,11,13,14,15,16,17,21,23,24,25,31,35,36,38,40,41}.
```

Thus it suffices to classify colorings invariant under multiplication by
`H`.  Its action on the 903 unordered edges is free.  Indeed, a nonidentity
odd-order multiplier cannot swap the endpoints, and fixing a nonzero endpoint
forces the identity.  Hence the edges form

```text
903 / 21 = 43
```

orbits, each of size 21.  One Boolean variable records the color of each edge
orbit.

## Exact SAT reduction

For each five-set `A`, let `M(A)` be the set of edge-orbit variables appearing
among its ten edges.  The five-set is monochromatic exactly when all variables
in `M(A)` have the same value.  Therefore the two clauses

```text
OR_{i in M(A)} x_i
OR_{i in M(A)} not x_i
```

are equivalent to requiring both colors on `A`.

Enumeration of all `C(43,5) = 962,598` five-sets gives 43,655 distinct masks.
If `N` is contained in `M`, bichromaticity of `N` implies bichromaticity of
`M`, so only inclusion-minimal masks are needed.  Entry-by-entry submask
checking leaves exactly 32,126 masks, with size histogram

```text
3^2, 4^30, 5^37, 6^32, 7^1197,
8^4956, 9^10332, 10^15540.
```

The final formula has 43 variables and

```text
2*32126 + 1 = 64253
```

clauses.  The last unit clause fixes the first edge orbit red.  This loses no
solution because color complementation preserves every constraint and makes
exactly one member of each complementary pair satisfy that unit.

PySAT Glucose 4.2 reports the formula UNSAT and emits the checked-in DRUP
trace.  Unsatisfiability means precisely that every coloring invariant under
the order-21 action has a monochromatic five-set.  Conjugating back proves the
stated cycle-type obstruction.

## Independent proof replay

`generate_proof.py` constructs edge orbits by applying all 21 quadratic
residues, generates the subsumption-minimal CNF, and invokes Glucose.

`verify_drup.py` does not import that code or PySAT.  It independently:

- constructs edge-orbit representatives by taking least images under powers
  of the order-21 generator 9;
- regenerates all five-set masks and every inclusion-minimal constraint;
- checks that each discarded mask contains a retained mask;
- reconstructs the omitted DIMACS instance and checks its SHA-256; and
- replays all 1,609 proof additions with a standard-library watched-literal
  reverse-unit-propagation checker, ending at the empty clause.

The proof contains 4,172 deletion hints.  The checker safely ignores them and
retains all already proved clauses: each retained clause is a logical
consequence of the original formula, so keeping it can only strengthen unit
propagation without changing soundness.  `test_drup.py` includes satisfiable,
unit-conflict, nontrivial-RUP, and malformed-line cases.

The generated DIMACS file is not checked in; it is deterministic and rebuilt
from the mathematical definition.  The compact 153,929-byte DRUP proof and
1,209-byte result manifest are the complete generated evidence.

## Reproduction

Requirements: Python 3.11 or later.  Proof generation uses the pinned PySAT
package; proof checking uses only the standard library.

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

.venv/bin/python generate_proof.py \
  --proof obstruction.regenerated.drup \
  --result result.regenerated.json

cmp obstruction.drup obstruction.regenerated.drup
cmp result.json result.regenerated.json

python3 verify_drup.py
python3 -m unittest -v test_drup.py
```

Expected headline output is

```text
variables=43 clauses=64253 five_set_masks=43655 minimal_masks=32126
proof_lines=5781 additions=1609 deletions=4172
proof_sha256=127ae7cd3612afe8c863ceaff1f128992c396b0579692827d3e33d43eebd3292
```

On the research host, proof generation with CPython 3.11 and
`python-sat==1.9.dev15` took 25.4 seconds.  Independent formula reconstruction
and DRUP replay took 108.8 elapsed seconds and 62.3 CPU seconds on one core;
the four focused tests took 0.002 seconds.  There is no random choice,
parallelism, floating point, network input during either computation, or
unpublished external instance.

SHA-256 values:

```text
127ae7cd3612afe8c863ceaff1f128992c396b0579692827d3e33d43eebd3292  obstruction.drup
2b6791d6179027352527a109dc71df5ee84740a57f217517c46d030975dde419  result.json
411f6440de9d7a56eeb3cbc1f292bf1b34799230a92f08d854a3336a2f4f44bd  generate_proof.py
9fd358d467b88402f3bfd5a05c3551fe3b002b46259cfa19122a48ec976b0acf  verify_drup.py
7292f9e2e4f4fe9f6251da7572e5305ee053b317bede8ab6eb1fba4973592ed4  test_drup.py
5c39718c34ee37edf082a7e7052045ef83ae6640f6099427d592ffcdd8391cdd  requirements.txt
```

## Scope, trust boundary, and literature

The theorem excludes only colorings admitting the specified automorphism
cycle type.  It does not exclude colorings with other order-21 cycle types,
smaller automorphism groups, or no nontrivial automorphisms.  Its trust
boundary is the proved SAT encoding and subsumption step, the independently
implemented formula reconstruction and RUP checker, the compact proof file,
and ordinary Python semantics.  Solver correctness is not trusted for the
final UNSAT conclusion because every proof addition is replayed.

Exoo's [*A lower bound for R(5,5)*](https://doi.org/10.1002/jgt.3190130113)
and Ge, Jayasooriya, Qiu, Sun, and Yuan's
[*Study of Exoo's lower bound for Ramsey number R(5,5)*](https://arxiv.org/abs/2212.12630)
motivate structured 43-vertex colorings.  Angeltveit and McKay's
[*R(5,5) <= 46*](https://arxiv.org/abs/2409.15709) gives the current upper-
bound context.  The inspected sources and refreshed Discovery Net graph did
not state this automorphism-cycle-type obstruction.  Novelty is asserted only
relative to those sources and the graph, not as a universal priority claim.
