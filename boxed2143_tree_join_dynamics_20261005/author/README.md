# Quinn's boxed-2143 legal-maximum-gap lane

This packet is groundwork toward the full growth decision ratified in chat 410. It does not prove an exponential bound or infinite limsup. The initial author derivation is in PROOF_DRAFT.md and awaits Theo's different-researcher check; finite implementation agreement is a separate scope.

Use Python 3.11.2 and the standard library. Entry indices are zero based and gap g follows g entries. Empty input is allowed as the unique insertion-tree root. Every other input is validated as a permutation of 1,...,n. A gap producing no *new* occurrence only gives an avoiding child when its parent is avoiding.

From this directory:

```sh
python3 -B kernel.py --pi 2,1,3
python3 -B verify_kernel.py --max-parent 7
```

The first command returns gaps 0,1,3 and an actual boxed-2143 witness after inserting 4 into gap 2. The second exhausts all 5914 parents of size 0 through 7, and all 46233 maximum-insertion instances. It compares complete child occurrence sets with a separately implemented literal definition. kernel_check_n7.json preserves the result, runtime, interpreter and occurrence-stream hash. This same-author check does not establish team-independent proof review or the infinite growth target.

Cross-team comparison uses the exact supplied checker files rather than rewriting their algorithms:

```sh
python3 -B compare_team_checkers.py --max-n 7 \
  --lyra /path/to/lyra/definition_checker.py \
  --theo /path/to/theo/rectangle_checker.py
```

team_check_n7.json records those exact hashes, all complete occurrence-set comparisons, and every new-maximum witness check through child size 7. Source bytes must remain stable during the run. This finite comparison uses three different reductions: four-index interior scans, canonical value rectangles, and nearest-greater triples under maximum restriction. The checks fail explicitly under malformed data or disagreement; no assertions are used as evidence.

graph_overlap_reuse.json records the narrow post-ratification committed audit reused from Lyra. Its filters and height do not establish absence of prior work or novelty. The coordinator's adaptive follow-up is also recorded in the checkpoint. No graph mutation, public push, or completion request is justified by routine setup.

Next structural obligation: control the evolving state for the entire class or give a compact counterexample to a proposed state. Such a state must support a uniform entropy/encoding proof before any full-target claim. Counts beyond source baselines are explicitly finite observations.
