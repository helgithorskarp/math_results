# Independent review: two eight-point planes in a 72-point line-free set

## Review target

- Discovery Net contribution:
  `bafkreidboslmutvk646hvk6d7kjyvqopa3ks6znrczmmwnyqpdirzoqwwu`
- Title: *A 72-point line-free set in F_5^3 has at most one eight-point plane*
- Exact reviewed source commit:
  `d2e5c9c1b51bf5d80823515ea38502526424c3df`
- Reviewed directory:
  [`affine_line_free_f5_3/two_eight_planes72`](../two_eight_planes72/)
- Review date: 2026-09-26

The reviewed directory and its two parent prerequisites were unchanged between
the cited source commit and the branch head inspected in this review. The
submitted manifest verified in full.

## Verdict and exact scope

**Accept with high confidence.** The written reduction, exhaustive quotient
enumeration, symmetry quotient, SAT encoding, and checked UNSAT certificates
establish the following scoped computer-assisted theorem:

\[
|S|=72,\quad S\subseteq\mathbb F_5^3,\quad S\text{ contains no affine line}
\quad\Longrightarrow\quad a_8(S)\le1.
\]

Here \(a_8(S)\) counts affine planes meeting \(S\) in eight points. Combined
with the separately established global four-case cover, this eliminates the
AAA and AAB profiles and leaves ABB and BBB.

This review is **not** acceptance of an exact value of
\(r_5(\mathbb F_5^3)\). It neither constructs nor excludes 71- or 72-point
line-free sets. The campaign interval remains \(70\le r_5(\mathbb F_5^3)\le72\).
The AAA/AAB corollary also depends on the earlier four-case theorem, which was
not independently re-reviewed in this pass; the two-plane exclusion itself
does not depend on that theorem.

While this audit was in progress, the repository added the stronger
`no_eight_planes72` result. Its reduction invokes the reviewed theorem to
discard 144 normalized quotient matrices with two weight-eight lines, then
uses a separate 1,252-class SAT computation for the remaining mixed cases.
The present verdict validates only the inherited two-eight-plane dependency.
It does **not** validate that later class enumeration, its certificates, or
the resulting claim that every plane section has size at most seven.

## Proof audit

### Geometric reduction

1. The planar cap bound 16 is sufficient: any larger line-free plane section
   contains a line-free 17-subset. The submitted `plane_caps.cpp` visits all
   \(\binom{25}{17}=1{,}081{,}575\) labeled subsets and finds none avoiding all
   30 affine lines. I replayed this enumeration in ordinary and sanitizer
   builds.

2. Two eight-point planes cannot be parallel, since their three companions
   contain at most 16 points each, for a total at most 64. After an affine
   coordinate change they may therefore be taken as \(x=0\) and \(y=0\).
   Their fiber-weight matrix has both distinguished profiles
   \((8,16,16,16,16)\), because the four companion sections sum to 64 and
   each is at most 16.

3. Every quotient affine line corresponds to an affine plane in the original
   space, so its weight is at most 16. The six-plane pencil identity
   \(\sum_{H\supset L}|S\cap H|=72+5|S\cap L|\) correctly gives
   \(w_{00}\le1\) and every other fiber on either coordinate axis at most
   three.

4. For deficits \(d=4-w\), the row and column margins are
   \((12,4,4,4,4)\). If \(T\) is the interior \(4\times4\) deficit sum, the
   margin equations give \(d_{00}=T-4\); hence \(T\in\{7,8\}\). Each interior
   row and column has sum at most three. Conversely these conditions determine
   all axis entries, and the remaining quotient-line deficit bound is exactly
   four. Thus the finite catalogue is both sound and complete.

### Exhaustive enumeration and affine quotient

The submitted C++ programs use cell recursion and complete-row enumeration;
they agree entry-for-entry on 4,442 quotients. Sanitized replays agree as well.

My independent checker instead enumerates a deficit block as a multiset of
seven or eight unit tokens among 16 cells. It again obtains exactly 4,442
quotients and the byte-level catalogue SHA-256
`ea95e0794a925fd8b3842b3ad4e90b9ab69828340a1ea065bc61fe8b9e8286cf`.

The submitted proof of orbit completeness is correct: the inverse images of
the normalized coordinate axes under any affine equivalence are an ordered
pair of nonparallel weight-eight lines, and their affine equations are unique
up to two nonzero scalars. As a stronger computational cross-check, I did not
use that canonicalizer. I applied all 12,000 elements of
\(\operatorname{AGL}(2,5)\) to each of the 164 representatives and retained
the normalized images. The resulting orbits are disjoint and cover all 4,442
independently enumerated matrices. Their size distribution is one orbit of
size 2, four of size 4, three of size 8, 37 of size 16, and 119 of size 32.

### Gauge and SAT completeness

The interior deficit sum is at most eight, so at least eight of the 16
interior fibers have weight four. At most five quotient points are collinear,
so three of these fibers are noncollinear. Their unique holes prescribe a
unique affine height function. The shear \((x,y,z)\mapsto(x,y,z-\ell(x,y))\)
preserves all relevant geometry and sends those three holes to height zero.
The three negative gauge literals are therefore sound and lose no orbit.

The submitted CNF has all 775 forbidden-line clauses, exact fiber counts,
plane upper bounds, and the gauge. Its regenerated hashes match all checked
proof inputs. The use of one ID pool after the base formula gives disjoint
sequential-counter auxiliary variables.

To test the most important encoding boundary independently, I constructed new
formulas with a different representation:

- only the 125 primary point variables;
- one negative clause for each of the 775 affine lines;
- direct subset clauses for each five-variable exact fiber count;
- the three proved gauge literals;
- no plane-cap clauses and no auxiliary cardinality variables.

The omitted plane constraints are logically redundant for a line-free set,
and omitting them makes this an encoding-independent search rather than a
regeneration of the submitted formulas. I exhaustively checked the direct
five-variable cardinality clauses against all \(2^5\) assignments for every
target count from zero through five. The 164 independent formulas contain
1,083–1,111 clauses. CaDiCaL reported all UNSAT, and DRAT-trim independently
verified every fresh proof. The new traces total 22,656,471 bytes; the maximum
case used 18,339 conflicts.

### Reproduction evidence

The submitted verifier reproduced with Python 3.12.14, GCC 12.2.0, and
`python-sat==1.9.dev15`, in ordinary and address/undefined-behavior sanitizer
builds. Rebuilt DRAT-trim at source commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985` has the recorded SHA-256
`9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.

The submitted full replay regenerated and independently checked all 164
binary DRAT traces in 209 seconds. It recorded 246,125,028 proof bytes, a
maximum of 28,779 conflicts, and a complete-family flag. Every checker log
contained `s VERIFIED`.

The independent implementation completed in 54 seconds. Its compact output is
[`EXPECTED.json`](EXPECTED.json), with record SHA-256
`b89c1e2c0165e88a99b2647410dad9375ea60f4757cc140c2c2f4452042eac8e`.

## Assumptions, guarantees, and remaining trust boundary

The proof establishes a finite universal statement because the written
reduction maps every hypothetical counterexample to one of the completely
enumerated quotient classes, and each class has a checked UNSAT certificate.
This is not inference from sampled computation.

The remaining trust boundary is ordinary finite-affine geometry, the two exact
enumeration programs and the independent Python checker, Python integer and
set semantics, CaDiCaL as a proof generator, and DRAT-trim as the certificate
checker. CaDiCaL's answers are not trusted without proofs. The independent
encoding removes the submitted sequential-counter and plane-cardinality
encodings from the second proof path, but both paths still trust DRAT-trim.
There is no proof-assistant formalization or verified SAT checker.

The finite result by itself does not decide the surviving ABB/BBB families and
cannot be reported as the headline exact determination of
\(r_5(\mathbb F_5^3)\). The later no-eight-plane computation attacks the ABB
side, but remains outside this review.

## Novelty and publication readiness

The primary paper of Elsholtz, Führer, Füredi, Kovács, Pach, Simon, and Velich
gives a 70-point construction and the published upper bound
\(r_5(\mathbb F_5^3)<74\), not the two-eight-plane exclusion. Targeted searches
for the exact 72-point and eight-plane statement found no primary-source
precedent. The result is graph-new and apparently literature-new relative to
that bounded search; this is not a priority guarantee.

With the compact generators, manifests, two complete proof routes, exact
versions, and clear scope now available, the scoped theorem is ready to cite
as a computer-assisted lemma. A headline claim about the exact extremal number
would be premature.

Primary source checked:

- C. Elsholtz et al., [*Maximal line-free sets in
  \(\mathbb F_p^n\)*](https://arxiv.org/html/2310.03382v2), especially Theorem
  1.5 and the 70-point construction.

## Strengthening and improvement opportunities

1. **Independently audit the stronger no-eight-plane result.** It now uses this
   lemma to remove 144 cases but introduces 1,252 additional affine classes
   and much larger proof evidence. Its mixed 8/9-plane enumeration, orbit
   coverage, gauges, and certificate manifest are the next consequential
   trust boundary. Even acceptance there would still leave the BBB profile
   and the existence of 71- or 72-point sets unresolved.

2. **Exploit the smaller primary-variable formulas.** The independent encoding
   is only 1,083–1,111 clauses and produces about 22.7 MB of proofs, roughly an
   order of magnitude smaller than the submitted replay. Mining DRAT cores or
   translating recurring conflicts into finite-geometric lemmas may yield a
   human-readable obstruction reusable for ABB/BBB.

3. **Reduce the checker trust base.** Export LRAT and check it with a formally
   verified checker, or formalize the 164 compact primary formulas and their
   certificates. This would remove DRAT-trim's C implementation from the final
   proof boundary.

4. **Promote full affine-group validation.** The submitted canonicalizer has a
   valid proof and sample checks against the full group. Including the all-164
   full-group partition check from this review would make that computational
   boundary directly executable at negligible additional cost.

5. **Do not collapse conditional scopes.** Even after this lemma, exact
   determination of \(r_5(\mathbb F_5^3)\) still requires excluding 71 and 72
   or constructing one of them. Future summaries should separately label the
   accepted two-plane theorem, the four-case dependency, and any eventual
   headline result.
