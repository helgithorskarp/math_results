# Exact weight certificates and a fractional obstruction at P84

This package has two exact results within the previously verified
[global P84 anchor decomposition](../p84_global_cases/README.md).

1. **Whole case 1226 is impossible.** An integer point-weight certificate
   excludes its entire 73-point completion problem. The global frontier
   consequently decreases from 1,211 to **1,210 unresolved cases**.
2. **The largest remaining case, orbit 21, admits a fractional cover even
   when its three eleven-classes are grouped into a single admissible block.**
   An explicit 74-term rational certificate proves that point-weight bounds
   on tens and on these joint eleven-blocks cannot exclude this case in the
   stated relaxation. Separate certificates establish the analogous
   individual-class obstruction for cases zero and 600.

There is no integer P84 witness or complete P84 exclusion here. The bound
remains **81 <= SR(8) <= 85**. The one new exclusion removes 101 of the
62,855,493 previously remaining anchored packings, leaving **62,855,392**.
The main methodological result is the exact obstruction to the proposed
weight relaxation, including its stronger joint-eleven form.

## Reproduce

From this directory, using Python 3.11+ standard library and GCC/G++ with
C++20 and unsigned 128-bit support:

```sh
python3 reproduce.py --work /tmp/p84-weight-certificates --sanitizers
sha256sum -c SHA256SUMS
```

Expected final output includes `verified: true`, `remaining_cases: 1210`,
and `fractional_certificates: 3`. The driver regenerates the eleven-catalog,
checks its established hash and canonical ordering, verifies every rational
identity and set in the fractional certificates, and computes the required
ten-weight maximum by two complete algorithms. Their entire ten-catalogs
match byte for byte. Small exhaustive tests and sanitizer builds exercise
both enumerators and the weighted maxima. Corrupted fractional coefficients
are rejected. `validation.json` records the completed delivery run.

Use a fresh work directory outside the source tree. Python optimized mode is
rejected because assertions check evidence. The two full ten-catalog files,
binaries and detailed outputs stay in that work directory. No optimizer,
SAT result, downloaded catalog, private input or earlier generated file is
needed for this reproduction.

## Case convention and dependencies

All labels are zero-based, in `0,...,83`. Integer Sidon sets have distinct
unordered pair sums **including repeated summands**. The canonical orbit
rank is the one in the preceding global package: reflect by `x -> 83-x`,
choose the smaller membership mask in each eleven-orbit, and sort by
nonincreasing old weight, then mask. The complete 30,510-set catalog has
15,255 reflection pairs.

Case `j` fixes its canonical eleven-set `A_j`. The remaining 73 points
`R_j` must be covered by three eleven-classes and four ten-classes. No
remaining eleven-class may lie in an earlier orbit. The previous global
lemma covers every balanced P84 partition up to reflection; the separately
reviewed profile theorem makes it cover unrestricted eight-class P84.
`remaining_cases.txt` removes only case 1226 from the preceding unresolved
ledger. All previous cases and certificates are preserved.

The external [review of the global reduction](../../sidon_ramsey_8_p84_global_cases_review1/README.md)
accepted it with high confidence and independently replayed the profile
premise and ten-weight bound. That review concerns the preceding package,
not the new certificates here.

## Integer exclusion of case 1226

Its canonical anchor is

```text
1 3 8 23 33 34 57 61 69 75 78
```

Let `u` be the 84 integer weights in `exclusion_1226.json`; weights on the
anchor are zero. On its complement:

```text
sum u(x)                         = 6,453,610
max u(T), T a Sidon ten-set      = 1,000,705
max u(E), E an allowed eleven    =   797,466
```

There are **5,906,761** ten-sets on this complement. Both the difference
and fixed-endpoint/pair-sum enumerators give the stated maximum and identical
catalogs. There are **3,514** allowed eleven-sets: filter the complete catalog
for sets disjoint from the anchor whose orbit rank is at least 1226. Their
maximum is checked directly using Python integer sums.

A completion would imply

```text
6,453,610 <= 4*1,000,705 + 3*797,466 = 6,395,218,
```

which is impossible. The strict integer gap is **58,392**. This excludes
all assignments in the case, regardless of which of its 101 qualifying
four-eleven packings might be chosen. It is not a bounded neighborhood of a
seed partition.

`weighted_catalog.cpp` uses the two established enumeration methods from the
global package, adding exact weight sums and a maximizing witness. Method
zero tracks unused positive differences; method one fixes endpoints and
tracks unordered pair sums. The only span pruning uses the necessary number
of distinct positive consecutive gaps. Every generated set is sorted by its
84-bit mask before serialization as its increasing point bytes. The complete
59,067,610-byte ten-catalog has SHA-256

```text
288672a1f728e3f2532be4e3f5ce7813567ef7fd27db44c482e5f63a9d31914d
```

All point and difference shifts fit unsigned 128-bit integers. Pair sums lie
in `0,...,166` and use two words. Input weights are bounded by one million;
each supported class has at most twelve elements, so weight sums fit signed
64-bit integers. The Python certificate arithmetic has arbitrary precision.

## A proved limitation of point-weight bounds

For case 21 the canonical anchor is

```text
5 8 19 21 25 46 53 58 68 76 77
```

It is the largest remaining case by the preceding anchored packing count:
**939,604** qualifying four-eleven packings.

Let `T` range over every Sidon ten-set disjoint from this anchor. Let `B`
range over unions of three pairwise disjoint allowed eleven-sets, disjoint
from the anchor, for which the old weight of `A_21 union B` is at least
**7,685,948**. This is the entire joint-eleven family in the previous
necessary packing reduction. It preserves the old weight cutoff and all
orbit restrictions; it is stronger than treating the three elevens
individually. It does not impose disjointness between a separately selected
ten and a separately selected joint block.

`fractional_joint_21.json` supplies **51 tens and 23 joint blocks**, with
strictly positive rational coefficients `lambda_T` and `mu_B`, satisfying

```text
sum lambda_T = 4
sum mu_B = 1
sum(T containing x) lambda_T + sum(B containing x) mu_B = 1
    for every x in R_21.
```

Each joint block includes its explicit decomposition into three elevens.
The checker verifies all Sidon properties, sizes, pairwise disjointness,
point membership, allowed orbit ranks and the old weight cutoff. The 73
point identities and both coefficient totals hold exactly over the rationals.
The certificate is a fractional cover, not an integer partition and not
proof that an integer completion exists.

**Obstruction theorem.** For any real point weights `w`, and any bounds `m10`
and `m33` valid respectively for every allowed ten and joint block,

```text
sum(x in R_21) w(x)
  = sum lambda_T*w(T) + sum mu_B*w(B)
  <= 4*m10 + m33.
```

Thus no choice of point weights, including signed weights, can produce the
strict reverse inequality needed to exclude this case using this relaxation.
Taking `m33=3*m11` also rules out all individual-class cap certificates for
case 21. This conclusion covers the full weight family, not merely the
floating-point weights tried in one run.

The qualification “this relaxation” matters. Additional compatibility
constraints or valid restrictions shrinking the ten/block families could
invalidate this fractional witness. In particular, the certificate does not
require a ten term to avoid a joint block appearing in another term. Keeping
that compatibility is the concrete next direction indicated by this result.

`fractional_0.json` and `fractional_600.json` similarly provide 74-term exact
certificates using individual tens and elevens, with coefficient totals four
and three. They prove
`sum w(R_j) <= 4*m10 + 3*m11` for all real point weights in those two cases.
No claim about their stronger joint-block relaxation is made.

## Discovery, validation and scope

The weights were discovered with SciPy 1.17.1 / HiGHS row generation. The
floating LP objective maximized `sum u(R)-3*z` subject to `u(T)<=1` for tens
and `u(E)<=z` for allowed elevens. Missing ten constraints were priced over
the full residual catalog. The case-1226 candidate was scaled to integers,
then its actual integer maxima were recomputed. Floating feasibility or
optimality is not used in the exclusion proof.

At cases zero, 21 and 600, the individual-class relaxation instead had a
floating optimum of four. Its dual support was reconstructed by exact
rational Gaussian elimination and verified directly. The stronger case-21
experiment replaced individual elevens with complete admissible triple
unions and coefficient total one. It also yielded the explicit rational
certificate above. No claim of minimum certificate support is made.

A shared-weight scan across all 1,488 eligible anchors transferred the new
weight vector to no additional unresolved case. A quadratic-weight pilot
also produced no additional whole-case exclusion. These were method-selection
experiments, not premises of either theorem. Together with the exact
fractional obstruction, they do not support continuing the same weight
optimization as the main search strategy.

The current milestone is one whole-case exclusion, a proved obstruction to
an entire class of proposed weight certificates in the largest case, and
preserved global coverage of the remaining 1,210 cases. The next phase should
retain the global coordinates and couple the choice of the joint eleven
block to its compatible tens. No seed search or problem reselection follows
from this method change.

These are exact computer-assisted results with a written reduction and
explicit certificates. The remaining trust boundary is the source, finite
catalog completeness, compiler/runtime and integer/rational arithmetic.
The two ten enumerators have a different mathematical organization but share
code ancestry with the earlier package. This new work has not had external
review or proof-assistant formalization. Historical priority is not asserted.
