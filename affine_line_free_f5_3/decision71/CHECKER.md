# Proof-checker configuration and controls

The proof format is standard binary DRAT. All traces can be checked with
the unmodified official [DRAT-trim](https://github.com/marijnheule/drat-trim)
at source commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.
The upstream `drat-trim.c` SHA256 is
`d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee`.

The production run uses two recorded checker configurations. Early cases
used the stock build. Subsequent cases use the two-line
[patch](small-initial-allocation.patch):

1. Set the initial allocation and hash-bucket constant `BIGINIT` to
   65,536 instead of 1,000,000.
2. Repeat database growth until the next complete clause fits, replacing
   the single `if` growth guard by `while`.

The first change removes substantial repeated allocation cost for these
small 125-variable inputs. The second ensures that lowering the initial
capacity cannot leave a large incoming clause beyond the grown buffer.
The patch does not change the proof rules, deletion matching, propagation,
or success condition. Hash collisions are resolved by comparing clause
literals; the bucket count does not identify clauses mathematically.

The modified source SHA256 is
`9c8dfa3e02fe7ab6102ee799165f04188d6738c1dbe5ba249b1cb86a1dd2b288`.
To build it locally from the pinned upstream source:

```sh
python3 build_checker.py --source /path/to/drat-trim/drat-trim.c \
  --out /tmp/decision71-checker
```

This checks the upstream source hash, applies exactly the two changes,
checks the modified source hash, and compiles with `gcc -std=gnu99 -O2`.
It records the actual binary hash. Binary hashes can vary with the
compiler and embedded source path; the source hashes are the portable
provenance check. No checker binary or third-party source dump is
committed to this package.

Before production use, the modified checker rechecked 122 traces already
accepted by the stock checker: 120 stratified direct/strengthened lift
proofs and two larger grouped-formula proofs. Both configurations rejected
an empty proof, a false empty-clause assertion, and a real UNSAT trace
applied to a known satisfiable 70-point formula. The public pipeline
controls additionally regenerate fourteen direct traces covering type and
process boundaries and exercise the same invalid-proof controls.

AddressSanitizer and UndefinedBehaviorSanitizer checker builds passed
three representative controls, including one of the larger grouped
formulas. Leak detection was disabled in that checker experiment because
the upstream standalone program leaves small allocations for process
exit; invalid-memory-access and undefined-behavior checks remained
enabled. This limitation does not apply to the complete C++ enumeration
sanitizer run.

The stock production binary SHA256 was
`9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`;
the modified production binary SHA256 was
`4cb27fe1b1f45ea9441f5dbe271f2b279305621c3019195b7ea4060631c18eb2`.
Every original case record preserves the actual checker identity. The
final evidence manifest reports the number checked by each configuration;
it does not describe the entire production corpus as stock-checked.

The remaining proof-checking trust is ordinary DRAT-trim execution and
the documented patch. This is independent of the SAT solver, but it is
not a formally verified proof checker. A reader may replay every trace
with the stock checker to avoid trusting the allocation patch.
Use [recheck.py](recheck.py) with a new output directory to keep the
original logs and checker identities intact; see [CORPUS.md](CORPUS.md).

After the first full range completed, its hardest production case, index
20,750, also passed a fresh stock-checker replay. Its 84,295-conflict
trace has 3,482,287 bytes. This supplemental control is recorded in
`VALIDATION.json`; it does not change the original per-case checker
identities or claim that the entire corpus was replayed with stock code.
