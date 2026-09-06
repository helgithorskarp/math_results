# Exact interactions of 122 archived Heule completion centres

The fixed 122 fresh completion centres induce a **two-choosable graph**:
65 tree components and one 37-vertex component with a unique four-cycle.
The entire fresh graph has 57 edges. This gives a uniform sufficient
criterion for extending any colouring of any retained H510 vertices,
and an exact forest-based reduction for all other list assignments.
It establishes no graph improving the 509-vertex benchmark.

[PROOF.md](PROOF.md) states and proves the mathematical claims.
[certificate.json](certificate.json) gives every fresh edge, all 66
components and the unique cycle. Labels are the original `centre_index`
values from the archived table, not H510 vertex labels or positions in
the fresh list. The cycle is `1239,1370,1522,1371` in cyclic order.

The extension criterion is simple: if every retained fresh point sees
at most two colours on its retained old H510 neighbours, the old
four-colouring extends over all selected fresh points simultaneously.
With arbitrary lists, including singleton or empty lists, the tree
components admit exact bottom-up propagation; fixing one cycle colour
reduces the remaining component to a forest. This gives at most four
forest passes for a fixed old four-colouring, with no SAT call.

## Reproduce and verify

From the repository root, CPython 3.11.2 with the standard library suffices:

```sh
python3 -B hadwiger_nelson_heule_fresh122_incidence/verify.py \
  --out /tmp/hn-fresh122-check
```

This standalone check reads the two pinned public input files and this
package. It computes every one of the 7,381 fresh pairs and 62,220 fresh
versus old pairs exactly, reconstructs the component structure, and
compares the entire certificate. No original triple census, SAT solver,
colouring library, raw transcript or other scratch output is required.

For separate production and entrywise comparison of all exact norms:

```sh
python3 -B hadwiger_nelson_heule_fresh122_incidence/census.py \
  --out /tmp/hn-fresh122-run
cmp hadwiger_nelson_heule_fresh122_incidence/certificate.json \
  /tmp/hn-fresh122-run/certificate.json
cmp hadwiger_nelson_heule_fresh122_incidence/result.json \
  /tmp/hn-fresh122-run/result.json
python3 -B hadwiger_nelson_heule_fresh122_incidence/verify.py \
  --out /tmp/hn-fresh122-audit --transcript /tmp/hn-fresh122-run/norms.txt
```

Expected facts: 122 distinct fresh points, common denominator 96, 57
fresh edges, 551 old attachments, 66 components, and the displayed sole
four-cycle. The canonical stream of 69,601 complete squared-distance
vectors has SHA-256

```
f319dfe814bb9a2259a914b74c79adde9272422e4e761d57dc308fc750a638f7
```

Each stream line is `F centre_i centre_j n0 ... n7` for increasing fresh
pairs, followed by `H centre_i old_vertex n0 ... n7` in fresh-then-old
order. The n values are coefficients of squared distance multiplied by
96^2. ASCII decimal integers, single spaces and LF endings are used.

The producer uses rational XOR arithmetic; the verifier uses sparse
integer square expansion with squarefree-radicand reduction. They also
use different component/cycle algorithms. The producer took about 12.3
seconds and the independent implementation about 1.3 seconds on the
producing machine. The checker includes four exact norm controls, all
1,296 two-element four-colour list assignments on the cycle, and five
malformed-certificate rejection checks. [validation.json](validation.json)
records the actual runs. This is implementation independence within one
author's pass; no independent author review or formalization is claimed.

## Inputs, coordination and claim boundary

[plan.json](plan.json) freezes the two coordinate inputs and the finite
comparison domains before the census. [manifest.json](manifest.json)
records source provenance and dependencies. The fresh table comes from
the completed `hadwiger_nelson_heule510_completion_frontier` census. Its
original 21,978,620 triple enumeration was not repeated here and is not
a premise of the conditional theorem for these 122 explicitly defined
points. Their recorded old neighbour sets are rechecked completely.

The closed H514 family supplies historical motivation only. Its four
fresh points belong to the new 37-vertex component, which includes 33
additional points. The H517, H574 and parked Parts support closures
remain closed; this pass performs no deletion search in those supports.
The teammate's new two-centre circle/domination theorem is a separate
geometric mechanism, with no dependency in this proof.

The remaining trust boundary is the interpretation of the two hashed
coordinate tables, the elementary exact-field and graph arguments,
CPython arbitrary-precision arithmetic and the checker's code. There
are no floating-point decisions, native solver verdicts, UNSAT traces
or assumed colouring-library completeness in this result.

The next coherent direction is a bounded whole-support test on
H510 union all 122 centres, using the certified forest/cycle structure
to project fresh choices. A given old positive colouring must first
extend across the chosen fresh support before it yields a valid cut.
The 37-vertex coupled component identifies where the old H514 path
interacts with additional points. No extension oracle, candidate search,
new support-colouring query or background computation has started in
this package. A full 632-point family closure remains open.
