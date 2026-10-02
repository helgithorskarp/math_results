# Orbit-16 exclusion in the H3 regular period-620 construction family

Author: **six-vdw-1, researcher**.

Every H3={1,5,25}-invariant, AP7-free regular cyclic core modulo 620 avoids
the 160-member affine class of phase row 16 on all ten field cosets.
This reduces the 580 locally admissible antipodal rows to 420. The other
rows are arbitrary; this proof assumes no phase-power law or affine-row
membership. See [PROOF.md](PROOF.md) for the precise modular definition,
complete reduction, strict certificate and scope.

This is a necessary construction restriction. It supplies neither a
3704-point coloring nor a change in W(2,7).

## Reproduction

The mathematical code uses Python standard library only. Recorded interpreter:
Python 3.12.14. External proposal tools are CaDiCaL 1.9.5 and drat-trim;
they are untrusted producers. The public strict kernel and full definition
auditor make the certificate checkable without trusting their verdicts.
Generated CNFs, complete traces, controls and logs stay in a fresh private
output directory; none is committed.

Supply absolute paths to the two executables and run from this directory:

```bash
python3 -B reproduce.py --work /tmp/h3-620-fresh \
  --solver /absolute/path/to/cadical --converter /absolute/path/to/drat-trim
```

The command verifies SOURCE_PINS.json before executing mathematical helper
code, rebuilds the entire model and fixed-phase census, runs definition,
physical controls and normalization in normal and -O modes, then freezes
the audited inputs. It makes one fresh native proposal, converts its trace,
strictly replays it in both modes, and runs damaged-proof controls. Whole
mathematical result objects must equal EXPECTED.json. It preserves every
stage receipt in the output directory and refuses an existing directory.
The optional `--barrier-root PATH` checks the campaign's stop/handover
markers before each child; it changes no controls.

All children are serial with numerical threads fixed at one. Each child
has a 35-second process-group guard. The native proposal has a requested
49900-conflict limit, hard actual ceiling 50000, native 30-second and
subprocess 32-second guards. Conversion uses `-t 20`. The total serial
reproduction can exceed 35 seconds; no individual guard is raised.
UNKNOWN, timeout, interrupted checking or a missing proof causes failure,
and establishes no exclusion. Existing incomplete older models are not
inputs or premises and are never retried by this command.

Final expected status:

    COMPLETE_H3_ANY_COSET_ORBIT16_EXCLUSION_REPRODUCED

The canonical model has 100 variables, 43250 clauses and 90 original free
bits before AP constraints. Per strict mode: 22391 additions, 65609
deletions, 256730 positive propagation hints and an empty-clause derivation.
Normalization covers 4800 CRT maps, all ten cosets and 2880000 regular
point identities. The full proof hash is

    8c50f2ea6d53a5bd57c1f5fca206114b045d83dd46fbe35894db0bf543dd7bd2

EXPECTED.json pins the whole outputs and canonical CNF/model/native trace
hashes. Exact canonical trace comparison reproduces this specific evidence;
a different valid strict proof could prove the same CNF but would not pass
this unchanged fixture. Native-version parity alone does not guarantee
bit-identical proofs across different builds.

## External source and trust

Recorded CaDiCaL source: https://github.com/arminbiere/cadical , commit
146207318796f094dcded87349a64f0c6927309e (version 1.9.5). Its tested binary
SHA256 is 2d3fb92d83b7b2f3b15fc19ab5c05e2ce65958724781c3763f73399e3e707802.

Converter source:
https://raw.githubusercontent.com/marijnheule/drat-trim/2e3b2dc0ecf938addbd779d42877b6ed69d9a985/drat-trim.c

Its source SHA256 is
d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee.
The tested build used `cc -O2 -std=c99 -D_GNU_SOURCE drat-trim.c -o drat-trim`;
binary SHA256 f0023a4a6b2862dcf8324d6c259a3bd4e050fd22152b0b8a2a8af029e0eba50f.
No converter is downloaded or built by reproduce.py.

strict_rup.py is the byte-identical credited copy of
https://raw.githubusercontent.com/helgithorskarp/math_results/223f0eaa45d24ff924e10edaa1e327fbf8a7259f/van_der_waerden_618_binary_fibers/check_rup_lrat.py
with SHA256 55543f905d42aaf0955906f97a8484ec8522a182512b1d2e8fe132bb45cb545c.
It was not newly authored for this contribution.

Trust remains in the ordinary CNF-equivalence/affine-transport arguments,
the independently implemented physical auditor and strict RUP algorithm,
their exact execution and the pinned source. Same-author separate algorithms
do not imply an external reviewer verdict or formalization. See
[VALIDATION.md](VALIDATION.md) for the finite coverage and recorded guards.
