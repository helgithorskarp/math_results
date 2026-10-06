# An auxiliary zero-pool injection for boxed2143 completion

Quinn / literature-researcher-3; complete different internal check by
Lyra / literature-researcher-2. Author892, review916, actual whole author
acceptance926, 2026-10-06. This directory publishes a conditional all-size
lemma and its proofs. The full boxed2143 growth problem remains open in
this campaign. This is an internal team check, not external peer review
or a claim of novelty.

For boxed2143, the selected positions satisfy i1<i2<i3<i4 and their values
satisfy p[i2]<p[i1]<p[i4]<p[i3]. An occurrence additionally requires that
no UNSELECTED point lie in the open rectangle with horizontal endpoints
i1,i4 and vertical endpoints p[i2],p[i3]. In particular the upper value
is that of the THIRD selected point. Avoidance throughout an actual
completion episode, rather than just at its final word, is a hypothesis
of the lemma below.

## Exact partial result

Fix an actual completed parent P under the original/AUX source-unit and
ordered-birth completion conventions in the included dependencies.
Greater neighbors and eligibility are geometric: a point is eligible
when both nearest greater endpoints are genuine and the left endpoint's
value is smaller than the right endpoint's. ORIGINAL boundaries and END
have unit weight; AUX boundaries have zero weight. K_P(j) counts the
boundaries strictly after j through its nearest greater right fence,
including a unit before an ORIGINAL right fence.

Let J(P) be the DISTINCT old AUX points j initially ineligible with K_P(j)=1
for which some actual next-original episode selects a unit outside
(j,r_P(j)] and ends with j eligible and K(j)>0. This is an existential
point set; it does not count successful gaps or repetitions, and may be
empty. Let Z_0(P) be the initially eligible AUX points with K_P=0.

The included ordered-episode reduction gives a genuine initial AUX right
fence r, a unique initial ORIGINAL h in (j,r], and a first new RIGHT AUX a
with spatial j<h<a<r and birth values v(h)<v(j)<v(r)<v(a). Earlier new
births are outside (j,r); the selected original is last and beyond r.

**Lemma.** For every j in J(P), the maximum-value OLD point z(j) of the
initial open interval (h,r) exists and lies in Z_0(P). Its initial nearest
greater right fence is r. The map j -> z(j) is injective, hence

    |J(P)| <= |Z_0(P)|.

The image point remains of mass zero under the actual source policy.
From an IMAGE point z and the fixed P, its right fence recovers the unique
initially ineligible geometric point having that fence, which is the
original j. No decoder or surjectivity is claimed for arbitrary Z_0(P).

Choose the rightmost old pre-h point x above h. The immediate selected
rectangle (x,h,a,r) has full height range (v(h),v(a)); every old point
between x and h is below its bottom and every prior new point is outside
its horizontal span. Avoidance therefore forces an old AUX blocker after
h. Its interval maximum has right neighbor r, a genuine smaller greater
left neighbor, and no remaining original units. Finally two initially
ineligible points cannot have the same genuine nearest greater right
fence: the later one's left neighbor would be smaller than that fence.
The complete case arguments and zero-absorption transport are in the
independent proof and dependencies.

## Source and status

- `author/draft892.md` preserves the unchanged original 5455-byte draft.
  Its historical UNREVIEWED and pending878 labels describe its writing
  time; the complete exchange above now closes this separate lemma.
- `review/independent_proof_v2.md` and `review/independent_verdict_v2.md`
  preserve the complete current different-researcher hand return.
  Their historical author-acknowledgement-pending sentences are superseded
  by `author/acceptance.md` and actual message926.
- `dependencies/` contains all seven named closed written documents.
  The transport718 and ordered reduction832 are the mathematical premises;
  retirement735 is context. Their original labels and finite-evidence
  qualifications remain intact. Neither review878 nor a finite empty
  positive-event table is used to prove this lemma.
- `review/correction.md` records the preserved, unissued V1 height-definition
  error and its correction before any return. V2 is the current proof.

The argument is conditional on an ACTUAL successful outside episode.
It constructs neither a nonempty J(P) nor a positive example. The larger
interval maximum lying before h and having K1 is only a conditional case
formula. An injection of points in one parent supplies no selected-gap,
repeated-event, changing-history or lifetime price. A persistent K0 image
provides no positive unit charge. Original births, LEFT-prefix transfers,
terminal repeats, actual source weights and an attained mean/C/theta_n
bound remain unproved here. This source does not establish general H or
either alternative of the full agreed growth target.

The full target is to decide whether the number a_n of boxed2143-avoiding
permutations admits a finite C>0 with a_n<=C^n for every n>=1, or instead
limsup a_n^(1/n)=infinity. An ordinary growth limit is not assumed.

## Reproducing the source-integrity check

From this directory, with Python 3.11 or later and its standard library:

```sh
python3 verify_source.py
```

Expected: `PASS: 14 named source files match the manifest.` The checker
reads files and compares exact lengths and SHA256 digests; it writes no
data and performs no mathematical experiment or proof verification.
The manifest's own bytes are excluded. The proofs require human checking
of their hypotheses and all-size arguments. No finite examples, old
census, generated certificate, solver or proof assistant is claimed as
fresh evidence for this result.
