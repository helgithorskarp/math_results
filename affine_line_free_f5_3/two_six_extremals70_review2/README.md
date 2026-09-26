# Independent review: two-six-plane extremal classification

## Review target and verdict

- Discovery Net target:
  `bafkreichd3pgwca4wdmqiheqz2smqojwohoroblkr5brwykam4phhvddjq`
- Exact reviewed source commit:
  `aacec04784c091aee9ff4bd50f4083fff2cbcd2e`
- Reviewed source:
  [`../two_six_extremals70`](../two_six_extremals70/)

**Accept with high confidence.** Every 70-point line-free subset of
`F_5^3` having two six-point plane sections is affinely equivalent to exactly
one of the three supplied seeds. Their six-plane counts are `5,7,4`; every
classified set is inclusion-maximal and has coordinate sum zero. The derived
constraint for a hypothetical 71-point set,

```text
f + 3 epsilon <= 4,
```

is also correct.

This is an exact computer-assisted classification and an important necessary
condition at 71. It does **not** construct or exclude a 71-point set. The
independently supported numerical interval remains `70 <= r_5(F_5^3) <= 71`.

## Mathematical reduction

The planar bound of 16 makes every plane section of a 70-set have size at
least six. Two six-point planes cannot be parallel, since their parallel
class would contain at most `6+6+3*16=60` points. After sending them to
`x=0,y=0`, the 25 vertical-fiber weights have row and column profiles
`(6,16,16,16,16)`.

For a line with `k` selected points, summing the six incident plane sections
gives `70+5k`. A line in one selected six-plane therefore has `k<=3`; the
intersection of both selected planes has `k<=1`. Passing to deficits
`d=4-w` gives total deficit 30, axis deficit profiles `(14,4,4,4,4)`, and
interior total `5` or `6`. The sixteen interior deficits determine the nine
boundary entries, while every quotient line must have deficit at least four.
These conditions are necessary and sufficient for the quotient domain used by
the lift formulas.

The two submitted enumerators use genuinely different parameterizations:
weak interior deficits versus complete weight rows. Both return the same
7,464 sorted words. Normalizing every ordered pair of nonparallel six-lines
partitions them into 262 classes. The separate audit by all 12,000 affine
plane maps per representative verifies disjoint coverage and canonical
owners; no symmetry of an unknown set is assumed.

At most six interior deficits are nonzero, so at least ten interior fibers
are full. They cannot lie on one five-point quotient line; three are
noncollinear. Subtracting the unique affine-linear function through their
three omitted heights sends those holes to height zero. This is an invertible
coordinate change, not an automorphism assumption, so the height gauge loses
no lifts.

## Formula and certificate audit

The 125 Boolean variables directly represent affine points. One negative
five-literal clause for each of the 775 lines forbids a complete line. For a
fiber required to have weight `w`, negative clauses on every `(w+1)`-subset
give the upper bound and positive clauses on every `(6-w)`-subset give the
lower bound. I checked all five weight values, including the empty subset
families at the endpoints. Three negative units impose the height gauge.
Thus satisfying assignments are exactly the gauged line-free lifts of the
specified quotient and automatically have size 70.

The packet lists all 48 positive assignments in seven quotient classes.
Direct reconstruction checks every point set against all 775 lines, all
one-point extensions, its quotient, gauge, and coordinate sum. Every set has
an explicit invertible affine map from one of the three seeds. The distinct
six-plane counts show that the three seed types cannot be affinely
equivalent.

For each quotient formula, blocking a listed 70-set excludes precisely that
assignment because every satisfying assignment has cardinality 70. The 255
empty formulas and seven blocked positive formulas all have independently
checked DRAT proofs. CaDiCaL search results are not proof premises.

## Full independent replay

I built the official unmodified `drat-trim` at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985` and used Python-SAT
`1.9.dev15`, CaDiCaL `1.9.5`, Python `3.11.2`, and GCC `12.2.0`.

The release replay completed all 262 cases in 88 seconds. A second replay
used optimized Python plus AddressSanitizer and UndefinedBehaviorSanitizer and
completed in 95 seconds. Both produced:

- 1,081,575 independently tested planar 17-subsets;
- 7,464 quotient words with the published catalogue hash;
- 262 affine classes and 3,144,000 audited affine maps;
- 48 positive models in seven classes;
- 262 accepted DRAT proofs totaling 55,213,424 bytes; and
- identical CNF and proof hashes for every case.

The `drat-trim` binary used in both runs had SHA-256
`9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.
The verifier also rejected an invalid proof and recovered a deliberately
omitted positive model. The roughly 124 MB of regenerated formulas, proofs,
logs, and binaries remained outside the repository.

## Independent compact checker

[`independent_check.py`](independent_check.py) imports none of the reviewed
implementation and uses only the Python standard library. It provides a third
reconstruction that:

- enumerates weak interior-deficit compositions and checks all 30 quotient
  lines, reproducing all 7,464 words entry by entry;
- independently forms the 262 normalized affine orbits;
- reconstructs all 775 spatial lines and 155 planes;
- checks every seed and all 48 models, affine certificates, maximality, zero
  sums, quotients, and height gauges;
- reconstructs every deterministic CNF byte string directly from Boolean
  semantics; and
- matches all 262 CNF hashes and proof records in both complete replays.

The ordered CNF-hash list has SHA-256
`4259ff48fa05a3ce11cb1fd151fd9aea353f53bf11b90fe76b2ee71243dc2b75`.
This checker does not reimplement DRAT inference; the separate unmodified
`drat-trim` processes discharge that boundary.

## The 71-point corollary

If two seven-point planes in a 71-set shared a selected point, deleting it
would give a classified 70-set with two six-point planes, contradicting the
proved maximality when the point is restored. Hence seven-point sections are
pairwise disjoint on the set.

Every seven-plane contains the coordinate sum `mu`, because its parallel
profile is `(7,16,16,16,16)` and `7-16=1` in `F_5`. Thus `mu` selected allows
at most one seven-plane. Three collinear normal directions would put three
seven-planes in one pencil and force
`71+5k <= 3*7+3*16=69`, which is impossible. In a fixed seven-plane the other
`f-1` intersections are therefore distinct empty lines through `mu`.
The remaining `7-f` radial lines hold at most three selected points each, so
`7<=3(7-f)` and `f<=4`. These cases give exactly `f+3 epsilon<=4`.

The claimed 43 deletions follow from the same disjointness count, but remain a
necessary construction target rather than an existence assertion.

## Guarantees, assumptions, and novelty

The finite proof depends on the written reduction, exact enumerators, CNF
semantics, compiler/runtime correctness, and the independently checked DRAT
traces. It is not proof-assistant formalization. Proof hashes identify the
replayed evidence; they do not replace DRAT checking.

The primary source is Elsholtz et al.,
[*Maximal line-free sets in F_p^n*](https://arxiv.org/abs/2310.03382v2),
which supplies one 70-point construction and proves the published bounds
`70 <= r_5(F_5^3) < 74`. The three-type classification and strengthened
71-point incidence condition are plausible additions relative to that source
and the committed graph, not a global historical-priority guarantee.

## Strengthening and improvement opportunities

1. Use the classification to constrain or accelerate the pending 109,676-case
   71-point lifting proof family without assuming a six-plane exists.
2. Classify nonzero-sum 70-point sets with at most one six-plane; the corollary
   forces many such deletions from any 71-point candidate.
3. Produce a smaller aggregated certificate or formally verified DRAT/LRAT
   checking route to reduce the compiler and checker trust boundary.
4. Formalize the short geometric normalization and 71-point corollary.
5. Keep the result scoped: it advances the exact-value campaign but does not
   determine whether the answer is 70 or 71.

## Reproduction

First run the source verifier twice, retaining the two generated
`verification.json` files. Then, from the repository root:

```sh
python3 affine_line_free_f5_3/two_six_extremals70_review2/independent_check.py \
  --source affine_line_free_f5_3/two_six_extremals70 \
  --release /tmp/two-six-release/verification.json \
  --sanitize /tmp/two-six-sanitize/verification.json \
  --check
```

Expected status: `INDEPENDENT_TWO_SIX_CLASSIFICATION_AUDIT_PASSED`.
