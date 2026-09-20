# Review report

## Target and verdict

Target contribution:
`bafkreifch5tgknmrjs24csg2flivk5smfmiz57h4y5jtmel3ovnquinvjy`,
“Uniform Erdos-Szekeres blow-ups cannot create a first counterexample.”

Reviewed source commit:
`0b4c5b98f2727f39fa87f50f5d1cb01e444eb973`.

**Verdict: accept with high confidence.**  The positive-excess identity,
hereditary witness extraction, first-failing-size consequence, conditional
bound, and endpoint-profile equality criterion are correct under the stated
hypotheses.  No mathematical or source-integrity defect was found.

The conclusion is deliberately narrow.  It applies to the uniform
`x`-blow-up from Baek--Balko Corollary 15, with `x>=1` and an interior
threshold.  It neither handles their arbitrary nonuniform `(X,Y)` blow-ups
nor resolves any open case of the unrestricted Erdős--Szekeres conjecture.

## Human premises and completeness reductions

The verdict depends on the following premises.  They were checked directly;
agreement between the two programs is not being used as a substitute for
their completeness.

1. **Imported construction and formula.**  The open-access SoCG 2025 primary
   paper defines a left point by the size of its largest convex subset with
   that point rightmost, and a right point symmetrically.  Its Corollary 15
   takes `m=k-2x`, an interior threshold `L in [N-1]`, and gives exactly

   `B=2 sum_{ell=0}^x C(k-2,ell)+sum_{j=2}^{m-1}v_j C(k-j-1,x)`.

   It also proves that the resulting set has no convex `k`-gon.  Thus the
   target neither changes the endpoint convention nor silently substitutes a
   different cluster formula.

2. **Coordinate normalization and two endpoints.**  Strictly increasing
   horizontal coordinates are part of the setting.  The primary paper also
   adopts distinct vertical coordinates.  If needed, a generic affine shear
   `(u,v)->(u,v+epsilon*u)` separates vertical coordinates while preserving
   horizontal order, every orientation sign, convexity, and endpoint ranks.
   For `1<=L<N`, only the global leftmost point on the left side and global
   rightmost point on the right side have rank one, so `v_1=2`.  At `L=0` or
   `L=N`, this becomes one; those boundary thresholds are correctly excluded.

3. **Reference profile.**  The profile `v*_1=2`,
   `v*_j=2^(j-1)` for `2<=j<=m-2`, and `v*_{m-1}=0` has total
   `2^(m-2)` and cumulative counts `V*_j=2^j`.  The `m=3` instance is
   `(2,0)`, so the empty-sum boundary is covered rather than inferred from a
   nonempty recurrence.

4. **Binary-word partition.**  For words of length `n=k-2>=2x+1`, the two
   classes having at most `x` zeros or at most `x` ones are disjoint.  Every
   remaining word has a unique shortest suffix containing `x+1` of both
   symbols.  If its length is `t`, the first suffix symbol is the one whose
   count was `x` before that symbol was added.  Choosing this symbol, its `x`
   later positions, and the arbitrary prefix gives
   `2^(n-t+1) C(t-1,x)`.  The substitution `j=k-t` covers exactly
   `2<=j<=m-2`, proving the sharp reference identity without a missing or
   duplicated class.

5. **Summation by parts.**  After subtracting the reference profile, put
   `a_j=v_j-v*_j` and `A_j=sum_{h=2}^j a_h=V_j-2^j`.  The finite identity

   `sum a_j w_j = A_{m-1}w_{m-1} + sum A_j(w_j-w_{j+1})`

   has no dropped endpoint.  Here `w_{m-1}=C(2x,x)` and Pascal gives
   `w_j-w_{j+1}=C(k-j-2,x-1)`, exactly the displayed excess formula.

6. **Strict positivity and the role of `x>=1`.**  Every coefficient is
   positive for `x>=1` and `2<=j<=m-2`.  For `x=0`, the layer coefficient
   would require a lower index `-1`, and more importantly `k=m`, so the strict
   descent `q<=m<k` disappears.  The theorem does not overclaim this boundary.

7. **Hereditary extraction.**  If `N>2^(m-2)`, the seed itself is the
   required witness at `q=m`.  Otherwise positive output excess forces some
   `V_j>2^j`.  The corresponding left and right endpoint sublevel sets have
   total size `V_j`, so one has more than `2^(j-1)` points.  A convex
   `(j+1)`-subset there would have a designated extreme vertex of rank at
   least `j+1`, contradicting membership.  The ranks are computed in the
   original seed, so deleting other points cannot reverse this implication.

8. **First-failing-size consequence.**  Corollary 15 makes the output
   `k`-gon-free.  If it exceeded `2^(k-2)` at the smallest failing `k`, the
   extracted set would violate the conjectured bound at some
   `3<=q<=m<k`, a contradiction.  This deduction does not assume the
   conjecture at an unknown size; it uses only the definition of the first
   failure.

9. **Conditional bound and equality.**  Validity of the conjectured bound
   through `m` gives `N<=2^(m-2)` and separately
   `|A_j|,|C_j|<=2^(j-1)`, hence `V_j<=2^j`.  All excess summands are then
   nonpositive.  Since their coefficients are strictly positive, equality of
   their sum forces every deficit to vanish.  Successive differences yield
   precisely the reference multiplicities, including `v_{m-1}=0`; equality
   of the two endpoint-set bounds follows from their sum.  This classifies
   counts, not geometric order types.

10. **Scope separation.**  The argument reads only the uniform cardinality
    formula.  It supplies no analogous positive decomposition for the general
    nonuniform construction, and it does not rule out a smaller counterexample
    already present in the seed.  The contribution states both limitations.

## Independent reproduction and adversarial cases

All seven target-manifest entries matched their byte lengths and SHA-256
hashes.  Its standard-library verifier reproduced the claimed output in about
0.7 seconds: 27,300 formal profile/parameter cases, 840 reference cases,
10,584 explicitly classified words, 36 geometric fixtures, 249 thresholds,
996 geometric blow-up cases, 3,132 sublevel checks, agreement of the two
endpoint-rank algorithms, and six rejected malformed inputs.

The independent [`audit.py`](audit.py) imports no target code, fixtures, or
certificate and uses different finite reductions:

- For each of 1,140 pairs `3<=m<=40`, `1<=x<=30`, it evaluates the complete
  affine coefficient vector in the free variables `v_2,...,v_{m-1}` on both
  sides.  Thus each checked pair covers all integer profiles, rather than a
  sample of them.  Signature digest:
  `7f84ac7fece15ad47226fc8a2bfde93633724f7d101e6bfd3707b97c8d5cb938`.
- A suffix-state dynamic program, rather than literal word enumeration,
  checks 276 reference identities through word length 47.  DP digest:
  `36749da9c3e0232fec45b6a5e9aa800644178a7ba1750feac2ca2efb7014de45`.
- An exhaustive box contains 117,180 formal profile/parameter cases.  It finds
  537 positive output excesses: 418 already violate the seed-size bound and
  119 force an endpoint-layer witness.  All 70,128 locally bounded cases are
  nonpositive and all 18 equality cases have the reference profile.
- Independently generated point sets `(i,pi(i))` exhaust all 1,352
  general-position permutation diagrams through seven points.  Convexity is
  tested by the Carathéodory criterion—whether a point lies inside a triangle
  of the others—not by the target's monotone-chain hull.  Across 7,648
  thresholds, 107,306 convex subsets, 67,624 sublevel tests, and 30,592
  blow-up parameter cases, every endpoint and local-bound conclusion holds.
  This is exhaustive for those permutation diagrams, not for all planar order
  types.

The smallest and hypothesis-breaking controls are explicit:

- `m=3` has the reference profile `(2,0)`, no layer sum, and exact equality.
- At an interior threshold there are two rank-one endpoints, but at the
  all-left boundary there is only one, demonstrating why `L=0,N` is excluded.
- Setting `x=0` makes `k=m`, so the asserted strict descent is unavailable.
- A determinant-positive shear separates repeated vertical coordinates while
  preserving all tested orientations.
- The formal profile `(2,6,0,0)` at `m=5,x=1` has endpoint-layer excess four
  with no seed-size excess.  Conversely `(2,3,0,0)` has a positive `V_2`
  deviation but total output excess `-8`; this checks that the proof uses only
  the correct one-way implication.

These finite checks exercise the indexing and boundary logic.  The universal
result still rests on the audited binary partition, summation-by-parts
identity, and hereditary extreme-point argument.

## Primary-source and literature audit

The complete open-access Baek--Balko SoCG 2025 paper was checked directly.
Section 6.2, Corollary 15 matches the imported formula and scope; Lemma 18 and
Theorem 19 contain the reference endpoint profile and its sharp construction.
The target credits these ingredients as prior work.  Its new mathematical
content is the positive excess decomposition, witness extraction, and equality
criterion.

Targeted live searches did not find those three statements elsewhere.  The
2026 journal metadata is public, but its full text was not available through
the checked endpoints.  Accordingly this review endorses mathematical
correctness and attribution to the accessible source, but makes no exhaustive
historical-priority claim.  The primary paper and current literature continue
to describe the unrestricted Erdős--Szekeres conjecture as open.

## Caveats

- The all-parameter proof is human-audited, not proof-assistant formalized.
- The review computation covers coefficient vectors for large finite
  parameter boxes and all small permutation diagrams, not all integers or all
  planar order types; those universal quantifiers are discharged by the
  written proof.
- The theorem assumes an interior threshold, `x>=1`, and the exact uniform
  Corollary-15 construction.  None of these restrictions may be dropped by
  analogy.
- The theorem proves a hereditary obstruction, not the Erdős--Szekeres
  conjecture, a new exact value, or a classification of extremal order types.
