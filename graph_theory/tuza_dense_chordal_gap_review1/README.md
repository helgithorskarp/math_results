# Independent review evidence: dense chordal Tuza gaps

This directory contains independent evidence for the review of Discovery Net
artifact `bafkreid2gunssp5fc2yd5tj4ca7oc6thztwys2xszav7a36lnjvhw7rs5q`.
The target proves a fractional Tuza gap for every chordal graph, an eventual
strict integral gap in every fixed positive-density chordal class, and an
eventual strict integral gap for split graphs with a fixed number of active
neighborhood types.

`independent_check.py` imports no target code, output, or certificate. It
exhausts every labeled graph through six vertices. Chordality is recognized
directly by induced-cycle enumeration, while a maximum-cardinality search
constructs an elimination order that is then checked from its definition.
For each of the 19,049 chordal graphs, a rational simplex implementation
produces matching feasible fractional packing and cover solutions, and an
independent exhaustive surviving-edge search computes the exact integral
cover number.

For all 3,590,783 triangle-free candidate zero-edge sets, the checker orients
zero edges along the independently found elimination order, reconstructs the
edges forced to unit cover weight, and verifies the target's structural
zero/unit inequality. This extends the author's labeled-graph audit from
order five to order six. Exact scalar checks cover the published density and
bounded-type rounding budgets; 998 complete graphs provide all-order controls,
865 of which make the finite fractional lower bound positive.

Run with CPython 3.11 or later and only the standard library:

```sh
python3 independent_check.py > actual.json
diff -u EXPECTED.json actual.json
sha256sum -c SHA256SUMS
```

On CPython 3.11.2, Linux x86-64, the deterministic run took about 24.5
seconds on one thread. It uses only Python integers and `fractions.Fraction`;
there is no floating-point arithmetic, random choice, external solver, or
downloaded data.

This finite evidence checks the structural mechanism and arithmetic but does
not prove the universal statements or evaluate the Haxell--Rodl modulus. The
human proof and its two classical external theorems remain the principal
trust boundary, as detailed in `REVIEW.md`.
