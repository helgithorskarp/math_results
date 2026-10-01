Every standard thirteen-input sorter beginning with the literal changed
28-gate prefix in fixture.json needs at least45 total comparators, at
arbitrary suffix order and depth. A complete three-event argument
reduces it to the teammate's31-gate B/low0/high29 target; seven selected
nested-pruning domains exclude that root.

See [the proof](PROOF.md), [literal fixture](fixture.json),
[compact certificate](certificate.json), [column producer](generate.py)
and [standalone numeric checker](verify.py). From the repository root:

    python3 round-two/six-sorting-2/changed-b28-barrier/generate.py
    python3 round-two/six-sorting-2/changed-b28-barrier/verify.py

Python3.11.2, standard library, one job and BLAS/OpenMP threads1.
Expected status CHANGED_B28_SCALAR_CERTIFICATE_VERIFIED, selected
mass36*2^39 >2^44, seven domains and total lower bound45.
The producer pins dependencies in the neighboring native24-kernel-cover
and semantic-pruning directories. Normal/-O bytes and numeric finite
fields agree. The proof is author-checked and unformalized; external
independent review is not asserted.

The global44..45 gap remains open. No earlier changed-P19 patch cover,
native P21 exclusion or45-comparator completion is claimed.
