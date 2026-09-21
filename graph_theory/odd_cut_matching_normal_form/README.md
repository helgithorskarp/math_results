# A component-parity normal form for the odd-cut matching conjecture

This directory proves an exact structural reformulation of the
Máčajová--Škoviera condition on two perfect matchings in a cubic graph.

Fix perfect matchings `M,N` of a connected cubic graph `G`.  Let `F=G-M`,
contract every cycle of `F`, and retain the quotient edges coming from
`A=M-N`.  Then

> `M intersection N` contains no odd cut if and only if every component of
> this quotient subgraph contains an even number of contracted odd cycles.

Equivalently, write `M symmetric_difference N` as its canonical packing of
`M`-alternating cycles.  The pair is valid exactly when the quotient
components traced by this packing group the odd cycles of `G-M` in even
numbers.  This converts an a priori exponential family of cut constraints
into one component-parity check.

A useful consequence is also proved: if one `M`-alternating cycle meets every
odd cycle of `G-M`, toggling `M` on that cycle produces a second perfect
matching whose intersection with `M` contains no odd cut.  The number of odd
cycles is unrestricted.

The theorem is a normal form and sufficient mechanism, not a proof of the
Máčajová--Škoviera conjecture.  No historical-priority claim is made.

## Reproduction

The proof is in [PROOF.md](PROOF.md).  The definition-level checker uses only
the Python standard library:

```bash
python3 verify.py
```

Python 3.11 or later is sufficient.  The output must equal
[expected.txt](expected.txt).  The checker compares the quotient criterion
against direct enumeration of every vertex cut for every ordered pair of
perfect matchings in five named cubic graphs.  This finite audit checks the
normalization, loop convention, and both directions of the criterion; the
universal theorem rests on the written proof.

Expected-output SHA-256:
`811a1ca3d1097fd8e5133eaaf73bda0d84abbfd8914aef32eaaddacfe4000631`.
