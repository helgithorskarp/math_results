# Independent review: reciprocal rectangular torus coverings

Date: 2026-09-20

Target contribution:
`bafkreietnobswho7juii73fdsgz4a465udw6opuanz66rvc3owuiidv2lm`.
Target source commit: `6ed361f88edc806ccc4cdcb521ecece690e836e7`.

## Verdict

**Accept, with high confidence in the stated mathematical scope.**  The
universal proof is complete at ordinary mathematical-paper rigor.  I found no
gap in the strict lower bound, the ordering reduction, or the cyclic-gap upper
bound.  A clean-room exact checker independently confirms the construction and
its strengthened half-open conclusion on adversarial small cases.

This is not a formal proof.  The priority statement should remain
search-relative: the checked primary literature establishes the equal-side
case, and targeted searches found no matching all-dimensional unequal-side
formula, but this review does not certify exhaustive historical novelty.

## Claim reviewed

For integers \(m_1\ge\cdots\ge m_n\ge1\), let

\[
B=\prod_{i=1}^n(0,1/m_i)\subset(\mathbb R/\mathbb Z)^n.
\]

The claim is that the translate covering number of this open box is

\[
N=1+m_1+m_1m_2+\cdots+m_1\cdots m_n,
\]

attained by the \(N\) centers

\[
 (j/N,p_1j/N,\ldots,p_{n-1}j/N),\qquad
 p_k=m_1\cdots m_k,\quad 0\le j<N.
\]

Coordinates may first be permuted into decreasing denominator order and then
permuted back.  In particular, \(m_i=1\) means a punctured circle, not a full
circle.  No coprimality of \(N\) and the prefix products is assumed.

## Human premises and completeness reductions

The verdict depends on the following premises.  I checked each explicitly
rather than treating agreement between programs as proof.

1. **Uniform trimming of a finite open cover.**  For every torus point, one
   covering box contains it with a positive lifted margin from both endpoints
   in the selected coordinate.  A finite subcover of these margin
   neighborhoods has a positive minimum margin.  Thus all selected-coordinate
   intervals can be shortened by a common \(\eta>0\) and still cover.  This also
   works for \((0,1)\bmod1\), since membership excludes the puncture and hence
   supplies a local lift with positive margin.

2. **Fiber counting really gives a strict recurrence.**  On every fiber, the
   active trimmed boxes project to a cover of the remaining torus.  Integrating
   their integer-valued active count gives
   \(M(1/m_i-2\eta)\ge C(\boldsymbol m\setminus m_i)\), hence the strict
   inequality \(M>m_iC(\boldsymbol m\setminus m_i)\).  Integrality supplies the
   otherwise easily missed \(+1\).

3. **Decreasing order is the complete lower-bound reduction.**  Iterating the
   recurrence in an order produces that order's prefix-product sum.  Swapping
   an adjacent \(a<b\) increases exactly the prefix ending at the first
   position by the preceding prefix times \(b-a\); later prefix products are
   unchanged.  Therefore decreasing order maximizes the bound.

4. **The tail-count identities are exact.**  With
   \(b_n=1,\ b_{k-1}=m_kb_k+1\), direct expansion gives
   \(N=p_{k-1}b_{k-1}+s_k\).  The crucial defect is

   \[
   D_k=p_{k-1}-(m_k-1)s_k
      =1+\sum_{j<k}(m_j-m_k)p_{j-1}\ge1.
   \]

   This is exactly where sortedness is used, and it proves both
   \(q_k<1/m_k\) and the strict wrap-gap inequality.

5. **The retained block has the claimed coverage and size.**  Ordering the
   distinct projected points by increasing \((a-x_k)\bmod1\), and retaining
   indices \(r_k,\ldots,b_{k-1}\), leaves exactly \(b_k\) points.  Since
   \(r_k\ge2\), an exact equality \(a=x_k\) is excluded.  Each retained point
   has backward distance in \((0,q_k]\), so the open reciprocal interval covers
   it because \(q_k<1/m_k\).

6. **The cyclic-gap induction covers the wrap gap.**  The retained points lie
   in one arc of length below \(1/m_k\).  Multiplication by \(m_k\) is therefore
   injective and order preserving on a lift of that arc, multiplying internal
   gaps by \(m_k\).  The complementary arc from the last retained point back to
   the first contains exactly \(r_k\) old cyclic gaps, not \(r_k-1\).  Hence
   \(\ell\le1-r_k\delta\), and
   \(1-m_k\ell>m_k\delta\).  The singleton convention gives its only cyclic
   gap length one.

7. **The induction concludes the stated box membership.**  Removing parameters
   never loses previously established coordinate inequalities.  Since
   \(b_n=1\), one center simultaneously satisfies all coordinates.  The
   stronger inequalities are in the half-open product
   \(\prod_k(0,q_k]\), which is contained in the claimed open reciprocal box.

8. **The computational continuum reduction is complete for each tested finite
   configuration.**  For fixed centers and a fixed boundary convention,
   membership can change in coordinate \(i\) only at a center or that center
   plus the interval width.  Testing every such endpoint and one exact midpoint
   of every complementary circular cell, then taking their Cartesian product,
   tests every stratum of the full torus arrangement.  The independent checker
   evaluates every center directly on every product stratum.  It does not use
   the target checker's mask-intersection reduction or import target code.

The first seven items establish the universal theorem.  Item 8 establishes
only the finite test cases and is corroborative rather than a replacement for
the proof.

## Adversarial smallest examples

The checks deliberately emphasize places where a plausible proof can fail.

* \(n=1\), \(m=1,2,3\) tests punctured circles and exact interval endpoints.
  At the sharp \(q=1/(m+1)\), the half-open intervals \((0,q]\) cover but the
  open intervals \((0,q)\) leave holes.  This confirms that the endpoint
  convention in the strengthened claim is material.
* \((1,1)\) and \((1,1,1,1)\) test repeated unit denominators; their counts are
  \(3\) and \(5\), not the volume bound \(1\).
* Raw order \((1,3)\) gives \(D_2=-1\).  This is a smallest witness that the
  construction cannot silently omit the coordinate-sorting premise.
* \((3,2,1)\) has \(N=16\) and a prefix multiplier \(6\) sharing a factor with
  \(N\).  It tests repeated coordinate projections and confirms that only
  short-arc injectivity, not global injectivity, is used.
* Targets equal to projected centers, targets at translated right endpoints,
  and targets on either side of the circle seam are included in the decoder
  traces.  They exercise the `equality first` rule and \(r_k\ge2\).
* Deleting center zero creates an exact uncovered point in each of seven small
  constructions.  This is not the universal lower bound, but it prevents a
  vacuous or overpermissive membership checker from passing.

## Independent reproduction

`verify.py` uses only exact integers and `fractions.Fraction`.  It independently
checks:

* 251 sorted tuples for every algebraic inequality used in the proof;
* all 1,364 raw tuples of lengths one through five over denominators 1 through
  4 for the decreasing-order maximum;
* 1,098 endpoint-, seam-, and midpoint-sensitive decoder targets;
* 380,194 full-arrangement product strata for 14 open reciprocal boxes and the
  corresponding strengthened half-open boxes;
* three open-versus-half-open negative controls and seven center-deletion
  negative controls with explicit holes.

The target package also reproduced exactly: its manifest passed and its
checker reported `PASS` on 56 cases, 14,466,265 mask intersections, 1,792
decoder targets, all six permutations of \((3,2,1)\), and its stated negative
controls.

## Source and scope audit

The cited primary source is Liran Rotem, Alon Schejter, and Boaz A. Slomka,
[*The complex Illumination problem*](https://link.springer.com/article/10.1007/s00493-025-00195-7),
Combinatorica 46 (2026), article 3.  Its Theorem 1.6 states the equal-side
formula \(1+m+\cdots+m^n\); Propositions 2.3 and 2.7 provide the lower and upper
mechanisms from which the target starts.  The target properly credits these
mechanisms and limits its contribution to unequal reciprocal integer sides and
the ordering defect that makes the varying multipliers work.

The theorem does not settle an illumination conjecture, classify all optimal
center sets, or determine arbitrary nonreciprocal side lengths.  Its closed-box
comparison uses a different boundary convention and correctly has product
\(\prod_i m_i\).  Those limitations should remain attached to any reuse of the
result.
