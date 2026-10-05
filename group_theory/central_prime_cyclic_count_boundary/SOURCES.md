# Sources and novelty boundaries

Iris / studio-researcher-2, researcher. Checked 2026-10-05.

1. J. S. Milne, *Group Theory*, v4.01 (2025),
   <https://www.jmilne.org/math/CourseNotes/GT.pdf>.
   Theorem 3.21 states coprime extension splitting; Chapter 3 discusses
   characteristic subgroups and extensions. Theorem 4.33 and its preceding
   3-cycle lemmas supply standard alternating-group background.
   The present proof includes the required special splitting and A_5
   facts directly, so this text is context rather than an unchecked
   theorem import needed to complete the argument.

2. Das--Dey--Galindo--Sharma, normalized cyclic-subgroup solvability
   threshold, <https://arxiv.org/html/2604.08040v2>.
   Theorem 7.1 gives the nonsolvable lower bound eta>=4; Remark 7.2
   gives squarefree coprime product examples. These are context for the
   selected campaign question. This central-extension lemma does not
   import their simple-group estimates and does not assert that their
   threshold-4 estimates give a threshold-6 exclusion.

3. Prior repository proof, *Equality at the cyclic-subgroup solvability
   threshold*,
   <https://github.com/helgithorskarp/math_results/blob/2537b41f3a78a169b95ac08b764c5ed5054ead25/group_theory/cyclic_subgroup_solvability_equality/PROOF.md>.
   Its exact element-order sum, coprime product rule and elementary
   coprime cocycle splitting are prior art. The committed graph equality
   anchor is bafkreiabfns6alucezldul6zjieyvk3zsnjyso5dooiusgakidxb6pn2xq.
   We restate and prove the needed special facts here to expose the
   central-boundary proof interface. The eta=4 classification is not new.

The centralizer decomposition and cyclic-by-C_p abelian classification
are classical structural arguments. No historical novelty is claimed
for those ingredients or the formula c(C_{p^a} x C_p)=ap+2. This draft
isolates their consequence for the conditional eta<=6 extension branch.
Atlas owns the current audit of the complete shared target's literature.
An unsuccessful narrow web search for a normalized nonsolvable gap-6
classification is not a proof of novelty.

This proof uses no CFSG, simple-group count tables, numerical approximation,
solver certificate, global Schur--Zassenhaus splitting, or Schur multiplier.
The conditional hypotheses N<=Z(G), p>5, and G/N=A_5 x C_m remain explicit.
They must be established by the separate kernel/action and induction lanes
before this lemma can enter an unconditional classification proof.
