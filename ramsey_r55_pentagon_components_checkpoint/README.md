# Unclosed all-pentagon component approach for good43

**The first all-pentagon milestone failed.** No complete good43 incidence
class was excluded, no target graph was found, and no Ramsey bound changed.
This package preserves an exact local calculation and the missing global
join. It is a failed-method checkpoint, not a global decision certificate.

The declared split was whether the hypergraph of **all** induced pentagons
has connected support spanning the 43 vertices. The disconnected or
nonspanning class was the intended exclusion. Every physical graph has a
unique such component partition; no automorphism or fixed pentagon is
assumed in the target.

The calculation found 344,282 ways to place all 25 arbitrary cross edges
between two pentagons without creating a pentagon meeting both. Survivors
exist at every cross-edge count from 0 to 25. A separate truth-vector checker
verifies the complete 33,554,432-assignment space, entry for entry, without
using the generator's recursion or degree test.

The global factorization step remains unavailable. The familiar control
`C5[C5]` has five internal pentagons and 3,125 pentagons using all five bags.
Every restriction to at most four bags has only its internal pentagons.
Thus even all four-bag checks do not justify a component join. The control
is a known good25, not a new construction or a target extension; no earlier
pentagon-product research is resumed.

[MATHEMATICS.md](MATHEMATICS.md) gives the exact scope, conditional profile
cover, and failed inference. The external theorem `N5=21` is used only for
coverage bookkeeping. Its order-20 computation is not replayed. The 1,502
necessary size profiles, including all 1,501 disconnected/nonspanning
profiles, remain unresolved here. These are profile counts, not counts of
physical graphs or candidate isomorphism classes.

From this directory, using CPython 3.11+ and g++ with C++17 support:

```sh
python3 -B reproduce.py /tmp/new-pentagon-component-replay
sha256sum -c SHA256SUMS
```

The scratch directory must be new and outside the package. Expected status:
`REPRODUCED_FAILED_COMPONENT_APPROACH_CHECKPOINT`, with zero global terminal
decisions. The generated matrix list and executable stay in scratch. Exact
expected results are in [EXPECTED.json](EXPECTED.json). The complete local
truth vector has SHA-256
`9a327505b4913dbee93da35b84d345cdb173d06227b504939e45036db42749f1`.

Remaining trust is the unformalized counting/coverage argument, C++ and
Python integer semantics, the independent local checker, and ordinary
hardware. No SAT solver, missing refutation, graph catalog, or floating-point
verdict is used. Author validation is not an external review. No Discovery
Net mathematical claim is submitted for this failed milestone.

The final authorized incidence pass requires a genuinely different
all-pentagon approach. Expanding this component catalogue or converting its
residual to another physical gluing formula is not the continuation earned
by this checkpoint.
