# Stable transitivity on the degree-two `G8` box

This directory certifies the following finite theorem.  Let `G8` be the
canonical 20-arc partial tournament in `THEOREM.md`.  If `W` is any
2-tournament that has multiplicity two on every arc of `G8`, then

```text
m(W) = 3.
```

Equivalently, `m(T1+T2)=3` for every two (not necessarily equal) tournament
completions `T1,T2` of `G8`.  This fills the whole degree-two mixture box,
whereas the earlier ray result only supplies its 256 diagonal corners.

The correctness boundary is solver-free.  It consists of the explicit
`pair_profiles.txt` certificate and `verify.py`, which uses only Python's
standard library and integer arithmetic.  Run:

```bash
python3 verify.py
python3 -m unittest -v test_verify.py
sha256sum -c SHA256SUMS
```

The first command checks all 6,561 ternary targets, 183,708 exact pair-count
equations, and the exhaustive 40,320-order lower bound.  Its output must
match `EXPECTED_OUTPUT.txt`.

`generate_profiles.py` is a deterministic, solver-free reproduction of the
certificate from the 256 checked corner profiles.  It explores profiles by
adjacent swaps across the eight unspecified pairs, retains at most 100
profiles per target, and takes about half a minute on the discovery host:

```bash
python3 generate_profiles.py --output generated_pair_profiles.txt
cmp pair_profiles.txt generated_pair_profiles.txt
```

The generator is not trusted by the theorem: `verify.py` checks the emitted
certificate independently from the definitions.
