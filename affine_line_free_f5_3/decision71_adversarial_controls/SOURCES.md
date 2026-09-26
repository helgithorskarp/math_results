# Sources and dependencies

- [Exact author proof and formula interface](../decision71/README.md): graph
  `bafkreic22u2qpq62lbr7vkt743ec37j4gygbnnufblyklm63o7rntyttja`, height 6076;
  original full proof source `c358411e750e0cea4dfee77fd7cb13d4d3f7560b`.
- [Independent reconstruction of all inputs](../decision71_independent_proofs/REVIEW.md):
  graph `bafkreibzukiugw4pdgcpp4xvdgzysosq7icuwyso5l7v6kgu45nu7rjcqi`, height 6092;
  source `c72217b52bd58ac0e4ee3d7c099be7fa6e644e48`. These four controls
  do not duplicate that complete audit.
- Researcher 1's [checker handoff and framing guard](../decision71_independent_proofs/HANDOFF.md):
  graph `bafkreigeldkfsk2lfsywy2mmacp5v4aglxibxozheghdvmmpvlnt3sjzd4`, height 6110.
  Its qualification of `-w` is used only in the optional diagnostic pass.
- [Preserved seed collection](../one_six_extremals70/seeds.json): source
  `2f56a0ad2ca1c5c51d034c651f5c457f1a75f67d`, graph
  `bafkreifi4girilsshyd6kbpxhfji5rthpvbvikf55siiljxkzsvfyjhsay`, height 6082.
  Seeds are checked directly; its classification theorem is not a premise.
- The paper seed is due to Elsholtz, Fuehrer, Fueredi, Kovacs, Pach, Simon
  and Velich, [Maximal line-free sets in F_p^n](https://arxiv.org/abs/2310.03382v2),
  *Periodica Mathematica Hungarica* 90 (2025), 7–21,
  [DOI](https://doi.org/10.1007/s10998-024-00617-x).
  Other seeds originate in the team's [order-three](../odd_symmetry/README.md)
  and [reflection](../affine_asymmetry71/README.md) construction packages.
- Primary software sources: [Python-SAT](https://github.com/pysathq/pysat)
  and [DRAT-trim](https://github.com/marijnheule/drat-trim/blob/master/drat-trim.c).
  Pinned DRAT-trim commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, source
  SHA256 `d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee`.

The pass-start and prepublication reviews inspected Team A reports, the exact
proof's graph neighborhood, new input/checker handoffs and repository commits.
At the recorded graph refresh, height 6115, no incoming `VERIFIES` contribution
accepted the exact theorem. Complete author proof and independent acceptance
remain distinct; this control package does not authorize handoff.
The final source refresh also inspected the author's warning-boundary update,
`71baf97aa30042dae257246268c978e95ed614a1`, in [CHECKER.md](../decision71/CHECKER.md).
It discusses the printer issue; the dependency-shift reproducer here is separate.

Bounded searches on first-in-type inputs reached their conflict budgets
without a witness; those UNKNOWN results establish no obstruction. The useful
controls instead came from adding one point to preserved 70-point examples
and finding admissible canonical projections. No exhaustive symmetry or
extremal census was performed, and no novelty claim about the checker issue
is made.
