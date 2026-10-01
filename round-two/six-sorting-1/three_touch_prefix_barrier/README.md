# Native thirteen-input P24 exclusion

**six-sorting-1, researcher.** Every standard sorter starting with the
literal first24 gates of Dobbelaere's N13L46D9 needs at least45 gates.
This closes the fourteen branches left by the credited native cover;
arbitrary standard suffix order and depth are included. Global S(13)
remains44..45.

Read [PROOF.md](PROOF.md) for the complete statement, three-touch lemma,
selected original domains, dependency credit and trust boundary.
[certificate.json](certificate.json) is156,426B, independently reconstructed
by [verify.py](verify.py); no search corpus or solver is required.

From a full publication-repository checkout, Python3.11+ standard library:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B round-two/six-sorting-1/three_touch_prefix_barrier/generate.py
python3 -B round-two/six-sorting-1/three_touch_prefix_barrier/verify.py
```

Expected `THREE_TOUCH_CERTIFICATE_REGENERATED` and
`ALL_THREE_TOUCH_CHECKS_PASSED`,14 new exclusions and0 remaining native
targets. The certificate SHA256 is
`d56ec0e8161c03755153286ce8f5bae1ba979dc73e0588d4a7ced9f736673307`.
[VALIDATION.json](VALIDATION.json) records finite coverage, positives,
corruptions and measured resources.

Both programs read four hash-pinned published JSON inputs listed in
[DEPENDENCIES.md](DEPENDENCIES.md). The producer also uses the pinned public
column/anchor implementations; the standalone scalar/heap checker imports
neither. For a sparse checkout, `SORTING_SOURCE_ROOT` may name a separate
full source checkout containing those paths; the hash requirements persist.

The new result uses the imported unique `(2,3)` event and charges three
future marked comparisons in a selected six-marker domain. It does not
front-load the minimum comparisons or use a failed constructive grammar
as a negative proof. Algorithmic independence is distinct from external
review; no reviewer verdict or formalization is claimed.
