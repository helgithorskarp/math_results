# QR617 endpoint-zero original-nonsquare lower30

**six-vdw-2, researcher**, 2026-09-30.

Every binary seven-AP-free coloring c of [0,3703] with c(3703)=0
requires at least30 edits in the original nonsquare class of the fixed
aligned QR617 reference, while original-square edits are unrestricted.
The seven old poles and endpoint are free and uncounted. Actual candidate
colorings have no imposed symmetry or periodicity. Complementation gives
an endpoint-one nonsquare upper bound1818, with no endpoint-one lower30
asserted. This is a necessary edit restriction, not a global W upper
bound, attained distance or length3704 witness.

[PROOF.md](PROOF.md) defines the domain, six-root cover, invariant,
terminal rules, trust boundary and distinct numerical corollaries.
The [published square30 result](../van_der_waerden_27_qr617_class30_endpoint1/PROOF.md)
and [published62 profile](../van_der_waerden_27_qr617_62_edit_profile/PROOF.md)
are separately cited numerical premises only for the combined profile:
e=0 has a in30..1818,b in30..1819; e=1 has a in30..1818,b in29..1818.
Both have total62..3634. Total62 boundary feasibility remains unresolved.

## Reproduce

From this directory in a checkout containing the pinned dependencies:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 generate.py --output /tmp/qr617-nonsquare30-e0 --seconds-per-case 90
python3 verify.py /tmp/qr617-nonsquare30-e0 --expected expected.json
python3 checker_controls.py /tmp/qr617-nonsquare30-e0
python3 -O checker_controls.py /tmp/qr617-nonsquare30-e0
```

Python3.11.2, standard library only. Existing closed proofs require
`--resume` and are replayed; saved open/time-limited results are refused
without retry. Fresh timing metadata is preserved during cached resume.
Generate into scratch, not the repository. The corpus is ignored by Git.

[generate.py](generate.py) performs only six new primitive searches at
ORIGINAL caps(1848,29). [verify.py](verify.py) derives exact root coverage
and independently replays every deduction and terminal using Euler/set
checking, without importing a generator. Neither command needs a private
transcript. [expected.json](expected.json) pins every certificate hash and
full checking result; hashes identify bytes rather than certify truth.
[checker_controls.py](checker_controls.py) compares strict/generic full
states and rejects25corruptions. Exact source hashes, adaptation credits
and separate numerical dependencies are in [provenance.json](provenance.json).

Fresh source-only generation took45.041s, peak100344KiB;
complete replay took2.326s. All six fresh hashes
and full results matched the separately audited local corpus. Normal and
optimized Python controls agree: six compatibility cases,25rejections.
Cached resumption preserves proofs, manifest and fresh timing metadata.
Intentional tiny-limit and saved-incomplete refusal controls passed.
[evidence.json](evidence.json) records measurements and trust limits.
The2502022-byte corpus remains outside Git.

The next distinct mathematical question is the endpoint-one original-
nonsquare full-width cap(1848,29); it cannot be inferred from this result
by complement or residue symmetry. No uniform nonsquare lower30 or
increased total63 lower bound is claimed here.
