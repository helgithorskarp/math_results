# Exact exclusion of one Cyclic(43) defect-support repair family

This package certifies that an entire **2^60-assignment nonlocal repair
family** around a published Cyclic(43) objective-12 state contains no good43
graph.  The result is a complete-family exclusion, not a target construction
and not a new bound for `R(5,5)`.

Among the 238 published objective-12 representatives, an exact census selects
the smallest defect-edge support size and then the smallest source index.
Thirteen sources attain size 60; source 51 is selected.  It has twelve red
monochromatic five-sets.  The repair family frees every edge appearing in one
of those defects and fixes the other 843 physical edges as in source 51.

Every one of the 60 free edges has a five-vertex witness whose other nine
edges are fixed blue.  Avoiding a blue `K5` therefore forces that edge red.
After all 60 implications, the first original red defect is again a red
`K5`.  A 61-clause physical core—60 unit clauses and one ten-literal
clause—certifies UNSAT by unit propagation.  No SAT-solver answer is trusted.

From the repository root, run into a fresh directory:

```bash
python3 -B ramsey_r55_cyclic43_q12_defect_support_exclusion/reproduce.py \
  /tmp/r55-cyclic-defect-support-replay
```

Expected status:
`REPRODUCED_CYCLIC_Q12_DEFECT_SUPPORT_FAMILY_EXCLUSION`.
The replay compiles strict release and address/undefined-sanitized C++20
programs, regenerates the 238-row census, checks it with an independently
implemented clique-recursion census, rebuilds the complete 600-clause family
formula and compact core, verifies every physical five-set witness under
normal and `-O` Python, and rejects altered census and certificate inputs.

The family permits arbitrary simultaneous changes of its 60 edges; it is not
the earlier alternating two-switch neighborhood.  Only source 51 is decided.
No conclusion is drawn about the other 237 representatives, other choices of
free edges, the disconnected Cyclic landscape, or the h3987 q10 ledger.
See [PROOF.md](PROOF.md) and [HANDOFF.md](HANDOFF.md).
