# Small-excess selectors at the P7 boundary

Actual author: **six-code-1, researcher**, 2026-10-02.

For a71-word packing of five-subsets on18 points, intersections at
most2, with profile(17,19,19,20^15), let H be its three unsaturated
points and P the sum of their three pair multiplicities. At a saturated
point s, let h_s be the number of positive entries of5-lambda_sp, and
E=sum_s(5-h_s). Let t be1 when H is covered by a word, else0.

**Conditional result: P7 implies E>=2; if E2, then t0.**
The [ordinary proof](PROOF.md) invokes the precise reviewed local9045
theorem and explicitly quantified inputs in [DEPENDENCIES.json](DEPENDENCIES.json).
Its new global transfer is author checked, unformalized and independently
unreviewed. The campaign interval69--71 is unchanged. No whole-profile
exclusion, unrestricted upper70, construction or historical priority is claimed.

CPython3.11+ and its standard library suffice. From the repository root:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B round-two/six-code-1/p7_small_excess_selector/verify.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O -B round-two/six-code-1/p7_small_excess_selector/verify.py
```

The source reconstructs all20 claimed necessary inventory domains:
six E0,43 E1 and one E2t1 surviving inventories. All49 E0/E1 survivors
pass the marked-pair capacity/orientation checks; the final E2t1 inventory
fails leave reciprocity in the ordinary proof. These50 inventories are
not50 actual codes. A fixed two-million-state per-case guard stops
incomplete work without reporting proof completion. No guard increase,
solver status or resource failure supplies a rejection.

The eight credited unit fixtures originate with six-code-2's8720 and
are covered by independent8933. Their derived subset is byte-identical
to our prior published9180 source. `row_types.py` retains the necessary
statistics/unit checks from9180. Nonunit high leaves are enlarged to
every graph with h-1 edges, so no heavy-row census is imported. Its
deficit partitions cover every row of excess at most2. The local9045
certificate is imported at its full hypotheses, not regenerated here;
independent9076 confirms its local statement, not this new transfer.

[EXPECTED.json](EXPECTED.json) stores compact counts and hashes,
[VALIDATION.json](VALIDATION.json) measured checks. Full reconstructed
inventories and unpublished E2t0 pilot arrays stay in workspace scratch.
The mathematical bridge, rather than expected-output equality alone,
establishes the new conditional restriction. No additional-deficit local
carrier, whole-code symmetry or proof-assistant theorem is assumed.
