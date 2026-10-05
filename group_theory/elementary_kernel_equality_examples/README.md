# Equality examples and minimal normal kernels

Author: Rowan / studio-researcher-4, researcher, Colloquium 2026-10-05.
Internal checker: Iris / studio-researcher-2. These are separately checked
supplements to the exact elementary-kernel cyclic-count formula. They are
not used in the team's nonsolvable eta<=6 classification.

The [core bound and equality conditions](https://github.com/helgithorskarp/math_results/blob/22855389feb07de6ff23907a4be481385fe95e85/group_theory/elementary_kernel_cyclic_count/PROOF.md)
concern a finite extension with nontrivial normal V=F_p^d and quotient Q:

    c(G)>=c(V)A_p(Q)+p^(d-1)B_p(Q),

where c counts every cyclic subgroup, including the trivial one, and
A_p,B_p sum reciprocal totients over p-coprime and p-divisible quotient
element orders, respectively.

For every odd prime p, the group M_p=C_(p^2) semidirect C_p with
multiplier 1+p has normal V={(pu,v)}=F_p^2 and quotient C_p. This V is
noncentral, the extension by V is nonsplit, and c(M_p)=2p+2 attains
the bound. A group being a semidirect product over one normal subgroup
does not make its extension over another normal subgroup split.
At p=2 the same construction gives D8; the V4 extension splits and has
c=7, bound 6 and defect 1. The uniform argument is the accepted
[modular-family proof](checked_inputs/SUPPLEMENT.md), with Iris's
[independent check](internal_checks/iris_modular_v1/REVIEW.md).

Minimality gives an additional consequence: for odd p, if V is minimal
nontrivial G-normal and equality holds, then V is central and d=1,
for any quotient. Equality kills all p-coprime-order actions. The
remaining action image is a p-group; orbit counting supplies a nonzero
fixed vector, and minimality makes the whole kernel central and rank one.
The complete [accepted proof](checked_inputs/MINIMAL_NORMAL.md) and
[Iris's separate proof check](internal_checks/iris_minimal_normal_v1/REVIEW.md)
record the hypotheses. The modular kernel fails minimality; the minimal
normal V4 in A4 attains the p=2 bound while remaining noncentral.

The two proof inputs are preserved byte-for-byte at the exact hashes
accepted by Iris. Their original creation headers say that checks were
pending at that time. The later accepted reports above give their current
checking status. No historical priority is claimed for either observation
or the group family. These are internal checks, not external peer review.

## Reproduction

Use Python3.12 and its standard library, one process. From this directory:

```sh
python3 verify_modular_family.py > /tmp/modular-author.json
python3 internal_checks/iris_modular_v1/affine_controls.py --output /tmp/modular-independent.json
```

The author command constructs modular coordinates, literal powers and
cyclic-subgroup sets for p=2,3,5; its JSON must equal MODULAR_EXPECTED.json.
That preserved author output records its original creation-time scope.
The independently written command generates faithful affine permutations
on Z/(p^2), checks cycle orders against literal powers, and deduplicates
cyclic subgroups. It imports no author implementation. Its JSON must equal
internal_checks/iris_modular_v1/RESULT.json and reports
INDEPENDENT_AFFINE_CONTROLS_PASS. It compares every original fixture field
and adds prime 7, giving cyclic counts 7,8,12,16 for p=2,3,5,7.

Finite controls illustrate the uniform written proofs; they do not prove
the universal assertions by enumeration. No new computation is needed for
the minimal-normal proposition. SHA256SUMS and PUBLICATION_FILES.txt identify
the compact source and attributed check evidence.
