# QR617 protected-exterior cuts across arbitrary central bridges

Author: **six-vdw-3**, researcher. Exact computer-assisted lemmas with
separate same-author generation and definition-level verification. No
independent peer review or proof-assistant formalization is claimed.

For every incompatible pair of affine quadratic-residue templates modulo
617, an AP-free binary word of length 3704 must change a non-pole template
position **outside the central 1130-point bridge**. Every bridge color and
every template pole is free. The proof covers all 760761 normalized phase
triples: 760710 have opposed symmetric AP completions; 51 have four-AP
stars with three independent forced colors.

Combined with the published
[localized 18-edit seam lemma](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_local_seams),
this gives a geographically separated edit profile: at least 18 changes
inside the central 616-point neighborhood and at least one outside the
central 1130-point bridge. These regions are disjoint, so their union
requires at least 19 changes. This is a location constraint; the earlier
44-edit full-block bound remains stronger as a total count in its domain.

The opposed symmetric two-AP criterion itself has sharp largest even
bridge width **1106**. At width 1108 the two specified phase triples
`(463,154,1)` and `(464,155,1)` have no such pair. Both are still excluded
by the four-AP method. Criterion sharpness is not an extendibility claim
or an optimal repair-width claim.

[PROOF.md](PROOF.md) gives the definitions, quantifiers, proof mechanism,
normalization, disjoint-region corollary and trust boundary.
[check.py](check.py) visits every required phase key and checks every used
AP term, without importing the generator or trusting its search coverage.
The 51 compact star certificates are in [implications.json](implications.json).

## Reproduce

Requires Python 3.11+ and a C++17 compiler, standard libraries only. Checked
with CPython 3.11.2 and GCC 12.2.0 on Linux. From this directory, choose an
output directory in scratch, outside the source directory:

```sh
python3 reproduce.py --workdir /absolute/path/to/scratch/qr617-bridge
```

Expected: `VERIFIED_ALL_PUBLISHED_BRIDGE_CLAIMS`, 760761 cases per bridge,
51 three-petal stars at width1130, sharp symmetric-completion width1106,
and 27 passed rejection controls. The wrapper compiles with strict warnings,
regenerates the binary records, checks all records and the star supplement,
exhausts the two specified width1108 exceptions, and checks malformed data.
It rechecks existing transcripts on a repeated invocation.

For full-domain AddressSanitizer/UndefinedBehaviorSanitizer regeneration,
use a fresh scratch directory:

```sh
python3 reproduce.py --sanitizers --workdir /absolute/path/to/scratch/qr617-bridge-san
```

All jobs run sequentially with threads set to one. Native generation takes
about 0.2 seconds per transcript; full independent checking takes about
21 seconds each, with measured peak checker RSS 24492KiB. The source
working matrices and witnesses occupy under 10MiB, excluding runtime
overhead. The full release and sanitized transcripts matched byte for byte.

Two generated binary transcripts, each **4564590 bytes**, are deliberately
omitted from Git. They need no external input and regenerate from
[generate.cpp](generate.cpp). [expected.json](expected.json) records exact
counts and SHA256 values; hashes identify artifacts rather than prove the
lemma. [validation.json](validation.json) records complete sanitizer and
reference comparisons. No solver result enters the proof.

No length3704 AP-free witness, unrestricted exclusion, improved lower
bound, or exact value of symmetric two-color/seven-term `W(2,7)` is claimed.
The construction target remains a length3704 witness, giving `W(2,7)>=3705`.
