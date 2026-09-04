# Seven order-nine automorphism types excluded in Ramsey `(5,5;43)`

Let `G` be a graph on 43 vertices with neither a clique nor an independent
set of order five. Seven of the nine order-nine cycle types surviving the
known power constraint are impossible. Writing a type as

```text
(a,b,f) = (#9-cycles, #3-cycles, #fixed points),
```

the excluded types are

```text
(3,0,16), (3,1,13), (3,2,10), (3,3,7), (3,4,4),
(4,0,7), (4,1,4).
```

The types `(3,5,1)` and `(4,2,1)` remain open. This is deliberately a
partial structural theorem, not a complete order-nine obstruction, a
43-vertex construction, or an improvement to the Ramsey bound.

## Exact power filter

Cubing an order-nine permutation turns each 9-cycle into three 3-cycles and
fixes each original 3-cycle pointwise. The sibling sparse-motion theorem
requires an order-three element to have at least seven 3-cycles, hence
`3a>=7`. Together with

```text
9a + 3b + f = 43,
```

this gives `a=3` or `a=4` and exactly the following nine types. The first
seven marked entries are the theorem proved here.

| `(a,b,f)` | status | encoding | variables | clauses | CNF SHA-256 |
|---|---|---|---:|---:|---|
| `(3,0,16)` | excluded | direct | 207 | 218,040 | `dc391cbeadaa8a911f1789aefb93d92499025ac638b2697ffd512fca164a604d` |
| `(3,1,13)` | excluded | direct | 179 | 212,998 | `37ef68d66c76d26853ffb28b67acd3bf1a5406f5e5db16e5fe1ce46ca81a1108` |
| `(3,2,10)` | excluded | direct | 157 | 210,878 | `c70c5ab3d36cdbe8cc59e3dfada7071534bd245c0d2be2500e885b2f8136b871` |
| `(3,3,7)` | excluded | direct | 141 | 210,096 | `b461498c4fff2631bf3cdc2bddb808f17205bd9ab3afe18df566cbe2d6ab4143` |
| `(3,4,4)` | excluded | direct | 131 | 209,932 | `077dc82037c7584d58ad5934f1fd2b65c918f7939d10316edac3bcfc974c9021` |
| `(3,5,1)` | open | -- | -- | -- | -- |
| `(4,0,7)` | excluded | direct | 119 | 211,704 | `98d307992a9b01f57e340f1954364661f4cbfdefba311945edcaea206d9b59f1` |
| `(4,1,4)` | excluded | degree | 15,607 | 257,668 | `f1788f65351e2aef3d64f7fe8b63f242330f2ea4d18cf226baed6ac07ebacfde` |
| `(4,2,1)` | open | -- | -- | -- | -- |

`verify_cycle_types.py` independently exhausts the cycle equation,
permutation order, cube type, and exact closed/open scope.

## Formulas and certificates

The direct formulas use one variable per orbit of unordered pairs under the
order-nine permutation. For every one of the `C(43,5)=962,598` vertex
five-sets, two clauses over its distinct orbit variables require both
colors; duplicate clauses are removed. The first six excluded cases use
only this direct formula and no symmetry breaking.

The direct `(4,1,4)` formula reached the bounded screening cutoff. Its nine
vertex orbits were then given transparent 42-input Boolean sorting networks
requiring degrees in `[18,24]`, as forced by `R(4,5)=25`. The networks add
15,498 variables and 46,504 distinct clauses. This strengthened formula is
certified UNSAT.

drat-trim verified all seven source traces, two successive retained cores,
and every final checked-in proof. The final proofs total 12,793,221 bytes
uncompressed and 1,913,916 bytes under xz. Exact per-case hashes, clause
distributions, additions, and deletion counts are in `result.json`.

The Python generator uses least images under all nine powers. The independent
C++20 verifier reconstructs the permutation from the cycle counts, obtains
pair-orbits by disjoint-set unions, rebuilds every direct clause, independently
reconstructs the degree networks when present, and requires exact DIMACS
clause-set equality.

## Reproduction

Requirements are CPython 3.11 or later, a C++20 compiler, xz, and
[drat-trim commit `2e3b2dc`](https://github.com/marijnheule/drat-trim/commit/2e3b2dc0ecf938addbd779d42877b6ed69d9a985).
No Python package is required.

```bash
DRAT_TRIM=/path/to/drat-trim ./verify.sh
```

The script regenerates and compares the manifest, audits the power filter,
reconstructs all seven formulas in Python and independently in C++, and
replays all proofs. Every verdict must be `s VERIFIED`. The C++ verifier is
also tested under AddressSanitizer and UndefinedBehaviorSanitizer.

Proof generation used
[Kissat commit `8af8e56`](https://github.com/arminbiere/kissat/commit/8af8e56f174b778aef3aa45af9f739b2a5f492c2).
The recorded Kissat binary SHA-256 is
`2d185ea775f2c7c16d33a235ef852d2b69f0f3c8b437335b966b4a5aa6265b45`;
the drat-trim binary SHA-256 is
`9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.

## Scope and negative experiments

The theorem excludes exactly the seven displayed types. For each open type,
the direct formula timed out at 30 seconds, the degree-network formula timed
out at 60 seconds, and a further formula imposing the exact four-vertex
common-neighborhood cap for each moving monochromatic 3-cycle timed out at
60 seconds. These bounded timeouts establish nothing and none of their
uncertified formulas is retained here.

The inspected structured-construction literature and refreshed Discovery
Net graph did not state this seven-type obstruction. Novelty is claimed only
relative to those searched sources, not as a universal priority claim.
