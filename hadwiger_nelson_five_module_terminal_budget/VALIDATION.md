# Validation record

The universal theorem is established by the written reduction and the small
complement/matching lemma in `PROOF.md`. The executable work supplies a second
finite proof route and checks the reusable input interface.

`kernel.py` uses a residual-degree row recursion to enumerate every labelled
simple graph on five through eight vertices with every degree in `{4,5}`.
This is a superset of all possible vertex-minimal counterexamples. For each
graph it checks `K5` containment and otherwise constructs and directly checks
a palette-normalized proper four-colouring. The expected counts are:

| vertices | all degree-4/5 graphs | containing `K5` | `K5`-free and coloured |
|---:|---:|---:|---:|
| 5 | 1 | 1 | 0 |
| 6 | 76 | 16 | 60 |
| 7 | 6,912 | 0 | 6,912 |
| 8 | 848,932 | 0 | 848,932 |

`audit.py` does not import that generator. It counts the complementary degree
sequences as coefficients of

```text
product_(i<j) (1+x_i*x_j)
```

and obtains the same four totals. It generates the exact component-order
cases arising in the eight-vertex Tutte argument, checks all 1,024
five-vertex graphs used by the matching sublemma, and checks all 32,768
six-vertex graphs used by the pairwise-intersecting-edge classification.

`verify.py` compares the independent counts entry by entry, checks the four
pinned h4051 source hashes and inherited budget numbers, and tests every
selected-pair choice in three abstract interface fixtures. The fixtures are
definition-level tests of the reduction; no claim that their edge lists are
new physical constructions is made. Eight malformed or logically invalid
instances must be rejected.

On the publication container, simultaneous normal and assertion-disabled full
replays took 191.926 and 190.974 seconds respectively. Runtime is dominated by
the 848,932 labelled order-eight kernels; the audit itself takes under two
seconds. The two modes returned the identical pinned result.

All graph states use arbitrary-precision Python integers. Edge order, graph
mask order, degree-sequence order, palette normalization, and JSON receipts
are deterministic. There is no randomness, floating point, native extension,
SAT/SMT solver, downloaded graph catalogue, private input, or omitted large
certificate. The two computations are same-author internal methods rather
than external peer review or proof-assistant formalization.
