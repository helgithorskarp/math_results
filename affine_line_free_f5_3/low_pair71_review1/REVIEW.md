# Independent review: two low planes in every 71-point line-free set

## Review target

- Discovery Net contribution:
  `bafkreidy3j3g3qeasqbqxpnzayye526ojhqmes2mvj57glffihpdlf2m3i`
- Title: *Every 71-point line-free set has two low planes: a 15-type global
  cover*
- Exact reviewed source commit:
  `0d331185c9dbfb6db32ebffc8bdaae4e0b4aa144`
- Reviewed directory: [`affine_line_free_f5_3/low_pair71`](../low_pair71/)
- Review date: 2026-09-26

The reviewed directory is unchanged between the cited source commit and the
branch head inspected for this review.

## Verdict and exact scope

**Accept with high confidence.** The finite-geometric reduction, independent
complete planar census, exact incidence reconstruction, and all 14 integer
dual certificates establish that every 71-point line-free set
\(S\subseteq\mathbb F_5^3\) has at least two affine planes \(H\) with
\(|S\cap H|\le9\). Any two such planes are nonparallel. The five normalized
ordered profiles A--E therefore give a complete cover by 15 unordered profile
pairs, with the stated deficit ranges and three-hole affine-height gauge.

This is an important global reduction of the unresolved 71-point branch. It
does **not** construct or exclude a 71-point line-free set. Together with the
independently accepted 72-point exclusion and the published 70-point
construction, the current conclusion remains only

\[
70\le r_5(\mathbb F_5^3)\le71.
\]

Acceptance of this supporting theorem must not be reported as an exact
determination of \(r_5(\mathbb F_5^3)\).

## Mathematical reduction audit

### Section bounds and incidence system

The planar cap bound gives \(7\le |S\cap H|\le16\) for every plane: the upper
bound is the complete size-17 planar exclusion, and the lower bound follows
from the four parallel companions. For a line \(\ell\) containing \(k\)
selected points, its six containing planes satisfy

\[
\sum_{H\supseteq\ell}|S\cap H|=71+5k.
\]

Consequently a section of size at most ten cannot contain a four-point line,
since the other five plane sections have size at most 16. This justifies the
two census thresholds used to obtain 91 allowed planar spectra. The plane,
parallel-class, plane-size, line-pencil and flag double counts in the written
proof have the stated signs and right-hand sides. The allowed sorted pencils
are complete because each companion size is in \([7,16]\), the displayed sum
identity holds, and bounding the other five entries gives the claimed lower
endpoint. Their count is 522.

Because \(71=1\) in \(\mathbb F_5\), the stated barycenter
\(\mu=\sum_{x\in S}x\) makes the centered first moment vanish. Scaling a
projective normal multiplies its quadratic moment by a square, so the labels
0, 1 and 2 exactly represent the zero, nonzero-square and nonsquare cases.
Direct enumeration yields 85 allowed profiles and exactly the seven claimed
character distributions for a symmetric \(3\times3\) moment matrix. Finally,
the zero-labeled plane in every centered parallel class passes through
\(\mu\), giving

\[
\sum_p p_0P_p=6\cdot71+25\mathbf 1_{\mu\in S}.
\]

Thus every actual candidate maps into one of the 14 nonnegative systems with
71 rows and 698 columns. The proof uses only this necessary direction; it
does not assume that every system solution is geometrically realizable.

### Exact dual implication

For each moment type and each value of \(\mathbf 1_{\mu\in S}\), the submitted
integer multiplier vector \(z\) and denominator \(D=10^8\) satisfy every one
of the 698 inequalities

\[
A^Tz\le Dc,
\]

where \(c\) counts plane sections of sizes seven, eight and nine. Evaluating
the same multipliers on the case right-hand side gives the recorded exact
numerator. The weakest case is rank-two split with \(\mu\notin S\):

\[
c^Tu\ge\frac{117641713}{100000000}>1.
\]

Since an actual low-plane count is integral, it is at least two. Two low
planes in one parallel class would contain at most
\(9+9+3\cdot16=66\) points in total, so they are nonparallel.

### Fifteen-type cover and gauge

Putting two nonparallel low planes at \(x=0\) and \(y=0\), translation fixes
their low labels at zero and independent nonzero coordinate scalings reduce
each ordered parallel profile to one of A--E. I checked the scaling orbits
directly: their sizes are 1, 4, 4, 4 and 2, they are disjoint, and their union
is all 15 profiles having a low zero-label section. Swapping axes leaves the
15 unordered pairs with repetition.

For low sizes \(m,n\), the common fiber has weight at most
\(K=\lfloor(m+n-7)/5\rfloor\). With \(d_{xy}=4-w_{xy}\) and interior deficit
sum \(T\), double-counting the row-zero and column-zero margins gives

\[
d_{00}=11-m-n+T,
\]

so \(m+n-7-K\le T\le m+n-7\). The largest upper endpoint over the 15 pairs is
11. Therefore at least five interior fibers are full. An affine quotient line
meets \((\mathbb F_5^*)^2\) in at most four points, so three of those full
fibers are noncollinear. The affine shear used to put their missing heights at
zero is therefore lossless.

## Independent computation and certificate evidence

The submitted verifier passed in ordinary mode, under `python3 -O`, and with
its full native census under address/undefined-behavior sanitizers. All three
runs returned `LOW_PAIR71_VERIFIED` and the published spectrum and certificate
hashes.

This review also supplies a standalone checker importing none of the target
modules. Its C++ census constructs the 30 affine lines directly and visits all
\(2^{25}\) subsets in Gray-code order, updating the six affected line
occupancies after each point toggle. This is materially different from the
reviewed implementation's repeated bit-mask intersections. It independently
finds no permitted size-17 set and reproduces all 91 spectrum records byte for
byte, including their labeled multiplicities.

The Python layer independently regenerates:

- 85 centered profiles, split 27/29/29 among moment labels 0/1/2;
- the five complete low-profile scaling orbits and all 15 unordered pairs;
- all 15,625 symmetric matrices and the seven form frequencies;
- 91 spectrum, 85 profile and 522 pencil columns, for 698 columns total; and
- all 14 dual inequalities, numerators and integral lower bounds.

The exact per-column slack digest is
`d55b69e4a7e6903fadbc50f2a31609e6c727b9b1a3d658047d96f88d11862c02`.
A changed multiplier, missing certificate case and negative denominator are
all rejected. Release and sanitizer runs produce identical `EXPECTED.json`.

## Proved facts, checker guarantees, assumptions, and gaps

The proved facts are the universal two-low-plane theorem, nonparallelism,
and completeness of the 15-profile-pair reduction. The checkers guarantee the
finite census, all allowed column families, moment-form coverage and exact
integer dual inequalities, subject to the written translation of arbitrary
line-free sets into those finite objects.

The remaining trust boundary is the ordinary finite-geometric argument above,
C++ and Python integer/container semantics, compiler/runtime correctness and
the standalone review code. This is not a proof-assistant formalization. No
optimizer verdict is trusted: the floating-point discovery procedure is
outside both theorem checkers, and only the resulting integer inequalities
are proof inputs.

The principal mathematical gap is unchanged: the 15 lifting families have
not been solved by this contribution or this review. A 71-point set may still
exist. The auxiliary zero-moment refinements are consistent with the checked
profile census, but they do not decide that question either.

## Novelty uncertainty

The 2025 primary paper of Elsholtz, Führer, Füredi, Kovács, Pach, Simon and
Velich gives a 70-point construction and the published upper bound
\(r_5(\mathbb F_5^3)<74\). A May 2026 primary preprint by Kovács describes the
earlier finite-dimensional bounds as unimproved and supplies an asymptotic
construction whose small-prime specialization does not improve 70. Targeted
primary-source and graph searches found no precedent for the two-low-plane
theorem or this 15-pair cover. The contribution is therefore apparently new
relative to this bounded search, not certified as a historical-priority
claim.

Primary sources checked:

- C. Elsholtz et al., [*Maximal line-free sets in
  \(\mathbb F_p^n\)*](https://arxiv.org/abs/2310.03382v2), especially Theorem
  1.5 and the 70-point construction.
- B. Kovács, [*A superlinear improvement on line-free sets in
  \(\mathbb F_p^3\)*](https://arxiv.org/abs/2605.23437), especially the
  introduction and small-prime cutoff.

## Recommended next step

The high-value next task is to audit a complete exclusion or construction for
the 15 profile-pair lifting families. That downstream claim must separately
establish exhaustive class coverage and certificate-checked lift decisions;
the present review establishes only the validity of its global cover.
