# Validation record

Actual agent: **six-vdw-1**, role **researcher**, 2026-10-01.
The complete source-only reproduction passed in **13.162842 seconds**,
with peak child resident memory **127284 KiB**, on Python3.11.2 and GCC12.2.0.
Every stage ran serially with one thread under the existing1CPU/2GiB scope.
No solver or downloaded proof input is used.

The release and ASAN/UBSAN native builds emitted byte-identical output.
The independent Python checker and its `-O` run emitted byte-identical
checked results. The pinned result SHA256 is
`24ec7d30444929e3d561d088d809df80cc3fdbcc4042174f46ea9099384867a1`.
It hashes the canonical compact JSON result dictionary, not the prose proof.

Complete mathematical coverage checked:

- All4194304 normalized23-bit words, with entry-by-entry comparison of the
  complete46-word survivor list to the independently constructed QR orbit.
- All256 normalized nine-bit words, including exact39 then3 then0 survival
  counts, with the three intermediate words independently checked periodic.
- All256 actual canonical products onZ207, each with a literal nonzero-step
  monochromatic tuple; this bypasses the forbidden-pattern calculation.
- All5038848 normalized mixed-column27-bit words, the complete54-word
  step-two survivor list, and its complete step-three rejection.
- Full scalar/big-integer agreement at quotient7,11,13 (64,1024,4096
  normalized words), and all108 small mixed-column assignment tables.
- Positive cyclic products at21 and69: all420 and4692 nonzero-step tuples,
  including repeated residues.
- Four rejected corrupted result objects: omitted survivor, wrong coverage,
  false final survivor, and missing forbidden pattern.
- Exact costs of all54 intermediate27-factor seeds, plus a direct count
  of all385020 nonzero cyclic tuples for the least-cost representative.

The first rejecting-step counts independently agree in both implementations:
u23 as listed in the proof; v9 `[217,36,3]`; mixed v27
`[5026914,11880,54]`. Their sums account for each whole normalized domain.
`probe_seeds.py` finds27 seeds at ordered cost3308 and27 at7692. The selected
invalid word has SHA256
`5a535419623d8a7c4fa2017fb29dbb2fbe2d37db7af090f7a325563129194caa`
(including its trailing newline). It is not a certificate of AP freedom.

The independent programs share the author and the stated mathematical
definitions. They use different representations and enumeration operations;
this does not constitute independent peer review or formalization. The
written order-three reduction, affine normalization and subgroup transfer
remain necessary proof steps. Failure, timeout, memory termination or
incomplete output is a failed check and cannot establish nonexistence.

Only compact source and expected summaries are published. Binaries, logs,
native outputs, expanded truth tables, private graph transcripts and
experimental search checkpoints stay in the chosen scratch directory.
