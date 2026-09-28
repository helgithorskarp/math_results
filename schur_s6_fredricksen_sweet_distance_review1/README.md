# Independent review of the 51-edit obstruction near S(6)

This directory audits the finite certificate in the sibling
[`schur_s6_fredricksen_sweet_distance`](../schur_s6_fredricksen_sweet_distance)
directory. The audited claim is conditional: if a valid six-colouring of
`[1,537]` exists, its restriction to `[1,536]` differs from the specified
Fredricksen--Sweet colouring in at least 51 positions, under every palette
labelling. It does **not** establish `S(6)=536` or exhibit a 537-colouring.

## Verdict and proof scope

**Accepted as an exact local certificate theorem.** For a putative colour `c`
of 537, each baseline-monochromatic complementary pair `(x,537-x)` of colour
`c` forces an edit. There are `64,43,55,38,32,35` such pairs. For selected
pairs, the certificate supplies, for both endpoints and every other colour,
a Schur triple whose remaining entries have that other baseline colour.
Changing either endpoint therefore forces a further edit in its support.
Within each `c` case the selected-pair supports are disjoint and contain no
baseline-`c` entry, so these extra edits are distinct from each other and from
the compulsory pair edits. The resulting six bounds are
`64,51,55,51,51,51`.

`audit.py` checks this logic independently of the original `check.py`. It
uses colour-class sets to test the baseline sum-free condition, reconstructs
all 537-complementary pairs, checks each of the 560 witness triples and its
endpoint/new-colour coverage, and checks support disjointness. The original
checker and the independent audit agree. The generator was also run with
`--trials 1000`; its output matched the committed certificate byte-for-byte.
The generator is not part of the proof.

The 2000 paper prints the 536-colouring as 269 listed entries plus reflection
about 537, with the exceptional pair `179,358` split. `compare_paper.py`
checks that this construction matches all 536 positions of the committed
baseline. Six compressed first lines are transcribed from the paper because
the PDF's compact font merges their digits in text extraction; the remaining
lines are parsed from the PDF. This attribution check has a small manual
transcription boundary. The theorem itself needs only the checked baseline.

## Reproduce

Run from this directory with CPython 3.11 or later:

```sh
python3 audit.py
```

Expected first line:

```text
PASS independent_audit pair_counts=64,43,55,38,32,35 selected_counts=0,8,0,13,19,16 bounds=64,51,55,51,51,51 witnesses=560
```

The audit also prints these SHA-256 digests:

```text
baseline_sha256=2fdf85110de782426dd5deccfa7244f182441fda9870db64ba8e4eea7e3d600d
certificate_sha256=b9c28cde217a6b4d06f672d0f389c1c9fa9e7544897cf4eb392fad3985edaa4f
```

Optional paper attribution check, with `uv`, `pypdf==6.19.0`, and
`fonttools==4.66.0`:

```sh
curl -LfsS https://www.combinatorics.org/ojs/index.php/eljc/article/download/v7i1r32/pdf -o /tmp/fredricksen-sweet-2000.pdf
uv run --no-project --with pypdf==6.19.0 --with fonttools==4.66.0 python compare_paper.py /tmp/fredricksen-sweet-2000.pdf
```

Expected output:

```text
PASS paper_baseline_match source_entries=269 colors=536 exceptional_pair=179,358
```

Primary source: H. Fredricksen and M. M. Sweet, *Symmetric Sum-Free Partitions
and Lower Bounds for Schur Numbers*, Electronic Journal of Combinatorics 7
(2000), R32, [paper](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32).
The July 2026 [shifted S-templates preprint](https://arxiv.org/abs/2607.15034)
still uses the lower bound `S(6)>=536`. Targeted searches found no prior
publication of this specific 51-edit local theorem; absence from search is
not a priority proof. The finite theorem appears ready for publication as a
scoped certificate result, while its direct impact on determining `S(6)` is
limited.

## Strengthening and improvement opportunities

1. Optimize the disjoint-support packing and the choice of witnesses jointly
   for each possible colour of 537. A larger minimum would strengthen the
   local obstruction, but still would not decide 537-colourability.
2. Certify corresponding distance bounds for other known 536-colourings and
   their symmetry or equivalence families. Turning such bounds into a global
   upper bound requires a separate completeness theorem that covers every
   putative 537-colouring's 536-prefix by certified neighbourhoods.
3. An unconditional `S(6)<=536` result would instead need a complete
   exclusion of all six-colourings of `[1,537]`, for example a reproducible
   exact search with an independently checked proof certificate. The present
   local certificate supplies no such global reduction.

## Trust boundary

The finite claim rests on the committed `baseline.txt`, `certificate.json`,
the pair-and-support counting argument, and Python's exact integer/set
operations. The audit does not prove that the 51 bound is optimal, classify
all 536-colourings, or establish the existence or nonexistence of a
537-colouring. No SAT solver result is used.
