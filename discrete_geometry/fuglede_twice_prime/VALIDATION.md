# Validation record

Run on 2026-09-22 with Python 3.11.2, standard library, Linux x86-64.

- The definition-level search tested **145,999** subsets containing zero in
  eight declared groups, including **133,305 unbalanced** subsets.
- It found **1,734 spectral subsets**, all agreeing with the criterion and
  the separate exact counting formula. One found spectrum per positive set
  was verified by Ramanujan traces; the explicit spectrum and tiling were
  checked too. This is not a catalogue of every spectrum of each set.
- Base exclusions were tested independently by complete normalized subset
  searches at sizes `p` and `2p` for every small parameter pair.
- Both paired-extraction branches were tested at `p=3,5,7,11`: eight exact
  phase-vector fixtures. They intentionally test the vector algebra in
  noncoprime ambient moduli; they do not purport to realize the mixed profile
  in a coprime spectral pair.
- The weighted two-matching identity was checked in **14,080** equations,
  with **164** zero cases, by cyclotomic reduction and independently by
  Ramanujan traces. A noncoprime failure control was included.
- Profile partitions and the negative principal-Gram witness were checked
  at six primes through 17. Three larger product-group examples, a direct
  cyclic order-2310 example, and an empty-level projection fixture were
  checked exactly. Six malformed inputs were rejected.
- Eight unit tests passed. They include an independent literal enumeration
  of every possible normalized spectrum through cyclic order eight to test
  the clique oracle, small root-sum cross-checks, and extraction mutations.

The positive-record digest is

```text
edd3413eb18ab89f87f2fbe005bd39322ff63b665b8a5e54a85ac00cbb765392
```

The full audit took 12.091 seconds and 62,552 KiB maximum resident memory in
the measured run. Runtime is environment-dependent and is not hashed output.
The universal claim rests on PROOF.md, not the finite cutoff. No solver,
floating-point comparison, external dataset, or formal proof assistant is
part of the trust boundary. The literature assessment in SOURCES.md is a
separate reading, not a machine verification of the external preprints.
