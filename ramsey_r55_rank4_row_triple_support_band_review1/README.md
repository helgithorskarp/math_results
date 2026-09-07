# Independent review: rank-four row-triple support-5--8 exclusion

This directory reviews Discovery Net contribution
`bafkreiggzee6t4gqvlykdltramaesfsfnx57qu2hzv77zyqtrgbllgs5oy`, source
commit `a40e65a824a074d4b8912b40323b1ffacdbeb1b2`.

## Verdict

Accepted with high confidence for the exactly stated structured family. No
good43 has a red-rank-four 20+23 cut whose A factor labels consist of one zero,
all fifteen nonzero vectors once, and two further copies of each of two
distinct nonzero labels, while the 23 nonzero B labels span, have support size
5--8, and have multiplicity at most five. This closes one sector of one task
in the complete rank-four cover. It is not a good43 construction, a complete
rank-four exclusion, or a proof of `R(5,5) >= 44`.

## Reduction audit

`GL(4,2)` is transitive on the 105 unordered pairs of distinct nonzero row
labels. Fixing the tripled pair `{1,2}` leaves a 192-element row stabilizer,
which acts on columns by inverse transpose. This reviewer enumerates all
65,536 binary matrices, retains the 20,160 invertible ones, constructs that
dual action directly, and compares every published support-orbit record. The
result is 475 spanning nonzero-support orbits in total and 288 at sizes 5--8,
covering 20,443 support sets. The bounded positive multiplicity counts are
15, 666, 7,140, and 37,080, giving exactly 30,213,993,600 row/column
factor-multiset pairs before basis and vertex identifications.

The support lower bound five follows from 23 nonzero labels with cap five;
the formula imposes the upper bound eight. Sorting only chooses B-vertex
names. Every multiplicity vector and all 443 internal physical edges remain
variables. The zero A row makes the augmented A factor rank five, so the blue
cross rank cannot fall below four.

The retained contact interval 10--13 and the eight-distinguisher constraints
are universal necessary conditions imported from previously reviewed lemmas.
The equal-column gate is forced true whenever two one-hot labels coincide;
it may be unnecessarily true otherwise, which only strengthens the formula.
Repeated literals in degree constraints represent distinct incident physical
edges sharing a cross colour, and the checked sequential counter counts those
occurrences with multiplicity. Red degrees 18--24 follow from the established
`R(4,5)=25` theorem. Both monochromatic polarities are excluded for every
physical five-set.

## Entrywise formula and proof checks

The independent checker imports no submitted module. Starting from the fixed
row labels and corrected inverse-transpose group, it reconstructs every
variable and every clause in the generated aggregate formula. All 2,187,386
clauses compare entry by entry, including 32,212 exact support-symmetry
clauses, 323,867 distance/degree clauses, and 1,817,142 literal physical
five-set clauses. It confirms 155,551 variables, 93,795,698 CNF bytes, and
SHA-256

    e12f321f059f59b98e530042c61c965167f5b50c401681ec858b807819b99cc5

A fresh run used CaDiCaL 3.0.1 at source commit
`c60730422e758ef1cebe7aeddf2dda31c996bf04` to regenerate the binary DRAT
proof. The local binary build had SHA-256
`b59032bea0b86d5e4f47db0d26923fc2ae93c4323fcb25ba398478deae4e4cdd`,
different from the submitter's recorded build, but it emitted the exact same
125,479,174-byte proof. Pinned `drat-trim` independently returned `s VERIFIED`.
The proof SHA-256 is

    a3780cdf12fcb0467a88e1fa5277451101c9628967c4bd597e81bd3bc8c24819

Thus solver correctness is not trusted; the verdict uses the checked proof.

## Reproduction

The compact submitted replay is:

```bash
python3 -B ramsey_r55_rank4_row_triple_support_band/reproduce.py
python3 -O -B ramsey_r55_rank4_row_triple_support_band/reproduce.py
```

After following the target package's documented full-replay commands under a
scratch directory, run the independent entrywise audit from the repository
root:

```bash
python3 -B ramsey_r55_rank4_row_triple_support_band_review1/independent_check.py \
  ramsey_r55_rank4_row_triple_support_band \
  /scratch/research-team-v2/tmp/reviewer-1/rank4-row-triple-replay/base.cnf \
  /scratch/research-team-v2/tmp/reviewer-1/rank4-row-triple-replay/proof.drat \
  /scratch/research-team-v2/tmp/reviewer-1/rank4-row-triple-replay/proof.json
```

Expected final status:

    VERIFIED_INDEPENDENT_ROW_TRIPLE_SUPPORT_BAND_REVIEW

The generated CNF and proof are deliberately excluded from this repository.

## Imported premises and trust boundary

Imported rather than reopened here: the pair-distinguisher bound, the
rank-four cut caps and row-cap-three theorem, the tripled-row contact interval,
`R(4,5)=25`, and standard DRAT soundness. The previously accepted complete
rank-four task cover provides context but is not needed to validate this
fixed-family exclusion. Remaining trust includes the pinned `drat-trim` C
implementation, CPython integer/file semantics, the compiler/runtime,
SHA-256, the exact source bytes, this reviewer's independent transcription,
and ordinary hardware. The argument is not proof-assistant formalized.

The prepublication direct-action formula documented in
`SYMMETRY_CORRECTION.md` is rejected evidence. Only the corrected
inverse-transpose CNF and its fresh proof are accepted here.
