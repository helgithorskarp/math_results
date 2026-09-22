# Spectral sets with two points on every prime-coordinate level

For a prime `p` coprime to `n`, let
`A = {(a_j,j),(b_j,j): j in Z_p}` in `Z_n x Z_p`, with distinct points
on each level. We prove the following exact alternative:

**`A` is spectral if and only if it has a common binary character, or its
injective projection to `Z_n` is spectral.**

The first condition means that `n` is even and all the differences
`b_j-a_j mod n` have a common binary valuation `t < v_2(n)`. It gives the
explicit spectrum `{0,n/2^(t+1)} x Z_p` and the common tiling complement
`{(x,0): x mod 2^(t+1) < 2^t}`. Every spectrum using multiple prime-coordinate
levels forces this condition; one-level spectra descend to the base group.

In `Z_2310`, the published four-prime Fuglede theorem excludes the base
alternative. Thus a set with two points in each residue class modulo 11 is
spectral **exactly when it has one point in each residue class modulo 22**.
It then tiles by `22 Z_2310` and has spectrum `105 Z_2310`.
This closes the balanced two-point-level family, including sets with no full
prime fiber. It does not classify arbitrary 22-point spectral sets or settle
Fuglede's conjecture for `Z_2310`.

[PROOF.md](PROOF.md) gives the universal argument and a six-point
counterexample showing why coprimality is essential. The key step compares
the two possible matchings of two pairs of roots of unity, then reduces the
orthogonality equation in characteristic `p`.
[SOURCES.md](SOURCES.md) distinguishes the proposed family theorem from
classical Fourier machinery, the published large-prime common-spectrum
result, and the earlier full-fiber result. Novelty is search-relative and
independent mathematical review remains pending.

## Reproduce

Python 3.11 or newer, standard library only; run from this directory:

```sh
python3 verify.py --check
sha256sum -c SHA256SUMS
```

Expected terminal output from the first command:

```text
PASS: exact spectra, tilings, pairing equations, boundary, and expected output
```

To print the complete compact evidence, run `python3 verify.py`.
It must equal [expected.json](expected.json). The verifier raises explicit
exceptions, so Python optimization does not disable its checks.

The audit exhausts 31,297 balanced sets over eight declared small groups;
5,801 are spectral. Spectra are found by exact character-zero clique search
without using the claimed criterion. Ramanujan traces independently verify
the found and canonical spectra. It also checks 29,649 weighted-pairing
equations by both cyclotomic remainders and traces (200 vanish), three larger
explicit spectral/tiling fixtures, the noncoprime counterexample, six malformed
inputs, and missing-frequency/missing-translate controls.

These computations corroborate the proof and expose scope errors. They do
not constitute an exhaustive search at order 2310, a formalization, or an
independent review. The base-descent alternative is proved in prose; the
small-case audits all have an independently checked empty base alternative.
No large artifacts or external computational inputs are needed.
