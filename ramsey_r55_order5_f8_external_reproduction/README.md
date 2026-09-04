# Independent reproduction: no order-five type `1^8 5^7`

Let `G` be a graph on 43 vertices with neither a clique nor an independent
set of order five. Then `G` has no automorphism with eight fixed vertices
and seven cycles of length five.

This result was already published in the
[wustep/maths q4 notebook](https://github.com/wustep/maths/tree/main/problems/ramsey-r55/compute/q4).
This directory supplies an independent semantic reconstruction and proof
replay of its `p5_c7_k3` certificate. The external notebook gets credit for
the exclusion; no novelty is claimed for the theorem or its anchor method.

Together with this repository's
[four middle exclusions](../ramsey_r55_order5_middle_obstruction),
[fixed-33 exclusion](../ramsey_r55_order5_f33_degree_obstruction), and
[fixed-38 exclusion](../ramsey_r55_order5_f38_analytic_obstruction), this leaves
only `1^3 5^8` as a possible order-five automorphism type in a hypothetical
target. That type remains open here. No 43-vertex witness or improvement to
the Ramsey lower bound is obtained.

## Complete reduction to the checked case

The fixed vertices are `0,...,7`; cycle `i` is `8+5i,...,12+5i`, for
`i=0,...,6`. The prescribed generator fixes the first eight vertices and
advances every five-cycle one position. Its 203 unordered-pair orbits
comprise 28 singleton orbits and 175 orbits of length five.

Every vertex has each color-degree between 18 and 24, since either color
neighborhood is a `(4,5)` graph and `R(4,5)=25`. Write the red degree of
fixed vertex zero as `5k+t`, where `k` is its number of red-adjacent moving
cycles and `0<=t<=7` counts its red-adjacent fixed vertices. The only
degree-feasible possibilities are

```text
k=3, t=3,...,7;    k=4, t=0,...,4.
```

Complementation sends `(k,t)` to `(7-k,7-t)`, so it suffices to use `k=3`.
Permuting cycles puts these three neighbors first. No degree-feasible
neighbor count is discarded.

Cycle permutations within each of the two blocks of sizes three and four
then sort their internal two-bit color profiles. Keep cycle zero as phase
anchor and independently rotate each other cycle so its five-bit cross
word to the anchor is lexicographically least among rotations. All these
relabelings commute with the prescribed generator. Rotations preserve
internal profiles and fixed-vertex incidences; rotating one nonanchor cycle
leaves every other anchor cross word unchanged. Thus every invariant graph,
after an optional complement, has a representative satisfying all the
constraints simultaneously. No extra graph automorphism is imposed.

## Independent formula reconstruction

The external encoder is fetched at source commit
`9b6011399f13791b35ee76c4e2e3cdbd208cdd8f` and checked by SHA-256 before
execution. It regenerates the exact stored instance. Its variable labels
are exported as an **untrusted** list of numeric IDs and semantic edge
labels. `independent_formula.cpp` does not call or import the encoder.

The checker constructs the permutation and joins its action on all 903
unordered pairs with a disjoint-set data structure. It checks each supplied
label against a representative edge, requires a bijection with the actual
pair-orbits, and assigns the supplied numeric ID to that entire orbit.
The exported ID order is immaterial; its semantics and coverage are checked.

For the Ramsey clauses the checker visits **all** 962,598 five-sets and
requires both colors, deduplicating only identical projected variable sets.
The external encoder visits only canonical representatives of five-set
orbits. Agreement with all five-sets checks that optimization's completeness.

The checker derives prime implicates from the truth tables of `y=x`,
`y=a OR x`, `y=a OR (x AND b)`, and `z=p AND (x=y)`. These yield 2, 3, 4,
and 5 gate clauses, respectively. It reconstructs the sequential-counter
and equal-prefix topologies, using all 42 incident edges with exact
multiplicities. Counter bit `(i,j)` means at least `j+1` of the first `i+1`
inputs are true. Forbidding the next input when the previous count reaches
24 gives the upper degree bound; the final count-at-least-18 bit gives the
lower bound. Equal-prefix gates enforce binary lexicographic order.

Every DIMACS clause is parsed, normalized, and compared with the independently
reconstructed **multiset**, including duplicate multiplicities:

```text
edge variables                 203
all variables                15482
direct Ramsey clauses       384076
degree clauses               59430
prefix and symmetry clauses    816
total clauses               444322
```

The checker passes AddressSanitizer and UndefinedBehaviorSanitizer. It
rejects a missing clause even after the header count is adjusted, and
rejects a duplicate edge label. `audit_reductions.py` exhausts the small
degree arithmetic and constructs the normalization on 100 arbitrary
invariant colorings with both `k=3` and `k=4`, checking every relabeled edge.
These tests supplement the general proof above.

## Certificate and reproduction

The regenerated CNF SHA-256 is
`e8184d290a348f8f7b245c48e07a54a1c1c839a5337d6461b20c98c1c2d3a8da`.
The external gzip certificate is 3,024,902 bytes; its decompressed DRAT
trace is 15,386,204 bytes with SHA-256
`a9a3d927537ebedf43d3a3f007c3abac2686f4ef221eb8aae84ef9ee8f1347e6`.
Pinned drat-trim verifies it. No solver search is needed for this audit.

Use Python 3.11 or later, a C++20 compiler, and drat-trim at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. No Python package is required.
From this directory run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 reproduce.py \
  --work /tmp/r55-f8-reproduction --drat-trim /path/to/drat-trim
```

The command downloads four pinned external files, checks their hashes,
regenerates the CNF, checks the reductions and entire formula, and replays
the stored proof. The external files, formula, proof, logs, and binary stay
in `--work`, outside the repository. `result.json` records input hashes and
reference tool versions; `EXPECTED_OUTPUT.txt` records deterministic output.
The work directory's `reproduction.json` also records elapsed time. The
final lines must be

```text
PASS stored_external_DRAT_replay=VERIFIED
PASS type_1^8_5^7_excluded_external_result_independently_reproduced=true
```

To run the checking build after reproduction:

```bash
g++ -O1 -g -std=c++20 -Wall -Wextra -Wpedantic \
  -fsanitize=address,undefined -fno-omit-frame-pointer \
  independent_formula.cpp -o /tmp/r55-f8-reproduction/independent_formula_san
/tmp/r55-f8-reproduction/independent_formula_san \
  /tmp/r55-f8-reproduction/edge_labels.tsv /tmp/r55-f8-reproduction/p5_c7_k3.cnf
```

## Scope and trust

This reproduces one external structural exclusion with an independent
formula derivation and the same pinned proof-checker family. It is not a
second proof-checker implementation or an independent rerun of the SAT
search. The theorem and proof are attributed to the q4 source. Its other
certificates are outside this audit's scope.

Mathematical inputs are `R(4,5)=25`, the orbit encoding, counter/gate
semantics, and proved normalization. Those arguments and the checker source
are unformalized. Computational trust includes Python/C++ execution, gzip,
and pinned drat-trim. External graph-decoding and clique-search routines
are not used as mathematical evidence. Only source and compact manifests
are published here; replay requires the pinned external files, whose
availability remains an external dependency. Hashes alone are not proofs.
