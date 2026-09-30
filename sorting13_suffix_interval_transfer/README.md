K18 suffix intervals after a generalized prefix

Author and executing agent: **six-sorting-2, researcher**.

Every 18-comparator completion of the exact 127-state ten-wire set K in fixture.json has interval components in every suffix graph on its actual output channels. A suffix graph has one vertex per channel and one edge for each comparator in that suffix. This is a necessary restriction for this fixed-prefix frontier; the published terminal-block theorem itself is reused with explicit credit.

The 17-comparator prefix of eleven inputs has oriented comparators and a wire permutation. Its normalized wire frame is [0,1,4,2,3,7,8,5,6,9,10], so an argument is required to transfer the ordinary terminal-block theorem back to the actual K wires. [PROOF.md](PROOF.md) gives that argument using deterministic untangling, a reverse frame induction and the known eleven-input lower bound 35. It applies to all comparator orders and allowable depths.

The terminal-block theorem is Theorem 2 and its consecutive-channel consequence in [Codish et al., Sorting Networks: to the End and Back Again](https://arxiv.org/html/1507.01428#S3.SS1). The eleven-input bound comes from [Harder, An Answer to the Bose-Nelson Sorting Problem for 11 and 12 Channels](https://arxiv.org/abs/2012.04400); the [current table](https://bertdobbelaere.github.io/sorting_networks.html) gives S11=35 and the unresolved S13=44..45, checked 2026-09-30. The K fixture and its provenance are reused from [the double-pure obstruction](https://github.com/helgithorskarp/math_results/tree/main/sorting13_double_pure_obstruction), source b10a2bd5584e90135012808e6eef049bd3544fca, graph bafkreibfy2xvvhtwcnd7yjvo4rg7up5dzasdvufticbqbfj76buoo6cs3q. The earlier K18 route restrictions and pure-minimum exclusion remain separate dependencies of the research frontier.

There are 512 interval partitions of ten channels. A backward comparator may erase zero or one separated boundary. Spanning two separated boundaries would join nonadjacent blocks and is forbidden. Comparators within the same block remain allowed. interval_blocks.py adds 171 Boolean variables and 9243 clauses to an 18-slot selector encoding, whose choices already select exactly one of all 45 pairs at each slot. Any depth is covered by sequentially ordering the 18 comparators.

Reproduce with standard-library Python 3.11 or later, without -O, one CPU and one job at a time:

```bash
python3 check.py
python3 check_encoding.py
```

check.py independently regenerates the normalized prefix, all 2048 original Boolean inputs, the 127-state K image and the known 20-gate control. It also checks all 2430 three-comparator generalized-prefix/ordinary-suffix factorizations on three channels, including all 180 sorting instances; 378 two-comparator factorizations have no sorting instance. A four-comparator counterexample demonstrates why the comparison lower-bound premise cannot be dropped. These controls complement the written general proof.

check_encoding.py compares the generated clauses with an independent disjoint-set graph algorithm on all 512 partitions and 45 comparators: 23040 transitions, 11278 allowed transitions and 11762 rejected noninterval merges. It rejects 101502 wrong successor-bit controls and checks every clause on the independently simulated known 20-gate K control. certificate.json and source-manifest.json pin the compact fixture and source.

This restriction leaves the numeric frontiers K18..20, X21..22 and S13=44..45 unchanged. No K18 exclusion or 44-comparator construction is asserted. The trust boundary consists of the written untangling/frame argument and the two cited literature results. The finite source audits check the fixture, scope controls and exact encoding; they do not replace the general proof or constitute an external review or proof-assistant formalization.
