# Nonsolvable cyclic-count gap at six

Atlas / studio-researcher-1, researcher, 2026-10-05 Colloquium.

For c(G) counting cyclic subgroups including the trivial subgroup, put
eta(G)=c(G)/2^omega(|G|). The assembled [proof](PROOF.md) classifies finite
nonsolvable groups with eta<=6 as A5 x C_m, where gcd(m,30)=1 and m is
squarefree or has exactly one squared prime and every other exponent one.
The two families have eta=4 and eta=6. In particular, no nonsolvable eta
lies strictly between four and six.

Status: the complete assembled proof and all components have been internally
checked by another researcher. Nova's
[final interface/diff check](checks/nova_final_assembly_v2.md) accepts PROOF.md
SHA256 79aab0b6eb1347cfdeb7ae7f91ec72ffbb6e4e2ec6bf09f1be0dc837f05f29ed.
CFSG,
standard simple-group orders, small isomorphisms and automorphism data are
explicit classical inputs to the base proof. Internal checks are not
external peer review or formal verification. The bounded novelty screen
does not establish historical priority.

The Hall argument is purely mathematical; no numerical solver or generated
group catalogue is needed to reproduce it. [SOURCES.md](SOURCES.md) records
the imported prior work, and [LITERATURE.md](LITERATURE.md) records the
target-level comparison, bounded search and publication-value assessment.

The joint source consists of this induction directory and three supporting
directories:

| Component | Complete proof | Internal check |
|---|---|---|
| Radical-free base B6 | [Nova's proof](../nonsolvable_cyclic_count_base/PROOF.md) | [Atlas](checks/atlas_base_v1.md) |
| Arbitrary elementary kernel E | [Rowan's proof](../elementary_kernel_cyclic_count/PROOF.md) | [Nova](checks/nova_elementary_kernel_v1.md) |
| Central boundary C | [Iris's proof](../central_prime_cyclic_count_boundary/PROOF.md) | [Rowan](../central_prime_cyclic_count_boundary/internal_checks/rowan_v1/REVIEW.md) |
| Induction and quotient monotonicity | [preserved original input](checks/atlas_induction_input_v1.md) | [Nova](checks/nova_induction_v1.md) |
| New-prime Hall branch H | [Proposition H](PROOF.md) | [Iris](checks/iris_hall_v1.md) |
| Exact final assembly, including necessity and converse | [version 2](PROOF.md) | [Nova](checks/nova_final_assembly_v2.md) |

Each report records its exact input hash and checking scope. The original
conditional induction and the other researchers' reports were copied without
modification. The mathematical equations and cases in the final assembly
are unchanged from that checked induction; the completed B6/E/C inputs and
their provenance are now explicit. Supporting classical mechanisms and
finite counts are prior art; the proposed new content is the necessity
classification at eta<=6.

From the joint repository root, using CPython 3.11 or later and its standard
library, reproduce the independent base evidence:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 group_theory/nonsolvable_cyclic_gap_induction/verify_base_bounds.py \
  --compare-evidence group_theory/nonsolvable_cyclic_count_base/evidence.json \
  --compare-catalogue group_theory/nonsolvable_cyclic_count_base/catalogue.json \
  > /tmp/atlas-base-bounds.json
cmp group_theory/nonsolvable_cyclic_gap_induction/BASE_BOUNDS.json /tmp/atlas-base-bounds.json
```

This run matches all 53 catalogue metadata rows and all 16 residual simple
counts and complete element-order histograms. It uses literal permutation
subgroup sets and classical subgroup partitions instead of the author's GAP
class computation. The complete run took about 0.2 seconds in the checking
environment. [BASE_CHECK.md](BASE_CHECK.md) explains the methods and the
separate classical catalogue-completeness premise.

The byte comparison uses the committed evidence and catalogue as fixed inputs.
A fresh GAP export may reorder conjugacy-class records while preserving every
paired class order/size and mathematical output. The independent check also
records its input SHA256, so that provenance field can differ after such an
export; use the fixed committed inputs for the byte comparison above.

Reproduce Iris's supporting Hall controls, independently written with
explicit semidirect multiplication and changed parameters:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 group_theory/nonsolvable_cyclic_gap_induction/checks/iris_hall_v1.py \
  --output /tmp/iris-hall-v1.json
cmp group_theory/nonsolvable_cyclic_gap_induction/checks/iris_hall_v1.json /tmp/iris-hall-v1.json
```

The largest fixture has 5819 elements; the checker took about 14.4 seconds
in Iris's environment. It uses one process and no external package or solver.
The optional sharper margin in Iris's report is outside the original Hall
handoff and is not required or used by the classification proof.
