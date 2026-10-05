# Central prime-extension boundary for cyclic-subgroup counts

Iris / **studio-researcher-2**, researcher, 2026-10-05.

Conditional lemma: independently internally checked by Rowan /
studio-researcher-4 on 2026-10-05. This is an internal check, not external
peer review, formal verification or a novelty verdict. The universal
nonsolvable eta<=6 classification has a [separate assembled proof and
internal check](../nonsolvable_cyclic_gap_induction/README.md).

The proof is frozen byte-for-byte at the version Rowan checked,
SHA256 `ea938c7b0313e008db5e7632a144d06c4a8038576f24714a99fdec294a59a769`.
Its initial draft-status line records its creation state; current check
acceptance and scope are in [Rowan's report](internal_checks/rowan_v1/REVIEW.md).

For a central order-p extension of A_5 x C_m, with p>5 and gcd(m,30)=1,
the [proof](PROOF.md) splits off A_5, classifies the remaining abelian
factor, and gives its exact normalized cyclic-subgroup count. At a
persistent prime the eta<=6 boundary forces the cyclic p-squared lift;
the split C_p x C_p lift has eta>=18. This is conditional on centrality
and the quotient form, and does not complete the universal campaign target.

The proof uses explicit cocycle averaging over A_5 and elementary
centralizer/counting arguments. It needs neither a Schur-multiplier
table nor a simple-group catalogue.

Run the finite supporting computation from the repository root:

```sh
python3 group_theory/central_prime_cyclic_count_boundary/verify.py \
  --output /tmp/central-prime-fixtures.json
```

Python 3.11 or later, standard library only, one process, no native solver.
The largest fixture has 20,580 elements. The program constructs even
permutations and modular coordinates, generates every cyclic subgroup
as a literal set of powers, and compares the number of distinct sets
with an exact element-order/totient sum. It also checks perfectness and
the center of the concrete A_5 model. Small fixtures are supporting
evidence for the formulas, not a proof that all extensions were covered.

Files:

- [PROOF.md](PROOF.md): uniform statement, proof and precise remaining interfaces.
- [verify.py](verify.py): literal finite fixture enumeration.
- [SOURCES.md](SOURCES.md): prior art and imported-fact boundaries.
- [fixtures.json](fixtures.json): compact output from the author's exact run.
- [internal_checks/rowan_v1](internal_checks/rowan_v1): independent report,
  checker, fixed input and compact result, copied without modification
  from Rowan's exact transferred version.

To reproduce the independent finite check from the repository root:

```sh
python3 group_theory/central_prime_cyclic_count_boundary/internal_checks/rowan_v1/independent_counts.py
```

Expected JSON status: `INDEPENDENT_FINITE_CONTROLS_PASS`, seven author
fixture comparisons and six changed inputs. This alternate check uses
cycle decomposition and gcd/lcm coordinate orders rather than walking
literal powers and deduplicating subgroups. It compares every element-order
histogram and both lift cosets, and uses a distinct commutator-generation
control for A_5's perfectness and center. The necessary source fixture
is included and its SHA256 checked by the program.

This package provides checked supporting source for the campaign's conditional
central-extension bridge. The assembled classification and its independent
internal-check scope are recorded in the linked induction directory.
