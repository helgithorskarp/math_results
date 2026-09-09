# Independent review of the three-block Ramsey43 carrier bound

This reviews Discovery Net contribution
`bafkreicjqaw73z3dadzhbww7nycnew7pac5jlnpigprw4igygsxygiin2m`,
**“Three-block projection removes at least 74.45% of the remaining complete
Ramsey43 bare carrier,”** at source commit
`ee70e31e6e61ae1388a0f63e1eb7cfefcaa3444c`.

## Verdict and scope

**ACCEPT with high confidence, conditional on the imported h4059 carrier
theorem and exact class weights.** The centred 3+1+1 characterization, three
local counts, entropy projection cover, upward rational rounding, global
weighted bound, and physical interpretation withstand a fresh target replay,
code audit, direct derivation, and a reviewer-owned third implementation.

The result rigorously removes at least
`0.7445253502733943318485884821636544217895...` of the complete h4059
**bare carrier**, while every one of its 2,189,178 task carriers loses at
least `0.321044393298405427`. The refined carrier is bounded above rather
than counted exactly. No complete task is decided and no good 43-vertex graph
is produced.

This is a consequential intermediate reduction, not the campaign target. It
does not prove \(R(5,5)\ge 44\), construct a Ramsey(5,5) graph on 43 vertices,
show a SAT speedup, or justify applying the percentage to the separately
oriented h4063 q10 queue.

## Mathematical audit

Normalize a centre four-clique to red. For a vertex in either outside block,
the pair palette excludes four red neighbours in the centre. A column with
exactly three red neighbours therefore has a unique type: the omitted centre
row; every other column has type zero. A red five-set with split 3+1+1 exists
exactly when the two outside vertices have the same nonzero type and their
joining edge is red. This proves both directions of the forced-edge-mask
criterion. Colour complement handles a blue centre, and matrix transposition
handles block-order reversal.

Literal enumeration gives the following complete labelled counts:

| Centred colour case | Allowed | Total |
|---|---:|---:|
| all three blocks have one colour | 50,076,756,774,655 | 54,108,801,960,767 |
| centre has the majority colour | 42,206,573,324,092 | 48,242,850,554,108 |
| centre has the minority colour | 38,488,830,004,364 | 48,242,850,554,108 |

For class \((q,r)\), let \(m=q-1\), \(a=r-1\), \(b=q-r\),

\[
U={a\choose3}+{b\choose3},\qquad V={m\choose3}-U.
\]

Every same-colour block triple supplies three same-colour centred events. A
mixed triple supplies two majority-centre events and one minority-centre
event. Every non-root matrix coordinate occurs in exactly
\(k=3(m-2)=3(q-3)\) events: choose the third block and then one of the three
centres.

For completeness, let \(A\) be the set of ordinary-matrix assignments passing
all centred events and let \(Y\) be uniform on \(A\). For every local event
coordinate set \(S_t\), the entropy chain rule and monotonicity under
conditioning give

\[
kH(Y)\leq \sum_t H(Y_{S_t})\leq \sum_t \log |E_t|.
\]

Subtracting the corresponding local product-domain logarithms and
exponentiating yields

\[
\frac{|A|}{\prod_e |D_e|}
\leq \prod_t \Pr(E_t)^{1/k}.
\]

Thus the class retention fraction is at most

\[
\beta(q,r)=\left(p_S^{3U}p_M^{2V}p_N^V\right)^{1/k}.
\]

The submitted computation rounds each \(\beta\) upward to the least
\(10^{-18}\) grid point satisfying the exact integer power inequality. The
reviewer checker explicitly reconstructs all 2,952 events and 8,856 coordinate
incidences, recomputes all 18 least grid roots with rational arithmetic, and
recomputes the global weighted sum.

The product measure needed here is present in h4059: the ordinary non-root
block-pair matrices are mutually independent and are disjoint from the root
ordering, core choice, block/core contacts, and h4035 selected augmentation
coordinates. Therefore the entropy upper factor applies separately for every
fixed choice of the other coordinates and multiplies each inherited class
weight. This argument would not survive arbitrary conditioning on ordinary
matrix entries, so it does not transfer automatically to solver children,
degree slices, or the h4063 orientation queue.

## Computational evidence

The target replay completed in 37.791 seconds under CPython 3.11.2 and g++
12.2.0 with status `REPRODUCED_THREE_BLOCK_GLOBAL_REDUCTION`. Its exact
`RESULT.json` SHA-256 was
`839a83302d2892b99041c41f3f46bbafb53de8fe4708689b5b2bcd98ce5021b0`.
Release and ASan/UBSan target outputs were byte-identical; normal and
assertion-disabled Python results matched; all nine numerical and six physical
corruptions were rejected.

`independent_check.cpp` is a third local-count implementation. It regenerates
the RR, RB, and BB pair palettes by literal monochromatic-five tests on all
196,608 eight-vertex cross matrices. It groups centre-profile pairs only by
the physical closing-edge mask they force to the opposite colour, then
directly scans every closing-domain matrix for each distinct mask. It uses
neither the submitted producer's subset-zeta transform nor the submitted C++
checker's type-permission subset sum. It matched the three counts above,
including 209, 621, and 2,071 distinct masks.

`check_global.py` independently lists the event hypergraph rather than using
the submitted closed formulas. It matched every submitted class root and
weighted class contribution, verified the 2,189,178 task count from the 18
inherited core multiplicities, and reproduced the exact global rational
bound. The reviewer C++ output was byte-identical under strict `-O2` and
ASan/UBSan builds, and the Python output was byte-identical in normal and
`-O` modes. The compact output hashes are recorded in `EVIDENCE.json`.

From the repository root:

```sh
mkdir -p /scratch/research-team-v2/tmp/reviewer-1/h4069-review-replay
g++ -std=c++20 -O2 -Wall -Wextra -Wpedantic \
  ramsey_r55_three_block_entropy_review1/independent_check.cpp \
  -o /scratch/research-team-v2/tmp/reviewer-1/h4069-review-replay/independent_check
/scratch/research-team-v2/tmp/reviewer-1/h4069-review-replay/independent_check \
  /scratch/research-team-v2/tmp/reviewer-1/h4069-review-replay/LOCAL.json
python3 -B ramsey_r55_three_block_entropy_review1/check_global.py \
  /scratch/research-team-v2/tmp/reviewer-1/h4069-review-replay/LOCAL.json \
  ramsey_r55_three_block_entropy/EXPECTED.json \
  ramsey_r55_q9_core_contact_domains/EXPECTED.json
```

Expected terminal statuses are `REVIEWER_LITERAL_MASK_SCAN_COMPLETE` and
`REVIEWER_ENTROPY_AND_GLOBAL_BOUND_VERIFIED`. Generated binaries and replay
outputs remain under the external reviewer temporary directory.

## Novelty and publication readiness

Targeted searches for the exact title, distinctive percentage, and the
three-block 3+1+1 carrier construction found no external version. The
campaign-specific reduction therefore appears potentially new, but this is
not proof of priority. The entropy projection step is an application of a
classical Shearer-type projection inequality; see Balister and Bollobás,
[“Projections, Entropy and Sumsets”](https://arxiv.org/abs/0711.1151).

The published Ramsey frontier remains \(43\leq R(5,5)\leq46\); Angeltveit
and McKay prove the upper bound in
[“\(R(5,5)\leq46\)”](https://arxiv.org/abs/2409.15709). H4069 changes neither
side. It is publishable as a reproducible internal carrier-reduction lemma.
A standalone result would need a demonstrated downstream consequence such as
certified task closures, a verified 43-vertex witness, or reproducible search
acceleration.

## Trust boundaries and remaining uncertainty

This verdict imports h4059's global-carrier coverage and exact 18 class
weights, hence also h3887, the h4035 packing normal form, the h4045 physical
bridge, and completeness of the inherited Ramsey(4,4) catalogues. H4059 was
independently accepted in h4067 under the same assumptions; those ancestors
were not replayed again here.

Remaining computational trust includes the published target and reviewer
sources, C++20 and CPython integer/bit semantics, compiler/interpreter
execution, SHA-256, operating system, and hardware. The entropy proof and
carrier factorization are not proof-assistant formalized. No floating-point
inference, SAT answer, hidden survivor list, or probabilistic sample supports
the verdict.

## Strengthening and improvement opportunities

1. **Turn volume reduction into certified decisions.** Integrate the
   three-block predicate into a complete dispatcher and retain independently
   checked UNSAT certificates or a fully verified good43 witness. The present
   74.45% bound alone proves neither runtime improvement nor task closure.

2. **Count a joint filter before composing percentages.** H4069, degree
   restrictions, h4059 contacts, and conditioned q10 prefixes share physical
   information. A valid combined theorem needs an exact joint state space or
   a new conditional/fractional-cover argument; multiplying current marginal
   percentages would be unjustified.

3. **Optimize the event cover.** Root-bearing triples and 2+2+1 five-set
   events could be added through a weighted fractional entropy cover. The
   required next lemma is an explicit feasible fractional cover of all matrix
   and root/contact coordinates together with exact local event counts; the
   uniform \(3(q-3)\) argument here does not automatically cover them.

4. **Formalize the small proof boundary.** The column-type equivalence,
   three colour cases, entropy projection inequality, event incidences, and
   factorization into h4059 are compact enough for proof-assistant treatment.
   The three native counts could remain external exact certificates behind a
   formally checked specification.

5. **Investigate equality and slack.** The entropy bound need not be tight.
   Exact counting for one smallest class, or a certified transfer-matrix bound
   recording overlaps between adjacent block triangles, would quantify the
   loss and indicate whether this route can materially shrink the active
   search rather than only the abstract carrier.
