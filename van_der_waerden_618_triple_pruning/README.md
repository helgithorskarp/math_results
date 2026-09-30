# Exact three-column pruning in the period-618 construction

Agent: **six-vdw-1**. Role: **researcher**. This is a construction-search reduction for symmetric two-color/seven-term van der Waerden numbers. It does not provide a progression-free coloring of 3704 points or a new van der Waerden bound. Both supplied words are invalid. The reusable result is the minority-row bound below, together with a complete, independently checked application to two explicitly specified words.

For the preferred word of static cost 584, the bound discards **22,099,375** of the **22,106,375** changes to exactly three distinct columns. Independent exact checking of the remaining **7,000** alternatives shows that every three-column change strictly increases the cost. For the specified cost-585 exit word, the bound discards **22,100,250** changes; checking the remaining **6,125** shows that no three-column change lowers its cost. Each conclusion is local to its named word. Other words, larger moves, and the unrestricted construction remain open.

The static cost is the number of violated long signed NAE constraints, each with unit weight. A positive score means a cost reduction. The residual maximum scores are -2 and -1, respectively; these are **not** asserted to be the maximum scores over the whole neighborhood, since pruned alternatives are handled by upper bounds.

## Construction and exact model

Write a period-618 word as

\[
c(t)=\mathbf1\{(t\bmod6-\phi(t\bmod103))\bmod6\ge3\},
\qquad \phi:\mathbb Z/103\mathbb Z\longrightarrow\mathbb Z/6\mathbb Z.
\]

All 103 phases are free. This is the full six-state column family, with no fixed multiplicative skeleton, reflection condition, or affine stabilizer restriction. The halfword on residues 0 through 308 determines the other half by complementation. Canonical signed NAE constraints partition its 309 variables into 103 disjoint triples. Each triple has six legal states, hence five alternative states. Every long row has seven literals from seven distinct columns. A three-column move changes all three chosen columns to different legal states, giving

\[
\binom{103}{3}5^3=22,106,375
\]

alternatives. Column identifiers in the output refer to the order of the canonical signed triple constraints, not to the CRT residue labels.

The generator checks the exact model SHA256 `093dd57840c2e9de0eb17dd3aa90df45cb9361e3dee72809a20c942145713986`: 103 short rows and 94,554 long rows. It enumerates starts 0 through 308 and steps 1 through 309, reduces tautological and repeated signed literals, identifies a row with its global complement, and sorts the remaining rows. Other starts complement the row; other steps reverse it. No large model file is committed.

The [binary-fiber reduction](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_618_binary_fibers) establishes that, for legal columns, the complete number of monochromatic cyclic start/step pairs is four times this unit cost. The [phase normal form](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_618_phase_symmetry) describes the six-state columns. Only those bridges are used here; their separate restricted-family exclusions are not premises of this pruning lemma. The previous [exactly-two-exception cut](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_618_two_exception_cut) is background to this different, variable-column construction direction.

## Minority-row lemma

Consider any signed NAE model whose variables are partitioned into columns, whose legal column states have specified alternatives, and whose cost rows contain seven literals from distinct columns. Nonnegative row weights are allowed in this abstract lemma. Fix a legal word and let the score be old cost minus new cost. Write \(s_a(i)\) for the score of alternative state \(i\) in column \(a\). For two states, define the exact pair correction

\[
K_{ab}(i,j)=G_{ab}(i,j)-s_a(i)-s_b(j).
\]

For three changed columns the exact score has the expansion

\[
G_{abc}(i,j,k)=s_a(i)+s_b(j)+s_c(k)
 +K_{ab}(i,j)+K_{ac}(i,k)+K_{bc}(j,k)+T_{abc}(i,j,k).
\]

Let \(P_{abc}\) be the total weight of these rows:

1. Current monochromatic rows containing all three columns.
2. Rows with exactly two minority literals, both in the selected columns, and a third selected column containing a majority literal.

Then \(T_{abc}(i,j,k)\le P_{abc}\) for every choice of states.

To prove it, consider one row with current true-literal count \(q\), and put \(V(q)=\mathbf1\{q=0\text{ or }q=7\}\). A changed column flips either its sole row literal or none. If any of the three literals does not flip, the row's third difference is zero. Otherwise write \(\delta_a=1-2b_a\), where \(b_a\) is its current truth value, and similarly for the other two literals. The third correction is

\[
V(q)-\sum_{u\in\{a,b,c\}}V(q+\delta_u)
 +\sum_{\{u,v\}\subset\{a,b,c\}}V(q+\delta_u+\delta_v)
 -V(q+\delta_a+\delta_b+\delta_c).
\]

It belongs to \(\{-1,0,1\}\), and is positive exactly in cases 1 and 2 above. This follows by counting the minority literals; `row_controls()` also checks all 128 truth words and all 35 selected triples (4,480 cases). Multiply each row inequality by its nonnegative weight and sum. The score expansion itself is the three-variable finite-difference identity, summed over rows. No historical-priority claim is made for finite differences or local search.

For completeness, when two row literals actually flip, their pair correction is

\[
V(q+\delta_a)+V(q+\delta_b)-V(q)-V(q+\delta_a+\delta_b).
\]

It is -1 on a current monochromatic row, +1 when the pair consists of a sole minority and a majority literal, -1 when it consists of both minority literals in a two-minority row, and zero otherwise. If either literal does not flip, the correction is zero. These cases form the literal interaction matrix; all 2,688 pair cases are checked separately.

## Consistent-anchor bound

Set \(M_{ab}=\max_{i,j}K_{ab}(i,j)\) and

\[
C_{ab}(i)=\max_j\{s_b(j)+K_{ab}(i,j)\}.
\]

Keeping column \(a\)'s state consistent across both adjacent pairs gives

\[
G_{abc}(i,j,k)\le
 U_a:=\max_i\{s_a(i)+C_{ab}(i)+C_{ac}(i)\}+M_{bc}+P_{abc}.
\]

The analogous \(U_b,U_c\) also bound every score. So does the coarse sum of the three maximum single scores, the three \(M\)'s, and \(P_{abc}\). Use the minimum of these four bounds. For an integer target score \(h\), a triple with upper bound less than \(h\) needs no state enumeration. The implementation skips anchor evaluation when the coarse bound already falls below the cutoff; its recorded bound histogram then retains that sufficient coarse bound. The implementation is for **unit weights**; the stated nonnegative-weight extension is an elementary written argument, not an implemented weighted experiment.

In the preferred-word application \(h=0\), leaving 56 triples (7,000 choices). In the exit-word application \(h=1\), leaving 49 triples (6,125 choices). Each discarded triple represents all 125 legal choices. Every retained choice is scored by a separate truth-row bitset formula: a row becomes monochromatic precisely when all its minority literals flip and none of its majority literals flips. This checker does not use the finite-difference tensor or the pruning bound to calculate scores. It is compared with direct signed-literal evaluation in 21,875 small-model cases covering all initial truth counts 0 through 7. Every one of the 131,325 production pair entries also agrees between the literal interaction matrix and the independent bitset evaluator.

## Reproduction

Python 3.10 or later and its standard library suffice; the recorded run used Python 3.11. Run without Python `-O`. From this directory:

```sh
python3 reproduce.py
```

This runs one child at a time, with 30-second internal budgets, a 45-second parent timeout, and all numerical thread settings equal to one. Each exact case has fewer than 200,000 residual choices. It reconstructs the model in memory, checks every pair interaction, prunes all 176,851 triples, independently evaluates all remaining choices, and compares the deterministic summaries with `expected.json`. Generated histograms and halfwords stay in ignored `build/`. A tiny deadline must fail without producing a complete summary. A timeout or incomplete computation proves no exclusion.

The separate [definition-level checker](check_coloring.py) then enumerates all **381,306** cyclic start/step pairs and all **1,141,450** positive-step integer seven-term progressions on 3704 positions. It reports 2,336 cyclic monochromatic pairs and 6,995 integer progressions for the preferred word, and 2,340 and 7,009 for the exit. Thus both remain invalid. Integer indices in its output are zero-based; adding one gives the coloring of `[1,3704]`.

For one bound computation:

```sh
python3 triple_pruning.py --case preferred584 --output build/preferred.json --expected expected.json
```

Choose a new output path or a new `--builddir` for replay. `cases.json` contains only the two small input halfwords; `expected.json` contains counts and canonical histogram hashes; `ap_expected.json` contains independent AP-check results. The core `analyze` function accepts another legal halfword in this same exact model, with an explicit score cutoff and bounded residual domain. Bounds cannot be transferred between words without recomputation.

The proof is an unformalized exact finite argument with same-author independent algorithms, not an external review or proof-assistant theorem. No SAT result, proof converter, solver timeout, private ledger, or omitted large certificate is needed. Large model files, binaries, raw search dumps, and dynamic search states are intentionally absent.

Primary context is [Monroe, Tables 1 and 2](https://arxiv.org/html/1603.03301v7), giving the symmetric seven-term/two-color seed `>3703` and prime 617. Monroe writes `W(length,colors)`, reversing this campaign's `W(colors,length)`. The paper's seed is background, not a novelty claim. Related construction context is [Herwig et al., A New Method to Construct Lower Bounds for van der Waerden Numbers](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf). This period-618 local-search reduction has different hypotheses from the complementary fixed QR617 repair and affine-seam edit bounds; none of their numerical constants is used.
