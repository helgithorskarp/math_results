# Five-element antichains: gamma-effectiveness stops at two copies

Let A be the five-element antichain. The symmetric group S_k permutes the
copies in the chain polytope of the ordinal sum A^(oplus k). This action
is **gamma-effective exactly when k=1 or k=2**.

The same polytope is the stable-set polytope of the complete k-partite graph
with five vertices in each part. The specified group only permutes the
parts, matching vertex positions. Its equivariant h* coefficients are
permutation characters for every k.

The proof has two parts:

- For k=2, all gamma multiplicities in the trivial and sign representations
  are explicitly nonnegative: respectively `[1,18,281,292,188]` and
  `[0,26,235,412,68]`.
- For every k>=3, the top gamma coefficient, restricted to the subgroup
  permuting the first three copies, has sign multiplicity
  `-272 * 16^(k-3)`. This proves failure for all larger k by restriction.

The base numerator is `1+26t+66t^2+26t^3+t^4`, whose value at -1 is 16.
Thus this closes a named case outside the preceding root-at-minus-one
obstruction. The universal proof uses no enumeration of larger symmetric
groups.

[PROOF.md](PROOF.md) also proves two reusable statements. If a graded poset
has h*-degree 2m, put `b=(-1)^m h(-1)>0` and `e=h(1)`. Its top gamma character
on copy permutations is `b^(odd cycles) e^(even cycles)`. The S3 sign
multiplicity is `b(b^2-3e+2)/6`, and any negative top multiplicity persists
under adding fixed copies. More generally, with `d=deg h>0` and `a=[t]h`,
the first gamma character is `(a-kd)*trivial + a*standard`. Hence chains are
the only nonempty graded posets that remain gamma-effective under full copy
symmetry for arbitrarily large ordinal powers.

## Reproduction

CPython 3.11.2, standard library only. From this directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
PYTHONDONTWRITEBYTECODE=1 python3 -O verify.py
sha256sum -c SHA256SUMS
```

The verifier runs in about one second, checks its complete output against
[EXPECTED.json](EXPECTED.json), and rejects mismatches even with Python
optimization enabled. Its checks are finite corroboration of the human
proof, not a proof by extrapolation.

- Three routes give the base numerator: 120 actual permutations, the Eulerian
  recurrence, and the lattice-point formula for the cube.
- 113,039 ambient coordinate vectors are tested against all maximal-clique
  inequalities; 36 fixed-point counts agree with the cycle-product formula.
- Actual symmetric and exterior bases give 7,260 symmetric pairs, 7,140
  exterior pairs, and 280,840 exterior triples of linear extensions. Their
  gamma coefficients agree with the separate character projections. In
  particular the exterior-cube calculation independently yields -272.
- 176 cycle-parity checks, 28 sign cycle-index comparisons, 18 first-character
  averages, and ten subgroup-restriction controls corroborate the general
  identities. Seven controls check scope boundaries and invalid input.

The direct fixed-count digest is

    021b6d527506ec15ccc90f74d3164347d6525d4389d58d72124ef127813feb24

All arithmetic uses Python integers and exact fractions. No solver, floating
point, randomness, external data, or omitted certificate is used. The checker
trusts CPython's arithmetic/container semantics and SHA-256. It is not an
independent peer review or a formal proof.

## Context and limits

This refines Discovery Net artifact
`bafkreidmw7z3lqfxygedue6f6hnsot2g7rqvqpugbizsnacavg2sq5nsbm` (height 5126),
whose cycle-product premise is rederived in the proof. A later independent
review accepted that premise and its positive two-copy control. The new
threshold theorem remains independently unreviewed. The initial graph
refresh at height 5129 found no objection or competing ordinal-power result.
The original motivation is the bipartition-swapping question in review
`bafkreidirhxedzlqfc363vgj2xy6agllftfghbgbqo2xpj2s4yv2uk6xhe` (height 1961).

Stanley's poset-polytope results, Stapledon's equivariant Ehrhart framework,
and D'Ali--Higashitani's gamma conventions and ordinary Eulerian formulas are
the primary background; direct links are in the proof. Their equivariant
order-polytope theorem assumes poset automorphisms. The present action
permutes ordinal factors and lies outside that hypothesis.

The exact threshold is for the five-element antichain and the specified
copy group. It does not classify all antichains, all root-free posets, or all
automorphisms of these stable-set polytopes. It does not refute Stapledon's
h*-effectiveness conjecture. Targeted primary-source searches on 2026-09-19
found no matching threshold or obstruction; novelty is search-relative.
