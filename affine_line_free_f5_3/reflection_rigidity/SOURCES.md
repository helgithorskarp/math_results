# Sources, dependencies, and novelty scope

1. C. Elsholtz, J. Führer, E. Füredi, B. Kovács, P. P. Pach, D. G. Simon,
   and N. Velich, *Maximal line-free sets in F_p^n*, Periodica Mathematica
   Hungarica **90** (2025), 7–21.
   [Primary paper](https://arxiv.org/html/2310.03382v2),
   [DOI](https://doi.org/10.1007/s10998-024-00617-x).
   This supplies the parameter and prior interval 70–73, and recalls
   the planar bound $(p-1)^2$. The present Gray-code census independently
   verifies the planar bound 16 for $p=5$.

2. Earlier campaign [odd-symmetry obstruction](../odd_symmetry/PROOF.md),
   source commit `3703f831791312b938f79cae978f11da50b4639f`,
   Discovery Net `bafkreic3tyudobjbkcrty6ihjmfggsqpef7a6g7lxqttj2gaes42a6gxee`.
   The final group theorem imports the order-three obstruction and the
   elementary exclusions of orders five and 31, which force a 2-group
   at size 71. Central inversion at 71 is ruled out directly in the new
   proof. The stronger bound two in this package follows from the
   new line-reflection and order-four obstructions.

3. Team A researcher 2's [upper-bound-71 theorem](../upper_bound71/README.md)
   closes the general 72-point case, giving the current interval 70–71.
   It was published during the present work and is context only.
   No part of that 4,332-case SAT exclusion is a premise here.

The two finite family bounds in this package do not use any campaign
global upper bound, low-plane certificate, or odd-order theorem.
Only the earlier odd-order obstructions enter the final group deduction.

Primary-source searches for line-free involution constructions and the
team graph refresh found no matching complete family obstruction before
this work. This is novelty relative to the searched sources, not an
exhaustive priority claim. The small controls verify the algorithms and
make no new lower-bound claim.

The team moment and two-nine-plane approaches provided complementary
global structure at 72. The certificate team has now closed that case.
The present result addresses the remaining 71-point construction frontier
and does not assume that arbitrary candidates have symmetry.
