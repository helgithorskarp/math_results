# Inputs and contribution scope

Rowan / studio-researcher-4, researcher, Colloquium 2026-10-05.

The sole research-lemma input is the
[exact elementary-kernel formula and equality conditions](https://github.com/helgithorskarp/math_results/blob/22855389feb07de6ff23907a4be481385fe95e85/group_theory/elementary_kernel_cyclic_count/PROOF.md),
PROOF.md SHA256: 813c8449357199d7db6ff9ac3f13725b6239dbb44f2bb721a78f748a90adc7de.
Its [Nova internal report](https://github.com/helgithorskarp/math_results/blob/22855389feb07de6ff23907a4be481385fe95e85/group_theory/elementary_kernel_cyclic_count/internal_checks/nova_v1/REPORT.md)
is separately scoped and is not expanded by these supplements.

Iris's modular-family check accepts checked_inputs/SUPPLEMENT.md SHA256
09e718b545780412c31f54d1f002c4bf72d74cfa17b92ccf922585e3d4406be5,
verify_modular_family.py SHA256: 3b5b6d306d21a94f30ef457ff39a5dd897ada12aaaac568af2883818d885a90a
and MODULAR_EXPECTED.json SHA256: 77183f0a4cbcc15c1af16b793c4c8c3ce2eeed81eb9783ff6a6562ff3ebb2fb8.
Her report SHA256 is f948f16fdb0c09cf9e16c93a3a68ee9bd4247f6aaf21b5afde980261e3bc7650;
independent permutation source, fixed comparison input and output are copied
unchanged to internal_checks/iris_modular_v1. Her optional final observation
is preserved with its original pending-check status; it is not counted as
another accepted source proof or another finite computation.

Iris separately accepts checked_inputs/MINIMAL_NORMAL.md SHA256
7c8f13f4a339f422db2210c5f7f06940bbaf97d4bda79516d50df79b3a593243.
The exact report SHA256 ac3e8021a477ef0f21d6c52c4e48acb607193d2ad105afa1c7d7a63a706ff450
is copied unchanged to internal_checks/iris_minimal_normal_v1. Its alternate
argument using Cauchy's theorem and a power of a preimage independently
checks Rowan's cyclic-parts argument. Both then use orbit-stabilizer and the elementary properties of
minimal normal and central subgroups; no CFSG, quotient classification,
irreducible-module theorem, faithful action or complement is imported.

The construction, norm identity, finite p-group facts and Cauchy/orbit
arguments are not asserted to be historically new. The value of these
notes is to state precisely when the core equality condition does or does
not imply centrality, and to preserve independently checkable examples.
The p=2 comparison and A4/V4 exception prevent an odd-prime assertion from
being silently broadened. The groups in the modular family are solvable
and do not refute the selected nonsolvable classification.

All original author/check files are preserved at their reviewed hashes.
Creation-time status text in those inputs is historical evidence; the
current acceptance is recorded in README and the later exact reports.
Neither the primary core proof nor the team's frozen classification is
modified by this separate source package. Internal checks and finite
controls do not establish historical priority or external publication value.
