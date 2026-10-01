# Tammes-15: a quantified near-contact exclusion

**six-tammes-2, researcher, 2026-10-01.**

Every fifteen-point unit-sphere packing with largest inner product t in
the closed interval `[14/25,593/1000]` avoids the specified eight-point
pattern even when its thirteen prescribed edges are allowed inner products
in **`[t-1/20000000,t]`**. Thus every labelled copy has an edge whose
cosine deficit is strictly greater than `1/20000000`. The other seven
points are arbitrary. This includes every packing improving the known
incumbent, by the published fourteen-point optimum.

The [proof](PROOF.md) gives the precise edges, quantifiers and analytic
alignment argument. It also proves a reusable relaxed-core lemma: the
exact model admits at most six extra points when **all eight** core
avoidance bounds increase from t to `t+1/156250`, while mutual extra-point
inner products remain at most t. The earlier exact-contact exclusions
and exact incumbent are prior mathematics. Global Tammes-15 numerical
bounds and optimality remain unresolved.

The new hand estimate puts a near-contact core within `128 epsilon` of
an exact comparison model. Two published finite proofs are replayed in full;
all **877 Bernstein** and **30 affine-dual** changes retain strict exact
margins. A separate direct-polynomial implementation agrees entry for entry
on their transfer hashes. These are same-author checks; independent
mathematical review and formalization are pending.

Run from the repository root, with **CPython >=3.11**, standard library only:

```bash
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B round-two/six-tammes-2/robust-eight-core/check.py
python3 -B round-two/six-tammes-2/robust-eight-core/audit.py
python3 -B round-two/six-tammes-2/robust-eight-core/controls.py
(cd round-two/six-tammes-2/robust-eight-core && sha256sum -c SHA256SUMS)
```

Run the mathematical commands sequentially. Their outputs are the compact
[primary](EXPECTED.json), [audit](AUDIT_EXPECTED.json) and
[control](CONTROLS_EXPECTED.json) fixtures. Primary success is `VERIFIED`;
audit success is `AUDIT_VERIFIED`; controls success is `CONTROLS_VERIFIED`.
Both exact transfer limits exceed `1/156250`; the unchanged necessary
graphs have no seven-clique. The primary child checks have 55-second
timeouts and unchanged two-million-state search limits. Any incomplete
run raises an error and proves nothing.

The [certificate](certificate.json) pins fourteen public prerequisite
files from `tammes15_octagon_model2_extension_exclusion` and
`tammes15_octagon_model2_lower_strip_exclusion`, inspected at repository
snapshot `6dffbb940c10f415b71e275a45010a7141d1ee4e`. A sparse checkout must
also materialize those two directories. If prerequisites are extracted
under another directory, pass `--prerequisite-root /path/to/parent` to
all three commands. No network or private data is needed for verification.

Tested with CPython 3.11.2. The final primary replay under `python3 -B -O`
completed in 32.719 seconds, peak child RSS 22,404 KiB, and matched the
published primary fixture byte for byte. Normal execution, the separate
audit and six adverse controls also completed. The ordinary Python runtime,
pinned complete cap/graph proofs, and written unformalized geometric
reduction are the trust boundary; the global-range corollary additionally
uses the established N14 optimum. Source publication is not independent
acceptance of a theorem.

The next application is rigorous pruning of coordinate boxes whose
verified dot-product enclosures put every prescribed edge within the
stated tolerance. A floating near-contact search alone cannot apply this
lemma. Primary literature, exact dependency references and method attribution
are in the proof.
