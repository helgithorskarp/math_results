# Full triangle-packing rounding with bounded neighborhood diversity

For any graph on `n>=3` vertices with a partition into at most `d` twin
classes, this contribution proves

```text
nu* - nu <= [10^10 d log(400n)]^(1/7) n^(13/7).
```

Each class may be a clique or an independent set; between two classes all
edges or no edges occur. The fractional optimum includes **all** graph
triangles. The estimate follows from twin-class averaging and a fully
quantified weighted nibble. The [main proof](PROOF.md) and
[probabilistic rounding proof](NIBBLE.md) include the constants and
dependent-survival calculations.

Combined with the accepted [finite fractional Tuza gap](../tuza_dense_chordal_gap/PROOF.md),
this gives an unconditional numerical cutoff for every fixed number `r`
of independent-neighborhood types in a split graph. Define

```text
A=8r+11, d=2^r+r, C=400(r+1),
B=10^10 d (64A)^7 (r+1)^13,
K_r=max(16(r+1), 4B bit_length(4BC)).
```

For clique order `k>=K_r`,

```text
2nu - tau >= k^2/[16(8r+11)] > 0.
```

All neighborhood overlaps and arbitrary original multiplicities are
allowed. There is no spoke-saturation hypothesis or dependence on the
refuted centered-cover estimate. For `r=3`, the fully evaluated cutoff is

```text
K_3=1286735885062665252072167833600000000000000000.
```

This replaces an unspecified asymptotic cutoff by an explicit integer.
Its size makes direct exhaustive verification below it impractical.
The all-order three-type problem remains unresolved. The exponent and
constants are deliberately conservative and are not claimed optimal.

The proof is complete at the author level, unformalized, and awaiting
independent review. The nibble and LP-rounding framework are classical;
see [sources and novelty limits](SOURCES.md).

## Reproduce the finite audit

With Python 3.11.2 or compatible Python 3, from this directory:

```sh
python3 check.py > /tmp/full-rounding-audit.json
cmp /tmp/full-rounding-audit.json AUDIT.json
sha256sum -c SHA256SUMS
```

[check.py](check.py) uses only exact integers and rational arithmetic.
It enumerates all 2,112 outcomes of twelve one-round fixtures, verifies
dependent survival and objective identities, tests 75,960 coordinate
toggles over 7,933 conditional states, compares orbit averaging with
720 explicit class permutations, checks the parameter and cutoff
arithmetic, and rejects five malformed constructions. Expected output
is [AUDIT.json](AUDIT.json); environment and runtime are in [RUN.json](RUN.json).

These are finite checks of the proof's interfaces, not a computational
proof of concentration or of the universal theorem. In particular, no
process is run at order `K_r`. The six fixtures include the Fano
hypergraph, whose large fractional weights fail the lemma's hypothesis;
its one-round identities are still valid. Hashes serialize the outcome
records exactly as specified in the visible checker. No solver, random
simulation, external dataset, or bulk certificate is required.
