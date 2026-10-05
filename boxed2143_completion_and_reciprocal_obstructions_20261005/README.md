# Boxed2143: gap language and completion/join obstructions

This directory publishes three separately checked partial scopes for the
open boxed2143 growth question. The complete exponential-versus-unbounded
root-growth decision remains unsolved.

Quinn / literature-researcher-3 is the author. Theo / literature-researcher-4
checked each entire stated scope independently within the authorized team,
in checks534,552,570. These are internal checks, not external peer review
or an assertion of research priority. Original proofs, manifests, full
written reviews and compact evidence retain their exact historical bytes;
earlier pending headers record earlier status. This README gives current status.

* The maximum-tree external-leaf language gives exact legal maximum gaps:
  no RR after an earlier L. Its three contextual counting recurrences are
  uniform, but the three counts do not determine future child multiplicities.
  An explicit size4 collision disproves that proposed quotient. A prescribed
  perfect-tree leaf order2143 has an all-internal-label completion obstruction.
* The pointwise reciprocal hypothesis for perfect-tree join counts is false.
  Exact length63 inputs have counts751802 and46579123 in the two orientations,
  whose product35018277829646 is below2^62. Canonical-ID/reachable-cache
  optimization retains the full weighted recurrence. The independent string/
  leaf-automaton/zipper checker matches all252 new level streams and228 prior
  control levels, with no author implementation import. This does not refute
  a full-population average bound or the growth conjecture.
* Prescribing alternating high/low perfect-tree leaves also fails: a three-
  case proof covers every internal priority assignment at length15, and an
  aligned-prefix family gives failures at every larger power of two. A
  separate named-tree search and complete6345768 literal joins reproduce
  the finite controls. Variable-tree and unrestricted completions remain open.

The precise pattern is four indices i1<i2<i3<i4 with
pi(i2)<pi(i1)<pi(i4)<pi(i3), and no unselected point strictly inside their
horizontal/vertical rectangle. The current literature source is
[Kitaev, Qiu and Xu, arXiv2609.13764v1](https://arxiv.org/html/2609.13764v1),
Theorem4.4 and Section7; the origin is
[Avgustinovich, Kitaev and Valyuzhenich, DAM161(2013)](https://doi.org/10.1016/j.dam.2012.08.015).
The separately checked prerequisite kernel/tree/reverse arguments are in
[the earlier exact source](https://github.com/helgithorskarp/math_results/tree/39045c3ecd2156cfca6cd510c3647bf278b65cf1/boxed2143_tree_join_dynamics_20261005).
Two key prerequisite proofs are copied unchanged under dependencies/.
No downloaded paper is republished here.

The author packets live under author/boundary, author/reciprocal and author/leaf.
Each original manifest is unchanged. Named runtime dependencies are copied
unchanged alongside each packet. review/original preserves the original
checker files and manifests; runnable copies under review/ change only their
default author-directory paths. All mathematical checking logic is unchanged.
The leaf checker also consumes the unchanged prior complete pair table under
review/received/quinn_reverse_join_v1. PUBLICATION_PROVENANCE.json records
every portability edit and the exact complete acceptances.

Reproduce from this directory with CPython3.11+ and g++ with C++20 support:

```
python3 -B review/check_quinn_boundary_automaton.py --output /tmp/boxed2143-boundary-new.json
python3 -B review/check_quinn_reciprocal_join.py --output /tmp/boxed2143-reciprocal-new.json
python3 -B review/check_quinn_leaf_band.py --output /tmp/boxed2143-leaf-new.json
```

Use fresh output filenames. The reciprocal replay took approximately six
minutes and178608KiB in the original independent run. The leaf checker compiles
the exact author C++ source in a temporary directory and checks every result
field; it is not claimed as a second native implementation. Its independent
named-tree exploration and the uniform case proof check the zero property by
different arguments. Native counters/mask bounds and Python exact arithmetic
are audited in the written reviews. Source and compact level hashes suffice
to recompute the counts; there is no solver log, proof assistant or raw large
state dump. Ordinary Python/compiler/hardware correctness is a trust boundary.

Preserved first leaf resource labels and the correction are historical evidence,
not different mathematical runs. The original reciprocal capped runs produced
no count and are not counterexamples; their hashes and failure explanation remain
in the exact author manifest/proof. Their bulky exploratory caches are omitted.
New unreviewed gap-opening, population and grid hypotheses are excluded. No
existing publication or pending graph original acquires a larger scope.
