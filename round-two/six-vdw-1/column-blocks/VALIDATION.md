# Source-only validation

Author: six-vdw-1, researcher, 2026-10-01. The mathematical result is an
elementary conditional-cost identity and exact minimum algorithm. Its written
proof is unformalized; these computations validate the implementation and
the explicit invalid coloring data. Independent peer review is not claimed.

The complete reproduction passed in88.561044 seconds with448952KiB maximum
child RSS, including compiler/sanitizer jobs. All jobs were sequential and
all solver/BLAS/OpenMP thread counts were one. No limits were increased.

- The C++ kernel checks all4096 Gray-code assignments against direct
  polynomial evaluation in120 fixtures. A separate Python checker directly
  evaluates every state, its actual edit profile and allowed-flip mask,
  verifying the minimum in87 feasible and33 infeasible fixtures:
  **491520 states**, all four reference-class combinations. Normal/-O agree.
- ASAN/UBSAN kernel output matches release bytes. A ten-move sanitized
  native repair run matches all release checkpoint, best-word, gain, pair
  and block-cost bytes. Nine invalid kernel inputs are rejected.
- Literal geometry covers4464 actual APs at primes7,11,13,17,19,23. A
  twelve-bit p7 fixture checks all4096 assignments against140 literal APs,
  with nonzero cross terms. A boundary-column cubic control is exactly-3,
  demonstrating that the ordinary-column hypothesis is necessary.
- Three evidence corruptions (minimum score, infeasible status, fixture
  count) are independently rejected.
- A200-move run and100+100 restart match all saved bytes. A complete sweep
  and a partially saved/resumed sweep also match checkpoint, best-word,
  gains, pair costs, all4096 block costs, sweep state and sweep report.
- Five complete188805-pair sweeps reproduce the frozen-fixture curve
  **747,681,634,607,592,576**. Independent normal/-O audits count all
  **1141450** APs, verify all7408 raw/weighted single gains,16 pair entries,
  all8192 block cost entries, and the floor-constrained block optimum.
- Both supplied invalid words are counted independently. The526 word has
  original-reference edit profile[31,34] and supplies explicit bad APs.

Canonical reproduction result SHA256, excluding timing/resource metadata:

```text
6e1db99e12b294bbc7a7bfb7d51fefcc2aa054a6588ba8b2d4c111a52197ae88
```

The supplied747 word SHA256 including its newline is
`3e9e467b6a58dbd1e2f0c48d0bedcbaf2a1fd1c40b316e3091787caf5a32d552`;
the supplied526 word is
`584629f61ab417648b7c00b94f6a8f71acfa70ec65a3af2549f17e41fe455fc2`.
Generated576 word:
`6f786146aa13e8ce34dcbac61ce522557d35bd538da23d8f8516d6934ce8f04d`.

The checker imports no search or kernel implementation. Its conditional
census groups actual windows by their required selected-bit patterns rather
than using a quadratic coefficient formula. The optimizer check enumerates
states rather than conditioning/sorting. Exact Python integers are used.
No solver verdict, interrupted computation, positive cost or UNKNOWN result
is a premise of a mathematical exclusion. Full pair coverage concerns one
frozen finite neighborhood under prescribed edit floors.
