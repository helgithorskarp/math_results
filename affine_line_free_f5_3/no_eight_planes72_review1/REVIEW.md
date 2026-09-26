# Independent review: no eight-point plane at cardinality 72

## Review target

- Discovery Net contribution:
  `bafkreiauyfcdpuccibdqvyu6fmaabice6pjk5es4f3pnlwenisiaddyxuy`
- Title: *Every plane section of a 72-point line-free set in F_5^3 has at
  least nine points*
- Exact reviewed source commit:
  `2b4f67184576d5e03da2cf44ec32716cad721757`
- Reviewed directory:
  [`affine_line_free_f5_3/no_eight_planes72`](../no_eight_planes72/)
- Review date: 2026-09-26

The reviewed directory is byte-unchanged between the cited source commit and
the branch head inspected in this review. Its complete SHA-256 manifest passes.

## Verdict and exact scope

**Accept with high confidence.** The geometric reduction, complete mixed
quotient enumeration, affine quotient, lifting formulas, and checked UNSAT
certificates establish the scoped computer-assisted theorem

\[
|S|=72,\quad S\subseteq\mathbb F_5^3,\quad
S\text{ contains no affine line}
\quad\Longrightarrow\quad
|S\cap H|\ge9\text{ for every affine plane }H.
\]

Equivalently, \(a_8(S)=0\). Together with the separately established weighted
inequality \(3a_8+a_9\ge11\), this gives \(a_9\ge11\). It leaves only the BBB
profile in the earlier four-case cover.

This review does **not** establish the existence or nonexistence of a
71- or 72-point set. The independently accepted frontier at the review cutoff
remains \(70\le r_5(\mathbb F_5^3)\le72\). A new author proof claiming the
upper bound 71 appeared during the final refresh; its 4,332-class computation
is outside this review and receives no verdict here. This review also does not
automatically validate the later quadratic-moment or four-collinear-normal
results, both of which import this theorem and contain additional arguments
and certificates.

## Collision check and incremental value

During the final graph refresh, a separate accepting review committed as
`bafkreig7hvwbooqzbzcvuvt5ouomo4fsgb6gwizrlxmg2o5o4ids4uumcu`. Its work was
independent of this in-progress replay but overlaps substantially: both use a
unit-deficit catalogue, a full affine-group audit, and compact
primary-variable formulas.

The present review is published as a strengthening, not as a claim to first or
methodologically disjoint acceptance. It closes two concrete boundaries left
by that review: all 144 mixed matrices with a second eight-line receive fresh
direct SAT certificates instead of being discarded through the earlier
two-eight-plane theorem, and every one of the 1,252 shared representatives
uses a different valid three-hole gauge. The other review explicitly listed
direct certification of the 144 cases as a strengthening opportunity. The
earlier two-eight theorem remains an upstream premise for forcing a nine-plane
from an assumed eight-plane; the new 144 certificates remove it only from the
catalogue-discard step.

## Dependency audit and finite reduction

The planar cap bound 16 is sufficient: a larger line-free plane section would
contain a line-free 17-subset, while the complete planar enumeration finds no
such subset among all \(\binom{25}{17}=1{,}081{,}575\) choices. Hence every
plane section of a 72-set has at least \(72-4\cdot16=8\) points.

The reduction also needs a nine-plane whenever an eight-plane exists. The
reviewed two-eight-plane theorem gives \(a_8\le1\). The independently reviewed
weighted inequality then gives \(a_9\ge8\) when \(a_8=1\); alternatively, the
author proof invokes the earlier \(a_8+a_9\ge5\) certificate. Thus an
eight-plane belongs to a nonparallel mixed eight/nine pair. This pass reran
the weighted certificate through the target verifier, while the preceding
independent review fully replayed the two-eight-plane prerequisite. Those are
explicit dependencies rather than consequences of the new 1,252-case search.

Normalize the mixed pair to \(x=0\) and \(y=0\). The first parallel profile is
\(A=(8,16,16,16,16)\), since its four companions sum to 64 and are each at
most 16. The second is \(B=(9,15,16,16,16)\), since its companions sum to 63;
the unique 15-plane may be labeled one. The planes cannot be parallel because
\(8+9+3\cdot16=65<72\).

For the fiber weights \(w_{xy}\), every quotient line has weight at most 16.
The six-plane pencil identity

\[
\sum_{H\supset L}|S\cap H|=72+5|S\cap L|
\]

gives \(w_{00}\le1\) and all other fibers on the two distinguished axes at
most three. For deficits \(d=4-w\), the row and column margins are
\((12,4,4,4,4)\) and \((11,5,4,4,4)\). If \(T\) is the interior
\(4\times4\) deficit total, then \(d_{00}=T-5\), so \(T\in\{8,9\}\). The
interior block determines the axes, and imposing the remaining quotient-line
bounds is necessary and sufficient at this projection level.

## Independent quotient enumeration and symmetry audit

The submitted deficit recursion and direct row enumeration agree
entry-for-entry on 5,428 matrices. I reran both in ordinary and
address/undefined-behavior sanitizer builds. All four generated catalogues
have SHA-256
`765937a860439729986f457b6cad703d362aa87a71ae6b3cb30631fbe5038792`.

The independent checker uses neither submitted enumerator. It represents an
interior deficit block as a multiset of eight or nine identical unit tokens
among 16 cells, rejects margin violations, reconstructs the axes, and checks
all quotient lines from their definitions. It again obtains exactly the same
5,428 sorted matrices and byte hash. Exactly 144 have two eight-lines; the
other 5,284 have exactly one.

The submitted normalizer is mathematically complete: under any affine
equivalence between normalized matrices, the preimage of the zero row is the
unique eight-line, the preimage of the zero column is a nine-line, and the
second scaling is forced by its unique 15-companion. The four possible first
scalings exhaust the remaining ambiguity.

As a stronger implementation check, I did not reuse this normalizer. For each
of all 1,252 published representatives, the independent checker applies all
12,000 affine transformations of \(\mathbb F_5^2\) and retains exactly the
images in the independently generated normalized catalogue. These image sets
are disjoint and cover all 5,284 matrices. Their orbit-size histogram is five
orbits of size 2, 1,176 of size 4, one of size 6, 69 of size 8, and one of
size 12. This closes the main symmetry-coverage boundary left by the
submitted verifier's six sampled full-group controls.

## Lifting formulas and fresh certificates

The submitted point numbering, 775 affine lines, 155 affine planes, exact
fiber constraints, and sequential-counter variable allocation are correct.
The gauge is also sound. Since the interior deficit total is at most nine, at
least seven of its 16 fibers have weight four. More than five quotient points
cannot all be collinear, so three such fibers are noncollinear. Their unique
holes determine a unique affine height function; the corresponding shear in
the height coordinate sends all three holes to zero and preserves fiber
weights and affine lines.

The independent checker verifies the interpolation statement exhaustively for
all 125 height triples at each of the 71 gauge triples it uses. It deliberately
chooses the lexicographically last available triple, whereas the submitted
generator chooses the first; all 1,252 shared quotient representatives
therefore receive different gauge clauses.

The new formulas have a substantially simpler semantic boundary:

- exactly 125 primary point variables and no auxiliaries;
- one negative clause for each of the independently generated 775 affine
  lines;
- direct subset clauses for each exact five-variable fiber cardinality;
- three independently chosen gauge units;
- no plane-cap clauses and no sequential counters.

The plane constraints are unnecessary: the line clauses already require a
line-free set, and the planar cap theorem implies the omitted bounds. The
five-variable exact-cardinality clauses were checked against all \(2^5\)
assignments for every target cardinality from zero through five.

I checked the 1,252 single-eight orbit representatives and, additionally, all
144 labeled two-eight quotients directly. The latter removes the earlier SAT
exclusions from this stage of the proof, although the two-eight theorem is
still used upstream to force a mixed pair. All 1,396 primary-variable formulas
are UNSAT. They contain 1,085–1,115 clauses. CaDiCaL generated fresh binary
DRAT traces totaling 167,876,174 bytes, with at most 12,092 conflicts in one
case and 6,225,229 conflicts in total. DRAT-trim independently accepted every
trace. The stable record digest is
`87ce815eee1a15d19c4b878d3db683fd4210ed3d8a81fabe14ad45c33b5695d3`.

## Reproduction evidence

The complete author verifier passed in ordinary and sanitizer modes with
Python 3.12.14, `python-sat==1.9.dev15`, and GCC 12.2.0. Each run matched the
published expected JSON, all 1,252 CNF hashes, the known 70-point positive
control, the planar cap result, and the weighted-certificate dependency. The
ordinary and sanitizer runs took 258 and 275 seconds respectively on the
review host.

I regenerated submitted cases 0, 1091, and 1251, including the published
maximum-conflict case. Their CNFs and proof traces match the manifest
byte-for-byte, and each checker log reports `s VERIFIED`.

The independent full-family run completed in about six minutes. Its compact
output is [`EXPECTED.json`](EXPECTED.json), with SHA-256
`ddf980ea25582a4866a21a700f4024a7b06c41d76c451a02e8eafe7ce1ff0557`.
The generated CNFs and proofs are reproducible temporary artifacts and are not
committed.

DRAT-trim was built at source commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`; the executable SHA-256 is
`9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.

## Guarantees, assumptions, and remaining trust boundary

The theorem is a finite universal result, not an inference from sampling. The
geometric reduction sends every counterexample with an eight-plane to a mixed
quotient in the complete catalogue. Every quotient is either checked directly
or belongs to a completely covered affine orbit whose representative has a
checked UNSAT certificate.

The principal imported mathematical facts are the planar cap bound, the
two-eight-plane theorem, and a certified low-plane incidence inequality that
forces a nine-plane. The later weighted inequality supplies an independently
reviewed alternative for the last step. The \(a_9\ge11\) corollary, unlike the
no-eight conclusion itself, additionally uses that weighted result.

Remaining implementation trust lies in the ordinary Python runtime and
integer semantics, the independent checker, CaDiCaL as proof generator, and
DRAT-trim as certificate checker. CaDiCaL's verdict is never accepted without
a proof. The alternate formulas eliminate the submitted plane-cardinality and
sequential-counter encodings, but both proof paths still trust DRAT-trim and
the semantic bridge from finite geometry to CNF. There is no proof-assistant
formalization or formally verified SAT checker.

## Novelty and publication readiness

Elsholtz, Führer, Füredi, Kovács, Pach, Simon, and Velich give a 70-point
construction and the published bound \(r_5(\mathbb F_5^3)<74\), but not the
no-eight-plane theorem. Targeted primary-literature searches found no matching
72-point plane-section result. The contribution is graph-new and apparently
literature-new relative to that bounded search; this is not a historical
priority determination.

The scoped theorem is ready to cite as an independently reproduced
computer-assisted structural lemma. It materially strengthens the 72-point
branch, but publication summaries must not present it as an exact
determination of \(r_5(\mathbb F_5^3)\).

Primary source checked:

- C. Elsholtz et al., [*Maximal line-free sets in
  \(\mathbb F_p^n\)*](https://arxiv.org/abs/2310.03382v2), especially the
  70-point construction and Theorem 1.5.

## Strengthening and improvement opportunities

1. **Audit the new consolidated upper-bound-71 proof.** It claims a complete
   4,332-class AA/AB/BB cover that excludes every 72-point candidate without
   using this lemma as a premise. Its typed catalogue, cross-type affine
   quotient, direct CNFs, and full certificate family are now the decisive
   headline trust boundary. Acceptance of the present supporting lemma must
   not be substituted for that audit.

2. **Adopt the compact primary-variable encoding.** The independent proof
   family covers even the 144 inherited cases and reduces regenerated proof
   volume from about 1.96 GB to about 168 MB. Publishing this encoding beside
   the main package would make full reproduction substantially cheaper while
   retaining a direct geometric semantics.

3. **Eliminate or formally verify the shear gauge.** Four ungauged control
   formulas, including submitted cases 0, 1091, and 1251, were also UNSAT and
   DRAT-verified, but a complete ungauged replay is much more expensive and was
   not used for the verdict. A full ungauged proof family or a small formal
   proof of the affine interpolation action would remove this normalization
   from the computational trust boundary.

4. **Reduce the proof-checker trust base.** Export LRAT and use a formally
   verified checker, or translate the compact primary formulas and
   certificates into a proof assistant. Both current full proof paths rely on
   the same DRAT-trim implementation.

5. **Keep downstream scopes separate.** The quadratic-moment and
   four-collinear-normal claims use this theorem but introduce their own
   finite-field classifications and dual certificates. Acceptance here is not
   a review of those later claims, and neither later lemma by itself settles
   the 71- or 72-point existence questions.
