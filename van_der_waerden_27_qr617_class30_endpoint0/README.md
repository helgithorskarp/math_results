# Fixed QR617: endpoint zero requires 30 square-class edits

**six-vdw-2, researcher**, 2026-09-30.

For any binary seven-AP-free coloring c of `[0,3703]`, compare the
nonpole prefix with q=0 on nonzero squares modulo617 and q=1 on
nonsquares. If `c(3703)=0`, at least **30 original-square positions**
must change, with the other original class entirely unrestricted.
Complementation gives `c(3703)=1 => a<=1818` for the same square-class
edit count a. It does not give an endpoint-one lower30 bound.

The actual coloring has no imposed symmetry or periodicity. All seven
prefix poles and the endpoint remain free and uncounted. This is a
necessary edit condition relative to a fixed reference; no length3704
witness, global W upper bound, exact W value or attained repair minimum
is claimed. Translation by one gives the named `[1,3704]` target.

The [proof](PROOF.md) covers exactly six endpoint-zero roots at caps
`(29,1848)`. Six complete mandatory-AP splits have28 children. Every
child inherits its checked parent state and closes by exact replay.
No previous numerical bound is used in those branch proofs. The
[earlier62 profile](../van_der_waerden_27_qr617_62_edit_profile/PROOF.md)
is a separate premise for the combined endpoint-specific corollary.

Use Python3.11.2 and its standard library. Keep the two computational
dependency directories in their original sibling locations in this
repository; exact commits and hashes are in [provenance.json](provenance.json).
With numerical threads one, run from this directory:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 generate.py --output build --seconds-per-case 90
python3 verify.py build --expected expected.json
python3 checker_controls.py build --output build/controls.json
python3 -O checker_controls.py build --output build/controls-optimized.json
```

[generate.py](generate.py) uses the published square/bit-mask kernel.
[verify.py](verify.py) imports the unchanged Euler/set tree checker,
never a generator. [checker_controls.py](checker_controls.py) checks
primitive compatibility, Boolean cover semantics, inherited states,
complete root coverage and malformed certificates, with explicit guards
that remain active under `python3 -O`.

The roughly14MB proof corpus is generated locally and excluded from Git.
[expected.json](expected.json) records every checked file hash and its
full checking summary. Hash agreement identifies previously checked
bytes; the proof authority is exact replay and the written argument.
[evidence.json](evidence.json) records fresh generation, entry-level
comparison, controls, resumption and resource observations. Generation
requires no private certificate input.

The generator preserves partial proofs. `--resume` replays cached closed
trees and can continue unsearched child placeholders. It refuses saved
timeouts and previously searched stalled children. A timeout, open child,
missing root or failed search proves no exclusion. A separate fresh
directory is required to change the search design; do not increase limits
or silently retry an exhausted case.

Exact Python semantics, the inspected checker and the written AP,
invariant, covering and complement arguments remain the trust boundary.
The generator and independent checker share an author; no external review
or proof-assistant formalization is asserted. The combined corollary also
trusts the explicitly cited62 theorem, which this command does not reprove.
