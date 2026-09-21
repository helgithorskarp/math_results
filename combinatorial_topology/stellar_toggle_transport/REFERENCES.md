# Sources, dependencies, and claim boundary

Checked against the committed graph and live primary sources on 2026-09-21.

1. Antoine Amarilli, Mikael Monet, and Dan Suciu,
   [The Non-Cancelling Intersections Conjecture](https://arxiv.org/html/2401.16210),
   especially Propositions 4.7 and 5.8 and Section 7. The signed-multiplicity
   lower bound and the positive/negative and left-linear strengthenings are
   prior work. The present result combines those two strengthenings under a
   specific subdivision operation, assuming a suitable word on the input.

2. Hermann Wilhelm,
   [The Non-Cancelling-Intersections Conjecture Fails for Left-Linear Trees](https://arxiv.org/html/2608.19414v1),
   Definition 3.1, gives the lattice toggle game used here and counterexamples
   to universal winnability. His subsequent
   [Refutation of the Non-Cancelling-Intersections Conjecture](https://arxiv.org/html/2608.27416v1)
   refutes even the unrestricted tree version. We make no claim that NCI
   remains open, or that this closure theorem proves it for all complexes.

3. W. B. R. Lickorish,
   [Simplicial moves on complexes and manifolds](https://arxiv.org/abs/math/9911256),
   Geometry & Topology Monographs 2 (1999), 299–320; see Section 3 for stellar
   subdivisions and welds. The operation, its topological interpretation,
   and stellar equivalence are classical. Equivalence allows inverse moves;
   the forward transport theorem alone does not prove PL invariance.

4. Garett Cunningham, Daniel Zach, and Stefan Friedl,
   [Formalizing Abstract Simplicial Complexes & Stellar Subdivisions in Lean](https://arxiv.org/html/2607.10216v1),
   Section 3, provides a recent formal treatment of subdivision identities
   and links. Our Mobius identities are elementary consequences of the
   standard face structure, proved directly here. Their formalization does
   not verify our toggle compiler; no such implication is claimed.

5. Francesco Brenti and Volkmar Welker,
   [f-Vectors of Barycentric Subdivisions](https://arxiv.org/abs/math/0606356),
   for established subdivision face enumeration. Counting chains by ordered
   partitions and Stirling numbers is classical. Formula (4) in PROOF.md
   interprets the resulting Mobius-weighted count as an attained game optimum.

6. Previously published campaign result,
   [Shellings give universally optimal toggle words](https://github.com/helgithorskarp/math_results/blob/main/combinatorial_topology/shellable_toggle_optimality/PROOF.md),
   graph `bafkreibn42gwh6srjayktdnhjo5bj66lkjznpvlwdz2agvr6qnxgbnj3sm`,
   and its
   [independent review](https://github.com/helgithorskarp/math_results/tree/main/combinatorial_topology/shellable_toggle_optimality_review1),
   graph `bafkreifqtc2vcwo4a3txgzswtwj2d4katehheuwwkp6lxnms43uj4pj6yy`.
   The local cone-boundary word is an application of that compiler, recalled
   self-containedly here. The new step synchronizes arbitrary global input
   states through carrier fibers, and transports the exact multiplicities.

The graph-first source problem is
`bafkreiekhqdhv76zckh7tv4twtazwyhrjwjwrtha27a54lodtkxkx4nr2i`
(minimum order of an unwinnable lattice). Its full contribution/review
neighborhood was checked before work and refreshed before publication.

A bounded search combining NCI/toggle with stellar subdivision found no prior
legal-word transport statement. This supports only “new to the searched
sources”, not historical priority. The known shellable result already covers
subdivisions that remain shellable; the conditional theorem applies also to
nonpure and nonshellable inputs, with explicit RP2/torus examples. Mere
winnability of zero-free face lattices is known and is not the claimed advance.
The all-surface optimum, converse under stellar welds, and minimum unwinnable
lattice order remain unresolved by this work.
