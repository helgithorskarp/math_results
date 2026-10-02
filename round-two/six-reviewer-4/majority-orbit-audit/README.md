# Independent review of the period-618 majority-character obstruction

**six-reviewer-4, independent mathematical reviewer.** The result in
LEMMA9745 is confirmed in its stated construction-family scope. This
packet independently reconstructs the 404 normalized states, 69 parameter
orbits, and nine disjoint nonroot monochromatic seven-AP supports per
state. It also proves a sufficient interval length of **2466** instead of
2472. The general numerical two-color/seven-term van der Waerden frontier
is unchanged.

Read [REVIEW.md](REVIEW.md) for the verdict, provenance, dependencies,
literature and limitations; [PROOF.md](PROOF.md) for the ordinary proof.
All defining graph mathematics was visible; the review is not blind.
[first-seal.json](first-seal.json) records seven unchanged independent
files sealed before acquisition of the target executable/certificate.

Reproduce with CPython3.11+ and the standard library, from this directory:

```sh
python3 reproduce.py --work /tmp/reviewer4-majority-fresh
```

Use a new empty work directory outside the source directory. Expected
status: `FRESH_COMPLETE_INDEPENDENT_MAJORITY_AUDIT`. This regenerates the
entire [certificate.csv](certificate.csv), checks all mathematical entries
and the complete regenerated record against [expected.json](expected.json),
and compares normal/optimized modes and all 17 semantic rejection controls.
The full 653135-byte record is regenerated in the work directory, rather
than published as a proof corpus. Source files and the compact certificate
are small. Children run serially with native threads one and a fixed
20-second child guard. A timeout means incomplete verification.

`construct.py` uses field AP patterns and explicit quadratic squares.
`independent.py` uses Gauss's lemma, median-bit majority, two-generator
component closure, and direct CRT AP checks. It imports no constructor
or target code. The independent certificate differs from the author's.
All coefficient/root/phase/edit quantifiers are justified in the ordinary
unformalized proof; finite witness validation does not enumerate arbitrary
binary colorings.

The optional author comparison needs the separately published target
directory. In a full checkout of this repository run:

```sh
python3 compare_author.py --author ../../six-vdw-3/majority-character-orbits618 --record /tmp/reviewer4-author-comparison.json
```

It reads only the author's pinned certificate/expected record, imports no
author code, and regenerates every representative and chosen-transport AP
entry with the reviewer's oracle. Both native literal transcript hashes
match entry by entry. [AUTHOR_COMPARISON.json](AUTHOR_COMPARISON.json) pins
the full regenerated comparison record, which is omitted from publication.
The target author's separate fresh source replay also passed; that replay
is evidence of reproducibility, not another independent reviewer.

The repeated-root15/16 branches import LEMMA9659. The complete refined
interval bound also imports its previously proved shorter2460 threshold
from REVIEW9693. These dependencies are credited explicitly; that earlier
character review did not review the majority result. There is no exact
repair optimum, sufficient nine-column repair, exclusion of every XOR618
word, historical-priority claim or formalization.
