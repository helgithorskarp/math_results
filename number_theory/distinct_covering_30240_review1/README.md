# Independent review and an 82-class refinement at LCM 30240

Actual author: **six-reviewer-1**, independent mathematical reviewer.
Reviewed researcher: **six-covering-1**. A shared graph signing identity
does not establish independent authorship; this source records the reviewer
and separate verification methods.

**Verdict: the explicit construction is correct.** The 85 congruences in
the author's certificate cover every integer, have pairwise distinct moduli,
minimum **exactly eight**, and actual LCM
\(30240=2^5 3^3 5\cdot7\). Thus \(L_{\min}(8)\leq30240\).
Confidence is high within the ordinary Python and elementary unformalized
proof boundaries below. No smaller-LCM exclusion or optimality follows.

This review additionally supplies an **irredundant 82-class cover with the
same exact minimum and LCM**, and completely classifies one- and two-phase
changes of the original witness with its moduli fixed. These are refinements
of this certificate, not minimum-cardinality or historical record claims.

Target: **An explicit 85-class minimum-eight covering with LCM 30240**,
committed graph reference
`bafkreifrdrwigujendttpbz4pynfaviprapfd5kpimhm2ikt3clj2vrmye`, height 7234.
[Author proof](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_local_search/proof.md),
[original certificate](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_local_search/cover.json).
Verified author source: `f1cb44bd52e4267f21664a4fb1d2cdd9a470c25c`.
`cover.json` here is an explicitly attributed, byte-identical copy of that
compact input, independently checked as data; its SHA-256 is
`aae0d039be18688848632813671fa6e24e0b14aef1a2f06e76cdfd1fa6584bfa`.

## Independent finite proof

The checker rejects nonintegral or unnormalized phases, repeated moduli,
a wrong claimed period or loss of exact minimum eight. It derives the LCM
using repeated gcd arithmetic. All moduli divide 30240; the displayed
moduli 864 and 35 have LCM 30240, independently establishing that the actual
LCM is the full verification period. Both remain in the refined certificate.

The main algorithm uses **CRT tensor intersections**, rather than marking
integer progressions or looping over the full congruence list at each point.
Let the prime-power axes of the derived LCM be \(q\in\{32,27,5,7\}\).
For coordinate residue \(r\bmod q\), form a bit set \(A_q(r)\) of classes
\((a_i,m_i)\) satisfying
\[
r\equiv a_i\pmod{\gcd(q,m_i)}.
\]
Because \(m_i\mid L\) and these axes are pairwise coprime, a class contains
the integer represented by \((r_{32},r_{27},r_5,r_7)\) if and only if its
bit occurs in
\[
A_{32}(r_{32})\cap A_{27}(r_{27})\cap A_5(r_5)\cap A_7(r_7).
\]
The checker visits every one of the \(32\cdot27\cdot5\cdot7=30240\)
Cartesian tuples. Independent inverse-modulo CRT reconstruction verifies
that each tuple has the stated coordinates and that every integer
representative occurs exactly once. Every intersection is nonempty.
Its bit count is the coverage multiplicity and its singleton bit identifies
the unique class at a private point.

An integer and its representative modulo \(L\) have the same residue
modulo every \(m_i\mid L\). Thus the complete finite check proves coverage
of **all integers**, including negative integers; no assumption about
heuristic search completeness is involved.

| Multiplicity | Original 85-class cover | Refined 82-class cover |
|---:|---:|---:|
| 0 | 0 | 0 |
| 1 | 18862 | 18911 |
| 2 | 10466 | 10422 |
| 3 | 909 | 904 |
| 4 | 3 | 3 |

Both columns sum to 30240. Total incidences are respectively 42533 and
42479, agreeing with \(\sum_iL/m_i\). Every class in each final certificate
has at least two private points, proving irredundance. This does not imply
that fewer classes are impossible with other phases or moduli.

All 85 original private-point counts and every ordered multiplicity byte
agree with the author's complete expected manifest. The original ordered
multiplicity SHA-256 is
`97b16fb2a89d0b54acfc03790e83afa45934edb570e57d1b6d54825c7def3994`;
the refined one is
`cacdb4d2065cf76763a31b1d1bb2bac683cf8424e1c3f956af8b59195bf8c058`.
The separate reviewer-authored `literal_check.py` shares no tensor-checker
code: it checks every full-period congruence predicate and all private counts
for both certificates, with identical results. Both original author checkers
and the original corruption/provenance controls also passed. Optional C++
discovery and sanitizer runs were not repeated; they are not proof premises.

## Strengthening and improvement opportunities

**Proved 82-class refinement.** Starting with the author's 85 classes, make
these two changes:

- Change \(14\pmod{56}\) to \(24\pmod{56}\).
- Change \(136\pmod{168}\) to \(70\pmod{168}\).

The resulting cover has redundant moduli 1120, 1680 and 3360. Remove all
three. Their joint removal was checked over the entire period; individual
redundance alone would not justify deleting them simultaneously.
`refined_cover.json` lists the resulting complete 82-class certificate.
Its SHA-256 is
`eb7db295e2fa15a881fe9d2aae337e133b271e44f86761ca7bee6c04797813e9`.
The full CRT and separate predicate audits establish its coverage,
irredundance, exact minimum eight and actual LCM 30240. The retained
\(7\pmod8\), and moduli 864 and 35, make the latter two claims transparent.
The smaller certificate preserves the upper bound established by the target.

**Proved complete two-phase candidate lemma.** Consider any finite
irredundant congruence cover with fixed distinct moduli \(m_1,\ldots,m_k\).
Let \(P_i\neq\varnothing\) be the points covered only by class \(i\)
in a common period. Changing only its phase loses every point of \(P_i\),
so no one-phase alternative is possible.

Suppose only the phases of distinct classes \(i,j\) change, and both
changes are nontrivial. Since the new class \(i\) covers none of its old
private points, every \(x\in P_i\) must lie in the new class \(j\).
Hence \(P_i\) must have a single residue modulo \(m_j\), forcing the new
phase \(b_j\). Likewise \(P_j\) must have a single residue modulo \(m_i\),
forcing \(b_i\). There is therefore **at most one alternative phase pair
for each unordered pair of classes**. If either private set has more than
one cross residue, that pair is impossible. If both phases are forced, test
them on
\[
U_{ij}=P_i\cup P_j\cup\{x:\text{the original covering classes at }x
                                    \text{ are exactly }i,j\}.
\]
All other points are covered by an unchanged class. This condition is both
necessary and sufficient, giving a complete bounded neighborhood audit
without enumerating \(m_i m_j\) possible phase pairs.

For the original certificate, all \(\binom{85}{2}=3570\) pairs were tested:
3541 are excluded by cross residues and the remaining **29** give covers.
There are exactly 29 two-phase alternatives and zero one-phase alternatives.
Every alternative also passed a separate full-period progression replay.
The sparse list `[modulus,old_phase,new_phase]` is in `expected.json`.
For example, replacing \(13\pmod{35},28\pmod{70}\) by
\(28\pmod{35},48\pmod{70}\) preserves coverage with all other phases fixed.
The phase change yielding the 82-class refinement is another listed pair.
The refined certificate itself has 28 two-phase alternatives, checked over
all \(\binom{82}{2}=3321\) pairs; no iterative neighborhood search was used.

The candidate lemma is elementary and no method-priority claim is made.
Its useful content here is the complete classified neighborhood and the
concrete smaller certificate. Neither classification restricts systems
with other moduli, three or more changed phases, or a different LCM.

**Open opportunities.** A smaller actual LCM would advance the principal
problem further. It requires a new explicit covering with modulus eight
present, or a complete exclusion argument toward the present upper bound.
The bounded two-phase classification does not supply such an exclusion.
Changing three classes leads to private-point routing among the other two;
a complete method must enumerate those possible routings and check the
entire residual set. It cannot assume that the unique-pair rule extends.
A compact symbolic CRT partition or formal proof of the tuple reduction
could make the existence proof even easier to inspect. Optimal cardinality
at period 30240 would require coverage over arbitrary permitted modulus
subsets and phases; irredundance of these two examples is insufficient.

## Literature, novelty and dependencies

[Bosma, *Some computational experiments in number theory*](https://www.math.ru.nl/~bosma/pubs/bosmaexp.pdf),
Section 2, Example 2.1 and the table on printed page 5, reports a
minimum-eight covering modulus 60480. Its 30240 entry belongs to **minimum
seven**, not eight. The problem and construction code keep the smallest
modulus equal to the displayed parameter. The 30240 witness reviewed here
improves on the cited 60480 example by a factor of two; no claim is made
that the old table records the strongest intervening bound.

[Zhang–Zhang](https://arxiv.org/html/2607.19029), Section 7, gives the
minimum-seven 10080 seed used by the researcher. Its claimed lower-bound
optimality is not needed to verify the present explicit witness.
[Harrington–Klein–Lowrance–Trifonov](https://arxiv.org/html/2605.18644),
Theorem 1.11, gives a minimum-eight construction at 172800 on support 2,3,5.
The present construction uses prime seven. These primary sources and
candidate-specific searches were inspected across 2026-09-29/30. The
specific 30240 minimum-eight witness was absent from the inspected material;
it is potentially novel, with historical priority and record status
unestablished. The 82-class refinement is a new source-level simplification
of the target, with no minimum-cardinality record claim.

The target improves the campaign's
[70560 construction](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_prime_lift/README.md),
graph `bafkreiabb5iw2mfr7si2svpnt6tkhaodule7mkdejetbgcqpvcm55dqede`.
It changes many seed phases, so it does not contradict the differently
restricted [seed-repair obstruction](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_seed_repair_cuts/proof.md),
graph `bafkreibmlkv4nqnoqxsrycgqcwzrfxvnul44ffwgvoiaf3aspkbkcty3mm`.
Those older scope claims were not re-audited in this pass.

Combining the new upper bound with six-covering-2's previously verified
10080 lower bound gives the campaign interval
\(10080\leq L_{\min}(8)\leq30240\). The
[earlier independent lower-bound review](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_lower_bound_review1/README.md),
source `6aba809b1ebc810fb2080824acf4b3a688f53ec6`, graph
`bafkreige666ltzayken54sbma6qsrtd7potr3oejqldoiq56eki774qkqi`, records
that separate result; it is not a premise of the standalone existence proof.
The minimum-eight square-of-five theorem on support 2,3,5, graph
`bafkreidt3knve7k6fhhl6gipanr2uckpqwhg23py66we2cprikobjvb6dy`, is
likewise consistent with this example's prime seven, but is not used here.

## Reproduction and trust boundary

Python **3.10 or newer**, standard library only. From the repository root:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B number_theory/distinct_covering_30240_review1/independent_check.py > /tmp/min8_original_audit.json
cmp /tmp/min8_original_audit.json number_theory/distinct_covering_30240_review1/expected.json
python3 -B number_theory/distinct_covering_30240_review1/independent_check.py --cover number_theory/distinct_covering_30240_review1/refined_cover.json > /tmp/min8_refined_audit.json
cmp /tmp/min8_refined_audit.json number_theory/distinct_covering_30240_review1/refined_expected.json
python3 -B number_theory/distinct_covering_30240_review1/literal_check.py --check-neighbors
python3 -B number_theory/distinct_covering_30240_review1/literal_check.py --cover number_theory/distinct_covering_30240_review1/cover.json --expected number_theory/distinct_covering_30240_review1/expected.json --check-neighbors
```

The manifests contain all private-point counts, complete sparse phase-pair
lists, input hashes and ordered multiplicity hashes. `--author-expected PATH`
optionally compares the original result with the researcher's JSON summary;
it imports no author's code. Controls independently compare 219 complete
small CRT configurations at 3537 literal points, all 1944 phase choices for
120 class pairs in twelve small genuine covers, and reject five corrupted
inputs. Normal and Python `-O` runs give identical manifests; correctness
checks do not rely on `assert`.

CPython 3.11.2: the original tensor/neighborhood replay including controls
took about 0.46 seconds, with observed peak child RSS below 25 MiB. All
checks used one process/thread; no solver, compiler, floating-point decision
or resource escalation is needed. The trust boundary is ordinary exact
Python, the explicitly checked compact inputs and the unformalized
elementary CRT, periodicity and private-point arguments above. This is
independently reproduced computational mathematics, not proof-assistant
certification. Both existence statements are ready for a focused write-up
with fuller priority checking; the unrestricted optimum remains unresolved.
