# Completed validation

six-vdw-2, researcher; 2026-10-02. These are same-author checks using
separate algorithms, not an external reviewer verdict or formalization.

A fresh compact-source work directory regenerated all ten canonical CNFs,
reconstructed the entire field/counter clause multiset normally and with
-O, and strictly replayed all ten positive-only RUP refutations in both
modes. Untrusted local proof candidates were copied only after their
canonical CNF/proof digests matched the frozen fixture. Every candidate
was replayed again. This check did not repeat the stopped native UNKNOWN.
All model and proof bytes reproduced. Per mode:174147 additions and2968781
propagation hints. The compact-source check took47.040s,
child peak71756KiB.

The original complete fourteen-model audit took31.267s,
child peak72032KiB, and covered all j=4..10/b=0,1
before any native proposal. The native/conversion/strict sequence obtained
the ten j=6..10 refutations, then stopped on j=5/background0 UNKNOWN at
50000 conflicts. The other three cases were never proposed. This sequence
took76.101s, child peak69596KiB.
No endpoint or unrestricted exclusion follows from the incomplete search.

All sixteen semantic/source/proof damage controls were rejected, including
with repaired CNF metadata and with Python -O: missing either endpoint of
the forbidden-head cover, altered exact-seven counter units, a removed
semantic input clause, changed selected count, a changed helper rejected
before import, an empty clause without hints and an absent live hint.
Two valid toy positive-RUP refutations were accepted. Controls took
13.522s, child peak58616KiB.

Transfer DP and separate zero-run double counting independently returned
178983 rooted phase inputs per background, versus2345553 before the new
rule. Sixty tiny count controls,984 admitted literal deficit words and152
binary first-next controls passed in both modes. These counts concern
phase profiles, not field colorings, rotation orbits or witnesses.

All jobs were serial with one solver/BLAS/OpenMP thread. Native limits
remained50000 conflicts/30s; conversion25 internal/30 external; strict
replay30s per mode; definition audits55s per stage. One initial launch
failed before solver entry because its interpreter lacked python-sat;
it was preserved and the existing pinned solver environment was selected.
Neither that error nor UNKNOWN is a mathematical refutation.

The mathematical source and frozen fixture did not change after the
compact-source check. VERIFICATION.json and this completed validation
record were added afterward; final SHA256SUMS covers all compact files.
The earlier manifest digest and tested file digests remain in
VERIFICATION.json. Large generated certificates, models and logs remain
outside Git. The published endpoint10/34 band is unchanged; the new result
is the gap-two successor restriction and quantified phase-input reduction.
