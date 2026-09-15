Exact computer-assisted construction lemma and stopping result.  Let G be the
ten-point Golomb graph and B Parts' exact 214-point distance-three inequality
gadget, with marked terminals +3/2 and -3/2.  Under the two fixed isometries
L(x,y)=(x-1/2,y) and R(x,y)=(-x+1/2,y), each copy contains all ten Golomb
points.  Their collision-merged complete strict unit graph has 343 physical
points and 1,782 edges.  Of these, 108 are genuine cross-copy contacts outside
the inherited component edge sets.

After normalizing a Golomb unit triangle to colours 0,1,2, the bare Golomb
graph has exactly 95 proper four-colour patterns.  The complete opposed-B214
support admits exactly 66.  The pattern 0121212203 has checked proper lifts
through each B214 copy separately but no lift through the physical union, so
the interaction gain is strictly stronger than the isolated input relations.
All 66 positive patterns have literal full-graph colour words.  One
1,401-variable/9,823-clause CNF represents extension of any of the 29 missing
patterns; a deletion-free 1,382-lemma RUP trace derives the empty clause.  The
standard-library verifier regenerates the CNF and exact geometry and checks
the proof with its own watched-literal propagator.  The trace also passes
drat-trim -U.

The declared cap-feasible completion adjoins the full native A159 gadget.
Exact merging identifies 143 of its points, so only 16 are new; the resulting
support has 359 points and 1,893 complete unit edges, including 32 newly
introduced cross contacts.  Its complete Golomb relation remains the same 66
patterns and it has a checked proper four-colouring.  Both the 343- and
359-point graphs have chromatic number exactly four.  Thus the B214
subassembly is a positive physical relation source, while the native A159
completion is relation-neutral and this fixed architecture stops.

Public source and proof:
https://github.com/helgithorskarp/math_results/tree/42fd5e441e190a4022743479458aabf2ca55a85b/hadwiger_nelson_golomb_opposed_b214_stop

Standard-library verifier:
https://github.com/helgithorskarp/math_results/blob/42fd5e441e190a4022743479458aabf2ca55a85b/hadwiger_nelson_golomb_opposed_b214_stop/verify.py

Reproduce from a complete checkout with Python 3.11 or later:

```text
python3 -B hadwiger_nelson_golomb_opposed_b214_stop/verify.py --check-expected
python3 -O -B hadwiger_nelson_golomb_opposed_b214_stop/verify.py --check-expected
sha256sum -c hadwiger_nelson_golomb_opposed_b214_stop/SHA256SUMS
```

Mathematical-package commit:
42fd5e441e190a4022743479458aabf2ca55a85b.  S343 point/edge SHA-256 values
are 8e44b5746cc16badb0ddc6db1bb33d5d64baa088f0715a175632977c5d371a13
and af420d47cfdfd1ba44b8115b2e1a9d4e2364ff24f37690190625b46674f7e557.
S359 point/edge SHA-256 values are
9bfd53c6c77cd7e289cd076207bd6b6c2bd3302699ae6bf1270b622251cb2efd
and 99d62aea9625da3f23c7324f15feb22a51fbc9a941b7c951801911026bada85f.

This is author-side exact evidence, not an independent review, a five-chromatic
graph, a sub-509 candidate, or a record improvement.  It classifies only the
two fixed B214 frames and the one native A159 completion, and it does not
license a nearby phase, copy, or frame sweep.  Parts' 509-point/2,442-edge
construction remains the supported unrestricted record comparison:
https://arxiv.org/abs/2010.12665 .
