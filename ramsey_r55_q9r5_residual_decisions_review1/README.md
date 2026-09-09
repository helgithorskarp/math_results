# Independent review of the complete q9,r5 residual test

**Verdict: ACCEPT with high confidence, conditional on the inherited task-family
cover.** The literal evidence establishes exactly the negative result claimed in
h4089: each of the 362 listed forced 23-vertex residuals is feasible, so this
necessary-condition gate excludes none of the corresponding parent tasks.

This is an intermediate reduction result, not the target Ramsey breakthrough.
A feasible residual need not extend across the omitted first 20 vertices. The
evidence supplies no 43-vertex Ramsey(5,5) graph, decides no complete parent
task, and does not prove `R(5,5) >= 44`.

## Independent recheck

[check_bitsets.py](check_bitsets.py) ignores the submitted CNFs, clause
metadata, encoder, and SAT solver. It independently decodes the graph6 core and
each 253-bit literal edgeword, checks the four pinned blue K4 blocks and exact
core, then searches for red K4s and blue K5s with an ordered bitset recursion.
It also checks all task identities and statuses, validates that every one of the
362 catalogue records is literally Ramsey(4,4), and requires 362 distinct
witnesses.

The bitset clique routine is checked against direct subset enumeration for all
1,024 labelled graphs on five vertices and clique orders 2 through 5 (4,096
comparisons). Five deliberately damaged inputs—padding, a fixed block edge, a
red K4, a blue K5, and the pinned core—are rejected. The compact expected result
is [EXPECTED.json](EXPECTED.json).

From the repository root, with the pinned 2,172-byte `r44_7.g6` catalogue:

```sh
python3 -B ramsey_r55_q9r5_residual_decisions_review1/check_bitsets.py \
  /path/to/r44_7.g6 \
  --expected ramsey_r55_q9r5_residual_decisions_review1/EXPECTED.json
```

The review obtained:

```text
status = ALL_362_LITERAL_RESIDUAL_WITNESSES_VALID
tasks_checked = 362
red_K4_found = false
blue_K5_found = false
new_whole_task_exclusions = 0
good43_found = false
solver_calls = 0
ledger_sha256 = b468fd4f3c24a955d84fcc9ad36f15bbdac70be33e175a7d153a0ca3884bfd60
```

I also ran the target's full solver-free replay. It regenerated and reverse-
audited all 362 formulas and 9,603,776 clauses, ran the complete release C++
audit, checked all 362 witnesses under ASan/UBSan, checked formulas 0, 181, and
361 under sanitizers, and passed all stated corruption controls. Its exact
`RESULT.json` SHA256 was
`c4250c607f9e3cf26e5bab01d62e21676220fdfe64dc458f6babb7292b035311`.
The large generated CNFs, binaries, and logs remain outside Git.

## Mathematical bridge and scope

Under h3887's parent-task convention, physical vertices 0 through 19 are five
red K4 packing blocks, vertices 20 through 35 are four blue K4 blocks, and
vertices 36 through 42 are a pinned seven-vertex core. Maximality of the red K4
packing makes the induced residual on vertices 20 through 42 red-K4-free; the
Ramsey target makes it blue-K5-free. Thus any complete parent solution restricts
to one of the residual problems. An UNSAT residual would exclude its parent,
while a SAT residual proves only that this necessary local condition is
feasible.

The 362 published edgewords directly prove feasibility of the 362 *listed*
residual instances. Elevating “listed” to “all q9,r5 tasks” imports two
completeness claims not re-proved here: McKay's isomorphism completeness for the
seven-vertex Ramsey(4,4) catalogue and h3887's completeness of the ordered
maximal-packing task cover. The global count of 2,188,660 UNKNOWN whole tasks is
also imported administrative state. These boundaries do not affect the literal
validity of any individual witness.

For external context, McKay's [Ramsey graph catalogue](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)
lists 362 Ramsey(4,4) graphs on seven vertices. The current published upper-bound
work is Angeltveit and McKay's [`R(5,5) <= 46`](https://arxiv.org/abs/2409.15709).
Neither source independently certifies this team's task-cover machinery.

## Strengthening and improvement opportunities

- Do not retry the same residual gate: every member now has a literal feasible
  witness. Attack extension to the first 20 vertices, or add a genuinely
  stronger necessary condition.
- Try to extend witnesses to complete parent tasks. For failures, retain
  independently checkable UNSAT certificates such as DRAT rather than solver
  return codes.
- Analyze common structure across the 362 witnesses to find constraints that
  survive the omitted parent interface and could separate extendible from
  non-extendible residuals.
- Formalize the maximal-packing-to-residual implication and independently
  regenerate the parent task cover or catalogue completeness if an
  unconditional “all q9,r5 tasks” statement becomes load-bearing.

## Provenance

Target Discovery ref:
`bafkreibxskzkrn3qrrmne6oebzxopuuto6mbjggmwrrldzgi6ywaoansku` (h4089).
Target source commit:
`eae6ccf7b93f81c17af4319c91b6b0491496852e`.
The review package is at the stable
[GitHub directory](https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_q9r5_residual_decisions_review1);
its publication commit is recorded in the associated Discovery Net review.
Machine-readable scope and replay details are in [EVIDENCE.json](EVIDENCE.json).
