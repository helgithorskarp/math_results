# Nonzero centered cubic moment at 71 points

Every 71-point line-free subset \(S\subseteq\mathbb F_5^3\) has
\[
 \sum_{x\in S}\bigl(v\cdot(x-\mu)\bigr)^3\not\equiv0,
 \qquad \mu=\sum_{x\in S}x.
\]
At least 15 projective directions therefore have nonzero cubic moment.
This is an affine-invariant necessary condition; the exact maximum
remains unresolved between 70 and 71.

[PROOF.md](PROOF.md) gives a self-contained computer-assisted proof.
Seven quadratic normal forms and complete quartic enumeration leave
1,681 candidates in 29 verified subgroup orbits. All 37 barycenter
membership cases have small integer Farkas contradictions.
The proof uses global moments and point/line incidence, with no
assumption of affine symmetry.

## Reproduce

Requirements: Python 3.11 or later with its standard library and a C++20
compiler. From the repository root:

```sh
python3 affine_line_free_f5_3/nonzero_cubic_moment71/verify.py
python3 -O affine_line_free_f5_3/nonzero_cubic_moment71/verify.py
```

Output must agree with [EXPECTED.json](EXPECTED.json) and report
`NONZERO_CUBIC_MOMENT71_VERIFIED`, including:

* all 15,625 symmetric matrices normalized by checked basis changes;
* 100,442,349 quartic information words tested in total;
* 53,765 locally allowed quartics, reduced to 1,681 candidates;
* 29 subgroup orbits and all 37 exact certificates;
* 4,180 integer column inequalities checked, with no unexcluded cases.

The largest multiplier has absolute value 155. The certificate file is
about 15 KB, with SHA-256
`98c5f9fb805ce89aeef65798473f1055bbf0a6e9443abb3ba13bb218431178f8`.
Temporary executables are built outside the repository. Raw catalogues,
solver output, and binaries are not published.

For a complete sanitizer replay:

```sh
python3 affine_line_free_f5_3/nonzero_cubic_moment71/verify.py \
  --cxxflags='-O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer -no-pie'
```

Verification uses no solver. Optional rediscovery requires
[requirements-discovery.txt](requirements-discovery.txt):

```sh
python3 affine_line_free_f5_3/nonzero_cubic_moment71/discover.py \
  --out /tmp/rediscovered-cubic-certificates.json
python3 affine_line_free_f5_3/nonzero_cubic_moment71/verify.py \
  --certificates /tmp/rediscovered-cubic-certificates.json \
  --expected /tmp/rediscovered-cubic-summary.json --write-expected
```

The second command checks every proof obligation before writing the
new summary. Different valid certificates may have different hashes.
The discovery script also checks each rationally reconstructed
certificate with exact integers before saving it.

See [VALIDATION.md](VALIDATION.md) for the author audit and
[SOURCES.md](SOURCES.md) for provenance and the dependency boundary.
Independent acceptance of this new theorem is not claimed.
