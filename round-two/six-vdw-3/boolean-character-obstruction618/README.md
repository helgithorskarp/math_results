# Nine-column obstruction for arbitrary Boolean rules on three characters

six-vdw-3, researcher, 2026-10-02. This is a computer-assisted structural
lemma in the **two-color/seven-term** van der Waerden family.

Take any Boolean function of three affine quadratic-character bits over
F103 and add any six-row phase. Keep **all original roots free**, including
roots of inputs the function ignores. Any AP7-free coloring agreeing with
this background outside its free roots and arbitrarily edited nonroot
columns needs **at least nine edited nonroot columns**. Values in an
edited column may depend arbitrarily on the integer position. The result
applies to cyclic618 sequences with nonzero step, or to [1,N] for N>=2466.

The exact root-count-preserving cover has2176 parameter classes:
2168 with three original roots, six with two, and two with one. An
independent square-set/ordered-root-pair checker covers all12938 raw
normalized parameter states and literally checks116442 transported APs.
The ordinary normalization, Burnside, phase and interval bridges are in
[PROOF.md](PROOF.md); implementation controls are in
[VALIDATION.md](VALIDATION.md).

This broadens the uniform nine-obstruction part of the
[majority lemma](../majority-character-orbits618/PROOF.md). The previously
proved stronger affine16 and repeated-root-majority15/16 remain special
results. Their numerical bounds are not premises of this full Boolean
certificate. The family is broader than affine characters, character
products and majority, but the physical-coloring equivalence count is
not claimed. There is no3704 coloring, repair optimum, sufficient
nine-edit construction, numerical W bound improvement or priority claim.

Use CPython3.11+ and the standard library only (measured with3.11.2).
From the repository root, choose a new private work directory:

```sh
python3 round-two/six-vdw-3/boolean-character-obstruction618/reproduce.py \
  --work /tmp/boolean618-reproduction
```

The wrapper verifies all nine source/expected-file pins, regenerates
seventeen128-case batches per mode, runs cover/controls and nine
256-case transport checks, then independently checks/merges the complete
case range. Normal and `-O` modes compare **whole CSV bytes, every entire
stage record and the entire expected final record**. Children are serial,
numerical threads are one and
every child has a fixed20-second guard. A timeout or failure gives an
incomplete record; it does not prove an exclusion.

The regenerable155886-byte full CSV is deliberately kept in private
work, with no external input or published large dataset. Its SHA256 is
`e7ecddbc9d917d193dafe60472e7a2fe16c8d30ac27beddd3c72e79e85045e28`.
The compact full checker record is [expected.json](expected.json), SHA256
`bd004412d40ef466aa6fc180fc1c18698916b67bbb18a89ec3b23e13f5ecd56c`.

For checking the parameter cover and representative APs of an already
regenerated full table (one stage, not the whole replay):

```sh
python3 round-two/six-vdw-3/boolean-character-obstruction618/check.py \
  --stage cover \
  --certificate /tmp/boolean618-reproduction/normal.csv \
  --out /tmp/boolean618-check.json
```

The template uses F103 and period618 as a search restriction. Monroe's
published length7/two-color seed uses prime617; the two fields are distinct.
Monroe writes length first, W(7,2), while this campaign uses color first,
W(2,7). Both refer to two colors/seven terms. See the primary references
and the precise mathematical scope in the proof.

The shorter2466 lift credits the separately published
[majority audit9772](../../six-reviewer-4/majority-orbit-audit/PROOF.md).
Its argument is rederived here for the full Boolean family, without
transferring the earlier audit's verdict.
