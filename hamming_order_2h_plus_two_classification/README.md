# The order-`2h+2` Hamming-core boundary for `h >= 6`

This directory proves a rank-uniform classification of the next boundary after the sharp `2h+2` essential-dimension lower bound for Hamming `h`-cores.

Let

```text
H = K_(n1) square ... square K_(nd)
```

be any finite Hamming graph. A set `C` is an `h`-core if the induced graph `H[C]` has minimum degree at least `h`.

## The theorem

For every `h >= 6`, every Hamming `h`-core `C` of order `2h+2` has exactly one of the following canonical forms, distinguished by its maximum selected coordinate-line size `M`:

1. `M=2h+2`: one coordinate line;
2. `M=h+1`: the union of two vertex-disjoint `(h+1)`-point subsets of distinct coordinate lines (cross-edges are allowed);
3. `M=h+2`: the union of an `(h+2)`-point line subset and an `h`-point subset of a distinct line, with every point of the smaller set adjacent to the larger set.

All three forms are sufficient. The third is necessarily contained in a coordinate two-flat. The maximum-line qualifiers are essential for exclusivity: without them, the second and third descriptions can overlap under a different choice of supporting lines.

Consequently, a connected `C` of order `2h+2` that is not contained in a coordinate two-flat has exactly one normal form: two `(h+1)`-point lines in different directions, joined by one edge whose direction is different from both line directions. Its essential dimension is exactly three.

This genuinely three-dimensional form exists for every `h`, for example

```text
{(a,0,0): 0 <= a <= h} union {(0,b,1): 0 <= b <= h}.
```

The full classification's threshold is sharp: at `h=5`, the `4 x 3` grid has order 12 and minimum degree 5 but is not a union of two lines.

The complete human proof is in [PROOF.md](PROOF.md).

## Majority-C consequence

Set `h=s-1`. For `s>=7`, a connected legal minor-box part of order `2s` that uses all three minor coordinates is forced to be the unique-edge two-line form above. An extremal majority-C colouring may be assumed to have connected colour classes, because disconnected components can be recoloured separately. Thus the theorem reduces every three-coordinate repair at this second-carry boundary to one explicit orientation test.

## Reproduction

Requirements: CPython 3.11 or later; no third-party packages.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify.py --max-h 60 --profile-max-h 15 \
  | diff -u expected_stdout.txt -
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
sha256sum -c SHA256SUMS
```

The first command exhausts all capped directional profiles through `h=15`, checks the proof's symbolic inequalities and explicit sharp family through `h=60`, audits the canonicalization of the review's overlap witness, and enumerates all 88,074 disjoint pairs of nontrivial coordinate-line subsets in the four-dimensional ternary Hamming graph. The last line is `all exact checks passed`.

## Trust boundary

The corrected universal theorem rests on the written shell-incidence inequality, capped-majorization argument, divisibility contradiction, maximum-line split, and coordinate-line incidence lemma. An independent review accepted the cover and all consequences after identifying the missing maximum-line qualifiers in the original graph wording. The standard-library checker uses exact Python integers and rational numbers; it is finite corroboration and regression protection, not a proof for unbounded `h` or arbitrary host alphabets. There is no solver, floating point, randomness, network input, external data, or omitted certificate.

Literature and graph status are recorded in [SOURCES.md](SOURCES.md). Novelty is search-relative and is not a priority claim.
