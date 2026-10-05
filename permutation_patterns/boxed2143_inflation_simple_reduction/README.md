# Boxed2143 inflation and simple-permutation reduction

Theo (literature-researcher-4), 2026-10-05. Lyra
(literature-researcher-2) independently accepted the complete stated partial
proof A–E. This is internal team checking, not external peer review or a
novelty certificate. The full boxed2143 growth problem remains **unsolved**.

For a permutation p, a boxed2143 occurrence selects i1<i2<i3<i4 with
p[i2]<p[i1]<p[i4]<p[i3] and no other point inside their open rectangle.
Let a_n count avoiding permutations and s_n the simple avoiding permutations
(simple means no proper nonsingleton interval of consecutive positions and
consecutive values).

`ARBITRARY_INFLATION_BOUNDARIES_V1.md` proves:

* Every nonempty block inflation injectively retains all old boxed2143
  occurrences. Ordinary inflation cannot repair an input that contains a box.
* Blocks starting at their minimum and ending at their maximum satisfy exact
  occurrence additivity: occurrences of the parent plus occurrences within
  blocks. Universally safe single blocks are precisely anchored avoiders.
* A complete arbitrary-inflation formula adds weighted boxed132, boxed213
  and boxed12 terms, using two one-sided record-pair statistics of the blocks.
* Bounded-exponential growth of a_n is equivalent to bounded-exponential
  growth of s_n. In particular, s_k<=D^k for all k>=1 and D>=1 implies
  a_n<=(16D^2)^n. The proof uses interval contraction and deterministic
  substitution trees; it does not assume arbitrary-subsequence heredity.

The last statement reduces the entire original decision problem to simple
avoiders. It supplies neither the missing constant D nor an unbounded-rate
simple family. The general substitution framework is prior work, credited to
Albert–Atkinson, [Discrete Mathematics 300 (2005)](https://doi.org/10.1016/j.disc.2005.06.016),
with their [primary author manuscript](https://cs.otago.ac.nz/research/publications/oucs-2003-08.pdf),
Section2/Proposition2. The boxed-pattern question comes from Avgustinovich,
Kitaev–Valyuzhenich, [Discrete Applied Mathematics 161 (2013)](https://doi.org/10.1016/j.dam.2012.08.015),
and the current unresolved statement appears in Kitaev–Qiu–Xu,
[arXiv2609.13764v1](https://arxiv.org/html/2609.13764v1), Section7.

Run with CPython3.11+, standard library, one process/thread:

```sh
python3 -B arbitrary_inflation_controls_v1.py --output /tmp/boxed2143-inflation-author.json
python3 -B check_theo_arbitrary_inflation.py > /tmp/boxed2143-inflation-reviewer.json
```

Run from this directory. Expected deterministic results:

* 4545 all-block,3927 single-block and422 anchored inflations, checking
  complete occurrence sets and canonical lifts.
* All873 blocks through length6, with839 explicit unsafe contexts; safe-block
  counts1,1,1,2,6,23.
* All5913 positive-length permutations through7, substitution-tree decoding,
  simple labels and avoiding labels under interval contraction.
* Arbitrary stream:2f0ec6abbefa9fb7c6ffbf831f3207318c45862c0465c5ba8eda3c5ec7c7afa6.
  Anchored stream:136fe69d10648a57c563d3f0939423f06981b81e2d4d110901742470488f0095.
  Tree stream:90705fc4bdea4bb094a5647096dc50adfa6087827123b6588e801c8606796da4.

The independent checker enumerates literal quadruple/interior geometry and
uses an iterative contraction log followed by rank-path decoding, rather
than the author's interval scanner and recursive tree graft/evaluation.
Finite controls support implementation alignment; the written proof and
separate written review carry the uniform arguments.

`MANIFEST.json` freezes the five original author files. The accepted proof
hash is a577429ccb2563d53afdf81d5e20d89e882038948054a2c996c3c0f1b1bb455f.
`theo_arbitrary_inflation_review.md` and the original reviewer evidence are
unchanged. They retain their historical workspace paths and pending-author
wording; the complete subsequent acceptance is in the review. The only
reviewer-code edit is a default input path replaced by this directory;
`PORTABILITY_EDITS.json` pins both code hashes. `PORTABLE_REPLAY.json` records
the complete deterministic comparison with the frozen reviewer evidence.
Original machine timings are historical measurements, not requirements.

This packet is distinct from the earlier structural/one-sided publication.
It includes no private chat, checkpoint, paper PDF, key, binary, exhaustive
dump or graph ledger. Queue acceptance and graph commitment are separate
from source verification and mathematical correctness.
