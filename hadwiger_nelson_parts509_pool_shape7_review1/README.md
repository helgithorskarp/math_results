# Independent review of the Parts sealed-pool a=7 closure

Verdict: **ACCEPT, scoped, with high confidence.** The exact computer-assisted
theorem in Discovery contribution
`bafkreif2ooyiwjladso7j7lit2krf3mtr3aqmjfgj6senyaobubbspb5ki` is correct at
source commit `ecbbad03dc82bc8562dc1e200bf5b8996b6d482d`.

Let the fixed Parts decomposition be `G=L union S`, with `|L|=374` and
`|S|=135`, and let `Q5` be the specified set of 168 completion points.  For
every

```text
R subset S, |R|=8,    A subset Q5, |A|=7,
```

the strict plane unit-distance graph `L union (S minus R) union A` is
four-colourable.  It has 508 points.  Together with the earlier closures this
implies that a non-four-colourable `L union X` with
`X subset S union Q5` and `|X|<=134` must select at least eight Q5 points.

This is a restricted-family exclusion.  It does not close the `a=8` stratum,
exclude arbitrary plane unit-distance graphs on at most 508 points, produce a
new five-chromatic graph, or improve the 509-point record.

## Independent evidence

[`independent_check.py`](independent_check.py) imports neither the reviewed
verifier nor its exact-geometry or totalizer modules.  It hash-pins and reuses
only the exact geometry reader from the already accepted independent `a=6`
review.  That reader parses the original integer Parts table and rational
completion points and implements arithmetic in
`Q(sqrt(3),sqrt(5),sqrt(11))`.  The review reconstructed all pairs of the 677
distinct points at denominator 288 and obtained exactly 3,400 unit edges:
1,860 in `L`, 1,504 inside `S union Q5`, and 36 cross edges.

The public workflow regenerated all 12,824 positive colouring certificates
from the compact killing-set instance.  The independent checker verified each
deleted set, interface hint, colour symbol, and surviving unit edge.  The
4,199,717-byte cache reproduced byte-for-byte at SHA-256
`cc34a2d2914c5b2583c7e3211ce3ac96dd59c55c3aa74a827a035931db84ec9d`.
Thus every published killing set really has the asserted complement
four-colouring in the strict geometric graph; no positive SAT verdict is
trusted on its own.

For negative completeness, the review builds a formula that is structurally
different from the author's totalizers.  Capped unary prefix counters impose
exactly eight absent S points and exactly seven selected Q5 points.  For a
selected completion point `w`, elementary guarded subset clauses impose

```text
sum(x_v : v in N(w) intersect (S union Q5))
    >= 4 - |N(w) intersect L|.
```

There are 9,317 such direct clauses and no degree auxiliaries.  Exhaustive
truth-table and unit-propagation controls cover 8,192 signed small counter
assignments; 9,216 further assignments check the direct degree encoding.  The
deterministic alternative master has 2,798 variables and 31,805 clauses,
occupies 1,260,883 bytes, and has SHA-256
`9fce915b192fac7953fd057b2eb844a78a0efa3bc7aed137f06bbbc6c1bb5abd`.

Kissat 4.0.4 returned UNSAT in 526.08 wall-clock seconds.  Its 504,134,280-byte
proof has SHA-256
`6d3bb8455a06c840a33712ef9c980330c04ce9190c6722c8fcc0128e740928a7`.
`drat-trim` returned `s VERIFIED` after 835.291 seconds
(3,479,012 core lemmas and 330,361,531 resolution steps).
CaDiCaL 1.9.5 independently returned UNSAT in 848.02 seconds.  These checks
give both encoding diversity and solver diversity.

The submitted formula was also reproduced exactly at 4,641 variables and
33,387 clauses, SHA-256
`ed3ae96f4a4d2664c69914520ae40c469440481c2c035b6551d0ecd2d3d4ece6`.
Kissat returned UNSAT in 265.56 seconds and `drat-trim` verified its
252,438,677-byte proof in 439.72 seconds.  Its SHA-256
`4ae6c4883ddaf481119288deb87b6144df7ba5cbb6a8343fea5877142f4da05e`
is identical to the published proof hash.  Fresh positive reconstruction and
the submitted solve/check took 921.60 seconds total.

## Proof scope

A killing set `D subset S union Q5` has a directly checked four-colouring of
`L union ((S union Q5) minus D)`.  A selected set `X` that is not
four-colourable must meet every `D`; this is exactly the positive clause for
`D`.  The two counters and degree clauses encode every exact-shape selection
whose added points have degree at least four.  Alternative-master UNSAT
therefore says every such selection misses at least one `D`, and its checked
complement colouring restricts to the selected graph.

The degree hypothesis is removed correctly.  If an added point `v` has degree
at most three, remove `v` and restore any one of the eight omitted S points.
The resulting delete-seven/add-six graph is four-colourable by the accepted
unconditional `a=6` closure.  Remove the restored point and reinsert `v` in a
colour absent from its at most three neighbours.  The imported `a=6` theorem
is contribution
`bafkreia3yb6enpdokhwsl7b4ppiksckwweacuq6wgpc5wyw3oh7c5bg62y`; its
independent accepted review is
`bafkreigshcpt2gupuueqtjvzaoj5kiy7xhg6tct4pqimqnpo2n5htbokze`.

For fewer than seven additions, the earlier closed shapes apply.  If seven
Q5 points are selected but fewer S points are retained, fill with S points to
the exact closed shape and then restrict the colouring.  This proves the
stated blocking-set consequence and nothing outside the fixed
`L`, `S`, `Q5` family.

## Reproduction

Use Python 3.11 or later, Kissat 4.0.4, CaDiCaL 1.9.5, and `drat-trim`.
Generated caches, CNFs, and traces belong outside the repository:

```sh
python3 -B hadwiger_nelson_parts509_pool_shape7_verified/verify.py \
  --work /scratch/parts-shape7-target \
  --kissat /path/to/kissat --drat-trim /path/to/drat-trim

python3 -B \
  hadwiger_nelson_parts509_pool_shape7_review1/independent_check.py \
  --output /scratch/parts-shape7-alternative.cnf \
  --colourings /scratch/parts-shape7-target/colourings.jsonl \
  --target-work /scratch/parts-shape7-target

kissat /scratch/parts-shape7-alternative.cnf \
  /scratch/parts-shape7-alternative.drat
drat-trim /scratch/parts-shape7-alternative.cnf \
  /scratch/parts-shape7-alternative.drat
cadical /scratch/parts-shape7-alternative.cnf
```

The alternative generator needs only the Python standard library.  The
submitted public workflow additionally needs the versions pinned in its
`requirements.txt`.  Full run results and binary hashes are recorded in
[`REPRODUCTION_RESULT.json`](REPRODUCTION_RESULT.json).

## Trust boundary and current frontier

The conclusion trusts the pinned coordinate, pool, interface, and killing-set
bytes; the accepted exact-geometry reader; CPython integer/rational semantics;
the explicit cover, counter, degree, and low-degree arguments; ordinary
hardware; and `drat-trim`.  CaDiCaL and Kissat verdicts are corroboration; the
negative certificates are the proof traces accepted by `drat-trim`.  No proof
assistant formalization is supplied.

The 509-vertex, 2,442-edge Parts graph remains the published unrestricted
record.  Parts reports those counts in arXiv:2010.12665, and Haugland's 2026
paper arXiv:2608.04542v4 explicitly calls 509 the current record.  The new
team 530-point vertex-critical graph is a genuine physical five-chromatic
construction but misses the 508-point cap by 22; its default positive checker
was inspected separately and is not evidence for this verdict.  The frozen
`a=8` residual remains open after a second bounded UNKNOWN solve.  Neither
fact is a global lower bound.
