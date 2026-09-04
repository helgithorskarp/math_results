# Degree-network obstruction for order-five type `1^33 5^2`

Let `G` be a graph on 43 vertices with neither a clique nor an independent
set of order five. No automorphism of `G` has cycle type

```text
1^33 5^2.
```

Together with the sibling four-type obstruction and the subsequent analytic
exclusion of `1^38 5`, this leaves only `1^3 5^8` and `1^8 5^7` among the
eight possible order-five types. This is an exact computer-assisted
structural theorem, not a 43-vertex construction or a Ramsey bound
improvement.

## Direct orbit formula

Fix the permutation that leaves vertices `0,...,32` fixed and rotates each
of two five-cycles. Its action on unordered edges has

```text
C(33,2) + 33*2 + 2*2 + 5*C(2,2) = 603
```

orbits. One Boolean variable records each edge-orbit color. For every
five-set `A`, the two clauses over the distinct orbit variables on its ten
edges require both colors on `A`. Enumerating all `C(43,5)=962,598`
five-sets and deduplicating gives the direct Ramsey clauses.

The complete centralizer normalization first sorts the two five-cycles by
their two-bit internal-distance profiles, then sorts the 33 fixed vertices
by their two-bit incidence profiles, and finally phases the second cycle so
its five-bit cross-edge word with the first is least among rotations. Each
operation preserves the preceding profiles and retains a representative of
every centralizer orbit. The resulting base formula has 603 variables and
762,858 distinct clauses.

## Exact degree network

The equality `R(4,5)=25` forces every vertex degree of a target graph into
`[18,24]`. For every vertex orbit, expand its incident orbit colors with
multiplicity to a list of exactly 42 Boolean inputs:

- a fixed vertex has 32 fixed--fixed inputs and two fixed--cycle inputs, each
  repeated five times;
- a moving vertex has 33 fixed incidences, two internal-distance variables
  repeated twice, and five cross-cycle variables.

Thus the number of true inputs is exactly the red degree, without weighted
arithmetic or an external cardinality library.

Each 42-input list is sorted in descending Boolean order by a fixed bubble
network of `C(42,2)=861` compare--exchange gates. For inputs `a,b`, a gate
has outputs

```text
high = a OR b,       low = a AND b,
```

encoded by the six clauses for both equivalences. Exhaustive truth-table
tests verify the gate, and exhaustive tests on every eight-bit input verify
the network schedule. After sorting, unit clauses require output 18 true and
output 25 false, exactly `18 <= degree <= 24`.

There are 35 vertex orbits, so the networks add 60,270 variables, 180,810
gate clauses, and 70 boundary units. The final deterministic formula has

```text
variables: 60,873
clauses:   943,738
SHA-256:   20a4dbcef743846145cb91f0bd1e811e31569e6a8e9ae7e8792e065fe3af10ce
```

## Independent reconstruction and proof replay

`base_formula.py` and `generate_formula.py` construct edge orbits by least
images under powers of the permutation. The independent C++20 verifier uses
a disjoint-set union for the edge action, rebuilds all five-set and
centralizer clauses with nested loops, reconstructs all 35 comparator
networks, parses the generated DIMACS, and requires exact clause-set
equality.

Kissat 4.0.4 returned UNSAT in 7.73 process-seconds and emitted a
2,897,510-byte DRAT trace. drat-trim verified the source proof and each of
two successive core extractions. The final proof was verified once more; it
has 5,758 lines, comprising 844 additions and 4,914 deletion hints, and ends
at the empty clause. Its 135,425 bytes compress to the checked-in 21,964-byte
xz stream. Full byte counts and SHA-256 digests are in `result.json`.

## Reproduction

Requirements are CPython 3.11 or later, a C++20 compiler, xz, and
[drat-trim commit `2e3b2dc`](https://github.com/marijnheule/drat-trim/commit/2e3b2dc0ecf938addbd779d42877b6ed69d9a985).
No Python package is required.

```bash
DRAT_TRIM=/path/to/drat-trim ./verify.sh
```

The script regenerates and byte-compares the manifest, runs the exact local
tests, reconstructs the formula independently in C++, and streams the proof
to drat-trim. Its final proof verdict must be `s VERIFIED`. The C++ build is

```text
g++ -O3 -std=c++20 -Wall -Wextra -Wpedantic
```

and the complete verifier is also tested under AddressSanitizer and
UndefinedBehaviorSanitizer.

Proof regeneration uses
[Kissat commit `8af8e56`](https://github.com/arminbiere/kissat/commit/8af8e56f174b778aef3aa45af9f739b2a5f492c2):

```bash
python3 generate_formula.py formula.cnf
/path/to/kissat formula.cnf proof.regenerated.drat
```

The recorded Kissat binary SHA-256 is
`2d185ea775f2c7c16d33a235ef852d2b69f0f3c8b437335b966b4a5aa6265b45`;
the drat-trim binary SHA-256 is
`9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.

## Scope, provenance, and trust boundary

The proof closes exactly `1^33 5^2`. The types `1^3 5^8` and `1^8 5^7`
remain open. The bounded solver timeout on `1^38 5^1` established nothing;
that type is instead closed by the separate
[`ramsey_r55_order5_f38_analytic_obstruction`](../ramsey_r55_order5_f38_analytic_obstruction).
The result does not exclude all order-five automorphisms or asymmetric
colorings.

Mathematical inputs are the orbit-CNF equivalence, centralizer normalization,
the degree-multiplicity expansion, comparator-network lemma, and the known
equality `R(4,5)=25`. Computational inputs are the independent Python/C++
reconstructions, exact language/container semantics, the checked-in proof,
xz, and drat-trim. Kissat's exit code is not trusted without proof replay.

Exoo's [*A lower bound for R(5,5)*](https://doi.org/10.1002/jgt.3190130113)
and Ge--Jayasooriya--Qiu--Sun--Yuan's
[*Study of Exoo's lower bound for Ramsey number R(5,5)*](https://arxiv.org/abs/2212.12630)
give the structured-construction context. Angeltveit--McKay's
[*R(5,5) <= 46*](https://arxiv.org/abs/2409.15709) supplies the current upper
bound. The inspected primary sources and refreshed Discovery Net graph did
not state this cycle-type obstruction. Novelty is claimed only relative to
those searched sources, not as a universal priority claim.
