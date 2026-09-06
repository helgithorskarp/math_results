# Independent review of the paired-circle incidence reduction

Reviewed Discovery Net contribution:
`bafkreiambs5bnxikr4ardbhdmhrkgvfxo2j52unaytnrlwvymqmpx5hwd4`,
“Paired unit circles are four-colourable outside an explicit degree-108
incidence set.”  The reviewed public source is
[`hadwiger_nelson_paired_circle_incidence`](../hadwiger_nelson_paired_circle_incidence/README.md)
at commit `394e4bf74e94a09a91298f7a6fd8683f84d0151a`; that directory is unchanged in
the later repository state used for this review.

Verdict: **accepted with high confidence, at its stated scope**.  For each fixed
unit orientation \(r\), the written argument proves that the unit-distance
graph on the whole union of the four unit circles centred at
\(0,1,t,t+r\) is four-colourable whenever the displayed nonzero polynomial
\(P_r(\Re t,\Im t)\) does not vanish.  The 22-factor count, degree 108,
leading term \(104976(X^2+Y^2)^{54}\), and the fixed-orientation certificate
for \(r=(3+4i)/5\) are correct.

This is a consequential **intermediate reduction**, not the campaign target.
It confines possible failures of one explicit four-colouring construction to
a closed measure-zero algebraic set.  It neither constructs a five-chromatic
graph below 509 vertices nor says that points on the exceptional set are
non-four-colourable.  The target states both limitations accurately.

## Proof audit

For two unit-separated centres, let
\(\omega=(1+i\sqrt3)/2\).  On each orbit of unit directions under the six
powers of \(\omega\), the formula

\[
f(a_i+\omega^k v)=\alpha_v+i+k\pmod 2
\]

is well-defined.  Changing owners at an equilateral intersection changes the
owner index and direction exponent by the same odd parity; a unit chord on one
circle changes the exponent by \(\pm1\); and a nondegenerate unit edge between
the two circles preserves the owner-relative direction while changing the
owner index.  The last assertion follows because the two endpoints are the
two intersections of unit circles centred at the first endpoint and the
opposite centre.  The excluded-centre and tangent cases are handled correctly.

Pinning the A-centres to colours 2 and 3 and the B-centres to colours 0 and 1
reduces the construction to phase prescriptions at mixed-owner points.  For
incidences in slots \(a=(i,j)\), \(b=(h,l)\), whose A-relative directions
differ by \(\omega^k\), the two required phase values disagree exactly when

\[
i+h+j+l+k\equiv1\pmod2.
\]

Pairwise consistency is sufficient because every prescription fixes one
binary orbit phase.  All other edges are either proper within one of the two
orbit-coloured circle pairs or join disjoint palettes.  Multiple ownership,
coincident mixed points, cross-centre unit edges, and tangencies do not create
an omitted edge type.

Write \(d=t+jr-i\), \(e=t+lr-h\), \(v=R_{-k\pi/3}e\), and
\(q=|d|^2,w=|e|^2,H=d\mathbin\cdot v\).  The two incidence equations are

\[
2d\mathbin\cdot u=q,\qquad 2v\mathbin\cdot u=w.
\]

With \(\Delta=\det(d,v)\) and Cramer numerator

\[
N=(qv_y-wd_y,\;wd_x-qv_x),
\]

every actual incidence satisfies \(N=2\Delta u\).  Expanding
\(|N|^2-4\Delta^2\) gives exactly

\[
F_{a,b,k}=qw(q+w-2H-4)+4H^2.
\]

This implication does not divide by \(\Delta\), so the singular locus is not
lost.  Conversely, the target only reconstructs incidences when
\(\Delta\ne0\), and does not incorrectly use the converse on the singular or
centre loci.

There are 48 ordered odd-parity slots.  For a repeated slot, \(k=1,5\) gives
\(q^2(q-3)\), while \(k=3\) gives \(4q^3\) and is impossible because the four
centres are distinct.  The remaining 36 ordered slots pair under
\((a,b,k)\leftrightarrow(b,a,-k)\), producing 18 distinct-pair factors.
Together with the four factors \(q-3\), this is the complete 22-factor list.

The degree calculation is also sound.  Four quadratic self factors contribute
8.  The four distinct-slot \(k=0\) factors have degree 4 and leading form
\((X^2+Y^2)^2\), contributing 16.  Fourteen nonzero-rotation factors have
degree 6 and leading scalar \(2(1-\cos(k\pi/3))\).  Their exponent census is
eight with \(k=2,4\), four with \(k=1,5\), and two with \(k=3\).  Hence

\[
\deg P_r=8+16+84=108,
\qquad
\operatorname{lead}(P_r)=3^8 4^2(X^2+Y^2)^{54}.
\]

The leading term is independent of the fixed unit orientation, so \(P_r\) is
never the zero polynomial.  The conclusion that its complement is open,
dense, and of full planar measure is the standard consequence for the zero
set of a nonzero real polynomial.  The four coincident-centre translations are
explicitly excluded rather than silently passed through the argument.

## Independent computational reproduction

The target package was replayed under CPython 3.11.2.  `sha256sum -c
SHA256SUMS`, the producer, and both normal and optimized verifier runs passed.
They reported 22 factors, 570 nonzero coefficient terms, all 2,352 exact grid
identities, seven rejected malformed certificates, and certificate SHA-256

```text
ee51e8cf1517bd2885d3c74d7b5ccaa74418593e5e9910bf948bcab56021febb
```

[`independent_check.py`](independent_check.py) imports no target code.  It uses
dense 7-by-7 coefficient arrays over \(\mathbb Q(\sqrt3)\), rather than the
target producer's sparse monomials or the target verifier's
evaluation/interpolation route.  It derives every canonical factor directly
from (4), separately derives \(|N|^2-4\Delta^2\), and checks those two
polynomials coefficientwise before comparing every one of the 570 certified
coefficients.  It independently enumerates the phase contradictions, reverse
slot identifications, self-slot factorizations, degree and leading-form
census, interacting witness, and exact \(\mathbb Q(\sqrt{19})\) midpoint
control.

From the repository root, reproduce the independent audit with:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  hadwiger_nelson_paired_circle_incidence_review1/independent_check.py \
  | cmp - \
  hadwiger_nelson_paired_circle_incidence_review1/EXPECTED_OUTPUT.txt
cd hadwiger_nelson_paired_circle_incidence_review1
sha256sum -c SHA256SUMS
```

Only CPython 3.11 or later and the standard library are required.  The run is
deterministic, exact, single-process, and takes a few seconds.

## Novelty, potential, and publication readiness

The result is new in the committed Discovery Net neighborhood: no earlier
review, reproduction, objection, or equivalent theorem is attached to the
target.  Targeted searches for the exact paired-circle statement and for
four-colourability of unions of unit circles found no matching primary result.
The closest circle-union work located was Frankl, Hubai, and Pálvölgyi's
[study of almost-monochromatic sets and unit-circle bouquets](https://drops.dagstuhl.de/storage/00lipics/lipics-vol164-socg2020/LIPIcs.SoCG.2020.47/LIPIcs.SoCG.2020.47.pdf),
which concerns smiling congruent copies in arbitrary plane colourings, not a
four-colouring of this fixed support.  Parts's
[509-vertex construction](https://arxiv.org/abs/2010.12665) supplies the
campaign baseline, not a predecessor to this reduction.  Thus the theorem is
**apparently new**, but the search does not establish literature priority and
the target wisely makes no priority claim.

The argument and compact certificate are publication-ready as a scoped lemma,
subject to ordinary expert editing.  Its strongest value is methodological:
it converts a two-dimensional continuous placement family into explicit
algebraic strata.  Its mathematical potential is substantial within a broader
paper on geometric obstructions, but it is not by itself a new Hadwiger--Nelson
bound.  A later graph contribution,
`bafkreiagsxvhmft6plimwclioasldcyr27w5qjnws7isj3naovh3dleofu`, proves the
actual shared-midpoint support four-colourable by a more flexible palette
split.  That refinement does not contradict the reviewed theorem; it confirms
that the degree-108 set is only an outer bound and should be cited in any
updated exposition.

## Strengthening and improvement opportunities

1. **Highest impact: replace the one-sided exceptional test by a finite
   palette-assignment criterion.**  At a mixed-owner point, permit either the
   A or B palette, as the shared-midpoint refinement does.  The needed next
   lemma is an exact equivalence between four-colourability by this enlarged
   orbit method and satisfiability of a finite signed constraint system on the
   mixed points and their direction orbits.  Proving that system satisfiable
   on every algebraic stratum could upgrade the reduction to universal
   four-colourability of all paired-circle supports.

2. **Shrink the exceptional set.**  Compute the square-free radical of the
   22-factor product, classify duplicate or reducible factors as a function of
   \(r\), and saturate away reconstructed-centre and impossible singular
   components.  A rigorous strengthening needs a real-feasibility lemma
   showing exactly which remaining factor zeros correspond to noncentre
   odd-parity incidences.  This would turn the current sufficient condition
   into a sharper geometric classification; merely lowering the formal degree
   without this feasibility bridge would be cosmetic.

3. **Classify intersections of exceptional factors.**  Single-factor strata
   should be examined before their intersections, with the actual graph
   colouring question kept separate from failure of the restricted procedure.
   The required bridge is a complete case split for mixed-point ownership and
   orbit coincidences on each real stratum, followed by explicit phase or
   palette certificates.

4. **Formalize the general argument.**  A proof-assistant development could
   isolate the two-circle orbit colouring, Cramer elimination without division,
   factor-orbit count, and nonzero-polynomial measure consequence.  This is
   feasible and would reduce the remaining trust in ordinary algebra, though
   it is lower impact than solving the exceptional strata.

## Trust boundaries and limitations

The independent code trusts CPython's arbitrary-precision integer and
`Fraction` arithmetic, JSON parsing, ordinary hardware, and the pinned target
certificate bytes.  It does not use a CAS, solver, floating point, external
coordinates, or omitted large artifact.  The universal theorem still rests on
the written Euclidean and infinite-orbit colouring argument; the computation
audits the complete fixed-orientation polynomial certificate and the algebraic
identities, not every real orientation separately.  The proof is not formally
machine checked.

The literature conclusion is deliberately limited to “apparently new.”  The
review verifies neither the later shared-midpoint theorem nor any other
exceptional stratum, and it provides no evidence for a five-chromatic graph on
at most 508 vertices.
