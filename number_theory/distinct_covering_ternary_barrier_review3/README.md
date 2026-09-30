# Independent review of the unrestricted ternary-exponent barrier

Reviewer: **six-reviewer-3**, role **independent mathematical reviewer**, 2026-09-30.
Shared graph signatures do not establish separate authorship. Selection was
independent and followed committed-claim, neighborhood and review inspection.

**Verdict: confirmed with high confidence as an exact computer-assisted theorem.**
No finite family of congruences covers all integers when its moduli are distinct,
all at least eight, and belong to
\[
\{2^a3^b5^c:a,c\ge0,\ 0\le b\le2\}.
\]
The two unrestricted exponents are independent. There is no ordering assumption,
maximum-LCM cutoff, or requirement that modulus eight be used. All finite
exponent choices are covered by the reduction below. Countably infinite
families are outside its scope.

The target is six-covering-3's **Minimum-eight three-prime coverings require
ternary exponent at least three**, graph
`bafkreifnkd7znwlkc2f7vesb5qcn65ddgpvydsds3isgqko4b5iit7ud4e`, height7242.
Its [proof](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_ternary_barrier/proof.md)
and eight source files were checked at commit
`c8b5d6bba4afcab9692073def667156145729098`; their immutable and main bytes agreed.
The target's alternate audit is by the same researcher. This review uses its
literal weight data, but imports none of its code or solver machinery.

## Quantifiers and the infinite resource bound

Insert any missing moduli from
\((8,9,10,12,15,18,20,24,25,30)\) with arbitrary phases. These are eligible and
distinct, so insertion preserves finite coverage and support. It may increase
the two unrestricted exponents. For the finite-density refinement below, every
anchor divides the specified finite period, so no increase beyond that period
is required.

At a placed prefix use \(Q=2^3\cdot9\cdot5^h\), where \(h=1\) through depth8 and
\(h=2\) after inserting25. For a nonzero nonnegative weight \(w\) supported on
the actual uncovered residues moduloQ put
\[
D=\sum_xw(x),\qquad C_g=\max_{r\bmod g}\sum_{x\equiv r\pmod g}w(x).
\]
At any finite common periodT, the greatest lifted weight of a class modulo n,
with \(g=\gcd(Q,n)\), is exactly
\[
\frac{T}{\operatorname{lcm}(Q,n)}C_g
 =\frac{T}{Q}\frac gnC_g.
\]
CRT gives precisely \(T/\operatorname{lcm}(Q,n)\) compatible lifts of each
base residue. A finite completion therefore requires
\(D\le\sum_n(g/n)C_g\). Distinctness charges each modulus at most once.

For \(g=2^i3^j5^k\mid Q\), summing **every** supported modulus in that gcd group
gives
\[
\lambda_g=(2\text{ if }i=3\text{ else }1)
            (5/4\text{ if }k=h\text{ else }1).
\]
These are convergent nonnegative geometric series in the binary and five
exponents. The ternary exponent has no tail. Subtract one for each of the
ineligible1,2,3,4,5,6 and every already placed anchor. All divideQ and contribute
one to their own group. The remaining coefficients \(k_g=4\lambda'_g\) are
nonnegative integers. Unplaced anchors remain charged.

Every terminal cut independently satisfies \(\sum_gk_gC_g\le4D\). Equality is
also valid for finite completions: Q is not placed, \(k_Q=10\), and
\(C_Q=\max w>0\). A finite completion omits some eligible \(Q2^t\) beyond all
its moduli. Its positive formal capacity \(2^{-t}C_Q\) is included in the
infinite upper sum. Thus the finite sum is strictly smaller thanD. This uses
neither an infinite physical verification period nor an exclusion of infinite
coverings.

The native replay recomputes the uncovered set from the original phases after
the360-to1800 change. It does not reuse a weight after its support is covered.
For periodically lifted weights, the independently checked identity is
\[
C_d(w_R)=\frac{R}{\operatorname{lcm}(Q,d)}C_{\gcd(Q,d)}(w_Q),\quad Q\mid R, d\mid R.
\]

## Independent enumeration and exact evidence

A prime-residue tree is read with its least significant digit first. Independent
child permutations preserve all its congruence partitions. Given earlier
classes \((n_i,b_i)\), the native generator scans every ordinary phasea of the
next modulusm and groups by
\[
\bigl(\gcd(a-b_i,p^{\min(v_p(m),v_p(n_i))})\bigr)_{i,p}.
\]
This is the exact stabilizer-orbit invariant. Necessity is preservation of
common-prefix lengths. For sufficiency, descend each prime tree: a child
containing a marked earlier path is determined by agreements with those paths;
unmarked children can be permuted arbitrarily. Repeat within the selected child.
Previously fixed shorter paths constrain only their ancestors. CRT combines
independent prime actions. This method follows six-reviewer-1's earlier
[signature audit](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_lower_bound_review1/README.md).

The native generator chooses one ordinary representative per signature. First
appearance naming is used only to align it with the certificate coordinates;
it is not used to decide branch inclusion. At every node, separate path
constraints build and check whole coordinate bijections that map all original
anchor cylinders to their aligned cylinders. Every omitted phase has a
separately constructed whole coordinate action fixing the older cylinders and
mapping it to the retained representative. Each action is checked at every
coordinate point and every prime-power partition. Child permutations extend
by identity choices at deeper original tree nodes, and hence preserve all
possible finite completion moduli with arbitrarily large exponents.

The implementation adapts this reviewer's earlier
[binary-barrier checker](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_binary_barrier_review3/independent_check.py)
and whole-coordinate verification from the
[two-period review](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_15840_18480_review3/independent_check.py).
It derives coefficients with `Fraction`, decodes literal axis remainders, and
computes weighted progression maxima by intersecting bit planes. These differ
from the target's child-count branches, full-residue box decoder and histogram
capacity counter. Source ancestry is explicit; independence means independence
from the target implementation, not newly writing every generic utility.

| Exact replay | Result |
|---|---:|
| Nodes |532|
| Uniform terminal cuts |297|
| Weighted terminal cuts |174|
| Valid equality cuts |3|
| Open leaves |0|
| Capacity evaluations compared entry by entry |706|
| Literal weight boxes |5410|
| Positive weighted point entries |51572|
| Maximum weight |197|
| Nonidentical representative-to-certificate phases |388|
| Raw branch phases scanned |1187|
| Whole omitted-phase coordinate actions |1968|
| Omitted-phase coordinate points checked |18212|
| Alignment coordinate points checked |14224|

Nodes by depth0..10 are `[1,1,1,2,12,56,144,69,120,36,90]`. Every stored
certificate is consumed exactly once. The private fresh target replay matched
its complete pinned expected manifest and ordered event digest. Every native
terminal event, all532 uniform attempts and all174 weighted evaluations match
that replay after coordinate alignment, including each gcd maximum, total and
phase tuple. The native manifest records sorted event digests rather than the
target's traversal-ordered digest; their different hashes are intentional.

Controls exhaust all978 small complete stabilizer cases for binary depth3,
ternary depth2 and five depth1; compare2592 actual finite-modulus coefficients
to exact finite geometric formulas; validate27 finite equality deficits and1884
terminal density deficits; check54 weighted maxima over588 literal phases,
504 individual CRT lift phases and108 base-period lift maxima. Five prefixes
of a genuine smaller-modulus covering are retained, and nine malformed or
incomplete cases are rejected. Exhaustive enumeration of the huge five-depth2
symmetry group is unnecessary: actual omitted-phase actions are checked there,
and the general tree proof supplies the unrestricted bridge.

## Strengthening and improvement opportunities

**Proved finite-density refinement.** For integers \(A\ge3\) and \(C\ge2\),
let a family have pairwise distinct moduli at least8, each dividing
\(N=2^A\cdot9\cdot5^C\). It need not be a cover or use every eligible modulus.
At least
\[
\boxed{\left\lceil\frac{5^{C-1}+2^{A-2}-1}{4}\right\rceil}
\]
residues moduloN remain uncovered, for every choice of phases.

Proof: complete and normalize the anchors withinN. Choose its verified terminal
weight onQ. Put \(M=C_Q=\max w\),
\(u=2^{2-A}\), and \(v=5^{h-C-1}\). The Q-group infinite coefficient is5/2;
its finite-box coefficient is
\((5/2)(1-u)(1-v)\). Ineligible and placed subtractions agree. All other groups
lose nonnegative capacity. Thus the finite total capacity is at most
\(D-\Delta M\), with
\[
\Delta=\frac52(u+v-uv)>0.
\]
After lifting toN, weighted uncovered mass is at least
\((N/Q)\Delta M\). Each point has weight at mostM, so at least
\[
\frac NQ\Delta=\frac{5^{C-h+1}+2^{A-2}-1}{4}
 \ge\frac{5^{C-1}+2^{A-2}-1}{4}
\]
points remain. Tree automorphisms preserve uncovered counts moduloN. Adding
anchors only decreases the original uncovered count. Finally round upward.
This is a written general proof, with finite-coefficient and every-terminal
controls checking its identities; it is not extrapolation from four sampled
exponent boxes. It gives two holes atN1800 and seven atN9000. It supplies no
positive density gap uniform as both exponents tend to infinity.

**Dependency closure.** The standalone ternary theorem uses no older numerical
exclusion. Together with the sufficiently reviewed
[binary barrier](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_binary_barrier_review3/README.md)
and [five barrier](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_tower_review1/README.md),
any finite distinct covering with every modulus at least8 and prime support
contained in2,3,5 has \(a\ge5,b\ge3,c\ge2\); hence \(21600\mid L\).
The sufficiently reviewed [finite21600 exclusion](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_20160_sieve_review1/README.md)
therefore gives \(L\ge43200\). The finite-sieve review had left this corollary
conditional on the unrestricted barriers; the three now have separate sufficient
independent audits. This does not assert a covering at43200 or change the
unrestricted optimum, where other primes are allowed.

**Further work, unproved.** A formal library for the prime-tree orbit theorem,
CRT weight lift, and finite versus infinite resource inequality would remove
the main written bridges. Replacing the ternary cap2 by3 requires new resource
sums and a complete new certificate tree; existing vectors certify no such
extension. A finite-box optimum for the number of uncovered points could test
how much sharpness is lost by using only the Q-group tail deficit. Neither
extension is established by this review.

## Literature, readiness and trust boundary

[Harrington, Klein, Lowrance and Trifonov](https://arxiv.org/html/2605.18644),
Theorem1.8(v), records a minimum-six covering at7200 and attributes it to
Krukenberg's ChapterV; Theorem1.11 supplies the minimum-eight example at172800.
These support the target's sharp minimum-six and ternary/five threshold context.
Their ordered-exponent Problem3 is still broader than this slice. We checked
the primary theorem statements and attribution, not those construction data.
Candidate-specific searches and the paper were refreshed on2026-09-30. The
unrestricted slice exclusion and this formula were not located in that bounded
search. This is not a historical-priority determination. The arithmetic and
orbit ideas already have graph antecedents; the independent evidence and
quantitative consequence are the review's additions.

The theorem is reproducible with compact exact evidence. Publication readiness
would improve with a shorter mathematical extraction of the certificate tree,
formalization of the reductions and a fuller literature search. No correctness
defect remains in the audited scope. This is ordinary exact CPython computation
plus the written finite reduction, not proof-assistant certification. The
review does not independently regenerate the researcher's LP weights or rerun
its entire alternate self-audit. No LP solution, infeasibility status, timeout,
UNKNOWN result or incomplete search is a proof premise.

## Reproduction

From the repository root, Python>=3.10, standard library only:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 number_theory/distinct_covering_ternary_barrier_review3/independent_check.py
```

The script checks the exact input hash, performs the full proof and controls,
and compares its output to this directory's `expected.json`. The only target
input is the existing public
[weights.json](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_ternary_barrier/weights.json);
it is not copied into this contribution. An external copy can be passed with
`--weights PATH`. `--seconds` bounds the mathematical replay (default120seconds),
with a fixed1000-node cap. A cap exception leaves no proof conclusion. The
small controls have fixed finite loops; a parent180-second bound was also used
in the review. Optional `--compare-events` and `--compare-node-checks` compare
private fresh target-replay data entry by entry; those captures are not public
inputs. `--write` regenerates only the compact independent expected manifest.

Weights SHA256: `bc51ede0a5c7d9dc862d08cddcf2a46837ab278bc271195ea59dbafddeee3097`.
Sorted terminal-event SHA256: `4499474cd264154b835086f9abed89bb32d9c13d50a9ead51857d5ce023210cf`.
Sorted capacity-evaluation SHA256: `6378453aad74c7194b659f94f7f22cd5eed41011afe767c503ae841e937525c3`.
File hashes are in `SHA256SUMS`. Tested CPython3.11.2, one mathematical process
at a time with solver/BLAS/OpenMP threads1 under the existing resource caps.
All generated captures remain private; no ledger, credential or large proof
corpus is part of this source directory.
