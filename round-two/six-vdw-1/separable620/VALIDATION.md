# Recorded source-only verification

Actual author: **six-vdw-1, researcher**. All checks described in PROOF.md
passed in the fresh source-only replay on2026-10-01:

- 1111350 unique31-bit inputs and every literal product AP checked.
- All2^20 row inputs, the1024-row partition and every affine orbit audited.
- Pre-existing frozen entire deterministic evidence agreed; normal/-O
  row files and audits matched. The fixture was never written by replay.
- Every optimized/sanitized native output and record byte matched.
- 14322 small transfer-domain controls,602 positive inputs, and two
  extreme-domain controls passed;19 concrete damages rejected.

Fresh replay: 35.166186673 seconds, measured child peak459100KiB,33 sequential children.
Python3.11.2; GCC12.2.0; standard libraries only. Each child had a35-second
deadline, one thread and unchanged one-CPU/two-GiB scope. Peak includes
compiler/sanitizer children. Source hashes and compact expected outputs
are in SHA256SUMS and expected.json. Witnesses, binaries and per-stage
receipts regenerate outside Git.

Remaining trust: written CRT/orbit/walk-cardinality arguments, exact
source/checkers, interpreter and compiler runtime. No independent peer
verdict or formalization is asserted. The2480 cutoff is not claimed
optimal. General period620 and the3704-point target remain open.
