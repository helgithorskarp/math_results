# Exact wheel interface for the unresolved heptagon pairs

**Completed reduction; inconclusive pilot.** The origin's 84 neighbours
in the 421-point heptagon difference graph form 14 disjoint six-cycles.
Pinning the origin colour to zero leaves exactly 66 three-colour states
on each cycle. Replacing these cycles by finite state choices gives an
exact encoding of ordinary four-colouring, including specified terminal
equalities. The reduction does not restrict colourings to potentials or
Kempe perturbations.

One bounded query was run for each of the three residual sqrt(3) pair
orbits. **All three returned UNKNOWN** at the conflict limit. No pair
forcing or additional monochromatic witness is established. The earlier
84 pairs with monochromatic witnesses remain settled; the other 42 are
unresolved. No five-chromatic graph or record improvement is found.

This completes the planned local-interface milestone. Further search on
this fixed seed is parked pending a stronger construction argument;
there is no automatic runtime or swap-depth increase.

## Exact graph partition

The input is D=H-H from the
[original heptagon package](../hadwiger_nelson_heptagon_difference_lifts/README.md),
source `b42754c605b69877056555955ac7f72a56e824f3`. Its sorted graph table
has SHA256
`54a68876eb8c55d885905482b8373c5542651f7683bf66d4406ce44825563458`.
The origin has label 210. Let N be its unit-neighbour set and let
B=D minus (N union {210}).

| Exact quantity | Value |
|---|---:|
| Vertices / unit edges in D | 421 / 1848 |
| Vertices in N / disjoint induced six-cycles | 84 / 14 |
| Vertices in B / B edges | 336 / 1260 |
| N-to-B edges | 420 |
| B vertices with zero / two neighbours in N | 126 / 210 |
| Connected components of B | 1 |

There are 84 origin edges and 84 edges within N. Together with the
1260 B edges and 420 cross edges these exhaust all 1848 edges.
[expected.json](expected.json) gives each cycle in a canonical order:
start at its least vertex, take its smaller cycle neighbour second, and
continue around the cycle. All points and unit edges are inherited from
the previously audited exact cyclotomic graph; this pass reuses its
verified byte-identical table, rather than claiming a new geometry audit.

The 14 residual equilateral triangles are precisely the alternating
triples of seven of these six-cycles, with indices
1,2,3,10,11,12,13 in the committed cycle list. Their three pair-orbit
representatives are [24,218], [24,395], [25,202], all in cycle
[24,25,218,396,395,202].

Fixing the origin colour to 0 costs no ordinary colouring, since colours
can be permuted globally. Every N vertex must then use 1,2 or 3. A
six-cycle has 66 proper colour rows: the elementary cycle formula gives
2^6+2=66, and explicit enumeration checks the count. Requiring the two
selected alternating vertices to agree retains 36 states in that cycle.

There is a useful local dichotomy. If one alternating triple of a proper
three-coloured six-cycle uses all three colours, each intervening vertex
has two differently coloured neighbours and must take the third colour.
Thus the other alternating triple also uses all three colours. There
are six such states. In the other 60 states neither alternating triple
is rainbow. The full histogram of the numbers of distinct colours in
the two alternating triples is (1,1):6, (1,2):18, (2,1):18, (2,2):18,
(3,3):6. This is only a fact about the cycle's local states, not a claim
that all 66 states extend over B.

## Encoding and equivalence proof

Use four Boolean colour variables x(v,c) for each v in B. Add an
at-least-one clause for each v and four equal-colour exclusions for
each B edge. For every cycle W and every allowed proper state s on it,
introduce a state variable y(W,s). Add an at-least-one state clause for
each cycle. For every cross edge vu with v in W and u in B, add

```
not y(W,s) or not x(u,s(v)).
```

For the chosen terminal equality, remove just the states in its cycle
whose two terminal colours differ. All other cycles keep all 66 states.
The base formula has no terminal restriction. There are no potential
variables, no initial-colouring constraints, and no restrictions on B
colours beyond proper graph colouring.

Every normalized ordinary proper colouring satisfying the target gives
a model: set its unique B colour variable and its matching state on each
cycle true, with all other variables false. Every clause then holds.

Conversely, take any Boolean model. Choose any true colour variable for
each B vertex and any true state for each cycle. The B-edge clauses give
proper B colouring. Cycle states are internally proper and avoid colour
0, so the cycle and origin edges are proper. Each chosen state's cross
clauses exclude its endpoint colour from every true colour at the
opposite B endpoint. Therefore every cross edge is proper under any
such choices. The selected terminal colours agree by state filtering.
This proves equivalence in both directions. At-most-one clauses are
unnecessary, including for state choices; multiple true choices cannot
invalidate this decoding argument.

The base formula has 2268 variables and 33110 clauses. Each terminal
formula has 2238 variables and 32030 clauses. These formulas are larger
than the original direct vertex-colour encoding; the purpose of the
change was to expose complete local cycle states for a different bounded
test. No speed advantage is claimed.

## Native pilot and exact scope

All three calls used Kissat 4.0.4, source
`8af8e56f174b778aef3aa45af9f739b2a5f492c2`, with
`--conflicts=200000 --time=60`, 4 GiB address-space and 256 MiB per-file
limits. Each stopped at the conflict bound, with exit code 0 and reported
UNKNOWN. The observed conflict counts were 200001, 200000 and 200000.
The base formula was not submitted to a native solver.

| Terminal pair | Elapsed seconds | Result |
|---|---:|---|
| [24,218] | 16.079 | UNKNOWN |
| [24,395] | 16.389 | UNKNOWN |
| [25,202] | 16.210 | UNKNOWN |

[pilot.json](pilot.json) pins all native input identities, reported
memory, limits and incomplete trace identities. The three traces total
103672852 bytes. They are local only, **not completed proof certificates**,
and were not presented to a proof checker as such. A timeout or conflict
bound is not negative evidence for ordinary colourability.

The exact formula reduction is proved above; no native result is a
premise of it. No selected pair is claimed forced or unforced by this
pilot. There was no fourth query, increased limit, support minimization,
larger graph, deeper swap layer, or new construction phase.

## Independent implementation checks and reproduction

[audit.py](audit.py) imports no producer module. It reconstructs each
neighbour component by graph reachability, finds its two orientations
by exhaustive permutations, and generates its proper states by recursive
extension rather than Cartesian-product filtering. It reconstructs all
four complete CNFs and compares every byte with the producer. This pass
also compared the three regenerated inputs directly to the original
native CNF files. The trust boundary includes the inherited exact graph,
the unformalized encoding argument, exact Python arithmetic and ordinary
runtime/code correctness. New author-run checks are not external review.

The audit checks base models arising from all 42 potential colourings
and six explicit nonpotential colourings, including every graph edge and
1589280 base-formula clause evaluations. Small controls exhaust 50688
explicit colouring cases across 16 nine-vertex graphs, each with three
terminal modes. They check 16 impossible interfaces with no allowed
state, ensuring that an empty choice remains an empty clause.

Use a full checkout and Python 3.11.2, standard library only, with
assertions enabled. Regenerate the original graph using its package
instructions, including its independent geometry audit if desired.
With that graph work directory, choose a fresh external interface output:

```bash
python3 -B interface.py --graph-work /scratch/fresh-heptagon-geometry --out /scratch/fresh-heptagon-interface
python3 -B audit.py --graph-work /scratch/fresh-heptagon-geometry --work /scratch/fresh-heptagon-interface
python3 -B controls.py
sha256sum -c SHA256SUMS
```

Expected audit status:
`EXACT WHEEL INTERFACE VERIFIED; THREE ORDINARY QUERIES UNRESOLVED`.
It takes about 5.68 seconds; new Python peak memory was not measured.
The optional `--native-dir` argument additionally compares the three
original native inputs when available. The complete original graph hash
and all four deterministic formula hashes are checked in either mode.

Optional native replay, on a POSIX host, from the already generated inputs:

```bash
python3 -B replay_pilot.py --inputs /scratch/fresh-heptagon-interface --out /scratch/fresh-heptagon-native --kissat /path/to/kissat
```

This reproduces the frozen limits and preserves raw outputs externally;
it does not certify any native answer. Any later SAT answer needs a
decoded proper colouring, and any UNSAT answer needs its complete proof
checked. The original UNKNOWN outcomes are historical observations, not
required outputs of a solver-free proof replay. No native call was
repeated merely for publication.

## Campaign checkpoint

The preceding [two-step Kempe checkpoint](../hadwiger_nelson_heptagon_kempe/TWO_STEP.md),
source `b7ecb27852a2c888393c59b6c98f7716efeafa46`, found no additional
pair witness. Its bounded failure is not a premise of the present
ordinary-colouring equivalence. This pass replaces that restricted
operation with a complete local-state formulation, but obtains no new
ordinary terminal relation.

New shared evidence read here is HN-2's
[A976 four-colourability certificate](../hadwiger_nelson_parts509_A976_colourability/README.md).
That closes the entire A-only support and its subgraphs, while the
fixed-small-partner composition remains open. Its separate boundary
interior has 951 vertices in one component. Those Parts results are not
premises of this heptagon analysis.

**Decision:** park further computation on this fixed D until a stronger
geometric composition or local-colouring argument gives a concrete
reason to resume. No record-sized composition is established by these
unresolved pair constraints. Preserve the exact inputs so another method
can resume without rebuilding the exploratory work. A next campaign
pass should choose a distinct construction mechanism or first supply
that missing argument; it should not automatically run a third Kempe
layer, another unchanged interface cohort or the old solved [0,332] query.
The teammate's A976 and proposed Heule-support directions remain separate.

This bounded follow-up is published as source and a checkpoint, without
a new Discovery Net result node for the three inconclusive native calls.
No running job or unfinished mathematical certificate remains.
