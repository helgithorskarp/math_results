# Fixed QR617: endpoint one requires 30 square-class edits

**six-vdw-2, researcher**, 2026-09-30.

Let c be a binary seven-AP-free coloring of `[0,3703]`. Compare its
nonpole prefix with q=0 on nonzero squares modulo617 and q=1 on
nonsquares, and let a,b count edits in the original square/nonsquare
classes. The new independent lemma is **c(3703)=1 implies a>=30**, with
b unrestricted. Complementation gives `c(3703)=0 implies a<=1818`.

With the separately published
[endpoint-zero lemma](../van_der_waerden_27_qr617_class30_endpoint0/PROOF.md),
this gives **30<=a<=1818 at either endpoint color**. With the separately
[published62 profile](../van_der_waerden_27_qr617_62_edit_profile/PROOF.md),
the combined necessary conditions also include `29<=b<=1819` and
`62<=a+b<=3634`. Those two prior numerical premises are labelled in
the output and are not rechecked by this command.

The actual coloring has no imposed symmetry or periodicity. All seven
old poles and the endpoint are free and uncounted. Translation by one
gives the named `[1,3704]` target. No length3704 witness, global W upper
bound, exact W value or attained repair minimum is established. No
original-nonsquare lower30 or total63 theorem is asserted.

The [proof](PROOF.md) excludes the exact full-width cap `(29,1848)` for
all six endpoint-one roots. All six close directly, with no additional
cover split. No previous numerical cut enters a new branch proof.
The generator requires only the pinned public sibling sources in this
repository, listed in [provenance.json](provenance.json).

Use Python3.11.2 and its standard library. From this directory:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 generate.py --output build --seconds-per-case 90
python3 verify.py build --expected expected.json
python3 checker_controls.py build --output build/controls.json
python3 -O checker_controls.py build --output build/controls-optimized.json
```

[generate.py](generate.py) uses the published square/bit-mask kernel.
[verify.py](verify.py) imports the unchanged Euler/set tree checker,
never a generator. [checker_controls.py](checker_controls.py) also
replays the strict singleton checker, compares full primitive states,
and rejects missing roots, swapped class budgets, unsupported hypotheses,
invalid APs, false terminals and incomplete proofs. Its explicit guards
remain active under optimized Python.

The approximately1.7MB generated corpus is excluded from Git.
[expected.json](expected.json) holds every checked hash and full root
checking result; hashes identify previously checked bytes and never
replace exact replay. [evidence.json](evidence.json) records fresh
generation, comparison, controls and bounded resource measurements.
The already published endpoint-zero searches are not repeated.

The generator preserves partial proofs and exits unsuccessfully if a
root stays open. `--resume` replays closed saved proofs and refuses open
or timed-out roots without retry. Fresh timing metadata is preserved
during cache-only resumption. A timeout, STALLED or unsuccessful search
proves no exclusion. Every case has a positive cap of at most90 seconds.

Exact Python semantics, inspected checking code and written AP/invariant,
root-cover and complement arguments remain the trust boundary. The
generator and independent checker share an author; no external review
or proof-assistant formalization is claimed. The conditional corollaries
additionally trust the explicitly cited earlier numerical theorems.
