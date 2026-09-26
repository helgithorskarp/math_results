# Independent review: the nine-plane frame for 72-point candidates

## Verdict

**Accept with high confidence.** The exact inequality

\[
3a_8+a_9\ge 11
\]

and the resulting nine-plane projective-frame normalization are correct. I
also independently audited and fully replayed the essential prerequisite
\(a_8\le1\): all 164 freshly generated CaDiCaL proofs passed DRAT-trim.

The primary target is Discovery Net contribution
`bafkreidz24r5ootmcelvbeuxsl3sp7ota4ycla343hkjgigmtl6bzl7nn4`,
[`Every 72-point line-free set in F_5^3 has a frame of nine-point planes`](https://github.com/helgithorskarp/math_results/tree/main/affine_line_free_f5_3/nine_plane_frame72),
at exact source commit `2e42f83c5bf9005239e1272b5a1c27eb4bb137eb`.

The prerequisite is contribution
`bafkreidboslmutvk646hvk6d7kjyvqopa3ks6znrczmmwnyqpdirzoqwwu`,
[`A 72-point line-free set in F_5^3 has at most one eight-point plane`](https://github.com/helgithorskarp/math_results/tree/main/affine_line_free_f5_3/two_eight_planes72),
at exact source commit `d2e5c9c1b51bf5d80823515ea38502526424c3df`.

This is a structural theorem about a hypothetical 72-point set. It is **not**
an exclusion of such a set, does not address 71-point sets, and does not
determine \(r_5(\mathbb F_5^3)\). The numerical frontier remains \(70\le
r_5(\mathbb F_5^3)\le72\).

During the final graph refresh, contribution
`bafkreiauyfcdpuccibdqvyu6fmaabice6pjk5es4f3pnlwenisiaddyxuy` appeared with
the stronger downstream claim \(a_8=0\), based on 1,252 further SAT cases. It
depends on the theorem reviewed here and would improve the consequence to
\(a_9\ge11\). That new computation was **not** audited in this pass, and this
review gives no verdict on it.

## Mathematical audit

### The weighted incidence inequality

Every plane section has size between 8 and 16. Sections of size at most 11
cannot have a four-point line, because the six-plane pencil identity would
give \(72+5\cdot4\le11+5\cdot16\), i.e. \(92\le91\). The complete planar
census therefore supplies all 70 possible spectra. I checked each spectrum's
three intrinsic identities: 30 affine lines, \(6m\) point-line incidences,
and \(\binom m2\) pair-line incidences.

For every actual candidate, the plane-spectrum, parallel-profile, and
line-pencil counts form a nonnegative integral vector \(u\) satisfying the 61
displayed incidence equations \(Mu=b\). The counts 155 planes, 31 parallel
classes, 775 lines, 31 planes and lines through a point, six planes through a
pair, and one line through a pair are all correct for \(AG(3,5)\).

I independently rebuilt the 463 sparse columns rather than importing the
target matrix routine. With denominator \(D=10^6\), all columns satisfy

\[
M^Tz\le Dq,
\]

and \(b^Tz=10082223\). Hence nonnegativity gives
\(Dq^Tu\ge b^Tz\), so \(3a_8+a_9>10\). The left side is integral, proving
the claimed lower bound 11. Five columns have zero slack; the minimum slack is
exactly zero. No floating-point optimizer result is a proof premise.

### The inherited two-eight-plane exclusion

I checked the reduction separately rather than accepting it from the target.
Two nonparallel eight-point planes give a \(5\times5\) fiber-weight matrix with
both margins \((8,16,16,16,16)\). The pencil identity correctly forces the
intersection fiber to have weight at most one and the remaining axis fibers
to have weight at most three. Passing to deficits leaves a \(4\times4\)
interior block of total seven or eight, with every row and column total at most
three.

The two different enumerators agree entry-for-entry on 4,442 labelled
matrices. The affine normalization by ordered nonparallel weight-eight lines
covers their complete normalized orbits and yields 164 representatives. The
three-hole shear normalization is valid: at least eight interior fibers have
one hole, three of their quotient points are noncollinear, and a unique affine
height function sends those holes to zero without changing the fiber weights.

For every representative I regenerated the exact CNF and matched its published
CNF hash. The formula directly imposes all 775 forbidden full lines, the bound
16 on all 155 planes, exact counts on all 25 fibers, and only the proved shear
gauge. A model would decode to the prohibited set, so UNSAT is sufficient.

Fresh CaDiCaL 1.9.5 runs produced 164 binary DRAT traces totalling 246,125,028
bytes. DRAT-trim at source commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, binary SHA-256
`9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`,
verified every trace. The stable digest of the 164 tuples
`(index, CNF hash, proof hash, proof bytes, verified)` is
`11433c59cdf3caf3101c65016ec796a51c6cb9cdf32727421669adf76b8ecf23`.

The published manifest describes 107 historical ASCII proofs and 57 binary
proofs, whereas the fresh replay emits binary proofs throughout. Fifty-six
fresh proof hashes match the manifest byte-for-byte. The remaining historical
ASCII hashes are not expected to match; one fresh valid binary trace also
differs from the historical binary trace for the same CNF. This is harmless:
all fresh traces were checked against their exact CNFs. The compact details are
recorded in [`REPRODUCTION.json`](REPRODUCTION.json).

### From eight nine-planes to a frame

The reproduced prerequisite gives \(a_8\le1\), so the weighted inequality
gives \(a_9\ge8\). Two nine-point planes cannot be parallel, since that
parallel class would contain at most \(9+9+3\cdot16=66\) points. Their normals
are therefore eight distinct points of \(PG(2,5)\).

The frame lemma is sound. In a frame-free noncollinear set, choose a triangle
\(A,B,C\). Every other point lies on a side. If \(P\in AB\setminus\{A,B\}\),
then any point outside \(AB\cup\{C\}\) creates a four-point frame among
\(A,B,C,P,Q\). Thus the set lies in the six-point line \(AB\) together with
\(C\), and has size at most seven. The independent checker verifies this
containment step for all 3,875 projective triangles and 372,000 choices of
\(P,Q\), and counts 15,500 projective frames. Hence eight normals contain the
required frame.

For three chosen frame planes, each parallel profile is necessarily
\((9,15,16,16,16)\). The displayed affine coordinate map is invertible. Every
coefficient of the fourth frame normal is nonzero, leaving exactly
\(4\cdot4\cdot5=80\) possible normalized planes. Since the three coordinate
classes contain only their three chosen nine-planes, at least five of the
eight nine-planes lie outside those classes. The resulting BBB formulation is
therefore necessary for every 72-point candidate; its stated converse is
immediate from the explicit 72-point and line-free constraints.

## Reproduction

The compact independent audit imports no target module:

```sh
cd affine_line_free_f5_3/nine_plane_frame72_review2
python3 independent_check.py > actual.json
diff -u EXPECTED.json actual.json
sha256sum -c SHA256SUMS
```

The target replay was run in normal and optimized modes; outputs were
byte-identical with SHA-256
`c3b1ec1ae151c08fe2a550df161e3a287e81890aa83d6c32d6f26238d6a7fd21`.
The prerequisite reduction was replayed in normal and address/undefined
sanitizer modes; outputs were byte-identical with SHA-256
`28777a3ea719a3b2775aaf03b2ed9d6b751de8adb5da4b5b297ef528096dd146`.
The full proof replay used CPython 3.11.2, Python-SAT 1.9.dev15, CaDiCaL
1.9.5, GCC 12.2.0, and the DRAT-trim binary identified above.

The generated CNFs, DRAT traces, logs, binaries, and build directories remain
outside Git. They occupy hundreds of megabytes and are reproducible from the
published source; only the compact summary and checker are committed here.

## Proof, checker guarantees, and trust boundary

The written incidence reduction, exact dual certificate, projective frame
argument, and coordinate normalization prove the primary theorem once the
two-eight-plane prerequisite is accepted. The complete quotient enumeration,
CNF reduction, and all 164 checked DRAT proofs establish that prerequisite.

The compact independent checker guarantees the certificate arithmetic,
spectrum incidence identities, and finite projective-frame audit. The full
replay additionally guarantees UNSAT of the 164 generated CNFs. Remaining
trust lies in the written reductions, the two ordinary enumerators, Python-SAT's
cardinality encoding, CaDiCaL proof production, DRAT-trim, the compiler/runtime,
and the semantic correspondence between the CNFs and point sets. No proof
assistant formalizes these bridges.

## Literature and novelty

Elsholtz et al., *Maximal line-free sets in \(\mathbb F_p^n\)*,
[arXiv:2310.03382v2](https://arxiv.org/abs/2310.03382v2), supplies the known
70-point construction and the previously published 70--73 interval. Targeted
searches found no primary source containing the weighted inequality, the
two-eight-plane exclusion, or this nine-plane-frame normal form. These results
are therefore potentially novel relative to the searched literature and the
committed graph, but this is not a priority determination.

## Strengthening and improvement opportunities

1. **Exploit the whole eight-normal configuration.** The next high-impact step
   is to classify the `PGL(3,5)` orbits of admissible sets of at least eight
   nine-plane normals, not merely choose one frame. Feeding their line
   incidences into the point-level formulation could split the single BBB case
   into a small number of substantially tighter exact cases.
2. **Add cross-pencil compatibility to the dual system.** The 61 aggregate
   equations forget how low planes from different pencils intersect. Variables
   for pairs of planes, indexed by normal incidence and intersection-line
   weight, could yield a stronger integer dual certificate or a smaller SAT
   handoff. This requires a complete pair-type list and consistency equations;
   feasibility of the current relaxation alone cannot provide the upgrade.
3. **Stabilize proof-replay provenance.** Have `replay.py` emit a canonical
   timing-free aggregate digest and either publish a reference binary-proof
   manifest or explicitly mark the historical ASCII/binary split. Fresh valid
   proofs need not be byte-identical, but the current mixed manifest makes that
   distinction easy to misread.
4. **Reduce the cardinality-encoding trust boundary.** Add an independent
   semantic checker for the sequential-counter clauses, or generate a proof of
   equivalence between each geometric cardinality constraint and its CNF. DRAT
   proves the generated CNFs UNSAT, not by itself that every intended point set
   is encoded.

## Publication readiness

The theorem and its prerequisite are ready to circulate as independently
reproduced computer-assisted results, with the stated software and reduction
trust boundaries. They materially narrow the 72-point branch but must not be
reported as an exact determination of \(r_5(\mathbb F_5^3)\).
