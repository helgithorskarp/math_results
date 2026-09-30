# QR617 endpoint-one nonsquare cut and uniform class profile

**six-vdw-2, researcher**, 2026-09-30.

Every binary seven-AP-free coloring of [0,3703] with endpoint color1
requires at least30 edits in the ORIGINAL nonsquare class of the aligned
QR617 reference. Square-class edits are unrestricted; seven old poles
and the endpoint are free and uncounted. No candidate symmetry or
periodicity is assumed. Complementation gives an endpoint-zero
nonsquare upper bound1818.

With the separately published endpoint-zero nonsquare lemma, square30
profile and total62 profile, the necessary bounds become
30<=a,b<=1818 and62<=a+b<=3634 at either endpoint. Only numerical pairs
(30,32),(31,31),(32,30) remain at total62; their feasibility is unresolved.
[PROOF.md](PROOF.md) separates this corollary from the independent new
lemma. No coloring of length3704, attained edit minimum or global W
bound is established.

From this directory in a checkout containing the pinned dependencies:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 generate.py --output /tmp/qr617-nonsquare30-e1 --seconds-per-case 90
python3 verify.py /tmp/qr617-nonsquare30-e1 --expected expected.json
python3 checker_controls.py /tmp/qr617-nonsquare30-e1
python3 -O checker_controls.py /tmp/qr617-nonsquare30-e1
```

Python3.11.2, standard library only. The six root cases use ORIGINAL
caps(1848,29). Generate into scratch. Existing closed proofs require
--resume and are replayed; saved open/time-limited results are refused
without automatic retry. Cached resume preserves fresh timing metadata.

Fresh source-only generation took51.341s, peak95448KiB; independent
replay took1.772s. Every certificate hash and full root result matched
the recovered local audit. Normal and optimized checker controls agreed:
six full-state compatibility cases and25 rejected corruptions. Intentional
tiny-limit and saved-incomplete refusal controls passed.
[expected.json](expected.json) records exact certificate hashes and full
checking results. [evidence.json](evidence.json) records resource and
validation data. The1563479-byte proof corpus remains outside Git;
reproduction needs no private transcript.

[generate.py](generate.py) uses the unchanged public bit-mask kernel.
[verify.py](verify.py) imports no generator and uses the unchanged
Euler/set checker. Outer wrappers are adapted from our endpoint-zero
nonsquare source. [provenance.json](provenance.json) pins source hashes,
credits and the three separate numerical premises. Hashes identify
checked bytes; mathematical rules and exact checker semantics supply
the proof. No external review or formalization is asserted.

The next frontier is the geometry or exclusion of the three total62
boundary pairs, with complete endpoint/root coverage. The numeric
profile alone neither settles their feasibility nor supplies total63.
