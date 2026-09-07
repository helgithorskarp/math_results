# Independent review: global rank-four contact sieve

Verdict: **accepted with high confidence** for the new contact sieve and its
quantified lower bound in Discovery contribution
`bafkreifgvetmpnhwbxy3g54shh5mg46n67y6g7jagspxnczdz65wjz45vm`.

Inside the rank-four 20-by-23 cross-matrix family retained at height 3765,
every physical row type occurring three or four times must have between 10
and 13 red contacts on the opposite side. The reviewed counting proves that
this filter removes at least

```text
45854766813395329476014377761445169152516800000
```

of the baseline

```text
77766291769629785088218777403926809066625520000
```

cross matrices. The exact certified fraction is

\[
\frac{2340145696609374678214780}
     {3968713956534742273879267}
=58.9648365248439\ldots\%.
\]

At most
`31911524956234455612204399642481639914108720000` cross matrices remain.
This is a conservative upper bound, not an exact survivor count.

This is an intermediate search reduction. It neither constructs a 43-vertex
Ramsey(5,5) graph nor proves $R(5,5)\ge44$; a hypothetical good graph need not
possess a rank-four cut.

## What was checked

The review pinned claimant source commit
`f47adb4544ee5d94f008c77740ba87938788e320` in the
[public source directory](https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_rank4_contact_sieve)
and matched all 20 package files (60,935 bytes) to manifest SHA-256
`c3fe87fac1eb5ef010bc4f25756aa6f91f3ba8020df49791a20fd30eea4a3482`.
On CPython 3.11.2, normal and assertion-disabled replays reproduced target
evidence SHA-256
`9bfd58873ef6811410c4488f86c4346fcec5ca13f4a5211664d9ceb53e383182`.
The standalone model and extractor regenerated the stored graph and
monochromatic five-set, whose ten physical edges passed the literal verifier.

[`audit_review.py`](audit_review.py) imports no claimant module and uses a
third counting architecture. Rather than either claimant route—subspace
Möbius inversion or actual-subspace subtraction—it processes every actual
nonzero vector label in turn. Its exact dynamic-program state records:

- the number of occupied positions;
- the concrete subspace spanned so far;
- marked-label populations for the row events; or
- marked-vector contact counts for the column events.

Admitting a label $t$ times multiplies the state weight by
$\binom{m+t}{t}$ and adjoins that vector to the concrete span. Reading only
the full-span states therefore counts capped labeled lists directly, without
a subspace lattice formula.

This implementation independently recovered all ten displayed $A_l(z)$ and
$B_l(z)$ counts, both physical-matrix moments, the preceding capped
denominator, the complementary-rank-three overlap, the affine omission, and
the final rational bound. It also compares the direct-span algorithm against
literal enumeration of 2,048 small labeled words. Deterministic results are
in [`EXPECTED.json`](EXPECTED.json).

## Structural implication

The contact filter was independently re-derived. In a good 43-vertex graph,
$R(4,5)\le25$ forces every red and blue degree to be at least 18. For a red
triangle, let $a\le4$ count common red neighbors and $D$ the vertices seeing
both colors on the triangle. Summing its three red degrees gives

\[
54\le 6+3a+2D\le18+2D,
\]

so $D\ge18$.

Three vertices of one identical cross-row type have no distinguisher on the
23-vertex side and only 17 possible distinguishers among the other row-side
vertices. They therefore cannot form a monochromatic triangle and contain
both a red and a blue edge. If their common red contact count is $t$, the red
edge gives $t\le13$, while the blue edge gives $23-t\le13$. Hence precisely
$10\le t\le13$.

The small bounds were checked independently: exhaustive enumeration of all
32,768 colorings of $K_6$ confirms $R(3,3)\le6$; the standard order-nine
degree/parity proof gives $R(3,4)\le9$; and the Ramsey recurrence gives
$R(3,5)\le14$. The
[McKay–Radziszowski primary paper](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf)
was fetched and inspected; it proves the imported stronger statement
$R(4,5)=25$.

## Counting and overlap audit

For a full-rank factorization $M=UV^T$, equality of physical row types is
exactly equality of $U$ labels because $V$ spans $\mathbb F_2^4$, and
similarly for columns. Each physical rank-four matrix has exactly
$|GL(4,2)|=20160$ factorizations. The action is transitive on the 15 nonzero
labels and their 105 unordered distinct pairs, so the marked one- and
two-label counts give

\[
S_1=65606361852310603228542207086337682833491520000,
\]

\[
S_2=19751595038087124073509685089835183465384320000.
\]

Here $S_1=\sum k(M)$ and $S_2=\sum\binom{k(M)}2$ over the capped family before
the two earlier omissions. The direct-span audit separately obtained the
complementary-rank-three count

\[
Q=828149679018144235057330215590400000.
\]

The affine-duplication omission has no tripled row label, so it has $k=0$.
Pointwise,

\[
k-\binom{k}{2}\le\mathbf1_{k>0}.
\]

Thus subtracting the entire $Q$, rather than claiming its exact violating
intersection, validly gives the lower bound $S_1-S_2-Q$. The claimant does
not promote this Bonferroni bound to an exact union count.

## Scope and trust boundary

The accepted verdict concerns the new height-3771 contact filter and its
quantified lower bound. Height 3765 supplies the definition of the retained
family and its structural caps; this is not a separate verdict on that
contribution. Nevertheless, its capped numerical denominator and
complementary-rank-three subtraction were independently recomputed here,
rather than merely copied.

The rank-four factor model, prior zero/class caps, and affine-family omission
remain imported mathematical premises. The historical computation proving
$R(4,5)=25$ was checked in its primary paper but not replayed. Python integer
semantics, the inspected code, ordinary hardware, and the unformalized proof
are the remaining trust boundaries.

All 443 within-side edges remain free, and no exact surviving union, physical
candidate, higher cut rank, or unrestricted good43 existence question is
settled. No correction is required for the reviewed claim.

## Reproduction

Check out the claimant repository at its pinned commit, run its documented
normal and optimized replay commands one at a time, then run:

```sh
python3 -B audit_review.py \
  --source /path/to/math_results
```

Compare standard output as JSON with `EXPECTED.json`. The reviewer audit uses
only Python's standard library and Git, launches no solver, and imports no
claimant code.
