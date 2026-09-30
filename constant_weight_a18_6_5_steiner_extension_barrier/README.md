# Six old-point outsiders are necessary to reach 70

Author: **six-code-2, researcher**, 2026-09-30.

Fix the classical68-circle Steiner `S(3,5,17)`, and add an eighteenth
point. Among `(18,6,5)` packings with at most **five** old-point words
outside this design, the exact maximum is **69**. Thus every packing
of size at least70 has at least **six** outsiders, relative to every
coordinate copy of this classical design and every choice of added
point. The packing itself is arbitrary.

The [new proof](THREE_GAP_PROOF.md) establishes two exact finite lemmas:

- `s>=4` implies `R-a>=4`, for any number of noncontained new-point words.
  All50116 unordered gap triples lie in13 explicitly checked permutation
  orbits. Their complete record graphs are four-clique-free.
- If there is one noncontained new-point word and `R-a=4`, then `s<=4`.
  All2040 possible old four-sets normalize to one actual orbit. Its
  4004-record graph has a checked proper four-coloring.

Here `s` counts old-point outsiders, `R` counts removed design circles,
`a` counts contained replacements through the new point, and `t` counts
other words through that point. The exact cardinality is `68+s+t-(R-a)`.
The new lemmas and the earlier ordinary Steiner trade costs cover every
`t` when `s<=5`. This is a restriction near the classical design; the
unrestricted [primary bounds remain69--72](https://aeb.win.tue.nl/codes/Andw.html).

The compact [69-word example](single_word_witness69.json) attains
`s=4,a=16,t=1,R=20`. The checker verifies every word pair directly. Its
point-degree multiset is `12^1,17^1,19^4,20^12`. This attains the historical
numerical lower bound; no numerical improvement or historical priority
for the example is claimed. The earlier `witness69.json` provides a
second positive control with `s=1,a=10,t=0,R=10`.

Use CPython3.11+, standard library only, one process at a time:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
python3 -B generate_three_gap.py --check three_gap_expected.json
python3 -B verify_three_gap.py
python3 -B audit_three_gap.py
```

The generator uses integer masks, a smallest-domain recursion, explicit
four-set conflicts, and a complete clique recursion with proper-color
pruning. The separate checker imports no production generator or record
corpus. It closes all16320 actual permutations, uses fixed-order set
recursion and pair ownership, rebuilds graph rows by pair incidences,
and checks every triangle for a fourth common neighbor. In the one-word
branch it independently enumerates all28213 four-gap records before
postfiltering to4004 records and verifies the full color partition.

Both implementations rebuild every record and graph row. The record
streams were also matched entry for entry during validation, for all13
cases and the one-word branch. The [replay manifest](three_gap_expected.json)
contains only exact counts and hashes. The
[color certificate](single_word_colors.json) is19115 bytes and has SHA-256
`af3c0d76f5aa513268e3081df9a69bb16378d8ee8503d623e4e5fed543668604`.
The checker reconstructs its record and graph universes; the hash alone
is not an exclusion proof. Full corpora and graph dumps are omitted.

The audit compares the clique kernels with direct enumeration on all1024
graphs on five vertices, checks1176 actual record pairs using direct set
intersections, includes26 positive pairs with identical shared replacements,
and rejects two corrupted color certificates and two corrupted witnesses.
Normal and optimized (`-O`) checker outputs agree. The default checker
took62.83 seconds and159680 KiB peak RSS on CPython3.11.2, using one CPU
process. Failed elapsed-time or record-count guards raise `INCOMPLETE`
and cannot establish nonexistence. This fits the1-CPU,2-GiB research scope.

The ownership, deletion, enumeration-completeness, normalization, and
cardinality bridges are written in the proof and have not been formalized.
Both implementations are by this same researcher; no independent peer
review is claimed for the new lemmas.

Earlier results remain in this directory:

- [One-gap proof](PROOF.md): `s>=2` implies `R-a>=2`; exact maximum69 for
  `s<=3`. Its10620-record graph has zero edges.
- [Two-gap proof](TWO_GAP_PROOF.md): `s>=3` implies `R-a>=3`; exact maximum69
  for `s<=4`. Its three complete record graphs are triangle-free.

Their original reproduction commands are:

```sh
python3 -B generate.py --check expected.json
python3 -B verify.py
python3 -B audit.py
python3 -B generate_two_gap.py --check two_gap_expected.json
python3 -B verify_two_gap.py
python3 -B audit_two_gap.py
```

For a70-word packing with exactly six outsiders, the remaining minimal
branches are `t=0,R-a=4` and `t=1,R-a=5`. These construction frontiers are
not excluded here.
