# Odd-prime restrictions for Book Ramsey candidates

Author: **six-books-2**, role **researcher**, 2026-10-01.

[PROOF.md](PROOF.md) gives an ordinary proof excluding automorphism
orders7,13,17,19 for a simple22-vertex red graph of maximum degree ten,
red-edge page cap three and blue-edge page cap six. All order-seven
cycle types are covered. The difficult7^3 1 case is closed by a fixed
degree-seven root, correlations of three-sets in Z7, and an explicit
blue B7. No minimum-degree theorem or host census supports that proof.

With [the order-eleven result](../order_eleven_correlation/PROOF.md),
the conditional automorphism-group order is2^a3^b5^c. Combining the
credited [upper-ten theorem](../../../book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md)
and [previous order-five result](../order_five_four_cycles/PROOF.md)
gives2^a3^b for every valid22 graph. This global corollary inherits the
order-five theorem's finite proof and historical minimum-degree
classification; those are not premises of the new conditional proof.
The Ramsey interval22..23 and asymmetric construction possibilities
remain open. Independent review of this theorem is pending.

From this directory, CPython3.11+ and no third-party packages:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O verify.py
```

Both programs compare compact summaries with [expected.json](expected.json).
`check.py` uses sets and literal graphs to validate fixed-label packing,
the displayed scalar/correlation cases, all seven explicit phase books,
deterministic page identities, the primary21 incumbent and KG(7,2).
`verify.py` imports no checker and uses bitsets and a separate graph
construction. It validates the controls and covers all1,881,600
degree-seven fixed-root templates **after the ordinary scalar reduction**,
finding zero survivors. This is not an unrestricted host census. It
uses complete grouped rejection for choices whose A block already fails;
all remaining choices are evaluated. The theorem is ordinary mathematics
and does not depend on completing either program.

[phase_books.json](phase_books.json) contains seven small literal books,
with vertex coordinates defined in the proof. [primary21.rows](primary21.rows)
is the known93-edge witness derived from the authors' [primary matrix](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt),
off-diagonal complement taken as red. The original raw matrix SHA256 is
3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55;
the compact red rows SHA256 is
4f1dd2bc743590a0553107936656e469db6e7d742db0456d697353ce50aac5ec.
The primary graph and the KG(7,2) control are prior art. Their exact
verification is validation, not a new construction or lower bound.

Only compact proof, source, fixtures and expected summaries are included.
No private ledger, key, solver log or graph corpus is published. Source
publication does not replace the written coverage and counting arguments.
