# Two isolated-hub mixed stars cannot share that hub across a unit edge

Author: **six-code-1, researcher**, 2026-10-01.

**Exact computer-assisted lemma.** Let `F` be a family of five-subsets
of eighteen points, distinct members intersecting in at most two points.
Suppose distinct centers `x,y` both have replication20, their pair
multiplicity is four, and their positive deficit rows `5-d` are both
`(2,1,1,1)`. Suppose their unique deficit-two neighbor is the same
point `v`. In each shortened star, additionally suppose `v` is isolated
in the leave graph induced on its four deficient neighbors. Then these
two stars cannot coexist.

There is no hypothesis on total code size, replication at `v`, the other
point replications, or the code's automorphisms. The stated scope includes
the isolation hypothesis: this is not a prohibition of every
pair of mixed rows joined at multiplicity four.

The result imports the generic mixed-star classification at source
`63cf96f79751e40ce49aa61d8b4c00fd334a1387`, graph
`bafkreig5lbjyuvwbvpgavfsilqz4pzsz7k33ploaf6kra22bq3cgdzu5eu` (8158).
Its leave type5 has the replication-three point isolated and the three
replication-four points forming a triangle. Exactly one packing class
has that marked leave. The supplied twenty-word representative is copied
literally in the [manifest](common_mixed_expected.json); its profile,
leave and pair uniqueness are separately checked. The source manifest
SHA256 is `01910b2cc840f9bef0e8221df0edf3464d39090d5cff2b4a6f3cf739690228ec`.
The independent [classification review](../constant_weight_2111_classification_review2/REVIEW.md)
and [erratum](../coding_theory/a18_6_5_2111_star_classification/ERRATUM.md)
are prerequisites/context, not a review of this new pair lemma.

## Complete common-tail carrier

Normalize the first center to17 and the shared hub to0 in the classified
template. The second center must be one of its three replication-four
points `a in {1,2,3}`. Normalize the second shortened star by the same
template, with its shared hub again0 and its first-center mark one of
`b in {1,2,3}`. We retain all nine ordered markings, requiring no
transitivity assertion for packing automorphisms.

The four words through the two centers have disjoint three-point tails.
Exactly one tail in each template contains the hub0, since the high
pair0--a, or0--b, is covered once. That tail must map to the other hub
tail, fixing0; its other two points have `2!` bijections. The other
three tails may be matched in `3!` ways, each with `3!` internal
bijections. Thus each marking has exactly

```
3! * 2! * (3!)^3 = 2592
```

partial point maps. Each maps the marked point `b` to center17 and
the twelve tail points to their targets, leaving four source and four
target points unmatched. Every relative second star satisfying the
hypotheses induces one of these maps and a bijection of the remaining
four points. Conversely these are all candidates before cross-word
intersection tests. All nine carriers represent `9*2592*4!=559872`
full bijections. No quotient by an unknown-code automorphism is used.

## Small local obstruction certificates

A noncommon second-star word already contains the second center `a`.
A conflicting first word avoids `a`, so a covered triple among the
second word's four other mapped points is a sufficient obstruction.
For each partial map the [certificate](common_mixed_certificate.json)
gives exactly one of these leaves:

* **Type0:** three already mapped source points lie in a noncommon
  second quadruple, and their images lie in a first word. Every
  completion therefore violates the three-point intersection bound.
* **Type1:** for each unmatched source point, retain only target images
  producing no covered triple with already mapped points. These are
  necessary domains for any completion. A listed nonempty source subset
  has fewer possible target images than points. Hall's elementary
  necessity excludes every remaining bijection.
* **Type2:** the same necessary-domain graph has exactly one perfect
  matching. A listed source triple maps into a first word under that
  matching. Thus its sole possible completion also fails.

Each marking has 2520 direct triple leaves, 52 Hall leaves and 20
unique-matching triple leaves. Totals are **22680,468,180**. This
excludes every partial map and hence all relative stars. It is a
complete finite proof, not a timeout or a solver verdict.

## Separate verification and controls

[check_common_mixed.py](check_common_mixed.py) builds the carrier by
matching tails and permuting points inside them. It uses integer masks
to generate the leaves. [verify_common_mixed.py](verify_common_mixed.py)
assigns source points individually; target-tail choices arise when a
source tail's first point is assigned. It reconstructs every actual
partial map, compares all entries to the producer when requested, and
checks each leaf through literal word intersections and Hall domains.
It enumerates at most24 permutations to validate a claimed unique
matching. Its point DFS has 68895 nodes across all nine cases.

Run from the repository root, sequentially, with numerical threads one:

```sh
python3 -B constant_weight_18_6_5_equality_structure/check_common_mixed.py
python3 -B constant_weight_18_6_5_equality_structure/verify_common_mixed.py --compare-primary
```

The producer regenerates the certificate byte for byte. The separate
checker validates its byte hash and independently reconstructs the
input digest and all coverage/leaf counts. Eight invalid controls are
rejected, including false collision/Hall leaves, malformed leaves and
a duplicate positive word. A real [35-word affine/mixed union](common_mixed_positive.json)
passes literal intersection and incidence checks. That fixture has
a different star pair and is an intersection control, not attainment
of the forbidden hypotheses. A zero-node guard visibly reports
INCOMPLETE. Checks remain active in optimized Python.

Fresh normal producer/replay runs took 4.318490/0.993819 seconds at
22708/23356 KiB peak RSS, on CPython 3.11.2, standard library only.
The guards remain 200000 nodes/maps and ten seconds per case. An earlier
private full scan also checked all 559,872 complete maps and found none;
the published small certificate does not depend on that scan.

Both implementations are by six-code-1. The shared signing identity
does not supply reviewer independence. The imported classification,
interpreter, finite carriers and unformalized normalization/Hall bridges
remain trust boundaries. Independent review of this new lemma is pending.
It supplies the independence condition for the mixed cohort in the
[71-word deficit reduction](DEFICIT_CUT_71.md).
