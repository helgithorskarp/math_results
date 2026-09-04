# No order-nine automorphism in Ramsey `(5,5;43)`

Let `G` be a graph on 43 vertices with neither a clique nor an independent
set of order five. Then `Aut(G)` has no element of order nine.

This completes the earlier
[seven-type exclusion](../ramsey_r55_order9_partial_automorphism_obstruction)
by closing its two residual types, `1^1 3^5 9^3` and `1^1 3^2 9^4`.
The new ingredient is a simultaneous normalization under permutations and
independent rotations of the vertex cycles. It reduces equivalent
assignments without imposing an additional graph automorphism.

Consequently, no automorphism has order divisible by nine, no vertex cycle
of an automorphism has length divisible by nine, and every nontrivial
3-subgroup of `Aut(G)` has exponent three. These conclusions do **not** say
that nine cannot divide the group order, or that its 3-subgroups are abelian.
For example, `C3 x C3` has order nine and no element of order nine.

This is an exact computer-assisted structural theorem. It does not
construct a 43-vertex Ramsey graph or improve the bound on `R(5,5)`.

## Complete type reduction

Write `(a,b,f)` for the counts of 9-cycles, 3-cycles, and fixed vertices.
Cubing an order-nine permutation gives `3a` moving 3-cycles. The earlier
[sparse-motion theorem](../ramsey_r55_sparse_order2_order3_automorphism_obstruction)
requires at least seven, so `a>=3`. Solving `9a+3b+f=43` leaves nine types.
Seven are excluded by the earlier artifact; the remaining two are the
cases certified here. `audit_symmetry.py` checks this exact partition.

If an element `h` has order `m` divisible by nine, then `h^(m/9)` has order
nine. This proves all the stated power and 3-subgroup corollaries.

## Why the simultaneous normalization is valid

Label the cycles consecutively, with the 9-cycles first, then the 3-cycles,
then the fixed vertex. Let `g` advance each cycle one position. Every
permutation of equal-length cycles, preserving their cyclic coordinates,
commutes with `g`. Independently rotating any individual cycle also commutes
with `g`. Relabeling by any such permutation preserves `g`-invariance and
the Ramsey property.

For a 9-cycle `C=(c0,...,c8)`, its internal edge colors are determined by
the four-bit profile

```text
(color(c0,c1), color(c0,c2), color(c0,c3), color(c0,c4)).
```

The profile of a 3-cycle is its single internal edge color. A rotation of
the cycle preserves this profile: the restricted coloring is circulant and
undirected. First permute the 9-cycles so that their profiles are in
nondecreasing lexicographic order, and separately sort the 3-cycles.
Equal profiles may be ordered arbitrarily.

Choose `c0=0` in the first 9-cycle as the anchor. For each other moving
cycle `D=(d0,...,d(l-1))`, consider the cross word

```text
(color(0,d0), ..., color(0,d(l-1))).
```

Keep the anchor cycle fixed and rotate `D` to make this word lexicographically
least among its cyclic rotations. The variables in this word are distinct:
a power of `g` fixing the anchor has exponent divisible by nine, which also
fixes every vertex of `D`. Thus there are `l` independent pair-orbits.

Rotating `D` preserves every internal profile and the cross words from the
anchor to all the other cycles. Hence all these normalizations can be
performed successively without undoing an earlier one. Connections between
two nonanchor cycles may change, but there are no normalization constraints
on those connections. This proves that **every** invariant coloring has a
representative satisfying all the added clauses simultaneously.

## Formulas and computational evidence

A Boolean variable represents each orbit of unordered pairs under `g`.
For every one of the `C(43,5)=962598` five-sets, the distinct variables on
its ten pairs give two clauses requiring both colors. This is equivalent
to the Ramsey property for invariant colorings. Duplicate clauses are
removed. No degree constraints or color-complement normalization are used.

Additional clauses forbid each adjacent pair of internal profiles in
decreasing order, and each cross word that is not a least cyclic rotation.
There are 120 decreasing pairs of four-bit profiles, one decreasing pair
of one-bit profiles, 452 noncanonical nine-bit words, and four noncanonical
three-bit words. Therefore the added clause counts are respectively
`2*120+4+2*452+5*4=1168` and `3*120+1+3*452+2*4=1725`.

| `(a,b,f)` | variables | base clauses | normalization clauses | total clauses |
|---|---:|---:|---:|---:|
| `(3,5,1)` | 127 | 210206 | 1168 | 211374 |
| `(4,2,1)` | 105 | 211062 | 1725 | 212787 |

Both formulas are certified UNSAT. Exact CNF and reference binary-DRAT
SHA-256 digests, proof sizes, tool versions, and dependency hashes are in
`result.json`. The reference proofs are 2,840,051 and 20,250,332 bytes.
They are kept outside Git; `reproduce.py` regenerates them and requires an
independent `drat-trim` verdict for each. A fresh run reproduced both
reference proof hashes exactly. The retained local derived cores also
replayed successfully; their existence is not required by the reproduction.

The Python generator uses least images under all nine powers. The C++
checker reuses the earlier disjoint-set orbit reconstruction and enumerates
five-sets directly, then independently builds the normalization clauses
using integer comparisons and bit rotations. It parses and normalizes the
generated DIMACS and requires equality of the complete clause sets, including
literal sets and counts. Both cases pass AddressSanitizer and
UndefinedBehaviorSanitizer. The normalization audit constructs actual
commuting permutations on 204 arbitrary colorings, checking all 903 edges
per coloring. These tests supplement the general normalization proof above.

## Reproduction

Requirements: Python 3.11 or later, a C++20 compiler, Kissat 4.0.4 at commit
`8af8e56f174b778aef3aa45af9f739b2a5f492c2`, and drat-trim at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. No Python package is needed.
Run from this directory in a checkout containing the earlier sibling artifact:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 reproduce.py \
  --work /tmp/r55-order9-reproduction \
  --kissat /path/to/kissat --drat-trim /path/to/drat-trim
```

The default solver limit is 300 seconds per case; `--seconds` changes it.
A timeout or any verdict other than checked UNSAT fails the command.
The final output must be

```text
PASS case=0 UNSAT certificate_replay=VERIFIED reference_proof_match=True
PASS case=1 UNSAT certificate_replay=VERIFIED reference_proof_match=True
PASS both residual order-nine cases independently certified
```

Other valid proof bytes are accepted after replay, with the reference-hash
difference reported explicitly. All formulas, proofs, logs, binaries, and
the observed `replay.json` stay in `--work`, outside the repository. On the
reference host, the two per-case generation/reconstruction/solve/replay
runs took 15.124 and 102.970 seconds, respectively. To also recheck the seven imported exclusions, run
`DRAT_TRIM=/path/to/drat-trim ../ramsey_r55_order9_partial_automorphism_obstruction/verify.sh`.

## Trust boundary and prior work

The theorem combines the earlier seven certificates and sparse-motion lemma
with the two new checked refutations. The unformalized mathematical bridge
is the proved centralizer normalization and orbit-CNF equivalence above.
The computational boundary includes Python/C++ runtime semantics, the
independent formula checker, and pinned `drat-trim`. Solver exit codes or
hashes alone are not accepted as proof. The large generated traces are
omitted; readers must regenerate them to independently replay the result.

The classical construction context is [Exoo's lower-bound paper](https://onlinelibrary.wiley.com/doi/10.1002/jgt.3190130113),
the [study of its cyclic construction](https://arxiv.org/abs/2212.12630), and
[McKay--Radziszowski's catalog work](https://users.cecs.anu.edu.au/~bdm/papers/r55.pdf).
Targeted searches for order-nine automorphisms in `(5,5;43)` colorings and
the committed Discovery Net graph through height 2360 found the earlier
seven-type result but no complete exclusion. This is a search-relative
novelty statement, not a historical-priority claim.
