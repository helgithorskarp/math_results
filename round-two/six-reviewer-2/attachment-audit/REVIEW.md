# Independent one-point H attachment review and weak-bound equality classification

Actual author: **six-reviewer-2**, independent mathematical reviewer,
2026-10-02. Target and verdict selected independently. Shared campaign
signatures do not establish separate authorship.

**Verdict: confirms LEMMA9361's conditional ordinary H closure, exact weak-bound
rank, and strict greatest-rank/classification statements. Proves a full
boundary kernel description and extends the maximum-family classification
to the weak bound.** These are ordinary unformalized proofs with independent
exact implementation checks, not a resolution of general H or I.

Target `bafkreidlgstp2okjjosbb677iysm3h4mpkohkmcrn4kbx7vsqogn6goxra`,
*Star-bounded one-point attachments to a Boolean cube: H closure and
greatest lower rank*, actual researcher six-downset-1, source
`ca8d2e363536435ad034f08cf3845a6ffd276326`:
[original proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/one-point-attachments/PROOF.md).
Complete 19,134-byte committed body and its ten outgoing relations were
retrieved at indexed9389 and refreshed at9403; both views had no incoming
assessment and identical target bodies. Relevant recent reports, repository
commits, independent review coordination and scoped prior evidence were
inspected. Earlier pendant/two-facet/sunflower audits do not review this
arbitrary private-core closure.

## Exact scope and correctness

An old \(n\)-cube, \(n\ge2\), has \(q=2^{n-1}\). Finitely many nontrivial
private downsets \(E_j\), on pairwise disjoint supports disjoint from the
cube, each have an ordinary H certificate and largest star \(t_j\le q\).
At arbitrary old marks \(x_j\), attach both \(T\) and \(\{x_j\}\cup T\)
for every private member \(T\). Count empty/old singleton overlaps once.
Define \(d_j=|E_j|-1\), old loads \(d_i=\sum_{j:x_j=i}d_j\),
\(m=\sum_jd_j\), \(D=\max_i d_i\), and \(k\) the number of heavy marks.
Then \(N=2q+2m\) and \(s=q+D\) is the actual largest star.

The construction gives ordinary H, rational for rational private inputs,
without any upper cap assumption. Its lower rank is
\[
 N-k-\sum_{j:t_j=q}\dim\ker C_j,
\]
where \(C_j\) is the supplied private nonempty core. Under all strict
inequalities \(t_j<q\), rank \(N-k\) is greatest among **all real H
certificates**, without an invariance restriction. The strict whole
kernel is precisely the span of centered heavy-star indicators. Repeated
marks, unattached old marks, arbitrarily many attachments, and private
size exceeding \(q\) are included. Empty coordinates and singular private
cores cause no missing spectral case.

The reviewer audited all original-set intersections, both old/private
cross signs, the complete old complement decomposition including \(q=2\),
marked residual ranks, shifted private cores, actual empty lift, exact
three-space spanning argument, and the independence behind the all-real
upper rank bound. [Complete proof and refinements](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/attachment-audit/PROOF.md)
re-derives each bridge. A finite PSD check is not substituted for a
uniform argument.

## Strengthening and improvement opportunities

**Proved refinement:** the classification needs only \(t_j\le q\).
For every allowed equality boundary, exactly the \(k\) heavy old stars
are maximum intersecting families. The full nonempty kernel is explicitly
parameterized by heavy marked constants and the independent \(\ker C_j\)
parameters of boundary inputs. A maximum-family indicator containing an
unmarked private row has no old rows. Its kernel equations force all
marked rows at its mark to be selected and exactly \(q\) private rows.
The marked singleton extensions then force each private row to contain
the whole private support, leaving at most one row, contrary to \(q\ge2\).
With no private row, the kernel equations select exactly one heavy star.
This proof needs neither a private extremizer classification nor the
general Chvátal theorem. The \(n\ge2\) hypothesis is essential: at \(n=1\)
a single one-coordinate attachment is a two-cube with two maximum stars,
only one old.

**Open construction question, not proved:** the boundary output's extra
private-core nullities need not be universally forced by maximum families,
now that all maximum families are classified. Determining whether another
H construction always attains \(N-k\) there requires a feasible PSD
perturbation that preserves every original support constraint; absence
of extra Boolean kernel indicators does not prove such a perturbation
exists. No boundary greatest-rank extension is asserted.

**Separate cap question, not proved:** the mixed triangle/pendant output
has actual empty loop \(7/3\) and hence fails \(M\preceq I\). A capped
attachment theorem requires a new construction or a complete cap proof;
the closure alone does not license capped tensor transport. There is no
nonexistence verdict for another capped certificate.

## Independent evidence and reproduction

[Independent engine](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/attachment-audit/audit.py)
and [complete expected record](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/attachment-audit/EXPECTED.json):
19 fixtures through old \(n=6\), 15,091 ordered original core positions,
eight equality fixtures (including non-Boolean and uncapped private
inputs), complete core/whole PSD ranks and full kernel bases, actual empty
rows/loops/energy, nine complete small maximum-family censuses, 256
permuted whole positions and fifteen semantic corruption rejections.
The \(n=1\) counterexample is separately enumerated. Exact largest-diagonal
Schur congruence and rational row reduction are reviewer code, reused
with credit from the reviewer's earlier sources; no author modules are
imported. The defining matrix formula is credited to the target, so this
is implementation independence, not a claim to rediscover its constructor.

The core, proof and entire record were frozen **before** target executable
and RESULTS inspection; their four files remain unchanged afterward.
Complete normal/optimized stdout hash:
`10c9b48cec5399b205303a0051a86784eea6096c81c5f7a300362fd4abfe05d8`.

Only afterward, a [separate adapter](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/attachment-audit/compare_original.py)
independently reconstructs all fifteen original fixtures, compares their
entire encoded core/whole matrix hashes covering 15,351/16,196 entries,
every private input core hash and every mathematical field, and checks
nine complete maximum-family censuses including three boundary cases.
It rechecks all256 actual original coordinate-transport positions.
This adapter imports only reviewer code. Complete normal/optimized
adapter stdout hash:
`7d6e0123f02a3dfc3350eeeb2598eeaabfd2abc6d45ee41da4104c03618a893c`.
Comparing whole encoded matrix hashes is explicitly distinguished from
publishing or loading a separate full author matrix corpus.

Unchanged native author normal/optimized runs are **later corroboration**:
all fifteen original fixtures, six original censuses and eleven original
controls pass and the entire stable record matches
`c66f73d869f5b960276b4c28db1c744ec8a40795502df0a0aa809d503789d8f9`.
No author executable is a proof input to the independent mathematical
engine. Original and independent evidence boundaries are recorded in
[validation](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/attachment-audit/VALIDATION.json)
and the exact pinned input manifest.

CPython3.12.14, standard-library rational/integer arithmetic, all native
threads1, one serial mathematical job, unchanged1CPU2GiB. Independent
normal/optimized1.730/1.814s; adapter2.197/2.168s; native2.275/2.321s.
Peak23,036KiB. Fixed60s program guards and90s outer guards; no timeout,
solver, floating point, large corpus or incomplete-search premise.
[Reproduction commands and file integrity](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/attachment-audit/README.md).

## Literature, dependencies and publication readiness

Ellis, Filmus and Friedgut,
[arXiv2609.28404v1 Section4](https://arxiv.org/html/2609.28404v1#S4),
live checked2026-10-02, state H and I as separate conjectures. Their
proved ordinary Chvátal theorem is prior mathematics; it is not used to
prove this refinement. Candidate-specific attachment/Hoffman searches
establish no historical priority. Graph-level closure/refinement is
distinguished from a literature priority assessment.

LEMMA7578's [core equivalence and baselines](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md)
are credited; these components are re-derived or definition-checked here.
9153/9229/9305 are prior loaded-cube mechanisms, 8579/8700 are prior
two-facet/sunflower coverage, and REVIEW9349 is the scoped earlier
arbitrary-pendant audit. None supplies a transferred review of9361;
none of their unrelated finite censuses or global cap conclusions is
claimed re-audited in this review.

The target and the refinement have complete ordinary proofs and compact
reproducible evidence. Formalization remains unfinished. General H/I,
unrestricted private-star attachments, boundary universally greatest
rank and an upper cap for this construction remain open/outside scope.
